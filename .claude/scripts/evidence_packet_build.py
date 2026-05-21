"""Build a draft v1 evidence packet for a candidate."""
from __future__ import annotations

import argparse
import json

from research_governance_common import candidate_dir, evidence_packet_dir, read_json, utc_now, write_json


def build_packet(candidate_id: str, *, run_id: str = "", dry_run: bool = False) -> dict:
    candidate = read_json(candidate_dir(candidate_id) / "candidate-record.json")
    payload = {"schema_version": "evidence_packet.v1", "candidate_id": candidate_id, "run_id": run_id, "packet_status": "draft", "created_at": utc_now(), "core_evidence": candidate.get("draft_evidence", []), "human_confirmed": False, "confirmed_by": "", "confirmed_at": "", "boundary": "Draft evidence packet; scheduled automation cannot use it for active commit."}
    write_json(evidence_packet_dir(candidate_id) / "evidence-packet.draft.json", payload, dry_run=dry_run)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_packet(args.candidate_id, run_id=args.run_id, dry_run=args.dry_run), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
