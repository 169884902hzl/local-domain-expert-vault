Search the local Obsidian literature knowledge base before answering.

Argument: $ARGUMENTS (natural-language question or keyword query)

Run:
```powershell
python .claude/scripts/kb_search.py "$ARGUMENTS" --limit 12
```

Rules:
1. Use only returned local notes as evidence unless the user explicitly asks for web search.
2. Open the top relevant files before synthesizing an answer.
3. Cite local note paths in the answer.
4. If the script prints `NO_LOCAL_MATCHES`, say that the vault has no local evidence and ask whether to search externally.

For strict tag filters, use:
```powershell
python .claude/scripts/kb_search.py "$ARGUMENTS" --must-tag diffusion --must-tag DLO --type literature
```

The search script expands tag aliases from `.claude/scripts/schema.json`, so Chinese queries such as "扩散策略在双臂操控中的最新进展" should still retrieve local literature notes.
