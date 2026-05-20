"""Extract a long-term research-agenda evidence matrix from done topic notes."""
from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any

from kb_common import safe_print, safe_write
from research_agenda_common import (
    EVIDENCE_DIR,
    EVIDENCE_MATRIX,
    REQUIRED_EVIDENCE_FIELDS,
    detect_domains,
    ensure_agenda_dirs,
    frontmatter_list,
    iter_topic_notes,
    load_evidence_matrix,
    merge_evidence_records,
    note_is_done_literature,
    rel,
    render_frontmatter,
    split_csv,
    strip_quotes,
    write_jsonl,
    read_frontmatter,
)
from research_seed_v2_common import (
    artifact_dir,
    agenda_v2_path,
    ensure_v2_dirs,
    mark_state,
    write_json,
    write_jsonl as write_v2_jsonl,
)


LEGACY_STRUCTURED_FIELD_RE = re.compile(
    r"^- (?P<name>Problem|Method|Tasks|Sensors|Robot Setup|Metrics|Limitations|Evidence Notes):\s*(?P<value>.+)$",
    flags=re.MULTILINE,
)
DECORATED_STRUCTURED_FIELD_RE = re.compile(
    r"^- (?:\*\*)?(?P<name>Problem|Method|Tasks|Sensors|Robot Setup|Metrics|Limitations|Evidence Notes)(?:\*\*)?:\s*(?P<value>.+)$",
    flags=re.MULTILINE,
)
FIELD_TO_CLAIM = {
    "Problem": "problem",
    "Method": "method",
    "Tasks": "task",
    "Sensors": "sensor",
    "Robot Setup": "robot_setup",
    "Metrics": "metric",
    "Limitations": "limitation",
    "Evidence Notes": "evidence_note",
}
TRANSFER_DOMAINS = {
    "DLO": "transfer_to_DLO",
    "tactile": "transfer_to_tactile",
    "bimanual": "transfer_to_bimanual",
    "VLA": "transfer_to_VLA",
    "sim-to-real": "transfer_to_sim_to_real",
}
ANCHOR_TYPES = {"section", "figure", "table", "result_row", "snippet", "abstract", "note_only"}
STRICT_ANCHOR_TYPES = {"section", "figure", "table", "result_row", "snippet"}
PAPER_PRIMITIVE_CLAIMS = [
    "central_claim",
    "method_assumption",
    "strongest_baseline",
    "actual_baseline_result",
    "missing_ablation",
    "unmodeled_latent_variable",
    "evaluation_blind_spot",
    "interface_boundary",
    "transfer_failure",
    "reusable_primitive",
    "contradiction",
]
CLAIM_TO_SECTION = {
    "paper_summary": "Frontmatter summary",
    "problem": "Problem",
    "method": "Method",
    "task": "结构化提取",
    "sensor": "结构化提取",
    "robot_setup": "结构化提取",
    "metric": "结构化提取",
    "limitation": "Limitations",
    "open_question": "Limitations",
    "evidence_note": "结构化提取",
}
CLAIM_SECTION_CANDIDATES = {
    "metric": ["Results", "Evaluation", "Experiments", "Metrics", "Evidence Notes"],
    "limitation": ["Limitations", "Discussion", "Failure Cases", "Evaluation", "Evidence Notes"],
    "evidence_note": ["Evidence Notes", "Results", "Evaluation", "Discussion"],
    "task": ["Tasks", "Experiments", "Evaluation"],
    "sensor": ["Sensors", "Method", "System"],
    "robot_setup": ["Robot Setup", "System", "Method"],
}
CLAIM_TO_STRUCTURED_FIELD = {
    "problem": "Problem",
    "method": "Method",
    "task": "Tasks",
    "sensor": "Sensors",
    "robot_setup": "Robot Setup",
    "metric": "Metrics",
    "limitation": "Limitations",
    "open_question": "Limitations",
    "evidence_note": "Evidence Notes",
}


def _clean(value: str) -> str:
    return " ".join(value.strip().strip('"').split())


def _structured_fields(body: str, *, include_decorated: bool = True) -> dict[str, str]:
    fields: dict[str, str] = {}
    pattern = DECORATED_STRUCTURED_FIELD_RE if include_decorated else LEGACY_STRUCTURED_FIELD_RE
    for match in pattern.finditer(body):
        fields[match.group("name")] = _clean(match.group("value"))
    return fields


