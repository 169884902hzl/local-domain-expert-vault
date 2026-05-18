# Desktop Adapter

The desktop adapter is a Windows-first configuration wizard for this vault. It gives new users a simple UI for the deployment steps that are otherwise described across the README and docs.

It is not an Obsidian plugin and it does not replace the existing Python, PowerShell, Zotero, Claudian, Gemini, OpenCode/DeepSeek, or Codex workflows. It is an orchestration layer around the existing scripts.

## What It Does

- validates that a selected folder is a valid `local-domain-expert-vault` checkout;
- runs base smoke checks such as `audit_kb.py` and `kb_search.py`;
- checks Zotero Desktop local connector and Zotero Web API preflight;
- helps write `ZOTERO_USER_ID`, `ZOTERO_API_KEY`, and `ZOTERO_COLLECTION_KEY` to the current Windows user's environment variables;
- runs arXiv OAI-PMH metadata mirror status, dry-run, incremental sync, and mirror-first pipeline dry-run;
- checks local CLI availability for Claude, Gemini, OpenCode, and Codex;
- dry-runs, registers, checks, runs, tails, and unregisters the three Windows scheduled tasks;
- exports a redacted diagnostics report for local debugging or issue reports.

## What It Does Not Do

- It does not install Python, Obsidian, Zotero, Claudian, Gemini CLI, OpenCode, DeepSeek, Codex, or model accounts.
- It does not log in to any AI provider.
- It does not save API keys, WebDAV passwords, cookies, or tokens into tracked repository files.
- It does not edit Zotero WebDAV credentials.
- It does not provide macOS/Linux scheduler registration in v0.1.
- It does not bypass Claude or Codex permissions.

## Security Model

The backend command runner is whitelist-only. There is no free-form shell input. Each button maps to a fixed command such as:

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/zotero_import.py --preflight --json
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
```

PowerShell commands are passed as argument arrays instead of user-built shell strings wherever the adapter controls the arguments. The UI lets users choose schedule times, but the backend validates `HH:mm` before invoking registration scripts.

Secrets follow the existing vault convention:

- Zotero Web API values go to Windows user environment variables through `setx`.
- Non-secret adapter preferences go to `.local/desktop-adapter/config.json`.
- Diagnostics are written under `.local/desktop-adapter/`.
- `.local/` is ignored by Git.

The diagnostics exporter redacts common API key names, tokens, email addresses, Windows absolute paths, and user-domain strings. Screenshot privacy is still the user's responsibility.

## Safe Test Mode

Before testing the adapter on a machine that already runs the real daily workflow, start it with:

```powershell
$env:ADAPTER_TEST_MODE = "1"
cd apps/desktop-adapter
npm run tauri dev
```

In test mode:

- Zotero credential forms do not call `setx`; the adapter writes only boolean configured/not-configured status to `.local/desktop-adapter/test-env.json`.
- real scheduled-task registration, run-now, and unregister commands are blocked.
- arXiv incremental sync is blocked.
- Zotero Web API collection listing is blocked.
- dry-run commands, base vault checks, CLI version checks, log tails, and diagnostics remain available.

This mode is for adapter validation only. It does not prove that the full production automation has been registered correctly.

## Development

The adapter lives in:

```text
apps/desktop-adapter/
```

Install frontend dependencies and run a web build:

```powershell
cd apps/desktop-adapter
npm ci
npm run build
```

Run Rust command-runner tests:

```powershell
cargo test --manifest-path apps/desktop-adapter/src-tauri/Cargo.toml
```

Run the Tauri development app:

```powershell
cd apps/desktop-adapter
npm run tauri dev
```

The repository CI checks the React/TypeScript build and Rust unit tests. A signed installer is not part of v0.1; users can build locally from source.

## First-Run Flow

1. Open the adapter.
2. Paste or validate the vault root path.
3. Run Base Vault checks.
4. Configure Zotero only if you need import/write automation.
5. Check or build the arXiv metadata mirror.
6. Check Claudian / Claude / Gemini / OpenCode / Codex availability.
7. Dry-run the scheduled tasks.
8. Register tasks only after the dry-runs are correct.
9. Use the Logs panel to inspect runtime outputs.
10. Export diagnostics only after reviewing the redacted report.

The adapter deliberately keeps `partial` states visible. Missing Zotero credentials, missing arXiv mirror, or missing model CLIs should not be hidden behind a fake green state.
