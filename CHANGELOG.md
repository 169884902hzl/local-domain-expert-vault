# Changelog

## v0.2.1 - Scheduled Formal Publish Hardening Rehearsal

### Added

- v2 intake now uses `selected_for_deep_read` to control daily Zotero import attempts and Claudian deep-read attempts.
- `paper_intake_triage.py` supports both flat JSONL and nested `RankedPaper.to_dict()` JSONL records.
- Novelty scan artifacts now record `verification_scope`, `external_providers_used`, `formal_promotion_allowed`, and formal publish risk markers.
- Formal seed publish now has explicit lock, duplicate-review, no-overwrite staging, and quarantine invariants.
- Promotion-critical v2 artifacts now have deeper JSON Schema validation and cross-artifact candidate alignment checks.
- Scheduled daily wrappers now expose explicit provider rehearsal parameters while defaulting to provider-free execution.

### Changed

- Daily v2 deep-read target defaults to 3 papers with a hard cap of 4 papers.
- Legacy `min_new_imports=10` no longer forces v2 import/read back to 10 papers unless `--legacy-import-fill` is explicitly set.
- Formal mode requires DeepSeek provider mode `opencode` and Codex execution provider mode `codex-cli` by default.
- `provider=json` remains available for seed-candidates-only fixtures and manual review, but formal mode blocks it unless `--allow-test-provider-for-formal` is explicitly passed and risk is recorded.
- CI now installs `jsonschema` explicitly and verifies the Draft 2020-12 validation path.

### Safety

- Scheduled daily automation remains on `seed-candidates-only`; it still does not publish formal seeds automatically.
- Scheduled daily automation remains provider-free by default. DeepSeek/Codex provider-backed gates complete only with explicit provider configuration; otherwise the v2 path fails closed / `partial`.
- Formal publish rejects local-only `likely_open` novelty. v0.2.1's minimum external scope is `local_plus_arxiv_api`, which records `formal_publish_risk=external_scope_arxiv_only_not_full_prior_art`; this is only a minimum arXiv API probe, not full prior-art verification.
- Scheduled wrappers must not pass `--v2-publish-policy formal`, `--allow-formal-seed-publish`, or `--allow-test-provider-for-formal`.
- Backfill remains ingest-only by default and cannot generate production formal seeds.

### Limitations

- v0.2.1 is hardening, not enablement. It does not prove generated ideas are doctoral-level, novel, publishable, or experimentally valid.

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
