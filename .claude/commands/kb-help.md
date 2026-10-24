Show the practical command menu for this literature vault.

Argument: $ARGUMENTS (optional)

Explain how to use Claudian commands in this vault. Keep the answer short and practical.

Must include:
- Type `/` in the Claudian input box to open the command dropdown.
- Pick a command, then type the argument after it.
- Best default: `/expert <your request>`.
- For domain questions: `/ask-kb <question>`.
- For knowledge graph usage: `/graph-help`.
- For importing one Zotero paper: `/ingest-paper <ZOTERO_KEY>`.
- For deep reading one paper: `/read-paper <ZOTERO_KEY>`.
- For comparing two papers: `/compare-papers <paper A> vs <paper B>`.
- For concept pages: `/update-concepts` or `/update-concepts <concept-slug>`.
- For experiment planning: `/plan-experiment <research question>`.
- For experiment-plan audit: `/audit-experiment-plan <projects/experiments/file.md>`.
- For daily arXiv embodied-AI scouting: `/daily-arxiv-scout`.
- For long-term research agenda update: `/research-agenda-update --all`.
- For research agenda review/audit: `/research-agenda-review`.
- For research agenda help: `/agenda-help`.
- For manual Gemini ideation prompt: `/gemini-idea-prompt`.
- For maintenance/audit: `/maintain-kb`.
- For weekly agenda review task registration: `powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1`.

Daily arXiv boundary:
- `/daily-arxiv-scout` is complete only after Zotero import, deep reading, strict KB maintenance, agenda update, and audits pass.
- Daily files are not final ideas. The final working set is `projects/research-agenda/idea_bank/`.
- If any gate fails, report `partial` with the failed command and file path.

Give 6 copyable examples:
```text
/expert 最近有哪些扩散策略做双臂操控的工作？
/ask-kb DLO 操控中 VLM 和触觉分别解决什么问题？
/graph-help
/ingest-paper ABCD1234
/read-paper ABCD1234
/daily-arxiv-scout --dry-run --max-candidates 10
/research-agenda-update --all --dry-run
/agenda-help
/gemini-idea-prompt
/compare-papers zhu2024scaling vs keunknowndiffuser
/plan-experiment 扩散策略 + 触觉 + 双臂 DLO 的实验规划
```

End by recommending `/expert` when the user is unsure which command to choose.
