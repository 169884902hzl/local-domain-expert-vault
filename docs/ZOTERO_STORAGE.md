# Zotero Storage And Attachments

This vault does not ship any private Zotero account, WebDAV server, API key, attachment directory, or PDF cache. You must choose and configure your own attachment strategy.

## What This Vault Needs From Zotero

The workflow can use Zotero in three levels:

| Level | Need | What works |
| --- | --- | --- |
| Metadata only | Zotero item metadata | Import title, authors, year, abstract, DOI, URL |
| Local fulltext | Zotero Desktop with local attachments | Claudian can read PDFs/fulltext from your machine |
| Syncable attachments | Stored PDF or configured linked attachment route | Daily automation can keep papers, notes, and PDF status aligned |

If you only browse `wiki/` or run `kb_search.py`, you do not need Zotero storage at all.

## Option A: Zotero Official Storage

Use this if you want the simplest sync path and your attachment volume fits Zotero's paid storage.

1. Open `Zotero -> Edit -> Settings -> Sync`.
2. Log in to your Zotero account.
3. Enable file syncing for the libraries you use.
4. Confirm new PDFs appear as stored Zotero attachments.
5. Run:

   ```powershell
   python .claude/scripts/zotero_import.py --preflight --json
   ```

Do not publish screenshots that show your account email or private library names.

## Option B: WebDAV File Sync

Use this if you want Zotero to sync stored attachments through a WebDAV provider.

1. Open `Zotero -> Edit -> Settings -> Sync`.
2. In file syncing, choose WebDAV.
3. Fill the provider URL, username, and password/app password.
4. Use Zotero's verification button.
5. Keep credentials in Zotero, not in this repository.

The vault scripts do not need your WebDAV password. They only need Zotero Desktop or Zotero Web API access.

## Option C: Linked Attachments

Use this if PDFs live in a local or cloud-synced folder outside Zotero storage.

1. Put PDFs in a stable folder outside the Git repository.
2. Configure Zotero linked attachment behavior with your preferred plugin or manual workflow.
3. Set a private local cache path if needed:

   ```powershell
   setx ZOTERO_LOCAL_PDF_CACHE "D:\path\to\your\zotero-pdf-cache"
   ```

4. Keep `attachments/`, `projects/arxiv-daily/zotero-pdf-cache/`, and `.local/` out of Git.

Linked attachments are machine-specific. Document the local rule for yourself, but do not commit absolute personal paths.

## Optional Plugins

These plugins may be useful, but the public vault does not require or configure them automatically:

| Plugin | Possible role |
| --- | --- |
| Better BibTeX | Stable citation keys and BibTeX export |
| ZotFile | Legacy attachment renaming and moving workflows |
| Attanger | Attachment moving/renaming workflows for newer Zotero setups |
| Zotero Connector | Browser capture and local connector access |

Only document a plugin as required if your own workflow really depends on it.

## Script Behavior

The public scripts are intentionally conservative:

- no maintainer collection key is hardcoded;
- missing collection configuration returns `missing_collection_key`;
- `zotero_import.py --preflight --json` redacts private collection metadata;
- `--unsafe-json` exists only for private debugging;
- PDF cache, SQLite metadata, and local attachment outputs are ignored by Git.

## Screenshots To Add Later

If you want the GitHub README to show your exact Zotero expansion setup, capture only the relevant route and redact private fields.

| Screenshot | Must show | Redact |
| --- | --- | --- |
| Zotero Sync | Sync enabled and account state | Email, username |
| Zotero File Sync | Official storage or WebDAV selection | Server credentials |
| WebDAV verification | Verification success | URL details if private, username, password |
| Linked attachment base | Base directory or plugin rule | Local username and private path |
| Better BibTeX / ZotFile / Attanger | Only settings you actually use | Personal paths and library names |

Do not add screenshots until private account names, server addresses, and local paths are masked.
