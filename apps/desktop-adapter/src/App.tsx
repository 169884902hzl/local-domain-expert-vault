import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type {
  AdapterConfig,
  CommandFinished,
  CommandOutput,
  CommandStarted,
  DiagnosticExport,
  EnvStatus,
  StatusKind,
  VaultValidation
} from "./types";

type ModuleId = "overview" | "base" | "obsidian" | "zotero" | "arxiv" | "ai" | "automation" | "logs";

interface LogLine {
  runId: string;
  stream: "stdout" | "stderr" | "system";
  line: string;
}

const moduleItems: Array<{ id: ModuleId; label: string; icon: string; caption: string }> = [
  { id: "overview", label: "Overview", icon: "◇", caption: "vault path and release boundary" },
  { id: "base", label: "Base Vault", icon: "✓", caption: "Python audit and local retrieval" },
  { id: "obsidian", label: "Obsidian", icon: "◫", caption: "vault UI and Claudian boundary" },
  { id: "zotero", label: "Zotero", icon: "◇", caption: "API, connector, WebDAV guidance" },
  { id: "arxiv", label: "arXiv Mirror", icon: "▦", caption: "OAI-PMH metadata mirror first" },
  { id: "ai", label: "AI Stack", icon: "✦", caption: "Claudian, Gemini, DeepSeek, Codex" },
  { id: "automation", label: "Automation", icon: "◷", caption: "Task Scheduler dry-run and register" },
  { id: "logs", label: "Logs", icon: "≡", caption: "tail logs and diagnostics" }
];

const defaultConfig: AdapterConfig = {
  vault_path: "",
  daily_time: "12:00",
  codex_time: "16:30",
  weekly_day: "Sunday",
  weekly_time: "20:00",
  enabled_modules: ["base", "obsidian", "zotero", "arxiv", "ai", "automation"]
};

const statusText: Record<StatusKind, string> = {
  idle: "idle",
  running: "running",
  success: "success",
  partial: "partial",
  missing_config: "missing config",
  blocked: "blocked",
  failed: "failed",
  unverified: "unverified"
};

const commandNames: Record<string, string> = {
  python_version: "Python version",
  audit_kb: "Audit KB",
  strict_audit_kb: "Strict audit",
  kb_search: "KB search",
  zotero_connector: "Zotero local connector",
  zotero_preflight: "Zotero preflight",
  zotero_collections: "List Zotero collections",
  arxiv_status: "arXiv mirror status",
  arxiv_dry_run: "arXiv OAI-PMH dry-run",
  arxiv_incremental: "arXiv incremental sync",
  pipeline_dry_run: "Mirror-first pipeline dry-run",
  check_claude: "Claude CLI",
  check_codex: "Codex CLI",
  check_gemini: "Gemini CLI",
  check_opencode: "OpenCode CLI",
  task_daily_dry_run: "Daily arXiv task dry-run",
  task_daily_register: "Register daily arXiv task",
  task_daily_status: "Daily arXiv task status",
  task_daily_run_now: "Run daily arXiv now",
  task_daily_unregister: "Unregister daily arXiv task",
  task_codex_dry_run: "Codex review task dry-run",
  task_codex_register: "Register Codex review task",
  task_codex_status: "Codex review task status",
  task_codex_run_now: "Run Codex review now",
  task_codex_unregister: "Unregister Codex review task",
  task_weekly_dry_run: "Weekly review task dry-run",
  task_weekly_register: "Register weekly review task",
  task_weekly_status: "Weekly review task status",
  task_weekly_run_now: "Run weekly review now",
  task_weekly_unregister: "Unregister weekly review task",
  codex_prepare_only: "Prepare Codex packet",
  codex_skip_codex: "Run Codex wrapper without model call"
};

