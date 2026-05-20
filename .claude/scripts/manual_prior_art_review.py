"""Create, validate, and summarize human manual prior-art reviews."""
from __future__ import annotations

import argparse
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import artifact_dir, ensure_v2_dirs, read_json, utc_now, validate_json_file, write_run_artifact


REQUIRED_CANNOT_WEAKEN = [
    "deepseek_success_required",
    "codex_accept_required",
    "external_novelty_required",
    "anchored_core_evidence_required",
    "no_unresolved_fatal_flaw",
    "fresh_external_cache_required",
]


def review_path(run_date: str):
    return artifact_dir(run_date) / "manual-prior-art-review.json"


def empty_payload(run_date: str) -> dict[str, Any]:
    return {
        "schema_version": "manual_prior_art_review.v1",
        "run_date": run_date,
        "reviews": [],
        "boundary": "Human prior-art review records risk; it cannot weaken hard gates.",
    }


def load_payload(run_date: str) -> dict[str, Any]:
    path = review_path(run_date)
    return read_json(path) if path.exists() else empty_payload(run_date)


def template_review(candidate_id: str) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "review_status": "template",
        "reviewer": "human",
        "reviewed_at": "",
        "decision": "needs_more_search",
        "searched_sources": [],
        "search_queries": [],
        "nearest_works": [],
        "explicit_no_near_work_reason": "",
        "strongest_baseline_judgment": {
            "status": "unknown",
            "baseline_name": "",
            "source_work_id": "",
            "source": "",
            "why_strongest": "",
            "kill_condition": "",
            "metric_or_task": "",
            "implementation_feasibility": "unknown",
        },
        "known_overlap_risk": "unknown",
        "remaining_delta": "",
        "reason": "",
        "limitations": "",
        "risk_acceptance": "",
        "cannot_weaken": REQUIRED_CANNOT_WEAKEN,
    }


def write_template(run_date: str, candidate_id: str, *, dry_run: bool = False) -> dict[str, Any]:
    ensure_v2_dirs(run_date)
    payload = load_payload(run_date)
    reviews = [item for item in payload.get("reviews", []) if item.get("candidate_id") != candidate_id]
    reviews.append(template_review(candidate_id))
    payload["reviews"] = sorted(reviews, key=lambda item: str(item.get("candidate_id", "")))
    write_run_artifact(run_date, "manual-prior-art-review.json", payload, state="manual_prior_art_template_written", dry_run=dry_run)
    return payload


def completion_errors(review: dict[str, Any]) -> list[str]:
    cid = str(review.get("candidate_id", ""))
    errors: list[str] = []
    if review.get("review_status") != "completed":
        return [f"{cid}:manual_prior_art_review_template_not_completed"]
    if review.get("reviewer") != "human":
        errors.append(f"{cid}:reviewer_not_human")
    if review.get("decision") not in {"allow_active_seed", "park", "reject"}:
        errors.append(f"{cid}:completed_decision_not_final")
    if not review.get("searched_sources"):
        errors.append(f"{cid}:searched_sources_empty")
    if not review.get("search_queries"):
        errors.append(f"{cid}:search_queries_empty")
    if not review.get("nearest_works") and not str(review.get("explicit_no_near_work_reason", "")).strip():
        errors.append(f"{cid}:nearest_works_or_explicit_no_near_work_reason_required")
    judgment = review.get("strongest_baseline_judgment", {}) if isinstance(review.get("strongest_baseline_judgment"), dict) else {}
    if not str(judgment.get("status", "")).strip():
        errors.append(f"{cid}:strongest_baseline_status_missing")
    if judgment.get("status") == "known":
        for field in ["baseline_name", "why_strongest", "kill_condition", "metric_or_task"]:
            if not str(judgment.get(field, "")).strip():
                errors.append(f"{cid}:strongest_baseline_{field}_missing")
    for field in ["remaining_delta", "risk_acceptance", "reason"]:
        if not str(review.get(field, "")).strip():
            errors.append(f"{cid}:{field}_missing")
    cannot_weaken = set(str(item) for item in review.get("cannot_weaken", []))
    missing = [item for item in REQUIRED_CANNOT_WEAKEN if item not in cannot_weaken]
    if missing:
        errors.append(f"{cid}:cannot_weaken_missing:{','.join(missing)}")
    return errors


def validate_reviews(run_date: str) -> tuple[dict[str, Any], list[str]]:
    payload = load_payload(run_date)
    errors = validate_json_file(review_path(run_date), "manual_prior_art_review.v1") if review_path(run_date).exists() else ["manual_prior_art_review_missing"]
    for review in payload.get("reviews", []):
        if isinstance(review, dict) and review.get("review_status") == "completed":
            errors.extend(completion_errors(review))
    return payload, errors


def completed_review_by_candidate(run_date: str) -> dict[str, dict[str, Any]]:
    payload = load_payload(run_date)
    completed: dict[str, dict[str, Any]] = {}
    for review in payload.get("reviews", []):
        if not isinstance(review, dict) or completion_errors(review):
            continue
        completed[str(review.get("candidate_id"))] = review
    return completed


def active_seed_review_allowed(review: dict[str, Any] | None) -> bool:
    return bool(review and not completion_errors(review) and review.get("decision") == "allow_active_seed")


def summarize(run_date: str) -> dict[str, Any]:
    payload = load_payload(run_date)
    reviews = payload.get("reviews", [])
    completed = [item for item in reviews if isinstance(item, dict) and not completion_errors(item)]
    active_allowed = [item for item in completed if item.get("decision") == "allow_active_seed"]
    return {
        "schema_version": "manual_prior_art_review_summary.v1",
        "run_date": run_date,
        "reviews": len(reviews),
        "completed_reviews": len(completed),
        "active_seed_allowed_reviews": len(active_allowed),
        "candidate_ids": [str(item.get("candidate_id")) for item in reviews if isinstance(item, dict)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--candidate-id", default="")
    parser.add_argument("--write-template", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.write_template:
        if not args.candidate_id:
            parser.error("--write-template requires --candidate-id")
        write_template(args.run_date, args.candidate_id, dry_run=args.dry_run)
        safe_print(f"MANUAL_PRIOR_ART_TEMPLATE: run_date={args.run_date} candidate_id={args.candidate_id}")
        return 0
    if args.validate:
        _payload, errors = validate_reviews(args.run_date)
        safe_print(f"MANUAL_PRIOR_ART_VALIDATE: errors={len(errors)}")
        for error in errors:
            safe_print(f"- {error}")
        return 0 if not errors else 2
    if args.summarize:
        summary = summarize(args.run_date)
        safe_print(str(summary))
        return 0
    parser.error("choose one of --write-template, --validate, or --summarize")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
