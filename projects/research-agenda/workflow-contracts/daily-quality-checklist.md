---
title: "Daily Quality Checklist"
tags: [research-agenda, automation, quality]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Checklist used by the daily automation quality audit."
---

# Daily Quality Checklist

## Pipeline Completeness

- Daily run log exists.
- Run status is `success` or a recoverable `partial`.
- Agenda update is `success` or `skipped_no_focus_keys`.
- Strict KB maintenance succeeded if reading ran.
- Every failed or unfinished read has backlog evidence.

## Reading Quality

- The daily target is 10 successful deep reads unless the run is explicitly resuming a smaller backlog.
- `read_elapsed_sec` is recorded for completed reads.
- Failed reads are not silently dropped.
- Resume runs skip notes already `status: done`.

## Gemini Greenhouse

- Raw archive JSON exists when there are focus keys.
- `raw_gemini_candidates >= min_raw_candidates`, or under-generation is explicitly recorded.
- Both `evidence_bound` and `wild_engineering` are represented when free divergence is enabled.
- Each raw candidate has non-obvious claim, anti-combination test, strongest baseline, killer experiment, rescue mutation, and claim compression.
- `quality_tier`/`potential_tier` are treated as potential only; `readiness_tier` and `promotion_decision` carry seed-readiness meaning.
- C-tier candidates are not promoted to formal seeds.

## Codex Review

- Packet contains raw candidates, formal seeds, allowed actions, potential/readiness boundary, quality boundary, and evidence briefs.
- Allowed actions are exactly `accept_for_user_review / rewrite / park / reject_with_rescue`.
- Report is completed or pending for a fresh run.
- Codex does not review stale results.

## Quality Readiness

- `ready`: no FAIL or WARN audit findings.
- `needs_attention`: no blocking failure, but quality or recovery issues need inspection.
- `blocked`: missing artifact, invalid packet, unsafe promotion, or non-recoverable failure.
