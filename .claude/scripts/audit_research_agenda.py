"""Audit the long-term research agenda workspace."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, vault_path
from research_agenda_common import (
    AGENDA_ROOT,
    EVIDENCE_MATRIX,
    IDEA_BANK_DIR,
    IDEA_STATES,
    REQUIRED_EVIDENCE_FIELDS,
    REQUIRED_IDEA_FILES,
    evidence_key,
    load_evidence_matrix,
    rel,
    strip_quotes,
)
from research_agenda_extract import extract_records
from research_agenda_review import iter_idea_folders, review_folder


WIKILINK_RE = re.compile(r"\[\[([^|\]#]+)")


def _done_topic_link_count(folder: Path) -> int:
    seen: set[str] = set()
    for path in folder.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for stem in WIKILINK_RE.findall(text):
            seen.add(stem.strip())
    count = 0
    for stem in seen:
        topic = vault_path("wiki", "topics", f"{stem}.md")
        if not topic.exists():
            continue
        parsed = extract_frontmatter(topic.read_text(encoding="utf-8"))
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        if strip_quotes(fields.get("status", "")) == "done":
            count += 1
    return count


def _text(folder: Path, name: str) -> str:
    path = folder / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _recent_evidence_count(folder: Path) -> int:
    text = _text(folder, "idea.md")
    match = re.search(r"^recent_evidence_count:\s*(\d+)", text, flags=re.MULTILINE)
    return int(match.group(1)) if match else 0


def audit_matrix(errors: list[str], warnings: list[str]) -> dict[str, Any]:
    if not EVIDENCE_MATRIX.exists():
        errors.append("missing_evidence_matrix")
        return {"records": 0, "sources": 0}
    records = load_evidence_matrix(EVIDENCE_MATRIX)
    sources = {record.get("source_note") for record in records}
    for index, record in enumerate(records, 1):
        for field in REQUIRED_EVIDENCE_FIELDS:
            if field not in record:
                errors.append(f"evidence_record_{index}:missing_field:{field}")
        source = str(record.get("source_note", ""))
        if not source.startswith("wiki/topics/"):
            errors.append(f"evidence_record_{index}:source_not_topic:{source}")
            continue
        source_path = vault_path(*source.split("/"))
        if not source_path.exists():
            errors.append(f"evidence_record_{index}:missing_source_note:{source}")
            continue
        parsed = extract_frontmatter(source_path.read_text(encoding="utf-8"))
        if not parsed:
            errors.append(f"evidence_record_{index}:missing_source_frontmatter:{source}")
            continue
        fields = parse_frontmatter_map(parsed[0])
        if strip_quotes(fields.get("status", "")) != "done":
            errors.append(f"evidence_record_{index}:source_not_done:{source}")
    if len(records) < 20:
        warnings.append(f"low_evidence_record_count:{len(records)}")
    current_keys = {evidence_key(record) for record in records}
    full_records, missing = extract_records(all_notes=True, zotero_keys=[], run_date=__import__("datetime").date.today().isoformat())
    full_keys = {evidence_key(record) for record in full_records}
    stale_missing = len(full_keys - current_keys)
    stale_extra = len(current_keys - full_keys)
    if stale_missing:
        warnings.append(f"evidence_matrix_stale_missing_records:{stale_missing}")
    if stale_extra:
        warnings.append(f"evidence_matrix_has_extra_records:{stale_extra}")
    if missing:
        warnings.append(f"evidence_matrix_full_extract_missing_keys:{len(missing)}")
    return {
        "records": len(records),
        "sources": len(sources),
        "full_extract_records": len(full_records),
        "stale_missing_records": stale_missing,
        "stale_extra_records": stale_extra,
    }


def audit_idea_bank(errors: list[str], warnings: list[str]) -> dict[str, Any]:
    counts: dict[str, int] = {state: 0 for state in IDEA_STATES}
    for state in IDEA_STATES:
        root = IDEA_BANK_DIR / state
        if not root.exists():
            errors.append(f"missing_idea_state_dir:{state}")
    for state, folder in iter_idea_folders():
        counts[state] += 1
        missing = [name for name in REQUIRED_IDEA_FILES if not (folder / name).exists()]
        if missing and state in {"promoted", "pilot-ready"}:
            errors.append(f"{rel(folder)}:missing_files:{','.join(missing)}")
        elif missing:
            warnings.append(f"{rel(folder)}:missing_files:{','.join(missing)}")
        if state != "promoted":
            continue
        evidence_count = _done_topic_link_count(folder)
        recent_count = _recent_evidence_count(folder)
        similar = _text(folder, "similar_work.md").lower()
        experiment = _text(folder, "experiment_plan.md").lower()
        novelty = _text(folder, "novelty_argument.md").lower()
        risk = _text(folder, "risk_review.md").lower()
        if evidence_count < 8:
            errors.append(f"{rel(folder)}:promoted_too_few_done_evidence:{evidence_count}")
        if recent_count < 2:
            errors.append(f"{rel(folder)}:promoted_too_few_recent_evidence:{recent_count}")
        if "similar" not in similar and "相近" not in similar:
            errors.append(f"{rel(folder)}:missing_similar_work_check")
        if "baseline" not in experiment or "metric" not in experiment or "pilot" not in experiment:
            errors.append(f"{rel(folder)}:missing_experiment_plan_gate")
        if "novelty" not in novelty and "not just" not in novelty and "不是" not in novelty:
            errors.append(f"{rel(folder)}:missing_novelty_argument")
        if "risk" not in risk and "fallback" not in risk and "失败" not in risk:
            errors.append(f"{rel(folder)}:missing_risk_review")
    return counts


def audit_maturity(warnings: list[str], notes: list[str]) -> dict[str, Any]:
    results = [review_folder(folder, state) for state, folder in iter_idea_folders()]
    state_counts = Counter(result["state"] for result in results)
    recommended_counts = Counter(result["recommended_state"] for result in results)
    metrics = {
        "ideas_total": len(results),
        "states": dict(state_counts),
        "recommended_states": dict(recommended_counts),
        "developing_ready": sum(1 for result in results if result["developing_ready"]),
        "promoted_ready": sum(1 for result in results if result["promoted_ready"]),
        "has_similar_work": sum(1 for result in results if result["has_similar_work"]),
        "has_experiment_plan": sum(1 for result in results if result["has_experiment_plan"]),
        "has_novelty_argument": sum(1 for result in results if result["has_novelty_argument"]),
        "has_risk_review": sum(1 for result in results if result["has_risk_review"]),
        "has_generated_similar_work": sum(1 for result in results if result.get("has_generated_similar_work")),
        "has_generated_experiment_plan": sum(1 for result in results if result.get("has_generated_experiment_plan")),
        "has_generated_novelty_argument": sum(1 for result in results if result.get("has_generated_novelty_argument")),
        "has_generated_risk_review": sum(1 for result in results if result.get("has_generated_risk_review")),
        "evidence_ge8": sum(1 for result in results if result["evidence_count"] >= 8),
        "recent_ge2": sum(1 for result in results if result["recent_evidence_count"] >= 2),
        "quality_blocked": sum(1 for result in results if result.get("quality_flags")),
        "generic_generated_cross_gap": sum(1 for result in results if "generic_generated_cross_gap" in result.get("quality_flags", [])),
        "max_score": max((result["score"] for result in results), default=0),
    }
    if results and state_counts.get("seed", 0) == len(results):
        warnings.append(f"all_ideas_remain_seed:{len(results)}")
    if results and metrics["developing_ready"] == 0:
        notes.append("no_idea_ready_for_developing")
    if results and metrics["has_similar_work"] == 0:
        warnings.append("no_idea_has_completed_similar_work_check")
    if results and metrics["has_experiment_plan"] == 0:
        if metrics["has_generated_experiment_plan"] > 0:
            notes.append("no_reviewed_experiment_plan_gate_yet")
        else:
            warnings.append("no_idea_has_generated_complete_experiment_plan")
    if results and metrics["has_generated_experiment_plan"] == 0:
        warnings.append("no_idea_has_generated_complete_experiment_plan")
    if results and metrics["evidence_ge8"] == 0:
        warnings.append("no_idea_has_8_done_local_evidence_sources")
    unresolved_quality = [
        result for result in results if result.get("quality_flags") and result["state"] not in {"rejected", "archived"}
    ]
    if unresolved_quality:
        warnings.append(f"quality_blocked_ideas_not_rejected:{len(unresolved_quality)}")
    return metrics


def audit() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    if not AGENDA_ROOT.exists():
        errors.append("missing_research_agenda_root")
    matrix = audit_matrix(errors, warnings)
    ideas = audit_idea_bank(errors, warnings)
    maturity = audit_maturity(warnings, notes)
    for relative in [
        "agenda-dashboard.md",
        "problem_pool/open_questions.md",
        "problem_pool/contradictions.md",
        "problem_pool/missing_experiments.md",
        "problem_pool/failure_modes.md",
        "problem_pool/transfer_opportunities.md",
    ]:
        if not (AGENDA_ROOT / relative).exists():
            errors.append(f"missing_agenda_file:{relative}")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "status": status,
        "matrix": matrix,
        "idea_counts": ideas,
        "maturity": maturity,
        "errors": errors,
        "warnings": warnings,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result['status']} matrix_records={result['matrix']['records']} matrix_sources={result['matrix']['sources']}")
        for error in result["errors"]:
            safe_print(f"ERROR: {error}")
        for warning in result["warnings"]:
            safe_print(f"WARN: {warning}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
