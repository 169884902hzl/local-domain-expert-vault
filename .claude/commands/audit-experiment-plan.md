Audit a local experiment plan for evidence-grounded proposal readiness.

Argument: $ARGUMENTS (path to a plan under `projects/experiments/`)

Run:
```powershell
python .claude/scripts/audit_experiment_plan.py "$ARGUMENTS"
```

Use JSON when machine-readable output is needed:
```powershell
python .claude/scripts/audit_experiment_plan.py "$ARGUMENTS" --json
```

Rules:
1. PASS means the draft is structurally complete and evidence-grounded enough for human review.
2. WARN means it can be discussed, but evidence gaps must be resolved before treating it as pilot-ready.
3. FAIL means do not use the plan as an experiment proposal.
4. Never approve a plan automatically; the user must approve `decision_status`.

Report format:
- Audit status.
- Errors and warnings with concrete section names.
- Evidence count and missing coverage.
- Recommended next action.
