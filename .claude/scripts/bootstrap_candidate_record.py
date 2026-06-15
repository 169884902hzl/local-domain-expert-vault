"""Bootstrap a v1 candidate record from an accepted v0.3 backlog item."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from research_governance_common import candidate_dir, ensure_v1_dirs, read_json, utc_now, validate_governance_payload, write_json


def _accepted_candidate_id(payload: dict[str, Any]) -> str:
    candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
    decision = payload.get("survival_decision", {}) if isinstance(payload.get("survival_decision"), dict) else {}
    return str(candidate.get("candidate_id") or decision.get("candidate_id") or payload.get("candidate_id") or "").strip()


def _accepted_title(payload: dict[str, Any], candidate_id: str) -> str:
    candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
    decision = payload.get("survival_decision", {}) if isinstance(payload.get("survival_decision"), dict) else {}
    return str(candidate.get("title") or decision.get("candidate_title") or candidate_id).strip()


def _draft_evidence(payload: dict[str, Any]) -> list[dict[str, Any]]:
    candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
    evidence = candidate.get("evidence", [])
    if not isinstance(evidence, list):
        return []
    items: list[dict[str, Any]] = []
    for item in evidence[:12]:
        if not isinstance(item, dict):
            continue
        statement = str(item.get("statement") or "").strip()
        source = str(item.get("source_note") or "").strip()
        if not statement and not source:
            continue
        items.append(
            {
                "evidence_type": str(item.get("claim_type") or "accepted_backlog_evidence"),
                "statement": statement,
                "source_artifact": source,
                "metadata": {"source_title": str(item.get("source_title") or "")},
            }
        )
    return items


def _metadata(payload: dict[str, Any], accepted_path: Path) -> dict[str, Any]:
    candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
    decision = payload.get("survival_decision", {}) if isinstance(payload.get("survival_decision"), dict) else {}
    keys = [
        "problem",
        "mechanism",
        "hypothesis",
        "minimum_no_hardware_pilot",
        "killer_experiment",
        "metric_suite",
        "baseline_matrix",
        "falsification",
    ]
    metadata = {key: candidate.get(key, "") for key in keys if str(candidate.get(key, "")).strip()}
    metadata.update(
        {
            "accepted_source": str(accepted_path),
            "accepted_run_date": str(payload.get("run_date") or decision.get("run_date") or ""),
            "accepted_bucket": str(payload.get("bucket") or "seed-candidates/accepted"),
        }
    )
    return metadata


def build_candidate_record(payload: dict[str, Any], accepted_path: Path, *, candidate_id: str = "") -> dict[str, Any]:
    cid = candidate_id or _accepted_candidate_id(payload)
    if not cid:
        raise ValueError("missing_candidate_id")
    record = {
        "schema_version": "candidate_record.v1",
        "candidate_id": cid,
        "title": _accepted_title(payload, cid),
        "state": "program_candidate_synthesized",
        "auto_promote_allowed": False,
        "draft_evidence": _draft_evidence(payload),
        "created_at": utc_now(),
        "boundary": "Bootstrap record only; active seed promotion requires human-confirmed governance artifacts and active_seed_commit.py.",
        "metadata": _metadata(payload, accepted_path),
    }
    errors = validate_governance_payload(record, "candidate_record.v1")
    if errors:
        raise ValueError(";".join(errors))
    return record


def bootstrap_from_accepted(path: Path, *, candidate_id: str = "", human_initiated: bool = False, dry_run: bool = False) -> dict[str, Any]:
    if not human_initiated:
        raise ValueError("missing_human_initiated_flag")
    payload = read_json(path)
    record = build_candidate_record(payload, path, candidate_id=candidate_id)
    ensure_v1_dirs(record["candidate_id"])
    write_json(candidate_dir(record["candidate_id"]) / "candidate-record.json", record, dry_run=dry_run, overwrite=False)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-accepted", required=True, help="Path to a seed-candidates/accepted JSON item.")
    parser.add_argument("--candidate-id", default="", help="Optional candidate id override.")
    parser.add_argument("--human-initiated", action="store_true", help="Required: acknowledge this bootstrap was manually requested.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        record = bootstrap_from_accepted(Path(args.from_accepted), candidate_id=args.candidate_id, human_initiated=args.human_initiated, dry_run=args.dry_run)
    except Exception as exc:
        print(json.dumps({"status": "blocked", "error": f"{type(exc).__name__}:{exc}"}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "dry_run" if args.dry_run else "success", "candidate_id": record["candidate_id"], "record": record}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
