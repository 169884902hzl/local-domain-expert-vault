"""Record v2 pilot outcomes and non-gate strategy feedback for existing seeds."""
from __future__ import annotations

import argparse
import json

from kb_common import safe_print
from research_seed_v2_common import agenda_v2_path, ensure_v2_dirs, utc_now, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-slug", required=True)
    parser.add_argument("--outcome", choices=["pilot_ready", "needs_revision", "killed"], required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs()
    payload = {
        "schema_version": "pilot_feedback.v1",
        "seed_slug": args.seed_slug,
        "outcome": args.outcome,
        "created_at": utc_now(),
        "evidence": args.evidence,
        "strategy_feedback": {
            "may_adjust": ["intake_weights", "lane_quota", "prompt_emphasis", "resurrection_candidates"],
            "cannot_weaken_hard_gates": True,
        },
    }
    write_json(agenda_v2_path("pilots", args.seed_slug, "pilot-feedback.json"), payload, dry_run=args.dry_run)
    safe_print(f"PILOT_FEEDBACK: seed={args.seed_slug} outcome={args.outcome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
