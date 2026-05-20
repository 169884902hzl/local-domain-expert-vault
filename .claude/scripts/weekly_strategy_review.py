"""Write safe v2 strategy overrides without weakening hard gates."""
from __future__ import annotations

import argparse
import json
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import HARD_GATE_FIELDS, agenda_v2_path, ensure_v2_dirs, read_json, utc_now, write_json


ALLOWED_OVERRIDE_KEYS = {
    "intake_weights",
    "lane_quota",
    "prompt_emphasis",
    "resurrection_candidates",
}


def sanitize_overrides(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    safe: dict[str, Any] = {
        "schema_version": "strategy_overrides.v1",
        "updated_at": utc_now(),
        "allowed_keys": sorted(ALLOWED_OVERRIDE_KEYS),
        "hard_gates": HARD_GATE_FIELDS,
        "overrides": {},
    }
    for key, value in payload.items():
        if key in HARD_GATE_FIELDS:
            errors.append(f"attempted_hard_gate_override:{key}")
            continue
        if key not in ALLOWED_OVERRIDE_KEYS:
            errors.append(f"unsupported_strategy_override:{key}")
            continue
        safe["overrides"][key] = value
    return safe, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-json", default="", help="Optional JSON object with strategy override keys.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs()
    payload = json.loads(args.input_json) if args.input_json else {}
    safe, errors = sanitize_overrides(payload)
    safe["validation_errors"] = errors
    write_json(agenda_v2_path("strategy", "active-overrides.json"), safe, dry_run=args.dry_run)
    safe_print(f"WEEKLY_STRATEGY_REVIEW: errors={len(errors)} overrides={len(safe['overrides'])}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
