"""Rerun historical Gemini idea generation into a separate archive.

This is a one-off recovery/re-evaluation tool. It never writes formal daily
agenda deltas, seed folders, Zotero records, or raw readings.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from gemini_cli_adapter import run_gemini_cli
from kb_common import safe_print, safe_write, vault_path
from research_agenda_common import DAILY_DIR, DIVERGENT_DIR, REVIEWS_DIR, load_evidence_matrix, rel, render_frontmatter
from research_agenda_ideate import (
    DEFAULT_MIN_RAW_CANDIDATES,
    QUALITY_RUBRIC_WEIGHTS,
    WORKFLOW_CONTRACTS,
    _apply_research_quality,
    _divergent_supporting,
    _extract_json_object,
    _gate_mechanism_candidate,
    _greenhouse_counts,
    _idea_keywords,
    _jsonable_candidate,
    _mechanism_candidates,
    _normalize_divergent_axis,
    _novelty_pressure_corpus,
    _quality_label_from_tier,
    _quality_sort_key,
    _recent_count,
    _source_count,
    _strong_source_count,
    _top_domains,
    render_greenhouse_markdown,
)


DEFAULT_OUTPUT_ROOT = vault_path("projects", "research-agenda", "divergent-reruns", "2026-05-08-0429-0507")
RERUN_GROUPS = ["historical_rl_token_context", "free_divergence_current_standard"]
QUALITY_PROMOTION_TIERS = {"S", "A"}


def _date_range(start_date: str, end_date: str) -> list[str]:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    days: list[str] = []
    current = start
    while current <= end:
        days.append(current.isoformat())
        current += timedelta(days=1)
    return days


def _read_text(path: Path, *, limit: int) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _focus_keys_from_agenda(run_date: str) -> list[str]:
    path = DAILY_DIR / f"{run_date}-agenda-delta.md"
    if not path.exists():
        return []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("- focus_zotero_keys:"):
            value = line.split(":", 1)[1].strip()
            if not value or value == "-":
                return []
            return [item.strip().upper() for item in value.split(",") if item.strip()]
    return []


def _old_greenhouse(run_date: str) -> dict[str, Any]:
    return _read_json(DIVERGENT_DIR / f"{run_date}-gemini-raw-candidates.json")


def _manual_greenhouse(run_date: str) -> dict[str, Any]:
    return _read_json(DIVERGENT_DIR / f"{run_date}-gemini-manual-raw-candidates.json")


def _candidate_count(payload: dict[str, Any]) -> int:
    for key in ["raw_gemini_candidates", "raw_candidates", "candidates"]:
        value = payload.get(key)
        if isinstance(value, list):
            return len(value)
    return 0


def _extract_candidate_list(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ["raw_gemini_candidates", "raw_candidates", "candidates"]:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _existing_seed_titles() -> list[str]:
    base = vault_path("projects", "research-agenda", "idea_bank", "seed")
    if not base.exists():
        return []
    titles: list[str] = []
    for path in sorted(base.glob("*/idea.md")):
        text = _read_text(path, limit=1200)
        for line in text.splitlines():
            if line.startswith("title:"):
                titles.append(line.split(":", 1)[1].strip().strip('"'))
                break
    return titles[:120]


def _focus_records(records: list[dict[str, Any]], focus_keys: set[str]) -> list[dict[str, Any]]:
    return [record for record in records if str(record.get("zotero_key", "")).upper() in focus_keys]


def _history_context(run_date: str) -> dict[str, Any]:
    old = _old_greenhouse(run_date)
    manual = _manual_greenhouse(run_date)
    old_titles = [item.get("title", "") for item in _extract_candidate_list(old)[:12]]
    manual_titles = [item.get("title", "") for item in _extract_candidate_list(manual)[:12]]
    positive_reference = _manual_greenhouse("2026-05-06")
    positive_titles = [item.get("title", "") for item in _extract_candidate_list(positive_reference)[:8]]
    return {
        "agenda_delta_excerpt": _read_text(DAILY_DIR / f"{run_date}-agenda-delta.md", limit=4500),
        "old_greenhouse_status": old.get("generator_status", ""),
        "old_greenhouse_candidate_count": _candidate_count(old),
        "old_greenhouse_titles": old_titles,
        "manual_greenhouse_candidate_count": _candidate_count(manual),
        "manual_greenhouse_titles": manual_titles,
        "positive_manual_reference_2026_05_06_titles": positive_titles,
    }


def _record_packet(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_note": record.get("source_note", ""),
        "source_title": record.get("source_title", ""),
        "zotero_key": record.get("zotero_key", ""),
        "claim_type": record.get("claim_type", ""),
        "domains": record.get("domains", []),
        "statement": str(record.get("statement", ""))[:700],
    }


def _cluster_packet(axis: dict[str, Any], evidence: list[dict[str, Any]], recent: int) -> dict[str, Any]:
    return {
        "title": axis.get("title", ""),
        "cluster_id": axis.get("cluster_id", ""),
        "domains": axis.get("domains", []),
        "problem": axis.get("problem", ""),
        "engineering_pathology": axis.get("engineering_pathology", ""),
        "mechanism": axis.get("mechanism", ""),
        "interface": axis.get("interface", ""),
        "hypothesis": axis.get("hypothesis", ""),
        "recent_sources": recent,
        "local_source_count": _source_count(evidence),
        "evidence": [_record_packet(item) for item in evidence[:8]],
    }


def _render_group_prompt(
    *,
    run_date: str,
    group: str,
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]],
    records: list[dict[str, Any]],
    focus_keys: set[str],
    raw_limit: int,
    min_raw_candidates: int,
) -> str:
    focus_records = _focus_records(records, focus_keys)
    common_rules = [
        "Return JSON only with key candidates.",
        f"Return {min_raw_candidates}-{raw_limit} candidates unless the evidence truly cannot support that many.",
        "Each candidate needs exactly these fields: title, candidate_group, rerun_group, problem, physical_failure_scene, engineering_pathology, mechanism, interface, interface_innovation, optimization_space, loss_placement, decoder_boundary, manifold_safety, hypothesis, evidence_links, speculative_jump, idea_archetype, contribution_shape, non_obvious_claim, anti_combination_test, top_tier_rationale, engineering_loop, method_improvement_claim, original_method_failure, replacement_or_coupled_technique, why_improvement_not_patch, why_now, strongest_baseline, baseline_failure_mode, killer_experiment, novelty_risk, reviewer_kill_shot, rescue_mutation, claim_compression, online_or_offline_mode, minimum_no_hardware_pilot, baseline_kill_table, what_would_make_this_not_a_paper, reviewer_pre_mortem, falsification_discriminates_mechanism, lab_fit, hardware_assumptions, negative_claim_boundary, version_evolution_story, core_insight, pipeline_steps, defense_patches, baseline_matrix, metric_suite, risk_assumptions, competition_map, two_week_sprint, promotion_reason, rescue_signal, nearest_pressure, pilot, baselines, metrics, falsification.",
        "candidate_group must be evidence_bound or wild_engineering.",
        "rerun_group must exactly match the rerun_group field in this packet.",
        "idea_archetype must be one of method_improvement, interface_invention, failure_model, evaluation_metric, closed_loop_system, data_or_labeling_strategy, representation_shift, control_policy_mechanism, instrumentation_or_sensing.",
        "contribution_shape must be one of architecture, algorithm, control_interface, mechanism, system, method_improvement, evaluation_protocol, benchmark, failure_model, or dataset.",
        "Do not write confirmed novelty, accepted claims, or experiment results.",
        "Before assigning a strong candidate, do reviewer_pre_mortem. If the pre-mortem kills the core claim, write promotion_reason=rewrite_needed.",
        "minimum_no_hardware_pilot must use logs, existing datasets, paper-derived examples, toy dynamics, benchmark slices, or offline ablations before new robot experiments.",
        "baseline_kill_table must be semicolon-separated: baseline -> how it kills us -> measurement needed to survive.",
        "what_would_make_this_not_a_paper must state the collapse condition where the idea is just a patch or A+B.",
        "For method_improvement, explain why the change alters a failure mechanism, interface, constraint, feedback loop, or evaluation signal.",
        "Do not start from paper A plus paper B. Start from a concrete robot failure episode, then use papers as tools or pressure.",
        "physical_failure_scene must name sensors, object, contact or occlusion, timing or geometry, and the actual robot failure.",
        "interface_innovation must state what changes at the VLA/RL-token/control boundary; adding an input or swapping a module is not enough.",
        "optimization_space/loss_placement/decoder_boundary/manifold_safety must explain where the objective lives and how it avoids breaking token/latent/action manifolds.",
        "falsification_discriminates_mechanism must distinguish mechanism from engineering patch, not merely compare two backbones.",
        "lab_fit must use or reject the local fit: Franka-quality arms, bimanual setup, wrist cameras, FlexiTac/tactile sensing, DLO/cable tasks, local logs.",
        "Use HapToken-v3 style as structure, not content: negative claim boundary, version evolution, core insight, runnable pipeline, defense patches, baseline matrix, metric suite, risk assumptions, competition map, and two-week sprint.",
        "baseline_matrix must include at least five controls: lower bound, strongest direct baseline, simple heuristic, ablation without the mechanism, and oracle/upper bound where possible.",
        "two_week_sprint must include the earliest kill test, not just generic implementation tasks.",
    ]
    if group == "historical_rl_token_context":
        group_rules = [
            "This pass preserves the 2026-04-29 to 2026-05-07 historical RL Token / VLA / online RL context.",
            "Reconsider whether RL-token-related candidates were unfairly suppressed by old scoring, but do not force every idea to be RL Token.",
            "Look for critic-side memory, token-level failure traces, VLA anchoring, online recovery, and action-chunk feedback loops only when they are mechanistically justified.",
        ]
    else:
        group_rules = [
            "This pass uses the current 2026-05-08 free-divergence standard.",
            "Do not privilege RL Token / VLA / Sim-to-Real unless the evidence and robot pathology make them central.",
            "Prefer fresh DLO, tactile, bimanual, wrist-camera, occlusion, contact-rich control, benchmark, failure-model, and method-improvement directions.",
        ]
    packet = {
        "task": "Rerun historical Gemini greenhouse idea generation with current top-tier prompt standards.",
        "run_date": run_date,
        "rerun_group": group,
        "role": "Severe Physical AI / robotics PhD advisor and invention partner.",
        "rules": [*common_rules, *group_rules],
        "quality_target": {
            "bar": "doctoral research seed under RSS/CoRL/ICRA/RA-L pressure, not an idea dump",
            "prefer": [
            "real robot pathology",
            "non-obvious causal mechanism or interface",
            "specific physical failure scene before method names",
            "interface and optimization-space choice before architecture choice",
            "strongest baseline that could kill the idea",
            "no-hardware pilot before expensive validation",
            "rescue mutation for risky but creative ideas",
            ],
            "avoid": [
                "simple A+B combination",
                "generic LLM/VLA wrapper",
                "RL-token framing without a distinct failure mechanism",
                "benchmark without a hidden failure metric",
                "online control system when offline replay is the right first paper",
            ],
        },
        "history_context": _history_context(run_date),
        "existing_seed_titles": _existing_seed_titles(),
        "focus_zotero_keys": sorted(focus_keys),
        "newly_read_evidence": [_record_packet(record) for record in focus_records[:32]],
        "matrix_clusters": [_cluster_packet(axis, evidence, recent) for _, axis, evidence, recent in candidates[:10]],
        "workflow_contracts": WORKFLOW_CONTRACTS,
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def _score_items(
    items: list[dict[str, Any]],
    *,
    records: list[dict[str, Any]],
    focus_keys: set[str],
    fallback_domains: list[str],
    raw_limit: int,
) -> list[tuple[int, dict[str, Any], list[dict[str, Any]], int]]:
    novelty_corpus = _novelty_pressure_corpus()
    scored: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]] = []
    for item in items[: max(1, raw_limit)]:
        rerun_group = str(item.get("rerun_group", "")).strip()
        axis = _normalize_divergent_axis(item, fallback_domains=fallback_domains)
        if rerun_group:
            axis["rerun_group"] = rerun_group
        evidence = _divergent_supporting(records, axis, focus_keys=focus_keys)
        recent = _recent_count(evidence, focus_keys)
        evidence_score = (
            _strong_source_count(evidence, axis) * 55
            + _source_count(evidence) * 6
            + recent * 25
            + len(_idea_keywords(axis))
        )
        axis = _apply_research_quality(
            axis,
            evidence,
            recent,
            evidence_score=evidence_score,
            novelty_corpus=novelty_corpus,
        )
        scored.append((evidence_score, axis, evidence, recent))
    return sorted(scored, key=_quality_sort_key, reverse=True)


def _label_scored(
    scored: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]],
    *,
    focus_keys: set[str],
    max_candidates: int,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for score, axis, evidence, recent in scored:
        title_key = str(axis.get("title", "")).strip().lower()
        if not title_key or title_key in seen:
            continue
        seen.add(title_key)
        issues = _gate_mechanism_candidate(axis, evidence, recent, focus_keys=focus_keys)
        item = _jsonable_candidate(axis, evidence, recent, issues=issues)
        item["rerun_group"] = axis.get("rerun_group", "")
        item["score"] = score
        item["evidence_support_score"] = axis.get("evidence_support_score", score)
        tier = str(axis.get("quality_tier", "C"))
        promoted = not issues and tier in QUALITY_PROMOTION_TIERS and len([i for i in output if i.get("greenhouse_label") == "promoted_to_seed"]) < 3
        item["greenhouse_label"] = _quality_label_from_tier(tier, issues, promoted=promoted)
        if issues and "park_reason" not in item:
            item["park_reason"] = "rerun_gate_issues"
        elif not promoted and tier not in QUALITY_PROMOTION_TIERS:
            item["park_reason"] = f"quality_tier_{tier}_not_promotable"
        elif not promoted:
            item["park_reason"] = "rerun_high_quality_limit_or_review_needed"
        output.append(item)
        if len(output) >= max_candidates:
            break
    return output


def _load_rerun_payload(path: Path) -> dict[str, Any]:
    return _read_json(path)


def _render_rerun_markdown(run_date: str, payload: dict[str, Any]) -> str:
    report = {
        "generator": payload.get("generator"),
        "generator_status": payload.get("generator_status"),
        "gemini_model": payload.get("gemini_model"),
        "raw_candidate_limit": payload.get("raw_candidate_limit"),
        "min_raw_candidates": payload.get("min_raw_candidates"),
        "free_divergence": True,
        "free_divergence_start_date": "2026-05-08",
        "quality_rubric_weights": QUALITY_RUBRIC_WEIGHTS,
        "greenhouse": payload.get("raw_gemini_candidates", []),
    }
    return render_greenhouse_markdown(run_date, report)


def _render_rerun_delta(run_date: str, payload: dict[str, Any]) -> str:
    items = payload.get("raw_gemini_candidates", [])
    counts = _greenhouse_counts(items)
    tiers = Counter(str(item.get("quality_tier", "unrated")) for item in items)
    groups = Counter(str(item.get("rerun_group") or "unknown") for item in items)
    candidate_groups = Counter(str(item.get("candidate_group", "unclassified") or "unclassified") for item in items)
    lines = [
        render_frontmatter(
            f"Gemini Rerun Agenda Delta - {run_date}",
            ["research-agenda", "gemini-rerun", "agenda-delta"],
            "Historical Gemini rerun delta; does not replace formal daily agenda.",
        ).rstrip(),
        f"# Gemini Rerun Agenda Delta - {run_date}",
        "",
        "- update_scope: historical_gemini_rerun",
        "- boundary: does not replace formal daily agenda, seed folders, or paper claims.",
        f"- focus_zotero_keys: {', '.join(payload.get('focus_zotero_keys', [])) or '-'}",
        f"- generator_status: {payload.get('generator_status', '-')}",
        f"- raw_candidates: {len(items)}",
        f"- rerun_groups: {json.dumps(dict(groups), ensure_ascii=False, sort_keys=True)}",
        f"- candidate_groups: {json.dumps(dict(candidate_groups), ensure_ascii=False, sort_keys=True)}",
        f"- greenhouse_labels: {json.dumps(dict(counts), ensure_ascii=False, sort_keys=True)}",
        f"- quality_tiers: {json.dumps(dict(tiers), ensure_ascii=False, sort_keys=True)}",
        "",
        "## Strong Candidates For Review",
        "",
    ]
    strong = [item for item in items if item.get("quality_tier") in {"S", "A"}]
    if not strong:
        lines.append("- none")
    for item in strong[:12]:
        lines.append(
            f"- {item.get('title')}: tier={item.get('quality_tier')} label={item.get('greenhouse_label')} "
            f"group={item.get('rerun_group')} contribution={item.get('contribution_shape')} "
            f"score={item.get('research_quality_score')} baseline={item.get('strongest_baseline', '-')[:120]}"
        )
    lines.extend(["", "## All Candidates", ""])
    for item in items:
        lines.append(
            f"- {item.get('title')}: tier={item.get('quality_tier', '-')} "
            f"label={item.get('greenhouse_label', '-')} rerun_group={item.get('rerun_group', '-')} "
            f"candidate_group={item.get('candidate_group', '-')} score={item.get('research_quality_score', '-')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def _summarize_day(payload: dict[str, Any]) -> dict[str, Any]:
    items = payload.get("raw_gemini_candidates", [])
    text = " ".join(json.dumps(item, ensure_ascii=False).lower() for item in items)
    return {
        "run_date": payload.get("run_date"),
        "status": payload.get("status"),
        "generator_status": payload.get("generator_status"),
        "focus_key_count": len(payload.get("focus_zotero_keys", [])),
        "raw_candidates": len(items),
        "quality_tiers": dict(Counter(str(item.get("quality_tier", "unrated")) for item in items)),
        "rerun_groups": dict(Counter(str(item.get("rerun_group") or "unknown") for item in items)),
        "greenhouse_labels": dict(Counter(str(item.get("greenhouse_label", "unlabeled")) for item in items)),
        "rl_token_related_candidates": sum(1 for item in items if "rl token" in json.dumps(item, ensure_ascii=False).lower() or "rl-token" in json.dumps(item, ensure_ascii=False).lower()),
        "non_rl_token_signal_present": any(token in text for token in ["dlo", "tactile", "bimanual", "wrist", "occlusion", "contact"]),
    }


def _render_summary(output_root: Path, days: list[dict[str, Any]]) -> str:
    lines = [
        render_frontmatter(
            "Gemini Rerun Summary - 2026-04-29 to 2026-05-07",
            ["research-agenda", "gemini-rerun", "summary"],
            "Historical Gemini rerun summary for 2026-04-29 to 2026-05-07.",
        ).rstrip(),
        "# Gemini Rerun Summary - 2026-04-29 to 2026-05-07",
        "",
        "- boundary: rerun archive only; formal agenda and seed folders are unchanged.",
        f"- output_root: {rel(output_root)}",
        f"- days: {len(days)}",
        "",
        "## Daily Summary",
        "",
    ]
    for item in days:
        lines.append(
            f"- {item.get('run_date')}: status={item.get('status')} raw={item.get('raw_candidates')} "
            f"tiers={json.dumps(item.get('quality_tiers', {}), ensure_ascii=False, sort_keys=True)} "
            f"groups={json.dumps(item.get('rerun_groups', {}), ensure_ascii=False, sort_keys=True)} "
            f"rl_token_related={item.get('rl_token_related_candidates')} "
            f"non_rl_token_signal={item.get('non_rl_token_signal_present')}"
        )
    lines.extend(["", "## Cross-day Ranking Input", ""])
    all_items: list[dict[str, Any]] = []
    for summary in days:
        path = output_root / f"{summary.get('run_date')}-gemini-rerun-raw-candidates.json"
        payload = _load_rerun_payload(path)
        all_items.extend(payload.get("raw_gemini_candidates", []))
    ranked = sorted(
        all_items,
        key=lambda item: (
            {"S": 3, "A": 2, "B": 1}.get(str(item.get("quality_tier")), 0),
            int(item.get("research_quality_score") or 0),
        ),
        reverse=True,
    )
    for item in ranked[:20]:
        lines.append(
            f"- {item.get('run_date')} `{item.get('quality_tier', '-')}` {item.get('title')}: "
            f"group={item.get('rerun_group')} score={item.get('research_quality_score')} "
            f"baseline={str(item.get('strongest_baseline', '-'))[:120]}"
        )
    return "\n".join(lines).rstrip() + "\n"


def rerun_day(
    *,
    run_date: str,
    records: list[dict[str, Any]],
    output_root: Path,
    gemini_model: str,
    timeout: int,
    raw_limit: int,
    min_raw_candidates: int,
    dry_run: bool,
) -> dict[str, Any]:
    focus_keys = set(_focus_keys_from_agenda(run_date))
    out_json = output_root / f"{run_date}-gemini-rerun-raw-candidates.json"
    out_md = output_root / f"{run_date}-gemini-rerun-raw-candidates.md"
    out_delta = output_root / f"{run_date}-rerun-agenda-delta.md"
    if not focus_keys:
        payload = {
            "run_date": run_date,
            "status": "skipped_no_focus_keys",
            "generator": "gemini-rerun",
            "generator_status": "skipped:no_focus_keys",
            "gemini_model": gemini_model,
            "focus_zotero_keys": [],
            "raw_candidate_limit": raw_limit,
            "min_raw_candidates": min_raw_candidates,
            "raw_gemini_candidates": [],
        }
        if not dry_run:
            safe_write(out_json, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            safe_write(out_md, _render_rerun_markdown(run_date, payload))
            safe_write(out_delta, _render_rerun_delta(run_date, payload))
        return payload

    candidates = _mechanism_candidates(records, focus_keys=focus_keys)
    focus_records = _focus_records(records, focus_keys)
    fallback_domains = _top_domains(focus_records)
    all_scored: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]] = []
    statuses: list[str] = []
    group_outputs: dict[str, int] = {}
    prompts: dict[str, str] = {}
    for group in RERUN_GROUPS:
        prompt = _render_group_prompt(
            run_date=run_date,
            group=group,
            candidates=candidates,
            records=records,
            focus_keys=focus_keys,
            raw_limit=raw_limit,
            min_raw_candidates=min_raw_candidates,
        )
        prompts[group] = prompt
        if dry_run:
            statuses.append(f"{group}:dry_run")
            group_outputs[group] = 0
            continue
        result = run_gemini_cli(prompt, timeout_sec=timeout, model=gemini_model)
        suffix = (
            f"model={result.get('requested_model') or 'auto'}:"
            f"effective={result.get('effective_model') or 'auto'}:"
            f"fallback={str(bool(result.get('effective_fallback'))).lower()}"
        )
        if result.get("error"):
            statuses.append(f"{group}:failed:{result.get('error')}:{suffix}")
            group_outputs[group] = 0
            continue
        parsed = _extract_json_object(result.get("clean_output", ""))
        raw_items = parsed.get("candidates", []) if isinstance(parsed, dict) else []
        raw_items = [item for item in raw_items if isinstance(item, dict)]
        for item in raw_items:
            item["rerun_group"] = group
        group_outputs[group] = len(raw_items)
        statuses.append(f"{group}:success:{len(raw_items)}:{suffix}")
        all_scored.extend(
            _score_items(raw_items, records=records, focus_keys=focus_keys, fallback_domains=fallback_domains, raw_limit=raw_limit)
        )

    labelled = [] if dry_run else _label_scored(all_scored, focus_keys=focus_keys, max_candidates=12)
    for item in labelled:
        item["run_date"] = run_date
    payload = {
        "run_date": run_date,
        "status": "dry_run" if dry_run else ("success" if labelled else "partial"),
        "generator": "gemini-rerun",
        "generator_status": ";".join(statuses),
        "gemini_model": gemini_model,
        "focus_zotero_keys": sorted(focus_keys),
        "focus_evidence_sources": _source_count(focus_records),
        "raw_candidate_limit": raw_limit,
        "min_raw_candidates": min_raw_candidates,
        "rerun_groups": RERUN_GROUPS,
        "group_raw_counts": group_outputs,
        "output_json": rel(out_json),
        "output_markdown": rel(out_md),
        "output_delta": rel(out_delta),
        "history_context": _history_context(run_date),
        "dry_run_prompt_chars": {key: len(value) for key, value in prompts.items()} if dry_run else {},
        "quality_rubric_weights": QUALITY_RUBRIC_WEIGHTS,
        "workflow_contracts": WORKFLOW_CONTRACTS,
        "raw_gemini_candidates": labelled,
    }
    if not dry_run:
        safe_write(out_json, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        safe_write(out_md, _render_rerun_markdown(run_date, payload))
        safe_write(out_delta, _render_rerun_delta(run_date, payload))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="2026-04-29")
    parser.add_argument("--end-date", default="2026-05-07")
    parser.add_argument("--gemini-model", default="gemini-3.1-pro-preview")
    parser.add_argument("--idea-timeout", type=int, default=1200)
    parser.add_argument("--raw-candidate-limit", type=int, default=8)
    parser.add_argument("--min-raw-candidates", type=int, default=DEFAULT_MIN_RAW_CANDIDATES)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = vault_path(*output_root.parts)
    records = load_evidence_matrix()
    days = _date_range(args.start_date, args.end_date)
    payloads = [
        rerun_day(
            run_date=run_date,
            records=records,
            output_root=output_root,
            gemini_model=args.gemini_model,
            timeout=args.idea_timeout,
            raw_limit=args.raw_candidate_limit,
            min_raw_candidates=args.min_raw_candidates,
            dry_run=args.dry_run,
        )
        for run_date in days
    ]
    summaries = [_summarize_day(payload) for payload in payloads]
    summary_path = output_root / "2026-05-08-0429-0507-gemini-rerun-summary.md"
    if not args.dry_run:
        safe_write(summary_path, _render_summary(output_root, summaries))
    result = {
        "status": "dry_run" if args.dry_run else "done",
        "output_root": rel(output_root),
        "summary_path": rel(summary_path),
        "days": summaries,
    }
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in summaries:
            safe_print(
                f"{item['run_date']} status={item['status']} focus={item['focus_key_count']} "
                f"raw={item['raw_candidates']} tiers={json.dumps(item['quality_tiers'], ensure_ascii=False, sort_keys=True)}"
            )
        safe_print(f"SUMMARY_PATH: {rel(summary_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
