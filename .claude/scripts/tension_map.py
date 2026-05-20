"""Build and validate v2 research tensions from the claim graph."""
from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import artifact_dir, artifact_hashes, ensure_v2_dirs, load_jsonl, normalize_text, write_run_artifact, write_text


TENSION_TYPES = [
    "assumption_conflict",
    "evaluation_blind_spot",
    "missing_latent_variable",
    "interface_boundary_mismatch",
    "baseline_contradiction",
    "data_distribution_pathology",
    "lab_specific_engineering_bottleneck",
    "external_analogy_opportunity",
    "negative_result_opportunity",
    "benchmark_gap",
]
CONFIDENCE_ORDER = {"unusable": 0, "low": 1, "medium": 2, "high": 3}
STRICT_ANCHOR_TYPES = {"section", "snippet", "table", "figure"}


def _tension_id(tension_type: str, nodes: list[str]) -> str:
    basis = tension_type + "|" + "|".join(sorted(nodes))
    return "tension-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:14]


def _confidence(nodes: list[dict[str, Any]]) -> str:
    levels = [str(node.get("confidence", "low")) for node in nodes]
    safe = [level if level in CONFIDENCE_ORDER else "low" for level in levels]
    return min(safe, key=lambda item: CONFIDENCE_ORDER[item]) if safe else "low"


def _edge_confidence(edge: dict[str, Any], nodes: list[dict[str, Any]]) -> str:
    return _confidence([*nodes, {"confidence": edge.get("confidence", "low")}])


def _tension_item(
    *,
    tension_type: str,
    summary: str,
    supporting_nodes: list[str],
    supporting_edges: list[str] | None = None,
    confidence: str,
    source: str,
    do_not_use_as_seed_evidence: bool = False,
    original_tension_type: str = "",
) -> dict[str, Any]:
    item = {
        "tension_id": _tension_id(tension_type, supporting_nodes + (supporting_edges or [])),
        "tension_type": tension_type,
        "summary": summary[:320],
        "supporting_nodes": supporting_nodes,
        "supporting_edges": supporting_edges or [],
        "confidence": confidence if confidence in CONFIDENCE_ORDER else "low",
        "source": source,
        "do_not_use_as_seed_evidence": do_not_use_as_seed_evidence,
    }
    if original_tension_type:
        item["original_tension_type"] = original_tension_type
    if do_not_use_as_seed_evidence:
        item["allowed_lane"] = "breakthrough_speculative"
    return item


def _canonical_or_speculative(
    item: dict[str, Any],
    speculative: list[dict[str, Any]],
    tensions: list[dict[str, Any]],
) -> None:
    if item.get("confidence") in {"low", "unusable"} or not item.get("supporting_nodes"):
        speculative.append(
            _tension_item(
                tension_type="speculative_tension",
                summary=str(item.get("summary", "")),
                supporting_nodes=[str(node) for node in item.get("supporting_nodes", [])],
                supporting_edges=[str(edge) for edge in item.get("supporting_edges", [])],
                confidence=str(item.get("confidence", "low")),
                source=str(item.get("source", "claim_graph")),
                do_not_use_as_seed_evidence=True,
                original_tension_type=str(item.get("tension_type", "")),
            )
        )
    else:
        tensions.append(item)


def _edge_tension_type(edge: dict[str, Any], source: dict[str, Any], target: dict[str, Any]) -> str:
    relation = str(edge.get("relation", ""))
    source_type = str(source.get("claim_type", ""))
    target_type = str(target.get("claim_type", ""))
    node_types = {source_type, target_type}
    if relation == "contradicts":
        if node_types & {"strongest_baseline", "actual_baseline_result"}:
            return "baseline_contradiction"
        return "assumption_conflict"
    if relation == "exposes_gap":
        if source_type == "missing_ablation":
            return "negative_result_opportunity"
        return "benchmark_gap"
    if relation == "limits":
        if source_type == "evaluation_blind_spot":
            return "benchmark_gap"
        if source_type == "unmodeled_latent_variable":
            return "missing_latent_variable"
        if source_type == "transfer_failure":
            return "data_distribution_pathology"
        return "evaluation_blind_spot"
    if relation == "transfers_to":
        return "external_analogy_opportunity"
    return ""


