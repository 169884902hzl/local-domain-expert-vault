"""Create a v1 pilot plan required before active seed commitment."""
from __future__ import annotations
import argparse, json
from research_governance_common import pilot_plan_dir, utc_now, write_json

def write_plan(args: argparse.Namespace) -> dict:
    payload = {"schema_version": "pilot_plan.v1", "candidate_id": args.candidate_id, "plan_status": "ready" if args.human_confirmed else "draft", "owner": args.owner, "resource_budget": args.resource_budget, "timeline": args.timeline, "metric": args.metric, "baseline_implementation_path": args.baseline_implementation_path, "kill_criteria": args.kill_criteria, "human_confirmed": bool(args.human_confirmed), "confirmed_by": args.owner if args.human_confirmed else "", "confirmed_at": utc_now() if args.human_confirmed else "", "created_at": utc_now(), "boundary": "Pilot plan readiness is not active seed commitment and does not promote a candidate."}
    write_json(pilot_plan_dir(args.candidate_id) / "pilot-plan.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--resource-budget", required=True)
    parser.add_argument("--timeline", required=True)
    parser.add_argument("--metric", required=True)
    parser.add_argument("--baseline-implementation-path", default="")
    parser.add_argument("--kill-criteria", required=True)
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = write_plan(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["plan_status"] == "ready" else 1

if __name__ == "__main__":
    raise SystemExit(main())
