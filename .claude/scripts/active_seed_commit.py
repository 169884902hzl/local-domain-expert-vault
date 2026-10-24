"""Commit a human-governed v1 active seed.

This is the only script allowed to write governance active-seed records and the
governance ledger.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from research_governance_common import (
    active_commit_validation,
    active_seed_dir,
    active_seed_id_from_candidate,
    active_seed_record,
    append_jsonl,
    candidate_dir,
    governance_ledger_path,
    read_json,
    transition_errors,
    utc_now,
    write_json,
)


def _candidate_title(candidate_id: str) -> str:
    return str(read_json(candidate_dir(candidate_id) / "candidate-record.json").get("title") or candidate_id)


def _lock_path(active_seed_id: str) -> Path:
    return active_seed_dir(active_seed_id).with_suffix(".commit.lock")


def _acquire_lock(active_seed_id: str, *, dry_run: bool) -> Path | None:
    lock = _lock_path(active_seed_id)
    if dry_run:
        return lock
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return None
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps({"active_seed_id": active_seed_id, "created_at": utc_now()}, sort_keys=True) + "\n")
    return lock


def _release_lock(lock: Path | None, *, dry_run: bool) -> None:
    if dry_run or lock is None:
        return
    try:
        lock.unlink()
    except FileNotFoundError:
        pass


def _quarantine_active_seed_dir(active_seed_id: str) -> Path:
    source = active_seed_dir(active_seed_id)
    base = source.with_name(active_seed_id + ".quarantine")
    target = base
    counter = 1
    while target.exists():
        target = base.with_name(f"{base.name}-{counter}")
        counter += 1
    source.rename(target)
    return target


def commit_active_seed(candidate_id: str, *, actor: str, governance_signature: str, human_confirmed: bool, dry_run: bool = False) -> dict[str, Any]:
    active_seed_id = active_seed_id_from_candidate(candidate_id, _candidate_title(candidate_id))
    if not human_confirmed:
        return {"schema_version": "active_seed_commit_result.v1", "status": "blocked", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "errors": ["missing_human_confirmed_flag"]}
    if not governance_signature.strip():
        return {"schema_version": "active_seed_commit_result.v1", "status": "blocked", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "errors": ["missing_governance_signature"]}
    validation = active_commit_validation(candidate_id, active_seed_id=active_seed_id)
    errors = [*transition_errors("governance_review_requested", "active_seed_committed", mode="manual"), *validation.errors]
    if errors:
        return {"schema_version": "active_seed_commit_result.v1", "status": "blocked", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "errors": sorted(set(errors)), "warnings": validation.warnings}
    lock = _acquire_lock(active_seed_id, dry_run=dry_run)
    if lock is None:
        return {"schema_version": "active_seed_commit_result.v1", "status": "blocked", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "errors": ["concurrent_active_seed_commit_lock_exists"]}
    target = active_seed_dir(active_seed_id) / "active-seed-record.json"
    try:
        record = active_seed_record(candidate_id, active_seed_id=active_seed_id, actor=actor, governance_signature=governance_signature)
        write_json(target, record, dry_run=dry_run, overwrite=False)
        append_jsonl(
            governance_ledger_path(),
            {
                "schema_version": "governance_ledger_event.v1",
                "event_type": "active_seed_committed",
                "active_seed_id": active_seed_id,
                "candidate_id": candidate_id,
                "actor": actor,
                "created_at": utc_now(),
                "governance_signature": governance_signature,
            },
            dry_run=dry_run,
        )
    except Exception as exc:
        quarantine = ""
        if not dry_run and target.exists():
            quarantine = str(_quarantine_active_seed_dir(active_seed_id))
        return {"schema_version": "active_seed_commit_result.v1", "status": "blocked", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "errors": [f"active_seed_commit_exception:{type(exc).__name__}:{exc}"], "quarantine": quarantine}
    finally:
        _release_lock(lock, dry_run=dry_run)
    return {"schema_version": "active_seed_commit_result.v1", "status": "success" if not dry_run else "dry_run", "active_seed_id": active_seed_id, "candidate_id": candidate_id, "record_path": str(target), "ledger_path": str(governance_ledger_path()), "errors": []}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--actor", default="human")
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--governance-signature", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = commit_active_seed(args.candidate_id, actor=args.actor, governance_signature=args.governance_signature, human_confirmed=args.human_confirmed, dry_run=args.dry_run)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] in {"success", "dry_run"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
