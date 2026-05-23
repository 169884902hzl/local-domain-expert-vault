"""Prepare and wrap the daily Codex seed-review task."""
from __future__ import annotations

import argparse
from collections import Counter
import contextlib
from datetime import date, datetime
from datetime import timedelta
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, vault_path
from research_agenda_common import DAILY_DIR, REVIEWS_DIR, rel, render_frontmatter, strip_quotes
from research_agenda_common import agenda_path
from research_agenda_review import iter_idea_folders, review_folder
from research_seed_v2_common import (
    artifact_dir,
    artifact_hashes,
    candidate_id,
    ensure_v2_dirs,
    read_json,
    write_run_artifact,
)


MAX_SNIPPET_CHARS = 1800
COMPACT_TOPIC_CHARS = 650
REVIEW_TAGS = ["research-agenda", "seed-review", "codex-review", "automation"]
CODEX_ALLOWED_ACTIONS = ["accept_for_user_review", "rewrite", "park", "reject_with_rescue"]
EXECUTION_REVIEW_FIELDS = [
    "no_hardware_pilot_feasibility",
    "public_dataset_or_sim_availability",
    "baseline_training_cost",
    "metric_automation",
    "data_leakage_risk",
    "minimal_repo_plan",
    "real_robot_pilot_complexity",
    "reproducibility_path",
    "compute_time_budget",
]
CODEX_EXECUTION_ACTIONS = {
    "accept_for_user_review",
    "rewrite_before_seed",
    "park_for_weekly",
    "reject_with_rescue",
    "requires_human_decision",
}
CODEX_CONFIDENCE_VALUES = {"high", "medium", "low"}
CODEX_EXECUTION_REQUIRED_REVIEW_FIELDS = ["candidate_id", "status", "action", *EXECUTION_REVIEW_FIELDS]
WEEKLY_TOP_TIER_ACTIONS = [
    "push_to_user_review",
    "rewrite_for_mechanism",
    "park_for_weekly_followup",
    "reject_with_rescue",
]
QUALITY_RUBRIC_WEIGHTS = {
    "mechanism_nonobviousness": 20,
    "engineering_pathology": 18,
    "baseline_killer": 16,
    "originality": 16,
    "experimentability": 12,
    "generalizable_contribution": 12,
    "evidence_fit": 6,
}
WEEKLY_TOP_TIER_RUBRIC = {
    "breakthrough_potential": "Can this become more than an incremental A+B combination?",
    "engineering_pathology_strength": "Is the idea grounded in a real robot failure mode?",
    "non_obvious_mechanism": "Does it state a causal mechanism or interface that is not obvious?",
    "baseline_survivability": "Does it name the strongest baseline and a way to survive it?",
    "killer_experiment_clarity": "Can a small decisive experiment kill or upgrade it?",
    "venue_fit": "Which top robotics venue shape does it plausibly fit?",
    "rescue_value": "If not ready, what valuable signal should be preserved?",
}
RERUN_REVIEW_ACTIONS = ["accept_for_user_review", "rewrite", "park", "reject_with_rescue"]
WORKFLOW_CONTRACTS = {
    "daily_pipeline": "projects/research-agenda/workflow-contracts/daily-pipeline-contract.md",
    "gemini_greenhouse": "projects/research-agenda/workflow-contracts/gemini-greenhouse-contract.md",
    "codex_review": "projects/research-agenda/workflow-contracts/codex-review-contract.md",
    "weekly_top_tier": "projects/research-agenda/workflow-contracts/weekly-top-tier-contract.md",
    "failure_recovery": "projects/research-agenda/workflow-contracts/failure-recovery-contract.md",
    "idea_quality_source_basis": "projects/research-agenda/workflow-contracts/idea-quality-source-basis.md",
    "idea_taxonomy": "projects/research-agenda/workflow-contracts/idea-taxonomy.md",
    "daily_quality_checklist": "projects/research-agenda/workflow-contracts/daily-quality-checklist.md",
    "intake_and_routing": "projects/research-agenda/workflow-contracts/intake-and-routing.md",
    "daily_readable_workflow": "projects/research-agenda/workflow-contracts/daily-readable-workflow.md",
    "provider_matrix": "projects/research-agenda/workflow-contracts/provider-matrix.md",
}
ENGINEERING_PATHOLOGY_MARKERS = [
    "occlusion",
    "self-occlusion",
    "latency",
    "contact",
    "calibration",
    "drift",
    "depth",
    "viewpoint",
    "reset",
    "sim-to-real",
    "tactile",
    "bimanual",
    "dlo",
    "deformable",
    "grasp",
    "failure",
]
NON_OBVIOUS_MARKERS = [
    "instead",
    "rather than",
    "because",
    "before",
    "unlike",
    "interface",
    "residual",
    "critic",
    "state",
    "topology",
    "memory",
    "counterfactual",
    "closed-loop",
]
BASELINE_SURVIVAL_MARKERS = [
    "baseline",
    "against",
    "ablation",
    "outperform",
    "fail",
    "kill",
    "falsify",
    "threshold",
    "control",
    "compare",
]
KILLER_EXPERIMENT_MARKERS = [
    "pilot",
    "metric",
    "baseline",
    "ablation",
    "falsify",
    "fail",
    "threshold",
    "success",
    "latency",
    "contact",
    "occlusion",
    "reset",
]
GENERIC_COMBINATION_MARKERS = [
    "combine",
    "combination of",
    "integrate",
    "add",
    "use x with y",
    "apply",
]
FINAL_IDEA_STRUCTURE_FIELDS = [
    "negative_claim_boundary",
    "core_insight",
    "pipeline_steps",
    "defense_patches",
    "baseline_matrix",
    "metric_suite",
    "risk_assumptions",
    "competition_map",
    "two_week_sprint",
]
WEEKLY_STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "based",
    "because",
    "between",
    "candidate",
    "control",
    "could",
    "daily",
    "from",
    "into",
    "local",
    "mechanism",
    "paper",
    "policy",
    "robot",
    "robotic",
    "system",
    "that",
    "this",
    "with",
}


def _quiet_safe_write(path: Path, content: str, *, dry_run: bool) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        safe_write(path, content, dry_run=dry_run, backup=True)


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _compact_text(value: Any, *, max_chars: int) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text[:max_chars]


def _readiness_from_label(label: str) -> str:
    if label == "promoted_to_seed":
        return "seed_ready"
    if label == "speculative_preserve":
        return "speculative_weekly_review"
    if label == "rewrite_needed":
        return "rewrite_required"
    if label == "parked_for_weekly_review":
        return "weekly_review"
    if label == "blocked_with_rescue_signal":
        return "rescue_only"
    return "untriaged"


def _normalize_candidate_readiness(item: dict[str, Any]) -> dict[str, Any]:
    tier = str(item.get("potential_tier") or item.get("quality_tier") or "legacy_unrated")
    item.setdefault("quality_tier", tier)
    item.setdefault("potential_tier", tier)
    item.setdefault("potential_score", item.get("research_quality_score"))
    item.setdefault("quality_tier_semantics", "potential_only_not_seed_readiness")
    item.setdefault("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled"))))
    item.setdefault("promotion_decision", {
        "promoted_to_seed": "promote_to_seed",
        "speculative_preserve": "preserve_for_weekly_breakthrough_review",
        "rewrite_needed": "rewrite_before_seed",
        "parked_for_weekly_review": "park_for_weekly_review",
        "blocked_with_rescue_signal": "rescue_signal_only",
    }.get(str(item.get("greenhouse_label", "")), "not_ready"))
    return item


def _body_excerpt(path: Path, *, max_chars: int = MAX_SNIPPET_CHARS) -> str:
    text = _read(path)
    parsed = extract_frontmatter(text)
    body = parsed[1] if parsed else text
    lines = [line.rstrip() for line in body.splitlines() if line.strip()]
    return "\n".join(lines)[:max_chars]


def _frontmatter(path: Path) -> dict[str, str]:
    parsed = extract_frontmatter(_read(path))
    return parse_frontmatter_map(parsed[0]) if parsed else {}


def _body_field(path: Path, key: str) -> str:
    pattern = f"- {key}:"
    for line in _read(path).splitlines():
        stripped = line.strip()
        if stripped.startswith(pattern):
            return strip_quotes(stripped.removeprefix(pattern).strip().strip("`"))
    return ""


def _run_log_errors(path: Path) -> list[str]:
    text = _read(path)
    if not text:
        return []
    lines = text.splitlines()
    errors: list[str] = []
    in_errors = False
    for line in lines:
        if line.startswith("## "):
            if in_errors:
                break
            in_errors = line.strip() == "## Errors"
            continue
        if not in_errors:
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if value and value != "none":
            errors.append(value)
    return errors


def _frontmatter_or_body_field(path: Path, key: str) -> str:
    fields = _frontmatter(path)
    value = fields.get(key, "")
    if value:
        return strip_quotes(value.strip().strip("`"))
    return _body_field(path, key)


def _read_greenhouse(run_date: str) -> dict[str, Any]:
    path = agenda_path("divergent", f"{run_date}-gemini-raw-candidates.json")
    if not path.exists():
        return {
            "path": rel(path),
            "exists": False,
            "raw_gemini_candidates": [],
            "parked_candidates": [],
            "blocked_candidates": [],
        }
    try:
        payload = json.loads(_read(path))
    except json.JSONDecodeError as exc:
        return {
            "path": rel(path),
            "exists": True,
            "error": f"invalid_json:{exc}",
            "raw_gemini_candidates": [],
            "parked_candidates": [],
            "blocked_candidates": [],
        }
    payload["path"] = rel(path)
    payload["exists"] = True
    payload.setdefault("quality_rubric_weights", QUALITY_RUBRIC_WEIGHTS)
    payload.setdefault("raw_gemini_candidates", [])
    for item in payload["raw_gemini_candidates"]:
        if not isinstance(item, dict):
            continue
        if "quality_tier" not in item:
            item["quality_tier"] = "legacy_unrated"
            item["research_quality_score"] = None
            item["novelty_hits"] = []
            item["novelty_pressure"] = {"status": "legacy_unrated", "pressure": "not_checked"}
        _normalize_candidate_readiness(item)
    payload.setdefault("parked_candidates", [])
    payload.setdefault("blocked_candidates", [])
    return payload


def _read_mandatory_model_battle(run_date: str) -> dict[str, Any]:
    packet_path = agenda_path("model-debates", f"{run_date}-gemini-deepseek-debate-packet.json")
    review_path = REVIEWS_DIR / f"{run_date}-gemini-deepseek-debate.md"
    pending_path = REVIEWS_DIR / f"{run_date}-codex-review-pending.json"
    pending: dict[str, Any] = {}
    try:
        pending = json.loads(_read(pending_path)) if pending_path.exists() else {}
    except json.JSONDecodeError:
        pending = {}
    packet: dict[str, Any] = {}
    if packet_path.exists():
        try:
            loaded = json.loads(_read(packet_path))
            packet = loaded if isinstance(loaded, dict) else {}
        except json.JSONDecodeError as exc:
            packet = {"_read_error": f"invalid_json:{exc}"}
    status = str(packet.get("status") or pending.get("mandatory_model_battle_status") or "")
    return {
        "required": True,
        "status": status,
        "packet_path": rel(packet_path) if packet_path.exists() else str(pending.get("mandatory_model_battle_packet", "")),
        "report_path": rel(review_path) if review_path.exists() else str(pending.get("mandatory_model_battle_report", "")),
        "selected_items": packet.get("counts", {}).get("selected_items", packet.get("selected_items", "")),
        "deepseek_reviews": packet.get("counts", {}).get("deepseek_reviews", ""),
        "gemini_mutations": packet.get("counts", {}).get("gemini_mutations", ""),
        "mutation_actions": packet.get("counts", {}).get("mutation_actions", {}),
        "provider_status": packet.get("provider_status", {}),
        "review_excerpt": _body_excerpt(review_path, max_chars=1800),
        "read_error": packet.get("_read_error", ""),
    }


def _parse_daily_run_completion(run_date: str) -> tuple[datetime | None, datetime | None, int | None]:
    log_path = vault_path("projects", "arxiv-daily", "scheduled-task.log")
    text = _read(log_path)
    if not text:
        return None, None, None
    start_pattern = re.compile(rf"\[(\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}) [^\]]+\] START DailyArxivEmbodiedAIScout")
    end_pattern = re.compile(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) [^\]]+\] END exit_code=(\d+)")
    active_start: datetime | None = None
    latest_start: datetime | None = None
    latest_end: datetime | None = None
    latest_exit: int | None = None
    for line in text.splitlines():
        start = start_pattern.search(line)
        if start:
            active_start = datetime.strptime(start.group(1), "%Y-%m-%d %H:%M:%S")
            latest_end = None
            latest_exit = None
            continue
        end = end_pattern.search(line)
        if end and active_start is not None and active_start.date().isoformat() == run_date:
            latest_start = active_start
            latest_end = datetime.strptime(end.group(1), "%Y-%m-%d %H:%M:%S")
            latest_exit = int(end.group(2))
    return latest_start, latest_end, latest_exit


def _file_mtime(path: Path) -> datetime | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime)


def check_daily_readiness(run_date: str) -> dict[str, str]:
    run_log = vault_path("projects", "arxiv-daily", f"{run_date}-run.md")
    recovery_log = vault_path("projects", "arxiv-daily", f"{run_date}-backlog-recovery.md")
    agenda_delta = vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")
    reasons: list[str] = []
    run_status = _body_field(run_log, "status") if run_log.exists() else ""
    agenda_status = _body_field(run_log, "agenda_update_status") if run_log.exists() else ""
    run_errors = _run_log_errors(run_log) if run_log.exists() else []
    recovery_status = _body_field(recovery_log, "status") if recovery_log.exists() else ""
    recovery_agenda_status = _body_field(recovery_log, "agenda_update_status") if recovery_log.exists() else ""
    battle_status = _body_field(agenda_delta, "mandatory_model_battle_status") if agenda_delta.exists() else ""
    battle_only_errors = all(error == "research_agenda_update_failed" for error in run_errors)
    battle_partial = (
        run_date >= "2026-05-14"
        and agenda_delta.exists()
        and agenda_status == "partial"
        and battle_status
        and battle_status != "success"
        and battle_only_errors
    )
    latest_start, latest_end, latest_exit = _parse_daily_run_completion(run_date)
    manual_success = run_log.exists() and (run_status == "success" or battle_partial) and (agenda_status in {"success", "skipped_no_focus_keys"} or battle_partial) and agenda_delta.exists()
    recovery_success = (
        recovery_log.exists()
        and recovery_status == "success"
        and recovery_agenda_status in {"success", "skipped_no_focus_keys"}
        and agenda_delta.exists()
    )

    if not run_log.exists():
        reasons.append("missing_daily_run_log")
    elif run_status != "success" and not recovery_success and not battle_partial:
        reasons.append(f"daily_run_not_success:{run_status or 'missing'}")
    if run_log.exists() and agenda_status not in {"success", "skipped_no_focus_keys"} and not recovery_success and not battle_partial:
        reasons.append(f"agenda_update_not_ready:{agenda_status or 'missing'}")
    if not agenda_delta.exists():
        reasons.append("missing_agenda_delta")
    if latest_end is None:
        if not manual_success and not recovery_success:
            reasons.append("missing_successful_wrapper_end")
    elif latest_exit != 0 and not manual_success and not recovery_success and not battle_partial:
        reasons.append(f"latest_wrapper_exit_nonzero:{latest_exit}")
    agenda_mtime = _file_mtime(agenda_delta)
    if latest_start is not None and agenda_mtime is not None and agenda_mtime < latest_start and not recovery_success:
        reasons.append("agenda_delta_older_than_latest_daily_start")

    return {
        "ready": "false" if reasons else "true",
        "reason": ";".join(reasons),
        "run_log": rel(run_log),
        "recovery_log": rel(recovery_log) if recovery_log.exists() else "",
        "agenda_delta": rel(agenda_delta),
        "daily_status": run_status,
        "agenda_update_status": agenda_status,
        "run_errors": ";".join(run_errors),
        "mandatory_model_battle_status": battle_status,
        "battle_partial_review_allowed": str(battle_partial).lower(),
        "recovery_status": recovery_status,
        "recovery_agenda_update_status": recovery_agenda_status,
        "latest_daily_start": latest_start.isoformat() if latest_start else "",
        "latest_daily_end": latest_end.isoformat() if latest_end else "",
        "latest_daily_exit_code": "" if latest_exit is None else str(latest_exit),
    }


def _review_report_done(run_date: str) -> bool:
    report = REVIEWS_DIR / f"{run_date}-codex-seed-review.md"
    if not report.exists():
        return False
    text = _read(report)
    return 'status: "done"' in text or "status: done" in text or "- status: `done`" in text


