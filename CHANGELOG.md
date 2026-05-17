# Changelog

## v0.1.0 - 2026-05-17

Initial public release of the local-first research vault.

### Included

- Structured Obsidian wiki with `wiki/topics/`, `wiki/concepts/`, and `wiki/entities/`.
- Local evidence retrieval through `kb_search.py`.
- Knowledge-base integrity checks through `audit_kb.py`.
- Sanitized Claudian / Claude Code project commands and settings.
- Bundled Paper Reading Workbench Obsidian plugin for Zotero item and PDF back-links.
- Zotero API, WebDAV, and attachment setup documentation.
- arXiv OAI-PMH metadata mirror-first automation workflow.
- Windows Task Scheduler registration scripts for daily arXiv scout, daily Codex seed review, and weekly agenda review.
- GitHub Actions smoke checks for public-package health.

### Public Package Boundaries

- No API keys, tokens, cookies, Zotero databases, PDFs, SQLite mirrors, logs, or personal machine paths are included.
- Full AI automation requires local Zotero, Claudian / Claude Code, optional Gemini / Codex, and explicit permission setup.
- Research idea outputs are reviewable drafts, not verified novelty claims or experimental results.
