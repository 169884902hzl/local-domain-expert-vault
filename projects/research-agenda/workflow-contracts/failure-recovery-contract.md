---
title: "Failure Recovery Contract"
tags: [research-agenda, recovery, automation]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Contract for timeouts, retries, backlog, catch-up review, and non-blocking daily automation failure recovery."
---

# Failure Recovery Contract

## Principle

No single stage may silently stop the whole research workflow. Failures must be explicit, resumable, and non-destructive.

## Stage Rules

### arXiv Metadata

- Use local mirror first.
- If sync times out or fails, continue with the latest mirror and record staleness or fallback.
- Do not let a temporary arXiv API failure produce a false empty candidate day.

### Zotero Import

- New-only filtering should exclude already existing papers before import attempts.
- Import failure must be recorded with the key or arXiv ID and message.

### Claudian Reading

- Default per-paper timeout: `2700` seconds.
- Failed or unfinished reads must be written to the reading backlog.
- A resume run must skip notes already `status: done`.
- Partial reading is recoverable only when backlog evidence exists.

### Gemini

- Default timeout: `1200` seconds.
- Timeout, nonzero exit, empty output, invalid JSON, under-generation, and no-top-tier all get explicit status.
- Raw candidates or failure status must be preserved.

### Codex

- Daily review should catch up to the newest successful daily run without a completed review.
- Hard timeout must prevent indefinite hanging.
- If Codex fails, write deterministic fallback and preserve the packet.

## Recovery Labels

- `recoverable_backlog_present`
- `recoverable_gemini_retry_possible`
- `recoverable_codex_catch_up_pending`
- `blocked_missing_artifact`
- `blocked_no_resume_evidence`

## Audit Expectations

The daily quality audit must be able to answer:

- Which stage failed?
- Is the failure recoverable?
- Which file proves the recovery path exists?
- Did the failure affect idea quality, run reliability, or only scheduler status?
