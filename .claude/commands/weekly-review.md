Read all daily notes from the past 7 days in the daily/ directory. Generate a weekly summary that includes:

1. Main topics I worked on (grouped by project)
2. Papers read and key insights
3. Ideas worth remembering
4. Action items for next week
5. New concepts that should be added to wiki/

Save the summary to output/weekly/YYYY-WXX.md (use the ISO week number).

Also scan daily notes for any mentions of papers, concepts, or researchers that don't have wiki pages yet, and create stubs for them.

Use local retrieval only unless the user explicitly asks for web search:
```powershell
python .claude/scripts/kb_search.py "$ARGUMENTS" --limit 20
```