def _section_text(body: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", flags=re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", body[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    return body[start:end].strip()


def _short_snippet(value: str, *, limit: int = 260) -> str:
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), value)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^\s*[-*]\s*", "", text.strip(), flags=re.MULTILINE)
    text = _clean(text)
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _section_candidates_for_claim(claim_type: str, section: str) -> list[str]:
    candidates = [] if section == "结构化提取" else [section]
    candidates.extend(CLAIM_SECTION_CANDIDATES.get(claim_type, []))
    if section == "结构化提取":
        candidates.append("Evidence Notes")
    return list(dict.fromkeys(candidate for candidate in candidates if candidate))


def _snippet_for_claim(
    *,
    claim_type: str,
    statement: str,
    fields: dict[str, str],
    structured: dict[str, str],
    body: str,
) -> tuple[str, str, str, str]:
    section = CLAIM_TO_SECTION.get(claim_type, "结构化提取")
    field_name = CLAIM_TO_STRUCTURED_FIELD.get(claim_type)
    if claim_type == "paper_summary" and fields.get("summary"):
        return section, _short_snippet(fields["summary"]), "frontmatter_summary", "medium"
    for heading in _section_candidates_for_claim(claim_type, section):
        snippet = _short_snippet(_section_text(body, heading))
        if snippet:
            return heading, snippet, "section_summary", "medium"
    if field_name and structured.get(field_name):
        return section, _short_snippet(structured[field_name]), "structured_field", "low"
    return section, _short_snippet(statement), "claim_statement", "low"


def _anchor_for(path: Path, section: str) -> str:
    if section == "Frontmatter summary":
        return rel(path)
    return f"{rel(path)}#{section}"


def _anchor_type(section: str, snippet_type: str, snippet: str) -> str:
    lowered = f"{section} {snippet}".lower()
    if "table" in lowered or "表" in lowered:
        return "table"
    if "figure" in lowered or "fig." in lowered or "fig " in lowered or "图" in lowered:
        return "figure"
    if snippet_type == "frontmatter_summary":
        return "abstract"
    if snippet_type == "section_summary" and snippet:
        return "section"
    return "note_only"


def _risks_for_claim(claim_type: str, statement: str, structured: dict[str, str]) -> list[str]:
    risks: list[str] = []
    limitation = structured.get("Limitations", "")
    if claim_type == "limitation":
        risks.append("source_reports_limitation")
    if limitation:
        risks.append(limitation[:180])
    if any(token in statement.lower() for token in ["uncertain", "limitation", "risk", "failure", "not", "未", "限制", "失败"]):
        risks.append("requires_pilot_validation")
    return list(dict.fromkeys(risks))[:3]


def _supports_for_claim(claim_type: str, domains: list[str]) -> list[str]:
    support = [claim_type]
    support.extend(domains[:5])
    return list(dict.fromkeys(support))


def _record(
    *,
    path: Path,
    fields: dict[str, str],
    tags: list[str],
    structured: dict[str, str],
    body: str,
    claim_type: str,
    statement: str,
    run_date: str,
) -> dict[str, Any]:
    title = strip_quotes(fields.get("title", "")) or path.stem
    domains = detect_domains(f"{title} {statement} {' '.join(structured.values())}", tags)
    evidence_section, source_snippet, snippet_type, confidence = _snippet_for_claim(
        claim_type=claim_type,
        statement=statement,
        fields=fields,
        structured=structured,
        body=body,
    )
    record: dict[str, Any] = {
        "source_note": rel(path),
        "source_title": title,
        "zotero_key": strip_quotes(fields.get("zotero_key", "")),
        "year": strip_quotes(fields.get("year", "")),
        "venue": strip_quotes(fields.get("venue", "")),
        "claim_type": claim_type,
        "statement": statement,
        "domains": domains,
        "supports": _supports_for_claim(claim_type, domains),
        "risks": _risks_for_claim(claim_type, statement, structured),
        "tags": tags,
        "run_date": run_date,
        "evidence_section": evidence_section,
        "source_snippet": source_snippet,
        "source_snippet_type": snippet_type,
        "evidence_anchor": _anchor_for(path, evidence_section),
        "anchor_type": _anchor_type(evidence_section, snippet_type, source_snippet),
        "extraction_confidence": confidence,
    }
    for domain, key in TRANSFER_DOMAINS.items():
        record[key] = domain in domains
    return record


