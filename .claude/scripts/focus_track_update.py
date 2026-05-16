"""Update a focused research track from local evidence."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from focus_track_common import (
    AGENDA_EVIDENCE_MATRIX,
    FOCUS_ROOT,
    TRACK_STATES,
    dedupe_records,
    load_jsonl,
    note_status,
    note_title,
    rel,
    render_frontmatter,
    safe_write,
    strip_quotes,
    today,
    topic_path_from_stem,
    track_config,
    track_evidence_path,
    track_registry_payload,
    track_root,
    wikilink,
    write_jsonl,
)
from kb_common import safe_print, vault_path
from research_agenda_extract import extract_from_note


def _source_stem(record: dict[str, Any]) -> str:
    return Path(str(record.get("source_note", ""))).stem


def _match_reasons(record: dict[str, Any], config: dict[str, Any]) -> list[str]:
    similar_stems = {item["stem"] for item in config["similar_work"]}
    source_stem = _source_stem(record)
    reasons: list[str] = []
    if str(record.get("source_note", "")) == config["core_note"]:
        reasons.append("core_paper")
    if source_stem in similar_stems:
        reasons.append("similar_work")
    haystack = " ".join(
        [
            str(record.get("source_title", "")),
            str(record.get("statement", "")),
            " ".join(str(item) for item in record.get("domains", [])),
            " ".join(str(item) for item in record.get("tags", [])),
        ]
    ).lower()
    for keyword in config["keywords"]:
        if keyword.lower() in haystack:
            reasons.append(f"keyword:{keyword}")
    return list(dict.fromkeys(reasons))


def _focus_record(record: dict[str, Any], config: dict[str, Any], run_date: str) -> dict[str, Any] | None:
    reasons = _match_reasons(record, config)
    if not reasons:
        return None
    selected = dict(record)
    selected["track_relevance"] = reasons
    selected["track_run_date"] = run_date
    return selected


def collect_focus_evidence(track: str, run_date: str) -> list[dict[str, Any]]:
    config = track_config(track)
    records = load_jsonl(AGENDA_EVIDENCE_MATRIX)
    core_path = vault_path(*config["core_note"].split("/"))
    if core_path.exists() and note_status(core_path) == "done":
        records.extend(extract_from_note(core_path, run_date=run_date))
    selected = [_focus_record(record, config, run_date) for record in records]
    return dedupe_records([record for record in selected if record is not None])


def _source_count(records: list[dict[str, Any]]) -> int:
    return len({record.get("source_note") for record in records})


def _claim_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        counts[str(record.get("claim_type", "unknown"))] += 1
    return counts


def _similar_items(config: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for item in config["similar_work"]:
        path = topic_path_from_stem(item["stem"])
        items.append(
            {
                **item,
                "path": path,
                "exists": path.exists(),
                "status": note_status(path) if path.exists() else "missing",
                "title": note_title(path) if path.exists() else item["label"],
            }
        )
    return items


def render_dashboard(track: str, records: list[dict[str, Any]]) -> str:
    config = track_config(track)
    root = track_root(track)
    core_path = vault_path(*config["core_note"].split("/"))
    similar_done = [item for item in _similar_items(config) if item["status"] == "done"]
    claim_counts = _claim_counts(records)
    lines = [
        render_frontmatter(
            "RL Token Focus Track Dashboard",
            ["focus-track", "RL", "VLM", "robot-learning"],
            "Current state of the RL Token focused research track.",
        ).rstrip(),
        "# RL Token Focus Track Dashboard",
        "",
        f"- track: `{track}`",
        "- current_state: `replication-ready`",
        f"- allowed_states: {', '.join(f'`{state}`' for state in TRACK_STATES)}",
        f"- core_paper: {wikilink(core_path.stem, config['core_title'])}",
        f"- core_paper_status: `{note_status(core_path) if core_path.exists() else 'missing'}`",
        f"- evidence_records: {len(records)}",
        f"- evidence_sources: {_source_count(records)}",
        f"- similar_work_done: {len(similar_done)}",
        "- codex_second_pass: `done`",
        "- current_shortlist: [[rl-token-failure-memory|RL Token Failure Memory]]",
        "- core_paper_extraction: `pdf_pass_1_complete`",
        "- pilot_config_draft: `projects/focus-tracks/rl-token-vla-online-rl/experiments/pilot-run-config-draft.json`",
        "",
        "## Core Hypothesis",
        "",
        "A pretrained VLA can become a sample-efficient online RL substrate if its task-relevant hidden representation is exposed as an RL token, while a small actor-critic head performs local action refinement under VLA anchoring.",
        "",
        "## Gate Snapshot",
        "",
        "- paper_understood: requires `wiki/topics/xu2026token.md` to be `status: done` and pass strict KB audit.",
        "- similar_work_checked: `done`; reviewed pressure table is in [[similar-work-map|Similar Work Map]].",
        "- mechanism_clear: requires the track to distinguish RL token, actor-critic RL head, and VLA anchoring.",
        "- replication_plan_ready: `done`; low-cost offline pilot lock is in [[critic-first-failure-memory-spec|Critic-First Failure Memory Spec]].",
        "- extension_claim_safe: no paper claim can be promoted without local evidence or explicit `unverified` status.",
        "",
        "## Evidence By Claim Type",
        "",
    ]
    if not claim_counts:
        lines.append("- evidence_gap: no selected evidence records yet.")
    else:
        lines.extend(f"- {name}: {count}" for name, count in sorted(claim_counts.items()))
    lines.extend(
        [
            "",
            "## Working Files",
            "",
            f"- [[core-paper|Core Paper]]",
            f"- [[core-paper-extraction-checklist|RL Token Core Paper Extraction Checklist]]",
            f"- [[similar-work-map|Similar Work Map]]",
            f"- [[minimal-replication-plan|Minimal Replication Plan]]",
            f"- [[critic-first-failure-memory-spec|Critic-First Failure Memory Spec]]",
            f"- [[offline-pilot-v0-runbook|Offline Pilot v0 Runbook]]",
            f"- [[baseline-checklist|RL Token Failure Memory Baseline Checklist]]",
            f"- [[frozen-vla-small-rl-head|Frozen VLA Plus Small RL Head]]",
            f"- [[rl-token-failure-memory|RL Token Failure Memory]]",
            f"- schema: `{rel(root / 'experiments' / 'memory-index-schema.json')}`",
            f"- pilot_config_draft: `{rel(root / 'experiments' / 'pilot-run-config-draft.json')}`",
            f"- results_template: `{rel(root / 'experiments' / 'pilot-results-template.csv')}`",
            f"- run_template: `{rel(root / 'experiments' / 'runs' / '_template')}/`",
            f"- validator: `.claude/scripts/validate_rl_token_pilot.py`",
            f"- evidence: `{rel(root / 'evidence' / 'track_evidence.jsonl')}`",
            f"- daily: `{rel(root / 'daily')}/`",
            "",
            "## Blockers",
            "",
            "- PDF pass 1 is complete; exact hardware/controller, code configs, and per-task plot data still need code/author-level extraction before hardware or paper-writing claims.",
            "- no pilot result yet for `critic_memory_main` versus `rl_head_no_memory` and `random_memory_negative`.",
            "- similar-work pressure remains high around RACER, OmniVLA-RL, reflection memory, imperfect demonstrations, and long-horizon VLA planning.",
            "- no formal extension claim is accepted yet.",
            "",
            "## Next Experiment",
            "",
            "- primary_mechanism: `critic_input`",
            "- spec: [[critic-first-failure-memory-spec|Critic-First Failure Memory Spec]]",
            "- runbook: [[offline-pilot-v0-runbook|Offline Pilot v0 Runbook]]",
            "- paper_extraction: [[core-paper-extraction-checklist|RL Token Core Paper Extraction Checklist]]",
            f"- config_draft: `{rel(root / 'experiments' / 'pilot-run-config-draft.json')}`",
            "- baseline_checklist: [[baseline-checklist|RL Token Failure Memory Baseline Checklist]]",
            "- main_test: compare `critic_memory_main` against `rl_head_no_memory` and `random_memory_negative`.",
            "- minimum_loop: build frozen-token memory index, train no-memory head, train critic-memory head, train random-memory negative.",
            "- validation: run `validate_rl_token_pilot.py` before interpreting any pilot output.",
            "- claim_boundary: replication-ready only; accepted paper claims remain empty until pilot evidence exists.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_core_paper(track: str) -> str:
    config = track_config(track)
    core_path = vault_path(*config["core_note"].split("/"))
    status = note_status(core_path) if core_path.exists() else "missing"
    return "\n".join(
        [
            render_frontmatter(
                "RL Token Core Paper",
                ["focus-track", "core-paper", "RL", "VLM"],
                "Structured entry point for the RL Token paper.",
            ).rstrip(),
            "# RL Token Core Paper",
            "",
            f"- local_note: {wikilink(core_path.stem, config['core_title'])}",
            f"- local_status: `{status}`",
            "- arxiv: [2604.23073v1](http://arxiv.org/abs/2604.23073v1)",
            "- official_pdf: [Physical Intelligence PDF](https://www.pi.website/download/rlt.pdf)",
            "- extraction_checklist: [[core-paper-extraction-checklist|RL Token Core Paper Extraction Checklist]]",
            "- pilot_config_draft: `projects/focus-tracks/rl-token-vla-online-rl/experiments/pilot-run-config-draft.json`",
            "",
            "## Mechanism",
            "",
            "- **RL token**: a compact VLA readout representation used as the interface between pretrained VLA knowledge and online RL.",
            "- **Actor-critic RL head**: a small policy/value module trained on the RL token to refine actions for the target task.",
            "- **VLA anchoring**: a regularization/safety constraint that keeps the learned policy close to the pretrained VLA behavior.",
            "",
            "## Interpretation",
            "",
            "The mechanism is a three-part composition, not a single trick: representation interface + lightweight RL head + anchoring. A later extension must specify which part changes and why the RL token interface makes the change more sample-efficient than a normal adapter or full-model fine-tune.",
            "",
            "## Extraction Snapshot",
            "",
            "- pdf_pass_1: `done`",
            "- token: learned special-token readout over final-layer VLA embeddings; figure-level dimension `1 x 2048`.",
            "- online RL: TD3-style off-policy actor-critic over action chunks, with VLA reference-action anchoring.",
            "- action setup: `C=10`, 50 Hz, 14-dimensional per-step action in the original robot setting.",
            "- head setup: small MLP actor/critic; paper reports 2-layer hidden 256 for most tasks and 3-layer hidden 512 for screw installation.",
            "- observation setup: two wrist cameras plus one base camera, with task-dependent proprioception.",
            "- unresolved: exact hardware/controller, full RL-token transformer hyperparameters, exact optimizer/config values, exact plot data.",
            "",
            "## Remaining Open Extraction Tasks",
            "",
            "- verify exact robot platform, gripper/controller setup, and reset protocol from code or author materials.",
            "- map RL token encoder/decoder depth, heads, optimizer, LR, batch size, and exact actor-critic hyperparameters if code or appendix becomes available.",
            "- extract exact per-task success/throughput values from plot data before using numbers in a paper claim.",
            "- compare whether OpenVLA / Octo hidden states can approximate the same token interface.",
        ]
    ).rstrip() + "\n"


def render_similar_work(track: str) -> str:
    config = track_config(track)
    lines = [
        render_frontmatter(
            "RL Token Similar Work Map",
            ["focus-track", "similar-work", "RL", "VLM"],
            "Local similar-work checklist for the RL Token track.",
        ).rstrip(),
        "# RL Token Similar Work Map",
        "",
        "This file is a checklist, not a novelty claim. A work counts only when the local topic note exists and is `status: done`.",
        "",
        "## Local Similar Work",
        "",
    ]
    for item in _similar_items(config):
        link = wikilink(item["stem"], item["title"]) if item["exists"] else item["label"]
        lines.append(f"- {link}: status=`{item['status']}`; role={item['role']}")
    lines.extend(
        [
            "",
            "## Reviewed Pressure Table",
            "",
            "| Pressure | Why It Matters | Track Response |",
            "|---|---|---|",
            "| RL Token | establishes frozen VLA token + small actor-critic + anchoring | our extension must keep this interface isolated |",
            "| OmniVLA-RL | nearby VLA online RL direction | do not claim broad VLA+RL novelty |",
            "| OpenVLA / Octo | open representation baselines | use as low-cost token substitutes only with explicit boundary |",
            "| VLA-adapter | small adaptation/head pressure | compare memory critic against generic small-head capacity |",
            "| RACER / reflection memory | language-level failure-memory pressure | include prompt/reflection memory control before novelty claim |",
            "| imperfect demonstrations | failure data can help without retrieval critic | separate retrieval-conditioned critic from data filtering |",
            "",
            "## Safe Research Question",
            "",
            "Can retrieved failure memory injected into a critic over frozen VLA/RL-token features beat no-memory, random-memory, actor-memory, and prompt/reflection controls without breaking VLA anchoring?",
            "",
            "## Risk Questions",
            "",
            "- Does another VLA work already train a small RL/action head on frozen representations?",
            "- Is RL Token novel because of the representation interface, the head, the anchoring, or the real-robot online protocol?",
            "- If a proposed extension adds memory, tactile, or DLO state, where does that signal enter: VLA input, RL token readout, or RL head state?",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_hypothesis() -> str:
    return "\n".join(
        [
            render_frontmatter(
                "Frozen VLA Plus Small RL Head",
                ["focus-track", "hypothesis", "RL", "VLM"],
                "Seed hypothesis for testing RL token style online adaptation.",
                status="active",
            ).rstrip(),
            "# Frozen VLA Plus Small RL Head",
            "",
            "- state: `seed`",
            "- hypothesis: freezing most of a pretrained VLA and training a small actor-critic head on a task-relevant token is more stable than full-model online RL fine-tuning.",
            "- minimum_test: compare frozen-token head, action-head-only tuning, no-anchor head, and full fine-tuning on a low-cost manipulation benchmark.",
            "- required_evidence: local evidence from `track_evidence.jsonl` plus at least one pilot metric.",
            "- promotion_rule: cannot move beyond `seed` until the pilot has baseline, metric, failure analysis, and similar-work check.",
        ]
    ).rstrip() + "\n"


def render_experiment() -> str:
    return "\n".join(
        [
            render_frontmatter(
                "RL Token Minimal Replication Plan",
                ["focus-track", "experiment", "RL", "VLM"],
                "Low-cost replication plan for RL Token style VLA online RL.",
            ).rstrip(),
            "# RL Token Minimal Replication Plan",
            "",
            "## Pilot",
            "",
            "- environment: LIBERO, ManiSkill, or a simplified insertion/assembly simulator before real robot.",
            "- model: frozen OpenVLA/Octo-style encoder or a VLA-compatible visual-language representation if full VLA action interface is unavailable.",
            "- token: compare final hidden state, action-token hidden state, pooled visual-language token, and random projection.",
            "",
            "## Baseline",
            "",
            "- BC-only or pretrained VLA action head without RL.",
            "- small RL head without VLA anchoring.",
            "- full action-head fine-tune where feasible.",
            "- random/frozen visual feature RL head as a negative control.",
            "",
            "## Metric",
            "",
            "- success rate.",
            "- sample steps to reach a fixed success threshold.",
            "- task completion time or hardest-stage duration.",
            "- policy drift from pretrained action distribution.",
            "",
            "## Failure",
            "",
            "- reward hacking or shortcut policy.",
            "- token does not encode contact-relevant state.",
            "- RL head overfits task identity instead of using VLA representation.",
            "- anchor too strong blocks improvement, or too weak destroys pretrained skill.",
        ]
    ).rstrip() + "\n"


def render_claim_gate() -> str:
    return "\n".join(
        [
            render_frontmatter(
                "RL Token Paper Claim Gate",
                ["focus-track", "paper-claims", "RL", "VLM"],
                "Rules for promoting RL Token track claims.",
            ).rstrip(),
            "# RL Token Paper Claim Gate",
            "",
            "- accepted_claims_file: `paper-claims/accepted_claims.jsonl`",
            "- default_claim_state: `unverified`",
            "- allowed_track_states: `seed`, `replication-ready`, `extension-candidate`, `blocked`",
            "",
            "## Gate Rules",
            "",
            "- A claim must cite a local `wiki/topics/` note or be explicitly marked `unverified`.",
            "- An extension cannot be just `add memory`, `add tactile`, or `add DLO`; it must explain why the RL token interface is the right place for the added signal.",
            "- A replication claim must include baseline, metric, pilot setup, and failure mode.",
            "- Automation can summarize and audit; it cannot promote a claim to a formal research conclusion.",
        ]
    ).rstrip() + "\n"


def render_daily_delta(track: str, records: list[dict[str, Any]], run_date: str) -> str:
    config = track_config(track)
    sources = sorted({str(record.get("source_note", "")) for record in records})
    similar_done = [item for item in _similar_items(config) if item["status"] == "done"]
    lines = [
        render_frontmatter(
            f"RL Token Focus Delta - {run_date}",
            ["focus-track", "daily", "RL", "VLM"],
            "Daily focused-track delta for RL Token.",
        ).rstrip(),
        f"# RL Token Focus Delta - {run_date}",
        "",
        f"- track: `{track}`",
        "- state: `replication-ready`",
        f"- evidence_records_selected: {len(records)}",
        f"- evidence_sources_selected: {len(sources)}",
        f"- similar_work_done: {len(similar_done)}",
        "",
        "## Today Added Or Refreshed",
        "",
        "- refreshed track dashboard, core-paper entry, similar-work map, claim gate, and minimal replication plan.",
        "- regenerated `evidence/track_evidence.jsonl` from local done-paper evidence and the RL Token note.",
        "- kept [[rl-token-failure-memory|RL Token Failure Memory]] as `replication-ready` for experiment design, not as a promoted research claim.",
        "- kept critic-side failure memory as the primary mechanism and linked the offline pilot artifacts.",
        "",
        "## Manual Review Delta",
        "",
        "- reviewed_seed_source: [[2026-04-30-seed-quality-review|Manual Seed Quality Review - 2026-04-30]]",
        "- strongest_rewrite_candidate: `RL-token-mediated failure memory for online robot recovery`",
        "- decision: merge failure-memory and VLA-constraint seeds into the RL Token track as one mechanism hypothesis.",
        "- selected_mechanism: retrieved failure traces condition a value-risk critic over RL-token features.",
        "- ablations: actor memory, actor+critic memory, prompt memory, random memory, and later anchor/reward variants.",
        "",
        "## Local Evidence Sources",
        "",
    ]
    if not sources:
        lines.append("- evidence_gap: no local focus evidence selected.")
    for source in sources[:20]:
        lines.append(f"- {wikilink(Path(source).stem, Path(source).stem)}")
    lines.extend(
        [
            "",
            "## Replication Tasks",
            "",
            "- choose one low-cost environment before real robot.",
            "- implement token-readout comparisons before claiming RL Token generality.",
            "- run critic-memory vs no-memory and random-memory controls first.",
            "- define anchor metric and policy drift check.",
            "",
            "## Risks",
            "",
            "- exact experimental setup remains partially unverified until PDF/code details are extracted.",
            "- similar work can still invalidate a naive novelty claim.",
            "- no extension claim is mature today.",
            "- `replication-ready` means experiment spec is ready, not that a paper claim is accepted.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _write_if_missing(path: Path, content: str, *, dry_run: bool) -> None:
    if path.exists():
        safe_print(f"UNCHANGED existing: {rel(path)}")
        return
    safe_write(path, content, dry_run=dry_run, backup=True)


def run_update(args: argparse.Namespace) -> int:
    config = track_config(args.track)
    run_date = args.run_date or today()
    records = collect_focus_evidence(args.track, run_date)
    root = track_root(args.track)
    safe_print(
        "FOCUS_TRACK_UPDATE "
        f"track={args.track} records={len(records)} sources={_source_count(records)} dry_run={args.dry_run}"
    )
    if args.dry_run:
        safe_print(f"DRY-RUN would update: {rel(root)}")
        return 0

    for directory in [
        FOCUS_ROOT,
        root / "evidence",
        root / "hypotheses",
        root / "experiments",
        root / "similar-work",
        root / "paper-claims",
        root / "daily",
        root / "reviews",
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    safe_write(FOCUS_ROOT / "track-registry.json", json.dumps(track_registry_payload(), ensure_ascii=False, indent=2) + "\n", dry_run=False, backup=True)
    write_jsonl(track_evidence_path(args.track), records, dry_run=False)
    safe_write(root / "track-dashboard.md", render_dashboard(args.track, records), dry_run=False, backup=True)
    _write_if_missing(root / "core-paper.md", render_core_paper(args.track), dry_run=False)
    _write_if_missing(root / "similar-work" / "similar-work-map.md", render_similar_work(args.track), dry_run=False)
    _write_if_missing(root / "hypotheses" / "frozen-vla-small-rl-head.md", render_hypothesis(), dry_run=False)
    _write_if_missing(root / "experiments" / "minimal-replication-plan.md", render_experiment(), dry_run=False)
    safe_write(root / "paper-claims" / "claim-gate.md", render_claim_gate(), dry_run=False, backup=True)
    _write_if_missing(root / "paper-claims" / "accepted_claims.jsonl", "", dry_run=False)
    _write_if_missing(root / "decision-log.md", render_frontmatter("RL Token Decision Log", ["focus-track", "decision-log"], "Decision log for the RL Token track.") + "# RL Token Decision Log\n\n- no promoted research claim yet.\n", dry_run=False)
    delta_path = root / "daily" / f"{run_date}-focus-delta.md"
    safe_write(delta_path, render_daily_delta(args.track, records, run_date), dry_run=False, backup=True)
    safe_print(f"FOCUS_TRACK_ROOT: {rel(root)}")
    safe_print(f"FOCUS_TRACK_DELTA: {rel(delta_path)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run_update(args)


if __name__ == "__main__":
    raise SystemExit(main())
