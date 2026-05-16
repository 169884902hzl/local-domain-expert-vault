"""Validate an RL Token failure-memory pilot run directory."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path


TRACK_ROOT = vault_path("projects", "focus-tracks", "rl-token-vla-online-rl")
SCHEMA_PATH = TRACK_ROOT / "experiments" / "memory-index-schema.json"
REQUIRED_FILES = ["run-config.json", "memory-index.jsonl", "results.csv", "failure-rubric.md", "notes.md"]
REQUIRED_CONDITIONS = {"rl_head_no_memory", "critic_memory_main", "random_memory_negative"}


def _load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def _load_schema() -> dict[str, Any]:
    schema, error = _load_json(SCHEMA_PATH)
    if error or schema is None:
        return {}
    return schema


def _validate_memory_record(record: dict[str, Any], schema: dict[str, Any], line_no: int) -> list[str]:
    issues: list[str] = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    for key in required:
        if key not in record:
            issues.append(f"memory_index_line_{line_no}:missing_{key}")
    for key, value in record.items():
        prop = properties.get(key)
        if not prop:
            issues.append(f"memory_index_line_{line_no}:unexpected_{key}")
            continue
        expected_type = prop.get("type")
        if expected_type == "string" and not isinstance(value, str):
            issues.append(f"memory_index_line_{line_no}:bad_type_{key}")
        elif expected_type == "integer" and not isinstance(value, int):
            issues.append(f"memory_index_line_{line_no}:bad_type_{key}")
        elif expected_type == "number" and not isinstance(value, (int, float)):
            issues.append(f"memory_index_line_{line_no}:bad_type_{key}")
        elif expected_type == "array" and not isinstance(value, list):
            issues.append(f"memory_index_line_{line_no}:bad_type_{key}")
        enum = prop.get("enum")
        if enum and value not in enum:
            issues.append(f"memory_index_line_{line_no}:bad_enum_{key}:{value}")
    return issues


def _validate_memory_index(path: Path) -> tuple[int, list[str]]:
    schema = _load_schema()
    issues: list[str] = []
    count = 0
    if not schema:
        return 0, ["schema_unreadable"]
    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not raw.strip():
            continue
        count += 1
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            issues.append(f"memory_index_line_{line_no}:json_error:{exc.msg}")
            continue
        if not isinstance(record, dict):
            issues.append(f"memory_index_line_{line_no}:not_object")
            continue
        issues.extend(_validate_memory_record(record, schema, line_no))
    if count == 0:
        issues.append("memory_index_empty")
    return count, issues


def _validate_results(path: Path) -> tuple[int, set[str], list[str]]:
    issues: list[str] = []
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    if not rows:
        return 0, set(), ["results_empty"]
    conditions = {row.get("condition", "").strip() for row in rows if row.get("condition", "").strip()}
    missing = REQUIRED_CONDITIONS - conditions
    for condition in sorted(missing):
        issues.append(f"missing_required_condition:{condition}")
    required_columns = {
        "run_id",
        "run_date",
        "environment",
        "task_id",
        "token_source",
        "condition",
        "seed",
        "train_steps",
        "success_rate",
        "repeated_failure_rate",
        "anchor_drift",
    }
    missing_columns = required_columns - set(rows[0].keys())
    for column in sorted(missing_columns):
        issues.append(f"results_missing_column:{column}")
    return len(rows), conditions, issues


def validate_run(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not run_dir.exists():
        return {"status": "FAIL", "run_dir": str(run_dir), "errors": ["run_dir_missing"], "warnings": []}
    for name in REQUIRED_FILES:
        if not (run_dir / name).exists():
            errors.append(f"missing_file:{name}")
    config = None
    if (run_dir / "run-config.json").exists():
        config, config_error = _load_json(run_dir / "run-config.json")
        if config_error:
            errors.append(f"run_config_json_error:{config_error}")
    memory_count = 0
    if (run_dir / "memory-index.jsonl").exists():
        memory_count, memory_issues = _validate_memory_index(run_dir / "memory-index.jsonl")
        errors.extend(memory_issues)
    result_rows = 0
    conditions: set[str] = set()
    if (run_dir / "results.csv").exists():
        result_rows, conditions, result_issues = _validate_results(run_dir / "results.csv")
        errors.extend(result_issues)
    if config:
        configured_conditions = set(config.get("conditions", [])) if isinstance(config.get("conditions"), list) else set()
        missing_config = REQUIRED_CONDITIONS - configured_conditions
        for condition in sorted(missing_config):
            warnings.append(f"run_config_missing_required_condition:{condition}")
    status = "PASS" if not errors and not warnings else "WARN" if not errors else "FAIL"
    return {
        "status": status,
        "run_dir": str(run_dir),
        "memory_records": memory_count,
        "result_rows": result_rows,
        "conditions": sorted(conditions),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Pilot run directory under the vault, or an absolute path.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = vault_path(args.run_dir)
    result = validate_run(run_dir)
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(
            f"RL_TOKEN_PILOT_VALIDATION status={result['status']} "
            f"memory_records={result.get('memory_records', 0)} result_rows={result.get('result_rows', 0)}"
        )
        for item in result.get("errors", []):
            safe_print(f"ERROR: {item}")
        for item in result.get("warnings", []):
            safe_print(f"WARN: {item}")
    return 0 if result["status"] in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