def extract_from_note(path: Path, *, run_date: str, include_decorated_fields: bool = True) -> list[dict[str, Any]]:
    fields, body = read_frontmatter(path)
    if not fields:
        return []
    if strip_quotes(fields.get("type", "")) != "literature" or strip_quotes(fields.get("status", "")) != "done":
        return []
    tags = frontmatter_list(fields, "tags")
    structured = _structured_fields(body, include_decorated=include_decorated_fields)
    records: list[dict[str, Any]] = []
    summary = _clean(fields.get("summary", ""))
    if summary:
        records.append(
            _record(
                path=path,
                fields=fields,
                tags=tags,
                structured=structured,
                body=body,
                claim_type="paper_summary",
                statement=summary,
                run_date=run_date,
            )
        )
    for field_name, value in structured.items():
        if not value:
            continue
        records.append(
            _record(
                path=path,
                fields=fields,
                tags=tags,
                structured=structured,
                body=body,
                claim_type=FIELD_TO_CLAIM.get(field_name, field_name.lower().replace(" ", "_")),
                statement=value,
                run_date=run_date,
            )
        )
    if structured.get("Limitations"):
        records.append(
            _record(
                path=path,
                fields=fields,
                tags=tags,
                structured=structured,
                body=body,
                claim_type="open_question",
                statement=f"What remains unresolved or weakly validated: {structured['Limitations']}",
                run_date=run_date,
            )
        )
    return records


def _selected_notes(*, all_notes: bool, zotero_keys: list[str]) -> tuple[list[Path], list[str]]:
    missing: list[str] = []
    selected: list[Path] = []
    key_filter = {key.upper() for key in zotero_keys}
    found_keys: set[str] = set()
    for path in iter_topic_notes():
        fields, _ = read_frontmatter(path)
        key = strip_quotes(fields.get("zotero_key", "")).upper()
        if all_notes:
            if note_is_done_literature(path):
                selected.append(path)
        elif key in key_filter:
            found_keys.add(key)
            if note_is_done_literature(path):
                selected.append(path)
    if key_filter:
        missing = sorted(key_filter - found_keys)
    return selected, missing


def _paper_card(path: Path, records: list[dict[str, Any]]) -> str:
    first = records[0]
    lines = [
        render_frontmatter(
            first["source_title"],
            ["research-agenda", "paper-card"],
            "Structured research-agenda evidence extracted from a done literature note.",
        ).rstrip(),
        f"# {first['source_title']}",
        "",
        f"- source_note: [[{Path(first['source_note']).stem}|{first['source_title']}]]",
        f"- zotero_key: {first.get('zotero_key', '')}",
        f"- year: {first.get('year', '')}",
        f"- domains: {', '.join(first.get('domains', []))}",
        "",
        "## Evidence Claims",
        "",
    ]
    for item in records:
        lines.append(f"- **{item['claim_type']}**: {item['statement']}")
        if item.get("evidence_anchor"):
            lines.append(f"  - evidence_anchor: `{item.get('evidence_anchor')}`")
        if item.get("source_snippet"):
            lines.append(
                f"  - source_snippet ({item.get('source_snippet_type', 'unknown')}, "
                f"confidence={item.get('extraction_confidence', '-')})：{item.get('source_snippet')}"
            )
    return "\n".join(lines).rstrip() + "\n"


def write_paper_cards(records: list[dict[str, Any]], *, dry_run: bool) -> None:
    by_note: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_note.setdefault(record["source_note"], []).append(record)
    for source_note, items in by_note.items():
        path = EVIDENCE_DIR / "paper_cards" / f"{Path(source_note).stem}.md"
        safe_write(path, _paper_card(path, items), dry_run=dry_run, backup=True)


def extract_records(*, all_notes: bool, zotero_keys: list[str], run_date: str) -> tuple[list[dict[str, Any]], list[str]]:
    selected, missing = _selected_notes(all_notes=all_notes, zotero_keys=zotero_keys)
    records: list[dict[str, Any]] = []
    include_decorated = not all_notes
    for path in selected:
        records.extend(extract_from_note(path, run_date=run_date, include_decorated_fields=include_decorated))
    return records, missing


