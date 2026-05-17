# Local Domain Expert Vault

[![Smoke](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml/badge.svg)](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml)
[![Release](https://img.shields.io/github/v/release/169884902hzl/local-domain-expert-vault?label=release)](https://github.com/169884902hzl/local-domain-expert-vault/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#what-works-immediately-after-cloning)

> Turn an Obsidian + Zotero literature vault into a local domain expert: answer from `wiki/` evidence, run Claudian deep reading, jump back to Zotero/PDF sources, draft reviewable research ideas, and keep new papers flowing through mirror-first arXiv automation.

[中文 README](README.md)

This is an **Obsidian + Zotero + Claudian research vault** for researchers working with a specialized literature corpus. More precisely, it is a **local domain-expert vault**: instead of sending every question to a generic AI chat, it organizes the papers, concepts, entities, deep-reading reports, local retrieval, and research idea drafts of one field into traceable evidence.

The phrase "domain expert" does not mean this repository trains a new model. It means LLM-assisted reading, comparison, brainstorming, and experiment-plan drafting are constrained by local `wiki/` evidence, Zotero sources, concept networks, and human-review boundaries. The system is meant to behave like a research colleague that has long-term memory of your literature corpus, while keeping claims traceable.

The public vault uses robotic manipulation as its example domain, especially DLO manipulation, VLM/VLA systems, RL, Sim-to-Real, and embodied AI. The workflow is portable, but the papers, concepts, entities, Claudian prompts, and arXiv filters are domain-specific and should be replaced for another field.

It is useful for graduate students, PI/lab knowledge-base maintainers, and researchers who want LLM assistance to behave more like a local domain expert grounded in their own literature corpus.

Current public version: `v0.1.0`. This first release covers local browsing, knowledge-base audits, `kb_search.py` retrieval, Zotero/Obsidian setup documentation, Paper Reading Workbench, arXiv mirror-first automation docs, and the Windows scheduled-task entry point. Full AI automation still requires local Zotero, Claudian / Claude Code, Gemini, OpenCode / DeepSeek, Codex, and explicit permission configuration.

## What this is / is not

This is:

- a local domain-expert vault with long-term literature memory;
- an evidence-grounded workflow that searches `wiki/topics/`, `wiki/concepts/`, and `wiki/entities/` before writing domain answers;
- a Zotero / Obsidian / Claudian workflow for import, deep reading, finalization, audits, comparison, and concept maintenance;
- a research-agenda seed system for reviewable hypotheses, baselines, risks, and experiment-plan drafts;
- a sanitized public package without API keys, PDFs, SQLite mirrors, Zotero caches, logs, or personal machine paths.

This is not:

- a fully automated research system that works end-to-end immediately after cloning;
- a generator of verified novelty claims or experimental results;
- a PDF repository; PDFs remain managed by Zotero, WebDAV, or linked attachments;
- a robotics-only project; robotics is the example corpus.

## What works immediately after cloning

Without Zotero, Claudian, Gemini, OpenCode / DeepSeek, or Codex, you can run:

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

These commands validate the local knowledge structure and return evidence paths under `wiki/`. Obsidian is optional, but recommended for graph view, backlinks, dashboards, and reading notes.

## What The Full Workflow Requires

| Capability | Requires |
| --- | --- |
| Importing Zotero metadata | Zotero API key, user ID, collection key, or local Zotero Desktop |
| Jumping from Obsidian notes to Zotero item / PDF | Zotero Desktop, PDF attachment, Paper Reading Workbench |
| Claudian / Claude Code reading and QA commands | Core layer of the full local domain-expert workflow; local CLI, model account, explicit permission choices |
| Gemini idea divergence | Core idea-divergence layer; logged-in Gemini CLI |
| OpenCode / DeepSeek adversarial battle | Mandatory adversarial layer after Gemini greenhouse; OpenCode CLI and DeepSeek provider |
| Codex seed review | Core review layer; logged-in Codex CLI |
| Daily arXiv scouting and idea seeds | Local arXiv SQLite metadata mirror and network; full mode needs Zotero / Claudian / Gemini / DeepSeek / Codex |
| PDF syncing | Zotero storage, WebDAV, or linked attachments; PDFs are not committed |

Setup entry points:

- Obsidian / Claudian: [docs/OBSIDIAN_CLAUDIAN_SETUP.md](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- Zotero API, WebDAV, attachments: [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md)
- Automation, scheduled tasks, arXiv mirror-first: [docs/AUTOMATION.md](docs/AUTOMATION.md)
- Paper Reading Workbench security boundary: [docs/SECURITY_PLUGIN_WORKBENCH.md](docs/SECURITY_PLUGIN_WORKBENCH.md)

## Running it every day on your computer

The full automation is not a single `daily_arxiv_pipeline.py` call. The local cadence has three layers: daily paper discovery and reading, same-day Codex review, and weekly agenda review.

| Default time | Windows task | Wrapper | Purpose |
| --- | --- | --- | --- |
| Daily 12:00 | `DailyArxivEmbodiedAIScout` | `run_daily_arxiv_task.ps1` | Refresh the arXiv OAI-PMH metadata mirror, run the mirror-first daily pipeline, trigger the Zotero / Claudian / Gemini / OpenCode-DeepSeek chain, and write the daily quality audit. |
| Daily 16:30 | `DailyCodexSeedReview` | `run_daily_codex_seed_review_task.ps1` | Review today's seed packet, DeepSeek battle, and evidence packet with Codex. It can catch up to the newest unreviewed run from the last 7 days and does not promote ideas automatically. |
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

The goal is not to replace the researcher. It is to let an LLM accumulate context inside one specialized field and make careful research habits explicit and repeatable:

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
| Claude Code / Claude CLI | Script execution worker | `daily_arxiv_pipeline.py` can invoke Claude CLI for `/read-paper` style deep reading and vault edits. Public defaults do not bypass permissions; dangerous modes are explicit opt-in. |
| Gemini CLI | High-variance idea greenhouse | Gemini is used for divergence, not validation. Its broader and more speculative style is useful for raw candidates, but the hallucination risk is contained by evidence, baseline, and reviewer gates. |
| OpenCode / DeepSeek | Adversarial reviewer for Gemini ideas | `run_model_debate.py` makes DeepSeek attack weak mechanisms, A+B combinations, strongest baseline failures, and lab-fit risks. Since 2026-05-14, clean daily idea success requires this battle. |
| Codex / GPT | Structured second-pass reviewer | Codex reads the greenhouse output, DeepSeek battle, and local evidence packet, then classifies candidates as accept, rewrite, park, or reject-with-rescue. It does not auto-promote paper claims. |

The full loop is: `Claudian deep reading -> Gemini greenhouse -> OpenCode/DeepSeek adversarial battle -> Codex/GPT second-pass review -> human approval`.

## What Problem It Solves

Modern research workflows often split knowledge across PDFs, Zotero, Obsidian, AI chats, and scattered project folders. AI assistants can produce fluent summaries, but those summaries are often hard to trace back to local evidence.

This vault makes the workflow local-first:

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

The core principle is **local-first answerability**: domain answers should point back to local `wiki/` notes, concept pages, entity pages, or explicit evidence gaps.

## Example Outputs

Claudian can answer a research question by first retrieving local notes and then grounding the answer in concrete paper pages:

![Claudian local-first RL Token research answer](docs/assets/claudian-rl-token-result.png)

Deep reading reports are the middle layer between a paper and downstream answers. They convert a paper into evidence metadata, method extraction, experiment notes, limitations, and local citation notes:

![Deep reading report example](docs/assets/deep-reading-report-example.png)

Full example: [docs/examples/deep-reading-report-example.md](docs/examples/deep-reading-report-example.md).

The research-agenda workflow can turn local evidence into reviewable idea seeds with method claims, baseline analysis, novelty pressure, risk notes, and no-hardware pilot plans:

![Gemini-assisted research idea seed with local evidence and review fields](docs/assets/gemini-research-idea-seed-example.png)

## Adapting To Another Field

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

Run these commands from the repository root:

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

Open the folder as an Obsidian vault to browse `wiki/`, backlinks, graph view, and dashboard pages.

## Optional Dependencies

The base vault only needs Python for local audit and search. Extra integrations are opt-in:

| Integration | Needed for |
| --- | --- |
| Obsidian plugins | Graph/dashboard ergonomics, Smart Connections, Claudian UI |
| Paper Reading Workbench | Bundled local plugin for opening Zotero items/PDF attachments from literature notes; Zotero Desktop and a stored/linked PDF are still required |
| Zotero Desktop / Web API | Importing papers and syncing metadata |
| CSTCloud WebDAV or another storage route | Syncing Zotero stored attachments |
| Claudian / Claude Code | AI-assisted deep reading and project commands |
| Gemini CLI | Divergent research idea generation |
| OpenCode / DeepSeek CLI | Mandatory adversarial battle for Gemini greenhouse runs |
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
- Full idea/review loop: Gemini / OpenCode DeepSeek / Codex for divergent idea generation, adversarial battle, and review

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

Detailed docs are currently Chinese-first. The links below are still useful because commands, paths, and configuration keys are shown explicitly.

- [Getting Started](docs/GETTING_STARTED.md)
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) (Chinese-first)
- [Obsidian and Claudian Setup](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- [Automation](docs/AUTOMATION.md)
- [Zotero Storage and Attachments](docs/ZOTERO_STORAGE.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Paper Reading Workbench Security Notes](docs/SECURITY_PLUGIN_WORKBENCH.md)

## License

Code and documentation are released under the [MIT License](LICENSE). Third-party papers, figures, datasets, models, plugins, and services remain governed by their original licenses and terms.
