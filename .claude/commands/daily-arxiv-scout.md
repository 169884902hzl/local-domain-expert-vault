Run the daily arXiv embodied-AI scout once.

Argument: $ARGUMENTS (optional extra args for the Python script)

Required workflow:
1. Preview only when the user explicitly wants a check:
```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --max-candidates 10
```
2. Run the real daily pass:
```powershell
python .claude/scripts/daily_arxiv_pipeline.py --once $ARGUMENTS
```
3. Verify completion after the run:
```powershell
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
python .claude/scripts/audit_research_agenda.py --json
python .claude/scripts/zotero_import.py --preflight --json
python .claude/scripts/audit_scheduled_tasks.py --json
```
4. If Zotero write credentials, Claude reading, strict KB maintenance, or agenda update fail, report `partial` and the exact failed gate. Do not claim papers were imported/read.
5. Open or report these generated paths:
- `projects/arxiv-daily/YYYY-MM-DD-candidates.jsonl`
- `projects/arxiv-daily/review_queue/YYYY-MM-DD-review.md`
- `projects/arxiv-daily/YYYY-MM-DD-run.md`
- `projects/arxiv-daily/YYYY-MM-DD-reading-backlog.md`
- `projects/research-agenda/daily/YYYY-MM-DD-agenda-delta.md`
- `projects/research-agenda/agenda-dashboard.md`
- `projects/ideas/YYYY-MM-DD-embodied-ai-ideas.md` (compatibility pointer only)
- `projects/ideas/YYYY-MM-DD-gemini-idea-prompt.md`

Rules:
- `top1_candidate` means high-priority candidate by local scoring, not guaranteed top-tier truth.
- `venue_auto_import` means an accepted/published top-venue paper that is relevant to embodied AI / robotics; import it to Zotero without manual review, but do not treat it as automatically correct.
- Do not import review_queue papers automatically except when the daily new-import floor needs fill candidates; those fill imports still require relevance and audit.
- Imported papers that exceed the daily reading cap must be listed in `projects/arxiv-daily/YYYY-MM-DD-reading-backlog.md`.
- New daily imports default to being deep-read. `--max-read` defaults to `--min-new-imports`.
- A read is successful only when the local topic note for that Zotero key is `status: done`; Claude CLI exit code alone is not enough.
- After reading, strict KB maintenance must run through `.claude/scripts/fix_strict_kb_after_read.py`.
- Final success requires `audit_kb.py --strict-reading --strict-concepts` and `audit_research_agenda.py --json` to pass.
- Scheduled-task health is separate from a one-off run; use `audit_scheduled_tasks.py --json` to verify XML, wrapper paths, logs, and Task Scheduler query status.
- Do not use external web search beyond arXiv unless the user explicitly approves.
- Gemini is a manual divergent-thinking side channel. Generate the prompt file from the long-term agenda context, but do not call Gemini automatically.
- The daily output is an agenda delta, not a final idea list. Long-term ideas live under `projects/research-agenda/idea_bank/`.
- If Claude or agenda update fails, do not fabricate high-quality ideas; report `partial` and keep evidence gaps visible.

Answer format:
- `success` / `partial` / `unverified`
- Candidate count, top1 candidate count, venue_auto_import count, review queue count
- Zotero preflight and import status
- New import count and new read success count
- Strict KB maintenance status, KB audit status, and research agenda audit status
- Agenda delta path, agenda update status, Gemini prompt path, and any backlog
