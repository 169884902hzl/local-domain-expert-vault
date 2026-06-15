Report focused research track status.

Argument: $ARGUMENTS

Required workflow:

```powershell
python .claude/scripts/focus_track_review.py --track $ARGUMENTS --json
python .claude/scripts/audit_focus_tracks.py --track $ARGUMENTS --json
```

For RL Token, also check local retrieval:

```powershell
python .claude/scripts/kb_search.py "RL Token VLA online RL" --semantic --limit 12
```

Status language:
- `success`: all review/audit gates pass.
- `partial`: core files exist but one or more gates fail.
- `unverified`: the claim depends on external PDF/code details or experiments not yet in the vault.
