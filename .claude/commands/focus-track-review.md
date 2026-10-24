Review a focused research track gate state.

Argument: $ARGUMENTS

Required workflow:

```powershell
python .claude/scripts/focus_track_review.py --track $ARGUMENTS --json
python .claude/scripts/audit_focus_tracks.py --track $ARGUMENTS --json
```

Review gates:
- `paper_understood`
- `similar_work_checked`
- `mechanism_clear`
- `replication_plan_ready`
- `extension_claim_safe`

Do not promote claims automatically. A review can recommend next actions only.
