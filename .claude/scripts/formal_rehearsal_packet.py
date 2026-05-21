"""Build a v1 formal rehearsal packet without committing an active seed."""
from __future__ import annotations
import argparse, json
from research_governance_common import formal_rehearsal_dir, utc_now, write_json

def build_packet(args: argparse.Namespace) -> dict:
    payload = {"schema_version": "formal_rehearsal_packet.v1", "candidate_id": args.candidate_id, "packet_status": "ready", "created_at": utc_now(), "evidence_packet_confirmed": bool(args.evidence_packet_confirmed), "manual_prior_art_dossier_completed": bool(args.manual_prior_art_dossier_completed), "baseline_execution_ready": bool(args.baseline_execution_ready), "pilot_plan_ready": bool(args.pilot_plan_ready), "notes": args.notes, "active_seed_committed": False, "boundary": "Formal rehearsal packet is not an active seed and never writes governance active-seed records."}
    write_json(formal_rehearsal_dir(args.candidate_id) / "formal-rehearsal-packet.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--evidence-packet-confirmed", action="store_true")
    parser.add_argument("--manual-prior-art-dossier-completed", action="store_true")
    parser.add_argument("--baseline-execution-ready", action="store_true")
    parser.add_argument("--pilot-plan-ready", action="store_true")
    parser.add_argument("--notes", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_packet(args), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
