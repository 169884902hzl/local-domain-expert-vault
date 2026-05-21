"""Manually confirm a v1 evidence packet."""
from __future__ import annotations

import argparse
import json

from research_governance_common import evidence_packet_dir, read_json, utc_now, write_json


def confirm_packet(candidate_id: str, *, confirmed_by: str, human_confirmed: bool, dry_run: bool = False) -> dict:
    payload = read_json(evidence_packet_dir(candidate_id) / "evidence-packet.draft.json") or {"schema_version": "evidence_packet.v1", "candidate_id": candidate_id, "core_evidence": []}
    payload.setdefault("artifact_hashes", [])
    payload.update({"packet_status": "confirmed" if human_confirmed else "draft", "human_confirmed": bool(human_confirmed), "confirmed_by": confirmed_by if human_confirmed else "", "confirmed_at": utc_now() if human_confirmed else "", "boundary": "Human-confirmed evidence packet; still not active without dossier, baseline, pilot, and governance review."})
    write_json(evidence_packet_dir(candidate_id) / "evidence-packet.confirmed.json", payload, dry_run=dry_run)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--confirmed-by", required=True)
    parser.add_argument("--human-confirmed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = confirm_packet(args.candidate_id, confirmed_by=args.confirmed_by, human_confirmed=args.human_confirmed, dry_run=args.dry_run)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["human_confirmed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
