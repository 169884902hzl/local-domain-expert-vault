"""Run a bounded Gemini-DeepSeek debate over daily idea candidates.

This is the mandatory adversarial idea-quality stage for Gemini greenhouse runs.
It writes an archive under projects/research-agenda/model-debates and never
edits raw readings, Zotero items, or idea_bank seed folders.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from gemini_cli_adapter import DEFAULT_GEMINI_MODEL, run_gemini_cli
from kb_common import safe_print, safe_write, vault_path
from opencode_cli_adapter import DEFAULT_OPENCODE_MODEL, run_opencode_cli
from research_agenda_common import REVIEWS_DIR, rel, render_frontmatter
from research_agenda_ideate import _extract_json_object


DEFAULT_OUTPUT_ROOT = vault_path("projects", "research-agenda", "model-debates")
DEFAULT_ACTIONS = {"all"}
LEGACY_REVIEW_ACTIONS = {"rewrite", "park", "rewrite_once_more", "needs_codex_recheck"}
DEEPSEEK_FIELDS = [
    "title",
    "adversarial_verdict",
    "is_a_b_combination",
    "physical_failure_scene_score",
    "interface_innovation_score",
    "optimization_space_score",
    "strongest_baseline_kill",
    "not_a_paper_reason",
    "lab_fit_risk",
    "required_mutation",
    "rescue_signal",
    "recommended_action",
]
GEMINI_FIELDS = [
    "title",
    "mutated_title",
    "central_hypothesis",
    "physical_failure_scene",
    "core_mechanism",
    "interface_boundary_change",
    "optimization_space",
    "why_not_a_b_combination",
    "strongest_baseline",
    "killer_experiment",
    "two_week_sprint",
    "claim_boundary",
    "remaining_kill_shot",
    "recommended_action",
]
GEMINI_MUTATION_SHORT_INSTRUCTION = (
    "Return JSON only with key 'mutated_candidates' (array of objects). "
    "Each object needs: title, mutated_title, central_hypothesis, physical_failure_scene, "
    "core_mechanism, interface_boundary_change, optimization_space, why_not_a_b_combination, "
    "strongest_baseline, killer_experiment, two_week_sprint, claim_boundary, "
    "remaining_kill_shot, recommended_action. Do not return key 'candidates'."
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _vault_resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else vault_path(*value.parts)


def _read_text(path: Path | None, limit: int = 10000) -> str:
    if not path or not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def _candidate_title(item: dict[str, Any]) -> str:
    return str(item.get("title") or item.get("candidate") or item.get("mechanism") or "Untitled")


def _review_action(item: dict[str, Any]) -> str:
    for key in ["review_action", "codex_handoff_action", "recommended_action", "greenhouse_label"]:
        value = str(item.get(key, "")).strip()
        if value:
            return value
    return ""


def load_candidates(packet: dict[str, Any], *, actions: set[str], max_items: int) -> list[dict[str, Any]]:
    raw = [item for item in packet.get("raw_gemini_candidates", []) if isinstance(item, dict)]
    focused = [item for item in packet.get("parked_or_rewrite_candidates", []) if isinstance(item, dict)]
    reviews = [item for item in packet.get("candidate_reviews", []) if isinstance(item, dict)]
    by_title = {_candidate_title(item): item for item in raw}
    for item in focused:
        by_title[_candidate_title(item)] = {**by_title.get(_candidate_title(item), {}), **item}
    for review in reviews:
        title = _candidate_title(review)
        merged = {**by_title.get(title, {}), **review}
        by_title[title] = merged
    items = list(by_title.values())
    if "all" in actions:
        return items[:max_items]
    selected = [item for item in items if _review_action(item) in actions]
    if not selected:
        selected = [item for item in items if str(item.get("greenhouse_label", "")) in {"rewrite_needed", "parked_for_weekly_review"}]
    return selected[:max_items]


def render_deepseek_prompt(items: list[dict[str, Any]], *, codex_report_excerpt: str) -> str:
    payload = {
        "task": "Adversarial robotics research review of Gemini greenhouse ideas.",
        "role": "DeepSeek is the hostile reviewer. Do not improve the ideas yet. Attack weak mechanisms.",
        "output_contract": {
            "format": "Return JSON only.",
            "top_level_key": "deepseek_reviews",
            "required_fields": DEEPSEEK_FIELDS,
            "allowed_recommended_action": ["mutate", "park", "reject_with_rescue"],
        },
        "rules": [
            "Start from physical robot failure scenes, not paper A plus paper B.",
            "Flag A+B combination if the idea only adds an input, swaps a module, or wraps a residual.",
            "For RL-token ideas, inspect token/latent/action/critic space, decoder boundary, and off-manifold risk.",
            "Use lab fit: Franka, FlexiTac, wrist camera, DLO, bimanual manipulation are strengths; fleet-scale or low-cost hardware pathology is weaker.",
            "Name the strongest baseline that would kill the idea.",
            "Prefer rescue mutation over praise. Do not claim confirmed novelty.",
        ],
        "codex_report_excerpt": codex_report_excerpt,
        "candidates": items,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_gemini_mutation_prompt(items: list[dict[str, Any]], deepseek_reviews: list[dict[str, Any]]) -> str:
    payload = {
        "task": "Mutate Gemini greenhouse ideas after DeepSeek adversarial review.",
        "role": "Gemini is now the inventor under attack. Defend only if the mechanism survives; otherwise mutate or concede.",
        "output_contract": {
            "format": "Return JSON only.",
            "top_level_key": "mutated_candidates",
            "required_fields": GEMINI_FIELDS,
            "allowed_recommended_action": ["send_to_user_review", "needs_codex_recheck", "park", "reject_with_rescue"],
        },
        "rules": [
            "Do not produce a new unrelated idea.",
            "If DeepSeek finds A+B composition, change the boundary, feedback loop, controlled variable, or loss placement.",
            "The output must contain a concrete physical failure scene and a falsifiable hypothesis.",
            "The strongest baseline and killer experiment must discriminate mechanism from engineering polish.",
            "Do not accept a candidate whose remaining_kill_shot still kills the core claim.",
            "Quality reference: HapToken-v3 style depth, with claim boundary and two-week sprint.",
        ],
        "original_candidates": items,
        "deepseek_reviews": deepseek_reviews,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _normalize_list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key) or payload.get("candidates") or payload.get("reviews")
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _fallback_deepseek(items: list[dict[str, Any]], reason: str) -> list[dict[str, Any]]:
    return [
        {
            "title": _candidate_title(item),
            "adversarial_verdict": f"Fallback review only because DeepSeek failed: {reason}",
            "is_a_b_combination": "unknown",
            "physical_failure_scene_score": "unknown",
            "interface_innovation_score": "unknown",
            "optimization_space_score": "unknown",
            "strongest_baseline_kill": str(item.get("strongest_baseline", "")),
            "not_a_paper_reason": str(item.get("what_would_make_this_not_a_paper", "")),
            "lab_fit_risk": str(item.get("lab_fit", "")),
            "required_mutation": "Run manual adversarial review before promotion.",
            "rescue_signal": str(item.get("rescue_signal", "")),
            "recommended_action": "park",
        }
        for item in items
    ]


def _fallback_gemini(items: list[dict[str, Any]], reviews: list[dict[str, Any]], reason: str) -> list[dict[str, Any]]:
    by_title = {str(item.get("title", "")): item for item in reviews}
    rows: list[dict[str, Any]] = []
    for item in items:
        title = _candidate_title(item)
        review = by_title.get(title, {})
        rows.append(
            {
                "title": title,
                "mutated_title": title,
                "central_hypothesis": str(item.get("central_hypothesis") or item.get("hypothesis") or ""),
                "physical_failure_scene": str(item.get("physical_failure_scene") or item.get("engineering_pathology") or ""),
                "core_mechanism": str(item.get("mechanism", "")),
                "interface_boundary_change": str(item.get("interface_innovation") or item.get("interface", "")),
                "optimization_space": str(item.get("optimization_space", "")),
                "why_not_a_b_combination": str(item.get("why_not_a_b_combination", "")),
                "strongest_baseline": str(review.get("strongest_baseline_kill") or item.get("strongest_baseline", "")),
                "killer_experiment": str(item.get("killer_experiment", "")),
                "two_week_sprint": "Fallback only; rerun model debate or manual DeepThink before promotion.",
                "claim_boundary": "No claim accepted.",
                "remaining_kill_shot": f"Gemini mutation failed: {reason}",
                "recommended_action": "needs_codex_recheck",
            }
        )
    return rows


def render_markdown(packet: dict[str, Any]) -> str:
    deepseek = packet.get("deepseek_reviews", [])
    mutated = packet.get("gemini_mutations", [])
    counts = Counter(str(item.get("recommended_action", "")) for item in mutated)
    lines = [
        render_frontmatter(
            "Gemini DeepSeek Model Debate",
            ["research-agenda", "model-debate", "idea-quality"],
            "Mandatory Gemini-DeepSeek adversarial battle over daily greenhouse idea candidates.",
        ).rstrip(),
        "",
        "# Gemini DeepSeek Model Debate",
        "",
        "## Summary",
        "",
        f"- status: {packet.get('status')}",
        f"- source_packet: {packet.get('source_packet')}",
        f"- codex_report: {packet.get('codex_report')}",
        f"- selected_items: {packet.get('counts', {}).get('selected_items', 0)}",
        f"- mutated_actions: {json.dumps(dict(counts), ensure_ascii=False, sort_keys=True)}",
        "- boundary: mandatory for daily greenhouse agenda success; no seed, raw reading, or Zotero item is changed automatically.",
        "",
        "## DeepSeek Adversarial Review",
        "",
    ]
    for item in deepseek:
        lines.extend(
            [
                f"### {item.get('title', 'Untitled')}",
                "",
                f"- verdict: {item.get('adversarial_verdict', '')}",
                f"- a_b_combination: {item.get('is_a_b_combination', '')}",
                f"- strongest_baseline_kill: {item.get('strongest_baseline_kill', '')}",
                f"- required_mutation: {item.get('required_mutation', '')}",
                f"- recommended_action: {item.get('recommended_action', '')}",
                "",
            ]
        )
    lines.extend(["## Gemini Mutation", ""])
    for item in mutated:
        lines.extend(
            [
                f"### {item.get('mutated_title') or item.get('title', 'Untitled')}",
                "",
                f"- original_title: {item.get('title', '')}",
                f"- central_hypothesis: {item.get('central_hypothesis', '')}",
                f"- physical_failure_scene: {item.get('physical_failure_scene', '')}",
                f"- core_mechanism: {item.get('core_mechanism', '')}",
                f"- interface_boundary_change: {item.get('interface_boundary_change', '')}",
                f"- optimization_space: {item.get('optimization_space', '')}",
                f"- why_not_a_b_combination: {item.get('why_not_a_b_combination', '')}",
                f"- strongest_baseline: {item.get('strongest_baseline', '')}",
                f"- killer_experiment: {item.get('killer_experiment', '')}",
                f"- two_week_sprint: {item.get('two_week_sprint', '')}",
                f"- remaining_kill_shot: {item.get('remaining_kill_shot', '')}",
                f"- recommended_action: {item.get('recommended_action', '')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def run_debate(
    *,
    input_packet: Path,
    codex_report: Path | None,
    output_root: Path,
    actions: set[str],
    max_items: int,
    deepseek_model: str,
    gemini_model: str,
    deepseek_timeout: int,
    gemini_timeout: int,
    dry_run: bool,
    run_date: str | None = None,
    strict: bool = False,
) -> dict[str, Any]:
    source = _read_json(input_packet)
    items = load_candidates(source, actions=actions, max_items=max_items)
    stamp = run_date or date.today().isoformat()
    output_root.mkdir(parents=True, exist_ok=True)
    prompt_deepseek_path = output_root / f"{stamp}-gemini-deepseek-debate-deepseek-prompt.json"
    prompt_gemini_path = output_root / f"{stamp}-gemini-deepseek-debate-gemini-prompt.json"
    packet_path = output_root / f"{stamp}-gemini-deepseek-debate-packet.json"
    md_path = output_root / f"{stamp}-gemini-deepseek-debate.md"
    review_path = REVIEWS_DIR / f"{stamp}-gemini-deepseek-debate.md"
    codex_excerpt = _read_text(codex_report, limit=12000)
    deepseek_prompt = render_deepseek_prompt(items, codex_report_excerpt=codex_excerpt)
    if dry_run:
        return {
            "status": "dry_run",
            "selected_items": len(items),
            "selected_titles": [_candidate_title(item) for item in items],
            "output_root": rel(output_root),
            "deepseek_model": deepseek_model,
            "gemini_model": gemini_model,
        }
    if not items:
        status = "failed_no_candidates" if strict else "skipped_no_candidates"
        return {"status": status, "selected_items": 0, "output_root": rel(output_root)}
    deepseek_result = run_opencode_cli(
        deepseek_prompt,
        model=deepseek_model,
        timeout_sec=deepseek_timeout,
        title=f"{stamp}-deepseek-adversarial-review",
    )
    deepseek_payload = _extract_json_object(str(deepseek_result.get("clean_output", ""))) if not deepseek_result.get("error") else None
    deepseek_reviews = _normalize_list(deepseek_payload or {}, "deepseek_reviews")
    status = "success"
    if not deepseek_reviews:
        status = f"failed_deepseek:{deepseek_result.get('error') or 'invalid_json'}" if strict else f"fallback_deepseek:{deepseek_result.get('error') or 'invalid_json'}"
        deepseek_reviews = _fallback_deepseek(items, str(deepseek_result.get("error") or "invalid_json"))
    gemini_prompt = render_gemini_mutation_prompt(items, deepseek_reviews)
    gemini_result = run_gemini_cli(
        gemini_prompt,
        timeout_sec=gemini_timeout,
        model=gemini_model,
        short_instruction=GEMINI_MUTATION_SHORT_INSTRUCTION,
    )
    gemini_payload = _extract_json_object(str(gemini_result.get("clean_output", ""))) if not gemini_result.get("error") else None
    mutations = _normalize_list(gemini_payload or {}, "mutated_candidates")
    if not mutations:
        status = status + (
            f"; failed_gemini:{gemini_result.get('error') or 'invalid_json'}"
            if strict
            else f"; fallback_gemini:{gemini_result.get('error') or 'invalid_json'}"
        )
        mutations = _fallback_gemini(items, deepseek_reviews, str(gemini_result.get("error") or "invalid_json"))
    packet = {
        "status": status,
        "source_packet": rel(input_packet),
        "codex_report": rel(codex_report) if codex_report else "",
        "selected_items": items,
        "deepseek_reviews": deepseek_reviews,
        "gemini_mutations": mutations,
        "provider_status": {
            "deepseek": {
                "provider": deepseek_result.get("provider"),
                "requested_model": deepseek_result.get("requested_model"),
                "exit_code": deepseek_result.get("exit_code"),
                "timed_out": deepseek_result.get("timed_out"),
                "error": deepseek_result.get("error"),
            },
            "gemini": {
                "provider": gemini_result.get("provider"),
                "requested_model": gemini_result.get("requested_model"),
                "effective_model": gemini_result.get("effective_model"),
                "effective_fallback": gemini_result.get("effective_fallback"),
                "exit_code": gemini_result.get("exit_code"),
                "timed_out": gemini_result.get("timed_out"),
                "error": gemini_result.get("error"),
            },
        },
        "counts": {
            "selected_items": len(items),
            "deepseek_reviews": len(deepseek_reviews),
            "gemini_mutations": len(mutations),
            "mutation_actions": dict(Counter(str(item.get("recommended_action")) for item in mutations)),
        },
    }
    safe_write(prompt_deepseek_path, deepseek_prompt + "\n", backup=True)
    safe_write(prompt_gemini_path, gemini_prompt + "\n", backup=True)
    safe_write(packet_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", backup=True)
    markdown = render_markdown(packet)
    safe_write(md_path, markdown, backup=True)
    safe_write(review_path, markdown, backup=True)
    return {
        "status": status,
        "selected_items": len(items),
        "packet_path": rel(packet_path),
        "markdown_path": rel(md_path),
        "review_path": rel(review_path),
        "mutation_actions": packet["counts"]["mutation_actions"],
        "deepseek_error": deepseek_result.get("error", ""),
        "gemini_error": gemini_result.get("error", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-packet", required=True)
    parser.add_argument("--codex-report", default="")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--actions", default="all")
    parser.add_argument("--max-items", type=int, default=8)
    parser.add_argument("--deepseek-model", default=DEFAULT_OPENCODE_MODEL)
    parser.add_argument("--gemini-model", default=DEFAULT_GEMINI_MODEL)
    parser.add_argument("--deepseek-timeout", type=int, default=1200)
    parser.add_argument("--gemini-timeout", type=int, default=1200)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    actions = {item.strip() for item in str(args.actions).split(",") if item.strip()} or DEFAULT_ACTIONS
    result = run_debate(
        input_packet=_vault_resolve(args.input_packet),
        codex_report=_vault_resolve(args.codex_report) if args.codex_report else None,
        output_root=_vault_resolve(args.output_root),
        actions=actions,
        max_items=max(1, args.max_items),
        deepseek_model=args.deepseek_model,
        gemini_model=args.gemini_model,
        deepseek_timeout=args.deepseek_timeout,
        gemini_timeout=args.gemini_timeout,
        dry_run=args.dry_run,
        run_date=args.run_date or None,
        strict=args.strict,
    )
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            safe_print(f"{key}: {value}")
    if args.strict and str(result.get("status", "")) not in {"success", "dry_run"}:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
