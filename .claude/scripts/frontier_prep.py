"""Prepare a frontier-direction -> representative-paper map for the frontier-map workflow.

Groups the 30 topic clusters into named frontier directions (hand-curated from cluster
inspection), pulls each cluster's centroid-representative papers, and resolves their
wiki/topics note paths from kb_meta so per-direction deep-read agents know exactly which
core papers to read. No LLM.
"""
from __future__ import annotations

import json

from kb_common import safe_print, vault_path

EV = vault_path("projects", "research-agenda", "evidence")
META = EV / "embeddings" / "kb_meta.jsonl"
CLUSTERS = EV / "topic_clusters.json"
OUT = EV / "frontier_directions.json"

# frontier direction -> cluster ids (curated from the 30-cluster inspection)
DIRECTIONS = {
    "VLA-foundation-generalization": [19, 1, 6, 20],
    "VLA-efficiency-test-time-rl": [0, 15, 29],
    "diffusion-flow-policy": [24, 3, 22],
    "world-model-for-manipulation": [21],
    "tactile-contact-rich": [18, 27, 7],
    "sim-to-real-real-to-sim": [9],
    "bimanual-dexterous-coordination": [2],
    "long-horizon-planning-embodied": [8, 26, 5],
    "spatial-3d-perception": [14, 4],
}


def main() -> int:
    meta = [json.loads(line) for line in META.read_text(encoding="utf-8").splitlines() if line.strip()]
    key_to_path = {m.get("zotero_key"): m.get("path") for m in meta if m.get("zotero_key")}
    clusters = {c["cluster_id"]: c for c in json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]}

    out = []
    for name, cids in DIRECTIONS.items():
        papers, seen = [], set()
        for cid in cids:
            cluster = clusters.get(cid, {})
            for rep in cluster.get("representatives", [])[:6]:
                key = rep.get("zotero_key")
                if key and key not in seen and key_to_path.get(key):
                    seen.add(key)
                    papers.append({"title": rep.get("title"), "path": key_to_path[key], "year": rep.get("year")})
        out.append({"direction": name, "clusters": cids, "papers": papers[:10]})
        safe_print(f"{name:34s} clusters={cids} papers={len(papers[:10])}")

    OUT.write_text(json.dumps({"schema_version": "frontier_directions.v1", "directions": out}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
