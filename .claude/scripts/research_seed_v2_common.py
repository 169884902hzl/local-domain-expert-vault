"""Shared helpers for the v2 transactional research-seed state machine."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_agenda_common import AGENDA_ROOT, slugify


SCHEMA_ROOT = vault_path(".claude", "schemas", "research_seed_v2")
STATE_MACHINE_VERSION = "research_seed_state_machine.v2"
RUN_SCHEMA_VERSION = "research_run_manifest.v1"

ARTIFACT_SCHEMAS: dict[str, str] = {
    "intake-triage.json": "intake_triage.v1",
    "reading-summary.json": "reading_summary.v1",
    "paper-primitives-snapshot.jsonl": "paper_primitives.v1",
    "claim-graph-snapshot.jsonl": "research_claim_graph.v1",
    "tension-map.json": "tension_map.v1",
    "raw-candidates.json": "raw_candidate.v1",
    "selected-candidates.json": "selected_candidates.v1",
    "deepseek-review.json": "deepseek_review.v1",
    "gemini-mutations.json": "gemini_mutations.v1",
    "novelty-scan.json": "novelty_scan.v1",
    "codex-execution-review.json": "codex_execution_review.v1",
    "survival-decision.json": "survival_decision.v1",
    "publish-result.json": "publish_result.v1",
}

PUBLISH_REQUIRED_ARTIFACTS = [
    "selected-candidates.json",
    "deepseek-review.json",
    "novelty-scan.json",
    "codex-execution-review.json",
    "survival-decision.json",
]

FORMAL_SEED_REQUIRED_FILES = [
    "idea.md",
    "survival-decision.json",
    "deepseek-review.json",
    "novelty-scan.json",
    "codex-execution-review.json",
    "artifact-hashes.json",
]

HARD_GATE_FIELDS = {
    "allow_unknown_novelty_auto_promote": False,
    "allow_deepseek_fatal_flaw": False,
    "allow_codex_reject": False,
    "allow_anchorless_core_evidence": False,
}
V2_PUBLISH_POLICIES = {"disabled", "seed-candidates-only", "formal"}
DEFAULT_V2_PUBLISH_POLICY = "seed-candidates-only"


def agenda_root() -> Path:
    override = os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
    return Path(override).resolve() if override else AGENDA_ROOT


def agenda_v2_path(*parts: str) -> Path:
    return agenda_root().joinpath(*parts)


def run_dir(run_date: str) -> Path:
    return agenda_v2_path("runs", run_date)


def artifact_dir(run_date: str) -> Path:
    return run_dir(run_date) / "artifacts"


def publish_dir(run_date: str) -> Path:
    return run_dir(run_date) / "publish"


def logs_dir(run_date: str) -> Path:
    return run_dir(run_date) / "logs"


def tmp_dir(run_date: str) -> Path:
    return run_dir(run_date) / "tmp"


def v2_rel(path: Path) -> str:
    path = Path(path).resolve()
    roots = [agenda_root().resolve(), vault_path().resolve()]
    for root in roots:
        try:
            return str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
    return str(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_v2_dirs(run_date: str | None = None) -> None:
    root = agenda_root()
    for directory in [
        root / "paper-primitives",
        root / "evidence",
        root / "tensions",
        root / "greenhouse",
        root / "seed-candidates",
        root / "parked",
        root / "rescue",
        root / "overrides" / "human-overrides",
        root / "quarantine",
        root / "strategy",
        root / "pilots",
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    if run_date:
        for directory in [run_dir(run_date), artifact_dir(run_date), publish_dir(run_date), logs_dir(run_date), tmp_dir(run_date)]:
            directory.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, content: str, *, dry_run: bool = False) -> None:
    if dry_run:
        safe_print(f"DRY-RUN write: {v2_rel(path)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    safe_print(f"WRITE: {v2_rel(path)}")


def write_json(path: Path, payload: dict[str, Any], *, dry_run: bool = False) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", dry_run=dry_run)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        if raw.strip():
            records.append(json.loads(raw))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]], *, dry_run: bool = False) -> None:
    content = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    write_text(path, content, dry_run=dry_run)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def payload_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def artifact_hashes(run_date: str, artifact_names: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in artifact_names:
        path = artifact_dir(run_date) / name
        if path.exists():
            hashes[name] = file_sha256(path)
    return hashes


def schema_path(schema_version: str) -> Path:
    stem = schema_version.removesuffix(".v1").replace(".", "_")
    return SCHEMA_ROOT / f"{stem}.schema.json"


def _type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    return type(value).__name__


def validate_payload(payload: dict[str, Any], schema_version: str) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != schema_version:
        errors.append(f"schema_version_mismatch:expected={schema_version}:actual={payload.get('schema_version')}")
        return errors
    path = schema_path(schema_version)
    if not path.exists():
        errors.append(f"missing_schema:{v2_rel(path)}")
        return errors
    schema = read_json(path)
    for field in schema.get("required", []):
        if field not in payload:
            errors.append(f"missing_field:{field}")
    properties = schema.get("properties", {})
    for field, spec in properties.items():
        if field not in payload or "type" not in spec:
            continue
        allowed = spec["type"]
        allowed_types = allowed if isinstance(allowed, list) else [allowed]
        actual = _type_name(payload[field])
        if actual not in allowed_types:
            errors.append(f"type_mismatch:{field}:expected={allowed_types}:actual={actual}")
    return errors


def validate_json_file(path: Path, schema_version: str) -> list[str]:
    try:
        payload = read_json(path)
    except Exception as exc:
        return [f"invalid_json:{type(exc).__name__}:{exc}"]
    if not isinstance(payload, dict):
        return ["json_top_level_not_object"]
    return validate_payload(payload, schema_version)


def validate_jsonl_file(path: Path, schema_version: str) -> list[str]:
    errors: list[str] = []
    try:
        records = load_jsonl(path)
    except Exception as exc:
        return [f"invalid_jsonl:{type(exc).__name__}:{exc}"]
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict):
            errors.append(f"line_{index}:not_object")
            continue
        for issue in validate_payload(record, schema_version):
            errors.append(f"line_{index}:{issue}")
    return errors


def validate_artifact(run_date: str, artifact_name: str) -> list[str]:
    schema_version = ARTIFACT_SCHEMAS[artifact_name]
    path = artifact_dir(run_date) / artifact_name
    if not path.exists():
        return [f"missing_artifact:{artifact_name}"]
    if artifact_name.endswith(".jsonl"):
        return validate_jsonl_file(path, schema_version)
    return validate_json_file(path, schema_version)


def append_stage_event(run_date: str, stage: str, status: str, details: dict[str, Any] | None = None) -> None:
    ensure_v2_dirs(run_date)
    path = logs_dir(run_date) / "stage-events.jsonl"
    event = {
        "ts": utc_now(),
        "run_date": run_date,
        "stage": stage,
        "status": status,
        "details": details or {},
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def init_manifest(run_date: str, *, dry_run: bool = False, backfill_mode: str = "daily") -> dict[str, Any]:
    return init_manifest_with_policy(
        run_date,
        dry_run=dry_run,
        backfill_mode=backfill_mode,
        v2_publish_policy=DEFAULT_V2_PUBLISH_POLICY,
        formal_seed_publish_allowed=False,
        scheduled_daily_switched=False,
    )


def init_manifest_with_policy(
    run_date: str,
    *,
    dry_run: bool = False,
    backfill_mode: str = "daily",
    v2_publish_policy: str = DEFAULT_V2_PUBLISH_POLICY,
    formal_seed_publish_allowed: bool = False,
    scheduled_daily_switched: bool = False,
) -> dict[str, Any]:
    ensure_v2_dirs(run_date)
    if v2_publish_policy not in V2_PUBLISH_POLICIES:
        raise ValueError(f"invalid_v2_publish_policy:{v2_publish_policy}")
    path = run_dir(run_date) / "manifest.json"
    existing = read_json(path) if path.exists() else {}
    payload = {
        **existing,
        "schema_version": RUN_SCHEMA_VERSION,
        "state_machine_version": STATE_MACHINE_VERSION,
        "run_id": existing.get("run_id") or f"{run_date}-{payload_sha256({'run_date': run_date, 'created_at': utc_now()})[:10]}",
        "run_date": run_date,
        "created_at": existing.get("created_at") or utc_now(),
        "updated_at": utc_now(),
        "backfill_mode": backfill_mode,
        "v2_publish_policy": v2_publish_policy,
        "formal_seed_publish_allowed": bool(formal_seed_publish_allowed),
        "scheduled_daily_switched": bool(scheduled_daily_switched),
        "formal_seed_written": bool(existing.get("formal_seed_written", False)),
        "states": existing.get("states", []),
        "boundary": "v2 transactional research-seed run; legacy same-day outputs are not formal v2 seed artifacts.",
    }
    write_json(path, payload, dry_run=dry_run)
    return payload


def mark_state(run_date: str, state: str, artifact: str, *, dry_run: bool = False) -> None:
    path = run_dir(run_date) / "manifest.json"
    manifest = read_json(path) if path.exists() else init_manifest(run_date, dry_run=dry_run)
    states = [item for item in manifest.get("states", []) if item.get("state") != state]
    states.append({"state": state, "artifact": artifact, "ts": utc_now()})
    manifest["states"] = states
    manifest["updated_at"] = utc_now()
    write_json(path, manifest, dry_run=dry_run)


def normalize_text(value: Any) -> str:
    text = str(value or "").lower()
    text = re.sub(r"\W+", " ", text)
    return " ".join(text.split())


def candidate_id(candidate: dict[str, Any], *, prefix: str = "cand") -> str:
    existing = str(candidate.get("candidate_id") or "").strip()
    if existing:
        return existing
    basis = "|".join(
        normalize_text(candidate.get(key, ""))
        for key in ["title", "problem", "mechanism", "interface", "strongest_baseline"]
    )
    slug = slugify(str(candidate.get("title") or "candidate"), max_len=44)
    return f"{prefix}-{slug}-{hashlib.sha1(basis.encode('utf-8')).hexdigest()[:10]}"


def candidate_fingerprint(candidate: dict[str, Any]) -> str:
    basis = "".join(
        normalize_text(candidate.get(key, ""))
        for key in [
            "problem",
            "mechanism",
            "interface",
            "interface_boundary",
            "strongest_baseline",
            "novelty_remaining_delta",
        ]
    )
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def seed_like_roots() -> list[Path]:
    root = agenda_root()
    return [
        root / "idea_bank" / "seed",
        root / "seed-candidates",
        root / "parked",
        root / "rescue",
        root / "greenhouse",
    ]


def duplicate_guard(candidate: dict[str, Any]) -> dict[str, Any]:
    fingerprint = candidate_fingerprint(candidate)
    title_norm = normalize_text(candidate.get("title", ""))
    nearest: list[dict[str, str]] = []
    for root in seed_like_roots():
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if fingerprint and fingerprint in text:
                nearest.append({"path": v2_rel(path), "reason": "fingerprint_match"})
            elif title_norm and title_norm in normalize_text(text[:4000]):
                nearest.append({"path": v2_rel(path), "reason": "title_overlap"})
            if len(nearest) >= 5:
                break
        if len(nearest) >= 5:
            break
    if nearest:
        return {
            "status": "possible_duplicate",
            "fingerprint": fingerprint,
            "nearest_candidates": nearest,
            "action": "block",
        }
    return {"status": "pass", "fingerprint": fingerprint, "nearest_candidates": [], "action": "allow_with_lineage"}


def write_run_artifact(
    run_date: str,
    artifact_name: str,
    payload: dict[str, Any],
    *,
    state: str,
    dry_run: bool = False,
) -> Path:
    ensure_v2_dirs(run_date)
    expected = ARTIFACT_SCHEMAS[artifact_name]
    errors = validate_payload(payload, expected)
    if errors:
        append_stage_event(run_date, state, "partial_schema_blocked", {"artifact": artifact_name, "errors": errors})
        raise ValueError(";".join(errors))
    path = artifact_dir(run_date) / artifact_name
    write_json(path, payload, dry_run=dry_run)
    mark_state(run_date, state, f"artifacts/{artifact_name}", dry_run=dry_run)
    append_stage_event(run_date, state, "success", {"artifact": artifact_name})
    return path


def copy_json_artifact(src: Path, dst: Path, *, dry_run: bool = False) -> None:
    if dry_run:
        safe_print(f"DRY-RUN copy: {v2_rel(src)} -> {v2_rel(dst)}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