def _codex_review_output_complete(raw: str) -> bool:
    text = raw.strip()
    if not text:
        return False
    required_markers = [
        "# Daily Codex Seed Review",
        "## Executive Verdict",
        "- status: `done`",
        "## Shortlist For User",
        "## Creativity Preservation",
        "## Next 24 Hours",
    ]
    if not all(marker in text for marker in required_markers):
        return False
    allowed_actions_present = any(action in text for action in CODEX_ALLOWED_ACTIONS)
    return allowed_actions_present and "boundary: no paper claim is accepted" in text


def _codex_nonblocking_exit_reason(raw: str, codex_exit_code: int) -> str:
    if codex_exit_code == 0:
        return ""
    text = raw.lower()
    if "opentelemetry" in text or "127.0.0.1:4318" in text:
        return "post_output_telemetry_error"
    if "could not be terminated" in text or "operation attempted is not supported" in text:
        return "post_output_cleanup_error"
    return "post_output_nonzero_exit"


def _codex_exit_diagnostic_text(run_date: str, raw: str) -> str:
    pieces = [raw]
    for suffix in [".err.log", ".events.log"]:
        path = REVIEWS_DIR / f"{run_date}-codex-seed-review{suffix}"
        if path.exists():
            pieces.append(_read(path))
    return "\n".join(pieces)


def _pending_marker_exists(run_date: str) -> bool:
    return (REVIEWS_DIR / f"{run_date}-codex-review-pending.json").exists()


def resolve_review_run_date(run_date: str, *, catch_up: bool = False, days_back: int = 7) -> tuple[str, str]:
    if not catch_up:
        return run_date, "requested_date"
    today_date = date.fromisoformat(run_date)
    for offset in range(days_back + 1):
        candidate = (today_date - timedelta(days=offset)).isoformat()
        if _review_report_done(candidate):
            continue
        readiness = check_daily_readiness(candidate)
        if readiness["ready"] == "true" and (_pending_marker_exists(candidate) or (DAILY_DIR / f"{candidate}-agenda-delta.md").exists()):
            reason = "requested_date" if candidate == run_date else f"catch_up_unreviewed:{candidate}"
            return candidate, reason
    return run_date, "no_catch_up_candidate"


def _collect_ideas() -> list[dict[str, Any]]:
    ideas: list[dict[str, Any]] = []
    for state, folder in iter_idea_folders():
        if state == "archived":
            continue
        review = review_folder(folder, state)
        idea_path = folder / "idea.md"
        fields = _frontmatter(idea_path)
        if state == "rejected":
            idea_chars = 700
            evidence_chars = 500
            experiment_chars = 0
            risk_chars = 0
        else:
            idea_chars = MAX_SNIPPET_CHARS
            evidence_chars = 1200
            experiment_chars = 1000
            risk_chars = 800
        ideas.append(
            {
            "path": review["path"],
                "slug": folder.name,
                "title": review["title"],
                "state": review["state"],
                "score": review["score"],
                "recommended_state": review["recommended_state"],
                "evidence_count": review["evidence_count"],
                "recent_evidence_count": review["recent_evidence_count"],
                "has_similar_work": review["has_similar_work"],
                "has_novelty_argument": review["has_novelty_argument"],
                "has_experiment_plan": review["has_experiment_plan"],
                "has_risk_review": review["has_risk_review"],
                "quality_flags": review["quality_flags"],
                "generated_by_ideate": review["generated_by_ideate"],
                "created": strip_quotes(fields.get("created", "")),
                "updated": strip_quotes(fields.get("updated", "")),
            "generation_rule": strip_quotes(fields.get("generation_rule", "")),
            "generator_status": strip_quotes(fields.get("generator_status", "")),
            "quality_tier": strip_quotes(fields.get("quality_tier", "")) or _body_field(idea_path, "quality_tier"),
            "quality_tier_semantics": strip_quotes(fields.get("quality_tier_semantics", "")) or _body_field(idea_path, "quality_tier_semantics"),
            "potential_tier": strip_quotes(fields.get("potential_tier", "")) or _body_field(idea_path, "potential_tier"),
            "potential_score": strip_quotes(fields.get("potential_score", "")) or _body_field(idea_path, "potential_score"),
            "readiness_tier": strip_quotes(fields.get("readiness_tier", "")) or _body_field(idea_path, "readiness_tier"),
            "promotion_decision": strip_quotes(fields.get("promotion_decision", "")) or _body_field(idea_path, "promotion_decision"),
            "candidate_group": strip_quotes(fields.get("candidate_group", "")) or _body_field(idea_path, "candidate_group"),
            "origin_type": strip_quotes(fields.get("origin_type", "")) or _body_field(idea_path, "origin_type"),
            "research_claim_type": strip_quotes(fields.get("research_claim_type", "")) or _body_field(idea_path, "research_claim_type"),
            "bottleneck_type": strip_quotes(fields.get("bottleneck_type", "")) or _body_field(idea_path, "bottleneck_type"),
            "evidence_mode": strip_quotes(fields.get("evidence_mode", "")) or _body_field(idea_path, "evidence_mode"),
            "risk_class": strip_quotes(fields.get("risk_class", "")) or _body_field(idea_path, "risk_class"),
            "world_model_role": strip_quotes(fields.get("world_model_role", "")) or _body_field(idea_path, "world_model_role"),
            "portfolio_slot": strip_quotes(fields.get("portfolio_slot", "")) or _body_field(idea_path, "portfolio_slot"),
            "research_quality_score": strip_quotes(fields.get("research_quality_score", "")) or _body_field(idea_path, "research_quality_score"),
            "evidence_support_score": strip_quotes(fields.get("evidence_support_score", "")) or _body_field(idea_path, "evidence_support_score"),
            "support_score": strip_quotes(fields.get("support_score", "")) or _body_field(idea_path, "support_score"),
            "originality_score": strip_quotes(fields.get("originality_score", "")) or _body_field(idea_path, "originality_score"),
            "engineering_value_score": strip_quotes(fields.get("engineering_value_score", "")) or _body_field(idea_path, "engineering_value_score"),
            "sharpness_score": strip_quotes(fields.get("sharpness_score", "")) or _body_field(idea_path, "sharpness_score"),
            "evidence_execution_score": strip_quotes(fields.get("evidence_execution_score", "")) or _body_field(idea_path, "evidence_execution_score"),
            "ordinaryness_penalty": strip_quotes(fields.get("ordinaryness_penalty", "")) or _body_field(idea_path, "ordinaryness_penalty"),
            "contribution_shape": strip_quotes(fields.get("contribution_shape", "")) or _body_field(idea_path, "contribution_shape"),
            "decision_status": strip_quotes(fields.get("decision_status", "")) or _body_field(idea_path, "decision_status"),
                "claim_status": strip_quotes(fields.get("claim_status", "")) or _body_field(idea_path, "claim_status"),
                "has_generated_similar_work": review.get("has_generated_similar_work", False),
                "has_generated_novelty_argument": review.get("has_generated_novelty_argument", False),
                "has_generated_experiment_plan": review.get("has_generated_experiment_plan", False),
                "has_generated_risk_review": review.get("has_generated_risk_review", False),
                "idea_excerpt": _body_excerpt(folder / "idea.md", max_chars=idea_chars),
                "evidence_excerpt": _body_excerpt(folder / "evidence_pack.md", max_chars=evidence_chars),
                "experiment_excerpt": _body_excerpt(folder / "experiment_plan.md", max_chars=experiment_chars),
                "risk_excerpt": _body_excerpt(folder / "risk_review.md", max_chars=risk_chars),
            }
        )
    return sorted(ideas, key=lambda item: (item["state"] == "rejected", -item["score"], item["title"]))


def _compact_greenhouse_candidate(item: dict[str, Any]) -> dict[str, Any]:
    item = _normalize_candidate_readiness(dict(item))
    keep = [
        "title",
        "candidate_group",
        "greenhouse_label",
        "quality_tier",
        "quality_tier_semantics",
        "potential_tier",
        "potential_score",
        "readiness_tier",
        "promotion_decision",
        "research_quality_score",
        "research_quality_components",
        "evidence_support_score",
        "support_score",
        "originality_score",
        "engineering_value_score",
        "sharpness_score",
        "evidence_execution_score",
        "ordinaryness_penalty",
        "origin_type",
        "research_claim_type",
        "bottleneck_type",
        "evidence_mode",
        "risk_class",
        "world_model_role",
        "portfolio_slot",
        "idea_archetype",
        "contribution_shape",
        "problem",
        "physical_failure_scene",
        "engineering_pathology",
        "mechanism",
        "interface",
        "interface_innovation",
        "optimization_space",
        "loss_placement",
        "decoder_boundary",
        "manifold_safety",
        "hypothesis",
        "non_obvious_claim",
        "naive_combination_version",
        "strongest_baseline_kill_path",
        "post_kill_mutation",
        "anti_combination_test",
        "top_tier_rationale",
        "engineering_loop",
        "method_improvement_claim",
        "original_method_failure",
        "replacement_or_coupled_technique",
        "why_improvement_not_patch",
        "why_now",
        "strongest_baseline",
        "baseline_failure_mode",
        "killer_experiment",
        "reviewer_kill_shot",
        "rescue_mutation",
        "claim_compression",
        "online_or_offline_mode",
        "minimum_no_hardware_pilot",
        "baseline_kill_table",
        "what_would_make_this_not_a_paper",
        "reviewer_pre_mortem",
        "falsification_discriminates_mechanism",
        "lab_fit",
        "hardware_assumptions",
        "negative_claim_boundary",
        "version_evolution_story",
        "core_insight",
        "pipeline_steps",
        "defense_patches",
        "baseline_matrix",
        "metric_suite",
        "risk_assumptions",
        "competition_map",
        "two_week_sprint",
        "pilot",
        "baselines",
        "metrics",
        "falsification",
        "novelty_risk",
        "rescue_signal",
        "evidence_links",
        "novelty_pressure",
        "novelty_hits",
        "promotion_reason",
        "issues",
    ]
    compact: dict[str, Any] = {}
    for key in keep:
        value = item.get(key)
        if isinstance(value, str):
            compact[key] = _compact_text(value, max_chars=700)
        elif isinstance(value, list):
            compact[key] = value[:6]
        elif isinstance(value, dict):
            compact[key] = value
        elif value not in (None, ""):
            compact[key] = value
    return compact


def _compact_seed_candidate(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": item.get("path", ""),
        "title": item.get("title", ""),
        "state": item.get("state", ""),
        "score": item.get("score", 0),
        "evidence_count": item.get("evidence_count", 0),
        "quality_tier": item.get("quality_tier", ""),
        "quality_tier_semantics": item.get("quality_tier_semantics", ""),
        "potential_tier": item.get("potential_tier", item.get("quality_tier", "")),
        "potential_score": item.get("potential_score", item.get("research_quality_score", "")),
        "readiness_tier": item.get("readiness_tier", ""),
        "promotion_decision": item.get("promotion_decision", ""),
        "candidate_group": item.get("candidate_group", ""),
        "origin_type": item.get("origin_type", ""),
        "research_claim_type": item.get("research_claim_type", ""),
        "bottleneck_type": item.get("bottleneck_type", ""),
        "evidence_mode": item.get("evidence_mode", ""),
        "risk_class": item.get("risk_class", ""),
        "world_model_role": item.get("world_model_role", ""),
        "portfolio_slot": item.get("portfolio_slot", ""),
        "research_quality_score": item.get("research_quality_score", ""),
        "evidence_support_score": item.get("evidence_support_score", ""),
        "support_score": item.get("support_score", ""),
        "originality_score": item.get("originality_score", ""),
        "engineering_value_score": item.get("engineering_value_score", ""),
        "sharpness_score": item.get("sharpness_score", ""),
        "evidence_execution_score": item.get("evidence_execution_score", ""),
        "ordinaryness_penalty": item.get("ordinaryness_penalty", ""),
        "contribution_shape": item.get("contribution_shape", ""),
        "claim_status": item.get("claim_status", ""),
        "idea_excerpt": _compact_text(item.get("idea_excerpt", ""), max_chars=900),
        "experiment_excerpt": _compact_text(item.get("experiment_excerpt", ""), max_chars=550),
        "risk_excerpt": _compact_text(item.get("risk_excerpt", ""), max_chars=400),
    }


def _local_evidence_briefs(run_date: str) -> list[dict[str, str]]:
    agenda_daily = vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")
    briefs: list[dict[str, str]] = []
    in_section = False
    for line in _read(agenda_daily).splitlines():
        stripped = line.strip()
        if stripped == "## Newly Read Evidence":
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section or not stripped.startswith("- [["):
            continue
        match = re.search(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", stripped)
        if not match:
            continue
        note_slug = match.group(1)
        display_title = match.group(2) or note_slug
        note_path = vault_path("wiki", "topics", f"{note_slug}.md")
        fields = _frontmatter(note_path)
        body = _read(note_path)
        evidence_notes = []
        capture = False
        for body_line in body.splitlines():
            cleaned = body_line.strip()
            if cleaned.startswith("- **Evidence Notes**"):
                capture = True
                continue
            if capture and cleaned.startswith("- "):
                evidence_notes.append(cleaned[2:])
                if len(evidence_notes) >= 3:
                    break
            elif capture and cleaned.startswith("## "):
                break
        briefs.append(
            {
                "note": f"wiki/topics/{note_slug}.md",
                "title": strip_quotes(fields.get("title", display_title)),
                "zotero_key": strip_quotes(fields.get("zotero_key", "")),
                "summary": _compact_text(fields.get("summary", ""), max_chars=260),
                "evidence_notes": " | ".join(evidence_notes)[:520],
            }
        )
    return briefs[:14]


def _compact_focus_tracks(files: list[dict[str, str]]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    priority = ("track-dashboard", "decision-log", "baseline-checklist", "critic-first", "core-paper")
    for item in files:
        path = str(item.get("path", ""))
        if any(token in path for token in priority):
            selected.append(
                {
                    "path": path,
                    "excerpt": _compact_text(item.get("excerpt", ""), max_chars=700),
                }
            )
        if len(selected) >= 8:
            break
    return selected


def _focus_track_files() -> list[dict[str, str]]:
    root = vault_path("projects", "focus-tracks")
    if not root.exists():
        return []
    files: list[dict[str, str]] = []
    for path in sorted(root.glob("*/*.md")) + sorted(root.glob("*/*/*.md")):
        if path.name == "accepted_claims.jsonl":
            continue
        files.append({"path": rel(path), "excerpt": _body_excerpt(path, max_chars=1200)})
    return files[:40]


def _daily_high_quality_order(path: Path) -> dict[str, int]:
    order: dict[str, int] = {}
    in_section = False
    for line in _read(path).splitlines():
        stripped = line.strip()
        if stripped == "## High Quality Seed Candidates":
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section or not stripped.startswith("- "):
            continue
        title_match = re.match(r"^- (.+?): local_sources=", stripped)
        title = title_match.group(1).strip() if title_match else stripped[2:].split(":", 1)[0].strip()
        if title and title not in order:
            order[title] = len(order)
    return order


def _is_today_generated_seed(item: dict[str, Any], run_date: str, seed_order: dict[str, int]) -> bool:
    title = item.get("title", "")
    generation_rule = item.get("generation_rule", "")
    if item.get("state") != "seed":
        return False
    if generation_rule not in {"mechanism_cluster", "gemini_divergent"}:
        return False
    if item.get("decision_status") != "generated_for_review":
        return False
    if seed_order:
        return title in seed_order
    return item.get("created") == run_date or item.get("updated") == run_date


def _parse_review_actions(markdown: str) -> dict[str, str]:
    actions: dict[str, str] = {}
    current_title = ""
    title_pattern = re.compile(r"^\d+\.\s+(?:`([^`]+)`|(.+))")
    for line in markdown.splitlines():
        stripped = line.strip()
        match = title_pattern.match(stripped)
        if match:
            current_title = (match.group(1) or match.group(2) or "").strip()
            continue
        if current_title and re.match(r"^-?\s*action:", stripped):
            action = re.sub(r"^-?\s*action:\s*", "", stripped).strip().strip("`")
            if action:
                actions[current_title] = action
                current_title = ""
    return actions


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.split(":", 1)[0].strip().lower())


def _review_action_for_title(title: str, actions: dict[str, str]) -> str:
    target = _normalize_title(title)
    for action_title, action in actions.items():
        candidate = _normalize_title(action_title)
        if target == candidate or target.startswith(candidate) or candidate.startswith(target):
            return action
    return ""


def _replace_review_status(text: str, action: str) -> str:
    status = f"codex_reviewed_{action}"
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.strip().startswith("- status:"):
            lines[index] = f"- status: {status}"
            replaced = True
            break
    if not replaced:
        lines.append(f"- status: {status}")
    return "\n".join(lines).rstrip() + "\n"


def _without_existing_codex_section(text: str, run_date: str) -> str:
    marker = f"## Codex Review - {run_date}"
    lines = text.rstrip().splitlines()
    if marker not in lines:
        return text.rstrip()
    start = lines.index(marker)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[:start] + lines[end:]).rstrip()


