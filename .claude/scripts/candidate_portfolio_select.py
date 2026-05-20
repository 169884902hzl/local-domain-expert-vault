"""Select a deterministic v2 review portfolio from raw candidates."""
from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from kb_common import safe_print
from research_seed_v2_common import artifact_dir, artifact_hashes, candidate_id, ensure_v2_dirs, read_json, write_run_artifact


LANE_ORDER = [
    "grounded_mechanism",
    "interface_or_control_boundary",
    "infrastructure_or_benchmark",
    "data_or_evaluation_protocol",
    "outside_analogy",
    "breakthrough_speculative",
]


def _score(item: dict[str, Any]) -> int:
    total = 0
    for key in ["research_quality_score", "sharpness_score", "evidence_execution_score", "support_score", "originality_score"]:
        try:
            total += int(item.get(key, 0))
        except (TypeError, ValueError):
            pass
    try:
        total -= int(item.get("ordinaryness_penalty", 0))
    except (TypeError, ValueError):
        pass
    return total


def _mechanism_family(item: dict[str, Any]) -> str:
    text = str(item.get("mechanism") or item.get("core_insight") or item.get("title") or "").lower()
    for token in ["diffusion", "tactile", "world", "memory", "residual", "benchmark", "sim", "control", "topology"]:
        if token in text:
            return token
    return "misc"


def select_portfolio(raw_candidates: list[dict[str, Any]], *, max_selected: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    failure_recovery = 0
    ranked = sorted(raw_candidates, key=_score, reverse=True)

    def can_take(item: dict[str, Any]) -> tuple[bool, str]:
        lane = str(item.get("lane") or "")
        if not item.get("supporting_nodes") and lane != "breakthrough_speculative" and not item.get("evidence_links"):
            return False, "zero_claim_candidate_non_speculative"
        if family_counts[_mechanism_family(item)] >= 2:
            return False, "same_mechanism_family_cap"
        is_failure = "failure" in str(item.get("origin_type", "")).lower() or "failure" in str(item.get("problem", "")).lower()
        if is_failure and failure_recovery >= 2:
            return False, "failure_recovery_cap"
        return True, "selected"

    for item in ranked:
        item = dict(item)
        item["candidate_id"] = candidate_id(item)
        if len(selected) >= max_selected:
            item["selection_status"] = "not_selected"
            item["selection_reason"] = "portfolio_limit"
            rejected.append(item)
            continue
        ok, reason = can_take(item)
        if ok:
            item["selection_status"] = "selected"
            item["selection_reason"] = reason
            selected.append(item)
            family_counts[_mechanism_family(item)] += 1
            if "failure" in str(item.get("origin_type", "")).lower() or "failure" in str(item.get("problem", "")).lower():
                failure_recovery += 1
        else:
            item["selection_status"] = "not_selected"
            item["selection_reason"] = reason
            rejected.append(item)

    selected_lanes = {str(item.get("lane")) for item in selected}
    for required in ["infrastructure_or_benchmark", "data_or_evaluation_protocol"]:
        if selected_lanes & {"infrastructure_or_benchmark", "data_or_evaluation_protocol"}:
            break
        replacement = next((item for item in rejected if item.get("lane") == required), None)
        if replacement and selected:
            dropped = selected.pop()
            dropped["selection_status"] = "not_selected"
            dropped["selection_reason"] = "replaced_for_infrastructure_or_evaluation_quota"
            rejected.append(dropped)
            replacement["selection_status"] = "selected"
            replacement["selection_reason"] = "infrastructure_or_evaluation_quota"
            selected.append(replacement)
            rejected = [item for item in rejected if item["candidate_id"] != replacement["candidate_id"]]
            break
    if not (selected_lanes & {"outside_analogy", "breakthrough_speculative"}):
        replacement = next((item for item in rejected if item.get("lane") in {"outside_analogy", "breakthrough_speculative"}), None)
        if replacement and selected:
            dropped = selected.pop()
            dropped["selection_status"] = "not_selected"
            dropped["selection_reason"] = "replaced_for_speculative_quota"
            rejected.append(dropped)
            replacement["selection_status"] = "selected"
            replacement["selection_reason"] = "outside_or_breakthrough_quota"
            selected.append(replacement)
            rejected = [item for item in rejected if item["candidate_id"] != replacement["candidate_id"]]
    return selected, rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--max-selected", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    raw = read_json(artifact_dir(args.run_date) / "raw-candidates.json")
    selected, rejected = select_portfolio(raw.get("candidates", []), max_selected=args.max_selected)
    payload = {
        "schema_version": "selected_candidates.v1",
        "run_date": args.run_date,
        "selected": selected,
        "rejected": rejected,
        "selection_rules": {
            "max_selected": args.max_selected,
            "max_failure_recovery": 2,
            "max_same_mechanism_family": 2,
            "requires_infrastructure_or_evaluation_if_available": True,
            "requires_outside_or_breakthrough_if_available": True,
        },
        "artifact_hashes": artifact_hashes(args.run_date, ["raw-candidates.json"]),
        "boundary": "Portfolio selection is deterministic triage only; it cannot publish formal seed.",
    }
    write_run_artifact(args.run_date, "selected-candidates.json", payload, state="portfolio_selected", dry_run=args.dry_run)
    safe_print(f"PORTFOLIO_SELECTED: selected={len(selected)} rejected={len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
