"""Validate v2 research-seed run artifacts before downstream consumption."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import (
    ARTIFACT_SCHEMAS,
    PUBLISH_REQUIRED_ARTIFACTS,
    RUN_SCHEMA_VERSION,
    artifact_dir,
    file_sha256,
    init_manifest_with_policy,
    read_json,
    run_dir,
    validate_artifact,
    validate_json_file,
    v2_rel,
)


def _validate_manifest(run_date: str) -> list[str]:
    path = run_dir(run_date) / "manifest.json"
    if not path.exists():
        return [f"missing_manifest:{v2_rel(path)}"]
    return validate_json_file(path, RUN_SCHEMA_VERSION)


def _validate_referenced_hashes(run_date: str, artifact_name: str) -> list[str]:
    path = artifact_dir(run_date) / artifact_name
    if not path.exists() or artifact_name.endswith(".jsonl"):
        return []
    payload = read_json(path)
    errors: list[str] = []
    for name, expected in payload.get("artifact_hashes", {}).items():
        dep = artifact_dir(run_date) / name
        if not dep.exists():
            errors.append(f"{artifact_name}:hash_ref_missing:{name}")
            continue
        actual = file_sha256(dep)
        if actual != expected:
            errors.append(f"{artifact_name}:hash_mismatch:{name}:expected={expected}:actual={actual}")
    return errors


def validate_run(run_date: str, *, strict_publish: bool = False) -> dict[str, Any]:
    errors = _validate_manifest(run_date)
    checked: list[str] = ["manifest.json"]
    for artifact_name in ARTIFACT_SCHEMAS:
        path = artifact_dir(run_date) / artifact_name
        if not path.exists():
            if strict_publish and artifact_name in PUBLISH_REQUIRED_ARTIFACTS:
                errors.append(f"missing_publish_required_artifact:{artifact_name}")
            continue
        checked.append(f"artifacts/{artifact_name}")
        errors.extend(f"{artifact_name}:{issue}" for issue in validate_artifact(run_date, artifact_name))
        errors.extend(_validate_referenced_hashes(run_date, artifact_name))
    return {
        "schema_version": "research_run_validation.v1",
        "run_date": run_date,
        "status": "success" if not errors else "partial_schema_blocked",
        "checked": checked,
        "errors": errors,
    }


def validate_one(run_date: str, artifact_name: str) -> dict[str, Any]:
    if artifact_name not in ARTIFACT_SCHEMAS:
        return {
            "schema_version": "research_run_validation.v1",
            "run_date": run_date,
            "status": "partial_schema_blocked",
            "checked": [],
            "errors": [f"unknown_artifact:{artifact_name}"],
        }
    errors = validate_artifact(run_date, artifact_name)
    errors.extend(_validate_referenced_hashes(run_date, artifact_name))
    return {
        "schema_version": "research_run_validation.v1",
        "run_date": run_date,
        "status": "success" if not errors else "partial_schema_blocked",
        "checked": [f"artifacts/{artifact_name}"],
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    init_parser = sub.add_parser("init")
    init_parser.add_argument("--run-date", required=True)
    init_parser.add_argument("--backfill-mode", default="daily")
    init_parser.add_argument("--v2-publish-policy", choices=["disabled", "seed-candidates-only", "formal"], default="seed-candidates-only")
    init_parser.add_argument("--formal-seed-publish-allowed", action="store_true")
    init_parser.add_argument("--scheduled-daily-switched", action="store_true")
    init_parser.add_argument("--dry-run", action="store_true")

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--run-date", required=True)
    run_parser.add_argument("--strict-publish", action="store_true")
    run_parser.add_argument("--json", action="store_true")

    artifact_parser = sub.add_parser("artifact")
    artifact_parser.add_argument("--run-date", required=True)
    artifact_parser.add_argument("--artifact", required=True)
    artifact_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "init":
        payload = init_manifest_with_policy(
            args.run_date,
            dry_run=args.dry_run,
            backfill_mode=args.backfill_mode,
            v2_publish_policy=args.v2_publish_policy,
            formal_seed_publish_allowed=args.formal_seed_publish_allowed,
            scheduled_daily_switched=args.scheduled_daily_switched,
        )
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "artifact":
        result = validate_one(args.run_date, args.artifact)
    else:
        result = validate_run(args.run_date, strict_publish=getattr(args, "strict_publish", False))
    if getattr(args, "json", False):
        safe_print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        safe_print(f"VALIDATE_RESEARCH_RUN: {result['status']} checked={len(result['checked'])} errors={len(result['errors'])}")
        for error in result["errors"][:40]:
            safe_print(f"ERROR: {error}")
    return 0 if result["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
