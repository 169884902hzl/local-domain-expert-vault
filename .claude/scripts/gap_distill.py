"""Distill per-cluster tensions into a high-value gap shortlist for multi-agent synthesis.

Reads cluster_gap_index.json, loads each cluster's tension-map.json, keeps only audited
non-do_not_use tensions (the claim-graph quality gate; everything else is O(n^2)
medium-confidence noise), ranks high-value tension types above the analogy/blind-spot
chaff, sorts by support breadth, dedups by supporting-node overlap, and emits a top-K
per-cluster shortlist as the gap-synthesis input. No LLM.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kb_common import safe_print, vault_path

INDEX = vault_path("projects", "research-agenda", "evidence", "cluster_gap_index.json")
OUT = vault_path("projects", "research-agenda", "evidence", "distilled_gaps.json")

TYPE_WEIGHT = {
    "missing_latent_variable": 5,
    "interface_boundary_mismatch": 4,
    "benchmark_gap": 3,
    "negative_result_opportunity": 3,
    "evaluation_blind_spot": 1,
    "external_analogy_opportunity": 1,
}


def distill(tension_map_path: str, top_k: int) -> list[dict]:
    path = Path(tension_map_path)
    if not path.exists():
        return []
    tensions = json.loads(path.read_text(encoding="utf-8")).get("tensions", [])
    kept = [t for t in tensions if t.get("edge_quality_status") == "audited" and not t.get("do_not_use_as_seed_evidence")]

    def score(t):
        return (TYPE_WEIGHT.get(t.get("tension_type"), 1), 2 if t.get("confidence") == "high" else 1, len(t.get("supporting_nodes") or []))

    kept.sort(key=score, reverse=True)
    seen, out = [], []
    for t in kept:
        nodes = frozenset(t.get("supporting_nodes") or [])
        if nodes and any(len(nodes & s) / len(nodes | s) > 0.6 for s in seen):
            continue
        seen.append(nodes)
        out.append({
            "tension_type": t.get("tension_type"),
            "confidence": t.get("confidence"),
            "support": len(t.get("supporting_nodes") or []),
            "summary": (t.get("summary") or "").strip(),
        })
        if len(out) >= top_k:
            break
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top-k", type=int, default=40, help="Max distilled gaps per cluster.")
    args = parser.parse_args()

    index = json.loads(INDEX.read_text(encoding="utf-8"))["clusters"]
    clusters = []
    for entry in index:
        gaps = distill(entry["tension_map"], args.top_k)
        clusters.append({
            "cluster_id": entry["cluster_id"],
            "main_direction_score": entry.get("main_direction_score"),
            "papers": entry.get("papers"),
            "top_tags": entry.get("top_tags"),
            "raw_tensions": entry.get("tensions"),
            "distilled_gaps": gaps,
        })
        safe_print(f"[C{entry['cluster_id']:>2}] raw={entry.get('tensions'):>6} -> distilled={len(gaps)}")
    OUT.write_text(json.dumps({"schema_version": "distilled_gaps.v1", "top_k": args.top_k, "clusters": clusters}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_print(f"\nwrote {OUT}  ({sum(len(c['distilled_gaps']) for c in clusters)} gaps across {len(clusters)} clusters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
