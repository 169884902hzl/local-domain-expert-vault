"""Build per-cluster claim-graph + tension-map for topic clusters (deterministic gap fuel).

For each selected topic cluster, assemble a paper-primitives snapshot from the cluster's
member paper-primitives/<key>.json, then run research_claim_graph + tension_map on an
isolated run-date so cross-paper edges stay within-topic (keeps the O(n^2) bounded by
cluster size and makes tensions topic-coherent). Emits a gap index pointing at each
cluster's tension-map for the downstream multi-agent gap synthesis. No LLM.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter

from kb_common import safe_print, vault_path
from research_seed_v2_common import artifact_dir

PP_DIR = vault_path("projects", "research-agenda", "paper-primitives")
CLUSTERS = vault_path("projects", "research-agenda", "evidence", "topic_clusters.json")
SCRIPTS = vault_path(".claude", "scripts")
OUT = vault_path("projects", "research-agenda", "evidence", "cluster_gap_index.json")


def build_snapshot(member_keys: list[str], run_date: str) -> tuple[int, int]:
    art = artifact_dir(run_date)
    art.mkdir(parents=True, exist_ok=True)
    lines, missing = [], 0
    for key in member_keys:
        pp = PP_DIR / f"{key}.json"
        if pp.exists():
            lines.append(json.dumps(json.loads(pp.read_text(encoding="utf-8")), ensure_ascii=False))
        else:
            missing += 1
    (art / "paper-primitives-snapshot.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines), missing


def run_script(name: str, run_date: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / name), "--run-date", run_date], capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cluster-ids", default="", help="Comma-separated cluster ids; empty = use --min-main-score.")
    parser.add_argument("--min-main-score", type=int, default=25)
    parser.add_argument("--run-prefix", default="mapcluster")
    args = parser.parse_args()

    data = json.loads(CLUSTERS.read_text(encoding="utf-8"))
    if args.cluster_ids.strip():
        wanted = {int(x) for x in args.cluster_ids.split(",") if x.strip()}
        selected = [c for c in data["clusters"] if c["cluster_id"] in wanted]
    else:
        selected = [c for c in data["clusters"] if c["main_direction_score"] >= args.min_main_score]

    index = []
    for cl in selected:
        run_date = f"{args.run_prefix}-{cl['cluster_id']:02d}"
        n, missing = build_snapshot(cl["member_keys"], run_date)
        cg = run_script("research_claim_graph.py", run_date)
        tm = run_script("tension_map.py", run_date)
        tmap_path = artifact_dir(run_date) / "tension-map.json"
        tcount, ttypes = 0, {}
        if tmap_path.exists():
            tmj = json.loads(tmap_path.read_text(encoding="utf-8"))
            tensions = tmj.get("tensions", [])
            tcount = len(tensions)
            ttypes = dict(Counter(t.get("tension_type") for t in tensions))
        index.append({
            "cluster_id": cl["cluster_id"],
            "run_date": run_date,
            "papers": n,
            "missing": missing,
            "tensions": tcount,
            "tension_types": ttypes,
            "tension_map": str(tmap_path),
            "top_tags": cl["top_tags"][:6],
            "main_direction_score": cl["main_direction_score"],
            "cg_rc": cg.returncode,
            "tm_rc": tm.returncode,
        })
        safe_print(f"[C{cl['cluster_id']:>2}] papers={n} missing={missing} tensions={tcount}  cg_rc={cg.returncode} tm_rc={tm.returncode}")
        if cg.returncode or tm.returncode:
            safe_print(f"     cg_err={(cg.stderr or '')[-220:]}")
            safe_print(f"     tm_err={(tm.stderr or '')[-220:]}")

    failures = sum(1 for c in index if c.get("cg_rc", 0) != 0 or c.get("tm_rc", 0) != 0)
    OUT.write_text(json.dumps({"schema_version": "cluster_gap_index.v1", "clusters": index, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_print(f"\nwrote {OUT}  ({len(index)} clusters, {sum(c['tensions'] for c in index)} total tensions, {failures} failures)")
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
