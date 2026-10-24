Compare two local paper notes using vault evidence only.

Argument: $ARGUMENTS (two identifiers, each can be a Zotero key, topic note stem, or path)

Run:
```powershell
python .claude/scripts/compare_papers.py $ARGUMENTS
```

Rules:
1. Use only the returned local comparison table as evidence.
2. If a field says `待精读补充`, say the vault does not yet contain that evidence.
3. Do not infer method differences from titles alone.
4. For deeper comparison, run `/read-paper` on both papers first, then rerun this command.
