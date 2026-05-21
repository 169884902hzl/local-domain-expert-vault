"""Write or validate a manual v1 prior-art dossier."""
from __future__ import annotations

import argparse
import json

from research_governance_common import prior_art_dir, read_json, utc_now, write_json


def write_dossier(args: argparse.Namespace) -> dict:
    payload = {"schema_version": "prior_art_dossier.v1", "candidate_id": args.candidate_id, "dossier_status": "completed" if args.human_confirmed else "draft", "reviewer": args.reviewer, "reviewed_at": utc_now() if args.human_confirmed else "", "human_confirmed": bool(args.human_confirmed), "confirmed_by": args.reviewer if args.human_confirmed else "", "confirmed_at": utc_now() if args.human_confirmed else "", "screening_only": bool(args.screening_only), "manual_sources": [item.strip() for item in args.manual_sources.split(";") if item.strip()], "nearest_work_summary": args.nearest_work_summary, "provider_timeout_seen": bool(args.provider_timeout_seen), "timeout_covered_by_manual_dossier": bool(args.timeout_covered_by_manual_dossier), "boundary": "Manual prior-art dossier. External scans are screening inputs only, not novelty proof."}
    write_json(prior_art_dir(args.candidate_id) / "manual-prior-art-dossier.json", payload, dry_run=args.dry_run)
    return payload


def validate_dossier(candidate_id: str) -> dict:
    payload = read_json(prior_art_dir(candidate_id) / "manual-prior-art-dossier.json")
    errors = []
    if payload.get("dossier_status") != "completed":
        errors.append("manual_prior_art_dossier_not_completed")
    if payload.get("human_confirmed") is not True:
        errors.append("manual_prior_art_dossier_not_human_confirmed")
    if payload.get("screening_only") is True:
        errors.append("prior_art_screening_not_dossier")
    return {"schema_version": "prior_art_dossier_validation.v1", "candidate_id": candidate_id, "status": "success" if not errors else "failed", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--reviewer", default="human")
    parser.add_argument("--manual-sources", default="")
    parser.add_argument("--nearest-work-summary", default="")
    parser.add_argument("--screening-only", action="store_true")
    parser.add_argument("--provider-timeout-seen", action="store_true")
    parser.add_argument("--timeout-covered-by-manual-dossier", action="store_true")
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = validate_dossier(args.candidate_id) if args.validate else write_dossier(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status", "success") == "success" or not args.validate else 1


if __name__ == "__main__":
    raise SystemExit(main())
