"""Upgrade concept pages into evidence-grounded local overview pages."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
CONCEPTS_DIR = vault_path("wiki", "concepts")

SEMINAL_SLUGS = {
    "chi2024diffusion": 100,
    "zhao2023finegrained": 95,
    "fu2024mobile": 90,
    "brohan2023rt2": 88,
    "team2024octo": 86,
    "kim2024openvla": 84,
    "collaboration2025open": 82,
    "zhu2024scaling": 80,
}


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    summary: str
    year: str
    venue: str
    status: str
    tags: list[str]
    structured: dict[str, str]


def section(text: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", text, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^|\]#]+)", text)


def parse_structured(body: str) -> dict[str, str]:
    structured = {}
    for line in section(body, "## 结构化提取").splitlines():
        if not line.strip().startswith("-") or ":" not in line:
            continue
        name, value = line.split(":", 1)
        key = name.lstrip("-").strip().strip("*").strip()
        structured[key] = value.strip()
    return structured


def load_topics() -> dict[str, Topic]:
    topics = {}
    for path in sorted(TOPICS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(text)
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        body = parsed[1]
        topics[path.stem] = Topic(
            slug=path.stem,
            title=fields.get("title", path.stem).strip('"'),
            summary=fields.get("summary", "").strip('"'),
            year=fields.get("year", "").strip('"'),
            venue=fields.get("venue", "").strip('"'),
            status=fields.get("status", "").strip('"'),
            tags=parse_list_value(fields.get("tags", "")),
            structured=parse_structured(body),
        )
    return topics


def concept_entries(schema: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    entries = {}
    for tag, info in schema["literature"]["tag_taxonomy"].items():
        concept = info.get("concept")
        if concept:
            entries[concept] = (tag, info)
    return entries


def concept_page_papers(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [link for link in wikilinks(section(text, "## Related Papers")) if (TOPICS_DIR / f"{link}.md").exists()]


def score_topic(topic: Topic, concept_tag: str) -> tuple[int, int, str]:
    year = int(topic.year) if topic.year.isdigit() else 0
    score = SEMINAL_SLUGS.get(topic.slug, 0)
    if topic.status == "done":
        score += 20
    if concept_tag in topic.tags:
        score += 15
    if topic.structured.get("Metrics") and topic.structured.get("Metrics") not in {"-", "N/A"}:
        score += 5
    return score, year, topic.slug


def select_key_topics(topics: list[Topic], concept_tag: str, limit: int = 10) -> list[Topic]:
    return sorted(topics, key=lambda topic: score_topic(topic, concept_tag), reverse=True)[:limit]


def summarize_reason(topic: Topic) -> str:
    method = topic.structured.get("Method") or topic.summary
    metrics = topic.structured.get("Metrics", "")
    reason = method.strip().rstrip("。")
    if len(reason) > 85:
        reason = reason[:82].rstrip() + "..."
    if metrics and metrics not in {"-", "N/A"}:
        metric_text = metrics.strip().rstrip("。")
        if len(metric_text) > 55:
            metric_text = metric_text[:52].rstrip() + "..."
        reason += f"；证据：{metric_text}"
    return reason or topic.summary or topic.title


def method_families(topics: list[Topic], schema: dict[str, Any], concept_tag: str) -> str:
    taxonomy = schema["literature"]["tag_taxonomy"]
    counts: Counter[str] = Counter()
    examples: dict[str, list[Topic]] = {}
    for topic in topics:
        for tag in topic.tags:
            if tag == concept_tag or tag not in taxonomy:
                continue
            counts[tag] += 1
            examples.setdefault(tag, []).append(topic)
    if not counts:
        examples[concept_tag] = topics[:4]
        counts[concept_tag] = len(topics)
    lines = []
    for tag, count in counts.most_common(5):
        label = taxonomy.get(tag, {}).get("cn", taxonomy.get(tag, {}).get("title", tag))
        papers = "、".join(f"[[{topic.slug}]]" for topic in examples[tag][:4])
        lines.append(f"- {label}路径：本地有 {count} 篇相关文献，代表论文包括 {papers}。")
    return "\n".join(lines)


def key_ideas(info: dict[str, Any], topics: list[Topic], schema: dict[str, Any], concept_tag: str) -> str:
    ideas = list(info.get("key_ideas", []))
    tag_counts = Counter(tag for topic in topics for tag in topic.tags if tag != concept_tag)
    taxonomy = schema["literature"]["tag_taxonomy"]
    for tag, count in tag_counts.most_common(3):
        label = taxonomy.get(tag, {}).get("cn", tag)
        ideas.append(f"在当前 vault 中，{info.get('cn', info.get('title', concept_tag))}经常与{label}共同出现，已有 {count} 篇本地文献提供交叉证据。")
    if topics:
        years = sorted({topic.year for topic in topics if topic.year})
        ideas.append(f"本地证据覆盖 {len(topics)} 篇论文，时间跨度为 {years[0]}-{years[-1]}，适合支持趋势性问答但仍需结合具体论文证据。")
    return "\n".join(f"- {idea}" for idea in ideas[:8])


def key_papers(topics: list[Topic]) -> str:
    return "\n".join(f"- [[{topic.slug}]]：{summarize_reason(topic)}。" for topic in topics)


def evidence_map(topics: list[Topic], key_topics: list[Topic], schema: dict[str, Any], concept_tag: str) -> str:
    tag_counts = Counter(tag for topic in topics for tag in topic.tags if tag != concept_tag)
    taxonomy = schema["literature"]["tag_taxonomy"]
    strongest = "、".join(f"[[{topic.slug}]]" for topic in key_topics[:5]) or "暂无"
    lines = [
        f"- 本地证据规模：当前概念页连接 {len(topics)} 篇 literature notes，其中 {sum(1 for topic in topics if topic.status == 'done')} 篇为 `status: done`。",
        f"- 代表性证据链：{strongest}。",
    ]
    if tag_counts:
        cross = "、".join(f"{taxonomy.get(tag, {}).get('cn', tag)}({count})" for tag, count in tag_counts.most_common(5))
        lines.append(f"- 主要交叉主题：{cross}。")
    metric_topics = [topic for topic in key_topics if topic.structured.get("Metrics")]
    if metric_topics:
        links = "、".join(f"[[{topic.slug}]]" for topic in metric_topics[:5])
        lines.append(f"- 可核查实验结果主要来自：{links}；回答具体性能问题时应回到这些论文笔记核对指标。")
    else:
        lines.append("- 当前本地证据更偏方法与任务描述，量化指标覆盖不足；回答性能问题时需要逐篇核查原文证据。")
    return "\n".join(lines)


def open_problems(topics: list[Topic]) -> str:
    limitations = []
    for topic in topics:
        value = topic.structured.get("Limitations", "").strip()
        if value and value not in {"-", "N/A", "未明确"}:
            limitations.append((topic.slug, value))
    if not limitations:
        return "\n".join(
            [
                "- 本地笔记尚未提取足够多的明确 limitation，需要回到关键论文补充失败案例。",
                "- 需要区分真实机器人部署、仿真实验和数据集评测，避免把离线指标当作真实操控能力。",
                "- 长时序泛化、接触不确定性和跨任务迁移仍应作为后续阅读重点。",
            ]
        )
    lines = []
    for slug, value in limitations[:6]:
        text = value.rstrip("。")
        if len(text) > 95:
            text = text[:92].rstrip() + "..."
        lines.append(f"- [[{slug}]] 暴露的限制：{text}。")
    return "\n".join(lines)


def render_concept(path: Path, tag: str, info: dict[str, Any], related: list[Topic], schema: dict[str, Any]) -> str:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    parsed = extract_frontmatter(current)
    fields = parse_frontmatter_map(parsed[0]) if parsed else {}
    created = fields.get("created", today_iso()).strip('"')
    key_topics = select_key_topics(related, tag)
    frontmatter = render_frontmatter(
        "concept",
        {
            "title": fields.get("title", info.get("title", path.stem)).strip('"'),
            "tags": parse_list_value(fields.get("tags", "")) or ["concept", tag],
            "created": created,
            "updated": today_iso(),
            "type": "concept",
            "status": "done",
            "summary": fields.get("summary", info.get("summary", "")).strip('"'),
            "aliases": parse_list_value(fields.get("aliases", "")) or info.get("aliases", []),
        },
        schema,
    )
    related_papers = "\n".join(f"- [[{topic.slug}]]" for topic in sorted(related, key=lambda topic: topic.slug)) or "-"
    related_concepts = section(parsed[1], "## Related Concepts") if parsed else "-"
    if not related_concepts:
        related_concepts = "-"
    return (
        frontmatter
        + "\n"
        + "## Definition\n\n"
        + f"{info.get('summary', fields.get('summary', path.stem)).strip(chr(34))}\n\n"
        + "## Key Ideas\n\n"
        + f"{key_ideas(info, related, schema, tag)}\n\n"
        + "## Method Families\n\n"
        + f"{method_families(related, schema, tag)}\n\n"
        + "## Key Papers\n\n"
        + f"{key_papers(key_topics)}\n\n"
        + "## Evidence Map\n\n"
        + f"{evidence_map(related, key_topics, schema, tag)}\n\n"
        + "## Open Problems\n\n"
        + f"{open_problems(key_topics)}\n\n"
        + "## Related Concepts\n\n"
        + f"{related_concepts}\n\n"
        + "## Related Papers\n\n"
        + f"{related_papers}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("concept", nargs="?", help="Optional concept slug to upgrade.")
    args = parse_args_with_write_options(parser)

    schema = load_schema()
    topics = load_topics()
    entries = concept_entries(schema)
    selected = [args.concept] if args.concept else sorted(entries)
    updated = 0
    for concept in selected:
        if concept not in entries:
            safe_print(f"UNKNOWN_CONCEPT: {concept}")
            continue
        tag, info = entries[concept]
        path = CONCEPTS_DIR / f"{concept}.md"
        if not path.exists():
            safe_print(f"MISSING_CONCEPT_PAGE: {concept}")
            continue
        related = [topics[slug] for slug in concept_page_papers(path) if slug in topics]
        content = render_concept(path, tag, info, related, schema)
        if safe_write(path, content, dry_run=args.dry_run, backup=not args.no_backup):
            updated += 1
        safe_print(f"{concept}: {len(related)} related papers")
    safe_print(f"Done. Updated: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
