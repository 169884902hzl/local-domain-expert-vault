"""Interpret a pilot result as proposed strategy feedback only."""
from __future__ import annotations
import argparse, json
from research_governance_common import pilot_result_dir, utc_now, write_json

def write_result(args: argparse.Namespace) -> dict:
    payload = {"schema_version": "pilot_result.v1", "candidate_id": args.candidate_id, "active_seed_id": args.active_seed_id, "pilot_status": args.status, "result_summary": args.result_summary, "proposed_strategy_event": {"event_type": "pilot_feedback", "candidate_id": args.candidate_id, "signal": args.status, "summary": args.result_summary, "applied": False}, "created_at": utc_now(), "boundary": "Pilot result does not promote, kill, or resurrect seeds. strategy_ledger.py --apply --human-confirmed is required for applied strategy changes."}
    write_json(pilot_result_dir(args.candidate_id) / "pilot-result.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--active-seed-id", default="")
    parser.add_argument("--status", choices=["positive", "negative", "inconclusive", "killed"], required=True)
    parser.add_argument("--result-summary", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(write_result(args), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
