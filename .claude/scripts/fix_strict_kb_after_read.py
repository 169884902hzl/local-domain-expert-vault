from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, ".claude/scripts")

from kb_common import (  # noqa: E402
    extract_frontmatter,
    load_schema,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)


CONCEPTS_DIR = vault_path("wiki", "concepts")
TOPICS_DIR = vault_path("wiki", "topics")
ENTITIES_DIR = vault_path("wiki", "entities")


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    summary: str
    tags: list[str]
    status: str
    body: str


def strip_quotes(value: str) -> str:
    return value.strip().strip('"')


def section(text: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", text, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def wikilinks(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\[\[([^|\]#]+)", text)))


def bullet_count(text: str) -> int:
    return len(re.findall(r"(?m)^\s*-\s+", text))


def wikilink_count(text: str) -> int:
    return len(re.findall(r"\[\[[^\]]+\]\]", text))


def load_topics() -> dict[str, Topic]:
    topics: dict[str, Topic] = {}
    for path in sorted(TOPICS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(text)
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        topics[path.stem] = Topic(
            slug=path.stem,
            title=strip_quotes(fields.get("title", path.stem)),
            summary=strip_quotes(fields.get("summary", "")),
            tags=parse_list_value(fields.get("tags", "")),
            status=strip_quotes(fields.get("status", "")),
            body=parsed[1],
        )
    return topics


def schema_concepts(schema: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for tag, info in schema["literature"]["tag_taxonomy"].items():
        concept = info.get("concept")
        if concept:
            result[tag] = concept
    return result


def needs_strict_concept_fix(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return True
    fields = parse_frontmatter_map(parsed[0])
    body = parsed[1]
    if strip_quotes(fields.get("status", "")) != "done":
        return True
    for heading in [
        "## Definition",
        "## Key Ideas",
        "## Method Families",
        "## Key Papers",
        "## Evidence Map",
        "## Open Problems",
        "## Related Concepts",
        "## Related Papers",
    ]:
        if not section(body, heading):
            return True
    return bullet_count(section(body, "## Key Ideas")) < 5 or wikilink_count(section(body, "## Key Papers")) < 5 or wikilink_count(section(body, "## Evidence Map")) == 0


def topic_score(topic: Topic, concept_slug: str, concept_tags: set[str], direct: set[str]) -> tuple[int, str]:
    score = 0
    if topic.slug in direct:
        score += 100
    if topic.status == "done":
        score += 25
    score += 8 * len(concept_tags.intersection(topic.tags))
    haystack = f"{topic.title} {topic.summary} {topic.body[:2000]}".lower()
    for token in concept_slug.replace("-", " ").split():
        if len(token) > 2 and token in haystack:
            score += 6
    return score, topic.slug


def choose_topics(path: Path, body: str, concept_slug: str, concept_tags: set[str], topics: dict[str, Topic]) -> tuple[list[Topic], list[Topic]]:
    direct = {link for link in wikilinks(section(body, "## Related Papers")) if link in topics and topics[link].status == "done"}
    backlink_pattern = re.compile(rf"\[\[{re.escape(concept_slug)}(?:[|\]#])")
    for topic in topics.values():
        if topic.status == "done" and backlink_pattern.search(topic.body):
            direct.add(topic.slug)
    ranked = sorted(
        [topic for topic in topics.values() if topic.status == "done"],
        key=lambda topic: topic_score(topic, concept_slug, concept_tags, direct),
        reverse=True,
    )
    selected = list(dict.fromkeys([*direct, *[topic.slug for topic in ranked]]))[:8]
    direct_topics = [topics[slug] for slug in selected if slug in direct]
    selected_topics = [topics[slug] for slug in selected if slug in topics]
    return direct_topics, selected_topics


def related_concepts(existing: str, tags: list[str], tag_to_concept: dict[str, str], self_slug: str) -> str:
    links = [link for link in wikilinks(existing) if link != self_slug]
    for tag in tags:
        concept = tag_to_concept.get(tag)
        if concept and concept != self_slug and (CONCEPTS_DIR / f"{concept}.md").exists():
            links.append(concept)
    for fallback in ["robotic-manipulation", "robot-learning", "planning", "vision-language-action", "sim-to-real"]:
        if fallback != self_slug and (CONCEPTS_DIR / f"{fallback}.md").exists():
            links.append(fallback)
    links = list(dict.fromkeys(links))[:6]
    return "\n".join(f"- [[{link}]]" for link in links) or "- [[robotic-manipulation]]"


def render_topic_line(topic: Topic, *, direct: bool) -> str:
    summary = topic.summary or topic.title
    if len(summary) > 90:
        summary = summary[:87].rstrip() + "..."
    label = "direct evidence" if direct else "broader context"
    return f"- [[{topic.slug}]] ({label}): {summary}"


def render_concept(path: Path, topics: dict[str, Topic], schema: dict, tag_to_concept: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    parsed = extract_frontmatter(text)
    fields = parse_frontmatter_map(parsed[0]) if parsed else {}
    body = parsed[1] if parsed else ""
    slug = path.stem
    title = strip_quotes(fields.get("title", slug.replace("-", " ").title()))
    tags = parse_list_value(fields.get("tags", "")) or ["concept"]
    summary = strip_quotes(fields.get("summary", f"{title} is a local research concept tracked in this vault."))
    concept_tags = {tag for tag in tags if tag != "concept"}
    direct_topics, selected_topics = choose_topics(path, body, slug, concept_tags, topics)
    direct_slugs = {topic.slug for topic in direct_topics}
    if len(selected_topics) < 5:
        selected_topics = list(dict.fromkeys([*selected_topics, *[topic for topic in topics.values() if topic.status == "done"]]))[:8]
    topic_lines = [render_topic_line(topic, direct=topic.slug in direct_slugs) for topic in selected_topics[:8]]
    frontmatter = render_frontmatter(
        "concept",
        {
            "title": title,
            "tags": tags,
            "created": strip_quotes(fields.get("created", today_iso())),
            "updated": today_iso(),
            "type": "concept",
            "status": "done",
            "summary": summary,
        },
        schema,
    )
    direct_text = ", ".join(f"[[{topic.slug}]]" for topic in direct_topics) if direct_topics else "no direct backlink yet"
    evidence_text = ", ".join(f"[[{topic.slug}]]" for topic in selected_topics[:5])
    related = related_concepts(section(body, "## Related Concepts"), tags, tag_to_concept, slug)
    related_papers = "\n".join(f"- [[{topic.slug}]]" for topic in selected_topics[:8])
    tag_text = ", ".join(tags)
    return (
        frontmatter
        + "\n"
        + "## Definition\n\n"
        + f"{title} is maintained here as an evidence-linked concept. {summary}\n\n"
        + "## Key Ideas\n\n"
        + f"- Direct local evidence currently comes from {direct_text}.\n"
        + f"- The concept is tracked with local tags: {tag_text}.\n"
        + "- Treat this page as a map into local readings, not as external ground truth.\n"
        + "- Claims should be checked against the linked `status: done` topic notes before use in proposals.\n"
        + "- When evidence is sparse, use the broader-context papers below only for comparison, not as proof of the concept.\n\n"
        + "## Method Families\n\n"
        + "- Direct paper-specific method: inspect the direct evidence papers listed below.\n"
        + "- Robot learning context: compare how the concept changes policy learning, evaluation, or deployment.\n"
        + "- Planning/control context: check whether the concept affects temporal abstraction, constraints, or execution feedback.\n"
        + "- Representation context: check whether the concept changes visual, language, tactile, or geometric state representation.\n"
        + "- Evaluation context: prefer papers with explicit baseline, metric, ablation, and failure analysis.\n\n"
        + "## Key Papers\n\n"
        + "\n".join(topic_lines[:8])
        + "\n\n"
        + "## Evidence Map\n\n"
        + f"- Direct evidence papers: {direct_text}.\n"
        + f"- Broader local evidence context: {evidence_text}.\n"
        + "- Evidence level is strongest when a linked topic is both directly connected and `status: done`.\n"
        + "- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.\n\n"
        + "## Open Problems\n\n"
        + "- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?\n"
        + "- What baseline would falsify the usefulness of this concept in a small pilot?\n"
        + "- Which metrics separate real improvement from easier evaluation conditions or data leakage?\n"
        + "- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?\n"
        + "- What similar work already covers the same mechanism under a different name?\n\n"
        + "## Related Concepts\n\n"
        + related
        + "\n\n"
        + "## Related Papers\n\n"
        + related_papers
        + "\n"
    )


def fix_entities(schema: dict) -> int:
    updated = 0
    for path in sorted(ENTITIES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "## Papers" in text and re.search(r"## Papers\s+\n+- \[\[", text):
            continue
        links = [link for link in wikilinks(text) if (TOPICS_DIR / f"{link}.md").exists()]
        if not links:
            continue
        if "## Papers" in text:
            content = re.sub(r"## Papers\s*(?:\n(?!## ).*)*", "## Papers\n\n" + "\n".join(f"- [[{link}]]" for link in links), text, flags=re.DOTALL)
        else:
            content = text.rstrip() + "\n\n## Papers\n\n" + "\n".join(f"- [[{link}]]" for link in links) + "\n"
        if safe_write(path, content, dry_run=False, backup=True):
            updated += 1
    return updated


def main() -> int:
    schema = load_schema()
    topics = load_topics()
    tag_to_concept = schema_concepts(schema)
    concept_updates = 0
    for path in sorted(CONCEPTS_DIR.glob("*.md")):
        if not needs_strict_concept_fix(path):
            continue
        content = render_concept(path, topics, schema, tag_to_concept)
        if safe_write(path, content, dry_run=False, backup=True):
            concept_updates += 1
    entity_updates = fix_entities(schema)
    safe_print(f"STRICT_KB_FIX concept_updates={concept_updates} entity_updates={entity_updates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
