"""Static audit for the literature knowledge base."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from finalize_reading import extract_sections, strict_contract_issues
from kb_common import extract_frontmatter, load_schema, parse_frontmatter_map, parse_list_value, safe_print, vault_path


TOPICS_DIR = vault_path("wiki", "topics")
CONCEPTS_DIR = vault_path("wiki", "concepts")
ENTITIES_DIR = vault_path("wiki", "entities")
WAITING_TEXT = "待精读"
PLACEHOLDER_TEXT = "待精读补充"
STRICT_CONCEPT_SECTIONS = [
    "## Definition",
    "## Key Ideas",
    "## Method Families",
    "## Key Papers",
    "## Evidence Map",
    "## Open Problems",
    "## Related Concepts",
    "## Related Papers",
]


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path) -> tuple[dict[str, str], str, list[str]]:
    text = read(path)
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text, ["missing_frontmatter"]
    fm_text, body = parsed
    fields = parse_frontmatter_map(fm_text)
    keys = []
    for line in fm_text.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):", line)
        if match:
            keys.append(match.group(1))
    duplicates = [key for key, count in Counter(keys).items() if count > 1]
    issues = [f"duplicate_key:{key}" for key in duplicates]
    return fields, body, issues


def check_required(fields: dict[str, str], required: list[str]) -> list[str]:
    return [f"missing_required:{key}" for key in required if key not in fields]


def section_has_content(body: str, heading: str) -> bool:
    match = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    return bool(match and match.group(1).strip())


def section_content(body: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def bullet_count(section: str) -> int:
    return len(re.findall(r"(?m)^\s*-\s+\S", section))


def wikilink_count(section: str) -> int:
    return len(re.findall(r"\[\[[^|\]#]+", section))


def structured_field_name(line: str) -> str | None:
    if not line.startswith("-") or ":" not in line:
        return None
    name = line[1:].split(":", 1)[0].strip().strip("*").strip()
    return name or None


def is_generic_batch_summary(summary: str) -> bool:
    return summary.startswith("提出基于") and "的" in summary and "方法" in summary and summary.endswith("。")


def topic_zotero_keys(fields: dict[str, str]) -> set[str]:
    keys = {fields.get("zotero_key", "").strip('"').upper()}
    for alias_field in ("zotero_aliases", "zotero_keys"):
        keys.update(item.upper() for item in parse_list_value(fields.get(alias_field, "")))
    return {key for key in keys if key}


def find_topic_by_key(zotero_key: str) -> Path | None:
    requested_key = zotero_key.upper()
    for path in sorted(TOPICS_DIR.glob("*.md")):
        fields, _body, _issues = frontmatter(path)
        if requested_key in topic_zotero_keys(fields):
            return path
    return None


def audit_topic_note(
    path: Path,
    schema: dict[str, Any],
    *,
    strict_reading: bool = False,
    strict_contract: bool = False,
) -> tuple[dict[str, str], list[str], str, list[str], str]:
    fields, body, note_issues = frontmatter(path)
    required = schema["literature"]["required"]
    required_sections = schema["literature"].get("required_sections", [])
    structured_fields = schema["literature"].get("structured_fields", [])
    canonical = schema["literature"]["canonical_order"]
    allowed_status = set(schema["literature"]["fields"]["status"]["values"])

    note_issues.extend(check_required(fields, required))
    parsed = extract_frontmatter(read(path))
    keys = [line.split(":", 1)[0].strip() for line in parsed[0].splitlines() if ":" in line] if parsed else []
    actual = [key for key in keys if key in canonical]
    expected = [key for key in canonical if key in keys]
    if actual != expected:
        note_issues.append("frontmatter_order")
    status = fields.get("status", "").strip('"')
    summary = fields.get("summary", "").strip('"')
    if status not in allowed_status:
        note_issues.append(f"invalid_status:{status}")
    tags = parse_list_value(fields.get("tags", ""))
    if len(tags) > schema["literature"]["fields"]["tags"]["max"]:
        note_issues.append("too_many_tags")
    year = fields.get("year", "").strip('"')
    if year and not re.fullmatch(r"\d{4}", year):
        note_issues.append("invalid_year")
    zkey = fields.get("zotero_key", "").strip('"')
    for heading in required_sections:
        if heading not in body:
            note_issues.append(f"missing_heading:{heading}")
    structured_match = re.search(r"## 结构化提取\s*\n+(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    structured_body = structured_match.group(1) if structured_match else ""
    structured_names = [
        name
        for line in structured_body.splitlines()
        if (name := structured_field_name(line.strip()))
    ]
    duplicates = [field for field, count in Counter(structured_names).items() if count > 1]
    for field in duplicates:
        note_issues.append(f"duplicate_structured_field:{field}")
    for field in structured_fields:
        if field not in structured_names:
            note_issues.append(f"missing_structured_field:{field}")
    if status == "done":
        if WAITING_TEXT in body:
            note_issues.append("done_note_contains_waiting_text")
        if PLACEHOLDER_TEXT in structured_body:
            note_issues.append("done_note_contains_structured_placeholder")
        if "## Key Contributions" in body and "## 关键贡献" in body:
            note_issues.append("duplicate_key_contributions_section")
        if strict_reading:
            if "## 证据元数据" not in body:
                note_issues.append("strict_missing_evidence_metadata")
            if not summary or WAITING_TEXT in summary:
                note_issues.append("strict_bad_summary")
            elif is_generic_batch_summary(summary):
                note_issues.append("strict_generic_batch_summary")
            if strict_contract:
                sections = extract_sections(body)
                note_issues.extend(f"strict_{issue}" for issue in strict_contract_issues(sections))
    return fields, note_issues, status, tags, zkey


def audit_topics(schema: dict[str, Any], *, strict_reading: bool = False) -> tuple[list[dict[str, Any]], Counter[str], Counter[str]]:
    issues = []
    status_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    zkeys: defaultdict[str, list[str]] = defaultdict(list)

    for path in sorted(TOPICS_DIR.glob("*.md")):
        fields, note_issues, status, tags, zkey = audit_topic_note(path, schema, strict_reading=strict_reading)
        status_counts[status] += 1
        for tag in tags:
            tag_counts[tag] += 1
        if zkey:
            zkeys[zkey].append(rel(path))
        if note_issues:
            issues.append({"path": rel(path), "issues": note_issues})

    for zkey, paths in zkeys.items():
        if len(paths) > 1:
            issues.append({"path": ",".join(paths), "issues": [f"duplicate_zotero_key:{zkey}"]})
    return issues, status_counts, tag_counts


def audit_concepts(schema: dict[str, Any], *, strict_concepts: bool = False) -> list[dict[str, Any]]:
    issues = []
    required = schema["concept"]["required"]
    allowed_status = set(schema["concept"]["fields"]["status"]["values"])
    for path in sorted(CONCEPTS_DIR.glob("*.md")):
        fields, body, note_issues = frontmatter(path)
        note_issues.extend(check_required(fields, required))
        status = fields.get("status", "").strip('"')
        if status and status not in allowed_status:
            note_issues.append(f"invalid_status:{status}")
        if not section_has_content(body, "## Related Papers"):
            note_issues.append("missing_related_papers")
        if not section_has_content(body, "## Related Concepts"):
            note_issues.append("missing_related_concepts")
        if strict_concepts:
            for heading in STRICT_CONCEPT_SECTIONS:
                if not section_has_content(body, heading):
                    note_issues.append(f"strict_missing_or_empty:{heading.removeprefix('## ')}")
            if status != "done":
                note_issues.append(f"strict_concept_not_done:{status or 'missing'}")
            key_ideas = section_content(body, "## Key Ideas")
            if bullet_count(key_ideas) < 5:
                note_issues.append("strict_too_few_key_ideas")
            key_papers = section_content(body, "## Key Papers")
            if wikilink_count(key_papers) < 5:
                note_issues.append("strict_too_few_key_papers")
            evidence_map = section_content(body, "## Evidence Map")
            if wikilink_count(evidence_map) == 0:
                note_issues.append("strict_evidence_map_without_local_links")
        if note_issues:
            issues.append({"path": rel(path), "issues": note_issues})
    return issues


def resolve_note_path(note: str) -> Path:
    path = Path(note)
    if not path.is_absolute():
        path = vault_path(note)
    return path.resolve()


def target_payload(
    *,
    schema: dict[str, Any],
    args: argparse.Namespace,
    topic_issues: list[dict[str, Any]],
    concept_issues: list[dict[str, Any]],
    entity_issues: list[dict[str, Any]],
    tags_missing: list[str],
) -> tuple[dict[str, Any], bool]:
    issues: list[str] = []
    target_path: Path | None = None
    requested_key = (args.zotero_key or "").strip()
    note_arg = (args.note or "").strip()
    if requested_key:
        target_path = find_topic_by_key(requested_key)
        if target_path is None:
            issues.append(f"target_note_not_found:{requested_key}")
    if note_arg:
        note_path = resolve_note_path(note_arg)
        if not note_path.exists():
            issues.append(f"target_note_not_found:{note_arg}")
        elif target_path is not None and note_path != target_path.resolve():
            issues.append("target_note_mismatch:zotero_key_and_note_resolve_differently")
            target_path = note_path
        else:
            target_path = note_path

    target_zkey = requested_key
    if target_path and target_path.exists():
        fields, note_issues, _status, _tags, zkey = audit_topic_note(
            target_path,
            schema,
            strict_reading=args.strict_reading,
            strict_contract=args.strict_reading,
        )
        target_zkey = zkey or requested_key
        issues.extend(note_issues)
        if args.strict_reading and _status != "done":
            issues.append(f"strict_target_not_done:{_status or 'missing'}")
        if requested_key and requested_key.upper() not in topic_zotero_keys(fields):
            issues.append("target_note_mismatch:zotero_key_field_differs")
    payload = {
        "target_note": {
            "path": rel(target_path) if target_path and target_path.exists() else "",
            "zotero_key": target_zkey,
            "issues": issues,
            "strict_reading_pass": not issues,
        },
        "global_warnings": {
            "topic_issues": topic_issues,
            "concept_issues": concept_issues,
            "entity_issues": entity_issues,
            "tags_missing_from_taxonomy": tags_missing,
        },
        "exit_policy": "target_note_only",
    }
    return payload, not issues


def audit_entities(schema: dict[str, Any]) -> list[dict[str, Any]]:
    issues = []
    required = schema["entity"]["required"]
    for path in sorted(ENTITIES_DIR.glob("*.md")):
        fields, body, note_issues = frontmatter(path)
        note_issues.extend(check_required(fields, required))
        if "affiliation" not in fields:
            note_issues.append("missing_affiliation")
        if "url" not in fields:
            note_issues.append("missing_url")
        if "## Papers" not in body or not re.search(r"## Papers\s+\n+- \[\[", body):
            note_issues.append("missing_paper_links")
        if note_issues:
            issues.append({"path": rel(path), "issues": note_issues})
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict-reading", action="store_true", help="Also fail done notes that lack evidence metadata or still use generic batch summaries.")
    parser.add_argument("--strict-concepts", action="store_true", help="Also fail concept pages that remain stub-like indexes instead of evidence-grounded expert pages.")
    parser.add_argument("--zotero-key", default="", help="Audit one topic note by Zotero key and separate target issues from global warnings.")
    parser.add_argument("--note", default="", help="Audit one topic note by path and separate target issues from global warnings.")
    args = parser.parse_args()

    schema = load_schema()
    topic_issues, status_counts, tag_counts = audit_topics(schema, strict_reading=args.strict_reading)
    concept_issues = audit_concepts(schema, strict_concepts=args.strict_concepts)
    entity_issues = audit_entities(schema)
    taxonomy = schema["literature"]["tag_taxonomy"]
    tags_missing = sorted(set(tag_counts) - set(taxonomy))
    if args.zotero_key or args.note:
        payload, ok = target_payload(
            schema=schema,
            args=args,
            topic_issues=topic_issues,
            concept_issues=concept_issues,
            entity_issues=entity_issues,
            tags_missing=tags_missing,
        )
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    payload = {
        "counts": {
            "topics": len(list(TOPICS_DIR.glob("*.md"))),
            "concepts": len(list(CONCEPTS_DIR.glob("*.md"))),
            "entities": len(list(ENTITIES_DIR.glob("*.md"))),
        },
        "status_counts": dict(status_counts),
        "tag_counts": dict(tag_counts),
        "tags_missing_from_taxonomy": tags_missing,
        "topic_issues": topic_issues,
        "concept_issues": concept_issues,
        "entity_issues": entity_issues,
    }
    if args.json:
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        safe_print(
            "AUDIT "
            f"topics={payload['counts']['topics']} concepts={payload['counts']['concepts']} entities={payload['counts']['entities']} "
            f"topic_issues={len(topic_issues)} concept_issues={len(concept_issues)} entity_issues={len(entity_issues)}"
        )
        if payload["tags_missing_from_taxonomy"]:
            safe_print("TAGS_MISSING_FROM_TAXONOMY: " + ", ".join(payload["tags_missing_from_taxonomy"]))
        for section in ["topic_issues", "concept_issues", "entity_issues"]:
            for item in payload[section][:20]:
                safe_print(f"{section}: {item['path']} -> {', '.join(item['issues'])}")
    return 1 if topic_issues or concept_issues or entity_issues or payload["tags_missing_from_taxonomy"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