def _sync_review_logs(run_date: str, packet: dict[str, Any], body: str, report_path: Path, *, dry_run: bool) -> int:
    actions = _parse_review_actions(body)
    if not actions:
        return 0
    updated = 0
    for item in packet.get("today_mechanism_seed_candidates", []):
        action = _review_action_for_title(str(item.get("title", "")), actions)
        if not action:
            continue
        folder = vault_path(str(item.get("path", "")))
        log_path = folder / "review_log.md"
        existing = _read(log_path)
        if not existing:
            existing = f"# Review Log - {item.get('title', folder.name)}\n\n## Review Log\n\n- created_by: unknown\n"
        existing = _replace_review_status(existing, action)
        existing = _without_existing_codex_section(existing, run_date)
        section = [
            "",
            f"## Codex Review - {run_date}",
            "",
            f"- status: codex_reviewed",
            f"- action: {action}",
            f"- report: `{rel(report_path)}`",
            "- boundary: user remains final reviewer; no paper claim accepted.",
        ]
        content = existing.rstrip() + "\n" + "\n".join(section).rstrip() + "\n"
        if not dry_run:
            _quiet_safe_write(log_path, content, dry_run=False)
        updated += 1
    return updated


def _resolve_stale_packet_note(body: str, packet: dict[str, Any]) -> str:
    seed_count = len(packet.get("today_mechanism_seed_candidates", []))
    if seed_count <= 0:
        return body
    lines = []
    for line in body.splitlines():
        if "`today_mechanism_seed_candidates` is empty" in line:
            lines.append(
                "- packet_note: packet-builder inconsistency resolved; "
                f"current packet has {seed_count} `today_mechanism_seed_candidates`."
            )
        elif "Fix the packet builder or review script so `today_mechanism_seed_candidates` is populated" in line:
            lines.append(
                "- Packet builder/review-log sync fixed: current wrapper populates "
                f"{seed_count} `today_mechanism_seed_candidates` and backfills seed `review_log.md`."
            )
        else:
            lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def build_packet(run_date: str) -> dict[str, Any]:
    agenda_daily = vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")
    manual_review = vault_path("projects", "research-agenda", "reviews", f"{run_date}-seed-quality-review.md")
    ideas = _collect_ideas()
    seed_order = _daily_high_quality_order(agenda_daily)
    greenhouse = _read_greenhouse(run_date)
    mandatory_battle = _read_mandatory_model_battle(run_date)
    today_mechanism = [
        item
        for item in ideas
        if _is_today_generated_seed(item, run_date, seed_order)
    ]
    today_mechanism = sorted(today_mechanism, key=lambda item: seed_order.get(item.get("title", ""), 999))
    raw_candidates = [
        _compact_greenhouse_candidate(item)
        for item in greenhouse.get("raw_gemini_candidates", [])
        if isinstance(item, dict)
    ]
    today_mechanism_compact = [_compact_seed_candidate(item) for item in today_mechanism]
    all_seed_titles = [
        {"title": item.get("title", ""), "path": item.get("path", ""), "state": item.get("state", "")}
        for item in ideas
        if item.get("state") == "seed"
    ][:80]
    return {
        "run_date": run_date,
        "packet_mode": "compact_daily_review",
        "review_boundary": {
            "role": "Codex daily second-pass reviewer",
            "allowed_actions": CODEX_ALLOWED_ACTIONS,
            "forbidden_actions": ["auto_promote_to_paper_claim", "move_idea_folders", "write_accepted_claims"],
            "final_reviewer": "user",
        },
        "workflow_contracts": {
            "codex_review": WORKFLOW_CONTRACTS["codex_review"],
            "gemini_greenhouse": WORKFLOW_CONTRACTS["gemini_greenhouse"],
            "idea_quality_source_basis": WORKFLOW_CONTRACTS["idea_quality_source_basis"],
            "idea_taxonomy": WORKFLOW_CONTRACTS["idea_taxonomy"],
            "daily_readable_workflow": WORKFLOW_CONTRACTS["daily_readable_workflow"],
            "provider_matrix": WORKFLOW_CONTRACTS["provider_matrix"],
        },
        "top_tier_rubric": greenhouse.get("quality_rubric_weights", {}),
        "quality_boundary": {
            "seed_promotion_tiers": ["S", "A"],
            "quality_tier_semantics": "quality_tier and potential_tier are potential-only signals, not seed readiness or paper quality acceptance.",
            "seed_readiness_rule": "Only readiness_tier=seed_ready or greenhouse_label=promoted_to_seed means the generator considered a candidate seed-ready; Codex and the user can still downgrade it.",
            "source_filter_policy": "Gemini candidates should be survivors after internal adversarial filtering; rejected_drafts_summary is audit context and not a candidate list.",
            "novelty_boundary": "novelty_pressure is local-only and unverified; no novelty claim is accepted.",
            "novelty_pressure_policy": "local similarity is review evidence only; it must not automatically demote originality or block a wild candidate.",
            "candidate_groups": {
                "evidence_bound": "tighter evidence path; normally needs at least two newly read sources.",
                "wild_engineering": "larger engineering or architecture leap; lighter evidence can be acceptable if pathology, mechanism, baseline, and falsification are sharp.",
            },
            "score_split": "support_score, originality_score, and engineering_value_score are separate; Codex should not collapse them into evidence volume.",
            "portfolio_taxonomy": "Use origin_type, research_claim_type, bottleneck_type, evidence_mode, risk_class, world_model_role, and portfolio_slot to judge portfolio balance. Failure/recovery should not dominate the whole set.",
            "sharpness_execution_split": "Use sharpness_score and evidence_execution_score separately. A high-sharpness low-evidence candidate should be preserved or parked, not rejected solely for weak evidence.",
            "world_model_boundary": "A world-model idea is reviewable only if it states role, predicted state, physical invariant, decision boundary, and hallucination test.",
            "deepseek_role": "Mandatory DeepSeek/OpenCode battle is a scientific adversary and rescue proposer: novelty attack, baseline attack, mechanism attack, evaluation attack, scope attack, and rescue mutation.",
            "codex_execution_role": "Codex should focus on feasibility, dataset/simulation availability, reproducible evaluation, baseline cost, hidden leakage, no-hardware pilot, and minimal repo/experiment plan. Do not reject breakthrough ideas merely for being hard.",
            "mechanism_nonobviousness_boundary": "script score is only a field-depth heuristic; Codex must judge actual non-obviousness from mechanism, interface, strongest baseline, and killer experiment.",
            "anti_combination_boundary": "Codex must explicitly test whether each candidate is more than A+B. A candidate without a convincing anti_combination_test should be rewrite/park even if evidence is strong.",
            "adversarial_generation_boundary": "Codex must inspect naive_combination_version, strongest_baseline_kill_path, and post_kill_mutation. Accept only if the final idea clearly mutated after the strongest baseline killed the naive A+B version.",
            "mandatory_model_battle_boundary": "OpenCode DeepSeek battle is mandatory for daily greenhouse success from 2026-05-14. Codex must inspect mandatory_model_battle and should not treat missing/failed battle as a clean review.",
            "top_tier_boundary": "Top-tier alignment requires a causal mechanism, a real engineering pathology, a ruthless strongest baseline, and a small killer experiment. Do not accept generic stacking ideas.",
            "method_improvement_boundary": "Method-improvement ideas are not automatically incremental. Accept or rewrite them based on whether they change a failure mechanism, interface, constraint, feedback loop, or evaluation signal under a strong baseline.",
            "reviewer_kill_shot_boundary": "Codex must consider the strongest skeptical rejection argument before accepting any candidate.",
            "rescue_mutation_boundary": "If a candidate is not ready, Codex should preserve a concrete mutation path instead of deleting the creative signal.",
            "claim_compression_boundary": "A strong candidate should compress to one falsifiable claim. Vague combination claims should be rewrite or park.",
            "codex_role": "triage raw candidates and preserve rescue signals; do not delete creative ideas.",
        },
        "token_budget_guard": {
            "do_not_open_wiki_topics": True,
            "do_not_open_raw_or_fulltext": True,
            "use_packet_evidence_briefs_first": True,
            "inspect_seed_files_only_if_needed": True,
            "target_report_words": "900-1400",
        },
        "agenda_dashboard_excerpt": _body_excerpt(vault_path("projects", "research-agenda", "agenda-dashboard.md"), max_chars=1100),
        "agenda_delta_excerpt": _body_excerpt(agenda_daily, max_chars=1500),
        "same_day_manual_review_excerpt": _body_excerpt(manual_review, max_chars=1200),
        "local_evidence_briefs": _local_evidence_briefs(run_date),
        "focus_tracks": _compact_focus_tracks(_focus_track_files()),
        "greenhouse_path": greenhouse.get("path", ""),
        "greenhouse_generator_metadata": greenhouse.get("generator_metadata", {}),
        "portfolio_summary": greenhouse.get("portfolio_summary", {}),
        "mandatory_model_battle": mandatory_battle,
        "raw_gemini_candidates": raw_candidates,
        "parked_or_rewrite_candidates": [
            item
            for item in raw_candidates
            if item.get("greenhouse_label") in {"speculative_preserve", "parked_for_weekly_review", "rewrite_needed", "blocked_with_rescue_signal"}
        ],
        "today_mechanism_seed_candidates": today_mechanism_compact,
        "formal_seed_titles": all_seed_titles,
        "counts": {
            "raw_gemini_candidates": len(raw_candidates),
            "today_mechanism_seed_candidates": len(today_mechanism_compact),
            "formal_seed_titles": len(all_seed_titles),
            "candidate_group_evidence_bound": sum(1 for item in raw_candidates if item.get("candidate_group") == "evidence_bound"),
            "candidate_group_wild_engineering": sum(1 for item in raw_candidates if item.get("candidate_group") == "wild_engineering"),
            "origin_types": dict(Counter(str(item.get("origin_type", "unclassified") or "unclassified") for item in raw_candidates)),
            "research_claim_types": dict(Counter(str(item.get("research_claim_type", "unclassified") or "unclassified") for item in raw_candidates)),
            "risk_classes": dict(Counter(str(item.get("risk_class", "unclassified") or "unclassified") for item in raw_candidates)),
            "portfolio_slots": dict(Counter(str(item.get("portfolio_slot", "unclassified") or "unclassified") for item in raw_candidates)),
            "speculative_preserve": sum(1 for item in raw_candidates if item.get("greenhouse_label") == "speculative_preserve"),
        },
    }


def render_prompt(packet_path: str, run_date: str) -> str:
    return f"""# Daily Codex Seed Review - {run_date}

You are Codex running as a scheduled read-only second-pass reviewer for this Obsidian literature vault.

Read the local packet first:

`{packet_path}`

This packet is intentionally compact. Use the packet evidence briefs first. Do not open `wiki/topics/`, `raw/`, PDFs, or fulltext notes. Only inspect a referenced seed folder file if the packet is internally inconsistent or a decision cannot be made from the compact fields. Do not use web search. Do not modify files.

Your task is to produce a high-quality research triage report in English ASCII only. Avoid Chinese characters and non-ASCII punctuation because this scheduled Windows runner can corrupt non-ASCII Codex output. Review `raw_gemini_candidates` first, then compare them with `today_mechanism_seed_candidates`. The generator preserves 5-8 greenhouse candidates but promotes only a few formal seeds. Avoid a result that merely says "accepted/rejected counts". The correct behavior is to accept for user review, rewrite, park, or reject_with_rescue based on mechanism quality. Do not silently discard creative candidates.

Token budget: keep the final report around 900-1400 words. Do not expand all evidence notes. Do not print long quotes from the packet.

Required judgment criteria:

- mechanism clarity: does the idea name a concrete technical interface or causal mechanism?
- physical failure scene: does it start from a concrete robot episode, or only from an abstract algorithmic gap?
- local evidence fit: can the idea be traced to `wiki/topics/` or focus-track evidence?
- similar-work pressure: is the idea already occupied by local done papers?
- experimentability: can a low-cost pilot falsify it before real robot work?
- direction fit: from 2026-05-08 onward, do not prefer RL Token / VLA / Sim-to-Real unless the packet evidence makes them genuinely central; free divergence is allowed.
- creativity preservation: if a candidate is risky but contains a useful engineering pathology or interface, preserve the rescue signal instead of rejecting it outright.
- candidate groups: compare `evidence_bound` and `wild_engineering` fairly. Do not penalize a wild_engineering candidate merely because it has lighter evidence; penalize it only if pathology, mechanism, baseline, or falsification is weak.
- score split: use `support_score`, `originality_score`, and `engineering_value_score` separately. High support with low originality is not a top-tier idea; low support with high engineering value may be a rescue or rewrite candidate.
- portfolio taxonomy: inspect `origin_type`, `research_claim_type`, `bottleneck_type`, `evidence_mode`, `risk_class`, and `portfolio_slot`. Penalize visible failure/recovery mode collapse, but do not require every strong idea to start from a physical failure scene.
- sharpness/execution split: use `sharpness_score`, `evidence_execution_score`, and `ordinaryness_penalty`. If sharpness is high but evidence is light, preserve as speculative or park unless it is incoherent, non-falsifiable, already known, or impossible to test.
- world model role: if `research_claim_type=world_model_simulation`, check `world_model_role`, predicted state, physical invariant, decision boundary, hallucination test, and baseline kill. Vague "predict future then choose safe action" should be rewrite or reject_with_rescue.
- potential/readiness split: `quality_tier` and `potential_tier` mean potential only. They are not seed readiness. Use `readiness_tier`, `promotion_decision`, `greenhouse_label`, and your own review to decide accept/rewrite/park/rescue.
- source filtering: inspect `greenhouse_generator_metadata.rejected_drafts_summary` when present. It is not a candidate list, but it reveals whether Gemini killed weak drafts before output. If many weak drafts were killed and few candidates survived, judge the survivors strictly instead of demanding filler.
- mandatory model battle: inspect `mandatory_model_battle`. From 2026-05-14 onward, OpenCode DeepSeek adversarial battle is required before a clean daily idea stage. If it is missing or failed, report the daily idea stage as partial and focus your review on rescue/mutation rather than acceptance.
- DeepSeek role: treat DeepSeek as scientific adversary and rescue proposer. Look for novelty attack, baseline attack, mechanism attack, evaluation attack, scope attack, and rescue mutation. Do not read the battle as a simple winner-take-all vote.
- anti-combination test: explicitly ask whether the idea is just A+B. If yes, action must be `rewrite`, `park`, or `reject_with_rescue`.
- adversarial generation trace: inspect `naive_combination_version`, `strongest_baseline_kill_path`, and `post_kill_mutation`. The accepted mechanism must be the post-kill mutation. If the mutation only renames or slightly wraps the naive A+B version, action must be `rewrite` or `park`.
- interface innovation: do not accept candidates that only add an input, swap a module, or place a residual around RL tokens. The candidate must change a boundary, information flow, controlled variable, or feedback loop.
- optimization space: inspect optimization_space, loss_placement, decoder_boundary, and manifold_safety. For RL-token ideas, reject or rewrite if the candidate never explains why token/latent/action/critic space is the right place for the objective.
- top-tier rationale: judge whether the idea has a plausible RSS/CoRL/ICRA/RA-L contribution shape, not whether it merely sounds novel.
- engineering loop: prefer ideas that change a real robot loop: sensing -> representation -> control -> feedback -> learning/evaluation.
- method improvement: do not dismiss a candidate merely because it improves an existing method. It can be top-tier if it identifies the original method's failure mechanism, changes a key interface/constraint/feedback loop, and survives the strongest baseline.
- reviewer kill shot: name the strongest rejection argument before accepting a candidate.
- reviewer pre-mortem: before accepting S/A, ask whether the candidate's own pre-mortem already kills the core claim; if yes, action should be rewrite or park.
- online/offline mode: decide whether online_control is actually necessary. Many strong robotics papers can begin as offline_replay, benchmark, dataset, or analysis_tool contributions.
- no-hardware pilot: check whether the proposed minimum_no_hardware_pilot can separate the mechanism from engineering polish before any real robot run.
- baseline kill table: use the candidate's baseline_kill_table to judge whether the strongest baseline can really be beaten or whether the idea is only a wrapper.
- mechanism falsification: use falsification_discriminates_mechanism to judge whether the test separates a real mechanism from an engineering patch.
- lab fit: check lab_fit and hardware_assumptions. A candidate that needs low-cost robot pathology, fleet scale, unavailable sensors, or a resource profile mismatched to Franka/FlexiTac/wrist-camera/DLO strengths should be rewrite or park.
- final-idea structure: use HapToken-v3 style as a quality reference. Strong candidates need negative_claim_boundary, version_evolution_story or failed naive alternative, core_insight, pipeline_steps, defense_patches, baseline_matrix, metric_suite, risk_assumptions, competition_map, and two_week_sprint. Do not accept a candidate that only has a clever one-line mechanism.
- not-a-paper condition: if what_would_make_this_not_a_paper is likely true, do not accept; preserve rescue signal instead.
- rescue mutation: if the idea is not ready, preserve a concrete mutation path rather than only rejecting it.
- claim compression: prefer candidates that can be written as one falsifiable paper claim, not a vague combination slogan.
- Codex role: focus on execution reality, not aesthetic creativity ranking. Judge no-hardware pilot, data/simulation availability, reproducible metric, hidden leakage, baseline cost, minimal repo plan, and real-robot pilot complexity. A breakthrough idea cannot be rejected solely because it is hard.

Top-Tier Bar:

- non-obviousness: identify whether the core contribution is more than "combine A with B"; if not, action must be rewrite or park.
- kill-before-accept: restate the naive A+B version, the strongest baseline kill path, and the post-kill mutation before accepting any candidate.
- strongest baseline: name the baseline most likely to kill the idea and whether the candidate names a credible killer experiment.
- baseline failure mode: explain whether the candidate gives a credible reason the strongest baseline fails. If not, do not accept it.
- engineering pathology: prefer ideas grounded in real robot failures such as occlusion, latency, contact instability, calibration drift, poor depth, viewpoint failure, reset cost, or sim-to-real mismatch.
- RL-token bar: a good RL-token idea must explain what information survives compression, where the correction/memory/loss enters, whether it crosses the decoder boundary, and how off-manifold token deltas are detected.
- pilot readiness: accept only if baseline_matrix has enough controls and two_week_sprint names a day-1/day-3 kill test.
- contribution shape: classify as architecture, algorithm, control_interface, mechanism, system, evaluation_protocol, benchmark, failure_model, or dataset.
- method-improvement bar: if contribution_shape is `method_improvement`, decide whether it is `mechanism_improving_method` or only `incremental_patch`.
- novelty pressure: use only packet novelty_pressure / local similar-work evidence; do not claim confirmed novelty, and do not automatically demote a candidate solely because local pressure is high.
- potential tier: S/A means high potential, not seed readiness. A candidate still needs readiness_tier, promotion_decision, baseline survival, and Codex judgment before `accept_for_user_review`.
- portfolio balance: identify whether the greenhouse collapsed into one stress regime. A portfolio with too many safety/recovery patches should be called out even if individual candidates are plausible.
- breakthrough preservation: if `risk_class=breakthrough`, do not reject solely for light evidence. Reject only for incoherence, non-falsifiability, obvious prior art, impossible experiment, or safety/ethics infeasibility.
- execution bar: for every accept_for_user_review, name the no-hardware pilot, strongest feasible baseline, expected repo artifact, and smallest real-robot follow-up.

Required output format, Markdown only, no frontmatter:

# Daily Codex Seed Review - {run_date}

## Executive Verdict

- status: `done`
- reviewed_scope: ...
- top_decision: ...
- boundary: no paper claim is accepted; user remains final reviewer.

## Shortlist For User

Give 1-3 items maximum. Each item must include `action` as one of `accept_for_user_review`, `rewrite`, `park`, or `reject_with_rescue`; also include `potential_tier`, `readiness_tier`, `why`, `local_evidence`, and `next_gate`.

## Rewrite Or Merge

List ideas that should be rewritten or merged instead of rejected. Include the target focus track or new hypothesis name.

## Park

List useful but non-current ideas.

## Creativity Preservation

List raw Gemini candidates that should not be promoted today but should remain recoverable. Include `candidate`, `rescue_signal`, and `why_not_now`.

## Reject With Rescue

List weak/generated ideas whose evidence cluster contains reusable signal. Do not restore generic cross-gap folders; extract the useful signal. Use `reject_no_trace` only when there is no mechanism, no evidence fit, and no rescue signal.

## Reject No Rescue

Only use this when there is no mechanism, no evidence fit, and no useful cluster.

## Watchlist

Mention similar-work risks, missing experiments, and claims that must remain `unverified`.

## Next 24 Hours

Give concrete next actions for Claudian/Codex pipeline. Prioritize quality over quantity.
"""


