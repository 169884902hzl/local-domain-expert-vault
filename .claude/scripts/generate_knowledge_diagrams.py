"""Generate Obsidian knowledge diagrams for papers, clusters, and idea candidates."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from gemini_cli_adapter import DEFAULT_GEMINI_MODEL, DEFAULT_GEMINI_TIMEOUT_SEC, run_gemini_cli
from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, vault_path
from research_agenda_common import DOMAIN_KEYWORDS, rel, slugify
from research_agenda_extract import _section_text, _structured_fields


ROOT = vault_path("projects", "knowledge-diagrams")
PAPER_DIR = ROOT / "papers"
CLUSTER_DIR = ROOT / "clusters"
IDEA_DIR = ROOT / "ideas"
DAILY_LIGHTWEIGHT_DIR = vault_path("projects", "research-agenda", "mechanism-graphs")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def _frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = _read(path)
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text
    fields, body = parsed
    return parse_frontmatter_map(fields), body


def _quote(value: str, *, limit: int = 86) -> str:
    text = " ".join(str(value or "-").replace('"', "'").replace("[", "(").replace("]", ")").split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text or "-"


def _safe_node_id(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    return text.strip("_") or "node"


def _find_topic_by_key(zotero_key: str) -> Path | None:
    pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(zotero_key)}"?\s*$', re.MULTILINE)
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        if pattern.search(_read(path)):
            return path
    return None


def _resolve_topic(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    relative = vault_path(*candidate.parts)
    if relative.exists():
        return relative
    by_key = _find_topic_by_key(value.upper())
    if by_key:
        return by_key
    by_stem = vault_path("wiki", "topics", f"{value}.md")
    if by_stem.exists():
        return by_stem
    raise FileNotFoundError(f"topic_not_found:{value}")


def _domains(text: str) -> list[str]:
    lower = text.lower()
    hits = []
    priority = ["DLO", "tactile", "bimanual", "VLA", "sim-to-real"]
    for domain in priority:
        keywords = DOMAIN_KEYWORDS.get(domain, [])
        if any(keyword.lower() in lower for keyword in keywords):
            hits.append(domain)
    return hits[:5]


def _field(structured: dict[str, str], body: str, name: str, fallback: str = "not specified") -> str:
    return structured.get(name) or _section_text(body, name) or fallback


def build_paper_packet(path: Path, *, depth: str = "deep") -> dict[str, Any]:
    fields, body = _frontmatter(path)
    structured = _structured_fields(body, include_decorated=True)
    title = fields.get("title", path.stem).strip().strip('"')
    text = f"{title}\n{body}"
    packet = {
        "schema_version": "knowledge_diagram.paper.v1",
        "diagram_kind": "paper",
        "depth": depth,
        "title": title,
        "source_note": rel(path),
        "zotero_key": fields.get("zotero_key", "").strip().strip('"'),
        "problem_pathology": _field(structured, body, "Problem"),
        "observations_inputs": _field(structured, body, "Sensors", "not specified"),
        "core_mechanism": _field(structured, body, "Method"),
        "training_evaluation": _field(structured, body, "Tasks", "not specified"),
        "baselines": _field(structured, body, "Baselines", "not specified"),
        "metrics": _field(structured, body, "Metrics", "not specified"),
        "limitations_failure_modes": _field(structured, body, "Limitations"),
        "evidence_notes": _field(structured, body, "Evidence Notes", "not specified"),
        "research_relevance": _domains(text),
        "boundary": "Understanding aid only; not a formal claim or publication figure.",
    }
    return packet


def _llm_refine_packet(packet: dict[str, Any], *, timeout: int, model: str) -> dict[str, Any]:
    prompt = {
        "task": "Refine this Obsidian knowledge diagram packet for understanding a robotics paper. Keep it evidence-bound.",
        "rules": [
            "Do not invent experimental results or claims.",
            "Make labels concise and mechanism-oriented.",
            "Preserve the same JSON keys; improve unclear fields only when supported by the packet.",
            "Return JSON only.",
        ],
        "packet": packet,
    }
    result = run_gemini_cli(json.dumps(prompt, ensure_ascii=False), timeout_sec=timeout, model=model)
    raw = str(result.get("clean_output") or "").strip()
    if result.get("error") or not raw:
        packet["llm_refine_status"] = f"failed:{result.get('error') or 'empty_output'}"
        return packet
    try:
        refined = json.loads(raw)
    except json.JSONDecodeError:
        packet["llm_refine_status"] = "failed:invalid_json"
        return packet
    if isinstance(refined, dict):
        refined.setdefault("llm_refine_status", "success")
        return {**packet, **refined}
    packet["llm_refine_status"] = "failed:non_object_json"
    return packet


def render_paper_markdown(packet: dict[str, Any]) -> str:
    title = str(packet.get("title", "Untitled"))
    source = str(packet.get("source_note", ""))
    domains = ", ".join(packet.get("research_relevance", [])) or "-"
    return "\n".join(
        [
            "---",
            f'title: "Knowledge Diagram - {title.replace(chr(34), chr(39))}"',
            "tags: [knowledge-diagram, paper-workbench, understanding]",
            f'zotero_key: "{str(packet.get("zotero_key", "")).replace(chr(34), chr(39))}"',
            'type: "permanent"',
            'status: "stub"',
            'summary: "Obsidian understanding diagram for a paper; not a formal claim."',
            "---",
            f"# Knowledge Diagram - {title}",
            "",
            "- diagram_type: paper_knowledge_dissection",
            f"- depth: `{packet.get('depth', '-')}`",
            f"- source_note: [[{Path(source).stem}|{title}]]" if source else "- source_note: -",
            f"- research_relevance: {domains}",
            "- boundary: understanding aid only; not a publication figure or accepted claim.",
            "",
            "```mermaid",
            "flowchart LR",
            "    accTitle: Paper Knowledge Diagram",
            "    accDescr: Mechanism-oriented understanding graph covering problem, observations, mechanism, evaluation, baselines, limitations, and research relevance.",
            f"    pathology[\"Problem / pathology: {_quote(str(packet.get('problem_pathology', '')))}\"]",
            f"    observations[\"Inputs / observations: {_quote(str(packet.get('observations_inputs', '')))}\"]",
            f"    mechanism[\"Core mechanism: {_quote(str(packet.get('core_mechanism', '')))}\"]",
            f"    evaluation[\"Training / evaluation: {_quote(str(packet.get('training_evaluation', '')))}\"]",
            f"    baselines[\"Baselines: {_quote(str(packet.get('baselines', '')))}\"]",
            f"    metrics[\"Metrics: {_quote(str(packet.get('metrics', '')))}\"]",
            f"    failures[\"Limitations / failure modes: {_quote(str(packet.get('limitations_failure_modes', '')))}\"]",
            f"    relevance[\"Your research relevance: {_quote(domains)}\"]",
            "    pathology --> observations --> mechanism --> evaluation --> metrics",
            "    mechanism --> baselines",
            "    baselines --> metrics",
            "    mechanism --> failures",
            "    failures --> relevance",
            "```",
            "",
            "## Reading Notes",
            "",
            f"- problem_pathology: {packet.get('problem_pathology') or '-'}",
            f"- core_mechanism: {packet.get('core_mechanism') or '-'}",
            f"- baselines: {packet.get('baselines') or '-'}",
            f"- limitations_failure_modes: {packet.get('limitations_failure_modes') or '-'}",
            f"- evidence_notes: {packet.get('evidence_notes') or '-'}",
            "",
        ]
    )


def write_paper_diagram(value: str, *, run_date: str = "", depth: str = "deep", llm: bool = False, timeout: int = DEFAULT_GEMINI_TIMEOUT_SEC, model: str = DEFAULT_GEMINI_MODEL, dry_run: bool = False, output_dir: Path | None = None) -> dict[str, Any]:
    path = _resolve_topic(value)
    packet = build_paper_packet(path, depth=depth)
    if run_date:
        packet["run_date"] = run_date
    if llm:
        packet = _llm_refine_packet(packet, timeout=timeout, model=model)
    root = output_dir or PAPER_DIR
    if run_date and depth == "lightweight":
        root = DAILY_LIGHTWEIGHT_DIR / run_date
    md_path = root / f"{path.stem}.md"
    json_path = root / f"{path.stem}.json"
    safe_write(md_path, render_paper_markdown(packet), dry_run=dry_run, backup=True)
    safe_write(json_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
    return {"status": "ok", "diagram_kind": "paper", "source_note": rel(path), "markdown": rel(md_path), "json": rel(json_path)}


def _cluster_topics(values: list[str]) -> list[Path]:
    topics: list[Path] = []
    for value in values:
        topics.append(_resolve_topic(value))
    return topics


def build_cluster_packet(values: list[str], *, title: str) -> dict[str, Any]:
    topics = _cluster_topics(values)
    papers = [build_paper_packet(path, depth="cluster_brief") for path in topics]
    domain_counts: Counter[str] = Counter()
    for paper in papers:
        domain_counts.update(paper.get("research_relevance", []))
    method_families: defaultdict[str, list[str]] = defaultdict(list)
    for paper in papers:
        method = str(paper.get("core_mechanism", "not specified"))
        family = _quote(method, limit=42)
        method_families[family].append(str(paper.get("title", "")))
    return {
        "schema_version": "knowledge_diagram.cluster.v1",
        "diagram_kind": "cluster",
        "title": title,
        "papers": papers,
        "method_families": dict(method_families),
        "domain_counts": dict(domain_counts),
        "shared_assumptions": "review common assumptions from the paper packets; this deterministic version does not invent hidden assumptions",
        "comparison_axes": ["problem_pathology", "core_mechanism", "baselines", "metrics", "limitations_failure_modes", "research_relevance"],
        "common_failure_modes": [paper.get("limitations_failure_modes", "") for paper in papers[:8]],
        "open_gaps": "Use the failure-mode nodes and missing baselines as human review targets.",
        "boundary": "Cluster map is an understanding aid, not a formal survey claim.",
    }


def render_cluster_markdown(packet: dict[str, Any]) -> str:
    title = str(packet.get("title", "Cluster"))
    papers = packet.get("papers", [])
    lines = [
        "---",
        f'title: "Cluster Knowledge Map - {title.replace(chr(34), chr(39))}"',
        "tags: [knowledge-diagram, cluster, understanding]",
        'type: "permanent"',
        'status: "stub"',
        'summary: "Obsidian understanding map for a paper family."',
        "---",
        f"# Cluster Knowledge Map - {title}",
        "",
        "- diagram_type: paper_family_cluster_map",
        "- boundary: understanding aid only; not a formal survey claim.",
        "",
        "```mermaid",
        "flowchart LR",
        "    accTitle: Paper Cluster Map",
        "    accDescr: Paper family map showing representative papers, method families, shared comparison axes, failure modes, and gaps.",
    ]
    family_nodes: list[str] = []
    for idx, (family, titles) in enumerate(packet.get("method_families", {}).items()):
        node = f"family_{idx}"
        family_nodes.append(node)
        lines.append(f"    {node}[\"Method family: {_quote(family)}\"]")
        for paper_title in titles[:4]:
            paper_node = _safe_node_id(f"paper_{idx}_{paper_title}")[:48]
            lines.append(f"    {paper_node}[\"{_quote(paper_title, limit=58)}\"]")
            lines.append(f"    {node} --> {paper_node}")
    lines.extend(
        [
            "    axes[\"Comparison axes: pathology / mechanism / baseline / metric / failure\"]",
            "    gaps[\"Open gaps: failure modes and missing baselines\"]",
        ]
    )
    for node in family_nodes:
        lines.append(f"    {node} --> axes")
    lines.extend(["    axes --> gaps", "```", "", "## Papers", ""])
    for paper in papers:
        lines.append(f"- [[{Path(str(paper.get('source_note', ''))).stem}|{paper.get('title', '-')}]]: {paper.get('core_mechanism', '-')}")
    lines.extend(["", "## Common Failure Modes", ""])
    for item in packet.get("common_failure_modes", [])[:8]:
        lines.append(f"- {item or '-'}")
    lines.extend(["", "## Open Gaps", "", f"- {packet.get('open_gaps', '-')}"])
    return "\n".join(lines).rstrip() + "\n"


def write_cluster_diagram(values: list[str], *, title: str, dry_run: bool = False) -> dict[str, Any]:
    packet = build_cluster_packet(values, title=title)
    slug = slugify(title)
    md_path = CLUSTER_DIR / f"{slug}.md"
    json_path = CLUSTER_DIR / f"{slug}.json"
    safe_write(md_path, render_cluster_markdown(packet), dry_run=dry_run, backup=True)
    safe_write(json_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
    return {"status": "ok", "diagram_kind": "cluster", "markdown": rel(md_path), "json": rel(json_path), "paper_count": len(values)}


def _load_candidate(path: Path, index: int) -> dict[str, Any]:
    data = json.loads(_read(path))
    candidates = data.get("raw_gemini_candidates", [])
    if not candidates:
        raise ValueError("no_raw_gemini_candidates")
    if index < 0 or index >= len(candidates):
        raise IndexError(f"candidate_index_out_of_range:{index}")
    return candidates[index]


def build_idea_packet(path: Path, index: int) -> dict[str, Any]:
    item = _load_candidate(path, index)
    return {
        "schema_version": "knowledge_diagram.idea.v1",
        "diagram_kind": "idea",
        "title": item.get("title", "Untitled idea"),
        "source_archive": rel(path),
        "candidate_index": index,
        "engineering_pathology": item.get("engineering_pathology") or item.get("problem", ""),
        "proposed_mechanism": item.get("mechanism", ""),
        "interface": item.get("interface", ""),
        "strongest_baseline": item.get("strongest_baseline", ""),
        "killer_experiment": item.get("killer_experiment", "") or item.get("pilot", ""),
        "rescue_path": item.get("rescue_mutation", "") or item.get("rescue_signal", ""),
        "boundary": "Idea mechanism map is triage support; not a validated claim.",
    }


def render_idea_markdown(packet: dict[str, Any]) -> str:
    title = str(packet.get("title", "Untitled idea"))
    return "\n".join(
        [
            "---",
            f'title: "Idea Mechanism Map - {title.replace(chr(34), chr(39))}"',
            "tags: [knowledge-diagram, idea, greenhouse]",
            'type: "permanent"',
            'status: "stub"',
            'summary: "Mechanism map for one greenhouse idea candidate."',
            "---",
            f"# Idea Mechanism Map - {title}",
            "",
            "- diagram_type: idea_mechanism_map",
            f"- source_archive: `{packet.get('source_archive', '-')}`",
            "- boundary: triage support only; not a validated claim.",
            "",
            "```mermaid",
            "flowchart LR",
            "    accTitle: Idea Mechanism Map",
            "    accDescr: Idea map connecting engineering pathology, proposed mechanism, interface, strongest baseline, killer experiment, and rescue path.",
            f"    pathology[\"Engineering pathology: {_quote(str(packet.get('engineering_pathology', '')))}\"]",
            f"    mechanism[\"Proposed mechanism: {_quote(str(packet.get('proposed_mechanism', '')))}\"]",
            f"    interface[\"Interface: {_quote(str(packet.get('interface', '')))}\"]",
            f"    baseline[\"Strongest baseline: {_quote(str(packet.get('strongest_baseline', '')))}\"]",
            f"    experiment[\"Killer experiment: {_quote(str(packet.get('killer_experiment', '')))}\"]",
            f"    rescue[\"Rescue path: {_quote(str(packet.get('rescue_path', '')))}\"]",
            "    pathology --> mechanism --> interface --> experiment",
            "    baseline --> experiment",
            "    mechanism --> rescue",
            "```",
            "",
        ]
    )


def write_idea_diagram(candidate_path: str, *, index: int, dry_run: bool = False) -> dict[str, Any]:
    path = Path(candidate_path)
    if not path.is_absolute():
        path = vault_path(*path.parts)
    packet = build_idea_packet(path, index)
    slug = slugify(str(packet.get("title", "idea")))
    md_path = IDEA_DIR / f"{slug}.md"
    json_path = IDEA_DIR / f"{slug}.json"
    safe_write(md_path, render_idea_markdown(packet), dry_run=dry_run, backup=True)
    safe_write(json_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
    return {"status": "ok", "diagram_kind": "idea", "markdown": rel(md_path), "json": rel(json_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    paper = sub.add_parser("paper")
    paper.add_argument("--zotero-key")
    paper.add_argument("--topic")
    paper.add_argument("--run-date", default="")
    paper.add_argument("--depth", choices=["lightweight", "deep"], default="deep")
    paper.add_argument("--llm", action="store_true")
    paper.add_argument("--timeout", type=int, default=DEFAULT_GEMINI_TIMEOUT_SEC)
    paper.add_argument("--model", default=DEFAULT_GEMINI_MODEL)
    paper.add_argument("--dry-run", action="store_true")

    cluster = sub.add_parser("cluster")
    cluster.add_argument("--zotero-keys", default="")
    cluster.add_argument("--topics", default="")
    cluster.add_argument("--title", required=True)
    cluster.add_argument("--dry-run", action="store_true")

    idea = sub.add_parser("idea")
    idea.add_argument("--candidate-json", required=True)
    idea.add_argument("--index", type=int, default=0)
    idea.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.command == "paper":
        value = args.zotero_key or args.topic
        if not value:
            raise SystemExit("--zotero-key or --topic is required")
        result = write_paper_diagram(
            value,
            run_date=args.run_date,
            depth=args.depth,
            llm=args.llm,
            timeout=args.timeout,
            model=args.model,
            dry_run=args.dry_run,
        )
    elif args.command == "cluster":
        values = [item.strip() for item in (args.zotero_keys or args.topics).split(",") if item.strip()]
        if not values:
            raise SystemExit("--zotero-keys or --topics is required")
        result = write_cluster_diagram(values, title=args.title, dry_run=args.dry_run)
    else:
        result = write_idea_diagram(args.candidate_json, index=args.index, dry_run=args.dry_run)
    safe_print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
