"""Cluster the done-literature library into topic clusters via bge-m3 embeddings.

Reads the semantic index (kb_vectors.npy + kb_meta.jsonl), filters to literature
rows, runs k-means on the L2-normalized vectors (euclidean ~ cosine / spherical),
and emits per-cluster summaries (size / top tags / centroid-representative papers /
member keys) as the axis for the domain map. Deterministic given --seed. Read-only
except the single output JSON. No LLM.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

import numpy as np
from sklearn.cluster import KMeans

from kb_common import safe_print, vault_path

EMBED_DIR = vault_path("projects", "research-agenda", "evidence", "embeddings")
VECTORS = EMBED_DIR / "kb_vectors.npy"
META = EMBED_DIR / "kb_meta.jsonl"
OUT_JSON = vault_path("projects", "research-agenda", "evidence", "topic_clusters.json")

MAIN_KW = ("dlo", "deformable", "linear-object", "rope", "cable", "bimanual", "dual-arm", "vlm", "vla", "vision-language", "tactile", "sim-to-real", "sim2real")


def _is_main_tag(tag: str) -> bool:
    low = tag.lower()
    return any(kw in low for kw in MAIN_KW)


def load_literature() -> tuple[np.ndarray, list[dict]]:
    vectors = np.load(VECTORS)
    meta = [json.loads(line) for line in META.read_text(encoding="utf-8").splitlines() if line.strip()]
    keep = [i for i, m in enumerate(meta) if m.get("note_type") == "literature"]
    return vectors[np.array(keep)], [meta[i] for i in keep]


def summarize(vectors: np.ndarray, meta: list[dict], labels: np.ndarray, centers: np.ndarray, *, top_reps: int = 8, top_tags: int = 12) -> list[dict]:
    clusters = []
    for c in range(centers.shape[0]):
        members = [i for i, lab in enumerate(labels) if lab == c]
        if not members:
            continue
        center = centers[c] / (np.linalg.norm(centers[c]) + 1e-9)
        sims = vectors[members] @ center
        order = np.argsort(-sims)
        reps = [meta[members[o]] for o in order[:top_reps]]
        tags = Counter(t for i in members for t in (meta[i].get("tags") or []))
        main_hits = sum(1 for i in members for t in (meta[i].get("tags") or []) if _is_main_tag(t))
        clusters.append({
            "cluster_id": int(c),
            "size": len(members),
            "main_direction_score": int(main_hits),
            "top_tags": tags.most_common(top_tags),
            "representatives": [{"title": r.get("title"), "zotero_key": r.get("zotero_key"), "year": r.get("year"), "tags": r.get("tags") or []} for r in reps],
            "member_keys": [meta[i].get("zotero_key") for i in members],
        })
    clusters.sort(key=lambda x: (-x["main_direction_score"], -x["size"]))
    return clusters


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=30, help="Number of topic clusters.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--print-limit", type=int, default=30, help="How many clusters to print to stdout.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write the JSON.")
    args = parser.parse_args()

    vectors, meta = load_literature()
    km = KMeans(n_clusters=args.k, random_state=args.seed, n_init=10)
    labels = km.fit_predict(vectors)
    clusters = summarize(vectors, meta, labels, km.cluster_centers_)

    payload = {"schema_version": "topic_clusters.v1", "k": args.k, "seed": args.seed, "n_papers": int(vectors.shape[0]), "clusters": clusters}
    if not args.dry_run:
        OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    safe_print(f"=== topic clusters: k={args.k}, papers={vectors.shape[0]} (sorted by main-direction score) ===")
    for cl in clusters[: args.print_limit]:
        tag_str = ", ".join(f"{t}:{n}" for t, n in cl["top_tags"][:8])
        rep_str = " | ".join((r["title"] or "")[:42] for r in cl["representatives"][:3])
        safe_print(f"[C{cl['cluster_id']:>2}] n={cl['size']:>3} main={cl['main_direction_score']:>3}  {tag_str}")
        safe_print(f"        e.g. {rep_str}")
    if not args.dry_run:
        safe_print(f"\nwrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
