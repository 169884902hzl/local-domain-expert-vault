# Changelog

## v0.2.0 - Transactional Research-Seed State Machine

### Added

- Paper intake triage, paper primitives, research claim graph, and tension map.
- Raw-only research candidate generation and deterministic portfolio selection.
- Provider-backed DeepSeek scientific review and Codex execution review gates.
- Novelty/baseline scan, survival decision, and publish gate.
- Schema registry and strict research-run validation.
- `seed-candidates-only` rollout policy by default.

### Changed

- Formal seed publishing is no longer part of Gemini/local-score generation.
- `research_agenda_ideate.py` and `research_agenda_update.py` no longer write formal seeds.
- `publish_research_run.py` is the only script allowed to write `projects/research-agenda/idea_bank/seed/`.
- `quality_tier`, `sharpness_score`, `evidence_execution_score`, and `ordinaryness_penalty` are display / potential fields only, not promotion gates.

### Safety

- Formal publish requires both `--v2-publish-policy formal` and `--allow-formal-seed-publish`.
- Missing provider-backed DeepSeek or Codex reviews fail closed.
- Unknown novelty does not auto-promote.
- Backfill is `ingest-only` by default as an operating policy and cannot formal-publish.
- Scheduled daily automation remains on `seed-candidates-only`; it does not publish formal seeds automatically.

### Limitations

- v0.2.0 improves state control, review ordering, auditability, and rollout safety.
- It does not prove generated ideas are novel, publishable, or doctoral-level without external prior-art review, human judgment, and pilot results.

## v0.1.0 - 2026-05-17

Initial public release of Local Domain Expert Vault.

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
