"""Record a manual governance review request for v1 active seed commitment."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from research_governance_common import artifact_hash, governance_review_dir, novelty_screen_dir, provider_review_dir, utc_now, write_json

def write_review(args: argparse.Namespace) -> dict:
    pr = getattr(args, "provider_review_path", "") or ""
    nv = getattr(args, "novelty_screen_path", "") or ""
    provider_path = Path(pr) if pr else provider_review_dir(args.candidate_id) / "provider-review-packet.json"
    novelty_path = Path(nv) if nv else novelty_screen_dir(args.candidate_id) / "novelty-screen.json"
    artifact_hashes = [entry for entry in (artifact_hash(provider_path), artifact_hash(novelty_path)) if entry["sha256"]]
    payload = {"schema_version": "governance_review.v1", "candidate_id": args.candidate_id, "title": args.title, "review_status": "requested", "owner": args.owner, "resource_budget": args.resource_budget, "timeline": args.timeline, "kill_criteria": args.kill_criteria, "human_confirmed": bool(args.human_confirmed), "confirmed_by": args.reviewer if args.human_confirmed else "", "confirmed_at": utc_now() if args.human_confirmed else "", "reviewer": args.reviewer, "reviewed_at": utc_now() if args.human_confirmed else "", "governance_signature": args.governance_signature, "created_at": utc_now(), "artifact_hashes": artifact_hashes, "boundary": "Governance review requests active commitment; active_seed_commit.py still performs the only active write."}
    write_json(governance_review_dir(args.candidate_id) / "governance-review.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--resource-budget", required=True)
    parser.add_argument("--timeline", required=True)
    parser.add_argument("--kill-criteria", required=True)
    parser.add_argument("--reviewer", default="human")
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--governance-signature", default="")
    parser.add_argument("--provider-review-path", default="")
    parser.add_argument("--novelty-screen-path", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = write_review(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["human_confirmed"] and payload["governance_signature"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
