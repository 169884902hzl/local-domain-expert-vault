"""Create v2 intake triage and deep-read decisions from daily arXiv candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_seed_v2_common import ensure_v2_dirs, run_dir, write_run_artifact, write_text


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


def _category(item: dict[str, Any]) -> str:
    text = " ".join(str(item.get(key, "")) for key in ["title", "summary", "decision", "primary_category"]).lower()
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
    ranked = sorted(items, key=_score, reverse=True)
    decisions: list[dict[str, Any]] = []
    selected = 0
    seen_categories: set[str] = set()
    for index, item in enumerate(ranked):
        category = _category(item)
        decision = "defer"
        reason = "below_daily_read_budget"
        if selected < max_deep_read and (selected < target_deep_read or category not in seen_categories):
            decision = "deep_read"
            reason = "target_or_diversity_slot"
            selected += 1
            seen_categories.add(category)
        decisions.append(
            {
                "rank": index + 1,
                "paper_id": str(item.get("arxiv_id") or item.get("id") or item.get("paper_id") or ""),
                "title": str(item.get("title") or ""),
                "score": _score(item),
                "category": category,
                "decision": decision,
                "reason": reason,
            }
        )
    return {
        "schema_version": "intake_triage.v1",
        "run_date": run_date,
        "target_deep_read": target_deep_read,
        "max_deep_read": max_deep_read,
        "decisions": decisions,
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
