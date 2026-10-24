"""Write proposed v2/v1 strategy review events without weakening hard gates."""
from __future__ import annotations

import argparse
import json
from datetime import date
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import HARD_GATE_FIELDS, agenda_v2_path, ensure_v2_dirs, read_json, utc_now, write_json


ALLOWED_OVERRIDE_KEYS = {
    "intake_bias",
    "intake_weights",
    "lane_quota",
    "prompt_emphasis",
    "resurrection_queue",
    "resurrection_candidates",
    "manual_prior_art_queue",
    "pdf_evidence_queue",
    "baseline_table_queue",
    "baseline_execution_queue",
    "active_seed_qa_queue",
    "result_row_confirmation_queue",
    "cross_paper_edge_audit_queue",
    "pilot_candidate_queue",
}
FORBIDDEN_OVERRIDE_KEYS = {
    "disable_novelty_gate",
    "allow_unknown_novelty_seed",
    "disable_deepseek",
    "codex_accept_not_required",
    "allow_anchorless_formal_seed",
    "allow_stale_external_cache",
    "allow_codex_reject",
}


def sanitize_overrides(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    safe: dict[str, Any] = {
        "schema_version": "strategy_overrides.v1",
        "updated_at": utc_now(),
        "allowed_keys": sorted(ALLOWED_OVERRIDE_KEYS),
        "hard_gates": HARD_GATE_FIELDS,
        "overrides": {},
    }
    for key, value in payload.items():
        if key in HARD_GATE_FIELDS or key in FORBIDDEN_OVERRIDE_KEYS:
            errors.append(f"attempted_hard_gate_override:{key}")
            continue
        if key not in ALLOWED_OVERRIDE_KEYS:
            errors.append(f"unsupported_strategy_override:{key}")
            continue
        safe["overrides"][key] = value
    return safe, errors


def _week_id(run_date: str) -> str:
    day = date.fromisoformat(run_date)
    year, week, _weekday = day.isocalendar()
    return f"{year}-W{week:02d}"


def _queue_item(candidate_id: str, reason: str, source: str) -> dict[str, str]:
    return {"candidate_id": candidate_id, "reason": reason, "source": source}


def _empty_queues() -> dict[str, list[dict[str, str]]]:
    return {
        "external_novelty_unknown": [],
        "anchorless_evidence": [],
        "codex_rewrite_or_reject": [],
        "breakthrough_speculative": [],
        "manual_prior_art_queue": [],
        "pdf_evidence_queue": [],
        "baseline_table_queue": [],
        "baseline_execution_queue": [],
        "active_seed_qa_queue": [],
        "result_row_confirmation_queue": [],
        "cross_paper_edge_audit_queue": [],
        "pilot_candidate_queue": [],
    }


def _append_queue(queues: dict[str, list[dict[str, str]]], queue: str, candidate_id: str, reason: str, source: str) -> None:
    if source.startswith("accepted:"):
        queues[queue] = [item for item in queues[queue] if item.get("candidate_id") != candidate_id]
    elif any(item.get("candidate_id") == candidate_id for item in queues[queue]):
        return
    queues[queue].append(_queue_item(candidate_id, reason, source))


def route_decision(item: dict[str, Any], source_label: str, queues: dict[str, list[dict[str, str]]]) -> None:
    cid = str(item.get("candidate_id"))
    risks = {str(risk) for risk in item.get("risks", [])}
    blocks = {str(block) for block in item.get("blocks", [])}
    if "unknown_novelty_without_human_override" in blocks or item.get("novelty_classification") == "unknown":
        _append_queue(queues, "external_novelty_unknown", cid, "external novelty unknown", source_label)
    if "anchorless_core_evidence_risk" in risks:
        _append_queue(queues, "anchorless_evidence", cid, "anchorless core evidence", source_label)
        _append_queue(queues, "pdf_evidence_queue", cid, "needs deeper PDF/table evidence extraction", source_label)
    if str(item.get("codex_action", "")).startswith(("rewrite", "reject", "park")):
        _append_queue(queues, "codex_rewrite_or_reject", cid, "Codex requested rewrite/reject/park", source_label)
    if "manual_prior_art_review_missing" in risks:
        _append_queue(queues, "manual_prior_art_queue", cid, "needs manual prior-art review", source_label)
    if "manual_prior_art_quality_incomplete" in risks or "manual_prior_art_query_log_missing" in risks:
        _append_queue(queues, "active_seed_qa_queue", cid, "needs manual prior-art quality completion", source_label)
        _append_queue(queues, "manual_prior_art_queue", cid, "needs manual prior-art QA checklist/query log", source_label)
    if "strongest_baseline_unknown" in risks or "baseline_table_missing" in risks:
        _append_queue(queues, "baseline_table_queue", cid, "needs baseline table or strongest baseline judgment", source_label)
    if "baseline_execution_not_ready" in risks:
        _append_queue(queues, "baseline_execution_queue", cid, "needs baseline execution readiness", source_label)
    if "result_row_unconfirmed" in risks:
        _append_queue(queues, "result_row_confirmation_queue", cid, "needs manual result-row confirmation", source_label)
    if "cross_paper_edge_requires_human_check" in risks:
        _append_queue(queues, "cross_paper_edge_audit_queue", cid, "needs cross-paper edge audit", source_label)
    if item.get("decision") == "accept_for_user_review" or "active_seed_without_pilot_plan" in risks:
        _append_queue(queues, "pilot_candidate_queue", cid, "accepted candidate needs experiment or pilot draft triage", source_label)


def iter_accepted_decisions() -> list[tuple[dict[str, Any], str]]:
    accepted_root = agenda_v2_path("seed-candidates", "accepted")
    if not accepted_root.exists():
        return []
    items: list[tuple[dict[str, Any], str]] = []
    for path in sorted(accepted_root.rglob("*.json")):
        payload = read_json(path)
        decision = payload.get("survival_decision", {})
        if not isinstance(decision, dict) or not decision.get("candidate_id"):
            continue
        source = "accepted:" + str(path.relative_to(agenda_v2_path())).replace("\\", "/")
        items.append((decision, source))
    return items


def build_resurrection_review(run_date: str) -> dict[str, Any]:
    run_artifacts = agenda_v2_path("runs", run_date, "artifacts")
    queues = _empty_queues()
    survival_path = run_artifacts / "survival-decision.json"
    if survival_path.exists():
        for item in read_json(survival_path).get("decisions", []):
            if not isinstance(item, dict):
                continue
            route_decision(item, "survival-decision.json", queues)
    for item, source in iter_accepted_decisions():
        route_decision(item, source, queues)
    selected_path = run_artifacts / "selected-candidates.json"
    if selected_path.exists():
        for item in read_json(selected_path).get("selected", []):
            if isinstance(item, dict) and item.get("lane") == "breakthrough_speculative":
                queues["breakthrough_speculative"].append(_queue_item(str(item.get("candidate_id", "")), "breakthrough speculative lane", "selected-candidates.json"))
    return {
        "schema_version": "resurrection_review.v1",
        "run_date": run_date,
        "week_id": _week_id(run_date),
        "queues": queues,
        "hard_gate_boundary": "Weekly review may queue work but cannot weaken novelty, DeepSeek, Codex, cache, baseline, or evidence gates.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-json", default="", help="Optional JSON object with strategy override keys.")
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs()
    review = build_resurrection_review(args.run_date)
    payload = json.loads(args.input_json) if args.input_json else {
        "resurrection_queue": review["queues"]["external_novelty_unknown"] + review["queues"]["anchorless_evidence"],
        "manual_prior_art_queue": review["queues"]["manual_prior_art_queue"],
        "pdf_evidence_queue": review["queues"]["pdf_evidence_queue"],
        "baseline_table_queue": review["queues"]["baseline_table_queue"],
        "baseline_execution_queue": review["queues"]["baseline_execution_queue"],
        "active_seed_qa_queue": review["queues"]["active_seed_qa_queue"],
        "result_row_confirmation_queue": review["queues"]["result_row_confirmation_queue"],
        "cross_paper_edge_audit_queue": review["queues"]["cross_paper_edge_audit_queue"],
        "pilot_candidate_queue": review["queues"]["pilot_candidate_queue"],
    }
    safe, errors = sanitize_overrides(payload)
    safe["run_date"] = args.run_date
    safe["week_id"] = _week_id(args.run_date)
    safe["validation_errors"] = errors
    safe["applied"] = False
    safe["requires_strategy_ledger_apply"] = True
    week_id = _week_id(args.run_date)
    write_json(agenda_v2_path("strategy", "weekly-overrides", f"{week_id}-strategy-overrides.proposed.json"), safe, dry_run=args.dry_run)
    write_json(agenda_v2_path("strategy", "resurrection-review", f"{week_id}.json"), review, dry_run=args.dry_run)
    safe_print(f"WEEKLY_STRATEGY_REVIEW: errors={len(errors)} overrides={len(safe['overrides'])}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
