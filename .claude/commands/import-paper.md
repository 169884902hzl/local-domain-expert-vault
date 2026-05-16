Import a paper from Zotero into the knowledge base.

Argument: $ARGUMENTS (a Zotero item key, e.g. GQ9BVK8N)

Preferred deterministic path:
```powershell
python .claude/scripts/ingest_paper.py $ARGUMENTS --force-overwrite-stub
```

This command fetches Zotero metadata from `localhost:23119`, creates or refreshes
the `wiki/topics/` stub, then runs the local post-processing pipeline:
`fix_abstracts.py` → `ensure_literature_structure.py` →
`gen_entity_stubs.py --include-first-authors` → `fix_wikilinks.py` →
`backfill_concepts.py` → `extract_citation_links.py`.

Fallback path, only if the local script fails:
1. Use `mcp__zotero__zotero_item_metadata` to get metadata for the given key
2. Check if a note with this zotero_key already exists in wiki/topics/ (use Grep to search)
3. If exists: update the existing note's frontmatter with any missing fields
4. If not exists: create a new stub note in wiki/topics/ following the schema in .claude/scripts/schema.json
5. Filename format: lowercase-firstauthor + year + first-keyword (e.g., zhang2025dlograsping.md)
6. The frontmatter must follow the canonical field order from schema.json
7. Add English abstract with Chinese term annotations (use the same term list as fix_abstracts.py)
8. Add Chinese summary (one sentence)
9. Add `## 结构化提取` with explicit unknown placeholders rather than invented facts
10. Add `## 本地引用关系`; use `-` when no local citation evidence exists
11. Add research direction tags (max 5)
12. Run `/search-kb $ARGUMENTS` to verify local retrievability

Frontmatter template:
```
---
title: "Paper Title"
tags: [tag1, tag2]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
type: "literature"
status: "stub"
summary: "Chinese one-liner"
authors: "Last, First; Last, First"
year: "2024"
venue: "Conference Name"
zotero_key: "XXXXXXXX"
---
```

Use Chinese for summary and direction tags. Use English for title, authors, venue.
