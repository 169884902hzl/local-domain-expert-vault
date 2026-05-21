"""Create a v1 nearest-work matrix from screening evidence."""
from __future__ import annotations
import argparse, json
from research_governance_common import nearest_work_dir, utc_now, write_json

def build_matrix(args: argparse.Namespace) -> dict:
    works = []
    for raw in [item for item in args.work if item.strip()]:
        parts = [part.strip() for part in raw.split("|")]
        works.append({"title": parts[0] if parts else raw, "locator": parts[1] if len(parts) > 1 else "", "overlap": parts[2] if len(parts) > 2 else "", "screening_source": parts[3] if len(parts) > 3 else "manual"})
    payload = {"schema_version": "nearest_work_matrix.v1", "candidate_id": args.candidate_id, "created_at": utc_now(), "works": works, "boundary": "Nearest-work matrix is screening context only. It is not a manual prior-art dossier or novelty proof."}
    write_json(nearest_work_dir(args.candidate_id) / "nearest-work-matrix.json", payload, dry_run=args.dry_run)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--work", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_matrix(args), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