def prepare(run_date: str, *, dry_run: bool, catch_up: bool = False, catch_up_days: int = 7) -> dict[str, str]:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    requested_run_date = run_date
    run_date, selection_reason = resolve_review_run_date(run_date, catch_up=catch_up, days_back=catch_up_days)
    readiness = check_daily_readiness(run_date)
    if readiness["ready"] != "true":
        return {
            "status": "skipped_waiting_for_daily_pipeline",
            "requested_run_date": requested_run_date,
            "selected_run_date": run_date,
            "selection_reason": selection_reason,
            **readiness,
            "packet_path": "",
            "prompt_path": "",
            "raw_output_path": "",
            "idea_count": "0",
            "today_mechanism_seed_count": "0",
            "raw_gemini_candidate_count": "0",
        }
    packet_path = REVIEWS_DIR / f"{run_date}-codex-seed-review-packet.json"
    prompt_path = REVIEWS_DIR / f"{run_date}-codex-seed-review-prompt.md"
    raw_output_path = REVIEWS_DIR / f"{run_date}-codex-seed-review.raw.md"
    packet = build_packet(run_date)
    if not dry_run:
        _quiet_safe_write(packet_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=False)
        _quiet_safe_write(prompt_path, render_prompt(rel(packet_path), run_date), dry_run=False)
    return {
        "status": "prepared",
        "requested_run_date": requested_run_date,
        "selected_run_date": run_date,
        "selection_reason": selection_reason,
        "packet_path": rel(packet_path),
        "prompt_path": rel(prompt_path),
        "raw_output_path": rel(raw_output_path),
        "idea_count": str(len(packet.get("formal_seed_titles", packet.get("ideas", [])))),
        "today_mechanism_seed_count": str(len(packet["today_mechanism_seed_candidates"])),
        "raw_gemini_candidate_count": str(len(packet.get("raw_gemini_candidates", []))),
    }


