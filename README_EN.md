# Local-First Research Vault

> A local-first research OS that connects Zotero, Obsidian, Claudian / Claude Code, an arXiv metadata mirror, and local evidence retrieval into one auditable research workflow.

[中文 README](README.md)

This repository is not just a folder of Markdown notes or a Zotero export. It is a cloneable research workspace where papers become structured wiki pages, concept/entity networks, deep-reading reports, local retrieval evidence, and reviewable research-idea seeds. AI can help read, compare, summarize, and ideate, but the workflow is designed to keep answers tied to local evidence.

The public version starts from robotic manipulation literature, especially DLO manipulation, VLM/VLA systems, RL, Sim-to-Real, and embodied AI. The workflow itself is domain-independent: replace the papers, concepts, entities, prompts, and arXiv filters to adapt it to another research field.

## Why This Is Different

- **It is an evidence system, not an AI chat archive.** `kb_search.py` retrieves local `wiki/topics/`, `wiki/concepts/`, and `wiki/entities/` before an answer is written.
- **It is a reading pipeline, not a summary dump.** Zotero items can become topic notes, then Claudian reading reports, finalized notes, audits, and reusable evidence.
- **It is arXiv mirror-first, not Search API first.** Daily scouting ranks candidates from a local SQLite metadata mirror harvested via OAI-PMH; Search API is only a fallback.
- **It treats ideas as reviewable seeds, not proven novelty.** Research seeds carry local evidence, gaps, baselines, killer experiments, risk notes, and human-review boundaries.
- **It is designed for public reuse.** The package excludes API keys, PDFs, SQLite caches, logs, personal paths, and machine-specific runtime state.

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

## Configuration Roadmap

You do not need to configure the full automation stack on day one. Enable the system in layers:

| Level | What works | Required setup |
| --- | --- | --- |
| Level 0 | Browse `wiki/`, dashboards, graph-oriented notes, and example outputs | Obsidian optional; GitHub web view is enough |
| Level 1 | Local search and structure audits with `kb_search.py` and `audit_kb.py` | Python 3.10+ |
| Level 2 | Import Zotero metadata into topic notes | Zotero API key, user ID, collection key |
| Level 3 | Jump from an Obsidian reading note back to Zotero item / PDF | Zotero Desktop, PDF attachment, Paper Reading Workbench |
| Level 4 | Claudian / Claude Code reading, comparison, and question-answer commands | Local CLI, model account, explicit permission choices |
| Level 5 | Daily arXiv scouting, Zotero import, idea seeds, optional review | arXiv metadata mirror, Zotero write permission, optional Gemini / Codex |

Setup entry points:

- Obsidian / Claudian: [docs/OBSIDIAN_CLAUDIAN_SETUP.md](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- Zotero API, WebDAV, attachments: [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md)
- Automation, scheduled tasks, arXiv mirror-first: [docs/AUTOMATION.md](docs/AUTOMATION.md)
- Paper Reading Workbench security boundary: [docs/SECURITY_PLUGIN_WORKBENCH.md](docs/SECURITY_PLUGIN_WORKBENCH.md)

## Example Outputs

Claudian can answer a research question by first retrieving local notes and then grounding the answer in concrete paper pages:

![Claudian local-first RL Token research answer](docs/assets/claudian-rl-token-result.png)

Deep reading reports are the middle layer between a paper and downstream answers. They convert a paper into evidence metadata, method extraction, experiment notes, limitations, and local citation notes:

![Deep reading report example](docs/assets/deep-reading-report-example.png)

Full example: [docs/examples/deep-reading-report-example.md](docs/examples/deep-reading-report-example.md).

The research-agenda workflow can promote evidence-backed ideas into reviewable seeds with method claims, baseline analysis, novelty pressure, and no-hardware pilot plans:

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
| Codex CLI | Optional second-pass seed review |

Paper Reading Workbench is bundled and enabled in the public vault. Open a `wiki/topics/*.md` note with `zotero_key`, then run `Paper Reading Workbench: Open paper reading workbench for current note`. The plugin queries the local Zotero Connector API, creates a `projects/reading-workbench/<ZOTERO_KEY>-zotero-source.md` source note, and provides links back to the Zotero item, Zotero PDF attachment, and arXiv PDF fallback. Zotero Desktop must be open, and the Zotero item must already have a stored or linked PDF attachment. The plugin does not copy PDFs into the vault. It is local executable Obsidian plugin code; translation and diagram actions spawn the local Python helper scripts only when you click those actions.

Read [Paper Reading Workbench Security Notes](docs/SECURITY_PLUGIN_WORKBENCH.md) for the plugin's read scope, write directories, Python helper boundary, and disable path.

## Zotero Setup

Zotero is optional for browsing and local search. It is needed for import and automation.

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

For attachment syncing, this vault documents a CSTCloud Data Capsule WebDAV route:

![Zotero Desktop WebDAV file sync settings](docs/assets/zotero-desktop-webdav-settings.png)

See [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md) for details.

## Claudian / Claude Code

Claudian / Claude Code is optional. The repository can be inspected and searched without MCP servers.

Recommended public default:

- Required MCP: none
- Optional MCP: Zotero and arXiv for full automation
- Optional tools: Gemini / Codex for divergent idea generation and review

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
- [Obsidian and Claudian Setup](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- [Automation](docs/AUTOMATION.md)
- [Zotero Storage and Attachments](docs/ZOTERO_STORAGE.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Paper Reading Workbench Security Notes](docs/SECURITY_PLUGIN_WORKBENCH.md)

## License

Code and documentation are released under the [MIT License](LICENSE). Third-party papers, figures, datasets, models, plugins, and services remain governed by their original licenses and terms.
