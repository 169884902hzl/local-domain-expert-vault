Run routine maintenance and strict verification for the literature vault.

Argument: $ARGUMENTS (optional focus, such as citations, concepts, or all)

Use this command after importing, deep-reading, concept editing, or when the user asks whether the system still has warnings.

Required workflow:
1. Run deterministic maintenance:
```powershell
python .claude/scripts/ensure_literature_structure.py
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
```
2. Run strict audit:
```powershell
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
```
3. Run local search smoke tests:
```powershell
python .claude/scripts/kb_search.py "diffusion policy bimanual manipulation" --semantic --limit 8
python .claude/scripts/kb_search.py "DLO manipulation VLM tactile" --semantic --limit 8
python .claude/scripts/kb_search.py "Action Chunking Transformer ALOHA" --semantic --limit 8
```
4. Check for empty local citation sections in `wiki/topics/*.md`.

Report format:
- PASS/WARN/FAIL summary.
- Commands run.
- Files changed by maintenance.
- Remaining warnings with concrete paths.
- Recommended next action.
