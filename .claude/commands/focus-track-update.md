Update a focused research track from local evidence.

Argument: $ARGUMENTS

Use when the user asks to update a focused track, especially:

```powershell
python .claude/scripts/focus_track_update.py --track rl-token-vla-online-rl
```

Required workflow:

```powershell
python .claude/scripts/focus_track_update.py --track $ARGUMENTS
python .claude/scripts/focus_track_review.py --track $ARGUMENTS --json
python .claude/scripts/audit_focus_tracks.py --track $ARGUMENTS --json
```

Rules:
- The track may generate daily deltas, dashboards, evidence filters, hypotheses, and replication plans.
- It must not promote a seed into a formal research conclusion.
- Paper claims must cite local `wiki/topics/` evidence or be explicitly marked `unverified`.
- If audit fails, report `partial` and the exact failing gate.
