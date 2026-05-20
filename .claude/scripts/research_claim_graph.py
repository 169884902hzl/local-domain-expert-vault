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
CONFIDENCE_ORDER = {"unusable": 0, "low": 1, "medium": 2, "high": 3}
STRICT_ANCHOR_TYPES = {"section", "snippet", "table", "figure"}
EDGE_RELATIONS = {
    "supports",
    "contradicts",
    "limits",
    "exposes_gap",
    "baseline_for",
    "depends_on",
    "evaluates",
    "transfers_to",
}


def _node_id(paper_key: str, claim_type: str, statement: str) -> str:
    basis = f"{paper_key}|{claim_type}|{normalize_text(statement)}"
    return "claim-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _edge_id(source_node_id: str, target_node_id: str, relation: str) -> str:
    basis = f"{source_node_id}|{relation}|{target_node_id}"
    return "edge-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _strictly_anchored(anchor: dict[str, Any]) -> bool:
    return bool(
        anchor.get("anchor_type") in STRICT_ANCHOR_TYPES
        and (anchor.get("evidence_anchor") or anchor.get("anchor") or anchor.get("section") or anchor.get("snippet"))
    )


def _safe_confidence(value: Any) -> str:
    text = str(value or "low")
    return text if text in CONFIDENCE_ORDER else "low"


def _min_confidence(nodes: list[dict[str, Any]]) -> str:
    return min((_safe_confidence(node.get("confidence")) for node in nodes), key=lambda item: CONFIDENCE_ORDER[item])


def _legacy_claims(paper: dict[str, Any]) -> list[dict[str, Any]]:
    paper_key = str(paper.get("paper_key", ""))
    primitive_values = paper.get("primitives", {})
    confidence = paper.get("confidence", {})
    anchors = paper.get("anchors", {})
    claims: list[dict[str, Any]] = []
    for primitive_name, claim_type in PRIMITIVE_TO_CLAIM.items():
        statement = str(primitive_values.get(primitive_name, "")).strip()
        if not statement:
            continue
        anchor = anchors.get(primitive_name, {})
        claims.append(
            {
                "claim_id": _node_id(paper_key, claim_type, statement),
                "claim_type": claim_type,
                "statement": statement,
                "anchor": anchor,
                "evidence_anchor": anchor.get("evidence_anchor") or anchor.get("anchor") or "",
                "anchor_type": anchor.get("anchor_type", "note_only"),
                "confidence": confidence.get(primitive_name, "low"),
                "confidence_reason": "legacy_paper_primitives_record",
                "summary_origin": anchor.get("snippet_type", "legacy"),
                "requires_human_check": True,
                "domains": [],
            }
        )
    return claims


