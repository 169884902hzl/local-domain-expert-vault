"""Produce strict v2 scientific attack/rescue reviews for selected candidates."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from kb_common import safe_print
from opencode_cli_adapter import DEFAULT_OPENCODE_MODEL, run_opencode_cli
from research_seed_v2_common import artifact_dir, artifact_hashes, candidate_id, ensure_v2_dirs, read_json, write_json, write_run_artifact


REQUIRED_REVIEW_FIELDS = [
    "novelty_attack",
    "baseline_attack",
    "mechanism_attack",
    "evaluation_attack",
    "scope_attack",
    "a_plus_b_risk",
    "fatal_flaw",
    "rescue_mutation",
    "survivability_label",
    "allowed_next_stage",
]
OPTIONAL_EMPTY_REVIEW_FIELDS = {"fatal_flaw", "rescue_mutation"}
SURVIVABILITY_LABELS = {"survives", "survives_if_mutated", "park_for_unknown", "reject_with_rescue", "reject_fatal"}
ALLOWED_NEXT_STAGES = {"novelty_scan", "gemini_mutation", "parked", "rescue", "stop"}
A_PLUS_B_RISK = {"none", "low", "medium", "high", "fatal"}
DEFAULT_OPENCODE_BATCH_SIZE = 1
DEFAULT_OPENCODE_RETRIES = 2
PROVIDER_CANDIDATE_FIELDS = [
    "candidate_id",
    "title",
    "problem",
    "hypothesis",
    "claim_compression",
    "non_obvious_claim",
    "mechanism",
    "core_insight",
    "engineering_pathology",
    "interface",
    "interface_innovation",
    "strongest_baseline",
    "baseline_matrix",
    "baseline_kill_table",
    "anti_combination_test",
    "falsification",
    "killer_experiment",
    "minimum_no_hardware_pilot",
    "metric_suite",
    "negative_claim_boundary",
    "novelty_risk",
    "nearest_pressure",
    "competition_map",
    "lab_fit",
    "rescue_mutation",
    "post_kill_mutation",
    "risk_assumptions",
    "domains",
    "issues",
]


def _fallback_review_candidate(item: dict[str, Any]) -> dict[str, Any]:
    cid = candidate_id(item)
    text = " ".join(str(item.get(key, "")) for key in ["title", "problem", "mechanism", "interface", "strongest_baseline", "reviewer_kill_shot"]).lower()
    has_baseline = bool(str(item.get("strongest_baseline") or item.get("baseline_kill_table") or "").strip())
    has_pilot = bool(str(item.get("minimum_no_hardware_pilot") or item.get("pilot") or item.get("killer_experiment") or "").strip())
    fatal = ""
    if "impossible" in text or "fabricated" in text:
        fatal = "candidate_contains_impossible_or_fabricated_core_claim"
    elif not has_baseline:
        fatal = "missing_strongest_baseline"
    label = "survives"
    allowed = "novelty_scan"
    if fatal:
        label = "reject_fatal"
        allowed = "stop"
    elif not has_pilot:
        label = "survives_if_mutated"
        allowed = "gemini_mutation"
    return {
        "candidate_id": cid,
        "candidate_title": item.get("title", ""),
        "status": "failed_fallback_only",
        "novelty_attack": item.get("novelty_risk") or "nearest-prior overlap must be checked before promotion.",
        "baseline_attack": item.get("strongest_baseline") or "missing strongest baseline blocks promotion.",
        "mechanism_attack": item.get("reviewer_kill_shot") or "mechanism must isolate the causal variable rather than stack modules.",
        "evaluation_attack": item.get("killer_experiment") or "needs a falsifying no-hardware pilot and metric.",
        "scope_attack": item.get("negative_claim_boundary") or "scope must be narrowed to one interface or benchmark claim.",
        "a_plus_b_risk": "high" if "with" in text or "combine" in text else "low",
        "fatal_flaw": fatal,
        "rescue_mutation": item.get("rescue_mutation") or item.get("post_kill_mutation") or "",
        "survivability_label": label,
        "allowed_next_stage": allowed,
    }


def _load_provider_payload(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(path_value)
    if not path.exists():
        return {"_provider_error": f"provider_review_json_missing:{path}"}
    try:
        payload = read_json(path)
    except Exception as exc:
        return {"_provider_error": f"provider_review_json_invalid:{type(exc).__name__}:{exc}"}
    return payload if isinstance(payload, dict) else {"_provider_error": "provider_review_json_not_object"}


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


def _trim_provider_value(value: Any, *, limit: int = 1200) -> Any:
    if isinstance(value, str):
        text = value.strip()
        return text if len(text) <= limit else text[:limit] + "...[truncated]"
    if isinstance(value, list):
        return [_trim_provider_value(item, limit=limit) for item in value[:8]]
    if isinstance(value, dict):
        return {str(key): _trim_provider_value(item, limit=limit) for key, item in list(value.items())[:12]}
    return value


def _provider_candidate_view(item: dict[str, Any]) -> dict[str, Any]:
    view: dict[str, Any] = {"candidate_id": candidate_id(item)}
    for field in PROVIDER_CANDIDATE_FIELDS:
        if field == "candidate_id":
            continue
        value = item.get(field)
        if value not in (None, "", [], {}):
            view[field] = _trim_provider_value(value)

    evidence_items = item.get("evidence")
    if isinstance(evidence_items, list):
        view["evidence_excerpt"] = [
            {
                key: _trim_provider_value(record.get(key), limit=500)
                for key in ("claim_type", "source_title", "source_note", "statement")
                if isinstance(record, dict) and record.get(key)
            }
            for record in evidence_items[:6]
            if isinstance(record, dict)
        ]

    novelty_hits = item.get("novelty_hits")
    if isinstance(novelty_hits, list):
        view["novelty_hits_excerpt"] = [
            {
                key: _trim_provider_value(record.get(key), limit=300)
                for key in ("kind", "title", "source", "overlap_score")
                if isinstance(record, dict) and record.get(key) is not None
            }
            for record in novelty_hits[:6]
            if isinstance(record, dict)
        ]
    return view


def _provider_candidate_retry_view(item: dict[str, Any]) -> dict[str, Any]:
    view: dict[str, Any] = {"candidate_id": candidate_id(item)}
    for field in (
        "title",
        "problem",
        "hypothesis",
        "non_obvious_claim",
        "mechanism",
        "strongest_baseline",
        "falsification",
        "minimum_no_hardware_pilot",
        "novelty_risk",
        "nearest_pressure",
        "domains",
        "issues",
    ):
        value = item.get(field)
        if value not in (None, "", [], {}):
            view[field] = _trim_provider_value(value, limit=350)
    return view


def _render_opencode_prompt(
    selected: list[dict[str, Any]],
    *,
    run_date: str,
    retry_reason: str = "",
    previous_output: str = "",
    retry_compact: bool = False,
) -> str:
    candidates = [
        _provider_candidate_retry_view(item) if retry_compact else _provider_candidate_view(item)
        for item in selected
    ]
    if retry_compact:
        return json.dumps(
            {
                "task": (
                    "Return one raw JSON object only. No tools, no markdown. "
                    "Write one status=success review for each selected candidate_id."
                ),
                "schema_version": "deepseek_review.v1",
                "run_date": run_date,
                "retry_reason": retry_reason,
                "previous_invalid_output": previous_output[:300],
                "input_mode": "compact_retry",
                "required_review_fields": REQUIRED_REVIEW_FIELDS,
                "allowed_enums": {
                    "a_plus_b_risk": sorted(A_PLUS_B_RISK),
                    "survivability_label": sorted(SURVIVABILITY_LABELS),
                    "allowed_next_stage": sorted(ALLOWED_NEXT_STAGES),
                },
                "selected_candidates": candidates,
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    task = (
        "This is not a coding or implementation task; it is a research-candidate review serialization task. "
        "Do not run tools, inspect files, modify files, or start/cancel background tasks. "
        "Return strict JSON only. Do not use markdown fences or explanatory prose."
    )
    if retry_reason == "opencode_invalid_review_payload":
        task = (
            "Retry because the previous JSON did not contain exactly one valid review for every selected candidate_id. "
            "This is not a coding or implementation task; it is a research-candidate review serialization task. "
            "Do not run tools, inspect files, modify files, or start/cancel background tasks. "
            "Return exactly one raw JSON object with a reviews array containing one status=success review per selected candidate. "
            "Do not include markdown, commentary, analysis text, or code fences."
        )
    elif retry_reason:
        task = (
            "Retry because the previous provider output was not valid JSON. "
            "This is not a coding or implementation task; it is a research-candidate review serialization task. "
            "Do not run tools, inspect files, modify files, or start/cancel background tasks. "
            "Return exactly one raw JSON object starting with { and ending with }. "
            "Do not include markdown, commentary, analysis text, or code fences."
        )
    return json.dumps(
        {
            "task": task,
            "schema_version": "deepseek_review.v1",
            "run_date": run_date,
            "retry_reason": retry_reason,
            "previous_invalid_output": previous_output[:12000],
            "input_mode": "compact_retry" if retry_compact else "standard",
            "required_output_shape": {
                "schema_version": "deepseek_review.v1",
                "run_date": run_date,
                "status": "success",
                "provider_status": {
                    "provider": "deepseek",
                    "provider_backed": True,
                    "mode": "opencode",
                    "requested_model": "<filled_by_runner>",
                    "effective_model": "<filled_by_runner>",
                    "exit_code": 0,
                },
                "reviews": [
                    {
                        "candidate_id": "string",
                        "candidate_title": "string",
                        "status": "success",
                        "novelty_attack": "string",
                        "baseline_attack": "string",
                        "mechanism_attack": "string",
                        "evaluation_attack": "string",
                        "scope_attack": "string",
                        "a_plus_b_risk": "none|low|medium|high|fatal",
                        "fatal_flaw": "",
                        "rescue_mutation": "",
                        "survivability_label": "survives|survives_if_mutated|park_for_unknown|reject_with_rescue|reject_fatal",
                        "allowed_next_stage": "novelty_scan|gemini_mutation|parked|rescue|stop",
                    }
                ],
            },
            "validation_rules": [
                "Return exactly one review per candidate_id.",
                "Use status=success only when the review is substantive.",
                "fatal_flaw and rescue_mutation may be empty strings; every other required review field must be non-empty.",
                "Do not accept A+B combinations unless the mechanism survives baseline and evaluation attacks.",
            ],
            "selected_candidates": candidates,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _provider_error_payload(error: str, *, status: str, provider_status: dict[str, Any]) -> dict[str, Any]:
    return {
        "_provider_error": error,
        "_provider_failure_status": status,
        "_provider_status": {
            **provider_status,
            "provider": "deepseek",
            "provider_backed": False,
            "boundary": "Provider-backed success requires a completed external CLI call and validated JSON review.",
        },
    }


def _chunks(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    safe_size = max(1, size)
    return [items[index : index + safe_size] for index in range(0, len(items), safe_size)]


def _opencode_batch_cache_path(run_date: str, batch_index: int) -> Path:
    return artifact_dir(run_date) / "deepseek-review-batches" / f"batch-{batch_index:03d}.json"


def _load_opencode_batch_cache(selected: list[dict[str, Any]], *, run_date: str, batch_index: int) -> dict[str, Any] | None:
    path = _opencode_batch_cache_path(run_date, batch_index)
    if not path.exists():
        return None
    try:
        payload = read_json(path)
    except Exception:
        return None
    if payload.get("_provider_error"):
        return None
    errors = _validate_provider_reviews(selected, payload)
    provider_status = payload.get("provider_status", {})
    cached_ids = provider_status.get("batch_candidate_ids") or []
    expected_ids = [candidate_id(item) for item in selected]
    if errors or cached_ids != expected_ids or not provider_status.get("provider_backed"):
        return None
    payload["provider_status"] = {**dict(provider_status), "cache_hit": True}
    return payload


def _write_opencode_batch_cache(payload: dict[str, Any], *, run_date: str, batch_index: int) -> None:
    if payload.get("_provider_error"):
        return
    write_json(_opencode_batch_cache_path(run_date, batch_index), payload)


def _hydrate_provider_review_metadata(selected: list[dict[str, Any]], payload: dict[str, Any]) -> None:
    titles = {candidate_id(item): str(item.get("title") or item.get("candidate_title") or candidate_id(item)) for item in selected}
    for review in payload.get("reviews", []):
        if not isinstance(review, dict):
            continue
        cid = str(review.get("candidate_id") or "")
        if cid in titles and not str(review.get("candidate_title", "")).strip():
            review["candidate_title"] = titles[cid]


def _normalize_provider_payload_shape(payload: dict[str, Any]) -> dict[str, Any]:
    if "reviews" not in payload and payload.get("candidate_id"):
        return {"reviews": [payload]}
    return payload


def _opencode_provider_batch(
    selected: list[dict[str, Any]],
    *,
    run_date: str,
    model: str,
    timeout_sec: int,
    batch_index: int,
    retries: int = DEFAULT_OPENCODE_RETRIES,
) -> dict[str, Any]:
    attempt_count = max(1, retries + 1)
    attempt_statuses: list[dict[str, Any]] = []
    last_error_payload: dict[str, Any] | None = None
    retry_reason = ""
    previous_output = ""
    for attempt in range(1, attempt_count + 1):
        result = run_opencode_cli(
            _render_opencode_prompt(
                selected,
                run_date=run_date,
                retry_reason=retry_reason,
                previous_output=previous_output,
                retry_compact=attempt > 1,
            ),
            model=model,
            timeout_sec=timeout_sec,
            title=f"{run_date}-v2-deepseek-scientific-review-batch-{batch_index}-attempt-{attempt}",
        )
        status = {
            "mode": "opencode",
            "requested_model": model,
            "effective_model": result.get("effective_model") or model,
            "exit_code": result.get("exit_code"),
            "timed_out": bool(result.get("timed_out")),
            "event_count": result.get("event_count", 0),
            "batch_index": batch_index,
            "batch_size": len(selected),
            "batch_candidate_ids": [candidate_id(item) for item in selected],
            "attempt": attempt,
            "attempt_count": attempt_count,
        }
        attempt_statuses.append(dict(status))
        if result.get("timed_out"):
            status["attempt_statuses"] = attempt_statuses
            last_error_payload = _provider_error_payload(f"opencode_timeout:{timeout_sec}s", status="partial_provider_unavailable", provider_status=status)
            retry_reason = "opencode_timeout"
            continue
        if result.get("exit_code") != 0:
            status["attempt_statuses"] = attempt_statuses
            last_error_payload = _provider_error_payload(str(result.get("error") or f"opencode_nonzero_exit:{result.get('exit_code')}"), status="partial_provider_unavailable", provider_status=status)
            retry_reason = "opencode_nonzero_exit"
            continue
        try:
            payload = _extract_json_object(str(result.get("clean_output") or ""))
        except Exception as exc:
            previous_output = str(result.get("clean_output") or "")
            status["attempt_statuses"] = attempt_statuses
            status["clean_output_excerpt"] = previous_output[:500]
            last_error_payload = _provider_error_payload(f"opencode_invalid_json:{type(exc).__name__}:{exc}", status="partial_provider_invalid", provider_status=status)
            retry_reason = "opencode_invalid_json"
            continue
        payload = _normalize_provider_payload_shape(payload)
        payload["schema_version"] = "deepseek_review.v1"
        payload["run_date"] = run_date
        payload["status"] = "success"
        payload["provider_status"] = {
            **dict(payload.get("provider_status", {})),
            **status,
            "provider": "deepseek",
            "provider_backed": True,
            "attempt_statuses": attempt_statuses,
        }
        _hydrate_provider_review_metadata(selected, payload)
        validation_errors = _validate_provider_reviews(selected, payload)
        if validation_errors:
            previous_output = str(result.get("clean_output") or "")
            status["attempt_statuses"] = attempt_statuses
            status["validation_errors"] = validation_errors
            status["clean_output_excerpt"] = previous_output[:500]
            last_error_payload = _provider_error_payload(
                f"opencode_invalid_review_payload:{';'.join(validation_errors)}",
                status="partial_provider_invalid",
                provider_status=status,
            )
            retry_reason = "opencode_invalid_review_payload"
            continue
        return payload
    return last_error_payload or _provider_error_payload(
        "opencode_attempts_exhausted",
        status="partial_provider_unavailable",
        provider_status={
            "mode": "opencode",
            "requested_model": model,
            "effective_model": model,
            "exit_code": 1,
            "timed_out": False,
            "event_count": 0,
            "batch_index": batch_index,
            "batch_size": len(selected),
            "batch_candidate_ids": [candidate_id(item) for item in selected],
            "attempt_count": attempt_count,
            "attempt_statuses": attempt_statuses,
        },
    )


def _merge_opencode_provider_batches(
    selected: list[dict[str, Any]],
    *,
    run_date: str,
    model: str,
    batch_payloads: list[dict[str, Any]],
    batch_size: int,
) -> dict[str, Any]:
    batch_statuses = [dict(payload.get("_provider_status") or payload.get("provider_status") or {}) for payload in batch_payloads]
    failures = [payload for payload in batch_payloads if payload.get("_provider_error")]
    if failures:
        failure = failures[0]
        failure_status = str(failure.get("_provider_failure_status") or "partial_provider_unavailable")
        provider_status = {
            "mode": "opencode",
            "requested_model": model,
            "effective_model": model,
            "exit_code": 1,
            "timed_out": any(bool(status.get("timed_out")) for status in batch_statuses),
            "event_count": sum(int(status.get("event_count") or 0) for status in batch_statuses),
            "batch_count": len(batch_payloads),
            "batch_size": batch_size,
            "batch_statuses": batch_statuses,
        }
        return _provider_error_payload(
            f"opencode_batch_failed:{failure.get('_provider_error')}",
            status=failure_status,
            provider_status=provider_status,
        )

    reviews: list[dict[str, Any]] = []
    for payload in batch_payloads:
        reviews.extend([item for item in payload.get("reviews", []) if isinstance(item, dict)])
    return {
        "schema_version": "deepseek_review.v1",
        "run_date": run_date,
        "status": "success",
        "provider_status": {
            "provider": "deepseek",
            "provider_backed": True,
            "mode": "opencode",
            "requested_model": model,
            "effective_model": model,
            "exit_code": 0,
            "timed_out": False,
            "event_count": sum(int(status.get("event_count") or 0) for status in batch_statuses),
            "batch_count": len(batch_payloads),
            "batch_size": batch_size,
            "batch_statuses": batch_statuses,
            "batch_candidate_ids": [candidate_id(item) for item in selected],
        },
        "reviews": reviews,
    }


def _opencode_provider_payload(
    selected: list[dict[str, Any]],
    *,
    run_date: str,
    model: str,
    timeout_sec: int,
    batch_size: int = DEFAULT_OPENCODE_BATCH_SIZE,
    retries: int = DEFAULT_OPENCODE_RETRIES,
) -> dict[str, Any]:
    if not selected:
        return {
            "schema_version": "deepseek_review.v1",
            "run_date": run_date,
            "status": "success",
            "provider_status": {
                "provider": "deepseek",
                "provider_backed": True,
                "mode": "opencode",
                "requested_model": model,
                "effective_model": model,
                "exit_code": 0,
                "batch_count": 0,
                "batch_size": max(1, batch_size),
            },
            "reviews": [],
        }
    batches = _chunks(selected, batch_size)
    payloads: list[dict[str, Any]] = []
    for index, batch in enumerate(batches, start=1):
        cached_payload = _load_opencode_batch_cache(batch, run_date=run_date, batch_index=index)
        if cached_payload is not None:
            payloads.append(cached_payload)
            continue
        payload = _opencode_provider_batch(
            batch,
            run_date=run_date,
            model=model,
            timeout_sec=timeout_sec,
            batch_index=index,
            retries=retries,
        )
        if not payload.get("_provider_error"):
            _write_opencode_batch_cache(payload, run_date=run_date, batch_index=index)
        payloads.append(payload)
    if len(payloads) == 1:
        payloads[0].setdefault("provider_status", {})
        payloads[0]["provider_status"].setdefault("batch_count", 1)
        payloads[0]["provider_status"].setdefault("batch_size", max(1, batch_size))
        return payloads[0]
    return _merge_opencode_provider_batches(
        selected,
        run_date=run_date,
        model=model,
        batch_payloads=payloads,
        batch_size=max(1, batch_size),
    )


def _validate_provider_reviews(selected: list[dict[str, Any]], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    provider = payload.get("provider_status", {})
    if not provider.get("provider_backed"):
        errors.append("provider_status_not_provider_backed")
    if provider.get("provider") != "deepseek":
        errors.append(f"provider_not_deepseek:{provider.get('provider')}")
    reviews = [item for item in payload.get("reviews", []) if isinstance(item, dict)]
    selected_ids = [candidate_id(item) for item in selected]
    seen: dict[str, int] = {}
    for review in reviews:
        cid = str(review.get("candidate_id"))
        seen[cid] = seen.get(cid, 0) + 1
        if cid not in selected_ids:
            errors.append(f"unexpected_provider_review:{cid}")
    for cid, count in seen.items():
        if count > 1:
            errors.append(f"duplicate_provider_review:{cid}")
    by_id = {str(item.get("candidate_id")): item for item in reviews}
    for item in selected:
        cid = candidate_id(item)
        review = by_id.get(cid)
        if not review:
            errors.append(f"missing_provider_review:{cid}")
            continue
        if review.get("status") != "success":
            errors.append(f"provider_review_not_success:{cid}:{review.get('status')}")
        for field in REQUIRED_REVIEW_FIELDS:
            if field not in review:
                errors.append(f"provider_review_missing_field:{cid}:{field}")
            elif field not in OPTIONAL_EMPTY_REVIEW_FIELDS and not str(review.get(field, "")).strip():
                errors.append(f"provider_review_empty_field:{cid}:{field}")
        if not str(review.get("candidate_title", "")).strip():
            errors.append(f"provider_review_empty_field:{cid}:candidate_title")
        if review.get("a_plus_b_risk") not in A_PLUS_B_RISK:
            errors.append(f"provider_review_invalid_a_plus_b_risk:{cid}:{review.get('a_plus_b_risk')}")
        if review.get("survivability_label") not in SURVIVABILITY_LABELS:
            errors.append(f"provider_review_invalid_survivability_label:{cid}:{review.get('survivability_label')}")
        if review.get("allowed_next_stage") not in ALLOWED_NEXT_STAGES:
            errors.append(f"provider_review_invalid_allowed_next_stage:{cid}:{review.get('allowed_next_stage')}")
    return errors


def build_payload(selected: list[dict[str, Any]], *, run_date: str, provider_payload: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
    provider_payload = provider_payload or {}
    if provider_payload and not provider_payload.get("_provider_error"):
        errors = _validate_provider_reviews(selected, provider_payload)
        status = "success" if not errors and selected else "partial_provider_invalid"
        provider_status = {**dict(provider_payload.get("provider_status", {})), "validation_errors": errors}
        if status != "success":
            provider_status["provider_backed"] = False
        payload = {
            "schema_version": "deepseek_review.v1",
            "run_date": run_date,
            "status": status,
            "reviews": provider_payload.get("reviews", []),
            "provider_status": provider_status,
            "artifact_hashes": artifact_hashes(run_date, ["selected-candidates.json"]),
        }
        return payload, 0 if status == "success" else 2

    reviews = [_fallback_review_candidate(item) for item in selected]
    provider_error = provider_payload.get("_provider_error", "deepseek_provider_unavailable")
    provider_status = provider_payload.get("_provider_status") or {
        "provider": "deepseek",
        "provider_backed": False,
        "mode": "deterministic_strict_local_adapter",
        "provider_error": provider_error,
        "boundary": "Fallback artifact only; survival_decision must not accept this as provider-backed success.",
    }
    provider_status["provider_error"] = provider_error
    payload = {
        "schema_version": "deepseek_review.v1",
        "run_date": run_date,
        "status": provider_payload.get("_provider_failure_status") or ("partial_provider_unavailable" if reviews else "partial_empty_selection"),
        "reviews": reviews,
        "provider_status": provider_status,
        "artifact_hashes": artifact_hashes(run_date, ["selected-candidates.json"]),
    }
    return payload, 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--provider", choices=["json", "opencode", "none"], default="json")
    parser.add_argument("--provider-review-json", default=os.environ.get("DEEPSEEK_REVIEW_JSON", ""))
    parser.add_argument("--model", default=DEFAULT_OPENCODE_MODEL)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--provider-batch-size", type=int, default=DEFAULT_OPENCODE_BATCH_SIZE)
    parser.add_argument("--provider-retries", type=int, default=DEFAULT_OPENCODE_RETRIES)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    selected = read_json(artifact_dir(args.run_date) / "selected-candidates.json").get("selected", [])
    if args.provider == "opencode":
        provider_payload = _opencode_provider_payload(
            selected,
            run_date=args.run_date,
            model=args.model,
            timeout_sec=args.timeout,
            batch_size=args.provider_batch_size,
            retries=args.provider_retries,
        )
    elif args.provider_review_json:
        provider_payload = _load_provider_payload(args.provider_review_json)
    else:
        provider_payload = {}
    payload, exit_code = build_payload(selected, run_date=args.run_date, provider_payload=provider_payload)
    write_run_artifact(args.run_date, "deepseek-review.json", payload, state="attacked_by_deepseek", dry_run=args.dry_run)
    safe_print(f"DEEPSEEK_REVIEW: status={payload['status']} reviews={len(payload['reviews'])}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