def _fallback_report(run_date: str, packet: dict[str, Any], codex_exit_code: int) -> str:
    ideas = packet.get("ideas", [])
    seeds = packet.get("today_mechanism_seed_candidates") or [
        item for item in ideas if item.get("state") == "seed"
    ]
    rejected = [item for item in ideas if item.get("state") == "rejected"]
    top = sorted(seeds, key=lambda item: (-int(item.get("score", 0)), item.get("title", "")))[:5]
    raw_candidates = packet.get("raw_gemini_candidates", [])
    reviewed_scope = (
        f"today_mechanism_seed={len(seeds)} raw_gemini_candidates={len(raw_candidates)} "
        f"rejected_reference={len(rejected)}"
    )
    if packet.get("packet_mode") == "compact_daily_review":
        reviewed_scope = (
            f"today_mechanism_seed={len(seeds)} raw_gemini_candidates={len(raw_candidates)} "
            "packet_mode=compact_daily_review"
        )
    lines = [
        f"# Daily Codex Seed Review - {run_date}",
        "",
        "## Executive Verdict",
        "",
        "- status: `partial`",
        f"- codex_exit_code: `{codex_exit_code}`",
        "- boundary: Codex model review did not complete; this fallback is deterministic and must not be treated as manual-quality judgment.",
        f"- reviewed_scope: {reviewed_scope}",
        "",
        "## Shortlist For User",
        "",
    ]
    if not top:
        lines.append("- no seed ideas available for fallback shortlist.")
    for item in top:
        lines.append(
            f"- `{item.get('title')}` action=`needs_codex_review` "
            f"score={item.get('score')} evidence={item.get('evidence_count')} path=`{item.get('path')}`"
        )
    lines.extend(
        [
            "",
            "## Creativity Preservation",
            "",
            "- fallback mode did not complete model review; raw Gemini candidates remain recoverable.",
        "",
            "## Raw Candidate Rescue Queue",
            "",
        ]
    )
    if not raw_candidates:
        lines.append("- none")
    for item in raw_candidates[:8]:
        lines.append(
            f"- `{item.get('title')}` potential={item.get('potential_tier', item.get('quality_tier', '-'))} "
            f"readiness={item.get('readiness_tier', _readiness_from_label(str(item.get('greenhouse_label', '-'))))} "
            f"quality={item.get('research_quality_score', '-')} "
            f"label={item.get('greenhouse_label', '-')} "
            f"rescue_signal={item.get('rescue_signal') or item.get('engineering_pathology') or item.get('mechanism') or '-'}"
        )
    lines.extend(
        [
            "",
            "## Next 24 Hours",
            "",
            "- rerun `run_daily_codex_seed_review_task.ps1` after checking Codex CLI/auth.",
            "- do not promote or reject ideas from this fallback alone.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def wrap(run_date: str, codex_output: Path, codex_exit_code: int, *, dry_run: bool) -> dict[str, str]:
    packet_path = REVIEWS_DIR / f"{run_date}-codex-seed-review-packet.json"
    packet = json.loads(_read(packet_path)) if packet_path.exists() else build_packet(run_date)
    raw = _read(codex_output)
    completed = _codex_review_output_complete(raw)
    status = "done" if completed else "partial"
    diagnostic_text = _codex_exit_diagnostic_text(run_date, raw)
    nonblocking_exit_reason = _codex_nonblocking_exit_reason(diagnostic_text, codex_exit_code) if completed else ""
    body = raw.strip() + "\n" if completed else _fallback_report(run_date, packet, codex_exit_code)
    body = _resolve_stale_packet_note(body, packet) if completed else body
    report_path = REVIEWS_DIR / f"{run_date}-codex-seed-review.md"
    frontmatter = render_frontmatter(
        f"Daily Codex Seed Review - {run_date}",
        REVIEW_TAGS,
        f"Daily Codex second-pass seed review status: {status}.",
        status=status,
    )
    header = [
        f"- codex_review_status: `{status}`",
        f"- codex_raw_exit_code: `{codex_exit_code}`",
        f"- codex_output_complete: `{str(completed).lower()}`",
        f"- codex_exit_nonblocking: `{str(bool(nonblocking_exit_reason)).lower()}`",
        f"- codex_nonblocking_exit_reason: `{nonblocking_exit_reason or '-'}`",
        f"- packet: `{rel(packet_path)}`",
        f"- raw_output: `{rel(codex_output) if codex_output.exists() else str(codex_output)}`",
        "- boundary: review only; no idea folders moved and no paper claims accepted.",
        "",
    ]
    content = frontmatter + "\n".join(header) + body
    if not dry_run:
        _quiet_safe_write(report_path, content, dry_run=False)
        pending_path = REVIEWS_DIR / f"{run_date}-codex-review-pending.json"
        if completed and pending_path.exists():
            pending_path.unlink()
    synced_logs = _sync_review_logs(run_date, packet, body, report_path, dry_run=dry_run) if completed else 0
    return {
        "status": status,
        "report_path": rel(report_path),
        "codex_raw_exit_code": str(codex_exit_code),
        "codex_exit_nonblocking": str(bool(nonblocking_exit_reason)).lower(),
        "codex_nonblocking_exit_reason": nonblocking_exit_reason,
        "synced_review_logs": str(synced_logs),
    }


def _iter_greenhouse_payloads(end_date: str, days: int) -> list[dict[str, Any]]:
    end = date.fromisoformat(end_date)
    payloads: list[dict[str, Any]] = []
    for offset in range(days):
        run_date = (end - timedelta(days=offset)).isoformat()
        payload = _read_greenhouse(run_date)
        if payload.get("exists"):
            payload["run_date"] = run_date
            payloads.append(payload)
    return sorted(payloads, key=lambda item: item["run_date"])


def render_weekly_greenhouse_review(end_date: str, days: int) -> str:
    payloads = _iter_greenhouse_payloads(end_date, days)
    candidates: list[dict[str, Any]] = []
    for payload in payloads:
        for item in payload.get("raw_gemini_candidates", []):
            merged = dict(item)
            merged["run_date"] = payload.get("run_date", "")
            candidates.append(merged)
    counts = Counter(str(item.get("greenhouse_label", "unlabeled")) for item in candidates)
    tier_counts = Counter(str(item.get("quality_tier", "unrated")) for item in candidates)
    potential_counts = Counter(str(item.get("potential_tier", item.get("quality_tier", "unrated"))) for item in candidates)
    readiness_counts = Counter(str(item.get("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled"))))) for item in candidates)
    shape_counts = Counter(str(item.get("contribution_shape", "unclassified") or "unclassified") for item in candidates)
    lines = [
        f"# Weekly Gemini Greenhouse Review - {end_date}",
        "",
        f"- window_days: {days}",
        f"- source_files: {len(payloads)}",
        f"- raw_candidates: {len(candidates)}",
        f"- promoted_to_seed: {counts.get('promoted_to_seed', 0)}",
        f"- parked_for_weekly_review: {counts.get('parked_for_weekly_review', 0)}",
        f"- rewrite_needed: {counts.get('rewrite_needed', 0)}",
        f"- blocked_with_rescue_signal: {counts.get('blocked_with_rescue_signal', 0)}",
        f"- quality_tiers: {dict(tier_counts)}",
        "- quality_tier_semantics: potential_only_not_seed_readiness",
        f"- potential_tiers: {dict(potential_counts)}",
        f"- readiness_tiers: {dict(readiness_counts)}",
        f"- contribution_shapes: {dict(shape_counts)}",
        "",
        "## Mechanism-Sharp Watchlist",
        "",
    ]
    sharp = sorted(
        candidates,
        key=lambda item: (
            str(item.get("greenhouse_label")) != "parked_for_weekly_review",
            -int(item.get("research_quality_score") or 0),
            str(item.get("title", "")),
        ),
    )
    sharp = [
        item for item in sharp
        if item.get("greenhouse_label") != "promoted_to_seed"
        and int(item.get("research_quality_score") or 0) >= 45
    ]
    if not sharp:
        lines.append("- none")
    for item in sharp[:12]:
        lines.extend(
            [
                f"- {item.get('run_date')} `{item.get('title', 'Untitled')}` "
                f"potential=`{item.get('potential_tier', item.get('quality_tier', '-'))}` "
                f"readiness=`{item.get('readiness_tier', _readiness_from_label(str(item.get('greenhouse_label', '-'))))}` "
                f"quality={item.get('research_quality_score', '-')} "
                f"shape=`{item.get('contribution_shape', '-')}` label=`{item.get('greenhouse_label', '-')}`",
                f"  rescue_signal: {item.get('rescue_signal') or item.get('non_obvious_claim') or item.get('engineering_pathology') or '-'}",
            ]
        )
    lines.extend(
        [
            "",
            "## Parked Or Rewrite Candidates",
            "",
        ]
    )
    selected = [
        item
        for item in candidates
        if item.get("greenhouse_label") in {"parked_for_weekly_review", "rewrite_needed", "blocked_with_rescue_signal"}
    ]
    if not selected:
        lines.append("- none")
    for item in selected[:30]:
        lines.extend(
            [
                f"- {item.get('run_date')} `{item.get('title', 'Untitled')}` "
                f"label=`{item.get('greenhouse_label', 'unlabeled')}` "
                f"potential=`{item.get('potential_tier', item.get('quality_tier', '-'))}` "
                f"readiness=`{item.get('readiness_tier', _readiness_from_label(str(item.get('greenhouse_label', '-'))))}` "
                f"quality={item.get('research_quality_score', '-')} "
                f"shape=`{item.get('contribution_shape', '-')}`",
                f"  rescue_signal: {item.get('rescue_signal') or item.get('engineering_pathology') or item.get('mechanism') or '-'}",
            ]
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This is a review queue only; no seed is promoted by this report.",
            "- Use it to choose candidates for manual Gemini defend/mutate or user review.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def greenhouse_weekly(end_date: str, days: int, *, dry_run: bool) -> dict[str, str]:
    report_path = agenda_path("divergent", f"{end_date}-weekly-greenhouse-review.md")
    body = render_weekly_greenhouse_review(end_date, days)
    if not dry_run:
        _quiet_safe_write(report_path, body, dry_run=False)
    payloads = _iter_greenhouse_payloads(end_date, days)
    candidate_count = sum(len(payload.get("raw_gemini_candidates", [])) for payload in payloads)
    return {
        "status": "done",
        "report_path": rel(report_path),
        "source_files": str(len(payloads)),
        "raw_candidates": str(candidate_count),
    }


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _candidate_text(item: dict[str, Any]) -> str:
    fields = [
        "title",
        "problem",
        "engineering_pathology",
        "mechanism",
        "interface",
        "hypothesis",
        "speculative_jump",
        "idea_archetype",
        "contribution_shape",
        "non_obvious_claim",
        "naive_combination_version",
        "strongest_baseline_kill_path",
        "post_kill_mutation",
        "anti_combination_test",
        "top_tier_rationale",
        "engineering_loop",
        "method_improvement_claim",
        "original_method_failure",
        "replacement_or_coupled_technique",
        "why_improvement_not_patch",
        "strongest_baseline",
        "baseline_failure_mode",
        "killer_experiment",
        "reviewer_kill_shot",
        "rescue_mutation",
        "claim_compression",
        "novelty_risk",
        "pilot",
        "baselines",
        "metrics",
        "falsification",
        "rescue_signal",
    ]
    return " ".join(str(item.get(field, "")) for field in fields).lower()


def _marker_score(text: str, markers: list[str], max_score: int = 5) -> int:
    lowered = text.lower()
    hits = sum(1 for marker in markers if marker in lowered)
    if hits <= 0:
        return 0
    if hits >= 4:
        return max_score
    return min(max_score, hits + 1)


def _local_novelty_pressure_signal(item: dict[str, Any]) -> int:
    pressure = item.get("novelty_pressure", {})
    if not isinstance(pressure, dict):
        return 3
    value = pressure.get("pressure", "not_checked")
    if value in {"none", "low"}:
        return 4
    if value in {"medium", "high"}:
        return 3
    return 3


def _field_depth_score(item: dict[str, Any], checks: list[tuple[str, int, int]], max_score: int = 5) -> int:
    score = 0
    for field, min_chars, points in checks:
        if len(str(item.get(field, "")).strip()) >= min_chars:
            score += points
    return min(max_score, score)


def _weekly_keywords(text: str, *, limit: int = 14) -> list[str]:
    counts: Counter[str] = Counter()
    for token in re.findall(r"[a-z][a-z0-9-]{3,}", text.lower()):
        if token in WEEKLY_STOPWORDS:
            continue
        counts[token] += 1
    return [token for token, _ in counts.most_common(limit)]


def _similar_existing_seed_hits(item: dict[str, Any], ideas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    text = _candidate_text(item)
    keywords = _weekly_keywords(text, limit=16)
    if not keywords:
        return []
    title = str(item.get("title", "")).strip().lower()
    hits: list[dict[str, Any]] = []
    for idea in ideas:
        if idea.get("state") != "seed":
            continue
        idea_title = str(idea.get("title", ""))
        if idea_title.strip().lower() == title:
            continue
        idea_text = f"{idea_title} {idea.get('idea_excerpt', '')} {idea.get('evidence_excerpt', '')}".lower()
        overlap = [keyword for keyword in keywords if keyword in idea_text]
        if len(overlap) < 3:
            continue
        hits.append(
            {
                "title": idea_title,
                "path": idea.get("path", ""),
                "overlap_keywords": overlap[:8],
                "overlap_score": len(overlap),
            }
        )
    return sorted(hits, key=lambda hit: -_as_int(hit.get("overlap_score")))[:5]


def _venue_fit(item: dict[str, Any]) -> str:
    text = _candidate_text(item)
    if any(token in text for token in ["dlo", "deformable", "tactile", "bimanual", "grasp", "contact"]):
        return "ICRA/IROS/RA-L robotics manipulation fit"
    if any(token in text for token in ["vla", "foundation", "language", "online rl", "rl-token", "critic", "architecture"]):
        return "CoRL/RSS mechanism or learning-architecture fit"
    if any(token in text for token in ["workflow", "inspection", "control interface", "servo", "system", "latency"]):
        return "CASE/RA-L systems and automation fit"
    return "venue_fit_unclear_needs_rewrite"


def _weekly_rubric_scores(item: dict[str, Any]) -> dict[str, int]:
    text = _candidate_text(item)
    non_obvious = max(
        _marker_score(text, NON_OBVIOUS_MARKERS),
        _field_depth_score(
            item,
            [
                ("mechanism", 70, 1),
                ("interface", 35, 1),
                ("non_obvious_claim", 90, 2),
                ("naive_combination_version", 60, 1),
                ("strongest_baseline_kill_path", 80, 2),
                ("post_kill_mutation", 80, 2),
                ("anti_combination_test", 80, 1),
                ("engineering_loop", 60, 1),
                ("method_improvement_claim", 60, 1),
                ("why_improvement_not_patch", 70, 1),
                ("strongest_baseline", 35, 1),
                ("killer_experiment", 45, 1),
                ("reviewer_kill_shot", 60, 1),
                ("claim_compression", 50, 1),
            ],
        ),
    )
    pathology = _marker_score(text, ENGINEERING_PATHOLOGY_MARKERS)
    baseline = _marker_score(text, BASELINE_SURVIVAL_MARKERS)
    experiment = _marker_score(text, KILLER_EXPERIMENT_MARKERS)
    novelty_signal = _local_novelty_pressure_signal(item)
    rescue = 0
    if str(item.get("rescue_signal", "")).strip():
        rescue += 3
    if str(item.get("candidate_group", "")) == "wild_engineering":
        rescue += 1
    if str(item.get("contribution_shape", "")).strip().lower().replace("-", "_").replace(" ", "_") == "method_improvement":
        if str(item.get("original_method_failure", "")).strip() and str(item.get("why_improvement_not_patch", "")).strip():
            rescue += 1
    if pathology >= 3:
        rescue += 1
    if non_obvious >= 3:
        rescue += 1
    rescue = min(5, rescue)
    breakthrough = min(5, round((non_obvious + pathology + baseline + experiment + novelty_signal) / 5))
    if _as_int(item.get("sharpness_score")) >= 16:
        breakthrough = max(breakthrough, 4)
    elif _as_int(item.get("sharpness_score")) >= 12:
        breakthrough = max(breakthrough, 3)
    if any(marker in text for marker in GENERIC_COMBINATION_MARKERS) and non_obvious < 3:
        breakthrough = max(0, breakthrough - 1)
    return {
        "breakthrough_potential": breakthrough,
        "engineering_pathology_strength": pathology,
        "non_obvious_mechanism": non_obvious,
        "baseline_survivability": baseline,
        "killer_experiment_clarity": experiment,
        "venue_fit": 1 if _venue_fit(item).startswith("venue_fit_unclear") else 4,
        "rescue_value": rescue,
    }


def _structure_completeness(item: dict[str, Any]) -> tuple[int, list[str]]:
    missing = [field for field in FINAL_IDEA_STRUCTURE_FIELDS if not str(item.get(field, "")).strip()]
    return len(FINAL_IDEA_STRUCTURE_FIELDS) - len(missing), missing


def _has_rerun_accept_bar(item: dict[str, Any], scores: dict[str, int]) -> bool:
    completeness, missing = _structure_completeness(item)
    baseline_matrix = str(item.get("baseline_matrix", ""))
    risk_assumptions = str(item.get("risk_assumptions", ""))
    sprint = str(item.get("two_week_sprint", ""))
    field_depth = (
        len(str(item.get("physical_failure_scene", "")).strip()) >= 90
        and len(str(item.get("interface_innovation", "")).strip()) >= 70
        and len(str(item.get("optimization_space", "")).strip()) >= 60
        and len(str(item.get("falsification_discriminates_mechanism", "")).strip()) >= 80
        and len(str(item.get("lab_fit", "")).strip()) >= 60
    )
    enough_baselines = baseline_matrix.count(";") >= 3 or baseline_matrix.count("|") >= 4 or baseline_matrix.count("\n") >= 4
    enough_risks = risk_assumptions.count(";") >= 2 or risk_assumptions.count("|") >= 3 or risk_assumptions.count("\n") >= 3
    early_kill = any(token in sprint.lower() for token in ["day 1", "day1", "day 3", "day3", "kill", "生死"])
    return (
        completeness == len(FINAL_IDEA_STRUCTURE_FIELDS)
        and not missing
        and field_depth
        and enough_baselines
        and enough_risks
        and early_kill
        and scores["breakthrough_potential"] >= 4
        and scores["non_obvious_mechanism"] >= 4
        and scores["baseline_survivability"] >= 4
        and scores["killer_experiment_clarity"] >= 4
        and scores["engineering_pathology_strength"] >= 3
    )


def _weekly_action(item: dict[str, Any], scores: dict[str, int]) -> str:
    tier = str(item.get("potential_tier", item.get("quality_tier", "")) or "")
    label = str(item.get("greenhouse_label", "") or "")
    if str(item.get("risk_class", "")) == "breakthrough" and scores["non_obvious_mechanism"] >= 3:
        if scores["killer_experiment_clarity"] >= 3 or str(item.get("minimum_no_hardware_pilot", "")).strip():
            return "park_for_weekly_followup"
    decisive = (
        scores["breakthrough_potential"] >= 3
        and scores["baseline_survivability"] >= 3
        and scores["killer_experiment_clarity"] >= 3
        and scores["engineering_pathology_strength"] >= 3
    )
    if (
        decisive
        and scores["non_obvious_mechanism"] >= 3
        and (tier in {"S", "A", "legacy_unrated", ""} or label == "promoted_to_seed")
    ):
        return "push_to_user_review"
    if scores["non_obvious_mechanism"] < 3 or scores["baseline_survivability"] < 3 or scores["killer_experiment_clarity"] < 3:
        if scores["rescue_value"] >= 3 or label == "promoted_to_seed":
            return "rewrite_for_mechanism"
        return "reject_with_rescue"
    if tier == "B":
        return "park_for_weekly_followup"
    if scores["rescue_value"] >= 3 or decisive:
        return "park_for_weekly_followup"
    return "reject_with_rescue"


def _adversarial_notes(item: dict[str, Any], scores: dict[str, int]) -> list[str]:
    text = _candidate_text(item)
    notes: list[str] = []
    if any(marker in text for marker in GENERIC_COMBINATION_MARKERS) and scores["non_obvious_mechanism"] < 3:
        notes.append("generic_combination_pressure")
    if not str(item.get("naive_combination_version", "")).strip():
        notes.append("naive_combination_version_missing")
    if not str(item.get("strongest_baseline_kill_path", "")).strip():
        notes.append("strongest_baseline_kill_path_missing")
    if not str(item.get("post_kill_mutation", "")).strip():
        notes.append("post_kill_mutation_missing")
    if scores["engineering_pathology_strength"] < 3:
        notes.append("engineering_pathology_weak_or_implicit")
    if scores["baseline_survivability"] < 3:
        notes.append("strongest_baseline_not_yet_decisive")
    if scores["killer_experiment_clarity"] < 3:
        notes.append("killer_experiment_needs_sharpening")
    pressure = item.get("novelty_pressure", {})
    if isinstance(pressure, dict) and pressure.get("pressure") in {"medium", "high"}:
        notes.append(f"local_novelty_pressure_{pressure.get('pressure')}")
    if item.get("greenhouse_label") == "promoted_to_seed":
        notes.append("daily_seed_needs_weekly_pressure_test")
    return notes or ["no_immediate_blocker_from_local_rubric"]


def _weekly_candidate_review(item: dict[str, Any], ideas: list[dict[str, Any]]) -> dict[str, Any]:
    scores = _weekly_rubric_scores(item)
    action = _weekly_action(item, scores)
    local_novelty_hits = item.get("novelty_hits", [])
    if not isinstance(local_novelty_hits, list):
        local_novelty_hits = []
    return {
        "run_date": item.get("run_date", ""),
        "title": item.get("title", "Untitled"),
        "greenhouse_label": item.get("greenhouse_label", "unlabeled"),
        "candidate_group": item.get("candidate_group", "unclassified"),
        "quality_tier": item.get("quality_tier", "unrated"),
        "quality_tier_semantics": item.get("quality_tier_semantics", "potential_only_not_seed_readiness"),
        "potential_tier": item.get("potential_tier", item.get("quality_tier", "unrated")),
        "potential_score": item.get("potential_score", item.get("research_quality_score")),
        "readiness_tier": item.get("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled")))),
        "promotion_decision": item.get("promotion_decision", "not_ready"),
        "research_quality_score": item.get("research_quality_score"),
        "support_score": item.get("support_score"),
        "originality_score": item.get("originality_score"),
        "engineering_value_score": item.get("engineering_value_score"),
        "sharpness_score": item.get("sharpness_score"),
        "evidence_execution_score": item.get("evidence_execution_score"),
        "ordinaryness_penalty": item.get("ordinaryness_penalty"),
        "origin_type": item.get("origin_type", ""),
        "research_claim_type": item.get("research_claim_type", ""),
        "bottleneck_type": item.get("bottleneck_type", ""),
        "evidence_mode": item.get("evidence_mode", ""),
        "risk_class": item.get("risk_class", ""),
        "world_model_role": item.get("world_model_role", ""),
        "portfolio_slot": item.get("portfolio_slot", ""),
        "idea_archetype": item.get("idea_archetype", ""),
        "contribution_shape": item.get("contribution_shape", ""),
        "weekly_action": action,
        "weekly_rubric_scores": scores,
        "weekly_score": sum(scores.values()),
        "venue_fit": _venue_fit(item),
        "adversarial_notes": _adversarial_notes(item, scores),
        "engineering_pathology": item.get("engineering_pathology", ""),
        "non_obvious_claim": item.get("non_obvious_claim", ""),
        "naive_combination_version": item.get("naive_combination_version", ""),
        "strongest_baseline_kill_path": item.get("strongest_baseline_kill_path", ""),
        "post_kill_mutation": item.get("post_kill_mutation", ""),
        "anti_combination_test": item.get("anti_combination_test", ""),
        "top_tier_rationale": item.get("top_tier_rationale", ""),
        "engineering_loop": item.get("engineering_loop", ""),
        "method_improvement_claim": item.get("method_improvement_claim", ""),
        "original_method_failure": item.get("original_method_failure", ""),
        "replacement_or_coupled_technique": item.get("replacement_or_coupled_technique", ""),
        "why_improvement_not_patch": item.get("why_improvement_not_patch", ""),
        "strongest_baseline": item.get("strongest_baseline", "") or item.get("baselines", ""),
        "baseline_failure_mode": item.get("baseline_failure_mode", ""),
        "killer_experiment": item.get("killer_experiment", "") or item.get("pilot", "") or item.get("falsification", ""),
        "reviewer_kill_shot": item.get("reviewer_kill_shot", ""),
        "rescue_mutation": item.get("rescue_mutation", ""),
        "claim_compression": item.get("claim_compression", ""),
        "heilmeier": _heilmeier_check(item),
        "nabc": _nabc_pitch(item),
        "lab_affordance_fit": _lab_affordance_fit(item),
        "readiness_level": _readiness_level(item),
        "artifact_or_reproducibility_plan": _artifact_plan(item),
        "novelty_pressure": item.get("novelty_pressure", {}),
        "novelty_hits": local_novelty_hits[:5],
        "similar_existing_seed_hits": _similar_existing_seed_hits(item, ideas),
        "rescue_signal": item.get("rescue_signal", "") or item.get("engineering_pathology", "") or item.get("mechanism", ""),
    }


def _readiness_level(item: dict[str, Any]) -> str:
    text = _candidate_text(item)
    if any(token in text for token in ["real robot", "hardware", "bimanual", "wrist", "tactile", "force controller"]):
        return "readiness_real_robot_pilot_possible"
    if any(token in text for token in ["benchmark", "dataset", "metric", "evaluation", "protocol"]):
        return "readiness_offline_or_benchmark_first"
    if any(token in text for token in ["theory", "latent", "world model", "representation"]):
        return "readiness_concept_or_sim_first"
    return "readiness_unclear_needs_pilot_definition"


def _lab_affordance_fit(item: dict[str, Any]) -> str:
    text = _candidate_text(item)
    hits = []
    for token in ["bimanual", "dlo", "tactile", "wrist", "camera", "occlusion", "grasp", "force", "contact"]:
        if token in text:
            hits.append(token)
    if len(hits) >= 3:
        return "high:" + ",".join(hits[:6])
    if hits:
        return "medium:" + ",".join(hits[:6])
    return "low_or_unknown"


def _heilmeier_check(item: dict[str, Any]) -> dict[str, str]:
    return {
        "what_are_you_trying_to_do": item.get("claim_compression", "") or item.get("problem", "") or item.get("title", ""),
        "how_is_it_done_today": item.get("strongest_baseline", "") or "needs strongest baseline",
        "what_is_new": item.get("non_obvious_claim", "") or item.get("anti_combination_test", "") or "needs non-obvious mechanism",
        "who_cares": item.get("engineering_pathology", "") or "needs engineering pathology",
        "risk": item.get("reviewer_kill_shot", "") or item.get("novelty_risk", "") or "needs reviewer kill shot",
        "success_measure": item.get("killer_experiment", "") or item.get("metrics", "") or "needs killer experiment",
    }


def _nabc_pitch(item: dict[str, Any]) -> dict[str, str]:
    return {
        "need": item.get("engineering_pathology", "") or item.get("problem", ""),
        "approach": item.get("mechanism", "") or item.get("interface", ""),
        "benefit": item.get("claim_compression", "") or item.get("hypothesis", ""),
        "competition": item.get("strongest_baseline", "") or "needs strongest baseline",
    }


def _artifact_plan(item: dict[str, Any]) -> str:
    shape = str(item.get("contribution_shape", "")).strip().lower()
    if shape in {"benchmark", "evaluation_protocol", "failure_model"}:
        return "benchmark_protocol_plus_metrics_and_baseline_scripts"
    if shape in {"dataset"}:
        return "dataset_card_labeling_protocol_and_loader"
    if "tactile" in _candidate_text(item) or "force" in _candidate_text(item):
        return "small_robot_or_sensor_pilot_with_logged_traces"
    return "minimal_reproducible_pilot_script_plus_ablation_table"


