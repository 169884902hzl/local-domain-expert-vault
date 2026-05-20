"""Make the single v2 promotion/survival decision after all review gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import (
    artifact_dir,
    artifact_hashes,
    candidate_id,
    ensure_v2_dirs,
    read_json,
    run_dir,
    validate_json_file,
    write_run_artifact,
)


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


def decide(
    *,
    run_date: str,
    allow_human_override: bool,
) -> dict[str, Any]:
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
    decisions: list[dict[str, Any]] = []
    for item in _final_candidates(selected_payload.get("selected", []), mutation_payload.get("mutations", [])):
        cid = candidate_id(item)
        parent_id = str(item.get("parent_candidate_id") or cid)
        deepseek = deepseek_by_id.get(parent_id, {})
        novelty = novelty_by_id.get(cid, {})
        codex = codex_by_id.get(cid, {})
        override = overrides.get(cid)
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
        if _has_anchorless_core_evidence(item):
            blocks.append("fabricated_or_anchorless_core_evidence")
        if override and any(block in blocks for block in ["deepseek_fatal_flaw", "fabricated_or_anchorless_core_evidence"]):
            blocks.append("human_override_cannot_bypass_hard_block")

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
                "codex_action": codex.get("action", ""),
                "human_override_used": bool(override),
                "publish_target": "seed" if action == "accept_for_user_review" else action,
            }
        )
    status = "success" if not override_errors else "partial_schema_blocked"
    return {
        "schema_version": "survival_decision.v1",
        "run_date": run_date,
        "status": status,
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
            ],
        ),
        "boundary": "This is the only promotion brain; publish_research_run.py must follow these decisions and re-check hashes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--allow-human-override", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    payload = decide(run_date=args.run_date, allow_human_override=args.allow_human_override)
    write_run_artifact(args.run_date, "survival-decision.json", payload, state="survival_decided", dry_run=args.dry_run)
    counts: dict[str, int] = {}
    for item in payload["decisions"]:
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    safe_print(f"SURVIVAL_DECISION: status={payload['status']} counts={json.dumps(counts, sort_keys=True)}")
    return 0 if payload["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
