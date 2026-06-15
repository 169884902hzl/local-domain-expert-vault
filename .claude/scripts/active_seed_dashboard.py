"""Render a derived active-seed QA dashboard without changing promotion gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from baseline_table import baseline_execution_status, load_baseline_tables
from kb_common import safe_print
from manual_prior_art_review import completion_errors, load_payload, review_quality_errors
from research_agenda_common import slugify
from research_seed_v2_common import (
    agenda_v2_path,
    artifact_dir,
    artifact_hashes,
    candidate_id,
    ensure_v2_dirs,
    read_json,
    utc_now,
    write_json,
    write_run_artifact,
    write_text,
)
from research_governance_common import pilot_plan_dir


DASHBOARD_HASH_INPUTS = [
    "selected-candidates.json",
    "gemini-mutations.json",
    "manual-prior-art-review.json",
    "baseline-table.json",
    "novelty-scan.json",
    "claim-graph-snapshot.jsonl",
    "tension-map.json",
    "survival-decision.json",
]


def _final_candidates(run_date: str) -> dict[str, dict[str, Any]]:
    selected_path = artifact_dir(run_date) / "selected-candidates.json"
    if not selected_path.exists():
        return {}
    selected = read_json(selected_path).get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    by_parent = {str(item.get("parent_candidate_id")): item for item in mutations if isinstance(item, dict)}
    candidates: dict[str, dict[str, Any]] = {}
    for item in selected:
        if not isinstance(item, dict):
            continue
        final = by_parent.get(candidate_id(item), item)
        candidates[candidate_id(final)] = final
    return candidates


def _by_candidate(run_date: str, artifact_name: str, key: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / artifact_name
    if not path.exists():
        return {}
    payload = read_json(path)
    return {str(item.get("candidate_id")): item for item in payload.get(key, []) if isinstance(item, dict)}


def _manual_reviews(run_date: str) -> dict[str, dict[str, Any]]:
    return {str(item.get("candidate_id")): item for item in load_payload(run_date).get("reviews", []) if isinstance(item, dict)}


def _manual_status(review: dict[str, Any] | None) -> tuple[str, str]:
    if not review:
        return "missing", "missing"
    if review.get("review_status") != "completed" or review.get("is_template") is True:
        return "template", "template"
    decision = str(review.get("decision") or "")
    quality = "complete" if not review_quality_errors(review) else "incomplete"
    if decision == "allow_active_seed":
        return "completed_allow", quality
    if decision == "park":
        return "completed_park", quality
    if decision == "reject":
        return "completed_reject", quality
    if completion_errors(review):
        return "incomplete", quality
    return "incomplete", quality


def _novelty_cache_status(scan: dict[str, Any] | None) -> str:
    if not scan:
        return "missing"
    if scan.get("stale_external_novelty_cache") is True:
        return "stale"
    provider_results = scan.get("provider_results", {}) if isinstance(scan.get("provider_results"), dict) else {}
    statuses = [str(item.get("cache_status") or "missing") for item in provider_results.values() if isinstance(item, dict)]
    if "stale" in statuses:
        return "stale"
    if "fresh" in statuses:
        return "fresh"
    return "missing"


def _pilot_plan_status(candidate: dict[str, Any]) -> str:
    path = pilot_plan_dir(candidate_id(candidate)) / "pilot-plan.json"
    if not path.exists():
        return "missing"
    try:
        plan = read_json(path)
    except Exception:
        return "partial"
    required = ["metric", "baseline_implementation_path", "resource_budget"]
    if not all(str(plan.get(field, "")).strip() for field in required):
        return "partial"
    if plan.get("plan_status") == "ready" and plan.get("human_confirmed") is True:
        return "ready"
    return "draft"


def _current_state(decision: dict[str, Any] | None) -> str:
    if not decision:
        return "raw_candidate"
    action = str(decision.get("decision") or "")
    if action == "killed":
        return "killed"
    if action == "parked":
        return "parked"
    if action == "rescue":
        return "rescue"
    if decision.get("pilot_ready_allowed") is True:
        return "pilot_ready_candidate"
    if decision.get("active_seed_allowed") is True:
        return "active_seed_candidate"
    if decision.get("formal_rehearsal_allowed") is True:
        return "formal_rehearsal_candidate"
    return "seed_candidate"


def _evidence_anchor_status(risks: set[str]) -> str:
    if "anchorless_core_evidence_risk" in risks:
        return "anchorless"
    if "result_row_unconfirmed" in risks:
        return "result_row_unconfirmed"
    return "anchored"


def _result_row_status(risks: set[str]) -> str:
    return "unconfirmed" if "result_row_unconfirmed" in risks else "not_used_or_confirmed"


def _cross_paper_edge_status(risks: set[str]) -> str:
    return "requires_human_check" if "cross_paper_edge_requires_human_check" in risks else "not_used_or_confirmed"


def build_dashboard(run_date: str) -> dict[str, Any]:
    candidates = _final_candidates(run_date)
    decisions = _by_candidate(run_date, "survival-decision.json", "decisions")
    novelty = _by_candidate(run_date, "novelty-scan.json", "scans")
    manual = _manual_reviews(run_date)
    baselines = load_baseline_tables(run_date)
    rows: list[dict[str, Any]] = []
    all_ids = sorted(set(candidates) | set(decisions) | set(manual) | set(baselines))
    for cid in all_ids:
        candidate = candidates.get(cid, {})
        decision = decisions.get(cid, {})
        risks = set(str(item) for item in decision.get("risks", []) if item)
        blocks = [str(item) for item in decision.get("blocks", []) if item]
        review_status, quality_status = _manual_status(manual.get(cid))
        baseline = baselines.get(cid)
        baseline_status = str((baseline or {}).get("baseline_verification_status") or "missing")
        scan = novelty.get(cid)
        rows.append(
            {
                "candidate_id": cid,
                "title": str(candidate.get("title") or decision.get("candidate_title") or ""),
                "current_state": _current_state(decision),
                "formal_rehearsal_allowed": bool(decision.get("formal_rehearsal_allowed", False)),
                "active_seed_allowed": bool(decision.get("active_seed_allowed", False)),
                "pilot_ready_allowed": bool(decision.get("pilot_ready_allowed", False)),
                "manual_prior_art_status": review_status,
                "manual_review_quality_status": quality_status,
                "baseline_verification_status": baseline_status,
                "baseline_execution_status": baseline_execution_status(baseline),
                "novelty_scope": str((scan or {}).get("verification_scope") or "missing"),
                "novelty_cache_status": _novelty_cache_status(scan),
                "evidence_anchor_status": _evidence_anchor_status(risks),
                "result_row_status": _result_row_status(risks),
                "cross_paper_edge_status": _cross_paper_edge_status(risks),
                "pilot_plan_status": _pilot_plan_status(candidate) if candidate else "missing",
                "risk_markers": sorted(risks),
                "blocking_reasons": blocks or (sorted(risks) if decision.get("active_seed_allowed") is not True else []),
            }
        )
    return {
        "schema_version": "active_seed_dashboard.v1",
        "run_date": run_date,
        "generated_at": utc_now(),
        "source_of_truth": "derived_view_only",
        "rows": rows,
        "source_artifact_hashes": artifact_hashes(run_date, DASHBOARD_HASH_INPUTS),
        "boundary": "Derived dashboard only; survival_decision, validation, publish, and audit remain gate sources.",
    }


def _status_from_accepted_risks(risks: set[str]) -> tuple[str, str, str, str]:
    manual_status = "missing" if "manual_prior_art_review_missing" in risks else "not_blocked"
    manual_quality = "incomplete" if "manual_prior_art_quality_incomplete" in risks or "manual_prior_art_query_log_missing" in risks else "not_blocked"
    if "baseline_table_missing" in risks:
        baseline_verification = "missing"
        baseline_execution = "unknown"
    elif "strongest_baseline_unknown" in risks:
        baseline_verification = "partial"
        baseline_execution = "unknown"
    elif "baseline_execution_not_ready" in risks:
        baseline_verification = "present"
        baseline_execution = "partial"
    else:
        baseline_verification = "not_blocked"
        baseline_execution = "not_blocked"
    return manual_status, manual_quality, baseline_verification, baseline_execution


def iter_accepted_payloads() -> list[tuple[dict[str, Any], Path]]:
    accepted_root = agenda_v2_path("seed-candidates", "accepted")
    if not accepted_root.exists():
        return []
    payloads: list[tuple[dict[str, Any], Path]] = []
    for path in sorted(accepted_root.rglob("*.json")):
        payload = read_json(path)
        if isinstance(payload, dict) and isinstance(payload.get("survival_decision"), dict):
            payloads.append((payload, path))
    return payloads


def build_accepted_backlog() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for payload, path in iter_accepted_payloads():
        decision = payload.get("survival_decision", {})
        candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
        cid = str(decision.get("candidate_id") or payload.get("candidate_id") or candidate.get("candidate_id") or "")
        if not cid:
            continue
        risks = {str(item) for item in decision.get("risks", []) if item}
        blocks = [str(item) for item in decision.get("blocks", []) if item]
        manual_status, manual_quality, baseline_verification, baseline_execution = _status_from_accepted_risks(risks)
        source = str(path.relative_to(agenda_v2_path())).replace("\\", "/")
        row_candidate = {"candidate_id": cid, "title": str(candidate.get("title") or decision.get("candidate_title") or cid)}
        rows.append(
            {
                "candidate_id": cid,
                "title": str(candidate.get("title") or decision.get("candidate_title") or ""),
                "accepted_source": source,
                "run_date": str(payload.get("run_date") or decision.get("run_date") or path.parent.name),
                "current_state": _current_state(decision),
                "formal_rehearsal_allowed": bool(decision.get("formal_rehearsal_allowed", False)),
                "active_seed_allowed": bool(decision.get("active_seed_allowed", False)),
                "pilot_ready_allowed": bool(decision.get("pilot_ready_allowed", False)),
                "manual_prior_art_status": manual_status,
                "manual_review_quality_status": manual_quality,
                "baseline_verification_status": baseline_verification,
                "baseline_execution_status": baseline_execution,
                "novelty_scope": str(decision.get("verification_scope") or "missing"),
                "novelty_cache_status": "stale" if "stale_external_novelty_cache" in risks else "not_blocked",
                "evidence_anchor_status": _evidence_anchor_status(risks),
                "result_row_status": _result_row_status(risks),
                "cross_paper_edge_status": _cross_paper_edge_status(risks),
                "pilot_plan_status": _pilot_plan_status(row_candidate),
                "risk_markers": sorted(risks),
                "blocking_reasons": blocks or sorted(risks),
            }
        )
    return {
        "schema_version": "accepted_backlog_dashboard.v1",
        "run_date": "accepted-backlog",
        "generated_at": utc_now(),
        "source_of_truth": "derived_view_only",
        "rows": rows,
        "boundary": "Accepted backlog dashboard is diagnostic only and cannot promote seeds or satisfy governance evidence gates.",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Active Seed Dashboard - {payload['run_date']}",
        "",
        "- source_of_truth: `derived_view_only`",
        "- boundary: dashboard is diagnostic and cannot promote seeds",
        "",
        "| candidate | state | active | pilot | manual QA | baseline exec | novelty cache | risks |",
        "|---|---|---:|---:|---|---|---|---|",
    ]
    for row in payload.get("rows", []):
        risks = ", ".join(row.get("risk_markers", []))
        lines.append(
            "| `{candidate_id}` | {state} | {active} | {pilot} | {manual}/{quality} | {baseline} | {cache} | {risks} |".format(
                candidate_id=row.get("candidate_id", ""),
                state=row.get("current_state", ""),
                active=str(row.get("active_seed_allowed", False)).lower(),
                pilot=str(row.get("pilot_ready_allowed", False)).lower(),
                manual=row.get("manual_prior_art_status", ""),
                quality=row.get("manual_review_quality_status", ""),
                baseline=row.get("baseline_execution_status", ""),
                cache=row.get("novelty_cache_status", ""),
                risks=risks,
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def write_dashboard(run_date: str, *, latest: bool = True, dry_run: bool = False) -> dict[str, Any]:
    ensure_v2_dirs(run_date)
    payload = build_dashboard(run_date)
    write_json(artifact_dir(run_date) / "active-seed-dashboard.json", payload, dry_run=dry_run)
    write_text(artifact_dir(run_date) / "active-seed-dashboard.md", render_markdown(payload), dry_run=dry_run)
    if latest:
        write_json(agenda_v2_path("dashboard", "active-seed-dashboard.json"), payload, dry_run=dry_run)
        write_text(agenda_v2_path("dashboard", "active-seed-dashboard.md"), render_markdown(payload), dry_run=dry_run)
    return payload


def write_accepted_backlog(*, dry_run: bool = False) -> dict[str, Any]:
    ensure_v2_dirs()
    payload = build_accepted_backlog()
    write_json(agenda_v2_path("dashboard", "accepted-backlog.json"), payload, dry_run=dry_run)
    write_text(agenda_v2_path("dashboard", "accepted-backlog.md"), render_markdown(payload), dry_run=dry_run)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--no-latest", action="store_true")
    parser.add_argument("--accepted-backlog", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.accepted_backlog:
        payload = write_accepted_backlog(dry_run=args.dry_run)
        safe_print(json.dumps({"rows": len(payload["rows"]), "view": "accepted-backlog"}, ensure_ascii=False, sort_keys=True))
        return 0
    payload = write_dashboard(args.run_date, latest=not args.no_latest, dry_run=args.dry_run)
    safe_print(json.dumps({"run_date": args.run_date, "rows": len(payload["rows"])}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
