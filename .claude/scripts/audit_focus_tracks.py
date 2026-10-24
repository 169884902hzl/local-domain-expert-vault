"""Audit focused research tracks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from focus_track_common import (
    FOCUS_ROOT,
    TRACKS,
    load_jsonl,
    note_status,
    read_frontmatter,
    read_text,
    rel,
    topic_path_from_stem,
    track_config,
    track_evidence_path,
    track_root,
)
from focus_track_review import review
from kb_common import safe_print, vault_path


REQUIRED_DIRS = ["evidence", "hypotheses", "experiments", "similar-work", "paper-claims", "daily", "reviews"]
REQUIRED_FILES = [
    "track-dashboard.md",
    "core-paper.md",
    "evidence/track_evidence.jsonl",
    "similar-work/similar-work-map.md",
    "hypotheses/frozen-vla-small-rl-head.md",
    "experiments/minimal-replication-plan.md",
    "paper-claims/claim-gate.md",
    "paper-claims/accepted_claims.jsonl",
    "decision-log.md",
]


def _frontmatter_errors(path: Path) -> list[str]:
    fields, _ = read_frontmatter(path)
    required = ["title", "tags", "created", "updated", "type", "status", "summary"]
    errors = [f"{rel(path)}:missing_frontmatter:{key}" for key in required if key not in fields]
    if fields and fields.get("type", "").strip('"') != "permanent":
        errors.append(f"{rel(path)}:frontmatter_type_not_permanent")
    return errors


def _audit_evidence(track: str, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    path = track_evidence_path(track)
    if not path.exists():
        errors.append("missing_track_evidence")
        return {"records": 0, "sources": 0}
    records = load_jsonl(path)
    sources = {str(record.get("source_note", "")) for record in records}
    for index, record in enumerate(records, 1):
        source = str(record.get("source_note", ""))
        if not source.startswith("wiki/topics/"):
            errors.append(f"evidence_record_{index}:source_not_topic:{source}")
            continue
        source_path = vault_path(*source.split("/"))
        if not source_path.exists():
            errors.append(f"evidence_record_{index}:missing_source_note:{source}")
            continue
        if note_status(source_path) != "done":
            errors.append(f"evidence_record_{index}:source_not_done:{source}")
        if not record.get("statement"):
            errors.append(f"evidence_record_{index}:empty_statement")
        if not record.get("track_relevance"):
            warnings.append(f"evidence_record_{index}:missing_track_relevance")
    if len(records) < 3:
        warnings.append(f"low_focus_evidence_count:{len(records)}")
    return {"records": len(records), "sources": len(sources)}


def audit(track: str) -> dict[str, Any]:
    track_config(track)
    errors: list[str] = []
    warnings: list[str] = []
    root = track_root(track)
    if not FOCUS_ROOT.exists():
        errors.append("missing_focus_tracks_root")
    if not root.exists():
        errors.append(f"missing_track_root:{track}")
    for directory in REQUIRED_DIRS:
        if not (root / directory).exists():
            errors.append(f"missing_dir:{directory}")
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.exists():
            errors.append(f"missing_file:{relative}")
            continue
        if path.suffix == ".md":
            errors.extend(_frontmatter_errors(path))
    config = track_config(track)
    core_path = vault_path(*config["core_note"].split("/"))
    if not core_path.exists():
        errors.append(f"missing_core_note:{config['core_note']}")
    elif note_status(core_path) != "done":
        errors.append(f"core_note_not_done:{config['core_note']}")
    done_similar = 0
    for item in config["similar_work"]:
        path = topic_path_from_stem(item["stem"])
        if path.exists() and note_status(path) == "done":
            done_similar += 1
    if done_similar < 5:
        errors.append(f"too_few_done_similar_work:{done_similar}")
    claim_gate = read_text(root / "paper-claims" / "claim-gate.md")
    if "add memory" not in claim_gate or "add tactile" not in claim_gate or "add DLO" not in claim_gate:
        errors.append("claim_gate_missing_extension_guardrail")
    evidence = _audit_evidence(track, errors, warnings)
    review_result = review(track)
    for gate, passed in review_result["gates"].items():
        if not passed:
            warnings.append(f"review_gate_not_passed:{gate}")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "track": track,
        "status": status,
        "evidence": evidence,
        "similar_work_done": done_similar,
        "review_gates": review_result["gates"],
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit(args.track)
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result['status']} track={args.track} records={result['evidence']['records']}")
        for error in result["errors"]:
            safe_print(f"ERROR: {error}")
        for warning in result["warnings"]:
            safe_print(f"WARN: {warning}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