def _entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    entropy = 0.0
    for count in counter.values():
        if count <= 0:
            continue
        probability = count / total
        entropy -= probability * __import__("math").log2(probability)
    return round(entropy, 3)


def _weekly_genealogy_metrics(raw_candidates: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> dict[str, Any]:
    claim_counts = Counter(str(item.get("research_claim_type", "unclassified") or "unclassified") for item in raw_candidates)
    origin_counts = Counter(str(item.get("origin_type", "unclassified") or "unclassified") for item in raw_candidates)
    bottleneck_counts = Counter(str(item.get("bottleneck_type", "unclassified") or "unclassified") for item in raw_candidates)
    rejection_reasons = Counter()
    for item in reviews:
        for note in item.get("adversarial_notes", []):
            rejection_reasons[str(note)] += 1
    survived_breakthroughs = [
        item.get("title", "")
        for item in reviews
        if item.get("risk_class") == "breakthrough"
        and item.get("weekly_action") in {"push_to_user_review", "rewrite_for_mechanism", "park_for_weekly_followup"}
    ][:8]
    benchmark_opportunities = [
        item.get("title", "")
        for item in reviews
        if item.get("research_claim_type") in {"evaluation_benchmark", "data_curriculum"}
        and item.get("weekly_action") != "reject_with_rescue"
    ][:8]
    repeated_bottlenecks = [
        {"bottleneck_type": name, "count": count}
        for name, count in bottleneck_counts.most_common()
        if count >= 2 and name != "unclassified"
    ][:8]
    return {
        "category_entropy": _entropy(claim_counts),
        "origin_type_distribution": dict(origin_counts),
        "research_claim_type_distribution": dict(claim_counts),
        "bottleneck_type_distribution": dict(bottleneck_counts),
        "rejection_reason_histogram": dict(rejection_reasons.most_common(12)),
        "sharpness_vs_evidence_scatter": [
            {
                "title": item.get("title", ""),
                "sharpness_score": item.get("sharpness_score"),
                "evidence_execution_score": item.get("evidence_execution_score"),
                "weekly_action": item.get("weekly_action"),
            }
            for item in reviews[:20]
        ],
        "survived_breakthrough_bets": survived_breakthroughs,
        "benchmark_metric_opportunities": benchmark_opportunities,
        "repeated_bottleneck_clusters": repeated_bottlenecks,
    }


def build_weekly_top_tier_packet(end_date: str, days: int) -> dict[str, Any]:
    payloads = _iter_greenhouse_payloads(end_date, days)
    ideas = _collect_ideas()
    raw_candidates: list[dict[str, Any]] = []
    for payload in payloads:
        for candidate in payload.get("raw_gemini_candidates", []):
            if not isinstance(candidate, dict):
                continue
            merged = dict(candidate)
            merged["run_date"] = payload.get("run_date", "")
            merged["source_greenhouse_path"] = payload.get("path", "")
            _normalize_candidate_readiness(merged)
            raw_candidates.append(merged)
    candidate_reviews = [_weekly_candidate_review(item, ideas) for item in raw_candidates]
    candidate_reviews = sorted(
        candidate_reviews,
        key=lambda item: (
            WEEKLY_TOP_TIER_ACTIONS.index(str(item.get("weekly_action", "reject_with_rescue"))),
            -_as_int(item.get("weekly_score")),
            str(item.get("title", "")),
        ),
    )
    action_counts = Counter(str(item.get("weekly_action", "unlabeled")) for item in candidate_reviews)
    label_counts = Counter(str(item.get("greenhouse_label", "unlabeled")) for item in raw_candidates)
    tier_counts = Counter(str(item.get("quality_tier", "unrated")) for item in raw_candidates)
    potential_counts = Counter(str(item.get("potential_tier", item.get("quality_tier", "unrated"))) for item in raw_candidates)
    readiness_counts = Counter(str(item.get("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled"))))) for item in raw_candidates)
    group_counts = Counter(str(item.get("candidate_group", "unclassified") or "unclassified") for item in raw_candidates)
    origin_counts = Counter(str(item.get("origin_type", "unclassified") or "unclassified") for item in raw_candidates)
    claim_counts = Counter(str(item.get("research_claim_type", "unclassified") or "unclassified") for item in raw_candidates)
    risk_counts = Counter(str(item.get("risk_class", "unclassified") or "unclassified") for item in raw_candidates)
    slot_counts = Counter(str(item.get("portfolio_slot", "unclassified") or "unclassified") for item in raw_candidates)
    genealogy = _weekly_genealogy_metrics(raw_candidates, candidate_reviews)
    return {
        "end_date": end_date,
        "window_days": days,
        "review_mode": "deterministic_local_top_tier_pressure_test",
        "review_boundary": {
            "allowed_actions": WEEKLY_TOP_TIER_ACTIONS,
            "forbidden_actions": ["move_idea_folders", "delete_raw_candidates", "write_accepted_claims", "claim_confirmed_novelty"],
            "final_reviewer": "user",
            "network": "disabled_by_default",
        },
        "workflow_contracts": {
            "weekly_top_tier": WORKFLOW_CONTRACTS["weekly_top_tier"],
            "gemini_greenhouse": WORKFLOW_CONTRACTS["gemini_greenhouse"],
            "idea_quality_source_basis": WORKFLOW_CONTRACTS["idea_quality_source_basis"],
            "idea_taxonomy": WORKFLOW_CONTRACTS["idea_taxonomy"],
            "daily_readable_workflow": WORKFLOW_CONTRACTS["daily_readable_workflow"],
            "provider_matrix": WORKFLOW_CONTRACTS["provider_matrix"],
        },
        "weekly_top_tier_rubric": WEEKLY_TOP_TIER_RUBRIC,
        "source_greenhouse_files": [{"run_date": item.get("run_date", ""), "path": item.get("path", "")} for item in payloads],
        "raw_gemini_candidates": raw_candidates,
        "candidate_reviews": candidate_reviews,
        "genealogy_metrics": genealogy,
        "formal_seed_titles": [
            {"title": item.get("title", ""), "path": item.get("path", ""), "state": item.get("state", "")}
            for item in ideas
            if item.get("state") == "seed"
        ][:80],
        "counts": {
            "source_files": len(payloads),
            "raw_candidates": len(raw_candidates),
            "promoted_to_seed": label_counts.get("promoted_to_seed", 0),
            "speculative_preserve": label_counts.get("speculative_preserve", 0),
            "parked_for_weekly_review": label_counts.get("parked_for_weekly_review", 0),
            "rewrite_needed": label_counts.get("rewrite_needed", 0),
            "blocked_with_rescue_signal": label_counts.get("blocked_with_rescue_signal", 0),
            "quality_tiers": dict(tier_counts),
            "quality_tier_semantics": "potential_only_not_seed_readiness",
            "potential_tiers": dict(potential_counts),
            "readiness_tiers": dict(readiness_counts),
            "candidate_groups": dict(group_counts),
            "origin_types": dict(origin_counts),
            "research_claim_types": dict(claim_counts),
            "risk_classes": dict(risk_counts),
            "portfolio_slots": dict(slot_counts),
            "weekly_actions": dict(action_counts),
        },
    }


def _format_hits(hits: list[dict[str, Any]]) -> str:
    if not hits:
        return "none"
    parts = []
    for hit in hits[:3]:
        title = hit.get("title", "-")
        score = hit.get("overlap_score", "-")
        source = hit.get("source", hit.get("path", ""))
        parts.append(f"{title} (score={score}, source={source})")
    return "; ".join(parts)