function App() {
  const [activeModule, setActiveModule] = useState<ModuleId>("overview");
  const [config, setConfig] = useState<AdapterConfig>(defaultConfig);
  const [vaultPath, setVaultPath] = useState("");
  const [validation, setValidation] = useState<VaultValidation | null>(null);
  const [envStatus, setEnvStatus] = useState<EnvStatus | null>(null);
  const [statusByCommand, setStatusByCommand] = useState<Record<string, StatusKind>>({});
  const [activeRuns, setActiveRuns] = useState<Record<string, string>>({});
  const [logLines, setLogLines] = useState<LogLine[]>([]);
  const [tailOutput, setTailOutput] = useState("");
  const [diagnosticPath, setDiagnosticPath] = useState("");
  const [zoteroInputs, setZoteroInputs] = useState({
    zotero_user_id: "",
    zotero_api_key: "",
    zotero_collection_key: ""
  });
  const [dangerousModeAcknowledged, setDangerousModeAcknowledged] = useState(false);

  useEffect(() => {
    invoke<string>("suggest_vault_path")
      .then((suggested) => {
        if (suggested && !vaultPath) {
          setVaultPath(suggested);
          setConfig((current) => ({ ...current, vault_path: suggested }));
        }
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    const cleanups: Array<() => void> = [];
    listen<CommandOutput>("command-output", (event) => {
      setLogLines((current) => [
        ...current.slice(-700),
        {
          runId: event.payload.run_id,
          stream: event.payload.stream,
          line: event.payload.line
        }
      ]);
    }).then((unlisten) => cleanups.push(unlisten));
    listen<CommandFinished>("command-finished", (event) => {
      setStatusByCommand((current) => ({ ...current, [event.payload.command_id]: event.payload.status }));
      setActiveRuns((current) => {
        const next = { ...current };
        delete next[event.payload.command_id];
        return next;
      });
      setLogLines((current) => [
        ...current.slice(-700),
        {
          runId: event.payload.run_id,
          stream: "system",
          line: `${commandNames[event.payload.command_id] ?? event.payload.command_id} finished with ${event.payload.status} (${event.payload.exit_code ?? "no exit code"})`
        }
      ]);
    }).then((unlisten) => cleanups.push(unlisten));
    return () => cleanups.forEach((cleanup) => cleanup());
  }, []);

  const configuredModules = useMemo(
    () => [
      envStatus?.zotero_user_id,
      envStatus?.zotero_api_key,
      envStatus?.zotero_collection_key,
      validation?.ok
    ].filter(Boolean).length,
    [envStatus, validation]
  );

  async function validateVault() {
    if (!vaultPath.trim()) {
      appendSystem("Set a vault path first.");
      return;
    }
    try {
      const result = await invoke<VaultValidation>("validate_vault", { vaultPath });
      setValidation(result);
      setConfig((current) => ({ ...current, vault_path: result.vault_path }));
      setVaultPath(result.vault_path);
      appendSystem(result.ok ? "Vault validation passed." : `Vault validation blocked: ${result.missing.join(", ")}`);
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function loadConfig() {
    try {
      const result = await invoke<AdapterConfig>("load_adapter_config", { vaultPath });
      setConfig(result);
      setVaultPath(result.vault_path);
      appendSystem("Loaded .local desktop adapter config.");
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function saveConfig() {
    try {
      const result = await invoke<AdapterConfig>("save_adapter_config", {
        config: { ...config, vault_path: vaultPath }
      });
      setConfig(result);
      appendSystem("Saved non-secret adapter config under .local/desktop-adapter.");
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function refreshEnvStatus() {
    try {
      setEnvStatus(await invoke<EnvStatus>("get_env_status"));
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function saveZoteroEnv() {
    try {
      const result = await invoke<EnvStatus>("set_zotero_env", { request: zoteroInputs });
      setEnvStatus(result);
      setZoteroInputs({ zotero_user_id: "", zotero_api_key: "", zotero_collection_key: "" });
      appendSystem("Saved Zotero environment variables with setx. Reopen shells before running scripts manually.");
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function startCommand(commandId: string) {
    if (!vaultPath.trim()) {
      appendSystem("Set and validate a vault path before running commands.");
      return;
    }
    setStatusByCommand((current) => ({ ...current, [commandId]: "running" }));
    try {
      const started = await invoke<CommandStarted>("start_command", {
        request: {
          vault_path: vaultPath,
          command_id: commandId,
          options: {
            daily_time: config.daily_time,
            codex_time: config.codex_time,
            weekly_day: config.weekly_day,
            weekly_time: config.weekly_time
          }
        }
      });
      setActiveRuns((current) => ({ ...current, [commandId]: started.run_id }));
      appendSystem(`Started ${started.label} (${started.run_id}).`);
    } catch (error) {
      setStatusByCommand((current) => ({ ...current, [commandId]: "failed" }));
      appendSystem(String(error));
    }
  }

  async function cancelCommand(commandId: string) {
    const runId = activeRuns[commandId];
    if (!runId) return;
    try {
      await invoke("cancel_command", { runId });
      appendSystem(`Cancel requested for ${commandNames[commandId] ?? commandId}.`);
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function openObsidian() {
    try {
      await invoke("open_obsidian_vault", { vaultPath });
    } catch (error) {
      appendSystem(String(error));
    }
  }

  async function readLog(logId: string) {
    try {
      const output = await invoke<string>("tail_log", { vaultPath, logId, lines: 140 });
      setTailOutput(output);
      setActiveModule("logs");
    } catch (error) {
      setTailOutput(String(error));
      setActiveModule("logs");
    }
  }

  async function exportDiagnostics() {
    try {
      const result = await invoke<DiagnosticExport>("export_diagnostics", { vaultPath });
      setDiagnosticPath(result.path);
      setTailOutput(result.content);
      appendSystem(`Diagnostics exported to ${result.path}`);
    } catch (error) {
      appendSystem(String(error));
    }
  }

  function appendSystem(line: string) {
    setLogLines((current) => [...current.slice(-700), { runId: "ui", stream: "system", line }]);
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">LD</div>
          <div>
            <h1>Vault Adapter</h1>
            <p>Local domain expert deployment wizard</p>
          </div>
        </div>
        <nav aria-label="Adapter modules">
          {moduleItems.map((item) => (
              <button
                key={item.id}
                className={`nav-item ${activeModule === item.id ? "active" : ""}`}
                onClick={() => setActiveModule(item.id)}
              >
                <span className="icon-glyph">{item.icon}</span>
                <span>
                  <strong>{item.label}</strong>
                  <small>{item.caption}</small>
                </span>
                <span className="chevron">›</span>
              </button>
          ))}
        </nav>
        <div className="sidebar-note">
          <span className="icon-glyph">✓</span>
          <span>Whitelist-only runner. No arbitrary shell input.</span>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Windows-first Tauri adapter</p>
            <h2>Configure, verify, and schedule the local domain expert workflow.</h2>
          </div>
          <div className="topbar-actions">
            <button className="ghost" onClick={loadConfig}>Load config</button>
            <button className="primary" onClick={saveConfig}>
              <span>✓</span>
              Save local config
            </button>
          </div>
        </header>

        <section className="status-strip" aria-label="Current adapter status">
          <StatusTile label="Vault" status={validation?.ok ? "success" : validation ? "blocked" : "idle"} value={validation?.ok ? "validated" : "not validated"} />
          <StatusTile label="Zotero env" status={configuredModules >= 3 ? "success" : "partial"} value={`${configuredModules}/4 checks`} />
          <StatusTile label="Secrets" status="success" value="env only" />
          <StatusTile label="Tasks" status="unverified" value="dry-run first" />
        </section>

        {activeModule === "overview" && (
          <Panel title="Welcome / Vault Picker" icon="◇">
            <div className="vault-picker">
              <label>
                Vault root
                <input
                  value={vaultPath}
                  onChange={(event) => {
                    setVaultPath(event.target.value);
                    setConfig((current) => ({ ...current, vault_path: event.target.value }));
                  }}
                  placeholder="X:\\research\\local-domain-expert-vault"
                />
              </label>
              <button className="primary" onClick={validateVault}>
                <span>✓</span>
                Validate vault
              </button>
            </div>
            {validation && (
              <div className="validation-grid">
                <InfoBlock title="Required files" status={validation.ok ? "success" : "blocked"}>
                  {validation.ok ? "README.md, .claude/scripts, wiki, and pyproject.toml are present." : `Missing: ${validation.missing.join(", ")}`}
                </InfoBlock>
                <InfoBlock title="Warnings" status={validation.warnings.length ? "partial" : "success"}>
                  {validation.warnings.length ? validation.warnings.join(" ") : "No adapter-level warnings."}
                </InfoBlock>
              </div>
            )}
            <div className="feature-grid">
              <Feature icon="✓" title="No secret files" text="Credentials stay in user environment variables. The adapter never writes API keys into tracked repository files." />
              <Feature icon="▣" title="Whitelist runner" text="Every button maps to a fixed command. There is no arbitrary shell box." />
              <Feature icon="◷" title="Dry-run gate" text="Scheduled tasks must be dry-run before registration." />
            </div>
          </Panel>
        )}

        {activeModule === "base" && (
          <Panel title="Base Vault" icon="✓">
            <CommandGrid>
              <CommandButton id="python_version" label="Check Python" status={statusByCommand.python_version} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.python_version)} />
              <CommandButton id="audit_kb" label="Run KB audit" status={statusByCommand.audit_kb} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.audit_kb)} />
              <CommandButton id="strict_audit_kb" label="Strict audit" status={statusByCommand.strict_audit_kb} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.strict_audit_kb)} />
              <CommandButton id="kb_search" label="Search local evidence" status={statusByCommand.kb_search} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.kb_search)} />
            </CommandGrid>
            <p className="module-copy">Base Vault should pass without Zotero, Obsidian plugins, Gemini, DeepSeek, Codex, or API keys. The adapter treats missing AI layers as partial, not as a broken vault.</p>
          </Panel>
        )}

        {activeModule === "obsidian" && (
          <Panel title="Obsidian / Claudian" icon="◫">
            <div className="split">
              <InfoBlock title="Bundled workbench" status="success">
                Paper Reading Workbench is the bundled local plugin. It can jump from a topic note to Zotero item/PDF when Zotero Desktop and attachments are ready.
              </InfoBlock>
              <InfoBlock title="Community plugins" status="partial">
                Claudian, Smart Connections, Dataview, Templater, and Zotero Connector still need manual installation in Obsidian.
              </InfoBlock>
            </div>
            <button className="primary" onClick={openObsidian}>
              <span>↗</span>
              Open vault in Obsidian
            </button>
            <div className="command-help">
              <code>/search-kb question</code>
              <code>/read-paper ZOTERO_KEY</code>
              <code>/compare-papers PAPER_A PAPER_B</code>
            </div>
          </Panel>
        )}

        {activeModule === "zotero" && (
          <Panel title="Zotero" icon="◇">
            <div className="form-grid">
              <label>
                ZOTERO_USER_ID
                <input type="password" value={zoteroInputs.zotero_user_id} onChange={(event) => setZoteroInputs((current) => ({ ...current, zotero_user_id: event.target.value }))} />
              </label>
              <label>
                ZOTERO_API_KEY
                <input type="password" value={zoteroInputs.zotero_api_key} onChange={(event) => setZoteroInputs((current) => ({ ...current, zotero_api_key: event.target.value }))} />
              </label>
              <label>
                ZOTERO_COLLECTION_KEY
                <input type="password" value={zoteroInputs.zotero_collection_key} onChange={(event) => setZoteroInputs((current) => ({ ...current, zotero_collection_key: event.target.value }))} />
              </label>
            </div>
            <div className="button-row">
              <button className="primary" onClick={saveZoteroEnv}>Save Zotero env</button>
              <button className="ghost" onClick={refreshEnvStatus}>Refresh env status</button>
            </div>
            <CommandGrid>
              <CommandButton id="zotero_connector" label="Check local connector" status={statusByCommand.zotero_connector} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.zotero_connector)} />
              <CommandButton id="zotero_preflight" label="Run preflight" status={statusByCommand.zotero_preflight} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.zotero_preflight)} />
              <CommandButton id="zotero_collections" label="List collections" status={statusByCommand.zotero_collections} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.zotero_collections)} />
            </CommandGrid>
            <InfoBlock title="CSTCloud WebDAV route" status="unverified">
              Service: https://data.cstcloud.cn/. Zotero endpoint: https://data.cstcloud.cn/dav. Public guides describe about 20GB after identity verification; confirm the current quota in your own account. WebDAV credentials stay in Zotero Desktop, not this adapter.
            </InfoBlock>
          </Panel>
        )}

        {activeModule === "arxiv" && (
          <Panel title="arXiv Mirror" icon="▦">
            <CommandGrid>
              <CommandButton id="arxiv_status" label="Mirror status" status={statusByCommand.arxiv_status} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.arxiv_status)} />
              <CommandButton id="arxiv_dry_run" label="OAI-PMH dry-run" status={statusByCommand.arxiv_dry_run} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.arxiv_dry_run)} />
              <CommandButton id="arxiv_incremental" label="Incremental sync" status={statusByCommand.arxiv_incremental} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.arxiv_incremental)} />
              <CommandButton id="pipeline_dry_run" label="Pipeline dry-run" status={statusByCommand.pipeline_dry_run} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.pipeline_dry_run)} />
            </CommandGrid>
            <p className="module-copy">The mirror stores metadata and PDF URLs only. It does not store PDF files. A fresh clone without SQLite mirror should report mirror_missing instead of silently falling back to Search API.</p>
          </Panel>
        )}

        {activeModule === "ai" && (
          <Panel title="AI Stack" icon="✦">
            <CommandGrid>
              <CommandButton id="check_claude" label="Claude CLI" status={statusByCommand.check_claude} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.check_claude)} />
              <CommandButton id="check_gemini" label="Gemini CLI" status={statusByCommand.check_gemini} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.check_gemini)} />
              <CommandButton id="check_opencode" label="OpenCode CLI" status={statusByCommand.check_opencode} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.check_opencode)} />
              <CommandButton id="check_codex" label="Codex CLI" status={statusByCommand.check_codex} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.check_codex)} />
              <CommandButton id="codex_prepare_only" label="Prepare Codex packet" status={statusByCommand.codex_prepare_only} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.codex_prepare_only)} />
              <CommandButton id="codex_skip_codex" label="Codex wrapper no model" status={statusByCommand.codex_skip_codex} onRun={startCommand} onCancel={cancelCommand} running={Boolean(activeRuns.codex_skip_codex)} />
            </CommandGrid>
            <div className="split">
              <InfoBlock title="Role boundary" status="success">
                Claudian is the Obsidian interaction layer. Claude Code is the execution worker. Gemini generates high-variance candidates. DeepSeek attacks weak ideas. Codex performs the structured second pass.
              </InfoBlock>
              <InfoBlock title="Dangerous permissions" status={dangerousModeAcknowledged ? "partial" : "blocked"}>
                <label className="checkline">
                  <input type="checkbox" checked={dangerousModeAcknowledged} onChange={(event) => setDangerousModeAcknowledged(event.target.checked)} />
                  I understand dangerous Claude/Codex permission bypasses are not enabled by this adapter.
                </label>
              </InfoBlock>
            </div>
          </Panel>
        )}

        {activeModule === "automation" && (
          <Panel title="Automation" icon="◷">
            <div className="schedule-grid">
              <label>
                Daily arXiv time
                <input value={config.daily_time} onChange={(event) => setConfig((current) => ({ ...current, daily_time: event.target.value }))} />
              </label>
              <label>
                Codex review time
                <input value={config.codex_time} onChange={(event) => setConfig((current) => ({ ...current, codex_time: event.target.value }))} />
              </label>
              <label>
                Weekly day
                <select value={config.weekly_day} onChange={(event) => setConfig((current) => ({ ...current, weekly_day: event.target.value }))}>
                  {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].map((day) => <option key={day}>{day}</option>)}
                </select>
              </label>
              <label>
                Weekly time
                <input value={config.weekly_time} onChange={(event) => setConfig((current) => ({ ...current, weekly_time: event.target.value }))} />
              </label>
            </div>
            <AutomationGroup title="Daily arXiv scout" ids={["task_daily_dry_run", "task_daily_register", "task_daily_status", "task_daily_run_now", "task_daily_unregister"]} statuses={statusByCommand} activeRuns={activeRuns} onRun={startCommand} onCancel={cancelCommand} onTail={() => readLog("daily_arxiv")} />
            <AutomationGroup title="Daily Codex seed review" ids={["task_codex_dry_run", "task_codex_register", "task_codex_status", "task_codex_run_now", "task_codex_unregister"]} statuses={statusByCommand} activeRuns={activeRuns} onRun={startCommand} onCancel={cancelCommand} onTail={() => readLog("codex_review")} />
            <AutomationGroup title="Weekly agenda review" ids={["task_weekly_dry_run", "task_weekly_register", "task_weekly_status", "task_weekly_run_now", "task_weekly_unregister"]} statuses={statusByCommand} activeRuns={activeRuns} onRun={startCommand} onCancel={cancelCommand} onTail={() => readLog("weekly_review")} />
          </Panel>
        )}

        {activeModule === "logs" && (
          <Panel title="Logs / Diagnostics" icon="≡">
            <div className="button-row">
              <button className="ghost" onClick={() => readLog("daily_arxiv")}>Daily arXiv log</button>
              <button className="ghost" onClick={() => readLog("codex_review")}>Codex review log</button>
              <button className="ghost" onClick={() => readLog("weekly_review")}>Weekly review log</button>
              <button className="primary" onClick={exportDiagnostics}>Export redacted diagnostics</button>
            </div>
            {diagnosticPath && <p className="module-copy">Diagnostics written to: <code>{diagnosticPath}</code></p>}
            <pre className="log-panel">{tailOutput || "Select a log or export diagnostics."}</pre>
          </Panel>
        )}

        <section className="console" aria-label="Command output">
          <div className="console-header">
            <span>Command stream</span>
            <button className="ghost small" onClick={() => setLogLines([])}>Clear</button>
          </div>
          <pre>
            {logLines.length
              ? logLines.map((line, index) => `[${line.stream}] ${line.line}`).join("\n")
              : "No command output yet."}
          </pre>
        </section>
      </main>
    </div>
  );
}

