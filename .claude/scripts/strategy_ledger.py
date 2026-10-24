"""Append proposed or human-applied v1 strategy events."""
from __future__ import annotations
import argparse, json
from research_governance_common import append_jsonl, strategy_ledger_path, transition_errors, utc_now

def build_event(args: argparse.Namespace) -> dict:
    applied = bool(args.apply and args.human_confirmed)
    errors = []
    if args.apply and not args.human_confirmed:
        errors.append("strategy_apply_requires_human_confirmed")
    if applied:
        errors.extend(transition_errors("pilot_executed", "strategy_updated", mode="manual", applied_strategy_event=True))
    return {"schema_version": "strategy_event.v1", "event_type": args.event_type, "candidate_id": args.candidate_id, "summary": args.summary, "applied": applied, "human_confirmed": bool(args.human_confirmed), "confirmed_by": args.confirmed_by if args.human_confirmed else "", "confirmed_at": utc_now() if args.human_confirmed else "", "created_at": utc_now(), "errors": errors, "boundary": "Applied strategy changes require --apply --human-confirmed; proposals cannot update weights, kill rules, or resurrection policy."}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--candidate-id", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--confirmed-by", default="human")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = build_event(args)
    if not payload["errors"]:
        append_jsonl(strategy_ledger_path(), payload, dry_run=args.dry_run)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not payload["errors"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
