"""Validate v2 research-seed run artifacts before downstream consumption."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import (
    ARTIFACT_SCHEMAS,
    PUBLISH_REQUIRED_ARTIFACTS,
    RUN_SCHEMA_VERSION,
    artifact_dir,
    candidate_id,
    file_sha256,
    init_manifest_with_policy,
    load_jsonl,
    read_json,
    run_dir,
    schema_validator_available,
    validate_artifact,
    validate_json_file,
    v2_rel,
)


BROAD_EXTERNAL_NOVELTY_PROVIDERS = {"openalex", "semantic_scholar"}
WEAK_CORE_CONFIDENCE = {"low", "unusable"}
UNANCHORED_TYPES = {"note_only", "abstract", ""}


def _has_broad_external_provider(providers: list[str]) -> bool:
    return bool(BROAD_EXTERNAL_NOVELTY_PROVIDERS & set(providers))


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


def _candidate_node_ids(item: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ["core_claim_graph_nodes", "supporting_nodes"]:
        raw = item.get(key, [])
        if isinstance(raw, list):
            values.extend(str(value) for value in raw if value)
    return list(dict.fromkeys(values))


def _node_is_weak_or_unanchored(node: dict[str, Any]) -> bool:
    anchor = node.get("anchor", {}) if isinstance(node.get("anchor"), dict) else {}
    anchor_type = str(node.get("anchor_type") or anchor.get("anchor_type") or "")
    return (
        str(node.get("confidence", "low")) in WEAK_CORE_CONFIDENCE
        or anchor_type in UNANCHORED_TYPES
        or node.get("requires_human_check") is True
    )


def _validate_manifest(run_date: str) -> list[str]:
    path = run_dir(run_date) / "manifest.json"
    if not path.exists():
        return [f"missing_manifest:{v2_rel(path)}"]
    return validate_json_file(path, RUN_SCHEMA_VERSION)


def _validate_referenced_hashes(run_date: str, artifact_name: str) -> list[str]:
    path = artifact_dir(run_date) / artifact_name
    if not path.exists() or artifact_name.endswith(".jsonl"):
        return []
    payload = read_json(path)
    errors: list[str] = []
    for name, expected in payload.get("artifact_hashes", {}).items():
        dep = artifact_dir(run_date) / name
        if not dep.exists():
            errors.append(f"{artifact_name}:hash_ref_missing:{name}")
            continue
        actual = file_sha256(dep)
        if actual != expected:
            errors.append(f"{artifact_name}:hash_mismatch:{name}:expected={expected}:actual={actual}")
    return errors


def _final_candidate_ids(run_date: str) -> set[str]:
    selected = read_json(artifact_dir(run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations if isinstance(item, dict)}
    ids = {candidate_id(item) for item in selected if isinstance(item, dict) and candidate_id(item) not in mutated_parent_ids}
    ids.update(candidate_id(item) for item in mutations if isinstance(item, dict))
    return ids


def _final_candidates(run_date: str) -> list[dict[str, Any]]:
    selected = read_json(artifact_dir(run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations if isinstance(item, dict)}
    finals = [dict(item) for item in selected if isinstance(item, dict) and candidate_id(item) not in mutated_parent_ids]
    finals.extend(dict(item) for item in mutations if isinstance(item, dict))
    return finals


def _validate_formal_core_evidence(run_date: str) -> list[str]:
    artifacts = artifact_dir(run_date)
    if not (artifacts / "selected-candidates.json").exists() or not (artifacts / "survival-decision.json").exists():
        return []
    accepted = {
        str(item.get("candidate_id"))
        for item in read_json(artifacts / "survival-decision.json").get("decisions", [])
        if isinstance(item, dict) and item.get("decision") == "accept_for_user_review"
    }
    if not accepted:
        return []
    claim_nodes = _load_claim_nodes(run_date)
    errors: list[str] = []
    for item in _final_candidates(run_date):
        cid = candidate_id(item)
        if cid not in accepted:
            continue
        node_ids = _candidate_node_ids(item)
        resolved = [claim_nodes[node_id] for node_id in node_ids if node_id in claim_nodes]
        if item.get("anchorless_core_evidence") or not node_ids or not resolved:
            errors.append(f"formal_core_evidence_not_anchored:{cid}")
        elif all(_node_is_weak_or_unanchored(node) for node in resolved):
            errors.append(f"formal_core_evidence_not_anchored:{cid}")
        decision = next(
            (
                row
                for row in read_json(artifacts / "survival-decision.json").get("decisions", [])
                if isinstance(row, dict) and str(row.get("candidate_id")) == cid
            ),
            {},
        )
        risks = decision.get("risks", []) if isinstance(decision, dict) else []
        if "speculative_tension_not_formal_seed_evidence" in risks:
            errors.append(f"speculative_tension_not_formal_seed_evidence:{cid}")
    return errors


def _validate_candidate_alignment(run_date: str) -> list[str]:
    artifacts = artifact_dir(run_date)
    required = ["selected-candidates.json", "novelty-scan.json", "codex-execution-review.json", "survival-decision.json"]
    if any(not (artifacts / name).exists() for name in required):
        return []
    final_ids = _final_candidate_ids(run_date)
    errors: list[str] = []
    novelty_ids = {str(item.get("candidate_id")) for item in read_json(artifacts / "novelty-scan.json").get("scans", []) if isinstance(item, dict)}
    codex_ids = {str(item.get("candidate_id")) for item in read_json(artifacts / "codex-execution-review.json").get("reviews", []) if isinstance(item, dict)}
    survival_ids = {str(item.get("candidate_id")) for item in read_json(artifacts / "survival-decision.json").get("decisions", []) if isinstance(item, dict)}
    for label, ids in [("novelty_scan", novelty_ids), ("codex_execution_review", codex_ids), ("survival_decision", survival_ids)]:
        missing = sorted(final_ids - ids)
        extra = sorted(ids - final_ids)
        if missing:
            errors.append(f"candidate_alignment:{label}:missing={','.join(missing)}")
        if extra:
            errors.append(f"candidate_alignment:{label}:unexpected={','.join(extra)}")
    return errors


def _validate_formal_policy(run_date: str) -> list[str]:
    manifest_path = run_dir(run_date) / "manifest.json"
    if not manifest_path.exists():
        return []
    manifest = read_json(manifest_path)
    if manifest.get("v2_publish_policy") != "formal":
        return []
    errors: list[str] = []
    if not schema_validator_available():
        errors.append("schema_validator_unavailable_blocks_formal_publish")
    artifacts = artifact_dir(run_date)
    novelty_path = artifacts / "novelty-scan.json"
    if novelty_path.exists():
        for item in read_json(novelty_path).get("scans", []):
            if not isinstance(item, dict):
                continue
            cid = str(item.get("candidate_id"))
            if item.get("formal_promotion_allowed") is not True:
                errors.append(f"formal_novelty_not_allowed:{cid}")
            if item.get("verification_scope") == "local_only":
                errors.append(f"formal_novelty_local_only:{cid}")
            if item.get("verification_scope") == "local_plus_arxiv_api":
                errors.append(f"formal_novelty_arxiv_only_scope:{cid}")
            external_providers = [str(value) for value in item.get("external_providers_used", []) if value]
            if not external_providers:
                errors.append(f"formal_novelty_missing_external_provider:{cid}")
            if not _has_broad_external_provider(external_providers):
                errors.append(f"formal_novelty_missing_broad_external_provider:{cid}")
    if not manifest.get("test_provider_used_for_formal"):
        provider_expectations = [
            ("deepseek-review.json", "opencode"),
            ("codex-execution-review.json", "codex-cli"),
        ]
        for artifact_name, expected_mode in provider_expectations:
            path = artifacts / artifact_name
            if not path.exists():
                continue
            provider = read_json(path).get("provider_status", {})
            if provider.get("mode") != expected_mode:
                errors.append(f"formal_provider_mode_not_production:{artifact_name}:expected={expected_mode}:actual={provider.get('mode')}")
    errors.extend(_validate_formal_core_evidence(run_date))
    return errors


def validate_run(run_date: str, *, strict_publish: bool = False) -> dict[str, Any]:
    errors = _validate_manifest(run_date)
    checked: list[str] = ["manifest.json"]
    for artifact_name in ARTIFACT_SCHEMAS:
        path = artifact_dir(run_date) / artifact_name
        if not path.exists():
            if strict_publish and artifact_name in PUBLISH_REQUIRED_ARTIFACTS:
                errors.append(f"missing_publish_required_artifact:{artifact_name}")
            continue
        checked.append(f"artifacts/{artifact_name}")
        errors.extend(f"{artifact_name}:{issue}" for issue in validate_artifact(run_date, artifact_name))
        errors.extend(_validate_referenced_hashes(run_date, artifact_name))
    errors.extend(_validate_candidate_alignment(run_date))
    if strict_publish:
        errors.extend(_validate_formal_policy(run_date))
    return {
        "schema_version": "research_run_validation.v1",
        "run_date": run_date,
        "status": "success" if not errors else "partial_schema_blocked",
        "checked": checked,
        "errors": errors,
    }


def validate_one(run_date: str, artifact_name: str) -> dict[str, Any]:
    if artifact_name not in ARTIFACT_SCHEMAS:
        return {
            "schema_version": "research_run_validation.v1",
            "run_date": run_date,
            "status": "partial_schema_blocked",
            "checked": [],
            "errors": [f"unknown_artifact:{artifact_name}"],
        }
    errors = validate_artifact(run_date, artifact_name)
    errors.extend(_validate_referenced_hashes(run_date, artifact_name))
    return {
        "schema_version": "research_run_validation.v1",
        "run_date": run_date,
        "status": "success" if not errors else "partial_schema_blocked",
        "checked": [f"artifacts/{artifact_name}"],
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    init_parser = sub.add_parser("init")
    init_parser.add_argument("--run-date", required=True)
    init_parser.add_argument("--backfill-mode", default="daily")
    init_parser.add_argument("--v2-publish-policy", choices=["disabled", "seed-candidates-only", "formal"], default="seed-candidates-only")
    init_parser.add_argument("--formal-seed-publish-allowed", action="store_true")
    init_parser.add_argument("--scheduled-daily-switched", action="store_true")
    init_parser.add_argument("--dry-run", action="store_true")

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--run-date", required=True)
    run_parser.add_argument("--strict-publish", action="store_true")
    run_parser.add_argument("--json", action="store_true")

    artifact_parser = sub.add_parser("artifact")
    artifact_parser.add_argument("--run-date", required=True)
    artifact_parser.add_argument("--artifact", required=True)
    artifact_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "init":
        payload = init_manifest_with_policy(
            args.run_date,
            dry_run=args.dry_run,
            backfill_mode=args.backfill_mode,
            v2_publish_policy=args.v2_publish_policy,
            formal_seed_publish_allowed=args.formal_seed_publish_allowed,
            scheduled_daily_switched=args.scheduled_daily_switched,
        )
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "artifact":
        result = validate_one(args.run_date, args.artifact)
    else:
        result = validate_run(args.run_date, strict_publish=getattr(args, "strict_publish", False))
    if getattr(args, "json", False):
        safe_print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        safe_print(f"VALIDATE_RESEARCH_RUN: {result['status']} checked={len(result['checked'])} errors={len(result['errors'])}")
        for error in result["errors"][:40]:
            safe_print(f"ERROR: {error}")
    return 0 if result["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
