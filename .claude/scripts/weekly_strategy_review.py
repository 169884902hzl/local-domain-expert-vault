"""Write safe v2 strategy overrides without weakening hard gates."""
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


def build_resurrection_review(run_date: str) -> dict[str, Any]:
    run_artifacts = agenda_v2_path("runs", run_date, "artifacts")
    queues = {
        "external_novelty_unknown": [],
        "anchorless_evidence": [],
        "codex_rewrite_or_reject": [],
        "breakthrough_speculative": [],
        "manual_prior_art_queue": [],
        "pdf_evidence_queue": [],
        "baseline_table_queue": [],
    }
    survival_path = run_artifacts / "survival-decision.json"
    if survival_path.exists():
        for item in read_json(survival_path).get("decisions", []):
            if not isinstance(item, dict):
                continue
            cid = str(item.get("candidate_id"))
            risks = {str(risk) for risk in item.get("risks", [])}
            blocks = {str(block) for block in item.get("blocks", [])}
            if "unknown_novelty_without_human_override" in blocks or item.get("novelty_classification") == "unknown":
                queues["external_novelty_unknown"].append(_queue_item(cid, "external novelty unknown", "survival-decision.json"))
            if "anchorless_core_evidence_risk" in risks:
                queues["anchorless_evidence"].append(_queue_item(cid, "anchorless core evidence", "survival-decision.json"))
                queues["pdf_evidence_queue"].append(_queue_item(cid, "needs deeper PDF/table evidence extraction", "survival-decision.json"))
            if str(item.get("codex_action", "")).startswith(("rewrite", "reject", "park")):
                queues["codex_rewrite_or_reject"].append(_queue_item(cid, "Codex requested rewrite/reject/park", "survival-decision.json"))
            if "manual_prior_art_review_missing" in risks:
                queues["manual_prior_art_queue"].append(_queue_item(cid, "needs manual prior-art review", "survival-decision.json"))
            if "strongest_baseline_unknown" in risks or "baseline_table_missing" in risks:
                queues["baseline_table_queue"].append(_queue_item(cid, "needs baseline table or strongest baseline judgment", "survival-decision.json"))
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
    }
    safe, errors = sanitize_overrides(payload)
    safe["run_date"] = args.run_date
    safe["week_id"] = _week_id(args.run_date)
    safe["validation_errors"] = errors
    week_id = _week_id(args.run_date)
    write_json(agenda_v2_path("strategy", "weekly-overrides", f"{week_id}-strategy-overrides.json"), safe, dry_run=args.dry_run)
    write_json(agenda_v2_path("strategy", "resurrection-review", f"{week_id}.json"), review, dry_run=args.dry_run)
    write_json(agenda_v2_path("strategy", "active-overrides.json"), safe, dry_run=args.dry_run)
    safe_print(f"WEEKLY_STRATEGY_REVIEW: errors={len(errors)} overrides={len(safe['overrides'])}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
