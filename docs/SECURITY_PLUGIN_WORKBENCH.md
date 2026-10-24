# Paper Reading Workbench Security Notes

`paper-reading-workbench` is the only custom Obsidian plugin bundled and enabled in the public vault.

Its purpose is narrow: when a literature note contains a `zotero_key`, it creates a local reading workbench that links the Obsidian note back to the matching Zotero item, Zotero PDF attachment, and arXiv PDF fallback when available.

## What It Reads

- The active Obsidian note, mainly `zotero_key`, title, and frontmatter.
- Local Zotero Connector API responses from `http://localhost:23119`.
- Local vault files needed to build reading workbench views, translations, and knowledge-diagram entry points.

It does not need a Zotero Web API key. Zotero Web API credentials are configured separately for import automation.

## What It Writes

The plugin writes local working files under ignored `projects/` subdirectories:

- `projects/reading-workbench/`
- `projects/translations/`
- `projects/knowledge-diagrams/`

These are local runtime artifacts. They are not intended to be committed.

The plugin does not copy PDFs into the vault. Zotero remains the source of truth for PDF files.

## When It Runs Local Commands

Opening the workbench reads local metadata and builds the workbench view.

Python helper scripts are spawned only when you click actions such as translation or knowledge-diagram generation. The plugin uses the configured local Python command and project scripts such as:

- `.claude/scripts/translate_paper_workbench.py`
- `.claude/scripts/generate_knowledge_diagrams.py`

The plugin does not run these helpers automatically on vault startup.

## Network Boundary

The plugin talks to the local Zotero Connector API and opens `zotero://...` or `https://arxiv.org/...` links when you click them. It does not upload notes, PDFs, API keys, or credentials.

If Zotero Desktop is not running, the Zotero local API calls fail locally and the workbench shows the unavailable state or a fallback link.

## Path Visibility

The workbench can display local attachment status and Zotero attachment metadata. Treat screenshots of the workbench as potentially private if they show:

- local filesystem paths;
- Zotero item keys from a private library;
- paper titles you do not want to disclose;
- local cache paths.

Redact those fields before publishing screenshots.

## How To Disable

In Obsidian:

1. Open `Settings -> Community plugins`.
2. Disable `Paper Reading Workbench`.

Or edit `.obsidian/community-plugins.json` and remove:

```json
"paper-reading-workbench"
```

Restart Obsidian after editing the file manually.

Disabling the plugin does not affect browsing `wiki/`, running `kb_search.py`, or using the Python audit scripts.
