"""Create v2 rescue/mutation candidates with lineage preserved."""
from __future__ import annotations

import argparse
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import artifact_dir, artifact_hashes, candidate_id, ensure_v2_dirs, read_json, write_run_artifact


def build_mutations(selected: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(review.get("candidate_id")): review for review in reviews}
    mutations: list[dict[str, Any]] = []
    for item in selected:
        cid = candidate_id(item)
        review = by_id.get(cid, {})
        if review.get("survivability_label") != "survives_if_mutated":
            continue
        mutation = dict(item)
        mutation["parent_candidate_id"] = cid
        mutation["candidate_id"] = f"{cid}-mut-{len(mutations) + 1}"
        mutation["state"] = "rescued_or_mutated"
        mutation["lineage"] = {
            "parent_candidate_id": cid,
            "mutation_reason": review.get("evaluation_attack") or review.get("rescue_mutation") or "requires mutation before promotion",
            "must_rescan_novelty": True,
            "must_rerun_codex_execution_review": True,
        }
        if review.get("rescue_mutation"):
            mutation["mechanism"] = f"{mutation.get('mechanism', '')} Mutation: {review['rescue_mutation']}".strip()
        mutations.append(mutation)
    return mutations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    selected_payload = read_json(artifact_dir(args.run_date) / "selected-candidates.json")
    deepseek_payload = read_json(artifact_dir(args.run_date) / "deepseek-review.json")
    mutations = build_mutations(selected_payload.get("selected", []), deepseek_payload.get("reviews", []))
    payload = {
        "schema_version": "gemini_mutations.v1",
        "run_date": args.run_date,
        "mutations": mutations,
        "artifact_hashes": artifact_hashes(args.run_date, ["selected-candidates.json", "deepseek-review.json"]),
        "boundary": "Mutated candidates are not promotable until novelty and Codex execution review reference the final mutated candidate id.",
    }
    write_run_artifact(args.run_date, "gemini-mutations.json", payload, state="rescued_or_mutated", dry_run=args.dry_run)
    safe_print(f"GEMINI_MUTATIONS: mutations={len(mutations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