def validate_records(records: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for index, record in enumerate(records, 1):
        for field in REQUIRED_EVIDENCE_FIELDS:
            if field not in record:
                issues.append(f"record_{index}:missing_field:{field}")
        if not record.get("source_note", "").startswith("wiki/topics/"):
            issues.append(f"record_{index}:source_note_not_topic:{record.get('source_note')}")
        if not record.get("statement"):
            issues.append(f"record_{index}:empty_statement")
    return issues


def _anchor_confidence(record: dict[str, Any], claim_type: str) -> str:
    anchor = _record_anchor(str(record.get("source_note", "")), record)
    confidence, _reason, _requires_human_check = _claim_confidence(record, claim_type, anchor)
    return confidence


def _claim_id(paper_key: str, claim_type: str, statement: str) -> str:
    basis = f"{paper_key}|{claim_type}|{' '.join(str(statement).lower().split())}"
    return "paper-claim-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _record_anchor(source_note: str, record: dict[str, Any] | None) -> dict[str, Any]:
    if not record:
        return {
            "source_note": source_note,
            "evidence_anchor": "",
            "anchor_type": "note_only",
            "section": "",
            "snippet": "",
            "snippet_type": "note_only",
            "pdf_page": None,
        }
    anchor_type = str(record.get("anchor_type") or "note_only")
    if anchor_type not in ANCHOR_TYPES:
        anchor_type = "note_only"
    return {
        "source_note": source_note,
        "evidence_anchor": record.get("evidence_anchor", ""),
        "anchor": record.get("evidence_anchor", ""),
        "anchor_type": anchor_type,
        "anchor_source": record.get("anchor_source", "note_section"),
        "section": record.get("evidence_section", ""),
        "snippet": record.get("source_snippet", ""),
        "snippet_type": record.get("source_snippet_type", "note_only"),
        "pdf_page": record.get("pdf_page", None),
        "page": record.get("page", record.get("pdf_page", None)),
        "table_id": record.get("table_id", ""),
        "row_index": record.get("row_index", None),
        "row_text": record.get("row_text", ""),
        "metric_name": record.get("metric_name", ""),
        "baseline_name": record.get("baseline_name", ""),
        "reported_value": record.get("reported_value", ""),
        "task_or_dataset": record.get("task_or_dataset", ""),
    }


def _strictly_anchored(anchor: dict[str, Any]) -> bool:
    return bool(
        anchor.get("anchor_type") in STRICT_ANCHOR_TYPES
        and (anchor.get("evidence_anchor") or anchor.get("section") or anchor.get("snippet"))
    )


def _claim_confidence(record: dict[str, Any] | None, claim_type: str, anchor: dict[str, Any]) -> tuple[str, str, bool]:
    if not record:
        return "low", "claim_not_extracted_from_note", True
    snippet = str(anchor.get("snippet", ""))
    snippet_type = str(anchor.get("snippet_type", ""))
    anchor_type = str(anchor.get("anchor_type", "note_only"))
    anchored = _strictly_anchored(anchor)
    if claim_type == "actual_baseline_result" and not anchored:
        return "unusable", "actual_baseline_result_requires_section_snippet_table_or_figure_anchor", True
    if anchor_type == "note_only" or snippet_type in {"claim_statement", "structured_field"} or not snippet:
        return "low", "note_only_or_legacy_structured_field_without_strict_anchor", True
    if claim_type == "strongest_baseline" and not anchored:
        return "low", "strongest_baseline_without_strict_anchor_is_low_confidence", True
    if claim_type == "evaluation_blind_spot":
        if not anchored:
            return "low", "evaluation_blind_spot_requires_strict_anchor_for_medium_or_high", True
        return "medium", "evaluation_blind_spot_has_strict_anchor_but_requires_human_review", False
    if not anchored:
        return "low", "high_confidence_requires_section_snippet_table_or_figure_anchor", True
    if claim_type in {"missing_ablation", "interface_boundary", "transfer_failure", "contradiction", "reusable_primitive"}:
        return "medium", "strict_anchor_present_but_claim_requires_human_interpretation", False
    return "high", "strict_anchor_present", False


def _claim_from_record(
    *,
    paper_key: str,
    source_note: str,
    claim_type: str,
    statement: str,
    record: dict[str, Any] | None,
) -> dict[str, Any]:
    anchor = _record_anchor(source_note, record)
    confidence, confidence_reason, requires_human_check = _claim_confidence(record, claim_type, anchor)
    summary_origin = str(anchor.get("snippet_type") or "note_only")
    if summary_origin in {"frontmatter_summary", "claim_statement"} and not _strictly_anchored(anchor):
        requires_human_check = True
        if confidence == "high":
            confidence = "low"
            confidence_reason = "model_summary_without_strict_anchor_is_low_confidence"
    return {
        "claim_id": _claim_id(paper_key, claim_type, statement),
        "claim_type": claim_type,
        "statement": statement,
        "evidence_anchor": anchor.get("evidence_anchor", ""),
        "anchor_type": anchor.get("anchor_type", "note_only"),
        "anchor_source": anchor.get("anchor_source", "note_section"),
        "anchor": anchor,
        "confidence": confidence,
        "confidence_reason": confidence_reason,
        "summary_origin": summary_origin,
        "requires_human_check": requires_human_check,
        "domains": record.get("domains", []) if record else [],
    }


def _record_matches(record: dict[str, Any], claim_types: set[str], tokens: set[str] | None = None) -> bool:
    if str(record.get("claim_type")) not in claim_types or not record.get("statement"):
        return False
    if not tokens:
        return True
    text = " ".join(str(record.get(key, "")) for key in ["statement", "source_snippet", "evidence_section"]).lower()
    return any(token in text for token in tokens)


def _first_matching(
    records: list[dict[str, Any]],
    claim_types: set[str],
    *,
    tokens: set[str] | None = None,
) -> tuple[str, dict[str, Any] | None]:
    for record in records:
        if _record_matches(record, claim_types, tokens):
            return str(record["statement"]), record
    return "", None


def _first_prefer_matching(
    records: list[dict[str, Any]],
    claim_types: set[str],
    *,
    tokens: set[str],
) -> tuple[str, dict[str, Any] | None]:
    statement, record = _first_matching(records, claim_types, tokens=tokens)
    if record:
        return statement, record
    return _first_matching(records, claim_types)


def _legacy_confidence_map(claims: list[dict[str, Any]]) -> dict[str, str]:
    return {str(claim["claim_type"]): str(claim["confidence"]) for claim in claims}


def _legacy_anchor_map(claims: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(claim["claim_type"]): dict(claim["anchor"]) for claim in claims}


def _legacy_reason_map(claims: list[dict[str, Any]]) -> dict[str, str]:
    return {str(claim["claim_type"]): str(claim["confidence_reason"]) for claim in claims}


def _legacy_metadata_map(claims: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(claim["claim_type"]): {
            "claim_id": claim["claim_id"],
            "summary_origin": claim["summary_origin"],
            "requires_human_check": claim["requires_human_check"],
        }
        for claim in claims
    }


def _first_statement(records: list[dict[str, Any]], claim_types: set[str]) -> tuple[str, dict[str, Any] | None]:
    for record in records:
        if str(record.get("claim_type")) in claim_types and record.get("statement"):
            return str(record["statement"]), record
    return "", None


def build_paper_primitives(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_source.setdefault(str(record.get("source_note", "")), []).append(record)
    primitives: list[dict[str, Any]] = []
    for source_note, items in sorted(by_source.items()):
        paper_key = str(items[0].get("zotero_key") or Path(source_note).stem)
        central_claim, central_record = _first_statement(items, {"paper_summary", "problem"})
        method_assumption, method_record = _first_statement(items, {"method"})
        strongest_baseline, baseline_record = _first_statement(items, {"metric", "method"})
        actual_baseline_result, result_record = _first_statement(items, {"metric"})
        missing_ablation, ablation_record = _first_prefer_matching(
            items,
            {"limitation", "open_question", "evidence_note"},
            tokens={"ablation", "ablations", "消融", "对照"},
        )
        latent_variable, latent_record = _first_matching(
            items,
            {"limitation", "open_question", "evidence_note"},
            tokens={"latent", "unmodeled", "hidden", "未建模", "隐变量"},
        )
        evaluation_blind_spot, blind_record = _first_statement(items, {"limitation", "evidence_note"})
        interface_boundary, interface_record = _first_prefer_matching(
            items,
            {"method", "task", "sensor", "robot_setup", "limitation", "evidence_note"},
            tokens={"interface", "boundary", "handoff", "接口", "边界"},
        )
        transfer_failure, transfer_record = _first_matching(
            items,
            {"limitation", "open_question", "evidence_note"},
            tokens={"transfer", "sim-to-real", "generalization", "domain", "迁移", "泛化"},
        )
        reusable_primitive, primitive_record = _first_statement(items, {"method", "task", "sensor", "robot_setup"})
        contradiction, contradiction_record = _first_matching(
            items,
            {"limitation", "open_question", "evidence_note"},
            tokens={"contradiction", "conflict", "inconsistent", "反例", "矛盾", "冲突"},
        )
        record_by_name = {
            "central_claim": central_record,
            "method_assumption": method_record,
            "strongest_baseline": baseline_record,
            "actual_baseline_result": result_record,
            "missing_ablation": ablation_record,
            "unmodeled_latent_variable": latent_record,
            "evaluation_blind_spot": blind_record,
            "interface_boundary": interface_record,
            "transfer_failure": transfer_record,
            "reusable_primitive": primitive_record,
            "contradiction": contradiction_record,
        }
        primitive_values = {
            "central_claim": central_claim,
            "method_assumption": method_assumption,
            "strongest_baseline": strongest_baseline,
            "actual_baseline_result": actual_baseline_result,
            "missing_ablation": missing_ablation,
            "unmodeled_latent_variable": latent_variable,
            "evaluation_blind_spot": evaluation_blind_spot,
            "interface_boundary": interface_boundary,
            "transfer_failure": transfer_failure,
            "reusable_primitive": reusable_primitive,
            "contradiction": contradiction,
        }
        claims = [
            _claim_from_record(
                paper_key=paper_key,
                source_note=source_note,
                claim_type=claim_type,
                statement=statement,
                record=record_by_name.get(claim_type),
            )
            for claim_type, statement in primitive_values.items()
            if statement
        ]
        primitives.append(
            {
                "schema_version": "paper_primitives.v1",
                "paper_key": paper_key,
                "source_note": source_note,
                "source_title": items[0].get("source_title", Path(source_note).stem),
                "primitives": primitive_values,
                "claims": claims,
                "anchors": _legacy_anchor_map(claims),
                "confidence": _legacy_confidence_map(claims),
                "confidence_reasons": _legacy_reason_map(claims),
                "claim_metadata": _legacy_metadata_map(claims),
                "legacy_evidence_boundary": "legacy records without section/snippet/table/figure anchors are low confidence by default.",
            }
        )
    return primitives


def write_v2_primitives(run_date: str, records: list[dict[str, Any]], *, dry_run: bool) -> list[dict[str, Any]]:
    ensure_v2_dirs(run_date)
    primitives = build_paper_primitives(records)
    for item in primitives:
        write_json(
            agenda_v2_path("paper-primitives", f"{item['paper_key']}.json"),
            item,
            dry_run=dry_run,
        )
    write_v2_jsonl(artifact_dir(run_date) / "paper-primitives-snapshot.jsonl", primitives, dry_run=dry_run)
    mark_state(run_date, "reading_completed", "artifacts/paper-primitives-snapshot.jsonl", dry_run=dry_run)
    return primitives


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Extract from every done literature note.")
    parser.add_argument("--zotero-keys", default="", help="Comma-separated Zotero keys to extract.")
    parser.add_argument("--run-date", default="")
    parser.add_argument("--write-v2-primitives", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_date = args.run_date or __import__("datetime").date.today().isoformat()
    zotero_keys = split_csv(args.zotero_keys)
    if not args.all and not zotero_keys:
        safe_print("FAIL provide --all or --zotero-keys")
        return 1
    ensure_agenda_dirs()
    records, missing = extract_records(all_notes=args.all, zotero_keys=zotero_keys, run_date=run_date)
    issues = validate_records(records)
    source_count = len({record["source_note"] for record in records})
    claim_counts = Counter(record["claim_type"] for record in records)
    safe_print(
        "EXTRACT "
        f"sources={source_count} records={len(records)} "
        f"missing_keys={len(missing)} issues={len(issues)}"
    )
    for key, count in sorted(claim_counts.items()):
        safe_print(f"  {key}: {count}")
    for item in missing[:20]:
        safe_print(f"WARN missing_zotero_key:{item}")
    for issue in issues[:20]:
        safe_print(f"ERROR {issue}")
    if issues:
        return 1
    if args.dry_run:
        return 0

    merged = merge_evidence_records(load_evidence_matrix(), records)
    write_jsonl(EVIDENCE_MATRIX, merged, dry_run=False)
    write_paper_cards(records, dry_run=False)
    if args.write_v2_primitives:
        primitives = write_v2_primitives(run_date, records, dry_run=False)
        safe_print(f"PAPER_PRIMITIVES: {len(primitives)}")
    safe_print(f"EVIDENCE_MATRIX: {rel(EVIDENCE_MATRIX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
