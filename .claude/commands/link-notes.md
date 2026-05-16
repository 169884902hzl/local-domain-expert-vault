Read the note at $ARGUMENTS. Identify all entities (researcher names, paper titles, concepts, methods, datasets) that are mentioned in plain text.

For the whole vault maintenance path, prefer:
```powershell
python .claude/scripts/gen_entity_stubs.py --include-first-authors
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
```

For each entity:
1. Search the vault for an existing note that matches
2. If found, replace the plain text with a [[wikilink]]
3. If not found, create a new stub note in the appropriate wiki/ subdirectory and link it

Save the modified note. Do not change any content other than adding links.
