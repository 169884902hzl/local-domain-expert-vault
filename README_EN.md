# Local Domain Expert Vault

[![Smoke](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml/badge.svg)](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml)
[![Release](https://img.shields.io/github/v/release/169884902hzl/local-domain-expert-vault?label=release)](https://github.com/169884902hzl/local-domain-expert-vault/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#what-works-immediately-after-cloning)

> A local-first research vault that turns an Obsidian + Zotero library into a domain expert with memory: papers become `wiki/` evidence, Claudian reads and compares them, Gemini proposes raw candidates, DeepSeek / novelty scan / Codex / survival decision gate them, and human approval decides whether anything becomes a formal research seed.

[中文 README](README.md)

Most AI research workflows still behave like disposable conversations. You paste a paper, get a summary, ask for an idea, and a week later the answer is hard to trace back to a paper, a figure, a limitation, or a real gap in your own corpus.

This repository takes the opposite route. It is an **Obsidian + Zotero + Claudian research vault** for researchers who work inside a specialized literature field and want LLM assistance to stay grounded in local evidence. More precisely, it is a **local domain-expert vault**: papers, concepts, entities, deep-reading reports, retrieval results, idea seeds, reviewer attacks, and weekly reviews are organized as a traceable research memory.

The phrase "domain expert" does not mean this repository trains a new model. It means every LLM-assisted reading, comparison, hypothesis, and experiment-plan draft is forced back through local `wiki/` evidence, Zotero sources, concept networks, adversarial review, and human approval boundaries. The system is designed to act less like a general chatbot and more like a research colleague that has repeatedly read the same corpus you are building.

The public vault uses robotic manipulation as its example domain, especially DLO manipulation, VLM/VLA systems, RL, Sim-to-Real, and embodied AI. The workflow is portable, but the papers, concepts, entities, Claudian prompts, and arXiv filters are domain-specific and should be replaced for another field.

It is built for graduate students, PI/lab knowledge-base maintainers, and researchers who need long-term literature memory rather than another one-off summarizer.

Current public version: `v0.2.1`. `v0.1.0` was the first releasable local-first vault: local browsing, knowledge-base audits, `kb_search.py` retrieval, Zotero/Obsidian setup documentation, Paper Reading Workbench, arXiv mirror-first automation docs, and the Windows scheduled-task entry point. `v0.2.0` adds the research-seed v2 state machine on top of that base; `v0.2.1` hardens the gates needed before any future scheduled formal publish, but still does not enable scheduled formal publish.

`v0.2.0` is a major workflow architecture upgrade: the old Gemini greenhouse plus downstream-review scaffold is now a transactional research-seed state machine. It improves state control, review ordering, auditability, and rollout safety; it does not claim that generated ideas are automatically novel or publishable.

## Why This Exists

The core problem is not that researchers lack PDFs. The problem is that PDFs, Zotero items, Obsidian notes, AI chats, arXiv alerts, and project ideas usually live in separate places. That split makes it hard to answer practical research questions:

- Which papers in my own corpus actually support this claim?
- Which concept page should this new paper update?
- Can I jump from a polished note back to the Zotero item and PDF?
- Is this idea new, or just an A+B combination with a weak baseline?
- What did the system read this week, and which ideas survived review?

This vault is an attempt to make those questions operational. It treats the local literature corpus as the source of truth and turns the AI layer into a set of constrained research workers.

## Closed-Loop Design

The core design is not one model or one script. The repository is designed as a closed research loop:

```text
Zotero / arXiv
    -> wiki/topics, wiki/concepts, wiki/entities
    -> kb_search.py local evidence retrieval
    -> Claudian deep reading and paper comparison
    -> Gemini raw candidate generation
    -> portfolio selection
    -> provider-backed DeepSeek scientific review
    -> novelty / baseline scan
    -> provider-backed Codex execution review
    -> survival decision and publish gate
    -> weekly agenda review and top-tier pressure test
    -> revised filters, prompts, reading priorities, and next research ideas
```

Every stage writes an artifact that the next stage can consume. Papers are not summarized once and forgotten; they become local evidence. Deep-reading reports are decomposed into paper primitives, claim graphs, and tension maps. Gemini's speculative output is only a raw candidate; it does not become a formal seed unless it passes portfolio selection, DeepSeek scientific review, novelty/baseline scan, Codex execution review, survival decision, publish gates, and human approval.

The workflow is also designed to fail cleanly. Dry-runs, preflights, logs, `partial` states, mirror-missing status, and human review gates keep missing keys, missing mirrors, network failures, and unstable model output from contaminating the formal knowledge layer.

## v0.2.0: Transactional Research-Seed State Machine

The v0.2.0 workflow is:

```text
Zotero/arXiv
-> paper intake triage
-> Claudian deep reading
-> paper primitives
-> research claim graph
-> tension map
-> Gemini raw candidates
-> portfolio selection
-> DeepSeek scientific review
-> novelty/baseline scan
-> Codex execution review
-> survival_decision.py
-> publish_research_run.py
```

Important boundaries:

- `research_agenda_ideate.py` generates raw candidates only.
- `research_agenda_update.py` does not write formal seeds.
- `publish_research_run.py` is the only script allowed to write `projects/research-agenda/idea_bank/seed/`.
- `quality_tier`, `sharpness_score`, `evidence_execution_score`, and `ordinaryness_penalty` are potential/display fields only, not promotion gates.
- Formal seed publish is disabled by default.
- `seed-candidates-only` is the default rollout policy.
- Formal seed publish requires both `--v2-publish-policy formal` and `--allow-formal-seed-publish`, plus all hard gates passing.
- No seed today is a normal outcome; an unreviewed seed written to the formal seed folder is a failure.
- Scheduled daily automation should not be described as automatically publishing formal seeds.

v0.2.0 improves state control, review ordering, auditability, and rollout safety. It does not prove that generated ideas are novel, publishable, or doctoral-level by itself. That still requires real prior-art review, human judgment, and pilot outcomes.

## v0.2.1: Formal Publish Hardening Rehearsal

v0.2.1 is a hardening release, not a formal-publish enablement release. Scheduled daily automation still defaults to provider-free `seed-candidates-only` and does not automatically write to `projects/research-agenda/idea_bank/seed/`. The default wrapper enters the v2 state machine, but DeepSeek/Codex provider-backed gates complete only when explicit provider parameters are configured. Without those parameters, the review gates fail-closed / `partial`; this is expected safe behavior.

Key changes:

- v2 daily intake is now controlled by `paper_intake_triage.py` and its `selected_for_deep_read` output for both Zotero import attempts and Claudian deep-read attempts. The default daily target is 3 papers and the daily hard cap is 4 papers; the legacy `min_new_imports=10` floor no longer forces v2 deep reading back to 10 papers.
- `paper_intake_triage.py` supports both flat JSONL and nested `RankedPaper.to_dict()` JSONL, with stable `arxiv_id` and original candidate index tracking.
- Formal publish now requires novelty verification beyond `local_only`. In v0.2.1, the minimum accepted external scope is `local_plus_arxiv_api`, and the publish artifacts record `formal_publish_risk=external_scope_arxiv_only_not_full_prior_art`; this is only a minimum arXiv API probe, not full prior-art verification.
- Formal mode requires DeepSeek provider mode `opencode` and Codex execution provider mode `codex-cli` by default. The scheduled wrapper must be registered with `-DeepSeekProvider opencode` and `-CodexExecutionProvider codex-cli`, or the pipeline must be invoked manually with `--deepseek-provider opencode` and `--codex-execution-provider codex-cli`, before provider-backed review can complete. `provider=json` is allowed only with an explicit manual test override, and that path records `test_provider_not_production_provenance`.
- v2 artifacts now use deeper JSON Schema validation for promotion-critical nested fields, enum values, `candidate_id`, and cross-artifact alignment.
- Formal seed publish adds a lock, duplicate guard, no-overwrite staging, and quarantine invariant; scheduled wrappers still must not include formal publish flags.

These changes only make future manual formal publish tests harder to misuse. They do not prove that the system can generate doctoral-level research ideas.

## What this is / is not

This is:

- a local domain-expert vault with long-term literature memory;
- an evidence-grounded workflow that searches `wiki/topics/`, `wiki/concepts/`, and `wiki/entities/` before writing domain answers;
- a Zotero / Obsidian / Claudian workflow for import, deep reading, finalization, audits, comparison, and concept maintenance;
- a transactional research-seed system for raw candidates, seed candidates, blocked/rescue records, and reviewable experiment-plan drafts;
- a sanitized public package without API keys, PDFs, SQLite mirrors, Zotero caches, logs, or personal machine paths.

This is not:

- a fully automated research system that works end-to-end immediately after cloning;
- a generator of verified novelty claims or experimental results;
- a PDF repository; PDFs remain managed by Zotero, WebDAV, or linked attachments;
- a robotics-only project; robotics is the example corpus.

## What works immediately after cloning

Without Zotero, Claudian, Gemini, OpenCode / DeepSeek, or Codex, you can run:

```powershell
git clone https://github.com/169884902hzl/local-domain-expert-vault.git
cd local-domain-expert-vault
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

These commands validate the local knowledge structure and return evidence paths under `wiki/`. This is the smallest proof that the repository is not just a README: the public package contains a real structured literature layer and a local retrieval path.

Obsidian is optional for this smoke test, but recommended for graph view, backlinks, dashboards, and reading notes.

## What the Full Workflow Requires

| Capability | Requires |
| --- | --- |
| Importing Zotero metadata | Zotero API key, user ID, collection key, or local Zotero Desktop |
| Jumping from Obsidian notes to Zotero item / PDF | Zotero Desktop, PDF attachment, Paper Reading Workbench |
| Claudian / Claude Code reading and QA commands | Core layer of the full local domain-expert workflow; local CLI, model account, explicit permission choices |
| Gemini idea divergence | Raw candidate generator; logged-in Gemini CLI |
| OpenCode / DeepSeek scientific review | Pre-publish scientific review gate; OpenCode CLI and DeepSeek provider |
| Codex execution review | Pre-publish execution review gate; logged-in Codex CLI |
| Daily arXiv scouting and idea seeds | Local arXiv SQLite metadata mirror and network; full mode needs Zotero / Claudian / Gemini / DeepSeek / Codex |
| PDF syncing | Zotero storage, WebDAV, or linked attachments; PDFs are not committed |

Setup entry points:

- Obsidian / Claudian: [docs/OBSIDIAN_CLAUDIAN_SETUP.md](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- Zotero API, WebDAV, attachments: [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md)
- Automation, scheduled tasks, arXiv mirror-first: [docs/AUTOMATION.md](docs/AUTOMATION.md)
- Paper Reading Workbench security boundary: [docs/SECURITY_PLUGIN_WORKBENCH.md](docs/SECURITY_PLUGIN_WORKBENCH.md)

## Running it every day on your computer

The full automation is not a single `daily_arxiv_pipeline.py` call. The intended local cadence has three layers: daily paper discovery and reading, same-day Codex review, and weekly agenda review.

| Default time | Windows task | Wrapper | Purpose |
| --- | --- | --- | --- |
| Daily 12:00 | `DailyArxivEmbodiedAIScout` | `run_daily_arxiv_task.ps1` | Refresh the arXiv OAI-PMH metadata mirror, run the mirror-first daily pipeline, enter the Zotero / Claudian / Gemini / DeepSeek / Codex v2 state machine, and write the daily quality audit. The default is provider-free `seed-candidates-only`; it does not publish formal seeds automatically. DeepSeek/Codex provider-backed gates complete only after explicit provider configuration. |
| Daily 16:30 | `DailyCodexSeedReview` | `run_daily_codex_seed_review_task.ps1` | Review today's seed packet, DeepSeek scientific review, and evidence packet with Codex execution review. It can catch up to the newest unreviewed run from the last 7 days and does not promote ideas into formal seeds automatically. |
| Sunday 20:00 | `WeeklyResearchAgendaReview` | `run_weekly_agenda_review_task.ps1` | Summarize the week's research-agenda state, quality audit, and top-tier idea pressure test. It writes review artifacts but does not move idea folders automatically. |

`daily_arxiv_pipeline.py` is the daily arXiv workflow engine, but it is not the recommended Windows scheduler entry point. For a daily local run, use the wrapper and registration scripts:

```text
Windows Task Scheduler
    -> register_daily_arxiv_task.ps1      registers the scheduled task
    -> run_daily_arxiv_task.ps1           daily wrapper
    -> arxiv_metadata_sync.py             refreshes the local arXiv metadata mirror first
    -> daily_arxiv_pipeline.py            runs the mirror-first pipeline
```

Start with a dry run to inspect the task name, trigger time, and paths:

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
```

Then register the real task:

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -Time "12:00"
Get-ScheduledTask -TaskName DailyArxivEmbodiedAIScout
```

Codex review and the weekly agenda review should also be dry-run before registration:

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -DryRun -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun -DayOfWeek Sunday -Time "20:00"
```

Log entry points:

```powershell
Get-Content -Encoding UTF8 projects/arxiv-daily/scheduled-task.log -Tail 80
Get-Content -Encoding UTF8 projects/research-agenda/reviews/daily-codex-seed-review-task.log -Tail 80
Get-Content -Encoding UTF8 projects/research-agenda/reviews/weekly-agenda-review-task.log -Tail 80
```

Full registration, task removal, fallback behavior, and `partial` status handling are documented in the `Windows Task Scheduler` section of [docs/AUTOMATION.md](docs/AUTOMATION.md).

## Local Domain Expert Model

The goal is not to replace the researcher. It is to let LLMs accumulate context inside one specialized field while making careful research habits explicit and repeatable:

- **Long-term memory**: papers, concepts, authors, systems, and datasets live in `wiki/`, so the system remembers a field instead of starting from a blank chat.
- **Evidence discipline**: domain answers start from local retrieval; missing support is marked as an evidence gap rather than smoothed over.
- **Deep reading**: Zotero items can become topic notes, Claudian reading reports, finalized notes, audits, and reusable evidence.
- **Knowledge network**: papers connect to concept pages and entity pages, so later questions can follow methods, authors, datasets, and systems.
- **Hypothesis drafting**: research-agenda creates reviewable idea seeds; it does not treat local evidence as proven novelty.
- **Experiment-plan drafts**: idea seeds can be expanded into baselines, discriminating experiments, no-hardware pilots, failure conditions, and human review fields.

## Model Roles

The workflow does not ask several models the same question and average their answers. Each model is placed in a different research role:

| Layer | Role | Why it exists |
| --- | --- | --- |
| Claudian | Obsidian interaction and workflow routing | The researcher asks questions, starts deep reading, and compares papers inside Obsidian. Claudian routes those requests to `.claude/commands/` and local scripts. |
| Claude Code / Claude CLI | Script execution worker | The `research_agenda_ideate.py` idea-refinement path intentionally keeps `claude --dangerously-skip-permissions` for the current high-autonomy workflow; the `daily_arxiv_pipeline.py` Claude reading worker remains a separate opt-in. |
| Gemini CLI | Raw candidate generator | Gemini proposes high-variance raw candidates. It does not judge novelty and does not write formal seeds. |
| OpenCode / DeepSeek | Provider-backed scientific review gate | DeepSeek / opencode must produce `deepseek_review.v1` with `provider_backed=true`; deterministic fallback is not enough. |
| Novelty / baseline scan | Prior-art and ordinaryness pressure | `novelty_baseline_scan.py` checks baselines, ordinaryness, and near-neighbor pressure. Unknown novelty does not auto-promote. |
| Codex / GPT | Provider-backed execution review gate | Codex CLI must produce `codex_execution_review.v1` with `provider_backed=true`; field presence without provider-backed review cannot accept a candidate. |
| Survival decision | Final pre-publish gate | `survival_decision.py` aggregates scientific review, novelty scan, execution review, and hard gates into accepted / parked / rescue / blocked outcomes. |

The v0.2.0 loop is: `Claudian deep reading -> paper primitives -> claim graph -> tension map -> Gemini raw candidates -> portfolio selection -> DeepSeek scientific review -> novelty/baseline scan -> Codex execution review -> survival decision -> publish gate -> human approval`.

## What Problem It Solves

The working principle is **local-first answerability**: domain answers should point back to local `wiki/` notes, concept pages, entity pages, Zotero sources, or explicit evidence gaps.

```text
Zotero / arXiv
    ↓
wiki/topics/        one structured note per paper
    ↓
wiki/concepts/      reusable concept pages
    ↓
wiki/entities/      authors, labs, datasets, systems
    ↓
kb_search.py        local evidence retrieval before answering
    ↓
Claudian reading     deep reading reports and finalized notes
    ↓
research-agenda      reviewable idea seeds and automation logs
```

That is why this repository separates raw material, structured knowledge, retrieved evidence, speculative ideas, adversarial review, and human approval instead of merging them into one AI chat transcript.

## Example Outputs

The screenshots below show the intended behavior, not decorative mockups.

Claudian can answer a research question by first retrieving local notes and grounding the answer in concrete paper pages:

![Claudian local-first RL Token research answer](docs/assets/claudian-rl-token-result.png)

Deep reading reports are the middle layer between a paper and downstream answers. They convert a paper into evidence metadata, method extraction, experiment notes, limitations, and local citation notes:

![Deep reading report example](docs/assets/deep-reading-report-example.png)

Full example: [docs/examples/deep-reading-report-example.md](docs/examples/deep-reading-report-example.md).

The research-agenda workflow can turn local evidence into reviewable idea seeds with method claims, baseline analysis, novelty pressure, risk notes, and no-hardware pilot plans:

![Gemini-assisted research idea seed with local evidence and review fields](docs/assets/gemini-research-idea-seed-example.png)

## Adapting to Another Field

Robotics is only the example domain. To migrate the workflow, keep the local-first structure and replace the domain layer:

| Replace | With your own field's equivalent |
| --- | --- |
| `wiki/topics/` | Paper notes for your literature corpus |
| `wiki/concepts/` | Methods, tasks, theories, metrics, and datasets |
| `wiki/entities/` | Authors, labs, institutions, systems, datasets |
| `.claude/commands/` | Domain-specific import, reading, search, and comparison prompts |
| `.claude/scripts/daily_arxiv_pipeline.py` | Search queries, ranking keywords, and review filters |
| `.claudian/claudian-settings.json` | System prompt, tone, and local safety policy |

## What Is Included

| Path | Purpose |
| --- | --- |
| `wiki/topics/` | Structured literature notes |
| `wiki/concepts/` | Concept pages for methods, tasks, and theory |
| `wiki/entities/` | Authors, labs, datasets, systems, and organizations |
| `.claude/commands/` | Project commands for Claudian / Claude Code workflows |
| `.claude/scripts/` | Local retrieval, auditing, Zotero import, arXiv automation |
| `.claudian/claudian-settings.json` | Sanitized Claudian behavior configuration |
| `.obsidian/` | Vault-level Obsidian configuration |
| `docs/` | Setup, automation, Zotero storage, and privacy documentation |

The public package excludes private API keys, PDF caches, SQLite caches, logs, personal paths, and machine-specific runtime state.

## Quick Start

If you have already cloned the repository, the fastest useful check is:

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

The first command checks the structure of the public knowledge layer. The second command proves that local retrieval can return evidence paths before any AI layer is configured.

Then open the folder as an Obsidian vault to browse `wiki/`, backlinks, graph view, and dashboard pages.

## Optional Dependencies

The base vault only needs Python for local audit and search. Extra integrations unlock deeper layers of the workflow:

| Integration | Needed for |
| --- | --- |
| Obsidian plugins | Graph/dashboard ergonomics, Smart Connections, Claudian UI |
| Paper Reading Workbench | Bundled local plugin for opening Zotero items/PDF attachments from literature notes; Zotero Desktop and a stored/linked PDF are still required |
| Zotero Desktop / Web API | Importing papers and syncing metadata |
| CSTCloud WebDAV or another storage route | Syncing Zotero stored attachments |
| Claudian / Claude Code | AI-assisted deep reading and project commands |
| Gemini CLI | Divergent research idea generation |
| OpenCode / DeepSeek CLI | Provider-backed scientific review gate for Gemini raw candidates |
| Codex CLI | Second-pass seed review |

Paper Reading Workbench is bundled and enabled in the public vault. Open a `wiki/topics/*.md` note with `zotero_key`, then run `Paper Reading Workbench: Open paper reading workbench for current note`. The plugin queries the local Zotero Connector API, creates a `projects/reading-workbench/<ZOTERO_KEY>-zotero-source.md` source note, and provides links back to the Zotero item, Zotero PDF attachment, and arXiv PDF fallback. Zotero Desktop must be open, and the Zotero item must already have a stored or linked PDF attachment. The plugin does not copy PDFs into the vault. It is local executable Obsidian plugin code; translation and diagram actions spawn the local Python helper scripts only when you click those actions.

Read [Paper Reading Workbench Security Notes](docs/SECURITY_PLUGIN_WORKBENCH.md) for the plugin's read scope, write directories, Python helper boundary, and disable path.

## Zotero Setup

Zotero is not required for browsing or `kb_search.py`, but it is a core layer for full paper import, PDF cross-reading, attachment sync, and automation write-back.

To use the Web API route:

1. Open [Zotero API Keys](https://www.zotero.org/settings/keys).
2. Create a private key.
3. Use `Read` permission for import and inspection.
4. Add `Write` permission only when automation should create items or update collections.
5. Configure local environment variables:

```powershell
setx ZOTERO_USER_ID "<your-zotero-user-id>"
setx ZOTERO_API_KEY "<your-zotero-api-key>"
setx ZOTERO_COLLECTION_KEY "<your-collection-key>"
```

Open a new PowerShell window, then verify:

```powershell
python .claude/scripts/zotero_import.py --preflight --json
```

For attachment syncing, this vault documents a CSTCloud Data Capsule WebDAV route. The service entry is `https://data.cstcloud.cn/`, and Zotero uses the non-secret WebDAV endpoint `https://data.cstcloud.cn/dav`. Public guides and this setup route describe about 20 GB of storage after identity verification; confirm the current quota in your own account.

<img src="docs/assets/zotero-desktop-webdav-settings.png" alt="Zotero Desktop WebDAV file sync settings" width="720">

See [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md) for details.

## Claudian / Claude Code

Claudian / Claude Code is not required for basic browsing or `kb_search.py`, but it is the core agent layer of the full local domain-expert workflow.

Boundary:

- **Claudian** is the Obsidian plugin and interaction layer. It routes vault questions, `/search-kb`, `/read-paper`, and `/compare-papers` through `.claudian/claudian-settings.json`, `.claude/commands/`, and local scripts.
- **Claude Code / Claude CLI** is the execution worker. It can be called by Claudian or directly by automation scripts such as `daily_arxiv_pipeline.py`.

Recommended public default:

- Required MCP for basic browsing/search: none
- Full automation: Zotero and arXiv access
- Full idea/review loop: Gemini / OpenCode DeepSeek / Codex for raw candidate generation, provider-backed scientific review, and execution review. Scheduled provider-backed gates require explicit provider parameters; the provider-free default fails closed / `partial` instead of silently succeeding.

Project commands include:

| Command | Purpose |
| --- | --- |
| `/search-kb` | Search local wiki before answering |
| `/ingest-paper` | Import one Zotero item |
| `/read-paper` | Read, analyze, finalize, and audit one paper |
| `/compare-papers` | Compare two local paper notes |
| `/update-concepts` | Upgrade concept pages from evidence |

## Automation

The daily arXiv workflow is **local metadata mirror first**. It incrementally harvests arXiv metadata through the official OAI-PMH endpoint into a local SQLite database, ranks recent candidates from that local mirror, and uses the arXiv Search API only as a fallback/troubleshooting path in real daily runs when the mirror is stale or insufficient. The mirror stores metadata and PDF URLs, not PDF files.

Start with zero-write checks before enabling scheduled tasks:

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 5 --days-back 14 --idea-mode template --skip-read
```

If `--status` reports `missing=true`, the local SQLite mirror has not been created yet. In that case, the pipeline dry-run reports `arxiv_mirror_missing` quickly instead of silently using Search API fallback. If a tiny mirror exists but has too few matching papers, dry-run reports `arxiv_mirror_insufficient`. To preview real ranked candidates, first create a small local mirror:

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 5 --days-back 14 --idea-mode template --skip-read
```

Search API mode is a fallback/troubleshooting path because external services can return 429, timeout, or empty results. A Search API failure does not by itself mean the vault is broken.

arXiv data layer:

- OAI-PMH sync builds `projects/arxiv-daily/metadata/arxiv_metadata.sqlite`.
- The SQLite mirror stores metadata only: title, authors, abstract, dates, categories, URL, PDF URL, DOI, journal reference, comments.
- Default OAI-PMH sets are `cs` and `stat`; this is not a bundled all-arXiv database.
- The public repository does not include the SQLite mirror. Use `python .claude/scripts/arxiv_metadata_sync.py --status` to inspect your local mirror; this command is read-only and does not create the database when it is missing.
- Zotero import later uses selected metadata and PDF URLs to create library items; PDFs are managed by Zotero storage, WebDAV, or linked attachments.

Windows Task Scheduler setup and dry-run examples are documented in [docs/AUTOMATION.md](docs/AUTOMATION.md).

## Documentation

Detailed docs are currently Chinese-first, because this public vault was extracted from a real Chinese-language research workflow. The English README is meant to be self-contained for the main architecture, quick start, dependency boundary, Zotero setup, and arXiv automation model. The linked docs are still useful for non-Chinese readers because commands, paths, screenshots, and configuration keys are shown explicitly.

- [Getting Started](docs/GETTING_STARTED.md)
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) (Chinese-first)
- [Obsidian and Claudian Setup](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- [Automation](docs/AUTOMATION.md)
- [Zotero Storage and Attachments](docs/ZOTERO_STORAGE.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Paper Reading Workbench Security Notes](docs/SECURITY_PLUGIN_WORKBENCH.md)

## License

Code and documentation are released under the [MIT License](LICENSE). Third-party papers, figures, datasets, models, plugins, and services remain governed by their original licenses and terms.