def _node_from_claim(paper: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    paper_key = str(paper.get("paper_key", ""))
    claim_type = str(claim.get("claim_type", ""))
    statement = str(claim.get("statement", "")).strip()
    anchor = dict(claim.get("anchor") or {})
    anchor.setdefault("evidence_anchor", claim.get("evidence_anchor", ""))
    anchor.setdefault("anchor", claim.get("evidence_anchor", ""))
    anchor.setdefault("anchor_type", claim.get("anchor_type", "note_only"))
    anchored = _strictly_anchored(anchor)
    conf = _safe_confidence(claim.get("confidence"))
    confidence_reason = str(claim.get("confidence_reason", ""))
    requires_human_check = bool(claim.get("requires_human_check", False))
    if conf == "high" and not anchored:
        conf = "low"
        confidence_reason = "high_confidence_requires_section_snippet_table_or_figure_anchor"
        requires_human_check = True
    if anchor.get("anchor_type") == "note_only" and conf in {"medium", "high"}:
        conf = "low"
        confidence_reason = "note_only_cannot_be_medium_or_high_confidence"
        requires_human_check = True
    if claim_type == "actual_baseline_result" and not anchored:
        conf = "unusable"
        confidence_reason = "actual_baseline_result_requires_strict_anchor"
        requires_human_check = True
    return {
        "schema_version": "research_claim_graph.v1",
        "record_type": "node",
        "node_id": _node_id(paper_key, claim_type, statement),
        "paper_key": paper_key,
        "source_note": paper.get("source_note", ""),
        "source_title": paper.get("source_title", ""),
        "claim_type": claim_type,
        "statement": statement,
        "confidence": conf,
        "confidence_reason": confidence_reason,
        "evidence_anchor": anchor.get("evidence_anchor") or anchor.get("anchor") or "",
        "anchor_type": anchor.get("anchor_type", "note_only"),
        "summary_origin": claim.get("summary_origin", ""),
        "requires_human_check": requires_human_check,
        "anchor": anchor,
        "domains": claim.get("domains", []),
        "supporting_node_ids": [],
    }


def build_nodes(primitives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for paper in primitives:
        claims = paper.get("claims") if isinstance(paper.get("claims"), list) else _legacy_claims(paper)
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            statement = str(claim.get("statement", "")).strip()
            if not statement:
                continue
            nodes.append(_node_from_claim(paper, claim))
    return sorted(nodes, key=lambda item: (item["paper_key"], item["claim_type"], item["node_id"]))


def _edge_record(source: dict[str, Any], target: dict[str, Any], relation: str, reason: str) -> dict[str, Any]:
    if relation not in EDGE_RELATIONS:
        raise ValueError(f"invalid_edge_relation:{relation}")
    confidence = _min_confidence([source, target])
    return {
        "schema_version": "research_claim_graph.v1",
        "record_type": "edge",
        "edge_id": _edge_id(str(source["node_id"]), str(target["node_id"]), relation),
        "paper_key": source.get("paper_key", ""),
        "source_node_id": source["node_id"],
        "target_node_id": target["node_id"],
        "relation": relation,
        "confidence": confidence,
        "confidence_reason": f"bounded_by_min_node_confidence:{reason}",
        "requires_human_check": bool(source.get("requires_human_check") or target.get("requires_human_check") or confidence in {"low", "unusable"}),
        "supporting_node_ids": [source["node_id"], target["node_id"]],
    }


def build_edges(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_paper: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        by_paper.setdefault(str(node.get("paper_key", "")), []).append(node)
    edges: list[dict[str, Any]] = []
    seen: set[str] = set()

    def first(items: list[dict[str, Any]], claim_type: str) -> dict[str, Any] | None:
        return next((node for node in items if node.get("claim_type") == claim_type), None)

    def add(source: dict[str, Any] | None, target: dict[str, Any] | None, relation: str, reason: str) -> None:
        if not source or not target or source.get("node_id") == target.get("node_id"):
            return
        edge = _edge_record(source, target, relation, reason)
        if edge["edge_id"] in seen:
            return
        seen.add(str(edge["edge_id"]))
        edges.append(edge)

    for _paper_key, items in sorted(by_paper.items()):
        central = first(items, "central_claim")
        method = first(items, "method_assumption")
        baseline = first(items, "strongest_baseline")
        result = first(items, "actual_baseline_result")
        missing_ablation = first(items, "missing_ablation")
        blind_spot = first(items, "evaluation_blind_spot")
        interface = first(items, "interface_boundary")
        transfer_failure = first(items, "transfer_failure")
        reusable = first(items, "reusable_primitive")
        contradiction = first(items, "contradiction")
        latent = first(items, "unmodeled_latent_variable")

        add(method, central, "depends_on", "method_assumption_supports_central_claim")
        add(baseline, central, "baseline_for", "strongest_baseline_for_central_claim")
        add(result, baseline or central, "evaluates", "actual_baseline_result_evaluates_baseline_or_claim")
        add(missing_ablation, central or method, "exposes_gap", "missing_ablation_exposes_gap")
        add(blind_spot, central or method, "limits", "evaluation_blind_spot_limits_claim_scope")
        add(latent, central or method, "limits", "unmodeled_latent_variable_limits_claim_scope")
        add(transfer_failure, reusable or method or central, "limits", "transfer_failure_limits_reuse")
        add(contradiction, method, "contradicts", "contradiction_against_method_assumption")
        if reusable and (interface or reusable.get("domains") or (central and central.get("domains"))):
            add(reusable, interface or central, "transfers_to", "reusable_primitive_transfers_to_target_domain_or_task")
    return sorted(edges, key=lambda item: (item["paper_key"], item["relation"], item["edge_id"]))


def build_graph_records(primitives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes = build_nodes(primitives)
    node_ids = {str(node["node_id"]) for node in nodes}
    edges = [
        edge
        for edge in build_edges(nodes)
        if edge.get("source_node_id") in node_ids and edge.get("target_node_id") in node_ids
    ]
    return nodes + edges


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    primitives_path = artifact_dir(args.run_date) / "paper-primitives-snapshot.jsonl"
    primitives = load_jsonl(primitives_path)
    records = build_graph_records(primitives)
    nodes = [record for record in records if record.get("record_type") == "node"]
    edges = [record for record in records if record.get("record_type") == "edge"]
    snapshot_path = artifact_dir(args.run_date) / "claim-graph-snapshot.jsonl"
    write_jsonl(snapshot_path, records, dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "research_claim_graph.jsonl"), records, dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "paper_primitives.jsonl"), primitives, dry_run=args.dry_run)
    hashes = artifact_hashes(args.run_date, ["paper-primitives-snapshot.jsonl"])
    write_jsonl(artifact_dir(args.run_date) / "claim-graph-hashes.jsonl", [{"schema_version": "claim_graph_hashes.v1", "artifact_hashes": hashes}], dry_run=args.dry_run)
    mark_state(args.run_date, "claim_graph_built", "artifacts/claim-graph-snapshot.jsonl", dry_run=args.dry_run)
    safe_print(f"CLAIM_GRAPH: nodes={len(nodes)} edges={len(edges)} primitives={len(primitives)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
