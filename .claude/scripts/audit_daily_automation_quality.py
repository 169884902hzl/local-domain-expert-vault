"""Audit daily arXiv/Gemini/Codex quality readiness without mutating core artifacts."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
from typing import Any

from kb_common import safe_print, safe_write, vault_path
from research_seed_v2_common import (
    ARTIFACT_SCHEMAS,
    FORMAL_SEED_REQUIRED_FILES,
    PUBLISH_REQUIRED_ARTIFACTS,
    artifact_dir,
    run_dir,
    validate_artifact,
    validate_json_file,
    v2_rel,
)
from validate_research_run import validate_run as validate_v2_run


MIN_SUCCESSFUL_READS = 10
DEFAULT_MIN_RAW_CANDIDATES = 6
QUALITY_REPORT_DIR = vault_path("projects", "arxiv-daily", "quality")
PDF_REPAIR_DIR = vault_path("projects", "arxiv-daily", "zotero-pdf-repair")
CONTRACT_DIR = vault_path("projects", "research-agenda", "workflow-contracts")
SIDECAR_EFFECTIVE_DATE = "2026-05-11"
MANDATORY_BATTLE_EFFECTIVE_DATE = "2026-05-14"
PDF_REPAIR_SUCCESS_RESULTS = {"exists_stored_pdf", "created_stored_pdf", "exists_file_pdf_attachment"}
VALID_CANDIDATE_GROUPS = {"evidence_bound", "wild_engineering"}
VALID_IDEA_ARCHETYPES = {
    "method_improvement",
    "interface_invention",
    "failure_model",
    "evaluation_metric",
    "closed_loop_system",
    "data_or_labeling_strategy",
    "representation_shift",
    "control_policy_mechanism",
    "instrumentation_or_sensing",
}
VALID_CONTRIBUTION_SHAPES = {
    "architecture",
    "algorithm",
    "control_interface",
    "mechanism",
    "system",
    "method_improvement",
    "evaluation_protocol",
    "benchmark",
    "failure_model",
    "dataset",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _field(text: str, key: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(key)}:\s*(.*?)\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip().strip('"') if match else ""


def _int_field(text: str, key: str, default: int = 0) -> int:
    raw = _field(text, key)
    try:
        return int(float(raw))
    except Exception:
        return default


def _json_read(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(_read(path))
    except Exception as exc:
        return {"_read_error": f"{type(exc).__name__}:{exc}"}
    return data if isinstance(data, dict) else {"_read_error": "json_root_not_object"}


def _pdf_repair_verification(run_date: str) -> tuple[str, int]:
    if not PDF_REPAIR_DIR.exists():
        return "", 0
    reports = sorted(PDF_REPAIR_DIR.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for report_path in reports:
        report = _json_read(report_path)
        results = report.get("results")
        if not isinstance(results, list):
            continue
        date_results = [item for item in results if isinstance(item, dict) and item.get("run_date") == run_date]
        if not date_results:
            continue
        if all(str(item.get("result") or "") in PDF_REPAIR_SUCCESS_RESULTS for item in date_results):
            return _rel(report_path), len(date_results)
    return "", 0


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(vault_path())).replace("\\", "/")
    except ValueError:
        return str(path)


def _read_lines_for_section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = line.strip() == f"## {heading}"
            continue
        if in_section:
            out.append(line)
    return out


def _reading_items(text: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line in _read_lines_for_section(text, "Reading"):
        match = re.match(
            r"^\s*-\s*zotero_key=(?P<key>\S+)\s+ingest=(?P<ingest>\S+)\s+read=(?P<read>\S+)\s+read_elapsed_sec=(?P<elapsed>\S+)",
            line,
        )
        if not match:
            continue
        item = match.groupdict()
        try:
            item["read_elapsed_sec"] = float(item["elapsed"])
        except Exception:
            item["read_elapsed_sec"] = None
        items.append(item)
    return items


def _run_log(run_date: str) -> tuple[Path, str]:
    path = vault_path("projects", "arxiv-daily", f"{run_date}-run.md")
    return path, _read(path)


def _recovery_log(run_date: str) -> tuple[Path, str]:
    path = vault_path("projects", "arxiv-daily", f"{run_date}-backlog-recovery.md")
    return path, _read(path)


def _backlog_path(run_date: str) -> Path:
    return vault_path("projects", "arxiv-daily", f"{run_date}-reading-backlog.md")


def _greenhouse_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "divergent", f"{run_date}-gemini-raw-candidates.json")


def _codex_report_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "reviews", f"{run_date}-codex-seed-review.md")


def _codex_packet_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "reviews", f"{run_date}-codex-seed-review-packet.json")


def _codex_pending_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "reviews", f"{run_date}-codex-review-pending.json")


def _battle_packet_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "model-debates", f"{run_date}-gemini-deepseek-debate-packet.json")


def _battle_report_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "reviews", f"{run_date}-gemini-deepseek-debate.md")


def _agenda_delta_path(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")


def _concept_delta_paths(run_date: str) -> tuple[Path, Path]:
    root = vault_path("projects", "research-agenda", "concept-deltas")
    return root / f"{run_date}-concept-delta.json", root / f"{run_date}-concept-delta.md"


def _mechanism_graph_dir(run_date: str) -> Path:
    return vault_path("projects", "research-agenda", "mechanism-graphs", run_date)


def _classify_codex_state(run_date: str) -> dict[str, Any]:
    report = _codex_report_path(run_date)
    packet = _codex_packet_path(run_date)
    pending = _codex_pending_path(run_date)
    packet_data = _json_read(packet)
    if report.exists():
        state = "review_completed"
    elif pending.exists():
        state = "review_pending"
    elif packet.exists():
        state = "packet_prepared_no_report"
    else:
        state = "missing"
    return {
        "state": state,
        "report_path": _rel(report) if report.exists() else "",
        "packet_path": _rel(packet) if packet.exists() else "",
        "pending_path": _rel(pending) if pending.exists() else "",
        "raw_gemini_candidate_count": len(packet_data.get("raw_gemini_candidates", []))
        if isinstance(packet_data.get("raw_gemini_candidates", []), list)
        else 0,
        "allowed_actions": packet_data.get("review_boundary", {}).get("allowed_actions", []),
        "quality_boundary_present": bool(packet_data.get("quality_boundary")),
    }


def _classify_mandatory_battle(run_date: str, agenda_delta_text: str) -> dict[str, Any]:
    packet_path = _battle_packet_path(run_date)
    report_path = _battle_report_path(run_date)
    pending_path = _codex_pending_path(run_date)
    packet = _json_read(packet_path)
    pending = _json_read(pending_path)
    status = str(packet.get("status") or pending.get("mandatory_model_battle_status") or _field(agenda_delta_text, "mandatory_model_battle_status") or "")
    return {
        "effective_date": MANDATORY_BATTLE_EFFECTIVE_DATE,
        "required": run_date >= MANDATORY_BATTLE_EFFECTIVE_DATE,
        "status": status,
        "packet_path": _rel(packet_path) if packet_path.exists() else "",
        "report_path": _rel(report_path) if report_path.exists() else "",
        "pending_status": pending.get("mandatory_model_battle_status", "") if pending else "",
        "selected_items": packet.get("counts", {}).get("selected_items", 0) if packet else 0,
        "deepseek_reviews": packet.get("counts", {}).get("deepseek_reviews", 0) if packet else 0,
        "gemini_mutations": packet.get("counts", {}).get("gemini_mutations", 0) if packet else 0,
        "packet_read_error": packet.get("_read_error", ""),
        "provider_status": packet.get("provider_status", {}) if packet else {},
    }


def _issue(level: str, code: str, detail: str, evidence: str = "") -> dict[str, str]:
    return {"level": level, "code": code, "detail": detail, "evidence": evidence}


def _scan_for_direct_seed_writers() -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    scripts_dir = vault_path(".claude", "scripts")
    for path in sorted(scripts_dir.glob("*.py")):
        if path.name in {"publish_research_run.py", "audit_daily_automation_quality.py"}:
            continue
        text = _read(path)
        issues.extend(_scan_text_for_seed_writer(path, text))
    return issues


def _scan_scheduled_daily_rollout_policy() -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    wrapper = vault_path(".claude", "scripts", "run_daily_arxiv_task.ps1")
    text = _read(wrapper)
    if re.search(r"--v2-publish-policy\s+['\"]?formal\b", text):
        issues.append(
            _issue(
                "FAIL",
                "v2_scheduled_formal_publish_configured",
                "Scheduled daily wrapper is configured for formal v2 publish.",
                _rel(wrapper),
            )
        )
    if "--allow-formal-seed-publish" in text:
        issues.append(
            _issue(
                "FAIL",
                "v2_scheduled_formal_publish_allowed",
                "Scheduled daily wrapper must not enable formal seed publish by default.",
                _rel(wrapper),
            )
        )
    return issues


def _node_tokens(node: ast.AST) -> list[str]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.Add)):
        return [*_node_tokens(node.left), *_node_tokens(node.right)]
    if isinstance(node, ast.Constant):
        return [str(node.value)]
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [node.attr, *_node_tokens(node.value)]
    if isinstance(node, ast.Call):
        arg_tokens: list[str] = []
        for arg in node.args:
            arg_tokens.extend(_node_tokens(arg))
        for keyword in node.keywords:
            arg_tokens.extend(_node_tokens(keyword.value))
        if isinstance(node.func, ast.Name):
            return [f"{node.func.id}()", *arg_tokens]
        if isinstance(node.func, ast.Attribute):
            return [node.func.attr, *_node_tokens(node.func.value), *arg_tokens]
    if isinstance(node, ast.Subscript):
        return [*_node_tokens(node.value), *_node_tokens(node.slice)]
    if isinstance(node, ast.JoinedStr):
        return ["".join(str(part.value) for part in node.values if isinstance(part, ast.Constant))]
    return []


def _expr_may_target_seed(node: ast.AST, seed_vars: set[str]) -> bool:
    tokens = _node_tokens(node)
    lowered = [token.lower().replace("\\", "/") for token in tokens]
    if any(token in seed_vars for token in tokens):
        return True
    joined = "/".join(lowered)
    if "idea_bank/seed" in joined or "idea_bank" in joined and "/seed" in joined:
        return True
    has_seed = "seed" in lowered
    has_dynamic_state = any(token in {"recommended", "state", "target_state"} for token in lowered)
    if "idea_bank_dir" in lowered and (has_seed or has_dynamic_state):
        return True
    if "agenda_root()" in lowered and "idea_bank" in lowered and (has_seed or has_dynamic_state):
        return True
    return False


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = ".".join(_node_tokens(func.value))
        return f"{base}.{func.attr}" if base else func.attr
    return ""


def _scan_text_for_seed_writer(path: Path, text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if "write_seed_folder" in text and path.name not in {"audit_daily_automation_quality.py"}:
        issues.append(
            _issue("FAIL", "v2_direct_seed_writer_outside_publish", "Legacy write_seed_folder symbol appears outside publish_research_run.py.", _rel(path))
        )
    try:
        tree = ast.parse(text.lstrip("\ufeff"), filename=str(path))
    except SyntaxError as exc:
        return issues + [_issue("WARN", "v2_seed_writer_scan_parse_failed", f"{type(exc).__name__}:{exc}", _rel(path))]
    seed_vars: set[str] = set()
    writer_calls = {"safe_write", "write_text", "write_json", "open", "mkdir", "rename", "replace", "move", "copy2", "rmtree"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            if value is not None and _expr_may_target_seed(value, seed_vars):
                for target in targets:
                    if isinstance(target, ast.Name):
                        seed_vars.add(target.id)
        if isinstance(node, ast.Call):
            name = _call_name(node)
            short = name.split(".")[-1]
            if short not in writer_calls:
                continue
            call_parts = list(node.args) + [keyword.value for keyword in node.keywords]
            target_exprs = call_parts
            if isinstance(node.func, ast.Attribute):
                target_exprs.append(node.func.value)
            if any(_expr_may_target_seed(expr, seed_vars) for expr in target_exprs):
                issues.append(
                    _issue(
                        "FAIL",
                        "v2_direct_seed_writer_outside_publish",
                        f"Potential formal seed mutation call `{name}` detected outside publish_research_run.py.",
                        f"{_rel(path)}:{getattr(node, 'lineno', '?')}",
                    )
                )
    return issues


def _audit_v2_state_machine(run_date: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    run_path = run_dir(run_date)
    artifacts_path = artifact_dir(run_date)
    publish_result = run_path / "publish" / "publish-result.json"
    legacy_publish_result = artifacts_path / "publish-result.json"
    if not publish_result.exists() and legacy_publish_result.exists():
        publish_result = legacy_publish_result
    manifest_path = run_path / "manifest.json"
    manifest = _json_read(manifest_path)
    validation: dict[str, Any]
    if run_path.exists():
        validation = validate_v2_run(run_date, strict_publish=publish_result.exists())
        if validation.get("status") != "success":
            for error in validation.get("errors", [])[:30]:
                issues.append(_issue("FAIL", "v2_schema_or_hash_invalid", str(error), _rel(run_path)))
        for artifact_name in ARTIFACT_SCHEMAS:
            artifact_path = artifacts_path / artifact_name
            if artifact_path.exists():
                artifact_errors = validate_artifact(run_date, artifact_name)
                for error in artifact_errors[:20]:
                    issues.append(_issue("FAIL", "v2_artifact_schema_invalid", f"{artifact_name}: {error}", _rel(artifact_path)))
    else:
        validation = {
            "schema_version": "research_run_validation.v1",
            "run_date": run_date,
            "status": "not_started",
            "checked": [],
            "errors": [],
        }

    if publish_result.exists():
        publish_data = _json_read(publish_result)
        published = publish_data.get("published", []) if isinstance(publish_data.get("published"), list) else []
        policy = str(manifest.get("v2_publish_policy") or publish_data.get("v2_publish_policy") or "")
        formal_allowed = manifest.get("formal_seed_publish_allowed") is True
        manifest_formal_written = manifest.get("formal_seed_written") is True
        if publish_data.get("v2_publish_policy") and policy and publish_data.get("v2_publish_policy") != policy:
            issues.append(_issue("FAIL", "v2_publish_policy_mismatch", "Publish result policy disagrees with manifest policy.", _rel(publish_result)))
        if published:
            for artifact_name in PUBLISH_REQUIRED_ARTIFACTS:
                if not (artifacts_path / artifact_name).exists():
                    issues.append(_issue("FAIL", "v2_publish_required_artifact_missing", artifact_name, _rel(artifacts_path / artifact_name)))
            if not manifest_formal_written:
                issues.append(_issue("FAIL", "v2_manifest_not_marked_seed_written", "Publish result contains published seed but manifest formal_seed_written is false.", _rel(manifest_path)))
            if policy != "formal":
                issues.append(_issue("FAIL", "v2_formal_seed_written_policy_mismatch", "Formal seed was published while v2_publish_policy is not formal.", _rel(manifest_path)))
            if not formal_allowed:
                issues.append(_issue("FAIL", "v2_formal_seed_written_without_allow", "Formal seed was published without formal_seed_publish_allowed=true.", _rel(manifest_path)))
            if manifest.get("backfill_mode") != "daily":
                issues.append(_issue("FAIL", "v2_backfill_formal_seed_written", "Backfill run wrote a formal seed.", _rel(manifest_path)))
        if manifest_formal_written and not published:
            issues.append(_issue("FAIL", "v2_manifest_seed_written_without_publish_result", "Manifest says formal seed written but publish result has no published seed.", _rel(manifest_path)))
        if publish_data.get("formal_seed_written") and not manifest_formal_written:
            issues.append(_issue("FAIL", "v2_publish_result_manifest_seed_written_mismatch", "Publish result says formal seed written but manifest disagrees.", _rel(publish_result)))

    seed_root = vault_path("projects", "research-agenda", "idea_bank", "seed")
    v2_seed_count = 0
    legacy_seed_count = 0
    if seed_root.exists():
        for seed_dir in sorted(path for path in seed_root.iterdir() if path.is_dir()):
            v2_markers = [seed_dir / "artifact-hashes.json", seed_dir / "survival-decision.json"]
            if any(path.exists() for path in v2_markers):
                v2_seed_count += 1
                missing = [name for name in FORMAL_SEED_REQUIRED_FILES if not (seed_dir / name).exists()]
                for name in missing:
                    issues.append(_issue("FAIL", "v2_seed_missing_required_artifact", f"{seed_dir.name} missing {name}", _rel(seed_dir / name)))
            else:
                legacy_seed_count += 1

    override_root = vault_path("projects", "research-agenda", "overrides", "human-overrides", run_date)
    override_count = 0
    if override_root.exists():
        for override_path in sorted(override_root.glob("*.json")):
            override_count += 1
            errors = validate_json_file(override_path, "human_override.v1")
            data = _json_read(override_path)
            if data.get("reviewer") != "human":
                errors.append("reviewer_not_human")
            for error in errors:
                issues.append(_issue("FAIL", "v2_human_override_invalid", str(error), _rel(override_path)))

    issues.extend(_scan_for_direct_seed_writers())
    issues.extend(_scan_scheduled_daily_rollout_policy())
    return (
        {
            "run_dir": _rel(run_path) if run_path.exists() else "",
            "validation_status": validation.get("status", "not_started"),
            "checked": validation.get("checked", []),
            "errors": validation.get("errors", []),
            "publish_result": _rel(publish_result) if publish_result.exists() else "",
            "v2_publish_policy": manifest.get("v2_publish_policy", ""),
            "formal_seed_publish_allowed": bool(manifest.get("formal_seed_publish_allowed", False)),
            "scheduled_daily_switched": bool(manifest.get("scheduled_daily_switched", False)),
            "publish_required_artifacts": PUBLISH_REQUIRED_ARTIFACTS,
            "formal_seed_required_files": FORMAL_SEED_REQUIRED_FILES,
            "v2_seed_count": v2_seed_count,
            "legacy_seed_count": legacy_seed_count,
            "human_override_count": override_count,
            "boundary": "Only publish_research_run.py may create or modify formal seed folders.",
        },
        issues,
    )


def _readiness_from_label(label: str) -> str:
    if label == "promoted_to_seed":
        return "seed_ready"
    if label == "rewrite_needed":
        return "rewrite_required"
    if label == "parked_for_weekly_review":
        return "weekly_review"
    if label == "blocked_with_rescue_signal":
        return "rescue_only"
    return "untriaged"


def audit_run(run_date: str) -> dict[str, Any]:
    run_path, run_text = _run_log(run_date)
    recovery_path, recovery_text = _recovery_log(run_date)
    greenhouse_path = _greenhouse_path(run_date)
    greenhouse = _json_read(greenhouse_path)
    raw_candidates = greenhouse.get("raw_gemini_candidates", [])
    raw_candidates = raw_candidates if isinstance(raw_candidates, list) else []
    tier_counts = Counter(str(item.get("quality_tier", "unrated")) for item in raw_candidates if isinstance(item, dict))
    potential_tier_counts = Counter(
        str(item.get("potential_tier", item.get("quality_tier", "unrated")))
        for item in raw_candidates
        if isinstance(item, dict)
    )
    readiness_tier_counts = Counter(
        str(item.get("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled")))))
        for item in raw_candidates
        if isinstance(item, dict)
    )
    label_counts = Counter(str(item.get("greenhouse_label", "unlabeled")) for item in raw_candidates if isinstance(item, dict))
    group_counts = Counter(str(item.get("candidate_group", "unclassified") or "unclassified") for item in raw_candidates if isinstance(item, dict))
    shape_counts = Counter(str(item.get("contribution_shape", "unclassified") or "unclassified") for item in raw_candidates if isinstance(item, dict))
    issue_list: list[dict[str, str]] = []

    if not run_path.exists():
        issue_list.append(_issue("FAIL", "missing_run_log", "Daily run log is missing.", _rel(run_path)))
    status = _field(run_text, "status")
    agenda_status = _field(run_text, "agenda_update_status")
    recovery_status = _field(run_text, "recovery_status") or _field(recovery_text, "status")
    recovery_agenda_status = _field(recovery_text, "agenda_update_status")
    recovery_applied = (
        recovery_status == "success"
        and recovery_agenda_status in {"success", "skipped_no_focus_keys"}
        and status == "partial"
        and agenda_status not in {"success", "skipped_no_focus_keys"}
    )
    if recovery_applied:
        status = "success"
        agenda_status = recovery_agenda_status
    strict_kb = _field(run_text, "strict_kb_maintenance")
    successful_reads = _int_field(run_text, "new_imports_read_success")
    max_daily_reads = _int_field(run_text, "max_daily_reads")
    import_attempts = _int_field(run_text, "import_attempts")
    resumed_backlog_imports = _int_field(run_text, "resumed_backlog_imports")
    readings = _reading_items(run_text)
    failed_or_backlog_reads = [
        item for item in readings
        if not str(item.get("read", "")).startswith("success") and item.get("read") != "skipped"
    ]
    backlog = _backlog_path(run_date)
    agenda_delta = _agenda_delta_path(run_date)
    agenda_delta_text = _read(agenda_delta)
    concept_json_path, concept_md_path = _concept_delta_paths(run_date)
    concept_delta = _json_read(concept_json_path)
    mechanism_graph_dir = _mechanism_graph_dir(run_date)

    if status not in {"success", "partial"} and run_path.exists():
        issue_list.append(_issue("FAIL", "unknown_daily_status", f"Run status is `{status or 'missing'}`.", _rel(run_path)))
    if status == "partial":
        issue_list.append(_issue("WARN", "daily_partial", "Daily run ended partial; inspect recoverability and quality impact.", _rel(run_path)))
    if recovery_applied:
        issue_list.append(_issue("INFO", "recovered_run_log_stale", "Main run log was partial, but backlog recovery completed successfully.", _rel(recovery_path)))
    if agenda_status not in {"success", "skipped_no_focus_keys"} and run_path.exists():
        issue_list.append(_issue("FAIL", "agenda_not_ready", f"Agenda update status is `{agenda_status or 'missing'}`.", _rel(run_path)))
    if strict_kb not in {"success", "not_run", ""}:
        issue_list.append(_issue("FAIL", "strict_kb_failed", f"Strict KB maintenance status is `{strict_kb}`.", _rel(run_path)))
    if failed_or_backlog_reads and not backlog.exists():
        issue_list.append(_issue("FAIL", "missing_backlog_for_failed_reads", "Failed/backlog reads exist but backlog file is missing.", _rel(backlog)))
    if failed_or_backlog_reads and backlog.exists():
        issue_list.append(_issue("WARN", "read_partial_recoverable", f"{len(failed_or_backlog_reads)} reads remain failed/backlog and are recoverable.", _rel(backlog)))
    if import_attempts > 0 and max_daily_reads >= MIN_SUCCESSFUL_READS and successful_reads < MIN_SUCCESSFUL_READS:
        issue_list.append(_issue("WARN", "read_target_not_met", f"Successful reads {successful_reads} below target {MIN_SUCCESSFUL_READS}.", _rel(run_path)))
    if import_attempts == 0 and resumed_backlog_imports == 0 and run_path.exists():
        issue_list.append(_issue("WARN", "no_import_or_backlog_attempts", "No new import or backlog resume attempts were recorded.", _rel(run_path)))
    pdf_sync_markers = [
        "webdav_sync_note=linked_file_not_synced_by_webdav",
        "pdf_file_upload_failed",
        "linked_pdf_fallback_failed",
        "stored_pdf_required_failed",
        "stored_pdf_missing_existing",
        "status=pdf_pending",
    ]
    pdf_sync_hits = [marker for marker in pdf_sync_markers if marker in run_text]
    if pdf_sync_hits:
        repair_report, repair_count = _pdf_repair_verification(run_date)
        if repair_report:
            issue_list.append(
                _issue(
                    "INFO",
                    "zotero_pdf_sync_repaired",
                    "Historical Zotero PDF import errors are present in the run log, but repair verification confirms "
                    f"{repair_count} run items now have stored/file PDF attachments: " + ", ".join(pdf_sync_hits),
                    repair_report,
                )
            )
        else:
            issue_list.append(
                _issue(
                    "FAIL",
                    "zotero_pdf_sync_not_ready",
                    "Zotero import log contains PDF paths that are not confirmed syncable stored attachments: "
                    + ", ".join(pdf_sync_hits),
                    _rel(run_path),
                )
            )
    if not agenda_delta.exists() and agenda_status == "success":
        issue_list.append(_issue("FAIL", "missing_agenda_delta", "Agenda status says success but agenda delta is missing.", _rel(agenda_delta)))
    sidecars_expected = run_date >= SIDECAR_EFFECTIVE_DATE and agenda_status == "success"
    if sidecars_expected and not concept_md_path.exists():
        issue_list.append(_issue("WARN", "missing_concept_delta_md", "Agenda succeeded but concept delta markdown is missing.", _rel(concept_md_path)))
    if sidecars_expected and not concept_json_path.exists():
        issue_list.append(_issue("WARN", "missing_concept_delta_json", "Agenda succeeded but concept delta JSON is missing.", _rel(concept_json_path)))
    if concept_json_path.exists() and concept_delta.get("_read_error"):
        issue_list.append(_issue("WARN", "concept_delta_json_invalid", str(concept_delta.get("_read_error")), _rel(concept_json_path)))
    if sidecars_expected and successful_reads > 0 and not mechanism_graph_dir.exists():
        issue_list.append(_issue("WARN", "missing_mechanism_graph_dir", "Successful reads exist but mechanism graph sidecar directory is missing.", _rel(mechanism_graph_dir)))

    generator_status = str(greenhouse.get("generator_status", ""))
    min_raw = int(greenhouse.get("min_raw_candidates") or DEFAULT_MIN_RAW_CANDIDATES) if greenhouse else DEFAULT_MIN_RAW_CANDIDATES
    if agenda_status == "success" and not greenhouse_path.exists():
        issue_list.append(_issue("FAIL", "missing_greenhouse_archive", "Agenda succeeded but Gemini greenhouse archive is missing.", _rel(greenhouse_path)))
    if greenhouse_path.exists() and greenhouse.get("_read_error"):
        issue_list.append(_issue("FAIL", "greenhouse_json_invalid", str(greenhouse.get("_read_error")), _rel(greenhouse_path)))
    if greenhouse_path.exists() and len(raw_candidates) < min_raw:
        level = "WARN" if "under_generated_warning" in generator_status else "FAIL"
        issue_list.append(_issue(level, "raw_candidate_under_minimum", f"Raw candidates {len(raw_candidates)} below min {min_raw}.", _rel(greenhouse_path)))
    if greenhouse_path.exists() and not generator_status.startswith("gemini-divergent:success"):
        issue_list.append(_issue("FAIL", "gemini_not_success", f"Gemini generator status is `{generator_status or 'missing'}`.", _rel(greenhouse_path)))
    if greenhouse_path.exists() and not any(item.get("candidate_group") == "wild_engineering" for item in raw_candidates if isinstance(item, dict)):
        issue_list.append(_issue("WARN", "missing_wild_engineering_group", "No raw candidate is labelled wild_engineering.", _rel(greenhouse_path)))
    if greenhouse_path.exists() and not any(item.get("candidate_group") == "evidence_bound" for item in raw_candidates if isinstance(item, dict)):
        issue_list.append(_issue("WARN", "missing_evidence_bound_group", "No raw candidate is labelled evidence_bound.", _rel(greenhouse_path)))
    invalid_taxonomy_candidates = []
    for item in raw_candidates:
        if not isinstance(item, dict):
            continue
        invalid_fields = []
        if str(item.get("candidate_group", "") or "") not in VALID_CANDIDATE_GROUPS:
            invalid_fields.append("candidate_group")
        if str(item.get("idea_archetype", "") or "") not in VALID_IDEA_ARCHETYPES:
            invalid_fields.append("idea_archetype")
        if str(item.get("contribution_shape", "") or "") not in VALID_CONTRIBUTION_SHAPES:
            invalid_fields.append("contribution_shape")
        if invalid_fields:
            invalid_taxonomy_candidates.append({"title": item.get("title", "Untitled"), "invalid": invalid_fields})
    if invalid_taxonomy_candidates:
        issue_list.append(_issue("WARN", "raw_candidate_invalid_taxonomy", f"{len(invalid_taxonomy_candidates)} candidates have missing/invalid taxonomy fields.", _rel(greenhouse_path)))
    required_quality_fields = [
        "non_obvious_claim",
        "anti_combination_test",
        "strongest_baseline",
        "killer_experiment",
        "rescue_mutation",
        "claim_compression",
    ]
    weak_field_candidates = []
    for item in raw_candidates:
        if not isinstance(item, dict):
            continue
        missing = [field for field in required_quality_fields if not str(item.get(field, "")).strip()]
        if missing:
            weak_field_candidates.append({"title": item.get("title", "Untitled"), "missing": missing})
    if weak_field_candidates:
        issue_list.append(_issue("WARN", "raw_candidate_missing_quality_fields", f"{len(weak_field_candidates)} candidates miss required quality fields.", _rel(greenhouse_path)))
    promoted_c = [
        item.get("title", "Untitled")
        for item in raw_candidates
        if isinstance(item, dict)
        and item.get("greenhouse_label") == "promoted_to_seed"
        and item.get("quality_tier") not in {"S", "A"}
    ]
    if promoted_c:
        issue_list.append(_issue("FAIL", "non_top_tier_promoted", "Non-S/A candidate promoted: " + "; ".join(map(str, promoted_c[:5])), _rel(greenhouse_path)))
    if greenhouse_path.exists() and tier_counts.get("S", 0) + tier_counts.get("A", 0) == 0:
        issue_list.append(_issue("INFO", "quality_no_top_tier_seed_today", "No S/A raw candidate survived the local rubric; preserve greenhouse for review.", _rel(greenhouse_path)))

    mandatory_battle = _classify_mandatory_battle(run_date, agenda_delta_text)
    battle_expected = bool(mandatory_battle["required"] and greenhouse_path.exists() and generator_status.startswith("gemini-divergent:success"))
    if battle_expected and mandatory_battle["status"] != "success":
        issue_list.append(_issue("FAIL", "mandatory_model_battle_not_success", f"Mandatory model battle status is `{mandatory_battle['status'] or 'missing'}`.", mandatory_battle["packet_path"] or _rel(_battle_packet_path(run_date))))
    if battle_expected and not mandatory_battle["packet_path"]:
        issue_list.append(_issue("FAIL", "missing_mandatory_model_battle_packet", "DeepSeek battle is mandatory but packet is missing.", _rel(_battle_packet_path(run_date))))
    if battle_expected and not mandatory_battle["report_path"]:
        issue_list.append(_issue("FAIL", "missing_mandatory_model_battle_report", "DeepSeek battle is mandatory but markdown report is missing.", _rel(_battle_report_path(run_date))))
    if mandatory_battle["packet_read_error"]:
        issue_list.append(_issue("FAIL", "mandatory_model_battle_packet_invalid", str(mandatory_battle["packet_read_error"]), mandatory_battle["packet_path"]))
    if battle_expected and mandatory_battle["selected_items"] and len(raw_candidates) and mandatory_battle["selected_items"] < len(raw_candidates):
        issue_list.append(_issue("WARN", "mandatory_model_battle_partial_candidate_coverage", f"Battle selected {mandatory_battle['selected_items']} of {len(raw_candidates)} raw candidates.", mandatory_battle["packet_path"]))

    codex = _classify_codex_state(run_date)
    if greenhouse_path.exists() and codex["state"] == "missing":
        issue_list.append(_issue("WARN", "codex_review_missing", "No Codex packet, pending marker, or report found for this run.", _rel(_codex_report_path(run_date))))
    if codex["packet_path"] and codex["raw_gemini_candidate_count"] != len(raw_candidates):
        issue_list.append(_issue("WARN", "codex_packet_raw_count_mismatch", f"Packet raw count {codex['raw_gemini_candidate_count']} vs greenhouse {len(raw_candidates)}.", codex["packet_path"]))
    expected_actions = {"accept_for_user_review", "rewrite", "park", "reject_with_rescue"}
    if codex["allowed_actions"] and set(codex["allowed_actions"]) != expected_actions:
        issue_list.append(_issue("FAIL", "codex_allowed_actions_mismatch", f"Allowed actions are {codex['allowed_actions']}.", codex["packet_path"]))
    if codex["packet_path"] and not codex["quality_boundary_present"]:
        issue_list.append(_issue("FAIL", "codex_packet_missing_quality_boundary", "Codex packet lacks quality boundary.", codex["packet_path"]))

    contract_files = [
        CONTRACT_DIR / "daily-pipeline-contract.md",
        CONTRACT_DIR / "gemini-greenhouse-contract.md",
        CONTRACT_DIR / "codex-review-contract.md",
        CONTRACT_DIR / "weekly-top-tier-contract.md",
        CONTRACT_DIR / "failure-recovery-contract.md",
        CONTRACT_DIR / "idea-quality-source-basis.md",
        CONTRACT_DIR / "idea-taxonomy.md",
        CONTRACT_DIR / "daily-quality-checklist.md",
        CONTRACT_DIR / "intake-and-routing.md",
        CONTRACT_DIR / "daily-readable-workflow.md",
        CONTRACT_DIR / "provider-matrix.md",
        CONTRACT_DIR / "daily-readable-workflow.json",
        CONTRACT_DIR / "provider-matrix.json",
    ]
    missing_contracts = [path for path in contract_files if not path.exists()]
    if missing_contracts:
        issue_list.append(_issue("FAIL", "missing_workflow_contracts", "Missing contracts: " + ", ".join(_rel(path) for path in missing_contracts)))
    for contract_json, expected_schema in [
        (CONTRACT_DIR / "daily-readable-workflow.json", "daily_readable_workflow.v1"),
        (CONTRACT_DIR / "provider-matrix.json", "provider_matrix.v1"),
    ]:
        data = _json_read(contract_json)
        if data.get("_read_error"):
            issue_list.append(_issue("FAIL", "workflow_contract_json_invalid", f"{contract_json.name}: {data['_read_error']}", _rel(contract_json)))
        elif data and data.get("schema_version") != expected_schema:
            issue_list.append(_issue("FAIL", "workflow_contract_schema_mismatch", f"{contract_json.name} schema is `{data.get('schema_version')}` expected `{expected_schema}`.", _rel(contract_json)))

    v2_state_machine, v2_issues = _audit_v2_state_machine(run_date)
    issue_list.extend(v2_issues)

    fail_count = sum(1 for item in issue_list if item["level"] == "FAIL")
    warn_count = sum(1 for item in issue_list if item["level"] == "WARN")
    if fail_count:
        quality_readiness = "blocked"
    elif warn_count:
        quality_readiness = "needs_attention"
    else:
        quality_readiness = "ready"

    return {
        "run_date": run_date,
        "quality_readiness": quality_readiness,
        "status": status,
        "agenda_update_status": agenda_status,
        "recovery_status": recovery_status,
        "recovery_applied": recovery_applied,
        "recovery_log_path": _rel(recovery_path) if recovery_path.exists() else "",
        "strict_kb_maintenance": strict_kb,
        "run_log_path": _rel(run_path),
        "agenda_delta_path": _rel(agenda_delta) if agenda_delta.exists() else "",
        "reading": {
            "max_daily_reads": max_daily_reads,
            "import_attempts": import_attempts,
            "resumed_backlog_imports": resumed_backlog_imports,
            "new_imports_read_success": successful_reads,
            "recorded_read_items": len(readings),
            "failed_or_backlog_reads": failed_or_backlog_reads,
            "backlog_path": _rel(backlog) if backlog.exists() else "",
        },
        "gemini_greenhouse": {
            "path": _rel(greenhouse_path) if greenhouse_path.exists() else "",
            "generator_status": generator_status,
            "raw_candidate_limit": greenhouse.get("raw_candidate_limit"),
            "min_raw_candidates": min_raw,
            "raw_gemini_candidates": len(raw_candidates),
            "quality_tier_counts": dict(tier_counts),
            "quality_tier_semantics": "potential_only_not_seed_readiness",
            "potential_tier_counts": dict(potential_tier_counts),
            "readiness_tier_counts": dict(readiness_tier_counts),
            "greenhouse_label_counts": dict(label_counts),
            "candidate_group_counts": dict(group_counts),
            "contribution_shape_counts": dict(shape_counts),
            "weak_field_candidates": weak_field_candidates,
            "invalid_taxonomy_candidates": invalid_taxonomy_candidates,
        },
        "codex_review": codex,
        "mandatory_model_battle": mandatory_battle,
        "v2_state_machine": v2_state_machine,
        "contracts": [_rel(path) for path in contract_files if path.exists()],
        "notemd_sidecars": {
            "effective_date": SIDECAR_EFFECTIVE_DATE,
            "concept_delta_json": _rel(concept_json_path) if concept_json_path.exists() else "",
            "concept_delta_md": _rel(concept_md_path) if concept_md_path.exists() else "",
            "concept_count": concept_delta.get("concept_count", 0) if concept_delta and not concept_delta.get("_read_error") else 0,
            "mechanism_graph_dir": _rel(mechanism_graph_dir) if mechanism_graph_dir.exists() else "",
            "mechanism_graph_count": len(list(mechanism_graph_dir.glob("*.md"))) if mechanism_graph_dir.exists() else 0,
        },
        "issues": issue_list,
        "issue_counts": {"FAIL": fail_count, "WARN": warn_count, "INFO": sum(1 for item in issue_list if item["level"] == "INFO")},
    }


def render_markdown(report: dict[str, Any]) -> str:
    run_date = str(report["run_date"])
    lines = [
        "---",
        f'title: "Daily Automation Quality Audit - {run_date}"',
        "tags: [arxiv, automation, quality, research-agenda]",
        f'created: "{date.today().isoformat()}"',
        f'updated: "{date.today().isoformat()}"',
        'type: "permanent"',
        'status: "done"',
        f'summary: "Daily automation quality readiness: {report["quality_readiness"]}."',
        "---",
        "",
        f"# Daily Automation Quality Audit - {run_date}",
        "",
        "## Executive Verdict",
        "",
        f"- quality_readiness: `{report['quality_readiness']}`",
        f"- daily_status: `{report.get('status') or 'missing'}`",
        f"- agenda_update_status: `{report.get('agenda_update_status') or 'missing'}`",
        f"- recovery_status: `{report.get('recovery_status') or 'missing'}`",
        f"- recovery_applied: `{str(report.get('recovery_applied', False)).lower()}`",
        f"- strict_kb_maintenance: `{report.get('strict_kb_maintenance') or 'missing'}`",
        f"- issue_counts: {json.dumps(report.get('issue_counts', {}), ensure_ascii=False, sort_keys=True)}",
        "",
        "## Reading",
        "",
    ]
    reading = report.get("reading", {})
    for key in ["max_daily_reads", "import_attempts", "resumed_backlog_imports", "new_imports_read_success", "recorded_read_items", "backlog_path"]:
        lines.append(f"- {key}: {reading.get(key, '')}")
    failed_reads = reading.get("failed_or_backlog_reads", [])
    if failed_reads:
        lines.append("- failed_or_backlog_reads:")
        for item in failed_reads[:20]:
            lines.append(f"  - {item.get('key')} read={item.get('read')} ingest={item.get('ingest')}")
    else:
        lines.append("- failed_or_backlog_reads: none")
    greenhouse = report.get("gemini_greenhouse", {})
    lines.extend(
        [
            "",
            "## Gemini Greenhouse",
            "",
            f"- path: `{greenhouse.get('path', '')}`",
            f"- generator_status: `{greenhouse.get('generator_status', '')}`",
            f"- raw_gemini_candidates: {greenhouse.get('raw_gemini_candidates', 0)}",
            f"- min_raw_candidates: {greenhouse.get('min_raw_candidates', 0)}",
            f"- quality_tier_counts: {json.dumps(greenhouse.get('quality_tier_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- quality_tier_semantics: `{greenhouse.get('quality_tier_semantics', '')}`",
            f"- potential_tier_counts: {json.dumps(greenhouse.get('potential_tier_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- readiness_tier_counts: {json.dumps(greenhouse.get('readiness_tier_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- greenhouse_label_counts: {json.dumps(greenhouse.get('greenhouse_label_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- candidate_group_counts: {json.dumps(greenhouse.get('candidate_group_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- contribution_shape_counts: {json.dumps(greenhouse.get('contribution_shape_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- invalid_taxonomy_candidates: {len(greenhouse.get('invalid_taxonomy_candidates', []))}",
            "",
            "## Codex Review",
            "",
        ]
    )
    codex = report.get("codex_review", {})
    for key in ["state", "report_path", "packet_path", "pending_path", "raw_gemini_candidate_count", "allowed_actions", "quality_boundary_present"]:
        value = codex.get(key, "")
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False, sort_keys=True)
        lines.append(f"- {key}: {value}")
    v2_state = report.get("v2_state_machine", {})
    lines.extend(
        [
            "",
            "## Research Seed V2",
            "",
            f"- validation_status: `{v2_state.get('validation_status', 'not_started')}`",
            f"- run_dir: `{v2_state.get('run_dir', '')}`",
            f"- publish_result: `{v2_state.get('publish_result', '')}`",
            f"- v2_seed_count: {v2_state.get('v2_seed_count', 0)}",
            f"- legacy_seed_count: {v2_state.get('legacy_seed_count', 0)}",
            f"- human_override_count: {v2_state.get('human_override_count', 0)}",
            f"- boundary: {v2_state.get('boundary', '')}",
        ]
    )
    battle = report.get("mandatory_model_battle", {})
    lines.extend(
        [
            "",
            "## Mandatory Model Battle",
            "",
            f"- effective_date: {battle.get('effective_date', '')}",
            f"- required: {battle.get('required', False)}",
            f"- status: `{battle.get('status', '')}`",
            f"- packet_path: `{battle.get('packet_path', '')}`",
            f"- report_path: `{battle.get('report_path', '')}`",
            f"- selected_items: {battle.get('selected_items', 0)}",
            f"- deepseek_reviews: {battle.get('deepseek_reviews', 0)}",
            f"- gemini_mutations: {battle.get('gemini_mutations', 0)}",
        ]
    )
    sidecars = report.get("notemd_sidecars", {})
    lines.extend(
        [
            "",
            "## Notemd-Inspired Sidecars",
            "",
            f"- effective_date: {sidecars.get('effective_date', '')}",
            f"- concept_delta_json: `{sidecars.get('concept_delta_json', '')}`",
            f"- concept_delta_md: `{sidecars.get('concept_delta_md', '')}`",
            f"- concept_count: {sidecars.get('concept_count', 0)}",
            f"- mechanism_graph_dir: `{sidecars.get('mechanism_graph_dir', '')}`",
            f"- mechanism_graph_count: {sidecars.get('mechanism_graph_count', 0)}",
        ]
    )
    lines.extend(["", "## Issues", ""])
    issues = report.get("issues", [])
    if not issues:
        lines.append("- none")
    for issue in issues:
        evidence = f" evidence=`{issue.get('evidence')}`" if issue.get("evidence") else ""
        lines.append(f"- {issue.get('level')} `{issue.get('code')}`: {issue.get('detail')}{evidence}")
    lines.extend(
        [
            "",
            "## Contract Coverage",
            "",
        ]
    )
    for path in report.get("contracts", []):
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This audit does not promote, delete, or rewrite ideas.",
            "- `novelty_pressure` remains local-only and unconfirmed.",
            "- `quality_readiness=ready` means automation artifacts satisfy the contract checks; it does not mean a paper idea is accepted.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = audit_run(args.run_date)
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = QUALITY_REPORT_DIR / f"{args.run_date}-daily-quality-audit.json"
    md_path = QUALITY_REPORT_DIR / f"{args.run_date}-daily-quality-audit.md"
    if not args.dry_run:
        safe_write(json_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n", dry_run=False, backup=True)
        safe_write(md_path, render_markdown(report), dry_run=False, backup=True)
    if args.json:
        safe_print(json.dumps({**report, "json_path": _rel(json_path), "report_path": _rel(md_path)}, ensure_ascii=False, indent=2))
    else:
        safe_print(
            f"QUALITY_AUDIT status={report['quality_readiness']} "
            f"FAIL={report['issue_counts']['FAIL']} WARN={report['issue_counts']['WARN']} "
            f"report={_rel(md_path)}"
        )
    return 1 if report["issue_counts"]["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
