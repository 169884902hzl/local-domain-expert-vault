---
title: "Daily Automation Intake And Routing"
tags: [research-agenda, automation, routing]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Routing rules for deciding whether to read, resume, run Gemini, run Codex, or stop with an honest state."
---

# Daily Automation Intake And Routing

## Routing Table

| Condition | Route | Honest State |
|---|---|---|
| No arXiv mirror and search API failed | Stop candidate stage, keep stale mirror/cache evidence if available | `blocked_missing_source` |
| Mirror available but Zotero duplicate filter unavailable | Continue with local run, record prefilter failure | `partial_prefilter_unavailable` |
| Import created keys | Deep read up to target | `reading_in_progress` |
| Backlog keys exist and user requested resume | Resume backlog, skip done notes | `resume_backlog` |
| A read fails or times out | Record backlog and continue next key | `read_partial_recoverable` |
| No successful focus keys | Do not run Gemini | `skipped_no_focus_keys` |
| Focus keys exist | Run Gemini greenhouse | `gemini_greenhouse_required` |
| Gemini under-generates | Run one divergent retry | `gemini_under_generated_retry` |
| Gemini produces no S/A in free-divergence mode | Run quality rescue retry | `quality_rescue_retry` |
| Codex scheduled before daily completion | Skip and catch up later | `skipped_waiting_for_daily_pipeline` |
| Daily success but no Codex report | Prepare or catch up daily Codex review | `codex_review_pending` |

## Stop Conditions

Stop without pretending success when:

- required local artifacts are missing;
- JSON artifacts are invalid;
- C-tier ideas are promoted;
- a failed read has no backlog or recovery evidence;
- Codex packet lacks raw candidates despite Gemini archive existing.

## Non-Stop Conditions

Continue with explicit partial state when:

- arXiv live API fails but mirror is available;
- one paper read fails but backlog is written;
- Gemini has no S/A candidates but raw candidates are preserved;
- Codex fails but fallback report and packet are written.
