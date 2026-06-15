"""Prepare draft governance and experiment artifacts for a candidate without crossing human gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import novelty_screen
import plan_experiment
import provider_review_packet
from bootstrap_candidate_record import bootstrap_from_accepted
from evidence_packet_build import build_packet
from pilot_plan import write_plan as write_pilot_plan
from research_governance_common import active_commit_validation, read_json, utc_now


def prepare_candidate(args: argparse.Namespace) -> dict[str, Any]:
    if not args.human_initiated:
        return {"status": "blocked", "errors": ["missing_human_initiated_flag"]}
    candidate_id = args.candidate_id
    record = {}
    if args.from_accepted:
        record = bootstrap_from_accepted(Path(args.from_accepted), candidate_id=candidate_id, human_initiated=True, dry_run=args.dry_run)
        candidate_id = str(record["candidate_id"])
    if not candidate_id:
        return {"status": "blocked", "errors": ["missing_candidate_id"]}

    evidence = build_packet(candidate_id, run_id=args.run_id, dry_run=args.dry_run)
    query = plan_experiment.query_from_candidate(record) if record else plan_experiment.query_from_candidate_id(candidate_id)
    experiment = plan_experiment.plan_from_query(query, limit=args.limit, output=args.output or "", dry_run=args.dry_run)
    pilot = write_pilot_plan(
        argparse.Namespace(
            candidate_id=candidate_id,
            owner=args.owner,
            resource_budget=args.resource_budget,
            timeline=args.timeline,
            metric=args.metric,
            baseline_implementation_path=args.baseline_implementation_path,
            kill_criteria=args.kill_criteria,
            human_confirmed=False,
            dry_run=args.dry_run,
        )
    )
    provider = provider_review_packet.write_packet(
        argparse.Namespace(candidate_id=candidate_id, run_date=getattr(args, "run_date", ""), run_id=args.run_id, parent_candidate_id=getattr(args, "parent_candidate_id", ""), source_run_id="", validate=False, dry_run=args.dry_run)
    )
    novelty = novelty_screen.write_screen(
        argparse.Namespace(candidate_id=candidate_id, max_external_queries=getattr(args, "max_external_queries", 1), external_timeout=getattr(args, "external_timeout", 12), semantic_scholar_mode=getattr(args, "semantic_scholar_mode", "auto"), validate=False, dry_run=args.dry_run)
    )
    validation = active_commit_validation(candidate_id)
    status = "draft_prepared" if experiment.get("status") in {"success", "dry_run"} else "partial"
    return {
        "schema_version": "candidate_experiment_preparation.v1",
        "status": status,
        "candidate_id": candidate_id,
        "candidate_record_written": bool(record),
        "evidence_packet_status": evidence.get("packet_status"),
        "experiment": {key: value for key, value in experiment.items() if key != "content"},
        "pilot_plan_status": pilot.get("plan_status"),
        "provider_review_status": provider.get("review_status"),
        "novelty_screen_status": novelty.get("screen_status"),
        "active_commit_validation_ok": validation.ok,
        "active_commit_validation_errors": validation.errors,
        "generated_at": utc_now(),
        "boundary": "Draft preparation only; no evidence packet confirmation, governance review, or active seed commit is performed.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", default="")
    parser.add_argument("--from-accepted", default="")
    parser.add_argument("--human-initiated", action="store_true")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output", default="")
    parser.add_argument("--owner", default="human")
    parser.add_argument("--resource-budget", default="TO_CONFIRM")
    parser.add_argument("--timeline", default="TO_CONFIRM")
    parser.add_argument("--metric", default="TO_CONFIRM")
    parser.add_argument("--baseline-implementation-path", default="")
    parser.add_argument("--kill-criteria", default="TO_CONFIRM")
    parser.add_argument("--run-date", default="")
    parser.add_argument("--parent-candidate-id", default="")
    parser.add_argument("--max-external-queries", type=int, default=1)
    parser.add_argument("--external-timeout", type=int, default=12)
    parser.add_argument("--semantic-scholar-mode", default="auto")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = prepare_candidate(args)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == "draft_prepared" else 1


if __name__ == "__main__":
    raise SystemExit(main())
