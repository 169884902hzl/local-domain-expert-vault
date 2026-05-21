"""Make the single v2 promotion/survival decision after all review gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print
from baseline_table import baseline_allows_active_seed, baseline_execution_status, load_baseline_tables
from manual_prior_art_review import active_seed_review_allowed, completed_review_by_candidate, review_quality_errors
from research_agenda_common import slugify
from research_seed_v2_common import (
    agenda_v2_path,
    artifact_dir,
    artifact_hashes,
    candidate_id,
    ensure_v2_dirs,
    load_jsonl,
    read_json,
    run_dir,
    validate_artifact,
    validate_json_file,
    write_run_artifact,
)


BROAD_EXTERNAL_NOVELTY_PROVIDERS = {"openalex", "semantic_scholar"}
WEAK_CORE_CONFIDENCE = {"low", "unusable"}
UNANCHORED_TYPES = {"note_only", "abstract", ""}
PDF_VERIFIED_ANCHOR_TYPES = {"section", "snippet", "table", "figure", "result_row"}
ACTIVE_SEED_BLOCKING_RISKS = {
    "manual_prior_art_quality_incomplete",
    "manual_prior_art_query_log_missing",
    "result_row_unconfirmed",
    "cross_paper_edge_requires_human_check",
    "baseline_execution_not_ready",
    "stale_external_novelty_cache",
    "strongest_baseline_unknown",
    "active_seed_without_pilot_plan",
    "anchorless_core_evidence_risk",
    "speculative_tension_not_formal_seed_evidence",
}


def _has_broad_external_provider(providers: list[str]) -> bool:
    return bool(BROAD_EXTERNAL_NOVELTY_PROVIDERS & set(providers))


def _final_candidates(selected: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations}
    finals = [dict(item) for item in selected if candidate_id(item) not in mutated_parent_ids]
    finals.extend(dict(item) for item in mutations)
    return finals


def _load_overrides(run_date: str, *, allow: bool) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not allow:
        return {}, []
    root = run_dir(run_date).parents[1] / "overrides" / "human-overrides" / run_date
    consumed: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    if not root.exists():
        return consumed, errors
    for path in sorted(root.glob("*.json")):
        schema_errors = validate_json_file(path, "human_override.v1")
        if schema_errors:
            errors.extend(f"{path.name}:{issue}" for issue in schema_errors)
            continue
        payload = read_json(path)
        if payload.get("reviewer") != "human":
            errors.append(f"{path.name}:reviewer_not_human")
            continue
        consumed[str(payload["candidate_id"])] = payload
    return consumed, errors


def _has_anchorless_core_evidence(item: dict[str, Any]) -> bool:
    if item.get("fabricated_core_evidence"):
        return True
    if item.get("anchorless_core_evidence"):
        return True
    return not bool(item.get("evidence_links") or item.get("supporting_nodes"))


def _load_claim_nodes(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "claim-graph-snapshot.jsonl"
    if not path.exists():
        return {}
    nodes: dict[str, dict[str, Any]] = {}
    for record in load_jsonl(path):
        if record.get("record_type", "node") != "node":
            continue
        node_id = str(record.get("node_id", ""))
        if node_id:
            nodes[node_id] = record
    return nodes


def _load_claim_edges(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "claim-graph-snapshot.jsonl"
    if not path.exists():
        return {}
    edges: dict[str, dict[str, Any]] = {}
    for record in load_jsonl(path):
        if record.get("record_type") != "edge":
            continue
        edge_id = str(record.get("edge_id", ""))
        if edge_id:
            edges[edge_id] = record
    return edges


def _load_speculative_tensions(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "tension-map.json"
    if not path.exists():
        return {}
    payload = read_json(path)
    tensions: dict[str, dict[str, Any]] = {}
    for item in [*payload.get("tensions", []), *payload.get("speculative_tensions", [])]:
        if not isinstance(item, dict):
            continue
        tension_id = str(item.get("tension_id", ""))
        if tension_id:
            tensions[tension_id] = item
    return tensions


def _candidate_node_ids(item: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ["core_claim_graph_nodes", "supporting_nodes"]:
        raw = item.get(key, [])
        if isinstance(raw, list):
            values.extend(str(value) for value in raw if value)
    return list(dict.fromkeys(values))


def _candidate_tension_ids(item: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ["supporting_tensions", "tension_ids"]:
        raw = item.get(key, [])
        if isinstance(raw, list):
            values.extend(str(value) for value in raw if value)
    return list(dict.fromkeys(values))


def _candidate_edge_ids(item: dict[str, Any], tensions: dict[str, dict[str, Any]]) -> list[str]:
    values: list[str] = []
    for key in ["core_claim_graph_edges", "supporting_edges"]:
        raw = item.get(key, [])
        if isinstance(raw, list):
            values.extend(str(value) for value in raw if value)
    for tension_id in _candidate_tension_ids(item):
        tension = tensions.get(tension_id)
        if isinstance(tension, dict) and isinstance(tension.get("supporting_edges"), list):
            values.extend(str(value) for value in tension["supporting_edges"] if value)
    return list(dict.fromkeys(values))


def _node_is_weak_or_unanchored(node: dict[str, Any]) -> bool:
    anchor = node.get("anchor", {}) if isinstance(node.get("anchor"), dict) else {}
    anchor_type = str(node.get("anchor_type") or anchor.get("anchor_type") or "")
    return (
        str(node.get("confidence", "low")) in WEAK_CORE_CONFIDENCE
        or anchor_type in UNANCHORED_TYPES
        or node.get("requires_human_check") is True
    )


def _node_has_unconfirmed_result_row(node: dict[str, Any]) -> bool:
    anchor = node.get("anchor", {}) if isinstance(node.get("anchor"), dict) else {}
    anchor_type = str(node.get("anchor_type") or anchor.get("anchor_type") or "")
    if anchor_type != "result_row":
        return False
    return not (
        anchor.get("manual_confirmed") is True
        and str(anchor.get("confirmed_by", "")).strip()
        and str(anchor.get("confirmed_at", "")).strip()
        and str(anchor.get("confirmation_note", "")).strip()
    )


def _edge_requires_active_seed_confirmation(edge: dict[str, Any]) -> bool:
    if edge.get("edge_scope") != "cross_paper":
        return False
    if edge.get("human_confirmed") is True:
        return False
    return str(edge.get("edge_quality_status") or "") not in {"audited", "confirmed"}


def _pilot_plan(run_date: str, item: dict[str, Any]) -> dict[str, Any] | None:
    slug = slugify(str(item.get("title") or candidate_id(item)))
    path = agenda_v2_path("pilots", slug, "pilot-plan.json")
    if not path.exists():
        return None
    try:
        return read_json(path)
    except Exception:
        return None


def _pilot_plan_allows_active_seed(plan: dict[str, Any] | None) -> bool:
    if not plan:
        return False
    required = ["metric", "baseline_implementation_path", "resource_budget"]
    return all(str(plan.get(field, "")).strip() for field in required)


def _pilot_plan_allows_pilot_ready(plan: dict[str, Any] | None) -> bool:
    if not _pilot_plan_allows_active_seed(plan):
        return False
    return bool(plan.get("executable") is True and str(plan.get("metric_automation", "")).strip())


def _core_evidence_risks(
    item: dict[str, Any],
    claim_nodes: dict[str, dict[str, Any]],
    claim_edges: dict[str, dict[str, Any]],
    tensions: dict[str, dict[str, Any]],
) -> list[str]:
    risks: list[str] = []
    if item.get("fabricated_core_evidence"):
        risks.append("fabricated_core_evidence")
    node_ids = _candidate_node_ids(item)
    resolved_nodes = [claim_nodes[node_id] for node_id in node_ids if node_id in claim_nodes]
    if item.get("anchorless_core_evidence") or not node_ids or not resolved_nodes:
        risks.append("anchorless_core_evidence_risk")
    elif all(_node_is_weak_or_unanchored(node) for node in resolved_nodes):
        risks.append("anchorless_core_evidence_risk")
    if any(_node_has_unconfirmed_result_row(node) for node in resolved_nodes):
        risks.append("result_row_unconfirmed")
    edge_ids = _candidate_edge_ids(item, tensions)
    resolved_edges = [claim_edges[edge_id] for edge_id in edge_ids if edge_id in claim_edges]
    if any(_edge_requires_active_seed_confirmation(edge) for edge in resolved_edges):
        risks.append("cross_paper_edge_requires_human_check")
    for tension_id in _candidate_tension_ids(item):
        tension = tensions.get(tension_id)
        if tension and (
            tension.get("do_not_use_as_seed_evidence") is True
            or tension.get("tension_type") == "speculative_tension"
        ):
            risks.append("speculative_tension_not_formal_seed_evidence")
        if tension and "cross_paper_edge_requires_human_check" in tension.get("risk_markers", []):
            risks.append("cross_paper_edge_requires_human_check")
    if item.get("lane") == "breakthrough_speculative" and "anchorless_core_evidence_risk" in risks:
        risks.append("breakthrough_speculative_evidence_boundary")
    return list(dict.fromkeys(risks))


def decide(
    *,
    run_date: str,
    allow_human_override: bool,
    target_policy: str = "seed-candidates-only",
) -> dict[str, Any]:
    input_errors: list[str] = []
    for artifact_name in ["selected-candidates.json", "deepseek-review.json", "novelty-scan.json", "codex-execution-review.json"]:
        input_errors.extend(f"{artifact_name}:{error}" for error in validate_artifact(run_date, artifact_name))
    for artifact_name in ["manual-prior-art-review.json", "pdf-evidence-anchors.json", "baseline-table.json"]:
        if (artifact_dir(run_date) / artifact_name).exists():
            input_errors.extend(f"{artifact_name}:{error}" for error in validate_artifact(run_date, artifact_name))
    if input_errors:
        return {
            "schema_version": "survival_decision.v1",
            "run_date": run_date,
            "status": "partial_schema_blocked",
            "target_policy": target_policy,
            "decisions": [],
            "human_overrides_consumed": [],
            "human_override_errors": input_errors,
            "artifact_hashes": artifact_hashes(
                run_date,
                ["selected-candidates.json", "deepseek-review.json", "gemini-mutations.json", "novelty-scan.json", "codex-execution-review.json"],
            ),
            "boundary": "Invalid upstream artifacts are not consumed by survival decision.",
        }
    selected_payload = read_json(artifact_dir(run_date) / "selected-candidates.json")
    deepseek_payload = read_json(artifact_dir(run_date) / "deepseek-review.json")
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutation_payload = read_json(mutations_path) if mutations_path.exists() else {"mutations": []}
    novelty_payload = read_json(artifact_dir(run_date) / "novelty-scan.json")
    codex_payload = read_json(artifact_dir(run_date) / "codex-execution-review.json")
    overrides, override_errors = _load_overrides(run_date, allow=allow_human_override)

    deepseek_by_id = {str(item.get("candidate_id")): item for item in deepseek_payload.get("reviews", [])}
    novelty_by_id = {str(item.get("candidate_id")): item for item in novelty_payload.get("scans", [])}
    codex_by_id = {str(item.get("candidate_id")): item for item in codex_payload.get("reviews", [])}
    deepseek_provider = deepseek_payload.get("provider_status", {})
    codex_provider = codex_payload.get("provider_status", {})
    claim_nodes = _load_claim_nodes(run_date)
    claim_edges = _load_claim_edges(run_date)
    tensions = _load_speculative_tensions(run_date)
    manual_reviews = completed_review_by_candidate(run_date)
    baseline_tables = load_baseline_tables(run_date)
    decisions: list[dict[str, Any]] = []
    for item in _final_candidates(selected_payload.get("selected", []), mutation_payload.get("mutations", [])):
        cid = candidate_id(item)
        parent_id = str(item.get("parent_candidate_id") or cid)
        deepseek = deepseek_by_id.get(parent_id, {})
        novelty = novelty_by_id.get(cid, {})
        codex = codex_by_id.get(cid, {})
        override = overrides.get(cid)
        manual_review = manual_reviews.get(cid)
        baseline_table = baseline_tables.get(cid)
        pilot_plan = _pilot_plan(run_date, item)
        blocks: list[str] = []
        if deepseek_payload.get("status") != "success" or not deepseek_provider.get("provider_backed"):
            blocks.append("deepseek_not_provider_backed_success")
        if not deepseek or deepseek.get("status") != "success":
            blocks.append("deepseek_status_not_success")
        if deepseek.get("fatal_flaw"):
            blocks.append("deepseek_fatal_flaw")
        if deepseek.get("survivability_label") not in {"survives", "survives_if_mutated"}:
            blocks.append("deepseek_label_not_survivable")
        if item.get("parent_candidate_id") and deepseek.get("survivability_label") != "survives_if_mutated":
            blocks.append("mutation_without_deepseek_mutation_label")
        novelty_class = str(novelty.get("novelty_classification", "unknown"))
        if novelty_payload.get("status") not in {"completed", "completed_local_only"}:
            blocks.append("novelty_scan_not_completed")
        if novelty.get("promotion_allowed") is not True:
            blocks.append("novelty_promotion_not_allowed")
        verification_scope = str(novelty.get("verification_scope") or "local_only")
        external_providers_used = [str(value) for value in novelty.get("external_providers_used", []) if value]
        stale_external_cache = bool(novelty.get("stale_external_novelty_cache")) or any(
            isinstance(summary, dict) and summary.get("cache_status") == "stale"
            for provider, summary in novelty.get("provider_results", {}).items()
            if provider in BROAD_EXTERNAL_NOVELTY_PROVIDERS
        )
        if target_policy == "formal":
            if novelty.get("formal_promotion_allowed") is not True:
                blocks.append("formal_novelty_promotion_not_allowed")
            if verification_scope == "local_only":
                blocks.append("formal_novelty_requires_external_or_hybrid_scope")
            if verification_scope == "local_plus_arxiv_api":
                blocks.append("formal_novelty_arxiv_only_scope_not_broad_prior_art")
            if not external_providers_used:
                blocks.append("formal_novelty_requires_external_provider")
            if not _has_broad_external_provider(external_providers_used):
                blocks.append("formal_novelty_requires_openalex_or_semantic_scholar")
            if stale_external_cache:
                blocks.append("stale_external_novelty_cache")
        if novelty_class == "unknown" and not override:
            blocks.append("unknown_novelty_without_human_override")
        if novelty_class not in {"likely_open", "partial_overlap", "unknown"}:
            blocks.append(f"novelty_not_promotable:{novelty_class}")
        if novelty.get("duplicate_guard", {}).get("action") == "block":
            blocks.append("duplicate_guard_block")
        if codex_payload.get("status") != "success" or not codex_provider.get("provider_backed"):
            blocks.append("codex_not_provider_backed_success")
        if codex.get("status") != "success":
            blocks.append("codex_status_not_success")
        if codex.get("action") != "accept_for_user_review":
            blocks.append(f"codex_action_not_accept:{codex.get('action', 'missing')}")
        risks = _core_evidence_risks(item, claim_nodes, claim_edges, tensions)
        if not manual_review:
            risks.append("manual_prior_art_review_missing")
        elif manual_review.get("decision") in {"park", "reject", "needs_more_search"}:
            risks.append(f"manual_prior_art_review_{manual_review.get('decision')}")
        elif manual_review.get("decision") == "allow_active_seed":
            for error in review_quality_errors(manual_review):
                if error.endswith("manual_prior_art_query_log_missing"):
                    risks.append("manual_prior_art_query_log_missing")
                elif error.endswith("manual_prior_art_quality_incomplete"):
                    risks.append("manual_prior_art_quality_incomplete")
                else:
                    risks.append("manual_prior_art_quality_incomplete")
        if not baseline_table:
            risks.append("baseline_table_missing")
        elif not baseline_allows_active_seed(baseline_table):
            if baseline_execution_status(baseline_table) in {"unknown", "prohibitive", "partial"}:
                risks.append("baseline_execution_not_ready")
            risks.append("strongest_baseline_unknown")
        if stale_external_cache:
            risks.append("stale_external_novelty_cache")
        if not _pilot_plan_allows_active_seed(pilot_plan):
            risks.append("active_seed_without_pilot_plan")
        if "fabricated_core_evidence" in risks:
            blocks.append("fabricated_or_anchorless_core_evidence")
        if target_policy == "formal":
            if "anchorless_core_evidence_risk" in risks:
                blocks.append("formal_core_evidence_not_anchored")
            if "speculative_tension_not_formal_seed_evidence" in risks:
                blocks.append("speculative_tension_not_formal_seed_evidence")
        if override and any(
            block in blocks
            for block in [
                "deepseek_fatal_flaw",
                "fabricated_or_anchorless_core_evidence",
                "formal_core_evidence_not_anchored",
                "speculative_tension_not_formal_seed_evidence",
            ]
        ):
            blocks.append("human_override_cannot_bypass_hard_block")

        base_blocks = list(blocks)
        formal_rehearsal_allowed = bool(not base_blocks and manual_review and manual_review.get("decision") == "allow_active_seed" and baseline_table)
        legacy_active_gate_would_pass = bool(
            not base_blocks
            and active_seed_review_allowed(manual_review)
            and baseline_allows_active_seed(baseline_table)
            and not stale_external_cache
            and _pilot_plan_allows_active_seed(pilot_plan)
            and not (set(risks) & ACTIVE_SEED_BLOCKING_RISKS)
        )
        governance_review_possible = bool(legacy_active_gate_would_pass)
        active_commit_forbidden_reasons = sorted(
            set(
                [
                    "active_seed_commit_requires_active_seed_commit_py",
                    "survival_decision_is_model_risk_classifier_only",
                    *base_blocks,
                    *[risk for risk in risks if risk in ACTIVE_SEED_BLOCKING_RISKS],
                ]
            )
        )
        active_seed_allowed = False
        pilot_ready_allowed = False

        action = "accept_for_user_review" if not blocks else "killed"
        if blocks and any(block.startswith("codex_action_not_accept:park") or block == "duplicate_guard_block" for block in blocks):
            action = "parked"
        elif blocks and deepseek.get("rescue_mutation"):
            action = "rescue"
        decisions.append(
            {
                "candidate_id": cid,
                "parent_candidate_id": item.get("parent_candidate_id", ""),
                "candidate_title": item.get("title", ""),
                "decision": action,
                "blocks": blocks,
                "deepseek_label": deepseek.get("survivability_label", ""),
                "novelty_classification": novelty_class,
                "verification_scope": verification_scope,
                "external_providers_used": external_providers_used,
                "codex_action": codex.get("action", ""),
                "human_override_used": bool(override),
                "risks": risks,
                "formal_rehearsal_allowed": formal_rehearsal_allowed,
                "governance_review_possible": governance_review_possible,
                "active_commit_forbidden_reasons": active_commit_forbidden_reasons,
                "requires_human_governance": True,
                "active_seed_allowed": active_seed_allowed,
                "pilot_ready_allowed": pilot_ready_allowed,
                "publish_target": (
                    "formal-rehearsal" if formal_rehearsal_allowed else "seed-candidates"
                )
                if action == "accept_for_user_review"
                else action,
            }
        )
    status = "success" if not override_errors else "partial_schema_blocked"
    return {
        "schema_version": "survival_decision.v1",
        "run_date": run_date,
        "status": status,
        "target_policy": target_policy,
        "decisions": decisions,
        "human_overrides_consumed": sorted(overrides),
        "human_override_errors": override_errors,
        "artifact_hashes": artifact_hashes(
            run_date,
            [
                "selected-candidates.json",
                "deepseek-review.json",
                "gemini-mutations.json",
                "novelty-scan.json",
                "codex-execution-review.json",
                "manual-prior-art-review.json",
                "baseline-table.json",
            ],
        ),
        "boundary": "This is the only promotion brain; publish_research_run.py must follow these decisions and re-check hashes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--allow-human-override", action="store_true")
    parser.add_argument("--target-policy", choices=["disabled", "seed-candidates-only", "formal"], default="seed-candidates-only")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    payload = decide(run_date=args.run_date, allow_human_override=args.allow_human_override, target_policy=args.target_policy)
    write_run_artifact(args.run_date, "survival-decision.json", payload, state="survival_decided", dry_run=args.dry_run)
    counts: dict[str, int] = {}
    for item in payload["decisions"]:
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    safe_print(f"SURVIVAL_DECISION: status={payload['status']} counts={json.dumps(counts, sort_keys=True)}")
    return 0 if payload["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
