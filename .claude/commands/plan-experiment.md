Generate an evidence-grounded experiment plan from local vault notes.

Argument: $ARGUMENTS (research question or direction)

Use this command when the user asks for 实验规划, 设计实验, 实验方案, 怎么验证, or 怎么做实验.

Required workflow:
1. Generate the draft from local evidence only:
```powershell
python .claude/scripts/plan_experiment.py "$ARGUMENTS"
```
2. Open the generated file under `projects/experiments/`.
3. Audit the generated draft:
```powershell
python .claude/scripts/audit_experiment_plan.py "projects/experiments/YYYY-MM-DD-slug.md"
```
4. Report the generated path, audit status, evidence level, and remaining `evidence_gap` items.

Rules:
- Do not use external web/arXiv/PubMed unless the user explicitly approves.
- Do not claim the recommended design is correct; keep `decision_status: recommended_pending_approval`.
- Do not invent baseline results, trial counts, success rates, or hardware details.
- If local evidence is weak, output evidence gaps and paper-import suggestions instead of a strong recommendation.

Answer format:
- `success` / `partial` / `unverified`.
- Generated plan path.
- Audit status.
- Evidence gaps and human approval items.
