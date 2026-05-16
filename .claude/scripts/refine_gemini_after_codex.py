"""Run one bounded Gemini refinement pass after Codex review.

This is an optional, post-review refinement layer. It reads existing greenhouse
or handoff packets, uses Codex review reasons as critique, and writes a separate
archive. It never edits raw readings, daily run logs, formal agenda deltas, or
idea_bank seed folders.
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


DEFAULT_INPUT_PACKET = vault_path(
    "projects",
    "research-agenda",
    "divergent-reruns",
    "2026-05-13-haptoken-v3-style-0429-0507",
    "deepthink-handoff",
    "2026-05-13-deepthink-handoff-packet.json",
)
DEFAULT_OUTPUT_ROOT = vault_path("projects", "research-agenda", "post-codex-gemini-refinements")
DEFAULT_MODEL = "gemini-3.1-pro-preview"
ALLOWED_REFINED_ACTIONS = ["send_to_deepthink", "needs_codex_recheck", "park"]
REQUIRED_FIELDS = [
    "title",
    "title_zh",
    "source_title",
    "codex_critique_addressed",
    "revised_handoff_summary_en",
    "revised_handoff_summary_zh",
    "central_hypothesis",
    "physical_failure_scene",
    "core_insight",
    "interface_innovation",
    "optimization_space",
    "why_not_a_b_combination",
    "strongest_baseline",
    "baseline_kill_table",
    "seventy_two_hour_kill_test",
    "what_deepthink_must_decide",
    "negative_claim_boundary",
    "lab_fit",
    "dealbreaker_risks",
    "rescue_mutation",
    "recommended_action",
]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _handoff_items(packet: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [item for item in packet.get("handoff_candidates", []) if isinstance(item, dict)]
    reviews = [item for item in packet.get("codex_handoff_reviews", []) if isinstance(item, dict)]
    review_by_title = {str(item.get("title", "")): item for item in reviews}
    merged: list[dict[str, Any]] = []
    for item in candidates:
        row = dict(item)
        review = review_by_title.get(str(item.get("title", "")), {})
        row["codex_handoff_action"] = review.get("codex_handoff_action", "")
        row["codex_review_reasons"] = review.get("review_reasons", [])
        row["handoff_completeness"] = review.get("handoff_completeness", "")
        merged.append(row)
    return merged


def _daily_review_items(packet: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [item for item in packet.get("raw_gemini_candidates", []) if isinstance(item, dict)]
    parked_or_rewrite = [
        item for item in packet.get("parked_or_rewrite_candidates", [])
        if isinstance(item, dict)
    ]
    reviews = [item for item in packet.get("candidate_reviews", []) if isinstance(item, dict)]
    review_by_title = {str(item.get("title", "")): item for item in reviews}
    merged: list[dict[str, Any]] = []
    source_items = parked_or_rewrite or candidates
    for item in source_items:
        row = dict(item)
        review = review_by_title.get(str(item.get("title", "")), {})
        label = str(item.get("greenhouse_label", ""))
        if review.get("review_action"):
            action = review.get("review_action", "")
        elif label == "rewrite_needed":
            action = "rewrite"
        elif label == "parked_for_weekly_review":
            action = "park"
        else:
            action = label
        row["codex_handoff_action"] = action
        row["codex_review_reasons"] = (
            review.get("final_idea_structure_missing", [])
            or review.get("adversarial_notes", [])
            or item.get("issues", [])
            or [f"greenhouse_label:{label}"]
        )
        row["handoff_completeness"] = review.get("final_idea_structure_score", "")
        merged.append(row)
    return merged


def load_review_items(packet: dict[str, Any]) -> list[dict[str, Any]]:
    if packet.get("handoff_candidates"):
        return _handoff_items(packet)
    return _daily_review_items(packet)


def select_items(items: list[dict[str, Any]], *, actions: set[str], max_items: int) -> list[dict[str, Any]]:
    selected = [
        item for item in items
        if str(item.get("codex_handoff_action") or item.get("recommended_action") or "") in actions
    ]
    if not selected:
        selected = [
            item for item in items
            if str(item.get("recommended_action") or "") in actions
        ]
    return selected[:max_items]


def _read_text(path: Path, limit: int = 8000) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def render_prompt(items: list[dict[str, Any]], *, codex_report_excerpt: str = "") -> str:
    packet = {
        "task": "One-pass Gemini refinement after Codex critique.",
        "role": "Severe robotics PhD invention partner. Repair only the critique-targeted weaknesses; do not invent a new unrelated idea.",
        "output_contract": {
            "format": "Return JSON only.",
            "top_level_key": "refined_candidates",
            "required_fields": REQUIRED_FIELDS,
            "allowed_recommended_action": ALLOWED_REFINED_ACTIONS,
        },
        "rules": [
            "This is a bounded post-Codex pass, not open-ended ideation.",
            "For each item, directly address codex_review_reasons in codex_critique_addressed.",
            "Use codex_report_excerpt as adversarial context when available, but do not copy it verbatim.",
            "If Codex flagged lab mismatch, bind the idea to Franka/FlexiTac/DLO/wrist-camera/local logs or park it.",
            "If Codex flagged A+B weakness, rewrite the causal interface and the discriminating experiment.",
            "If Codex flagged weak hypothesis, rewrite it as: If pathology P is caused by bottleneck B, then interface/optimization change I should beat baseline X under kill test K.",
            "Do not claim confirmed novelty, accepted paper quality, or finished experiments.",
            "Do not add more than one new mechanism per candidate.",
            "Prefer making one candidate precise over making it flashy.",
        ],
        "codex_report_excerpt": codex_report_excerpt,
        "items_to_refine": items,
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def normalize_refined(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = payload.get("refined_candidates")
    if not isinstance(value, list):
        value = payload.get("candidates")
    if not isinstance(value, list):
        return []
    refined: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        row = {field: item.get(field, "") for field in REQUIRED_FIELDS}
        for key, value in item.items():
            if key not in row:
                row[key] = value
        action = str(row.get("recommended_action", ""))
        if action not in ALLOWED_REFINED_ACTIONS:
            row["recommended_action"] = "needs_codex_recheck"
        refined.append(row)
    return refined


def deterministic_fallback(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fallback: list[dict[str, Any]] = []
    for item in items:
        title = str(item.get("title", "Untitled"))
        fallback.append(
            {
                "title": title,
                "title_zh": str(item.get("title_zh", title)),
                "source_title": title,
                "codex_critique_addressed": f"Fallback only; original critique was {item.get('codex_review_reasons', [])}.",
                "revised_handoff_summary_en": str(item.get("handoff_summary_en") or item.get("mechanism") or ""),
                "revised_handoff_summary_zh": str(item.get("handoff_summary_zh") or "Gemini refinement failed; keep original candidate for manual review."),
                "central_hypothesis": str(item.get("central_hypothesis") or item.get("hypothesis") or ""),
                "physical_failure_scene": item.get("physical_failure_scene", ""),
                "core_insight": item.get("core_insight", ""),
                "interface_innovation": item.get("interface_innovation", ""),
                "optimization_space": item.get("optimization_space", ""),
                "why_not_a_b_combination": item.get("why_not_a_b_combination") or item.get("anti_combination_test", ""),
                "strongest_baseline": item.get("strongest_baseline", ""),
                "baseline_kill_table": item.get("baseline_kill_table", ""),
                "seventy_two_hour_kill_test": item.get("seventy_two_hour_kill_test") or item.get("minimum_no_hardware_pilot", ""),
                "what_deepthink_must_decide": item.get("what_deepthink_must_decide") or item.get("reviewer_pre_mortem", ""),
                "negative_claim_boundary": item.get("negative_claim_boundary", ""),
                "lab_fit": item.get("lab_fit", ""),
                "dealbreaker_risks": item.get("dealbreaker_risks") or item.get("what_would_make_this_not_a_paper", ""),
                "rescue_mutation": item.get("rescue_mutation", ""),
                "recommended_action": "needs_codex_recheck",
            }
        )
    return fallback


def _quick_codex_gate(item: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(str(item.get(field, "")) for field in REQUIRED_FIELDS).lower()
    missing = [field for field in REQUIRED_FIELDS if not str(item.get(field, "")).strip()]
    reasons: list[str] = []
    if missing:
        reasons.append("missing:" + ",".join(missing[:5]))
    if not ("if" in str(item.get("central_hypothesis", "")).lower() and "then" in str(item.get("central_hypothesis", "")).lower()):
        reasons.append("hypothesis_not_decision_shaped")
    if len(str(item.get("why_not_a_b_combination", ""))) < 70:
        reasons.append("anti_combination_still_weak")
    if not any(token in text for token in ["franka", "flextac", "dlo", "cable", "wrist", "双臂", "触觉", "腕部"]):
        reasons.append("lab_fit_still_weak")
    action = str(item.get("recommended_action", "needs_codex_recheck"))
    if reasons and action == "send_to_deepthink":
        action = "needs_codex_recheck"
    return {
        "title": item.get("title", ""),
        "codex_refinement_action": action,
        "review_reasons": reasons or ["refinement_ready_for_external_review"],
    }


def render_markdown(packet: dict[str, Any]) -> str:
    refined = packet.get("refined_candidates", [])
    reviews = packet.get("codex_refinement_reviews", [])
    counts = Counter(str(item.get("codex_refinement_action", "")) for item in reviews)
    frontmatter = render_frontmatter(
        "Post-Codex Gemini Refinement",
        ["research-agenda", "gemini-refinement", "codex-review"],
        "Optional one-pass Gemini refinement after Codex critique.",
        status="done" if refined else "partial",
    )
    lines = [
        frontmatter.rstrip(),
        "# Post-Codex Gemini Refinement",
        "",
        "## Executive Verdict",
        "",
        f"- status: {packet.get('status')}",
        f"- source_packet: {packet.get('source_packet')}",
        f"- refined_candidates: {len(refined)}",
        f"- codex_refinement_actions: {json.dumps(dict(counts), ensure_ascii=False, sort_keys=True)}",
        f"- gemini_effective_model: {packet.get('gemini_status', {}).get('effective_model', '-')}",
        "- boundary: optional archive only; no formal seed or daily output is changed.",
        "",
        "## Refined Candidates",
        "",
    ]
    review_by_title = {str(item.get("title", "")): item for item in reviews}
    for index, item in enumerate(refined, 1):
        review = review_by_title.get(str(item.get("title", "")), {})
        lines.extend(
            [
                f"### {index}. {item.get('title')}",
                "",
                f"- 中文名: {item.get('title_zh')}",
                f"- action: `{review.get('codex_refinement_action', item.get('recommended_action'))}`",
                f"- critique_addressed: {item.get('codex_critique_addressed')}",
                f"- summary_en: {item.get('revised_handoff_summary_en')}",
                f"- summary_zh: {item.get('revised_handoff_summary_zh')}",
                f"- central_hypothesis: {item.get('central_hypothesis')}",
                f"- physical_failure_scene: {item.get('physical_failure_scene')}",
                f"- core_insight: {item.get('core_insight')}",
                f"- interface_innovation: {item.get('interface_innovation')}",
                f"- strongest_baseline: {item.get('strongest_baseline')}",
                f"- 72h_kill_test: {item.get('seventy_two_hour_kill_test')}",
                f"- DeepThink question: {item.get('what_deepthink_must_decide')}",
                f"- review_reasons: {', '.join(review.get('review_reasons', [])) if review else '-'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- This is a one-pass refinement after Codex critique.",
            "- It should not loop automatically without human request.",
            "- User remains final reviewer before any formal seed promotion.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_refinement(
    *,
    input_packet: Path,
    output_root: Path,
    actions: set[str],
    max_items: int,
    model: str,
    timeout_sec: int,
    dry_run: bool,
    codex_report: Path | None = None,
) -> dict[str, Any]:
    source = _read_json(input_packet)
    items = select_items(load_review_items(source), actions=actions, max_items=max_items)
    output_root.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    prompt = render_prompt(items)
    prompt_path = output_root / f"{stamp}-post-codex-gemini-refine-prompt.json"
    packet_path = output_root / f"{stamp}-post-codex-gemini-refine-packet.json"
    md_path = output_root / f"{stamp}-post-codex-gemini-refine.md"
    review_path = REVIEWS_DIR / f"{stamp}-post-codex-gemini-refine-review.md"
    codex_report_excerpt = _read_text(codex_report, limit=9000) if codex_report else ""
    if dry_run:
        return {
            "status": "dry_run",
            "selected_items": len(items),
            "selected_titles": [item.get("title", "") for item in items],
            "prompt_path": rel(prompt_path),
            "output_root": rel(output_root),
        }
    if not items:
        return {
            "status": "skipped_no_candidates",
            "selected_items": 0,
            "output_root": rel(output_root),
        }
    prompt = render_prompt(items, codex_report_excerpt=codex_report_excerpt)
    result = run_gemini_cli(prompt, timeout_sec=timeout_sec, model=model)
    parsed = _extract_json_object(str(result.get("clean_output", ""))) if not result.get("error") else None
    refined = normalize_refined(parsed or {})
    status = "success"
    if not refined:
        status = f"fallback:{result.get('error') or 'invalid_json'}"
        refined = deterministic_fallback(items)
    reviews = [_quick_codex_gate(item) for item in refined]
    packet = {
        "status": status,
        "source_packet": rel(input_packet),
        "codex_report": rel(codex_report) if codex_report else "",
        "selected_items": items,
        "refined_candidates": refined,
        "codex_refinement_reviews": reviews,
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
            "selected_items": len(items),
            "refined_candidates": len(refined),
            "codex_refinement_actions": dict(Counter(str(item.get("codex_refinement_action")) for item in reviews)),
        },
    }
    safe_write(prompt_path, prompt + "\n", backup=True)
    safe_write(packet_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", backup=True)
    markdown = render_markdown(packet)
    safe_write(md_path, markdown, backup=True)
    safe_write(review_path, markdown, backup=True)
    return {
        "status": status,
        "selected_items": len(items),
        "refined_candidates": len(refined),
        "packet_path": rel(packet_path),
        "markdown_path": rel(md_path),
        "review_path": rel(review_path),
        "codex_refinement_actions": packet["counts"]["codex_refinement_actions"],
        "gemini_error": result.get("error", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-packet", default=str(DEFAULT_INPUT_PACKET))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--actions", default="rewrite_once_more,needs_codex_recheck")
    parser.add_argument("--max-items", type=int, default=3)
    parser.add_argument("--gemini-model", default=DEFAULT_MODEL)
    parser.add_argument("--idea-timeout", type=int, default=1200)
    parser.add_argument("--codex-report", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    actions = {item.strip() for item in str(args.actions).split(",") if item.strip()}
    result = run_refinement(
        input_packet=Path(args.input_packet),
        output_root=Path(args.output_root),
        actions=actions,
        max_items=max(1, args.max_items),
        model=args.gemini_model,
        timeout_sec=args.idea_timeout,
        dry_run=args.dry_run,
        codex_report=Path(args.codex_report) if args.codex_report else None,
    )
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            safe_print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
