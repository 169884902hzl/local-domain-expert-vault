"""Build a v2 research claim graph from paper primitives."""
from __future__ import annotations

import argparse
import hashlib
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import (
    agenda_v2_path,
    artifact_dir,
    artifact_hashes,
    ensure_v2_dirs,
    load_jsonl,
    mark_state,
    normalize_text,
    write_jsonl,
)


PRIMITIVE_TO_CLAIM = {
    "central_claim": "central_claim",
    "method_assumption": "method_assumption",
    "strongest_baseline": "strongest_baseline",
    "actual_baseline_result": "actual_baseline_result",
    "missing_ablation": "missing_ablation",
    "evaluation_blind_spot": "evaluation_blind_spot",
    "interface_boundary": "interface_boundary",
    "transfer_failure": "transfer_failure",
    "reusable_primitive": "reusable_primitive",
    "contradiction": "contradiction",
}


def _node_id(paper_key: str, claim_type: str, statement: str) -> str:
    basis = f"{paper_key}|{claim_type}|{normalize_text(statement)}"
    return "claim-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def build_nodes(primitives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for paper in primitives:
        paper_key = str(paper.get("paper_key", ""))
        primitive_values = paper.get("primitives", {})
        confidence = paper.get("confidence", {})
        anchors = paper.get("anchors", {})
        for primitive_name, claim_type in PRIMITIVE_TO_CLAIM.items():
            statement = str(primitive_values.get(primitive_name, "")).strip()
            if not statement:
                continue
            anchor = anchors.get(primitive_name, {})
            conf = str(confidence.get(primitive_name, "low"))
            anchored = bool(
                anchor.get("anchor_type") in {"section", "snippet", "table", "figure"}
                and (anchor.get("snippet") or anchor.get("section") or anchor.get("anchor"))
            )
            if conf == "high" and not anchored:
                conf = "low"
            if primitive_name == "actual_baseline_result" and not anchor.get("snippet"):
                conf = "unusable"
            nodes.append(
                {
                    "schema_version": "research_claim_graph.v1",
                    "node_id": _node_id(paper_key, claim_type, statement),
                    "paper_key": paper_key,
                    "source_note": paper.get("source_note", ""),
                    "source_title": paper.get("source_title", ""),
                    "claim_type": claim_type,
                    "statement": statement,
                    "confidence": conf,
                    "anchor": anchor,
                    "supporting_node_ids": [],
                }
            )
    return sorted(nodes, key=lambda item: (item["paper_key"], item["claim_type"], item["node_id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    primitives_path = artifact_dir(args.run_date) / "paper-primitives-snapshot.jsonl"
    primitives = load_jsonl(primitives_path)
    nodes = build_nodes(primitives)
    snapshot_path = artifact_dir(args.run_date) / "claim-graph-snapshot.jsonl"
    write_jsonl(snapshot_path, nodes, dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "research_claim_graph.jsonl"), nodes, dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "paper_primitives.jsonl"), primitives, dry_run=args.dry_run)
    hashes = artifact_hashes(args.run_date, ["paper-primitives-snapshot.jsonl"])
    write_jsonl(artifact_dir(args.run_date) / "claim-graph-hashes.jsonl", [{"schema_version": "claim_graph_hashes.v1", "artifact_hashes": hashes}], dry_run=args.dry_run)
    mark_state(args.run_date, "claim_graph_built", "artifacts/claim-graph-snapshot.jsonl", dry_run=args.dry_run)
    safe_print(f"CLAIM_GRAPH: nodes={len(nodes)} primitives={len(primitives)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