function Panel({ title, icon, children }: { title: string; icon: string; children: ReactNode }) {
  return (
    <section className="panel">
      <div className="panel-title">
        <span className="panel-icon">{icon}</span>
        <h3>{title}</h3>
      </div>
      {children}
    </section>
  );
}

function StatusTile({ label, status, value }: { label: string; status: StatusKind; value: string }) {
  return (
    <div className="status-tile">
      <span>{label}</span>
      <StatusBadge status={status} />
      <strong>{value}</strong>
    </div>
  );
}

function StatusBadge({ status = "idle" }: { status?: StatusKind }) {
  return <span className={`badge ${status}`}>{statusText[status]}</span>;
}

function InfoBlock({ title, status, children }: { title: string; status: StatusKind; children: ReactNode }) {
  return (
    <div className="info-block">
      <div className="info-head">
        <strong>{title}</strong>
        <StatusBadge status={status} />
      </div>
      <p>{children}</p>
    </div>
  );
}

function Feature({ icon, title, text }: { icon: string; title: string; text: string }) {
  return (
    <div className="feature">
      <span className="feature-icon">{icon}</span>
      <strong>{title}</strong>
      <p>{text}</p>
    </div>
  );
}

function CommandGrid({ children }: { children: ReactNode }) {
  return <div className="command-grid">{children}</div>;
}