def build_tensions(nodes: list[dict[str, Any]], edges: list[dict[str, Any]] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        by_type[str(node.get("claim_type", ""))].append(node)
    node_by_id = {str(node.get("node_id")): node for node in nodes if node.get("node_id")}
    tensions: list[dict[str, Any]] = []
    speculative: list[dict[str, Any]] = []
    for edge in edges or []:
        source = node_by_id.get(str(edge.get("source_node_id")))
        target = node_by_id.get(str(edge.get("target_node_id")))
        if not source or not target:
            continue
        tension_type = _edge_tension_type(edge, source, target)
        if not tension_type:
            continue
        supporting = [str(source["node_id"]), str(target["node_id"])]
        item = _tension_item(
            tension_type=tension_type,
            summary=f"{source.get('statement', '')} / {target.get('statement', '')}",
            supporting_nodes=supporting,
            supporting_edges=[str(edge["edge_id"])],
            confidence=_edge_confidence(edge, [source, target]),
            source="claim_graph_edge",
        )
        _canonical_or_speculative(item, speculative, tensions)
    node_only_pairs = [
        ("interface_boundary", by_type.get("interface_boundary", []), "interface_boundary_mismatch"),
        ("unmodeled_latent_variable", by_type.get("unmodeled_latent_variable", []), "missing_latent_variable"),
    ]
    for _claim_type, claim_nodes, tension_type in node_only_pairs:
        for node in claim_nodes:
            supporting = [str(node["node_id"])]
            confidence = _confidence([node])
            item = _tension_item(
                tension_type=tension_type,
                summary=str(node.get("statement", "")),
                supporting_nodes=supporting,
                confidence=confidence,
                source="claim_graph_node",
            )
            _canonical_or_speculative(item, speculative, tensions)
    seen = set()
    deduped: list[dict[str, Any]] = []
    for item in tensions:
        if item["tension_id"] not in seen:
            seen.add(item["tension_id"])
            deduped.append(item)
    return deduped, speculative


def validate_tensions(
    tensions: list[dict[str, Any]],
    node_ids: set[str],
    node_by_id: dict[str, dict[str, Any]],
    edge_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    for item in tensions:
        nodes = item.get("supporting_nodes", [])
        edges = item.get("supporting_edges", [])
        if not nodes:
            if item.get("tension_type") != "speculative_tension" or item.get("do_not_use_as_seed_evidence") is not True:
                errors.append(f"{item.get('tension_id')}:missing_supporting_nodes")
            if item.get("confidence") == "high":
                errors.append(f"{item.get('tension_id')}:high_confidence_llm_only_tension")
            continue
        missing = [node for node in nodes if node not in node_ids]
        if missing:
            errors.append(f"{item.get('tension_id')}:missing_claim_nodes:{','.join(missing)}")
        if edge_ids is not None:
            missing_edges = [edge for edge in edges if edge not in edge_ids]
            if missing_edges:
                errors.append(f"{item.get('tension_id')}:missing_claim_edges:{','.join(missing_edges)}")
        if item.get("confidence") == "high":
            if not any(
                node_by_id[node].get("confidence") == "high"
                and node_by_id[node].get("anchor", {}).get("anchor_type") in {"section", "snippet", "table", "figure"}
                for node in nodes
                if node in node_by_id
            ):
                errors.append(f"{item.get('tension_id')}:high_confidence_without_high_anchored_node")
        if item.get("tension_type") == "speculative_tension" and item.get("do_not_use_as_seed_evidence") is not True:
            errors.append(f"{item.get('tension_id')}:speculative_tension_must_not_support_seed_evidence")
    return errors


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Tension Map - {payload['run_date']}",
        "",
        f"- schema_version: {payload['schema_version']}",
        f"- tensions: {len(payload['tensions'])}",
        f"- speculative_tensions: {len(payload['speculative_tensions'])}",
        "",
        "## Tensions",
        "",
    ]
    for item in payload["tensions"]:
        edges = f" edges={', '.join(item.get('supporting_edges', []))}" if item.get("supporting_edges") else ""
        lines.append(f"- `{item['tension_type']}` {item['summary']} nodes={', '.join(item['supporting_nodes'])}{edges}")
    lines.extend(["", "## Speculative Lane", ""])
    for item in payload["speculative_tensions"]:
        edges = f" edges={', '.join(item.get('supporting_edges', []))}" if item.get("supporting_edges") else ""
        lines.append(f"- `{item.get('original_tension_type')}` {item['summary']} nodes={', '.join(item['supporting_nodes'])}{edges}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    graph_records = load_jsonl(artifact_dir(args.run_date) / "claim-graph-snapshot.jsonl")
    nodes = [
        record
        for record in graph_records
        if record.get("record_type", "node") == "node" and record.get("node_id")
    ]
    edges = [
        record
        for record in graph_records
        if record.get("record_type") == "edge" and record.get("edge_id")
    ]
    node_by_id = {str(node.get("node_id")): node for node in nodes}
    edge_ids = {str(edge.get("edge_id")) for edge in edges}
    tensions, speculative = build_tensions(nodes, edges)
    errors = validate_tensions(tensions + speculative, set(node_by_id), node_by_id, edge_ids)
    payload = {
        "schema_version": "tension_map.v1",
        "run_date": args.run_date,
        "tension_types": TENSION_TYPES,
        "tensions": tensions,
        "speculative_tensions": speculative,
        "validation_errors": errors,
        "artifact_hashes": artifact_hashes(args.run_date, ["claim-graph-snapshot.jsonl"]),
        "boundary": "Speculative tensions may feed breakthrough raw candidates but cannot support formal seed promotion.",
    }
    write_run_artifact(args.run_date, "tension-map.json", payload, state="tension_mapped", dry_run=args.dry_run)
    write_text(artifact_dir(args.run_date) / "tension-map.md", render_markdown(payload), dry_run=args.dry_run)
    safe_print(f"TENSION_MAP: tensions={len(tensions)} speculative={len(speculative)} errors={len(errors)}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
