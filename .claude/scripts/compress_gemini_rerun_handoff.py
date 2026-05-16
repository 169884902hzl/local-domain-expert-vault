"""Compress historical Gemini rerun candidates into DeepThink handoff briefs.

This script is archive-only. It does not modify formal agenda deltas, seed
folders, Zotero records, or raw readings.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from gemini_cli_adapter import run_gemini_cli
from kb_common import safe_print, safe_write, vault_path
from research_agenda_common import REVIEWS_DIR, rel, render_frontmatter
from research_agenda_ideate import _extract_json_object


DEFAULT_RERUN_ROOT = vault_path(
    "projects",
    "research-agenda",
    "divergent-reruns",
    "2026-05-13-haptoken-v3-style-0429-0507",
)
DEFAULT_REVIEW_PACKET = vault_path(
    "projects",
    "research-agenda",
    "reviews",
    "2026-05-13-haptoken-v3-style-0429-0507-codex-review-packet.json",
)
DEFAULT_OUTPUT_ROOT = vault_path(
    "projects",
    "research-agenda",
    "divergent-reruns",
    "2026-05-13-haptoken-v3-style-0429-0507",
    "deepthink-handoff",
)
DEFAULT_MODEL = "gemini-3.1-pro-preview"
REQUIRED_HANDOFF_FIELDS = [
    "title",
    "title_zh",
    "source_candidate_titles",
    "handoff_summary_en",
    "handoff_summary_zh",
    "central_hypothesis",
    "physical_failure_scene",
    "engineering_pathology",
    "core_insight",
    "interface_innovation",
    "optimization_space",
    "why_not_a_b_combination",
    "strongest_baseline",
    "baseline_kill_table",
    "seventy_two_hour_kill_test",
    "what_deepthink_must_decide",
    "negative_claim_boundary",
    "minimum_no_hardware_pilot",
    "lab_fit",
    "dealbreaker_risks",
    "rescue_mutation",
    "recommended_action",
]
ALLOWED_ACTIONS = ["send_to_deepthink", "rewrite_once_more", "park"]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _candidate_key(item: dict[str, Any]) -> str:
    return "|".join(
        [
            str(item.get("run_date") or item.get("daily_run_date") or ""),
            str(item.get("rerun_group", "")),
            str(item.get("title", "")),
        ]
    )


def _merge_reviews(packet: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [item for item in packet.get("raw_gemini_candidates", []) if isinstance(item, dict)]
    reviews = [item for item in packet.get("candidate_reviews", []) if isinstance(item, dict)]
    review_by_key = {_candidate_key(item): item for item in reviews}
    merged: list[dict[str, Any]] = []
    for item in candidates:
        enriched = dict(item)
        review = review_by_key.get(_candidate_key(item), {})
        for key, value in review.items():
            if key not in enriched or enriched.get(key) in ("", None, []):
                enriched[key] = value
        if review:
            enriched["codex_review_action"] = review.get("review_action", "")
            enriched["codex_weekly_score"] = review.get("weekly_score", "")
        merged.append(enriched)
    return merged


def _selection_score(item: dict[str, Any]) -> int:
    score = _as_int(item.get("codex_weekly_score") or item.get("weekly_score")) * 10
    score += _as_int(item.get("research_quality_score"))
    tier = str(item.get("quality_tier", ""))
    score += {"S": 45, "A": 25, "B": 5}.get(tier, 0)
    action = str(item.get("codex_review_action") or item.get("review_action"))
    score += {"rewrite": 20, "park": -10, "reject_with_rescue": -30}.get(action, 0)
    if str(item.get("rerun_group")) == "free_divergence_current_standard":
        score += 8
    if str(item.get("candidate_group")) == "wild_engineering":
        score += 5
    if len(str(item.get("physical_failure_scene", ""))) >= 100:
        score += 5
    if len(str(item.get("interface_innovation", ""))) >= 80:
        score += 5
    if len(str(item.get("minimum_no_hardware_pilot", ""))) >= 70:
        score += 4
    if str(item.get("novelty_pressure", "")).lower().find("high") >= 0:
        score -= 4
    return score


def select_top_candidates(items: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        title = str(item.get("title", ""))
        if not title:
            continue
        contribution = str(item.get("contribution_shape") or item.get("idea_archetype") or "unknown")
        buckets.setdefault(contribution, []).append(item)
    for group in buckets.values():
        group.sort(key=lambda item: (_selection_score(item), str(item.get("title", ""))), reverse=True)

    selected: list[dict[str, Any]] = []
    for group in sorted(buckets.values(), key=lambda values: _selection_score(values[0]), reverse=True):
        if len(selected) >= limit:
            break
        selected.append(group[0])

    if len(selected) < limit:
        seen = {_candidate_key(item) for item in selected}
        all_items = sorted(items, key=lambda item: (_selection_score(item), str(item.get("title", ""))), reverse=True)
        for item in all_items:
            if len(selected) >= limit:
                break
            key = _candidate_key(item)
            if key in seen:
                continue
            selected.append(item)
            seen.add(key)
    return selected[:limit]


def _compact_candidate(item: dict[str, Any]) -> dict[str, Any]:
    fields = [
        "title",
        "run_date",
        "rerun_group",
        "candidate_group",
        "quality_tier",
        "research_quality_score",
        "codex_review_action",
        "codex_weekly_score",
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
        "non_obvious_claim",
        "anti_combination_test",
        "core_insight",
        "strongest_baseline",
        "baseline_kill_table",
        "killer_experiment",
        "reviewer_pre_mortem",
        "what_would_make_this_not_a_paper",
        "minimum_no_hardware_pilot",
        "negative_claim_boundary",
        "lab_fit",
        "risk_assumptions",
        "rescue_mutation",
        "novelty_pressure",
        "novelty_hits",
    ]
    return {field: item.get(field, "") for field in fields}


def render_prompt(selected: list[dict[str, Any]], *, output_count: int) -> str:
    packet = {
        "task": "Compress historical Gemini rerun ideas into a small DeepThink handoff set.",
        "role": "Severe Physical AI PhD advisor. Your job is not to invent more ideas; your job is to reduce reviewer workload.",
        "output_contract": {
            "format": "Return JSON only.",
            "top_level_key": "handoff_candidates",
            "candidate_count": f"Return {output_count} to {output_count + 2} handoff candidates.",
            "required_fields": REQUIRED_HANDOFF_FIELDS,
            "allowed_recommended_action": ALLOWED_ACTIONS,
        },
        "non_negotiable_rules": [
            "Do not output a raw A+B combination. If a candidate survives, it must be a research hypothesis centered on a physical failure mechanism.",
            "The central_hypothesis must follow this form: If physical pathology P is caused by bottleneck B, then interface/optimization change I should beat baseline X under kill test K.",
            "Start from the robot failure scene, not from method names.",
            "Merge near-duplicate candidates when they share the same pathology. Do not preserve separate names just because the original candidates were separate.",
            "Do not claim confirmed novelty, accepted paper quality, or experiment results.",
            "Prefer candidates that are painful for a reviewer to dismiss with a simple baseline.",
            "Use bilingual handoff summaries: English for technical precision, Chinese for fast human review.",
            "what_deepthink_must_decide should be the exact uncertainty GPT Pro or Gemini DeepThink should spend reasoning budget on.",
            "seventy_two_hour_kill_test must be the smallest offline or no-new-hardware test that can kill the idea quickly.",
            "recommended_action must be send_to_deepthink, rewrite_once_more, or park.",
        ],
        "quality_target": {
            "not_required": "It does not need to be paper-ready today.",
            "required": "It must be concrete enough that GPT Pro/DeepThink can focus on one mechanism instead of cleaning up a vague idea.",
            "avoid": [
                "generic RL Token framing",
                "generic VLA wrapper",
                "adding one input to a critic",
                "module swap without interface change",
                "sim-to-real claim without a specific measurable failure",
            ],
        },
        "selected_source_candidates": [_compact_candidate(item) for item in selected],
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def _normalize_handoff_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = payload.get("handoff_candidates")
    if not isinstance(value, list):
        value = payload.get("candidates")
    if not isinstance(value, list):
        return []
    normalized: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        row = {field: item.get(field, "") for field in REQUIRED_HANDOFF_FIELDS}
        for key, extra in item.items():
            if key not in row:
                row[key] = extra
        action = str(row.get("recommended_action") or "").strip()
        if action not in ALLOWED_ACTIONS:
            row["recommended_action"] = "rewrite_once_more"
        normalized.append(row)
    return normalized


def deterministic_fallback(selected: list[dict[str, Any]], *, output_count: int) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for item in selected[: output_count + 2]:
        title = str(item.get("title", "Untitled"))
        items.append(
            {
                "title": title,
                "title_zh": title,
                "source_candidate_titles": [title],
                "handoff_summary_en": str(item.get("claim_compression") or item.get("core_insight") or item.get("mechanism", "")),
                "handoff_summary_zh": "自动兜底摘要：该候选需要进一步重写后再交给高级模型审查。",
                "central_hypothesis": str(item.get("hypothesis") or item.get("non_obvious_claim", "")),
                "physical_failure_scene": item.get("physical_failure_scene", ""),
                "engineering_pathology": item.get("engineering_pathology", ""),
                "core_insight": item.get("core_insight", ""),
                "interface_innovation": item.get("interface_innovation", ""),
                "optimization_space": item.get("optimization_space", ""),
                "why_not_a_b_combination": item.get("anti_combination_test", ""),
                "strongest_baseline": item.get("strongest_baseline", ""),
                "baseline_kill_table": item.get("baseline_kill_table", ""),
                "seventy_two_hour_kill_test": item.get("minimum_no_hardware_pilot", ""),
                "what_deepthink_must_decide": item.get("reviewer_pre_mortem", ""),
                "negative_claim_boundary": item.get("negative_claim_boundary", ""),
                "minimum_no_hardware_pilot": item.get("minimum_no_hardware_pilot", ""),
                "lab_fit": item.get("lab_fit", ""),
                "dealbreaker_risks": item.get("what_would_make_this_not_a_paper", ""),
                "rescue_mutation": item.get("rescue_mutation", ""),
                "recommended_action": "rewrite_once_more",
                "fallback_source": "deterministic",
            }
        )
    return items


def _handoff_completeness(item: dict[str, Any]) -> tuple[int, list[str]]:
    missing = [field for field in REQUIRED_HANDOFF_FIELDS if not str(item.get(field, "")).strip()]
    return len(REQUIRED_HANDOFF_FIELDS) - len(missing), missing


def _review_handoff(item: dict[str, Any]) -> dict[str, Any]:
    score, missing = _handoff_completeness(item)
    central = str(item.get("central_hypothesis", "")).lower()
    anti_combination = str(item.get("why_not_a_b_combination", "")).lower()
    baseline = str(item.get("strongest_baseline", "")).lower()
    kill_test = str(item.get("seventy_two_hour_kill_test", "")).lower()
    lab_fit = str(item.get("lab_fit", "")).lower()
    has_hypothesis_form = len(central) >= 90 and "if" in central and "then" in central
    has_baseline = len(baseline) >= 30
    has_kill_test = len(kill_test) >= 70 and any(
        token in kill_test
        for token in ["if", "measure", "test", "offline", "analyze", "extract", "simulate", "sim", "验证", "测试"]
    )
    has_not_ab = len(anti_combination) >= 70 and any(
        token in anti_combination
        for token in [
            "not just",
            "rather than",
            "instead",
            "structural",
            "interface",
            "mechanism",
            "不是",
            "而不是",
            "因果",
            "接口",
        ]
    )
    has_lab_fit = any(
        token in lab_fit
        for token in ["franka", "flextac", "wrist", "dlo", "cable", "bimanual", "双臂", "腕部", "触觉", "dot-sim"]
    )
    lab_mismatch = any(token in lab_fit for token in ["low-cost", "aloh", "aharobot", "低成本"])
    action = "send_to_deepthink"
    reasons: list[str] = []
    if score < len(REQUIRED_HANDOFF_FIELDS) - 2:
        action = "rewrite_once_more"
        reasons.append("missing_required_handoff_fields")
    if not has_hypothesis_form:
        action = "rewrite_once_more"
        reasons.append("central_hypothesis_not_decision_shaped")
    if not has_baseline:
        action = "rewrite_once_more"
        reasons.append("strongest_baseline_missing")
    if not has_kill_test:
        action = "rewrite_once_more"
        reasons.append("kill_test_not_concrete")
    if not has_not_ab:
        action = "rewrite_once_more"
        reasons.append("anti_combination_boundary_weak")
    if not has_lab_fit and action == "send_to_deepthink":
        action = "rewrite_once_more"
        reasons.append("lab_fit_not_visible")
    if lab_mismatch:
        action = "rewrite_once_more"
        reasons.append("lab_fit_mismatch_check_needed")
    if str(item.get("recommended_action")) == "park":
        action = "park"
        reasons.append("gemini_recommended_park")
    return {
        "title": item.get("title", ""),
        "recommended_action": item.get("recommended_action", ""),
        "codex_handoff_action": action,
        "handoff_completeness": score,
        "missing_fields": missing,
        "review_reasons": reasons or ["ready_for_external_deep_review"],
    }


def rebuild_existing_handoff(*, source_root: Path, output_root: Path) -> dict[str, Any]:
    packet_path = output_root / f"{date.today().isoformat()}-deepthink-handoff-packet.json"
    md_path = output_root / f"{date.today().isoformat()}-deepthink-handoff.md"
    report_path = REVIEWS_DIR / f"{source_root.name}-deepthink-handoff-codex-review.md"
    output_packet = _read_json(packet_path)
    if not output_packet:
        return {"status": "missing_existing_packet", "packet_path": rel(packet_path)}
    selected = [
        item for item in output_packet.get("selected_source_candidates", [])
        if isinstance(item, dict)
    ]
    handoff_items = [
        item for item in output_packet.get("handoff_candidates", [])
        if isinstance(item, dict)
    ]
    reviews = [_review_handoff(item) for item in handoff_items]
    output_packet["codex_handoff_reviews"] = reviews
    output_packet["counts"] = {
        "selected_source_candidates": len(selected),
        "handoff_candidates": len(handoff_items),
        "codex_handoff_actions": dict(Counter(str(item.get("codex_handoff_action")) for item in reviews)),
    }
    gemini_status = output_packet.get("gemini_status", {})
    markdown = render_markdown(
        source_root=source_root,
        selected=selected,
        handoff_items=handoff_items,
        reviews=reviews,
        gemini_status=gemini_status if isinstance(gemini_status, dict) else {},
    )
    safe_write(packet_path, json.dumps(output_packet, ensure_ascii=False, indent=2) + "\n", backup=True)
    safe_write(md_path, markdown, backup=True)
    safe_write(report_path, markdown, backup=True)
    return {
        "status": "rebuilt_existing",
        "packet_path": rel(packet_path),
        "markdown_path": rel(md_path),
        "review_path": rel(report_path),
        "selected_source_candidates": len(selected),
        "handoff_candidates": len(handoff_items),
        "codex_handoff_actions": output_packet["counts"]["codex_handoff_actions"],
    }


def render_markdown(
    *,
    source_root: Path,
    selected: list[dict[str, Any]],
    handoff_items: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    gemini_status: dict[str, Any],
) -> str:
    action_counts = Counter(str(item.get("codex_handoff_action", "unreviewed")) for item in reviews)
    frontmatter = render_frontmatter(
        "DeepThink Handoff Compression - Historical Gemini Rerun",
        ["research-agenda", "gemini-rerun", "deepthink-handoff"],
        "Compressed historical Gemini rerun ideas into a small external-review handoff set.",
        status="done" if handoff_items else "partial",
    )
    lines = [
        frontmatter.rstrip(),
        "# DeepThink Handoff Compression",
        "",
        "## Executive Verdict",
        "",
        f"- source_root: {rel(source_root)}",
        f"- selected_source_candidates: {len(selected)}",
        f"- handoff_candidates: {len(handoff_items)}",
        f"- codex_handoff_actions: {json.dumps(dict(action_counts), ensure_ascii=False, sort_keys=True)}",
        f"- gemini_provider: {gemini_status.get('provider', '-')}",
        f"- gemini_effective_model: {gemini_status.get('effective_model', '-')}",
        f"- gemini_fallback: {gemini_status.get('effective_fallback', False)}",
        "- boundary: archive-only; no formal seed, agenda, Zotero record, or raw reading is changed.",
        "",
        "## Source Candidates",
        "",
    ]
    for item in selected:
        lines.append(
            f"- {item.get('run_date')} `{item.get('quality_tier')}` {item.get('title')} "
            f"[{item.get('rerun_group')}] score={_selection_score(item)}"
        )
    lines.extend(["", "## Handoff Candidates", ""])
    if not handoff_items:
        lines.append("- no handoff candidates generated.")
    review_by_title = {str(item.get("title")): item for item in reviews}
    for index, item in enumerate(handoff_items, 1):
        review = review_by_title.get(str(item.get("title")), {})
        lines.extend(
            [
                f"### {index}. {item.get('title')}",
                "",
                f"- 中文名: {item.get('title_zh')}",
                f"- action: `{review.get('codex_handoff_action', item.get('recommended_action', '-'))}`",
                f"- source_candidates: {', '.join(str(x) for x in item.get('source_candidate_titles', [])) if isinstance(item.get('source_candidate_titles'), list) else item.get('source_candidate_titles', '-')}",
                f"- EN: {item.get('handoff_summary_en')}",
                f"- ZH: {item.get('handoff_summary_zh')}",
                f"- central_hypothesis: {item.get('central_hypothesis')}",
                f"- physical_failure_scene: {item.get('physical_failure_scene')}",
                f"- core_insight: {item.get('core_insight')}",
                f"- interface_innovation: {item.get('interface_innovation')}",
                f"- strongest_baseline: {item.get('strongest_baseline')}",
                f"- 72h_kill_test: {item.get('seventy_two_hour_kill_test')}",
                f"- DeepThink question: {item.get('what_deepthink_must_decide')}",
                f"- risks: {item.get('dealbreaker_risks')}",
                f"- review_reasons: {', '.join(review.get('review_reasons', [])) if review else '-'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- This report reduces reviewer workload; it does not claim paper readiness.",
            "- `send_to_deepthink` only means the brief is concrete enough for external deep review.",
            "- User remains final reviewer before any formal seed promotion.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def compress_handoff(
    *,
    review_packet: Path,
    source_root: Path,
    output_root: Path,
    model: str,
    timeout_sec: int,
    top_k: int,
    output_count: int,
    dry_run: bool,
) -> dict[str, Any]:
    packet = _read_json(review_packet)
    merged = _merge_reviews(packet)
    selected = select_top_candidates(merged, limit=top_k)
    output_root.mkdir(parents=True, exist_ok=True)
    prompt = render_prompt(selected, output_count=output_count)
    prompt_path = output_root / f"{date.today().isoformat()}-deepthink-handoff-prompt.json"
    raw_path = output_root / f"{date.today().isoformat()}-deepthink-handoff-raw.json"
    md_path = output_root / f"{date.today().isoformat()}-deepthink-handoff.md"
    report_path = REVIEWS_DIR / f"{source_root.name}-deepthink-handoff-codex-review.md"
    packet_path = output_root / f"{date.today().isoformat()}-deepthink-handoff-packet.json"

    if dry_run:
        return {
            "status": "dry_run",
            "selected_source_candidates": len(selected),
            "prompt_path": rel(prompt_path),
            "output_root": rel(output_root),
            "selected_titles": [item.get("title", "") for item in selected],
        }

    result = run_gemini_cli(prompt, timeout_sec=timeout_sec, model=model)
    parsed = _extract_json_object(str(result.get("clean_output", ""))) if not result.get("error") else None
    handoff_items = _normalize_handoff_items(parsed or {})
    generation_status = "success"
    if not handoff_items:
        generation_status = f"fallback:{result.get('error') or 'invalid_json'}"
        handoff_items = deterministic_fallback(selected, output_count=output_count)
    reviews = [_review_handoff(item) for item in handoff_items]
    output_packet = {
        "status": generation_status,
        "source_root": rel(source_root),
        "review_packet": rel(review_packet),
        "selected_source_candidates": [_compact_candidate(item) for item in selected],
        "handoff_candidates": handoff_items,
        "codex_handoff_reviews": reviews,
        "gemini_status": {
            "provider": result.get("provider", "gemini-cli"),
            "requested_model": result.get("requested_model", model),
            "effective_model": result.get("effective_model", ""),
            "effective_fallback": result.get("effective_fallback", False),
            "exit_code": result.get("exit_code"),
            "timed_out": result.get("timed_out", False),
            "error": result.get("error", ""),
        },
        "counts": {
            "selected_source_candidates": len(selected),
            "handoff_candidates": len(handoff_items),
            "codex_handoff_actions": dict(Counter(str(item.get("codex_handoff_action")) for item in reviews)),
        },
    }
    safe_write(prompt_path, prompt + "\n", backup=True)
    safe_write(raw_path, json.dumps(output_packet, ensure_ascii=False, indent=2) + "\n", backup=True)
    safe_write(packet_path, json.dumps(output_packet, ensure_ascii=False, indent=2) + "\n", backup=True)
    safe_write(
        md_path,
        render_markdown(
            source_root=source_root,
            selected=selected,
            handoff_items=handoff_items,
            reviews=reviews,
            gemini_status=output_packet["gemini_status"],
        ),
        backup=True,
    )
    safe_write(
        report_path,
        render_markdown(
            source_root=source_root,
            selected=selected,
            handoff_items=handoff_items,
            reviews=reviews,
            gemini_status=output_packet["gemini_status"],
        ),
        backup=True,
    )
    return {
        "status": generation_status,
        "output_root": rel(output_root),
        "packet_path": rel(packet_path),
        "markdown_path": rel(md_path),
        "review_path": rel(report_path),
        "selected_source_candidates": len(selected),
        "handoff_candidates": len(handoff_items),
        "codex_handoff_actions": output_packet["counts"]["codex_handoff_actions"],
        "gemini_error": result.get("error", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default=str(DEFAULT_RERUN_ROOT))
    parser.add_argument("--review-packet", default=str(DEFAULT_REVIEW_PACKET))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--gemini-model", default=DEFAULT_MODEL)
    parser.add_argument("--idea-timeout", type=int, default=1200)
    parser.add_argument("--top-k", type=int, default=14)
    parser.add_argument("--output-count", type=int, default=4)
    parser.add_argument("--reuse-existing", action="store_true", help="Rebuild Codex handoff review from the existing Gemini handoff packet.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.reuse_existing:
        result = rebuild_existing_handoff(source_root=Path(args.source_root), output_root=Path(args.output_root))
    else:
        result = compress_handoff(
            review_packet=Path(args.review_packet),
            source_root=Path(args.source_root),
            output_root=Path(args.output_root),
            model=args.gemini_model,
            timeout_sec=args.idea_timeout,
            top_k=max(4, args.top_k),
            output_count=max(3, args.output_count),
            dry_run=args.dry_run,
        )
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            safe_print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