def render_weekly_top_tier_review(packet: dict[str, Any]) -> str:
    end_date = str(packet.get("end_date", date.today().isoformat()))
    counts = packet.get("counts", {})
    genealogy = packet.get("genealogy_metrics", {})
    reviews = packet.get("candidate_reviews", [])
    status = "done" if reviews else "partial"
    frontmatter = render_frontmatter(
        f"Weekly Top-Tier Idea Review - {end_date}",
        ["research-agenda", "weekly-review", "top-tier-review", "automation"],
        f"Weekly top-tier idea review status: {status}.",
        status=status,
    )
    lines = [
        frontmatter.rstrip(),
        f"# Weekly Top-Tier Idea Review - {end_date}",
        "",
        "## Executive Verdict",
        "",
        f"- status: `{status}`",
        f"- review_mode: `{packet.get('review_mode')}`",
        f"- window_days: {packet.get('window_days')}",
        f"- source_greenhouse_files: {counts.get('source_files', 0)}",
        f"- raw_candidates: {counts.get('raw_candidates', 0)}",
        f"- candidate_groups: {json.dumps(counts.get('candidate_groups', {}), ensure_ascii=False, sort_keys=True)}",
        f"- origin_types: {json.dumps(counts.get('origin_types', {}), ensure_ascii=False, sort_keys=True)}",
        f"- research_claim_types: {json.dumps(counts.get('research_claim_types', {}), ensure_ascii=False, sort_keys=True)}",
        f"- risk_classes: {json.dumps(counts.get('risk_classes', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_slots: {json.dumps(counts.get('portfolio_slots', {}), ensure_ascii=False, sort_keys=True)}",
        f"- category_entropy: {genealogy.get('category_entropy', 0)}",
        f"- quality_tier_semantics: `{counts.get('quality_tier_semantics', 'potential_only_not_seed_readiness')}`",
        f"- potential_tiers: {json.dumps(counts.get('potential_tiers', {}), ensure_ascii=False, sort_keys=True)}",
        f"- readiness_tiers: {json.dumps(counts.get('readiness_tiers', {}), ensure_ascii=False, sort_keys=True)}",
        f"- weekly_actions: {json.dumps(counts.get('weekly_actions', {}), ensure_ascii=False, sort_keys=True)}",
        "- boundary: local-only top-tier pressure test; no idea is promoted, deleted, or claimed novel.",
        "",
        "## Top-Tier Adversarial Review",
        "",
    ]
    if not reviews:
        lines.append("- no greenhouse candidates found in this window; keep daily pipeline evidence before judging idea quality.")
    for item in reviews[:12]:
        lines.extend(
            [
                f"### {item.get('run_date')} - {item.get('title')}",
                "",
                f"- action: `{item.get('weekly_action')}`",
                f"- candidate_group: `{item.get('candidate_group', 'unclassified')}`",
                f"- origin_type: `{item.get('origin_type', '-')}`",
                f"- research_claim_type: `{item.get('research_claim_type', '-')}`",
                f"- bottleneck_type: `{item.get('bottleneck_type', '-')}`",
                f"- evidence_mode: `{item.get('evidence_mode', '-')}`",
                f"- risk_class: `{item.get('risk_class', '-')}`",
                f"- world_model_role: `{item.get('world_model_role', '-')}`",
                f"- portfolio_slot: `{item.get('portfolio_slot', '-')}`",
                f"- idea_archetype: `{item.get('idea_archetype', '-')}`",
                f"- greenhouse_label: `{item.get('greenhouse_label')}`",
                f"- quality_tier: `{item.get('quality_tier')}`",
                f"- quality_tier_semantics: `{item.get('quality_tier_semantics', 'potential_only_not_seed_readiness')}`",
                f"- potential_tier: `{item.get('potential_tier', item.get('quality_tier'))}`",
                f"- readiness_tier: `{item.get('readiness_tier', _readiness_from_label(str(item.get('greenhouse_label', 'unlabeled'))))}`",
                f"- promotion_decision: `{item.get('promotion_decision', 'not_ready')}`",
                f"- weekly_score: {item.get('weekly_score')}",
                f"- score_split: support={item.get('support_score', '-')} originality={item.get('originality_score', '-')} engineering={item.get('engineering_value_score', '-')} sharpness={item.get('sharpness_score', '-')} execution={item.get('evidence_execution_score', '-')} ordinaryness_penalty={item.get('ordinaryness_penalty', '-')}",
                f"- rubric_scores: {json.dumps(item.get('weekly_rubric_scores', {}), ensure_ascii=False, sort_keys=True)}",
                f"- adversarial_notes: {', '.join(item.get('adversarial_notes', []))}",
                f"- non_obvious_claim: {item.get('non_obvious_claim') or 'needs rewrite'}",
                f"- naive_combination_version: {item.get('naive_combination_version') or 'missing bad A+B version'}",
                f"- strongest_baseline_kill_path: {item.get('strongest_baseline_kill_path') or 'missing ruthless baseline kill path'}",
                f"- post_kill_mutation: {item.get('post_kill_mutation') or 'missing mutation after baseline kill'}",
                f"- anti_combination_test: {item.get('anti_combination_test') or 'needs rewrite'}",
                f"- top_tier_rationale: {item.get('top_tier_rationale') or 'needs review'}",
                f"- engineering_loop: {item.get('engineering_loop') or 'needs explicit robot loop'}",
                f"- method_improvement_claim: {item.get('method_improvement_claim') or 'not specified'}",
                f"- original_method_failure: {item.get('original_method_failure') or 'not specified'}",
                f"- why_improvement_not_patch: {item.get('why_improvement_not_patch') or 'not specified'}",
                f"- reviewer_kill_shot: {item.get('reviewer_kill_shot') or 'needs skeptical objection'}",
                f"- rescue_mutation: {item.get('rescue_mutation') or 'needs mutation path'}",
                f"- claim_compression: {item.get('claim_compression') or 'needs one-sentence claim'}",
                f"- lab_affordance_fit: {item.get('lab_affordance_fit')}",
                f"- readiness_level: {item.get('readiness_level')}",
                "",
            ]
        )
    lines.extend(["", "## Heilmeier / NABC Pressure", ""])
    for item in reviews[:8]:
        lines.append(f"### {item.get('title')}")
        lines.append(f"- heilmeier: {json.dumps(item.get('heilmeier', {}), ensure_ascii=False, sort_keys=True)}")
        lines.append(f"- nabc: {json.dumps(item.get('nabc', {}), ensure_ascii=False, sort_keys=True)}")
        lines.append(f"- artifact_or_reproducibility_plan: {item.get('artifact_or_reproducibility_plan')}")
        lines.append("")
    lines.extend(["## Idea Genealogy Review", ""])
    lines.append(f"- origin_type_distribution: {json.dumps(genealogy.get('origin_type_distribution', {}), ensure_ascii=False, sort_keys=True)}")
    lines.append(f"- research_claim_type_distribution: {json.dumps(genealogy.get('research_claim_type_distribution', {}), ensure_ascii=False, sort_keys=True)}")
    lines.append(f"- bottleneck_type_distribution: {json.dumps(genealogy.get('bottleneck_type_distribution', {}), ensure_ascii=False, sort_keys=True)}")
    lines.append(f"- rejection_reason_histogram: {json.dumps(genealogy.get('rejection_reason_histogram', {}), ensure_ascii=False, sort_keys=True)}")
    lines.append(f"- survived_breakthrough_bets: {json.dumps(genealogy.get('survived_breakthrough_bets', []), ensure_ascii=False)}")
    lines.append(f"- benchmark_metric_opportunities: {json.dumps(genealogy.get('benchmark_metric_opportunities', []), ensure_ascii=False)}")
    lines.append(f"- repeated_bottleneck_clusters: {json.dumps(genealogy.get('repeated_bottleneck_clusters', []), ensure_ascii=False, sort_keys=True)}")
    lines.append("")
    lines.extend(["## Novelty Pressure", ""])
    pressure_items = [
        item for item in reviews
        if isinstance(item.get("novelty_pressure"), dict)
        and item.get("novelty_pressure", {}).get("pressure") in {"medium", "high"}
    ]
    if not pressure_items:
        lines.append("- no medium/high local novelty pressure in reviewed candidates. This is not a confirmed novelty search.")
    for item in pressure_items[:10]:
        lines.append(
            f"- `{item.get('title')}` pressure=`{item.get('novelty_pressure', {}).get('pressure')}` "
            f"local_hits={_format_hits(item.get('novelty_hits', []))} "
            f"seed_overlap={_format_hits(item.get('similar_existing_seed_hits', []))}"
        )
    lines.extend(["", "## Strongest Baseline", ""])
    for item in reviews[:10]:
        lines.append(
            f"- `{item.get('title')}`: {item.get('strongest_baseline') or 'needs explicit strongest baseline'}; "
            f"baseline_failure_mode={item.get('baseline_failure_mode') or 'needs explicit reason baseline fails'}"
        )
    lines.extend(["", "## Killer Experiment Plan", ""])
    for item in reviews[:10]:
        lines.append(f"- `{item.get('title')}`: {item.get('killer_experiment') or 'needs a decisive small pilot before promotion'}")
    lines.extend(["", "## Venue Fit", ""])
    venue_counts = Counter(str(item.get("venue_fit", "unclear")) for item in reviews)
    lines.append(f"- venue_fit_counts: {json.dumps(dict(venue_counts), ensure_ascii=False, sort_keys=True)}")
    for item in reviews[:10]:
        lines.append(f"- `{item.get('title')}`: {item.get('venue_fit')}")
    lines.extend(["", "## Creativity Preservation", ""])
    rescue_items = [
        item for item in reviews
        if item.get("weekly_action") in {"rewrite_for_mechanism", "park_for_weekly_followup", "reject_with_rescue"}
    ]
    if not rescue_items:
        lines.append("- none; all reviewed candidates are already in the user-review push queue.")
    for item in rescue_items[:16]:
        lines.append(
            f"- `{item.get('title')}` action=`{item.get('weekly_action')}` "
            f"rescue_signal={item.get('rescue_signal') or 'none'}"
        )
    lines.extend(
        [
            "",
            "## Next 7 Days",
            "",
            "- Pick at most 1-2 `push_to_user_review` candidates for human review; do not promote automatically.",
            "- Rewrite candidates with weak non-obvious mechanism before asking Gemini to defend or mutate them.",
            "- For every candidate kept alive, define the strongest baseline and one killer experiment before any paper claim.",
            "- Treat novelty pressure as local-only and unverified; use live search only in a manual follow-up.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def top_tier_weekly(end_date: str, days: int, *, dry_run: bool) -> dict[str, str]:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    packet_path = REVIEWS_DIR / f"{end_date}-weekly-top-tier-packet.json"
    report_path = REVIEWS_DIR / f"{end_date}-weekly-top-tier-review.md"
    packet = build_weekly_top_tier_packet(end_date, days)
    body = render_weekly_top_tier_review(packet)
    if not dry_run:
        _quiet_safe_write(packet_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=False)
        _quiet_safe_write(report_path, body, dry_run=False)
    counts = packet.get("counts", {})
    status = "done" if counts.get("raw_candidates", 0) else "partial"
    return {
        "status": status,
        "review_mode": str(packet.get("review_mode", "")),
        "packet_path": rel(packet_path),
        "report_path": rel(report_path),
        "source_files": str(counts.get("source_files", 0)),
        "raw_candidates": str(counts.get("raw_candidates", 0)),
        "promoted_to_seed": str(counts.get("promoted_to_seed", 0)),
        "parked_for_weekly_review": str(counts.get("parked_for_weekly_review", 0)),
        "rewrite_needed": str(counts.get("rewrite_needed", 0)),
        "blocked_with_rescue_signal": str(counts.get("blocked_with_rescue_signal", 0)),
    }


def _iter_rerun_payloads(output_root: Path) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    if not output_root.exists():
        return payloads
    for path in sorted(output_root.glob("*-gemini-rerun-raw-candidates.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        payload["path"] = rel(path)
        payloads.append(payload)
    return payloads


def _rerun_candidate_review(item: dict[str, Any], ideas: list[dict[str, Any]]) -> dict[str, Any]:
    weekly = _weekly_candidate_review(item, ideas)
    action_map = {
        "push_to_user_review": "accept_for_user_review",
        "rewrite_for_mechanism": "rewrite",
        "park_for_weekly_followup": "park",
        "reject_with_rescue": "reject_with_rescue",
    }
    action = action_map.get(str(weekly.get("weekly_action")), "park")
    scores = {
        key: _as_int(weekly.get(key))
        for key in [
            "breakthrough_potential",
            "engineering_pathology_strength",
            "non_obvious_mechanism",
            "baseline_survivability",
            "killer_experiment_clarity",
        ]
    }
    structure_score, structure_missing = _structure_completeness(item)
    if not _has_rerun_accept_bar(item, scores):
        if action == "accept_for_user_review":
            action = "rewrite" if structure_score >= 7 else "park"
    return {
        **weekly,
        "rerun_group": item.get("rerun_group", ""),
        "daily_run_date": item.get("run_date", ""),
        "review_action": action,
        "allowed_actions": RERUN_REVIEW_ACTIONS,
        "final_idea_structure_score": structure_score,
        "final_idea_structure_missing": structure_missing,
        "online_or_offline_mode": item.get("online_or_offline_mode", ""),
        "minimum_no_hardware_pilot": item.get("minimum_no_hardware_pilot", ""),
        "baseline_kill_table": item.get("baseline_kill_table", ""),
        "what_would_make_this_not_a_paper": item.get("what_would_make_this_not_a_paper", ""),
        "reviewer_pre_mortem": item.get("reviewer_pre_mortem", ""),
        "negative_claim_boundary": item.get("negative_claim_boundary", ""),
        "version_evolution_story": item.get("version_evolution_story", ""),
        "core_insight": item.get("core_insight", ""),
        "pipeline_steps": item.get("pipeline_steps", ""),
        "defense_patches": item.get("defense_patches", ""),
        "baseline_matrix": item.get("baseline_matrix", ""),
        "metric_suite": item.get("metric_suite", ""),
        "risk_assumptions": item.get("risk_assumptions", ""),
        "competition_map": item.get("competition_map", ""),
        "two_week_sprint": item.get("two_week_sprint", ""),
    }


def build_rerun_review_packet(output_root: Path) -> dict[str, Any]:
    payloads = _iter_rerun_payloads(output_root)
    ideas = _collect_ideas()
    raw_candidates: list[dict[str, Any]] = []
    for payload in payloads:
        for candidate in payload.get("raw_gemini_candidates", []):
            if not isinstance(candidate, dict):
                continue
            merged = dict(candidate)
            merged["source_rerun_path"] = payload.get("path", "")
            _normalize_candidate_readiness(merged)
            raw_candidates.append(merged)
    candidate_reviews = [_rerun_candidate_review(item, ideas) for item in raw_candidates]
    candidate_reviews = sorted(
        candidate_reviews,
        key=lambda item: (
            RERUN_REVIEW_ACTIONS.index(str(item.get("review_action", "reject_with_rescue"))),
            -_as_int(item.get("weekly_score")),
            str(item.get("title", "")),
        ),
    )
    action_counts = Counter(str(item.get("review_action", "unlabeled")) for item in candidate_reviews)
    group_counts = Counter(str(item.get("rerun_group", "unknown")) for item in raw_candidates)
    tier_counts = Counter(str(item.get("quality_tier", "unrated")) for item in raw_candidates)
    potential_counts = Counter(str(item.get("potential_tier", item.get("quality_tier", "unrated"))) for item in raw_candidates)
    readiness_counts = Counter(str(item.get("readiness_tier", _readiness_from_label(str(item.get("greenhouse_label", "unlabeled"))))) for item in raw_candidates)
    return {
        "review_mode": "historical_gemini_rerun_codex_second_pass",
        "output_root": rel(output_root),
        "review_boundary": {
            "allowed_actions": RERUN_REVIEW_ACTIONS,
            "forbidden_actions": ["replace_formal_agenda", "move_idea_folders", "delete_old_candidates", "claim_confirmed_novelty"],
            "final_reviewer": "user",
            "network": "disabled_by_default",
        },
        "historical_boundary": {
            "rl_token_context": "Preserve the 2026-04-29 to 2026-05-07 RL Token / VLA / online RL emphasis as historical context.",
            "free_divergence": "Also judge current-standard free-divergence candidates that need not be RL Token.",
            "manual_reference": "2026-05-06 manual Gemini output is a positive quality reference, not ground truth.",
        },
        "workflow_contracts": {
            "codex_review": WORKFLOW_CONTRACTS["codex_review"],
            "gemini_greenhouse": WORKFLOW_CONTRACTS["gemini_greenhouse"],
            "idea_quality_source_basis": WORKFLOW_CONTRACTS["idea_quality_source_basis"],
            "idea_taxonomy": WORKFLOW_CONTRACTS["idea_taxonomy"],
            "daily_readable_workflow": WORKFLOW_CONTRACTS["daily_readable_workflow"],
            "provider_matrix": WORKFLOW_CONTRACTS["provider_matrix"],
        },
        "source_rerun_files": [{"run_date": item.get("run_date", ""), "path": item.get("path", "")} for item in payloads],
        "raw_gemini_candidates": raw_candidates,
        "candidate_reviews": candidate_reviews,
        "formal_seed_titles": [
            {"title": item.get("title", ""), "path": item.get("path", ""), "state": item.get("state", "")}
            for item in ideas
            if item.get("state") == "seed"
        ][:120],
        "counts": {
            "source_files": len(payloads),
            "raw_candidates": len(raw_candidates),
            "rerun_groups": dict(group_counts),
            "quality_tiers": dict(tier_counts),
            "quality_tier_semantics": "potential_only_not_seed_readiness",
            "potential_tiers": dict(potential_counts),
            "readiness_tiers": dict(readiness_counts),
            "review_actions": dict(action_counts),
        },
    }


def render_rerun_review_prompt(packet_path: str) -> str:
    return f"""# Historical Gemini Rerun Codex Review

You are Codex doing a read-only second-pass review for historical Gemini rerun output.

Read packet first:

`{packet_path}`

Do not use web search. Do not modify files. Do not promote or delete ideas.

Review goals:
- Compare historical_rl_token_context candidates with free_divergence_current_standard candidates.
- Preserve strong RL Token/VLA/online-RL ideas that were historically important.
- Also surface non-RL Token ideas in DLO, tactile, bimanual, wrist-camera occlusion, and contact-rich control.
- For every candidate, choose exactly one action: accept_for_user_review, rewrite, park, reject_with_rescue.
- Do not accept a candidate if reviewer_pre_mortem or what_would_make_this_not_a_paper already kills the core claim.
- Do not accept a candidate if naive_combination_version, strongest_baseline_kill_path, or post_kill_mutation is missing or if the mutation is only the same A+B idea with different wording.
- Use baseline_kill_table, strongest_baseline, minimum_no_hardware_pilot, and killer_experiment as the core review evidence.
- Use HapToken-v3 style as the acceptance bar: a candidate must have a negative claim boundary, core insight, runnable pipeline, defense patches, baseline matrix, metric suite, risk assumptions, competition map, and two-week sprint before it can be accepted for user review.
- For RL-token candidates, reject or rewrite if they never explain token compression, optimization/loss space, decoder boundary, and manifold safety.

Required Markdown sections:
- Executive Verdict
- Cross-day Ranking
- RL Token Historical Keepers
- Free-divergence New Directions
- Rewrite Queue
- Final-idea Structure Gaps
- Parked / Rescue Signals
- Strongest Baseline and No-hardware Pilot Gaps
- Boundary
"""


def render_rerun_review(packet: dict[str, Any]) -> str:
    counts = packet.get("counts", {})
    reviews = packet.get("candidate_reviews", [])
    status = "done" if reviews else "partial"
    frontmatter = render_frontmatter(
        "Historical Gemini Rerun Codex Review - 2026-04-29 to 2026-05-07",
        ["research-agenda", "codex-review", "gemini-rerun", "automation"],
        f"Historical Gemini rerun review status: {status}.",
        status=status,
    )
    lines = [
        frontmatter.rstrip(),
        "# Historical Gemini Rerun Codex Review - 2026-04-29 to 2026-05-07",
        "",
        "## Executive Verdict",
        "",
        f"- status: `{status}`",
        f"- review_mode: `{packet.get('review_mode')}`",
        f"- source_files: {counts.get('source_files', 0)}",
        f"- raw_candidates: {counts.get('raw_candidates', 0)}",
        f"- rerun_groups: {json.dumps(counts.get('rerun_groups', {}), ensure_ascii=False, sort_keys=True)}",
        f"- quality_tiers: {json.dumps(counts.get('quality_tiers', {}), ensure_ascii=False, sort_keys=True)}",
        f"- quality_tier_semantics: `{counts.get('quality_tier_semantics', 'potential_only_not_seed_readiness')}`",
        f"- potential_tiers: {json.dumps(counts.get('potential_tiers', {}), ensure_ascii=False, sort_keys=True)}",
        f"- readiness_tiers: {json.dumps(counts.get('readiness_tiers', {}), ensure_ascii=False, sort_keys=True)}",
        f"- review_actions: {json.dumps(counts.get('review_actions', {}), ensure_ascii=False, sort_keys=True)}",
        "- boundary: review only; no formal seed, agenda, or novelty claim is changed.",
        "",
        "## Cross-day Ranking",
        "",
    ]
    if not reviews:
        lines.append("- no rerun candidates found.")
    for item in reviews[:24]:
        lines.append(
            f"- `{item.get('review_action')}` {item.get('daily_run_date')} [{item.get('rerun_group')}] "
            f"potential={item.get('potential_tier', item.get('quality_tier'))} "
            f"readiness={item.get('readiness_tier', _readiness_from_label(str(item.get('greenhouse_label', 'unlabeled'))))} "
            f"score={item.get('weekly_score')} - {item.get('title')}"
        )
    rl_items = [item for item in reviews if str(item.get("rerun_group")) == "historical_rl_token_context"]
    free_items = [item for item in reviews if str(item.get("rerun_group")) == "free_divergence_current_standard"]
    lines.extend(["", "## RL Token Historical Keepers", ""])
    for item in rl_items[:12]:
        lines.append(
            f"- `{item.get('review_action')}` {item.get('title')}: baseline={item.get('strongest_baseline') or 'needs baseline'}; "
            f"pre_mortem={item.get('reviewer_pre_mortem') or item.get('reviewer_kill_shot') or 'needs pre-mortem'}"
        )
    if not rl_items:
        lines.append("- none")
    lines.extend(["", "## Free-divergence New Directions", ""])
    for item in free_items[:12]:
        lines.append(
            f"- `{item.get('review_action')}` {item.get('title')}: pathology={item.get('engineering_pathology') or 'needs pathology'}; "
            f"no_hardware={item.get('minimum_no_hardware_pilot') or 'needs no-hardware pilot'}"
        )
    if not free_items:
        lines.append("- none")
    lines.extend(["", "## Rewrite Queue", ""])
    rewrite = [item for item in reviews if item.get("review_action") == "rewrite"]
    for item in rewrite[:16]:
        lines.append(
            f"- {item.get('title')}: anti_combination={item.get('anti_combination_test') or 'missing'}; "
            f"not_a_paper={item.get('what_would_make_this_not_a_paper') or 'missing'}"
        )
    if not rewrite:
        lines.append("- none")
    lines.extend(["", "## Final-idea Structure Gaps", ""])
    for item in reviews[:20]:
        missing = []
        for field in FINAL_IDEA_STRUCTURE_FIELDS:
            if not str(item.get(field, "")).strip():
                missing.append(field)
        lines.append(
            f"- {item.get('title')}: structure_score={item.get('final_idea_structure_score', '-')}/9; "
            f"missing={', '.join(missing) if missing else 'none'}; "
            f"core_insight={str(item.get('core_insight', ''))[:160] or 'missing'}"
        )
    lines.extend(["", "## Parked / Rescue Signals", ""])
    rescue = [item for item in reviews if item.get("review_action") in {"park", "reject_with_rescue"}]
    for item in rescue[:20]:
        lines.append(f"- `{item.get('review_action')}` {item.get('title')}: rescue_signal={item.get('rescue_signal') or 'none'}")
    if not rescue:
        lines.append("- none")
    lines.extend(["", "## Strongest Baseline and No-hardware Pilot Gaps", ""])
    for item in reviews[:20]:
        lines.append(
            f"- {item.get('title')}: baseline_kill_table={item.get('baseline_kill_table') or 'missing'}; "
            f"minimum_no_hardware_pilot={item.get('minimum_no_hardware_pilot') or 'missing'}"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This report is deterministic/local triage over rerun greenhouse candidates.",
            "- It does not replace old agenda deltas or promote ideas.",
            "- User remains final reviewer before any idea enters developing/promoted/pilot-ready.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def review_rerun_range(output_root: Path, *, dry_run: bool) -> dict[str, str]:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    packet = build_rerun_review_packet(output_root)
    stem = output_root.name.strip() or "gemini-rerun"
    packet_path = REVIEWS_DIR / f"{stem}-codex-review-packet.json"
    prompt_path = REVIEWS_DIR / f"{stem}-codex-review-prompt.md"
    report_path = REVIEWS_DIR / f"{stem}-codex-review.md"
    if not dry_run:
        _quiet_safe_write(packet_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=False)
        _quiet_safe_write(prompt_path, render_rerun_review_prompt(rel(packet_path)), dry_run=False)
        _quiet_safe_write(report_path, render_rerun_review(packet), dry_run=False)
    counts = packet.get("counts", {})
    return {
        "status": "done" if counts.get("raw_candidates", 0) else "partial",
        "packet_path": rel(packet_path),
        "prompt_path": rel(prompt_path),
        "report_path": rel(report_path),
        "source_files": str(counts.get("source_files", 0)),
        "raw_candidates": str(counts.get("raw_candidates", 0)),
    }


def _v2_final_candidates(run_date: str) -> list[dict[str, Any]]:
    selected = read_json(artifact_dir(run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations}
    finals = [dict(item) for item in selected if candidate_id(item) not in mutated_parent_ids]
    finals.extend(dict(item) for item in mutations)
    return finals


def _load_execution_provider_payload(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(path_value)
    if not path.exists():
        return {"_provider_error": f"codex_execution_review_json_missing:{path}"}
    try:
        payload = read_json(path)
    except Exception as exc:
        return {"_provider_error": f"codex_execution_review_json_invalid:{type(exc).__name__}:{exc}"}
    return payload if isinstance(payload, dict) else {"_provider_error": "codex_execution_review_json_not_object"}


def _extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char != "{":
            continue
        try:
            payload, _ = decoder.raw_decode(stripped[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    raise ValueError("provider_output_json_object_not_found")


def _render_codex_execution_prompt(run_date: str, candidates: list[dict[str, Any]]) -> str:
    context = {
        "schema_version": "codex_execution_review.v1",
        "run_date": run_date,
        "final_candidates": [{**item, "candidate_id": candidate_id(item)} for item in candidates],
        "deepseek_review": read_json(artifact_dir(run_date) / "deepseek-review.json") if (artifact_dir(run_date) / "deepseek-review.json").exists() else {},
        "novelty_scan": read_json(artifact_dir(run_date) / "novelty-scan.json") if (artifact_dir(run_date) / "novelty-scan.json").exists() else {},
    }
    return json.dumps(
        {
            "task": "Return strict JSON only. Do not use markdown fences or explanatory prose. Do not edit files or run commands.",
            "required_output_shape": {
                "schema_version": "codex_execution_review.v1",
                "run_date": run_date,
                "status": "success",
                "provider_status": {"provider": "codex", "provider_backed": True, "mode": "codex-cli", "exit_code": 0},
                "reviews": [
                    {
                        "candidate_id": "string",
                        "candidate_title": "string",
                        "status": "success",
                        "action": "accept_for_user_review|rewrite_before_seed|park_for_weekly|reject_with_rescue|requires_human_decision",
                        "no_hardware_pilot_feasibility": "string",
                        "public_dataset_or_sim_availability": "string",
                        "baseline_training_cost": "string",
                        "metric_automation": "string",
                        "data_leakage_risk": "string",
                        "minimal_repo_plan": "string",
                        "real_robot_pilot_complexity": "string",
                        "reproducibility_path": "string",
                        "compute_time_budget": "string",
                        "blocking_issues": [],
                        "nonblocking_risks": [],
                        "rewrite_request": "",
                        "rescue_signal": "",
                        "confidence": "high|medium|low",
                        "field_presence_only": False,
                    }
                ],
            },
            "validation_rules": [
                "Return exactly one review per candidate_id.",
                "Required execution fields must be concrete and non-empty.",
                "field_presence_only must be false for any accepted review.",
                "If execution is not truly reproducible, choose rewrite_before_seed, park_for_weekly, reject_with_rescue, or requires_human_decision.",
            ],
            "context": context,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _kill_process_tree(pid: int) -> None:
    if sys.platform.startswith("win"):
        try:
            subprocess.run(["taskkill.exe", "/PID", str(pid), "/T", "/F"], text=True, capture_output=True, timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            pass
        return
    try:
        os.kill(pid, 9)
    except OSError:
        pass


def _provider_error_payload(error: str, *, status: str, provider_status: dict[str, Any]) -> dict[str, Any]:
    return {
        "_provider_error": error,
        "_provider_failure_status": status,
        "_provider_status": {
            **provider_status,
            "provider": "codex",
            "provider_backed": False,
            "boundary": "Provider-backed success requires a completed Codex CLI call and validated execution review JSON.",
        },
    }


def _run_codex_cli_provider(run_date: str, candidates: list[dict[str, Any]], *, timeout_sec: int) -> dict[str, Any]:
    codex_path = shutil.which("codex.cmd") or shutil.which("codex") or shutil.which("codex.exe")
    status: dict[str, Any] = {"mode": "codex-cli", "exit_code": None, "timed_out": False}
    if not codex_path:
        return _provider_error_payload("codex_cli_not_found", status="partial_provider_unavailable", provider_status=status)
    output_path = Path(tempfile.gettempdir()) / f"codex-v2-execution-review-{run_date}-{os.getpid()}.json"
    prompt = _render_codex_execution_prompt(run_date, candidates)
    command = [
        codex_path,
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--cd",
        str(vault_path()),
        "--sandbox",
        "read-only",
        "-c",
        'approval_policy="never"',
        "--output-last-message",
        str(output_path),
        "-",
    ]
    try:
        proc = subprocess.Popen(
            command,
            cwd=vault_path(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        stdout, _stderr = proc.communicate(prompt, timeout=timeout_sec)
        status["exit_code"] = proc.returncode
    except subprocess.TimeoutExpired:
        _kill_process_tree(proc.pid)
        status["timed_out"] = True
        return _provider_error_payload(f"codex_cli_timeout:{timeout_sec}s", status="partial_provider_unavailable", provider_status=status)
    except OSError as exc:
        return _provider_error_payload(f"codex_cli_error:{type(exc).__name__}:{exc}", status="partial_provider_unavailable", provider_status=status)
    if status["exit_code"] != 0:
        return _provider_error_payload(f"codex_cli_nonzero_exit:{status['exit_code']}", status="partial_provider_unavailable", provider_status=status)
    output_text = ""
    if output_path.exists():
        output_text = output_path.read_text(encoding="utf-8-sig", errors="replace")
        try:
            output_path.unlink()
        except OSError:
            pass
    if not output_text.strip():
        output_text = stdout or ""
    try:
        payload = _extract_json_object(output_text)
    except Exception as exc:
        return _provider_error_payload(f"codex_cli_invalid_json:{type(exc).__name__}:{exc}", status="partial_provider_invalid", provider_status=status)
    payload["schema_version"] = "codex_execution_review.v1"
    payload["run_date"] = run_date
    payload["status"] = "success"
    payload["provider_status"] = {
        **dict(payload.get("provider_status", {})),
        **status,
        "provider": "codex",
        "provider_backed": True,
    }
    return payload


def _has_substantive_execution_review_fields(review: dict[str, Any]) -> bool:
    if review.get("action") not in CODEX_EXECUTION_ACTIONS:
        return False
    return all(str(review.get(field, "")).strip() for field in EXECUTION_REVIEW_FIELDS)


def _hydrate_execution_provider_review_metadata(candidates: list[dict[str, Any]], payload: dict[str, Any]) -> dict[str, Any]:
    reviews = [item for item in payload.get("reviews", []) if isinstance(item, dict)]
    if not reviews:
        return payload
    by_id = {candidate_id(item): item for item in candidates}
    hydrated_candidate_id = False
    hydrated_status = False
    if len(candidates) == 1 and len(reviews) == 1:
        expected_id = candidate_id(candidates[0])
        if str(reviews[0].get("candidate_id", "")).strip() != expected_id:
            reviews[0]["candidate_id"] = expected_id
            hydrated_candidate_id = True
    for review in reviews:
        cid = str(review.get("candidate_id", "")).strip()
        candidate = by_id.get(cid)
        if candidate and not str(review.get("candidate_title", "")).strip():
            review["candidate_title"] = candidate.get("title", "")
        if not str(review.get("status", "")).strip() and _has_substantive_execution_review_fields(review):
            review["status"] = "success"
            hydrated_status = True
    payload["reviews"] = reviews
    provider_status = dict(payload.get("provider_status", {}))
    if hydrated_candidate_id:
        provider_status["candidate_id_hydrated_from_single_candidate_batch"] = True
    if hydrated_status:
        provider_status["review_status_hydrated_from_execution_fields"] = True
    if provider_status:
        payload["provider_status"] = provider_status
    return payload


def _schema_safe_execution_reviews(reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    safe_reviews: list[dict[str, Any]] = []
    for review in reviews:
        safe = dict(review)
        if safe.get("status") not in {"success", "failed_fallback_only"}:
            safe["status"] = "failed_fallback_only"
        if safe.get("action") not in CODEX_EXECUTION_ACTIONS:
            safe["action"] = "requires_human_decision"
        for field in CODEX_EXECUTION_REQUIRED_REVIEW_FIELDS:
            if not str(safe.get(field, "")).strip():
                safe[field] = "not_provided"
        safe_reviews.append(safe)
    return safe_reviews


def _validate_execution_provider_reviews(candidates: list[dict[str, Any]], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    provider = payload.get("provider_status", {})
    if not provider.get("provider_backed"):
        errors.append("provider_status_not_provider_backed")
    if provider.get("provider") not in {"codex", "implementation_review"}:
        errors.append(f"provider_not_codex_execution:{provider.get('provider')}")
    reviews = [item for item in payload.get("reviews", []) if isinstance(item, dict)]
    candidate_ids = [candidate_id(item) for item in candidates]
    seen: dict[str, int] = {}
    for review in reviews:
        cid = str(review.get("candidate_id"))
        seen[cid] = seen.get(cid, 0) + 1
        if cid not in candidate_ids:
            errors.append(f"unexpected_execution_review:{cid}")
    for cid, count in seen.items():
        if count > 1:
            errors.append(f"duplicate_execution_review:{cid}")
    by_id = {str(item.get("candidate_id")): item for item in reviews}
    for item in candidates:
        cid = candidate_id(item)
        review = by_id.get(cid)
        if not review:
            errors.append(f"missing_execution_review:{cid}")
            continue
        if review.get("status") != "success":
            errors.append(f"execution_review_not_success:{cid}:{review.get('status')}")
        for field in EXECUTION_REVIEW_FIELDS:
            if not str(review.get(field, "")).strip():
                errors.append(f"execution_review_missing_field:{cid}:{field}")
        if not str(review.get("candidate_title", "")).strip():
            errors.append(f"execution_review_missing_field:{cid}:candidate_title")
        if review.get("action") not in CODEX_EXECUTION_ACTIONS:
            errors.append(f"execution_review_invalid_action:{cid}:{review.get('action')}")
        if review.get("confidence") and review.get("confidence") not in CODEX_CONFIDENCE_VALUES:
            errors.append(f"execution_review_invalid_confidence:{cid}:{review.get('confidence')}")
        if review.get("action") == "accept_for_user_review" and review.get("field_presence_only"):
            errors.append(f"field_presence_only_accept_disallowed:{cid}")
    return errors


def _fallback_execution_review(item: dict[str, Any]) -> dict[str, Any]:
    cid = candidate_id(item)
    return {
        "candidate_id": cid,
        "candidate_title": item.get("title", ""),
        "status": "failed_fallback_only",
        "action": "reject_with_rescue",
        "execution_risks": ["provider_backed_codex_execution_review_missing"],
        "no_hardware_pilot_feasibility": "not_verified",
        "public_dataset_or_sim_availability": "not_verified",
        "baseline_training_cost": "not_verified",
        "metric_automation": "not_verified",
        "data_leakage_risk": "not_verified",
        "minimal_repo_plan": "not_verified",
        "real_robot_pilot_complexity": "not_verified",
        "reproducibility_path": "not_verified",
        "compute_time_budget": "not_verified",
        "field_presence_only": True,
        "boundary": "Fallback artifact only; formal promotion requires provider-backed implementation review.",
    }


def execution_review(run_date: str, *, dry_run: bool, provider_review_json: str = "", provider: str = "json", timeout_sec: int = 1200) -> dict[str, str]:
    ensure_v2_dirs(run_date)
    candidates = _v2_final_candidates(run_date)
    if provider == "codex-cli":
        provider_payload = _run_codex_cli_provider(run_date, candidates, timeout_sec=timeout_sec)
    elif provider_review_json:
        provider_payload = _load_execution_provider_payload(provider_review_json)
    else:
        provider_payload = {}
    if provider_payload and not provider_payload.get("_provider_error"):
        provider_payload = _hydrate_execution_provider_review_metadata(candidates, provider_payload)
        provider_errors = _validate_execution_provider_reviews(candidates, provider_payload)
        reviews = _schema_safe_execution_reviews([item for item in provider_payload.get("reviews", []) if isinstance(item, dict)])
        status = "success" if not provider_errors and candidates else "partial_provider_invalid"
        provider_status = {**dict(provider_payload.get("provider_status", {})), "validation_errors": provider_errors}
        if status != "success":
            provider_status["provider_backed"] = False
    else:
        reviews = [_fallback_execution_review(item) for item in candidates]
        status = provider_payload.get("_provider_failure_status") or ("partial_provider_unavailable" if reviews else "partial_empty_selection")
        provider_status = provider_payload.get("_provider_status") or {
            "provider": "codex",
            "provider_backed": False,
            "mode": "field_presence_fallback_only",
            "provider_error": provider_payload.get("_provider_error", "codex_execution_provider_unavailable"),
            "required_fields": EXECUTION_REVIEW_FIELDS,
            "boundary": "Field presence or polished prose is not an execution review and cannot promote.",
        }
        provider_status["provider_error"] = provider_payload.get("_provider_error", "codex_execution_provider_unavailable")
        if reviews:
            provider_status["fallback_reviews_fail_closed"] = True
            provider_status["provider_fallback_count"] = len(reviews)
    payload = {
        "schema_version": "codex_execution_review.v1",
        "run_date": run_date,
        "status": status,
        "reviews": reviews,
        "provider_status": provider_status,
        "artifact_hashes": artifact_hashes(run_date, ["selected-candidates.json", "gemini-mutations.json", "novelty-scan.json"]),
        "boundary": "Execution review only; no files are moved and no formal seed is written.",
    }
    write_run_artifact(run_date, "codex-execution-review.json", payload, state="execution_reviewed", dry_run=dry_run)
    return {
        "status": payload["status"],
        "reviews": str(len(reviews)),
        "fallback_reviews_fail_closed": str(bool(provider_status.get("fallback_reviews_fail_closed"))).lower(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--run-date", default=date.today().isoformat())
    prepare_parser.add_argument("--catch-up", action="store_true", help="Review the newest successful daily run without a done Codex report.")
    prepare_parser.add_argument("--catch-up-days", type=int, default=7)
    prepare_parser.add_argument("--dry-run", action="store_true")
    prepare_parser.add_argument("--json", action="store_true")

    wrap_parser = subparsers.add_parser("wrap")
    wrap_parser.add_argument("--run-date", default=date.today().isoformat())
    wrap_parser.add_argument("--codex-output", required=True)
    wrap_parser.add_argument("--codex-exit-code", type=int, required=True)
    wrap_parser.add_argument("--dry-run", action="store_true")
    wrap_parser.add_argument("--json", action="store_true")

    weekly_parser = subparsers.add_parser("greenhouse-weekly")
    weekly_parser.add_argument("--end-date", default=date.today().isoformat())
    weekly_parser.add_argument("--days", type=int, default=7)
    weekly_parser.add_argument("--dry-run", action="store_true")
    weekly_parser.add_argument("--json", action="store_true")

    top_tier_parser = subparsers.add_parser("top-tier-weekly")
    top_tier_parser.add_argument("--end-date", default=date.today().isoformat())
    top_tier_parser.add_argument("--days", type=int, default=7)
    top_tier_parser.add_argument("--dry-run", action="store_true")
    top_tier_parser.add_argument("--json", action="store_true")

    rerun_parser = subparsers.add_parser("review-rerun-range")
    rerun_parser.add_argument("--output-root", default="projects/research-agenda/divergent-reruns/2026-05-08-0429-0507")
    rerun_parser.add_argument("--dry-run", action="store_true")
    rerun_parser.add_argument("--json", action="store_true")

    execution_parser = subparsers.add_parser("execution-review")
    execution_parser.add_argument("--run-date", required=True)
    execution_parser.add_argument("--provider", choices=["json", "codex-cli", "none"], default="json")
    execution_parser.add_argument("--provider-review-json", default=os.environ.get("CODEX_EXECUTION_REVIEW_JSON", ""))
    execution_parser.add_argument("--timeout", type=int, default=1200)
    execution_parser.add_argument("--dry-run", action="store_true")
    execution_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.run_date, dry_run=args.dry_run, catch_up=args.catch_up, catch_up_days=args.catch_up_days)
    elif args.command == "wrap":
        output_path = Path(args.codex_output)
        if not output_path.is_absolute():
            output_path = vault_path(args.codex_output)
        result = wrap(args.run_date, output_path, args.codex_exit_code, dry_run=args.dry_run)
    elif args.command == "greenhouse-weekly":
        result = greenhouse_weekly(args.end_date, args.days, dry_run=args.dry_run)
    elif args.command == "top-tier-weekly":
        result = top_tier_weekly(args.end_date, args.days, dry_run=args.dry_run)
    elif args.command == "execution-review":
        result = execution_review(
            args.run_date,
            dry_run=args.dry_run,
            provider_review_json=args.provider_review_json,
            provider=args.provider,
            timeout_sec=args.timeout,
        )
    else:
        output_root = Path(args.output_root)
        if not output_root.is_absolute():
            output_root = vault_path(*output_root.parts)
        result = review_rerun_range(output_root, dry_run=args.dry_run)
    if getattr(args, "json", False):
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(" ".join(f"{key}={value}" for key, value in result.items()))
    if (
        args.command == "execution-review"
        and result.get("status") != "success"
        and result.get("fallback_reviews_fail_closed") != "true"
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
