# Package Manifest

Generated: 2026-05-21 16:28:35
Source: local working copy (path omitted from public package)

## Included

- wiki/ structured knowledge layer
- .claude/commands/, .claude/scripts/, .claude/agents/, .claude/skills/
- sanitized .claudian/claudian-settings.json
- minimal .obsidian/ settings and plugin config examples
- bundled local Obsidian plugin: `.obsidian/plugins/paper-reading-workbench/main.js` and `styles.css`
- templates/, SCHEMA.md, Dashboard.md, AGENTS.md, CLAUDE.md
- stable workflow contracts: `projects/research-agenda/workflow-contracts/`
- Research Governance Workbench v1 scripts: `.claude/scripts/research_governance_common.py`, `state_machine_guard.py`, `evidence_packet_build.py`, `evidence_packet_confirm.py`, `prior_art_dossier.py`, `nearest_work_matrix.py`, `baseline_execution_readiness.py`, `formal_rehearsal_packet.py`, `governance_review.py`, `active_seed_commit.py`, `pilot_plan.py`, `pilot_result_interpret.py`, `strategy_ledger.py`, `migrate_v03_to_v10.py`, `audit_governance_invariants.py`, and `audit_public_package_v1.py`
- Research Governance Workbench v1 schemas: `.claude/schemas/research_governance_v1/`
- GitHub Actions smoke workflow: `.github/workflows/smoke.yml`
- `pyproject.toml` and minimal `tests/` smoke/regression checks
- README.md, README_EN.md, CHANGELOG.md, LICENSE, docs/, docs/assets/, docs/examples/
- root GitHub documentation, license boundary, safety docs, `tools/build_github_package.ps1`, and `tools/scan_public_package.py`

## Excluded

- .claude/backups/, .claude/scripts/backups/, .claude/logs/, .claude/tmp/
- .claude/settings.local.json
- .claudian/sessions/
- .smart-env/, .omx/, .sisyphus/
- attachments/ contents
- raw/ contents
- output/ contents
- projects/ contents, except stable `projects/research-agenda/workflow-contracts/`
- v1 runtime governance records: `projects/research-agenda/runs/`, `projects/research-agenda/governance/active-seeds/`, `projects/research-agenda/governance/ledger/`, generated evidence packets, generated formal rehearsal packets, generated prior-art dossiers, generated strategy ledger entries, and generated legacy migration reports
- daily/, archive/, exports/, projectsideas/, Excalidraw/
- PDFs, SQLite databases, DB files, logs, local caches, `.env` files, API keys, private signatures, and machine-specific credentials

## Verify

    python -m pytest
    python tools/scan_public_package.py
    python .claude/scripts/audit_kb.py
    python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
    python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
    python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
    python .claude/scripts/arxiv_metadata_sync.py --status
    python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 5 --days-back 14 --idea-mode template --skip-read
    python .claude/scripts/audit_governance_invariants.py --strict
    python .claude/scripts/state_machine_guard.py --audit
    python .claude/scripts/migrate_v03_to_v10.py --dry-run
    python .claude/scripts/audit_public_package_v1.py
    python .claude/scripts/zotero_import.py --preflight --json
    powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
