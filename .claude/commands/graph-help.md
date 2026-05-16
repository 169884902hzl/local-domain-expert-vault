Explain how to use the knowledge graph in this literature vault.

Argument: $ARGUMENTS (optional)

Use this when the user asks about the knowledge graph, graph view, links, concepts, navigation, or how to use the wiki.

Must explain:
- The real knowledge graph lives under `wiki/`.
- `wiki/topics/` are paper nodes.
- `wiki/concepts/` are concept nodes.
- `wiki/entities/` are researcher/entity nodes.
- In Obsidian Graph View, use the filter `path:wiki` to avoid raw/output/config clutter.
- Start from `wiki/INDEX.md` or `wiki/GRAPH_GUIDE.md`.
- For a research question, `/ask-kb <question>` is usually better than manually browsing the graph.
- For a broad exploration, open a concept page and inspect `Related Papers`, `Related Concepts`, and backlinks.

Give copyable examples:
```text
/graph-help
/ask-kb What papers connect diffusion policy with bimanual manipulation?
/expert Build a local evidence map for DLO manipulation.
```

If the user asks whether the graph is healthy, run or recommend:
```powershell
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
```
