---
title: "Daily Pipeline Contract"
tags: [research-agenda, automation, quality]
created: "2026-05-08"
updated: "2026-05-21"
type: "permanent"
status: "done"
summary: "Contract for daily arXiv candidate selection, Zotero import, Claudian reading, agenda update, and quality audit."
---

# Daily Pipeline Contract

## Scope

This contract covers the scheduled daily arXiv workflow:

arXiv mirror sync -> candidate ranking -> Zotero new-only import -> Claudian deep reading -> strict KB maintenance -> evidence matrix update -> Gemini greenhouse -> mandatory Gemini-DeepSeek battle -> Codex review pending marker -> daily quality audit.

## Inputs

- Local arXiv metadata mirror, preferably `mirror-first`.
- Existing Zotero items and local done notes for new-only filtering.
- Daily candidate window, default `60` days.
- Read target, default `min_new_imports = 10`.
- Gemini settings: `gemini-divergent`, timeout `1200`, raw candidate limit `8`, minimum raw candidates `6`, seed-candidate review limit `3`.
- DeepSeek battle settings: OpenCode selector `deepseek/deepseek-v4-pro(max)` with provider model id `deepseek-v4-pro(max)`, timeout `1200`, candidate coverage `all` raw greenhouse candidates.

## Success Criteria

`pipeline_success` requires:

- run log exists for the date;
- run status is `success`;
- agenda update status is `success` or `skipped_no_focus_keys`;
- strict KB maintenance succeeded when reading ran;
- all failed or unfinished reads are written to the reading backlog;
- quality audit was generated after the run.
- when Gemini greenhouse runs on or after `2026-05-14`, mandatory Gemini-DeepSeek battle status is `success`.

`quality_success` is stricter:

- enough successful reads for the day's target or an explicit recovery/backlog reason;
- Gemini raw archive exists when there are focus keys;
- raw candidates meet `min_raw_candidates` unless an under-generation warning is recorded;
- C-tier candidates are not promoted to seed candidates, formal rehearsal packets, or active seed records;
- mandatory model battle covers all raw Gemini candidates for the date;
- Codex review is either pending for a fresh run or completed for a past run.

## Partial States

- `read_partial_recoverable`: at least one read failed or remains backlog, but the backlog is present and resumable.
- `gemini_partial_greenhouse_saved`: Gemini failed, timed out, or under-generated, but raw or failure status was preserved.
- `mandatory_model_battle_partial`: DeepSeek or Gemini mutation failed; greenhouse artifacts remain preserved, but the daily idea stage is not success.
- `codex_review_pending`: daily run completed before the review task; review must catch up later.
- `quality_no_top_tier_seed_today`: Gemini ran but no candidate reached seed readiness after potential/readiness separation. This is not a failure by itself.
- `blocked_missing_artifact`: required run log, agenda delta, greenhouse archive, or backlog is missing.

## Red Lines

- Do not call Gemini when there are no successfully read focus keys.
- Do not mark C-tier candidates as seed candidates, formal rehearsal packets, or active seed records.
- Do not treat `top1_candidate` as confirmed top-1 paper quality.
- Do not let a failed read disappear without backlog or retry evidence.
- Do not let Codex review stale results when a newer successful daily run is pending.
- Do not mark a `gemini-divergent` agenda update as clean success after `2026-05-14` unless the mandatory Gemini-DeepSeek battle succeeds.

## Required Report Fields

The run log or quality audit must expose:

- `status`
- `agenda_update_status`
- `new_imports_read_success`
- `read_failed_or_backlog`
- `gemini_generator_status`
- `raw_gemini_candidates`
- `quality_tier_counts`
- `quality_tier_semantics`
- `potential_tier_counts`
- `readiness_tier_counts`
- `mandatory_model_battle_status`
- `mandatory_model_battle_report`
- `seed_candidate_count`
- `codex_review_state`
- `quality_readiness`
