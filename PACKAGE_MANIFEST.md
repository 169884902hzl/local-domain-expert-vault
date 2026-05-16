# Package Manifest

Generated: 2026-05-17 00:40:00
Source: local working copy (path omitted from public package)

## Included

- wiki/ structured knowledge layer
- .claude/commands/, .claude/scripts/, .claude/agents/, .claude/skills/
- sanitized .claudian/claudian-settings.json
- minimal .obsidian/ settings and plugin config examples; plugin `main.js` files are not bundled
- templates/, SCHEMA.md, Dashboard.md, AGENTS.md, CLAUDE.md
- README.md, README_EN.md, LICENSE, docs/, docs/assets/, docs/examples/
- root GitHub documentation, license boundary, safety docs, and tools/build_github_package.ps1

## Excluded

- .claude/backups/, .claude/scripts/backups/, .claude/logs/, .claude/tmp/
- .claude/settings.local.json
- .claudian/sessions/
- .smart-env/, .omx/, .sisyphus/
- attachments/ contents
- raw/ contents
- output/ contents
- projects/ contents
- daily/, archive/, exports/, projectsideas/, Excalidraw/
- PDFs, SQLite databases, local caches, and machine-specific credentials

## Verify

    python .claude/scripts/audit_kb.py
    python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
    python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
    python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
    python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 5 --days-back 14 --idea-mode template --skip-read
