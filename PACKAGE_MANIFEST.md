# Package Manifest

Generated: 2026-05-16 20:50:19
Source: local working copy (path omitted from public package)

## Included

- wiki/ structured knowledge layer
- .claude/commands/, .claude/scripts/, .claude/agents/, .claude/skills/
- sanitized .claudian/claudian-settings.json
- minimal .obsidian/ settings and plugin config files
- templates/, SCHEMA.md, Dashboard.md, AGENTS.md, CLAUDE.md
- root GitHub documentation and safety docs

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
    python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