function CommandButton({
  id,
  label,
  status,
  running,
  onRun,
  onCancel,
  disabled,
  disabledReason
}: {
  id: string;
  label: string;
  status?: StatusKind;
  running?: boolean;
  onRun: (id: string) => void;
  onCancel: (id: string) => void;
  disabled?: boolean;
  disabledReason?: string;
}) {
  const buttonDisabled = Boolean(disabled && !running);
  return (
    <div className={`command-button ${buttonDisabled ? "disabled" : ""}`}>
      <div>
        <strong>{label}</strong>
        <StatusBadge status={running ? "running" : status ?? "idle"} />
        {buttonDisabled && disabledReason ? <small>{disabledReason}</small> : null}
      </div>
      <button className={running ? "danger" : "secondary"} disabled={buttonDisabled} onClick={() => (running ? onCancel(id) : onRun(id))}>
        <span>{running ? "■" : "▶"}</span>
        {running ? "Cancel" : "Run"}
      </button>
    </div>
  );
}

function AutomationGroup({
  title,
  ids,
  statuses,
  activeRuns,
  onRun,
  onCancel,
  onTail
}: {
  title: string;
  ids: string[];
  statuses: Record<string, StatusKind>;
  activeRuns: Record<string, string>;
  onRun: (id: string) => void;
  onCancel: (id: string) => void;
  onTail: () => void;
}) {
  return (
    <section className="automation-group">
      <div className="automation-title">
        <h4>{title}</h4>
        <button className="ghost small" onClick={onTail}>Tail log</button>
      </div>
      <CommandGrid>
        {ids.map((id) => (
              <CommandButton
            key={id}
            id={id}
            label={commandNames[id] ?? id}
            status={statuses[id]}
            running={Boolean(activeRuns[id])}
            onRun={onRun}
            onCancel={onCancel}
            disabled={requiresDryRun(id) && !dryRunPassed(statuses[dryRunIdFor(id)])}
            disabledReason="Run the dry-run check first."
          />
        ))}
      </CommandGrid>
    </section>
  );
}

function requiresDryRun(id: string): boolean {
  return id.endsWith("_register");
}

function dryRunIdFor(id: string): string {
  return id.replace("_register", "_dry_run");
}

function dryRunPassed(status?: StatusKind): boolean {
  return status === "success" || status === "partial";
}

export default App;
