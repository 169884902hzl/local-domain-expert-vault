"""Record v1 baseline execution readiness for a candidate."""
from __future__ import annotations
import argparse, json
from research_governance_common import baseline_readiness_dir, utc_now, write_json

def write_readiness(args: argparse.Namespace) -> dict:
    payload = {"schema_version": "baseline_execution_readiness.v1", "candidate_id": args.candidate_id, "readiness_status": args.status, "baseline_name": args.baseline_name, "implementation_path": args.implementation_path, "resource_budget": args.resource_budget, "not_applicable_reason": args.not_applicable_reason, "blocking_issues": [item.strip() for item in args.blocking_issue if item.strip()], "created_at": utc_now(), "boundary": "Baseline readiness is required for active commit; nearest work alone is insufficient."}
    write_json(baseline_readiness_dir(args.candidate_id) / "baseline-execution-readiness.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--status", choices=["ready", "partial", "unknown", "prohibitive", "not_applicable"], default="unknown")
    parser.add_argument("--baseline-name", default="")
    parser.add_argument("--implementation-path", default="")
    parser.add_argument("--resource-budget", default="")
    parser.add_argument("--not-applicable-reason", default="")
    parser.add_argument("--blocking-issue", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = write_readiness(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["readiness_status"] in {"ready", "not_applicable"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
