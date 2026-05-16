Show the long-term research agenda workflow.

Key paths:
- `projects/research-agenda/agenda-dashboard.md`
- `projects/research-agenda/evidence/evidence_matrix.jsonl`
- `projects/research-agenda/problem_pool/`
- `projects/research-agenda/idea_bank/`
- `projects/research-agenda/daily/YYYY-MM-DD-agenda-delta.md`

Commands:

```powershell
python .claude/scripts/research_agenda_extract.py --all --dry-run
python .claude/scripts/research_agenda_update.py --all
python .claude/scripts/research_agenda_update.py --run-date YYYY-MM-DD --zotero-keys KEY1,KEY2
python .claude/scripts/research_agenda_review.py
python .claude/scripts/audit_research_agenda.py --json
python .claude/scripts/audit_scheduled_tasks.py --json
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1
```

Meaning:
- Daily arXiv adds evidence and updates the agenda.
- High-quality ideas mature inside `idea_bank/`, not inside daily idea files.
- `promoted` ideas must pass the audit gate before becoming experiment proposals.

Claudian responsibility:
- Treat `daily/YYYY-MM-DD-agenda-delta.md` as an evidence delta, not a final idea list.
- Use the long-term `evidence_matrix.jsonl`, `problem_pool/`, and prior `idea_bank/` state before proposing idea changes.
- Keep weak candidates in `seed`; do not promote without enough local `status: done` evidence, recent evidence, similar-work check, baseline, metrics, pilot, risk review, and human approval.
- Treat `audit_research_agenda.py --json` WARN as a real quality signal when all ideas remain seed or when similar-work / experiment gates are placeholders.
- Always report the current maturity stage: `seed`, `developing`, `promoted`, `pilot-ready`, `rejected`, or `archived`.
- Weekly scheduled review runs Sunday 20:00 by default and writes artifacts under `projects/research-agenda/reviews/`; it does not apply promotions automatically.
