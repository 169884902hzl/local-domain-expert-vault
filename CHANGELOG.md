# Changelog

## v0.3.1 - Active-Seed QA Hardening

### Added

- `active_seed_dashboard.py` as a derived run-scoped active-seed QA dashboard plus latest-view copy.
- Manual prior-art QA fields for quality checklist, negative search log, venue/manual source checks, strongest-baseline comparison, reviewer signature, and template detection.
- Result-row manual confirmation fields and active-seed blocking when unconfirmed result rows are used as core evidence.
- Cross-paper edge audit fields and active-seed blocking when unaudited/unconfirmed cross-paper edges are used as core evidence.
- Baseline execution readiness with `ready`, `partial`, `unknown`, `prohibitive`, and `not_applicable` statuses.

### Changed

- Active seed now requires complete manual QA, fresh broad novelty, anchored core evidence, known strongest baseline, baseline execution readiness, and pilot plan.
- Result-row and cross-paper checks are conditional: candidates are blocked only when those artifacts are used as core active-seed evidence.
- Weekly resurrection and pilot feedback queue/record QA failures without weakening hard gates or auto-promoting seeds.
- Run packet export includes dashboard/manual/baseline/PDF/pilot/weekly/audit artifacts when present while redacting secrets, cache payloads, logs, raw PDFs, and private paths.

### Safety

- Dashboard is derived state only and is never a promotion source of truth.
- Formal rehearsal remains separate from active seed and never writes `idea_bank/seed/`.
- Scheduled formal publish remains disabled, and scheduled wrappers still must not pass formal/active publish flags.
- v0.2.2 novelty gates, v0.2.3 evidence gates, and v0.3.0 manual prior-art / baseline / pilot gates are not relaxed.
- Active seed is still not publication proof, and the system still does not claim doctoral-level idea generation.

## v0.3.0 - Supervised Research-Validity Hardening

### Added

- `manual_prior_art_review.py` and `manual_prior_art_review.v1` for human prior-art review templates, completion validation, and active-seed gating.
- `pdf_evidence_extract.py` and `pdf_evidence_anchors.v1` for best-effort PDF/text/table evidence anchors without modifying `raw/`.
- `baseline_table.py` and `baseline_table.v1` to separate nearest works, candidate baseline guesses, Codex feasibility baselines, manual strongest baseline, and final strongest baseline.
- Cross-paper claim graph edges with explicit relation rules, overlap evidence, bounded confidence, and supporting node references.
- Cross-paper tension fields, weekly resurrection review queues, pilot plan/result/strategy feedback files, and redacted research run packet export.

### Changed

- `formal_rehearsal_candidate` writes only to the seed-candidates formal-rehearsal bucket and never to `idea_bank/seed/`.
- `--v2-publish-policy formal` writes formal seeds only when `active_seed_allowed=true`.
- Active seed now requires completed human manual prior-art review, known strongest baseline, fresh broad external novelty, anchored core evidence, DeepSeek survival, Codex acceptance, and a minimal pilot plan.
- `note_section` anchors are no longer treated as PDF/table verified evidence; `result_row` anchors require page/table/row/metric/baseline/reported value fields.
- Novelty provider cache metadata now records TTL, expiry, provider status, normalized result fields, and provider health; stale cache is a risk marker only and cannot support active/formal promotion.

### Safety

- Scheduled formal publish remains disabled, and scheduled wrappers still must not pass formal/active publish flags.
- v0.2.2 external novelty gates and v0.2.3 anchored evidence gates are not relaxed.
- Manual prior-art review cannot bypass DeepSeek fatal flaws, Codex reject/rewrite, external novelty failure, stale cache, anchorless evidence, speculative tension, or missing survival decision.
- OpenAlex, Semantic Scholar, and arXiv remain external probes, not complete human prior-art review.
- Pilot feedback is a calibration signal, not publication proof.
- Generated candidates remain review artifacts, not proven doctoral-level novelty, publishability, or experimental results.

## v0.2.3 - Evidence Graph Hardening

### Added

- `paper_primitives.v1` now emits anchored per-claim records with claim id, claim type, evidence anchor, anchor type, confidence, confidence reason, summary origin, and human-check marker.
- `research_claim_graph.py` now writes both `record_type=node` and `record_type=edge` records to the canonical graph and run snapshot.
- Claim graph edge relations now include `supports`, `contradicts`, `limits`, `exposes_gap`, `baseline_for`, `depends_on`, `evaluates`, and `transfers_to`.
- `tension_map.py` now cites claim graph `supporting_nodes` and `supporting_edges`, and marks LLM-only / no-node tensions as `speculative_tension` with `do_not_use_as_seed_evidence=true`.
- Survival and strict validation now detect anchorless core evidence risk.

### Changed

- Note-only and legacy structured-field claims default to low confidence unless they carry a real section / snippet / table / figure anchor.
- High-confidence claim evidence now requires a `section`, `snippet`, `table`, or `figure` anchor.
- `actual_baseline_result` without a strict anchor is marked `unusable`; `strongest_baseline` without anchor is at most low confidence.
- Tension map generation now depends on claim graph nodes and edges instead of only deterministic claim-type mapping.
- Formal target policy blocks candidates whose core claim graph evidence is entirely low / note_only / requires_human_check with `formal_core_evidence_not_anchored`; `seed-candidates-only` records `anchorless_core_evidence_risk` instead.

### Safety

- v0.2.3 is evidence graph hardening, not formal publish enablement.
- Scheduled formal publish remains disabled, and scheduled wrappers still must not pass formal publish flags.
- v0.2.2 external novelty gates are not relaxed.
- Generated candidates remain review artifacts, not proven doctoral-level novelty, publishability, or experimental results.

## v0.2.2 - External Novelty Scan Hardening

### Added

- `novelty_baseline_scan.py` now keeps the local claim graph, local arXiv mirror, and arXiv API probe while adding OpenAlex and optional Semantic Scholar external prior-art probes.
- Novelty scan artifacts now include nested `provider_results`, `provider_errors`, `nearest_works`, `strongest_baseline`, `verification_scope`, `formal_promotion_allowed`, and `formal_publish_risk` fields.
- External provider calls use timeout, rate limiting, and runtime cache under the research-agenda cache path.

### Changed

- Formal publish now requires broad external verification: `external_providers_used` must include `openalex` or `semantic_scholar`.
- arXiv-only `local_plus_arxiv_api` scans remain valid as narrow external probes, but they keep `external_scope_arxiv_only_not_full_prior_art` and cannot produce formal seeds.
- `survival_decision.py`, `validate_research_run.py --strict-publish`, and `publish_research_run.py` all re-check the broad external provider requirement.

### Safety

- Provider failures do not fail open; when external providers are unavailable, novelty remains `unknown` or formal promotion is disallowed.
- Semantic Scholar is optional and runs only with `SEMANTIC_SCHOLAR_API_KEY` or `S2_API_KEY`; missing keys are recorded as `provider_unavailable`.
- Scheduled formal publish remains disabled. Scheduled wrappers still must not pass `--v2-publish-policy formal`, `--allow-formal-seed-publish`, or `--allow-test-provider-for-formal`.
- Generated candidates remain review artifacts, not proven doctoral-level novelty, publishability, or experimental results.

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
