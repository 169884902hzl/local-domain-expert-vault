Review long-term research agenda idea maturity.

Argument: $ARGUMENTS

Required workflow:

```powershell
python .claude/scripts/research_agenda_review.py $ARGUMENTS
python .claude/scripts/audit_research_agenda.py --json
```

Use `--apply` only if the user explicitly wants folder state moves.

Rules:
- Do not promote ideas that fail evidence, novelty, similar-work, pilot, baseline, metric, or risk gates.
- Gemini output can only be used as seed material until it passes local evidence review.
