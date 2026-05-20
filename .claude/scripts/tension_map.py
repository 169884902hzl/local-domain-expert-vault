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


def _tension_id(tension_type: str, nodes: list[str]) -> str:
    basis = tension_type + "|" + "|".join(sorted(nodes))
    return "tension-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:14]


def _confidence(nodes: list[dict[str, Any]]) -> str:
    levels = {str(node.get("confidence", "low")) for node in nodes}
    if "high" in levels:
        return "high"
    if "medium" in levels:
        return "medium"
    return "low"


def build_tensions(nodes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        by_type[str(node.get("claim_type", ""))].append(node)
    tensions: list[dict[str, Any]] = []
    speculative: list[dict[str, Any]] = []
    pairs = [
        ("evaluation_blind_spot", by_type.get("evaluation_blind_spot", []), "benchmark_gap"),
        ("missing_ablation", by_type.get("missing_ablation", []), "negative_result_opportunity"),
        ("interface_boundary", by_type.get("interface_boundary", []), "interface_boundary_mismatch"),
        ("strongest_baseline", by_type.get("strongest_baseline", []), "baseline_contradiction"),
    ]
    for claim_type, claim_nodes, tension_type in pairs:
        for node in claim_nodes:
            supporting = [str(node["node_id"])]
            confidence = _confidence([node])
            item = {
                "tension_id": _tension_id(tension_type, supporting),
                "tension_type": tension_type,
                "summary": str(node.get("statement", ""))[:320],
                "supporting_nodes": supporting,
                "confidence": confidence,
                "source": "claim_graph",
            }
            if confidence == "low":
                speculative.append({**item, "tension_type": "speculative_tension", "original_tension_type": tension_type})
            else:
                tensions.append(item)
    seen = set()
    deduped: list[dict[str, Any]] = []
    for item in tensions:
        if item["tension_id"] not in seen:
            seen.add(item["tension_id"])
            deduped.append(item)
    return deduped, speculative


def validate_tensions(tensions: list[dict[str, Any]], node_ids: set[str], node_by_id: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for item in tensions:
        nodes = item.get("supporting_nodes", [])
        if not nodes:
            errors.append(f"{item.get('tension_id')}:missing_supporting_nodes")
            continue
        missing = [node for node in nodes if node not in node_ids]
        if missing:
            errors.append(f"{item.get('tension_id')}:missing_claim_nodes:{','.join(missing)}")
        if item.get("confidence") == "high":
            if not any(
                node_by_id[node].get("confidence") == "high"
                and node_by_id[node].get("anchor", {}).get("anchor_type") in {"section", "snippet", "table", "figure"}
                for node in nodes
                if node in node_by_id
            ):
                errors.append(f"{item.get('tension_id')}:high_confidence_without_high_anchored_node")
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
        lines.append(f"- `{item['tension_type']}` {item['summary']} nodes={', '.join(item['supporting_nodes'])}")
    lines.extend(["", "## Speculative Lane", ""])
    for item in payload["speculative_tensions"]:
        lines.append(f"- `{item.get('original_tension_type')}` {item['summary']} nodes={', '.join(item['supporting_nodes'])}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    nodes = load_jsonl(artifact_dir(args.run_date) / "claim-graph-snapshot.jsonl")
    node_by_id = {str(node.get("node_id")): node for node in nodes}
    tensions, speculative = build_tensions(nodes)
    errors = validate_tensions(tensions, set(node_by_id), node_by_id)
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
