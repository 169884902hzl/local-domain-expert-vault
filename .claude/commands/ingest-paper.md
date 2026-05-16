One-step ingest a Zotero paper into the local literature knowledge base.

Argument: $ARGUMENTS (a Zotero item key, e.g. ULDP9XLR)

Run:
```powershell
python .claude/scripts/ingest_paper.py $ARGUMENTS --force-overwrite-stub
```

Expected result:
1. Fetch metadata from Zotero on `localhost:23119`
2. Create or refresh the literature stub in `wiki/topics/`
3. Normalize abstract headings and Chinese annotations
4. Ensure the literature note has `## 结构化提取` and `## 本地引用关系`
5. Create researcher entity stubs for first authors and recurring authors
6. Add topic → concept and topic → entity wikilinks
7. Backfill concept → paper and concept → concept links
8. Extract conservative local paper-to-paper citation links

After running, use `/search-kb <question>` to verify the paper is locally retrievable.
