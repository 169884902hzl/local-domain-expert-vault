"""Shared v1 Research Governance Workbench helpers.

v1 separates automated candidate production from human-governed active seed
commitment. Scheduled automation may write drafts, screens, critiques, queues,
and derived dashboards. Only active_seed_commit.py may write active seed records
or the governance ledger.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kb_common import vault_path
from research_agenda_common import AGENDA_ROOT, slugify

try:
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover
    Draft202012Validator = None  # type: ignore[assignment]


SCHEMA_ROOT = vault_path(".claude", "schemas", "research_governance_v1")
STATE_MACHINE_VERSION = "research_governance_state_machine.v1"

STATES = [
    "intake_screened",
    "paper_primitives_extracted",
    "evidence_packet_drafted",
    "evidence_packet_confirmed",
    "raw_hypothesis_drafted",
    "program_candidate_synthesized",
    "portfolio_screened_candidate",
    "model_reviewed_candidate",
    "external_screened_candidate",
    "formal_rehearsal_packet_ready",
    "manual_prior_art_dossier_completed",
    "baseline_execution_ready",
    "pilot_plan_ready",
    "governance_review_requested",
    "active_seed_committed",
    "pilot_executed",
    "strategy_updated",
    "candidate_parked",
    "candidate_rejected",
    "active_seed_killed",
    "resurrection_queued",
    "archived_legacy",
]

SCHEDULED_ALLOWED_STATES = {
    "intake_screened",
    "paper_primitives_extracted",
    "evidence_packet_drafted",
    "raw_hypothesis_drafted",
    "program_candidate_synthesized",
    "portfolio_screened_candidate",
    "model_reviewed_candidate",
    "external_screened_candidate",
    "candidate_parked",
}

SCHEDULED_FORBIDDEN_STATES = {
    "evidence_packet_confirmed",
    "formal_rehearsal_packet_ready",
    "manual_prior_art_dossier_completed",
    "baseline_execution_ready",
    "pilot_plan_ready",
    "governance_review_requested",
    "active_seed_committed",
    "active_seed_killed",
    "strategy_updated",
}

LEGAL_TRANSITIONS = {
    "intake_screened": {"paper_primitives_extracted", "candidate_parked", "candidate_rejected"},
    "paper_primitives_extracted": {"evidence_packet_drafted", "raw_hypothesis_drafted"},
    "evidence_packet_drafted": {"evidence_packet_confirmed", "raw_hypothesis_drafted", "candidate_parked"},
    "evidence_packet_confirmed": {"manual_prior_art_dossier_completed", "raw_hypothesis_drafted"},
    "raw_hypothesis_drafted": {"program_candidate_synthesized", "candidate_parked", "candidate_rejected"},
    "program_candidate_synthesized": {"portfolio_screened_candidate", "candidate_parked", "candidate_rejected"},
    "portfolio_screened_candidate": {"model_reviewed_candidate", "candidate_parked", "candidate_rejected"},
    "model_reviewed_candidate": {"external_screened_candidate", "candidate_parked", "candidate_rejected"},
    "external_screened_candidate": {
        "formal_rehearsal_packet_ready",
        "manual_prior_art_dossier_completed",
        "baseline_execution_ready",
        "candidate_parked",
        "candidate_rejected",
    },
    "formal_rehearsal_packet_ready": {"manual_prior_art_dossier_completed", "candidate_parked"},
    "manual_prior_art_dossier_completed": {"baseline_execution_ready", "pilot_plan_ready"},
    "baseline_execution_ready": {"pilot_plan_ready", "governance_review_requested"},
    "pilot_plan_ready": {"governance_review_requested"},
    "governance_review_requested": {"active_seed_committed", "candidate_parked", "candidate_rejected"},
    "active_seed_committed": {"pilot_executed", "active_seed_killed", "resurrection_queued"},
    "pilot_executed": {"strategy_updated", "active_seed_killed", "candidate_parked"},
    "strategy_updated": {"candidate_parked", "resurrection_queued"},
    "candidate_parked": {"resurrection_queued", "candidate_rejected", "archived_legacy"},
    "candidate_rejected": {"archived_legacy"},
    "active_seed_killed": {"resurrection_queued", "archived_legacy"},
    "resurrection_queued": {"portfolio_screened_candidate", "candidate_parked", "candidate_rejected"},
    "archived_legacy": set(),
}

FORBIDDEN_SCHEDULED_TOKENS = [
    "--target-policy formal",
    "--v2-publish-policy formal",
    "--allow-formal-seed-publish",
    "--allow-human-override",
    "--commit-active-seed",
    "formal_rehearsal_packet.py",
    "governance_review.py",
    "active_seed_commit.py",
    "strategy_ledger.py",
    "--apply-strategy",
    "--active-seed-id",
    "--human-confirmed",
    "--governance-signature",
]

PUBLIC_FORBIDDEN_SUFFIXES = {".pdf", ".sqlite", ".sqlite3", ".db", ".log", ".pyc", ".bak"}
PUBLIC_FORBIDDEN_PARTS = {
    ".env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "attachments/",
    "archive/",
    "/logs/",
    "backup",
    "secret",
    "projects/research-agenda/runs/",
    "projects/research-agenda/cache/",
    "projects/research-agenda/governance/active-seeds/",
    "projects/research-agenda/governance/ledger/",
    "projects/arxiv-daily/metadata/",
}

REQUIRED_ACTIVE_ARTIFACTS = {
    "candidate_record": "candidates/{candidate_id}/candidate-record.json",
    "confirmed_evidence_packet": "evidence-packets/{candidate_id}/evidence-packet.confirmed.json",
    "manual_prior_art_dossier": "prior-art-dossiers/{candidate_id}/manual-prior-art-dossier.json",
    "provider_review_packet": "provider-reviews/{candidate_id}/provider-review-packet.json",
    "novelty_screen": "novelty-screens/{candidate_id}/novelty-screen.json",
    "baseline_execution_readiness": "baseline-readiness/{candidate_id}/baseline-execution-readiness.json",
    "pilot_plan": "pilot-plans/{candidate_id}/pilot-plan.json",
    "governance_review": "governance/reviews/{candidate_id}/governance-review.json",
}

GOVERNANCE_SCHEMA_BY_ARTIFACT = {
    "candidate_record": "candidate_record.v1",
    "confirmed_evidence_packet": "evidence_packet.v1",
    "manual_prior_art_dossier": "prior_art_dossier.v1",
    "provider_review_packet": "provider_review_packet.v1",
    "novelty_screen": "novelty_screen.v1",
    "baseline_execution_readiness": "baseline_execution_readiness.v1",
    "pilot_plan": "pilot_plan.v1",
    "governance_review": "governance_review.v1",
}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


def agenda_root() -> Path:
    override = os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT") or os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
    return Path(override).resolve() if override else AGENDA_ROOT


def governance_path(*parts: str) -> Path:
    return agenda_root().joinpath(*parts)


def candidate_dir(candidate_id: str) -> Path:
    return governance_path("candidates", candidate_id)


def evidence_packet_dir(candidate_id: str) -> Path:
    return governance_path("evidence-packets", candidate_id)


def prior_art_dir(candidate_id: str) -> Path:
    return governance_path("prior-art-dossiers", candidate_id)


def provider_review_dir(candidate_id: str) -> Path:
    return governance_path("provider-reviews", candidate_id)


def novelty_screen_dir(candidate_id: str) -> Path:
    return governance_path("novelty-screens", candidate_id)


def nearest_work_dir(candidate_id: str) -> Path:
    return governance_path("nearest-work-matrices", candidate_id)


def baseline_readiness_dir(candidate_id: str) -> Path:
    return governance_path("baseline-readiness", candidate_id)


def formal_rehearsal_dir(candidate_id: str) -> Path:
    return governance_path("formal-rehearsals", candidate_id)


def pilot_plan_dir(candidate_id: str) -> Path:
    return governance_path("pilot-plans", candidate_id)


def pilot_result_dir(candidate_id: str) -> Path:
    return governance_path("pilot-results", candidate_id)


def governance_review_dir(candidate_id: str) -> Path:
    return governance_path("governance", "reviews", candidate_id)


def active_seed_dir(active_seed_id: str) -> Path:
    return governance_path("governance", "active-seeds", active_seed_id)


def governance_ledger_path() -> Path:
    return governance_path("governance", "ledger", "governance-ledger.jsonl")


def strategy_ledger_path() -> Path:
    return governance_path("strategy", "strategy-ledger.jsonl")


def legacy_v03_dir() -> Path:
    return governance_path("legacy-v03")


def run_artifact_dir(run_id: str) -> Path:
    return governance_path("runs", run_id, "artifacts")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_v1_dirs(candidate_id: str | None = None) -> None:
    dirs = [
        governance_path("runs"),
        governance_path("candidates"),
        governance_path("evidence-packets"),
        governance_path("prior-art-dossiers"),
        governance_path("provider-reviews"),
        governance_path("novelty-screens"),
        governance_path("nearest-work-matrices"),
        governance_path("baseline-readiness"),
        governance_path("formal-rehearsals"),
        governance_path("governance", "active-seeds"),
        governance_path("governance", "ledger"),
        governance_path("governance", "reviews"),
        governance_path("pilot-plans"),
        governance_path("pilot-results"),
        governance_path("strategy"),
        legacy_v03_dir(),
    ]
    if candidate_id:
        dirs.extend(
            [
                candidate_dir(candidate_id),
                evidence_packet_dir(candidate_id),
                prior_art_dir(candidate_id),
                provider_review_dir(candidate_id),
                novelty_screen_dir(candidate_id),
                nearest_work_dir(candidate_id),
                baseline_readiness_dir(candidate_id),
                formal_rehearsal_dir(candidate_id),
                pilot_plan_dir(candidate_id),
                pilot_result_dir(candidate_id),
                governance_review_dir(candidate_id),
            ]
        )
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any], *, dry_run: bool = False, overwrite: bool = True) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing_to_overwrite:{path}")
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_jsonl(path: Path, payload: dict[str, Any], *, dry_run: bool = False) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_hash(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": file_sha256(path)} if path.exists() else {"path": str(path), "sha256": ""}


def candidate_id_from_title(title: str, *, prefix: str = "cand") -> str:
    return f"{prefix}-{slugify(title, max_len=56)}"


def active_seed_id_from_candidate(candidate_id: str, title: str) -> str:
    digest = hashlib.sha1(candidate_id.encode("utf-8")).hexdigest()[:8]
    return f"active-{slugify(title or candidate_id, max_len=56)}-{digest}"


def transition_errors(from_state: str, to_state: str, *, mode: str = "manual", applied_strategy_event: bool = False) -> list[str]:
    errors: list[str] = []
    if from_state not in STATES:
        errors.append(f"unknown_from_state:{from_state}")
    if to_state not in STATES:
        errors.append(f"unknown_to_state:{to_state}")
    if errors:
        return errors
    if to_state not in LEGAL_TRANSITIONS.get(from_state, set()):
        errors.append(f"illegal_transition:{from_state}->{to_state}")
    if mode == "scheduled" and to_state in SCHEDULED_FORBIDDEN_STATES:
        errors.append(f"scheduled_forbidden_state:{to_state}")
    if mode == "scheduled" and to_state == "strategy_updated" and applied_strategy_event:
        errors.append("scheduled_forbidden_applied_strategy_event")
    return errors


def scheduled_command_errors(command_text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", command_text)
    return [f"scheduled_forbidden_token:{token}" for token in FORBIDDEN_SCHEDULED_TOKENS if token in normalized]


def is_human_confirmed(payload: dict[str, Any]) -> bool:
    return (
        payload.get("human_confirmed") is True
        and bool(str(payload.get("confirmed_by") or payload.get("reviewer") or "").strip())
        and bool(str(payload.get("confirmed_at") or payload.get("reviewed_at") or "").strip())
    )


def core_evidence_errors(evidence_packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    items = evidence_packet.get("core_evidence", [])
    if not items:
        return ["missing_core_evidence"]
    for index, item in enumerate(items):
        evidence_type = str(item.get("evidence_type") or "")
        if item.get("legacy_only") is True:
            errors.append(f"legacy_only_artifact_used_as_active_evidence:{index}")
        if item.get("dashboard_source") is True or str(item.get("source_artifact", "")).endswith("dashboard.json"):
            errors.append(f"dashboard_artifact_used_as_input:{index}")
        if evidence_type == "note_only":
            errors.append(f"note_only_evidence_cannot_support_active:{index}")
        if evidence_type == "result_row" and item.get("manual_confirmed") is not True:
            errors.append(f"result_row_unconfirmed:{index}")
        if evidence_type in {"cross_paper_support", "cross_paper_contradiction", "cross_paper_edge"}:
            if item.get("human_confirmed") is not True and item.get("edge_quality_status") not in {"audited", "confirmed"}:
                errors.append(f"cross_paper_edge_unconfirmed:{index}")
        if item.get("contradiction_status") == "unresolved":
            errors.append(f"unresolved_contradiction:{index}")
    return errors


def artifact_hash_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for item in payload.get("artifact_hashes", []):
        if not isinstance(item, dict):
            continue
        path_text = str(item.get("path") or "")
        expected = str(item.get("sha256") or "")
        if not path_text or not expected:
            continue
        path = Path(path_text)
        if not path.is_absolute():
            path = agenda_root() / path
        if not path.exists():
            errors.append(f"hash_source_missing:{path_text}")
        elif file_sha256(path) != expected:
            errors.append(f"hash_mismatch:{path_text}")
    return errors


def _schema_path(schema_version: str) -> Path:
    stem = schema_version.removesuffix(".v1").replace(".", "_")
    return SCHEMA_ROOT / f"{stem}.schema.json"


def _schema_errors(payload: dict[str, Any], schema_version: str) -> list[str]:
    if payload.get("schema_version") != schema_version:
        return [f"schema_version_mismatch:expected={schema_version}:actual={payload.get('schema_version')}"]
    path = _schema_path(schema_version)
    if not path.exists():
        return [f"missing_schema:{path}"]
    schema = read_json(path)
    if Draft202012Validator is None:
        return [f"missing_field:{field}" for field in schema.get("required", []) if field not in payload]
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        return [f"schema_invalid:{schema_version}:{type(exc).__name__}:{exc}"]
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path)):
        where = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"jsonschema:{schema_version}:{where}:{error.message}")
    return errors


def _hashes_include_current_file(payload: dict[str, Any], path: Path) -> bool:
    if not path.exists():
        return False
    expected = file_sha256(path)
    resolved = path.resolve()
    rel = str(path.relative_to(agenda_root())).replace("\\", "/") if path.is_relative_to(agenda_root()) else ""
    for item in payload.get("artifact_hashes", []):
        if not isinstance(item, dict):
            continue
        path_text = str(item.get("path") or "")
        actual_hash = str(item.get("sha256") or "")
        if actual_hash != expected:
            continue
        candidate = Path(path_text)
        if candidate.is_absolute() and candidate.resolve() == resolved:
            return True
        if path_text.replace("\\", "/") == rel:
            return True
    return False


def _provider_review_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    provider_status = payload.get("provider_status", {})
    provider_status = provider_status if isinstance(provider_status, dict) else {}
    provider_backed = payload.get("provider_backed") is True or provider_status.get("provider_backed") is True
    status = str(payload.get("review_status") or payload.get("status") or "")
    provider_state = str(provider_status.get("status") or "")
    if not provider_backed:
        errors.append("provider_review_not_provider_backed")
    if payload.get("test_provider_used") is True or provider_status.get("test_provider_used") is True:
        errors.append("test_provider_review_blocks_active")
    if status != "success":
        errors.append("provider_review_not_success")
    if status in {"timeout", "provider_unavailable", "partial_provider_unavailable"} or provider_state in {"timeout", "provider_unavailable", "partial_provider_unavailable"}:
        errors.append("provider_review_unavailable_blocks_active")
    return errors


def _novelty_screen_errors(payload: dict[str, Any], dossier: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = str(payload.get("screen_status") or payload.get("status") or "")
    if status != "success":
        errors.append("novelty_screen_not_success")
    if payload.get("stale") is True or payload.get("stale_external_novelty_cache") is True or payload.get("cache_status") == "stale":
        errors.append("stale_novelty_screen_blocks_active")
    if payload.get("screening_only") is not True:
        errors.append("api_screening_must_be_screening_only")
    if payload.get("replaces_manual_prior_art_dossier") is True or payload.get("manual_prior_art_replaced") is True:
        errors.append("api_screening_cannot_replace_manual_prior_art_dossier")
    provider_status = str(payload.get("provider_status") or payload.get("api_provider_status") or "")
    provider_errors = [str(item) for item in payload.get("provider_errors", []) if item]
    provider_unavailable = provider_status in {"timeout", "provider_unavailable", "partial_provider_unavailable"} or any(
        marker in " ".join(provider_errors).lower()
        for marker in ["timeout", "provider_unavailable", "unavailable"]
    )
    if provider_unavailable and dossier.get("timeout_covered_by_manual_dossier") is not True:
        errors.append("novelty_provider_unavailable_not_covered_by_manual_dossier")
    return errors


def active_commit_validation(candidate_id: str, *, active_seed_id: str | None = None) -> ValidationResult:
    errors: list[str] = []
    paths = {name: governance_path(template.format(candidate_id=candidate_id)) for name, template in REQUIRED_ACTIVE_ARTIFACTS.items()}
    payloads = {name: read_json(path) for name, path in paths.items()}
    for name, payload in payloads.items():
        if not payload:
            errors.append(f"missing_{name}")
            continue
        schema_version = GOVERNANCE_SCHEMA_BY_ARTIFACT.get(name)
        if schema_version:
            errors.extend(_schema_errors(payload, schema_version))

    candidate = payloads.get("candidate_record", {})
    evidence = payloads.get("confirmed_evidence_packet", {})
    dossier = payloads.get("manual_prior_art_dossier", {})
    provider_review = payloads.get("provider_review_packet", {})
    novelty_screen = payloads.get("novelty_screen", {})
    baseline = payloads.get("baseline_execution_readiness", {})
    pilot = payloads.get("pilot_plan", {})
    review = payloads.get("governance_review", {})

    if evidence:
        if evidence.get("packet_status") != "confirmed" or not is_human_confirmed(evidence):
            errors.append("missing_confirmed_evidence_packet")
        errors.extend(core_evidence_errors(evidence))
        errors.extend(artifact_hash_errors(evidence))
    if dossier:
        if dossier.get("dossier_status") != "completed" or not is_human_confirmed(dossier):
            errors.append("missing_manual_prior_art_dossier")
        if dossier.get("screening_only") is True:
            errors.append("prior_art_screening_not_dossier")
        if dossier.get("provider_timeout_seen") is True and dossier.get("timeout_covered_by_manual_dossier") is not True:
            errors.append("provider_timeout_not_covered_by_manual_dossier")
    if provider_review:
        errors.extend(_provider_review_errors(provider_review))
    if novelty_screen:
        errors.extend(_novelty_screen_errors(novelty_screen, dossier))
    if baseline:
        status = str(baseline.get("readiness_status") or "")
        if status not in {"ready", "not_applicable"}:
            errors.append("missing_baseline_execution_readiness")
        if status == "not_applicable" and not str(baseline.get("not_applicable_reason") or "").strip():
            errors.append("baseline_not_applicable_missing_reason")
    if pilot:
        if pilot.get("plan_status") != "ready" or not is_human_confirmed(pilot):
            errors.append("missing_pilot_plan")
    if review:
        if not is_human_confirmed(review) or not str(review.get("governance_signature") or "").strip():
            errors.append("missing_governance_signature")
        for field in ["owner", "resource_budget", "timeline", "kill_criteria"]:
            if not str(review.get(field) or "").strip():
                errors.append(f"active_seed_record_missing_{field}")
        errors.extend(artifact_hash_errors(review))
        for name in ["provider_review_packet", "novelty_screen"]:
            if not _hashes_include_current_file(review, paths[name]):
                errors.append(f"missing_{name}_hash")
    if candidate:
        if candidate.get("legacy_status") == "archived_legacy" or (candidate.get("auto_promote_allowed") is False and candidate.get("legacy_v03") is True):
            errors.append("legacy_seed_never_auto_promotes")
        if candidate.get("test_provider_used") is True:
            errors.append("test_provider_used_blocks_active_commit")
        if candidate.get("stale_novelty_cache") is True:
            errors.append("stale_novelty_cache_blocks_active")
        if candidate.get("novelty_provider_status") in {"timeout", "provider_unavailable"} and not dossier.get("timeout_covered_by_manual_dossier"):
            errors.append("api_novelty_timeout_fails_closed")
        if candidate.get("dashboard_artifact_used_as_input") is True:
            errors.append("dashboard_artifact_used_as_input")
    if active_seed_id and (active_seed_dir(active_seed_id) / "active-seed-record.json").exists():
        errors.append(f"active_seed_record_exists:{active_seed_id}")
    return ValidationResult(ok=not errors, errors=sorted(set(errors)), warnings=[])


def active_seed_record(candidate_id: str, *, active_seed_id: str, actor: str, governance_signature: str) -> dict[str, Any]:
    candidate = read_json(governance_path(REQUIRED_ACTIVE_ARTIFACTS["candidate_record"].format(candidate_id=candidate_id)))
    review = read_json(governance_path(REQUIRED_ACTIVE_ARTIFACTS["governance_review"].format(candidate_id=candidate_id)))
    paths = {name: governance_path(template.format(candidate_id=candidate_id)) for name, template in REQUIRED_ACTIVE_ARTIFACTS.items()}
    return {
        "schema_version": "active_seed_record.v1",
        "state_machine_version": STATE_MACHINE_VERSION,
        "active_seed_id": active_seed_id,
        "candidate_id": candidate_id,
        "title": str(candidate.get("title") or review.get("title") or candidate_id),
        "committed_at": utc_now(),
        "committed_by": actor,
        "owner": review.get("owner", ""),
        "resource_budget": review.get("resource_budget", ""),
        "timeline": review.get("timeline", ""),
        "kill_criteria": review.get("kill_criteria", ""),
        "governance_signature": governance_signature,
        "artifact_hashes": [artifact_hash(path) for path in paths.values()],
        "boundary": "Human-governed research commitment; not novelty proof, peer review, or publishability proof.",
    }
