"""Create v2 intake triage and deep-read decisions from daily arXiv candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_seed_v2_common import ensure_v2_dirs, run_dir, write_run_artifact, write_text

RESEARCH_VALUE_LANES = [
    "vla_action_interface",
    "physical_feedback_contact",
    "sim_to_real_robustness",
    "dlo_bimanual_manipulation",
    "frontier_anomaly",
    "contradiction",
    "tool_infrastructure_gap",
    "benchmark_metric_gap",
    "negative_result",
    "outside_analogy",
    "local_lab_fit",
    "baseline_weakness",
    "pilot_feasibility",
]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            records.append(json.loads(raw))
    return records


def _score(item: dict[str, Any]) -> int:
    for key in ["quality_score", "score", "research_value_score"]:
        try:
            return int(item.get(key, 0))
        except (TypeError, ValueError):
            continue
    return 0


def _paper(item: dict[str, Any]) -> dict[str, Any]:
    paper = item.get("paper")
    return paper if isinstance(paper, dict) else item


def _paper_id(item: dict[str, Any]) -> str:
    paper = _paper(item)
    return str(item.get("arxiv_id") or item.get("id") or item.get("paper_id") or paper.get("arxiv_id") or paper.get("id") or "")


def _title(item: dict[str, Any]) -> str:
    return str(item.get("title") or _paper(item).get("title") or "")


def _summary(item: dict[str, Any]) -> str:
    return str(item.get("summary") or item.get("abstract") or _paper(item).get("summary") or _paper(item).get("abstract") or "")


def _research_value_lanes(item: dict[str, Any]) -> list[str]:
    text = " ".join([_title(item), _summary(item)]).lower()
    patterns = {
        "vla_action_interface": [
            "vla",
            "vision-language-action",
            "rl token",
            "action interface",
            "action head",
            "decoder boundary",
            "vla anchoring",
        ],
        "physical_feedback_contact": ["tactile", "force", "force-torque", "haptic", "contact-rich", "contact rich"],
        "sim_to_real_robustness": [
            "sim-to-real",
            "sim2real",
            "real-to-sim",
            "domain randomization",
            "robustness",
            "failure recovery",
            "out-of-distribution",
            "ood",
        ],
        "dlo_bimanual_manipulation": ["dlo", "deformable linear object", "rope", "cable", "bimanual", "dual-arm", "dual arm"],
        "frontier_anomaly": ["anomaly", "unexpected", "emergent", "surprising"],
        "contradiction": ["contradict", "challenge", "against", "limitation"],
        "tool_infrastructure_gap": ["tool", "infrastructure", "system", "pipeline"],
        "benchmark_metric_gap": ["benchmark", "metric", "evaluation", "dataset", "protocol"],
        "negative_result": ["negative result", "failure", "does not", "no improvement", "ablation"],
        "outside_analogy": ["biology", "medical", "material", "graphics", "language model"],
        "local_lab_fit": ["dlo", "cable", "rope", "bimanual", "tactile", "force", "vla", "rl token", "franka", "sim-to-real"],
        "baseline_weakness": ["baseline", "strongest", "comparison", "outperform"],
        "pilot_feasibility": ["pilot", "small-scale", "low-cost", "offline", "replay", "simulation"],
    }
    lanes = [lane for lane, tokens in patterns.items() if any(token in text for token in tokens)]
    return lanes or ["quota_gap"]


def _category(item: dict[str, Any]) -> str:
    paper = _paper(item)
    diversity = " ".join(str(value) for value in item.get("diversity_features", []) if value)
    text = " ".join(
        [
            _title(item),
            _summary(item),
            str(item.get("decision", "")),
            str(item.get("primary_category") or paper.get("primary_category") or ""),
            diversity,
        ]
    ).lower()
    if any(token in text for token in ["benchmark", "evaluation", "dataset", "metric"]):
        return "infrastructure_or_evaluation"
    if any(token in text for token in ["tactile", "force", "haptic", "contact"]):
        return "tactile_contact"
    if any(token in text for token in ["deformable", "rope", "cable", "dlo", "cloth"]):
        return "dlo_or_deformable"
    if any(token in text for token in ["world model", "vla", "vision-language", "foundation model"]):
        return "vla_world_model"
    return "general_robot_learning"


def build_triage(
    items: list[dict[str, Any]],
    *,
    run_date: str,
    target_deep_read: int,
    max_deep_read: int,
) -> dict[str, Any]:
    ranked = sorted(enumerate(items), key=lambda row: _score(row[1]), reverse=True)
    decisions: list[dict[str, Any]] = []
    selected_for_deep_read: list[dict[str, Any]] = []
    selected = 0
    seen_categories: set[str] = set()
    for index, (original_index, item) in enumerate(ranked):
        category = _category(item)
        lanes = _research_value_lanes(item)
        decision = "defer"
        reason = "below_daily_read_budget"
        if selected < max_deep_read and (selected < target_deep_read or category not in seen_categories or not set(lanes) <= seen_categories):
            decision = "deep_read"
            reason = "target_or_diversity_slot"
            selected += 1
            seen_categories.add(category)
            seen_categories.update(lanes)
        row = {
            "rank": index + 1,
            "original_index": original_index,
            "arxiv_id": _paper_id(item),
            "paper_id": _paper_id(item),
            "title": _title(item),
            "score": _score(item),
            "category": category,
            "research_value_lanes": lanes,
            "decision": decision,
            "reason": reason,
        }
        decisions.append(row)
        if decision == "deep_read":
            selected_for_deep_read.append(
                {
                    "rank": row["rank"],
                    "original_index": original_index,
                    "arxiv_id": row["arxiv_id"],
                    "title": row["title"],
                    "score": row["score"],
                    "category": category,
                    "research_value_lanes": lanes,
                    "reason": reason,
                }
            )
    lane_counts = {lane: 0 for lane in RESEARCH_VALUE_LANES}
    for row in decisions:
        for lane in row.get("research_value_lanes", []):
            if lane in lane_counts:
                lane_counts[lane] += 1
    return {
        "schema_version": "intake_triage.v1",
        "run_date": run_date,
        "target_deep_read": target_deep_read,
        "max_deep_read": max_deep_read,
        "decisions": decisions,
        "selected_for_deep_read": selected_for_deep_read,
        "research_value_policy": "quota_or_explicit_gap",
        "research_value_quota_counts": lane_counts,
        "research_value_quota_gaps": [lane for lane, count in lane_counts.items() if count == 0],
        "counts": {
            "input_candidates": len(items),
            "deep_read": sum(1 for item in decisions if item["decision"] == "deep_read"),
            "defer": sum(1 for item in decisions if item["decision"] == "defer"),
        },
        "artifact_hashes": {},
        "boundary": "Intake ranking only; no idea generation or formal seed write occurs here.",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Intake Triage - {payload['run_date']}",
        "",
        f"- schema_version: {payload['schema_version']}",
        f"- target_deep_read: {payload['target_deep_read']}",
        f"- max_deep_read: {payload['max_deep_read']}",
        f"- deep_read: {payload['counts']['deep_read']}",
        "",
        "## Deep Read",
        "",
    ]
    for item in payload["decisions"]:
        if item["decision"] == "deep_read":
            lines.append(f"- {item['score']:3d} `{item['category']}` {item['title']} ({item['paper_id']})")
    lines.extend(["", "## Deferred", ""])
    for item in payload["decisions"][:30]:
        if item["decision"] != "deep_read":
            lines.append(f"- {item['score']:3d} `{item['category']}` {item['title']} ({item['paper_id']})")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--candidates", default="")
    parser.add_argument("--target-deep-read", type=int, default=3)
    parser.add_argument("--max-deep-read", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    candidates = Path(args.candidates) if args.candidates else vault_path("projects", "arxiv-daily", f"{args.run_date}-candidates.jsonl")
    ensure_v2_dirs(args.run_date)
    payload = build_triage(
        _read_jsonl(candidates),
        run_date=args.run_date,
        target_deep_read=args.target_deep_read,
        max_deep_read=args.max_deep_read,
    )
    write_run_artifact(args.run_date, "intake-triage.json", payload, state="intake_triaged", dry_run=args.dry_run)
    write_text(run_dir(args.run_date) / "artifacts" / "intake-triage.md", render_markdown(payload), dry_run=args.dry_run)
    safe_print(f"INTAKE_TRIAGE: status=success deep_read={payload['counts']['deep_read']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
