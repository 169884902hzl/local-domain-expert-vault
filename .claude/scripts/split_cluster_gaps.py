"""Split distilled_gaps.json into per-cluster files (merged with cluster representatives).

Each output file C<id>.json bundles a cluster's distilled gaps + top tags + representative
papers, so a fan-out agent can read just its own cluster instead of the whole 682-gap file.
No LLM.
"""
from __future__ import annotations

import json

from kb_common import safe_print, vault_path

EV = vault_path("projects", "research-agenda", "evidence")
OUTDIR = EV / "cluster_gaps"


def main() -> int:
    dg = json.loads((EV / "distilled_gaps.json").read_text(encoding="utf-8"))
    tc = {c["cluster_id"]: c for c in json.loads((EV / "topic_clusters.json").read_text(encoding="utf-8"))["clusters"]}
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for c in dg["clusters"]:
        cid = c["cluster_id"]
        reps = tc.get(cid, {}).get("representatives", [])[:10]
        out = {
            "cluster_id": cid,
            "papers": c.get("papers"),
            "top_tags": c.get("top_tags"),
            "representatives": reps,
            "distilled_gaps": c.get("distilled_gaps", []),
        }
        (OUTDIR / f"C{cid:02d}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_print(f"wrote {len(dg['clusters'])} cluster gap files to {OUTDIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
