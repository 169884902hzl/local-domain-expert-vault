Generate a manual Gemini prompt for divergent research ideas.

Argument: $ARGUMENTS (optional extra args for the Python script)

Purpose:
- Gemini is not part of the automatic Obsidian/Claudian execution path.
- This command prepares a broad, Gemini-friendly prompt file that the user can run manually.
- The prompt should use the long-term research agenda, not only today's arXiv abstracts.
- The prompt should be creative first and adversarial second: broad divergent seeds, then top-tier reviewer pressure tests.

Required workflow:
```powershell
python .claude/scripts/generate_gemini_idea_prompt.py $ARGUMENTS
```

Generated path:
- `projects/ideas/YYYY-MM-DD-gemini-idea-prompt.md`

Manual PowerShell command:
```powershell
$env:GEMINI_CLI_NO_RELAUNCH = 'true'
Get-Content -Raw '<local-vault-path>\projects\ideas\YYYY-MM-DD-gemini-idea-prompt.md' | gemini -p "请按输入内容发散研究 idea，优先给出新颖但可实验验证的方向。"
```

Rules:
- Do not call Gemini automatically from Claudian.
- Do not make Gemini purely strict or audit-like; the first pass is broad ideation.
- The generated prompt must still ask Gemini to test the strongest baseline, reviewer pre-mortem, no-hardware pilot, and why the idea is not just A+B.
- Do not treat Gemini output as validated. Selected Gemini ideas can only enter the research agenda as seeds or manual review input.
