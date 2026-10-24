Update the long-term research agenda from local done-paper evidence.

Argument: $ARGUMENTS

Use when the user asks to update the research agenda, idea bank, problem pool, or long-term idea system.

Required workflow:

```powershell
python .claude/scripts/research_agenda_update.py $ARGUMENTS
```

Common examples:

```powershell
python .claude/scripts/research_agenda_update.py --all
python .claude/scripts/research_agenda_update.py --run-date 2026-04-29 --zotero-keys A8TNG2G6,FXDXFRHQ,VQABQ7UD
python .claude/scripts/research_agenda_update.py --all --dry-run
```

Rules:
- This command updates `projects/research-agenda/`.
- It must not treat daily output as validated final ideas.
- Promoted ideas still need `audit_research_agenda.py` and human approval.
- Use all available local `status: done` evidence when updating seeds; do not generate one idea per paper.
- After updating, run:
```powershell
python .claude/scripts/audit_research_agenda.py --json
```
- If the audit fails, report `partial` and the failing gate instead of presenting the agenda as complete.
