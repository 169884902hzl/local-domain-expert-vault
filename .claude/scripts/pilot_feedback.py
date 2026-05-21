"""Record pilot plans, outcomes, and proposed strategy feedback for v0.3 seeds.

In v1, pilot feedback cannot promote, kill, resurrect, or update strategy by
itself. Applied strategy updates require strategy_ledger.py --apply
--human-confirmed.
"""
from __future__ import annotations

import argparse
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import agenda_v2_path, ensure_v2_dirs, read_json, utc_now, write_json


PILOT_STATUSES = {"planned", "running", "completed", "killed"}
PILOT_RESULTS = {"positive", "negative", "inconclusive", "blocked"}
FAILURE_REASONS = {
    "baseline_killed",
    "no_signal",
    "metric_failed",
    "implementation_blocked",
    "generator_signal_failure",
    "gate_false_positive",
    "gate_false_negative",
    "data_unavailable",
    "hardware_blocked",
    "unknown",
}
FORBIDDEN_STRATEGY_KEYS = {
    "disable_novelty_gate",
    "allow_unknown_novelty_seed",
    "disable_deepseek",
    "codex_accept_not_required",
    "allow_anchorless_formal_seed",
    "allow_stale_external_cache",
    "allow_codex_reject",
}


def pilot_dir(seed_slug: str):
    return agenda_v2_path("pilots", seed_slug)


def _plan_path(seed_slug: str):
    return pilot_dir(seed_slug) / "pilot-plan.json"


def _result_path(seed_slug: str):
    return pilot_dir(seed_slug) / "result.json"


def _feedback_path(seed_slug: str):
    return pilot_dir(seed_slug) / "feedback-to-strategy.json"


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _sanitize_strategy_update(update: dict[str, Any]) -> dict[str, Any]:
    sanitized = {
        "penalize_patterns": list(update.get("penalize_patterns", [])),
        "boost_patterns": list(update.get("boost_patterns", [])),
        "required_future_checks": list(update.get("required_future_checks", [])),
        "cannot_weaken_hard_gates": True,
    }
    for key in FORBIDDEN_STRATEGY_KEYS:
        sanitized.pop(key, None)
    return sanitized


def write_pilot_plan(args: argparse.Namespace) -> dict[str, Any]:
    ensure_v2_dirs()
    payload = {
        "schema_version": "pilot_plan.v1",
        "seed_slug": args.seed_slug,
        "candidate_id": args.candidate_id,
        "pilot_status": "planned",
        "created_at": utc_now(),
        "metric": args.metric,
        "metric_automation": args.metric_automation,
        "baseline_implementation_path": args.baseline_implementation_path,
        "resource_budget": args.resource_budget,
        "executable": bool(args.executable),
        "constraints": {
            "raw_modified": False,
            "auto_promote_formal_seed": False,
            "cannot_weaken_hard_gates": True,
        },
    }
    write_json(_plan_path(args.seed_slug), payload, dry_run=args.dry_run)
    return payload


def _feedback_from_result(result: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    update = {
        "penalize_patterns": _split_csv(args.penalize_patterns),
        "boost_patterns": _split_csv(args.boost_patterns),
        "required_future_checks": _split_csv(args.required_future_checks),
    }
    if result.get("failure_reason") in {
        "baseline_killed",
        "no_signal",
        "metric_failed",
        "implementation_blocked",
        "generator_signal_failure",
        "gate_false_positive",
        "gate_false_negative",
        "data_unavailable",
    }:
        update["required_future_checks"].append(str(result["failure_reason"]))
    if result.get("result") in {"negative", "blocked"}:
        update["penalize_patterns"].append(str(result.get("failure_reason") or "unknown_pilot_failure"))
    if result.get("result") == "positive":
        update["boost_patterns"].append("pilot_positive_signal")
    return {
        "schema_version": "pilot_feedback.v1",
        "seed_slug": result["seed_slug"],
        "candidate_id": result["candidate_id"],
        "pilot_status": result["pilot_status"],
        "result": result["result"],
        "failure_reason": result["failure_reason"],
        "baseline_result": result["baseline_result"],
        "metric_outcome": result["metric_outcome"],
        "what_generator_predicted_wrong": result["what_generator_predicted_wrong"],
        "strategy_update": _sanitize_strategy_update(update),
        "applied": False,
        "boundaries": {
            "raw_modified": False,
            "seed_deleted": False,
            "auto_promoted": False,
            "cannot_weaken_hard_gates": True,
            "requires_strategy_ledger_apply": True,
        },
    }


def write_pilot_result(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    ensure_v2_dirs()
    plan = read_json(_plan_path(args.seed_slug)) if _plan_path(args.seed_slug).exists() else {}
    payload = {
        "schema_version": "pilot_feedback.v1",
        "seed_slug": args.seed_slug,
        "candidate_id": args.candidate_id or plan.get("candidate_id", ""),
        "pilot_status": args.pilot_status,
        "result": args.result,
        "failure_reason": args.failure_reason,
        "baseline_result": args.baseline_result,
        "metric_outcome": args.metric_outcome,
        "what_generator_predicted_wrong": args.what_generator_predicted_wrong,
        "recorded_at": utc_now(),
        "state_action": "archive_feedback_only" if args.pilot_status == "killed" else "record_feedback_only",
        "constraints": {
            "raw_modified": False,
            "seed_deleted": False,
            "auto_promote_formal_seed": False,
            "cannot_weaken_hard_gates": True,
        },
    }
    feedback = _feedback_from_result(payload, args)
    write_json(_result_path(args.seed_slug), payload, dry_run=args.dry_run)
    write_json(_feedback_path(args.seed_slug), feedback, dry_run=args.dry_run)
    return payload, feedback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    plan = sub.add_parser("plan", help="Write an executable pilot plan skeleton for an active-seed candidate.")
    plan.add_argument("--seed-slug", required=True)
    plan.add_argument("--candidate-id", required=True)
    plan.add_argument("--metric", required=True)
    plan.add_argument("--baseline-implementation-path", required=True)
    plan.add_argument("--resource-budget", required=True)
    plan.add_argument("--metric-automation", default="")
    plan.add_argument("--executable", action="store_true")
    plan.add_argument("--dry-run", action="store_true")

    result = sub.add_parser("result", help="Record pilot outcome and strategy calibration feedback.")
    result.add_argument("--seed-slug", required=True)
    result.add_argument("--candidate-id", default="")
    result.add_argument("--pilot-status", choices=sorted(PILOT_STATUSES), required=True)
    result.add_argument("--result", choices=sorted(PILOT_RESULTS), required=True)
    result.add_argument("--failure-reason", choices=sorted(FAILURE_REASONS), default="unknown")
    result.add_argument("--baseline-result", default="")
    result.add_argument("--metric-outcome", default="")
    result.add_argument("--what-generator-predicted-wrong", default="")
    result.add_argument("--penalize-patterns", default="")
    result.add_argument("--boost-patterns", default="")
    result.add_argument("--required-future-checks", default="")
    result.add_argument("--dry-run", action="store_true")

    legacy = sub.add_parser("legacy-feedback", help="Compatibility wrapper for the old pilot feedback command.")
    legacy.add_argument("--seed-slug", required=True)
    legacy.add_argument("--outcome", choices=["pilot_ready", "needs_revision", "killed"], required=True)
    legacy.add_argument("--evidence", default="")
    legacy.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "plan":
        payload = write_pilot_plan(args)
        safe_print(f"PILOT_PLAN: seed={payload['seed_slug']} candidate={payload['candidate_id']}")
        return 0
    if args.command == "result":
        payload, _feedback = write_pilot_result(args)
        safe_print(f"PILOT_RESULT: seed={payload['seed_slug']} result={payload['result']}")
        return 0
    if args.command == "legacy-feedback":
        status = "killed" if args.outcome == "killed" else "completed"
        result = "positive" if args.outcome == "pilot_ready" else "inconclusive"
        legacy_args = argparse.Namespace(
            seed_slug=args.seed_slug,
            candidate_id="",
            pilot_status=status,
            result=result,
            failure_reason="unknown",
            baseline_result="",
            metric_outcome=args.evidence,
            what_generator_predicted_wrong="",
            penalize_patterns="",
            boost_patterns="pilot_ready" if args.outcome == "pilot_ready" else "",
            required_future_checks="manual_followup" if args.outcome == "needs_revision" else "",
            dry_run=args.dry_run,
        )
        payload, _feedback = write_pilot_result(legacy_args)
        safe_print(f"PILOT_FEEDBACK: seed={payload['seed_slug']} result={payload['result']}")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
