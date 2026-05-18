use regex::Regex;
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    fs,
    io::{BufRead, BufReader},
    path::{Path, PathBuf},
    process::{Command, Stdio},
    sync::{Arc, Mutex},
    thread,
    time::{SystemTime, UNIX_EPOCH},
};
use tauri::{AppHandle, Emitter, State};

#[derive(Clone, Default)]
struct ProcessRegistry {
    pids: Arc<Mutex<HashMap<String, u32>>>,
}

#[derive(Debug, Deserialize)]
struct CommandRequest {
    vault_path: String,
    command_id: String,
    options: Option<HashMap<String, String>>,
}

#[derive(Debug, Serialize)]
struct CommandStarted {
    run_id: String,
    command_id: String,
    label: String,
}

#[derive(Clone, Debug, Serialize)]
struct CommandOutput {
    run_id: String,
    stream: String,
    line: String,
}

#[derive(Clone, Debug, Serialize)]
struct CommandFinished {
    run_id: String,
    command_id: String,
    exit_code: Option<i32>,
    status: String,
}

#[derive(Debug, Serialize)]
struct CommandResult {
    exit_code: Option<i32>,
    status: String,
    stdout: String,
    stderr: String,
}

#[derive(Debug, Serialize)]
struct VaultValidation {
    ok: bool,
    vault_path: String,
    missing: Vec<String>,
    warnings: Vec<String>,
}

#[derive(Debug, Serialize)]
struct EnvStatus {
    zotero_user_id: bool,
    zotero_api_key: bool,
    zotero_collection_key: bool,
}

#[derive(Debug, Deserialize, Serialize)]
struct AdapterConfig {
    vault_path: String,
    daily_time: String,
    codex_time: String,
    weekly_day: String,
    weekly_time: String,
    enabled_modules: Vec<String>,
}

#[derive(Debug, Deserialize, Serialize)]
struct EnvWriteRequest {
    vault_path: Option<String>,
    zotero_user_id: Option<String>,
    zotero_api_key: Option<String>,
    zotero_collection_key: Option<String>,
}

#[derive(Debug, Serialize)]
struct DiagnosticExport {
    path: String,
    content: String,
}

#[derive(Clone, Debug)]
struct CommandSpec {
    program: String,
    args: Vec<String>,
    cwd: PathBuf,
    label: String,
}

const DAILY_TASK: &str = "DailyArxivEmbodiedAIScout";
const CODEX_TASK: &str = "DailyCodexSeedReview";
const WEEKLY_TASK: &str = "WeeklyResearchAgendaReview";

pub fn run() {
    tauri::Builder::default()
        .manage(ProcessRegistry::default())
        .invoke_handler(tauri::generate_handler![
            validate_vault,
            load_adapter_config,
            save_adapter_config,
            get_env_status,
            set_zotero_env,
            run_command,
            start_command,
            cancel_command,
            tail_log,
            export_diagnostics,
            open_obsidian_vault,
            suggest_vault_path
        ])
        .run(tauri::generate_context!())
        .expect("failed to run desktop adapter");
}

#[tauri::command]
fn validate_vault(vault_path: String) -> Result<VaultValidation, String> {
    let root = normalize_vault_path(&vault_path)?;
    let required = [
        "README.md",
        ".claude/scripts",
        "wiki",
        "pyproject.toml",
    ];
    let mut missing = Vec::new();
    for rel in required {
        if !root.join(rel).exists() {
            missing.push(rel.to_string());
        }
    }
    let mut warnings = Vec::new();
    if !root.join(".claudian/claudian-settings.json").exists() {
        warnings.push("Claudian settings are missing; AI workflow setup is incomplete.".to_string());
    }
    if !root.join(".obsidian/plugins/paper-reading-workbench/main.js").exists() {
        warnings.push("Paper Reading Workbench plugin body is missing.".to_string());
    }
    Ok(VaultValidation {
        ok: missing.is_empty(),
        vault_path: root.display().to_string(),
        missing,
        warnings,
    })
}

#[tauri::command]
fn load_adapter_config(vault_path: String) -> Result<AdapterConfig, String> {
    let root = normalize_vault_path(&vault_path)?;
    let path = adapter_config_path(&root);
    if !path.exists() {
        return Ok(default_config(&root));
    }
    let text = fs::read_to_string(path).map_err(|err| format!("read adapter config failed: {err}"))?;
    serde_json::from_str(&text).map_err(|err| format!("parse adapter config failed: {err}"))
}

#[tauri::command]
fn save_adapter_config(config: AdapterConfig) -> Result<AdapterConfig, String> {
    let root = normalize_vault_path(&config.vault_path)?;
    ensure_adapter_dir(&root)?;
    let path = adapter_config_path(&root);
    let mut sanitized = config;
    sanitized.vault_path = root.display().to_string();
    let text = serde_json::to_string_pretty(&sanitized).map_err(|err| format!("serialize config failed: {err}"))?;
    fs::write(path, text).map_err(|err| format!("write adapter config failed: {err}"))?;
    Ok(sanitized)
}

#[tauri::command]
fn get_env_status() -> EnvStatus {
    EnvStatus {
        zotero_user_id: std::env::var("ZOTERO_USER_ID").is_ok(),
        zotero_api_key: std::env::var("ZOTERO_API_KEY").is_ok(),
        zotero_collection_key: std::env::var("ZOTERO_COLLECTION_KEY").is_ok(),
    }
}

#[tauri::command]
fn set_zotero_env(request: EnvWriteRequest) -> Result<EnvStatus, String> {
    if test_mode_enabled() {
        let status = EnvStatus {
            zotero_user_id: has_value(request.zotero_user_id.as_deref()),
            zotero_api_key: has_value(request.zotero_api_key.as_deref()),
            zotero_collection_key: has_value(request.zotero_collection_key.as_deref()),
        };
        let root = match request.vault_path.as_deref().map(str::trim).filter(|value| !value.is_empty()) {
            Some(path) => normalize_vault_path(path)?,
            None => std::env::current_dir().map_err(|err| format!("read current dir failed: {err}"))?,
        };
        ensure_adapter_dir(&root)?;
        let path = root.join(".local").join("desktop-adapter").join("test-env.json");
        let text = serde_json::to_string_pretty(&status).map_err(|err| format!("serialize test env failed: {err}"))?;
        fs::write(path, text).map_err(|err| format!("write test env failed: {err}"))?;
        return Ok(status);
    }

    let pairs = [
        ("ZOTERO_USER_ID", request.zotero_user_id),
        ("ZOTERO_API_KEY", request.zotero_api_key),
        ("ZOTERO_COLLECTION_KEY", request.zotero_collection_key),
    ];
    for (name, maybe_value) in pairs {
        if let Some(value) = maybe_value {
            let trimmed = value.trim();
            if trimmed.is_empty() {
                continue;
            }
            run_setx(name, trimmed)?;
        }
    }
    Ok(get_env_status())
}

#[tauri::command]
fn run_command(request: CommandRequest) -> Result<CommandResult, String> {
    let root = normalize_vault_path(&request.vault_path)?;
    let spec = build_command_spec(&root, &request.command_id, request.options.as_ref())?;
    let output = Command::new(&spec.program)
        .args(&spec.args)
        .current_dir(&spec.cwd)
        .output()
        .map_err(|err| format!("failed to run {}: {err}", spec.label))?;
    let stdout = redact(&String::from_utf8_lossy(&output.stdout));
    let stderr = redact(&String::from_utf8_lossy(&output.stderr));
    let exit_code = output.status.code();
    Ok(CommandResult {
        exit_code,
        status: classify_exit(exit_code),
        stdout,
        stderr,
    })
}

#[tauri::command]
fn start_command(
    app: AppHandle,
    state: State<'_, ProcessRegistry>,
    request: CommandRequest,
) -> Result<CommandStarted, String> {
    let root = normalize_vault_path(&request.vault_path)?;
    let spec = build_command_spec(&root, &request.command_id, request.options.as_ref())?;
    let run_id = format!("run-{}", now_millis());
    let mut child = Command::new(&spec.program)
        .args(&spec.args)
        .current_dir(&spec.cwd)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|err| format!("failed to start {}: {err}", spec.label))?;
    let pid = child.id();
    {
        let mut pids = state.pids.lock().map_err(|_| "process registry lock poisoned".to_string())?;
        pids.insert(run_id.clone(), pid);
    }

    if let Some(stdout) = child.stdout.take() {
        stream_reader(app.clone(), run_id.clone(), "stdout", stdout);
    }
    if let Some(stderr) = child.stderr.take() {
        stream_reader(app.clone(), run_id.clone(), "stderr", stderr);
    }

    let finished_run_id = run_id.clone();
    let finished_command_id = request.command_id.clone();
    let finished_app = app.clone();
    let registry = state.pids.clone();
    thread::spawn(move || {
        let exit_code = child.wait().ok().and_then(|status| status.code());
        if let Ok(mut pids) = registry.lock() {
            pids.remove(&finished_run_id);
        }
        let payload = CommandFinished {
            run_id: finished_run_id,
            command_id: finished_command_id,
            exit_code,
            status: classify_exit(exit_code),
        };
        let _ = finished_app.emit("command-finished", payload);
    });

    Ok(CommandStarted {
        run_id,
        command_id: request.command_id,
        label: spec.label,
    })
}

#[tauri::command]
fn cancel_command(state: State<'_, ProcessRegistry>, run_id: String) -> Result<(), String> {
    let pid = {
        let mut pids = state.pids.lock().map_err(|_| "process registry lock poisoned".to_string())?;
        pids.remove(&run_id)
    };
    let Some(pid) = pid else {
        return Err("run id is not active".to_string());
    };
    let status = Command::new("taskkill.exe")
        .args(["/PID", &pid.to_string(), "/T", "/F"])
        .status()
        .map_err(|err| format!("failed to call taskkill: {err}"))?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("taskkill exited with {:?}", status.code()))
    }
}

#[tauri::command]
fn tail_log(vault_path: String, log_id: String, lines: Option<usize>) -> Result<String, String> {
    let root = normalize_vault_path(&vault_path)?;
    let path = log_path(&root, &log_id)?;
    tail_file(&path, lines.unwrap_or(120))
}

#[tauri::command]
fn export_diagnostics(vault_path: String) -> Result<DiagnosticExport, String> {
    let root = normalize_vault_path(&vault_path)?;
    ensure_adapter_dir(&root)?;
    let validation = validate_vault(root.display().to_string())?;
    let env = get_env_status();
    let logs = ["daily_arxiv", "codex_review", "weekly_review"]
        .iter()
        .map(|id| {
            let body = log_path(&root, id)
                .and_then(|path| tail_file(&path, 80))
                .unwrap_or_else(|err| format!("unavailable: {err}"));
            format!("## Log: {id}\n\n```text\n{}\n```\n", redact(&body))
        })
        .collect::<Vec<_>>()
        .join("\n");
    let content = format!(
        "# Local Domain Expert Vault Adapter Diagnostics\n\n\
         - vault_ok: {}\n\
         - missing: {:?}\n\
         - warnings: {:?}\n\
         - ZOTERO_USER_ID: {}\n\
         - ZOTERO_API_KEY: {}\n\
         - ZOTERO_COLLECTION_KEY: {}\n\n{}",
        validation.ok,
        validation.missing,
        validation.warnings,
        env.zotero_user_id,
        env.zotero_api_key,
        env.zotero_collection_key,
        logs
    );
    let path = root
        .join(".local")
        .join("desktop-adapter")
        .join(format!("diagnostics-{}.md", now_millis()));
    let redacted = redact(&content);
    fs::write(&path, &redacted).map_err(|err| format!("write diagnostics failed: {err}"))?;
    Ok(DiagnosticExport {
        path: path.display().to_string(),
        content: redacted,
    })
}

#[tauri::command]
fn open_obsidian_vault(vault_path: String) -> Result<(), String> {
    let root = normalize_vault_path(&vault_path)?;
    let encoded = urlencoding::encode(&root.display().to_string()).to_string();
    let uri = format!("obsidian://open?path={encoded}");
    let status = Command::new("cmd.exe")
        .args(["/C", "start", "", &uri])
        .status()
        .map_err(|err| format!("failed to open Obsidian URI: {err}"))?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("open Obsidian URI exited with {:?}", status.code()))
    }
}

#[tauri::command]
fn suggest_vault_path() -> Result<String, String> {
    let mut current = std::env::current_dir().map_err(|err| format!("read current dir failed: {err}"))?;
    loop {
        if current.join("README.md").exists()
            && current.join(".claude").join("scripts").exists()
            && current.join("wiki").exists()
        {
            return Ok(current.display().to_string());
        }
        if !current.pop() {
            return Ok(String::new());
        }
    }
}

fn build_command_spec(
    root: &Path,
    command_id: &str,
    options: Option<&HashMap<String, String>>,
) -> Result<CommandSpec, String> {
    if test_mode_enabled() && is_blocked_in_test_mode(command_id) {
        return Err(format!("blocked in ADAPTER_TEST_MODE: {command_id}"));
    }

    let opt = |key: &str, default_value: &str| -> String {
        options
            .and_then(|items| items.get(key))
            .map(|value| value.trim())
            .filter(|value| !value.is_empty())
            .unwrap_or(default_value)
            .to_string()
    };
    let spec = match command_id {
        "python_version" => python(root, "python --version", ["--version"]),
        "audit_kb" => python_script(root, "Audit KB", [".claude/scripts/audit_kb.py"]),
        "strict_audit_kb" => python_script(root, "Strict audit KB", [".claude/scripts/audit_kb.py", "--strict-reading", "--strict-concepts"]),
        "kb_search" => python_script(root, "Search local KB", [".claude/scripts/kb_search.py", "diffusion policy DLO", "--limit", "5"]),
        "zotero_preflight" => python_script(root, "Zotero preflight", [".claude/scripts/zotero_import.py", "--preflight", "--json"]),
        "zotero_connector" => powershell(root, "Zotero local connector check", [
            "-NoProfile",
            "-Command",
            "try { Invoke-RestMethod 'http://127.0.0.1:23119/api/users/0' -TimeoutSec 5 | ConvertTo-Json -Depth 4 -Compress } catch { Write-Error $_.Exception.Message; exit 1 }",
        ]),
        "zotero_collections" => powershell(root, "List Zotero collections", [
            "-NoProfile",
            "-Command",
            "$headers=@{'Zotero-API-Key'=$env:ZOTERO_API_KEY;'Zotero-API-Version'='3'}; Invoke-RestMethod \"https://api.zotero.org/users/$env:ZOTERO_USER_ID/collections?format=json&limit=100\" -Headers $headers | ForEach-Object { \"$($_.data.key)`t$($_.data.name)\" }",
        ]),
        "arxiv_status" => python_script(root, "arXiv mirror status", [".claude/scripts/arxiv_metadata_sync.py", "--status"]),
        "arxiv_dry_run" => python_script(root, "arXiv metadata dry-run", [".claude/scripts/arxiv_metadata_sync.py", "--dry-run", "--days-back", "14", "--max-pages", "1"]),
        "arxiv_incremental" => python_script(root, "arXiv metadata incremental sync", [".claude/scripts/arxiv_metadata_sync.py", "--incremental", "--days-back", "60", "--overlap-days", "3"]),
        "pipeline_dry_run" => python_script(root, "Mirror-first pipeline dry-run", [".claude/scripts/daily_arxiv_pipeline.py", "--dry-run", "--source", "mirror-first", "--max-candidates", "30", "--days-back", "14", "--idea-mode", "template", "--skip-read"]),
        "check_claude" => external_version(root, "claude"),
        "check_codex" => external_version(root, "codex"),
        "check_gemini" => external_version(root, "gemini"),
        "check_opencode" => external_version(root, "opencode"),
        "task_daily_dry_run" => task_script(root, "Daily task dry-run", "register_daily_arxiv_task.ps1", true, Some(normalize_time(&opt("daily_time", "12:00"))?), None),
        "task_daily_register" => task_script(root, "Register daily task", "register_daily_arxiv_task.ps1", false, Some(normalize_time(&opt("daily_time", "12:00"))?), None),
        "task_daily_status" => task_status(root, DAILY_TASK),
        "task_daily_run_now" => task_run(root, DAILY_TASK),
        "task_daily_unregister" => task_unregister(root, DAILY_TASK),
        "task_codex_dry_run" => task_script(root, "Codex review task dry-run", "register_daily_codex_seed_review_task.ps1", true, Some(normalize_time(&opt("codex_time", "16:30"))?), None),
        "task_codex_register" => task_script(root, "Register Codex review task", "register_daily_codex_seed_review_task.ps1", false, Some(normalize_time(&opt("codex_time", "16:30"))?), None),
        "task_codex_status" => task_status(root, CODEX_TASK),
        "task_codex_run_now" => task_run(root, CODEX_TASK),
        "task_codex_unregister" => task_unregister(root, CODEX_TASK),
        "task_weekly_dry_run" => task_script(root, "Weekly review task dry-run", "register_weekly_agenda_review_task.ps1", true, Some(normalize_time(&opt("weekly_time", "20:00"))?), Some(normalize_day(&opt("weekly_day", "Sunday"))?)),
        "task_weekly_register" => task_script(root, "Register weekly review task", "register_weekly_agenda_review_task.ps1", false, Some(normalize_time(&opt("weekly_time", "20:00"))?), Some(normalize_day(&opt("weekly_day", "Sunday"))?)),
        "task_weekly_status" => task_status(root, WEEKLY_TASK),
        "task_weekly_run_now" => task_run(root, WEEKLY_TASK),
        "task_weekly_unregister" => task_unregister(root, WEEKLY_TASK),
        "codex_prepare_only" => powershell(root, "Prepare Codex review packet", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ".claude/scripts/run_daily_codex_seed_review_task.ps1", "-PrepareOnly"]),
        "codex_skip_codex" => powershell(root, "Codex review wrapper without model call", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ".claude/scripts/run_daily_codex_seed_review_task.ps1", "-SkipCodex"]),
        _ => return Err(format!("command is not whitelisted: {command_id}")),
    };
    Ok(spec)
}

fn test_mode_enabled() -> bool {
    matches!(
        std::env::var("ADAPTER_TEST_MODE").unwrap_or_default().to_ascii_lowercase().as_str(),
        "1" | "true" | "yes" | "on"
    )
}

fn is_blocked_in_test_mode(command_id: &str) -> bool {
    matches!(
        command_id,
        "arxiv_incremental"
            | "zotero_collections"
            | "codex_prepare_only"
            | "codex_skip_codex"
            | "task_daily_register"
            | "task_daily_run_now"
            | "task_daily_unregister"
            | "task_codex_register"
            | "task_codex_run_now"
            | "task_codex_unregister"
            | "task_weekly_register"
            | "task_weekly_run_now"
            | "task_weekly_unregister"
    )
}

fn has_value(value: Option<&str>) -> bool {
    value.map(str::trim).is_some_and(|item| !item.is_empty())
}

fn python<const N: usize>(root: &Path, label: &str, args: [&str; N]) -> CommandSpec {
    CommandSpec {
        program: "python".to_string(),
        args: args.iter().map(|item| item.to_string()).collect(),
        cwd: root.to_path_buf(),
        label: label.to_string(),
    }
}

fn python_script<const N: usize>(root: &Path, label: &str, args: [&str; N]) -> CommandSpec {
    python(root, label, args)
}

fn powershell<const N: usize>(root: &Path, label: &str, args: [&str; N]) -> CommandSpec {
    CommandSpec {
        program: "powershell.exe".to_string(),
        args: args.iter().map(|item| item.to_string()).collect(),
        cwd: root.to_path_buf(),
        label: label.to_string(),
    }
}

fn powershell_args(root: &Path, label: String, args: Vec<String>) -> CommandSpec {
    CommandSpec {
        program: "powershell.exe".to_string(),
        args,
        cwd: root.to_path_buf(),
        label,
    }
}

fn external_version(root: &Path, tool: &str) -> CommandSpec {
    CommandSpec {
        program: tool.to_string(),
        args: vec!["--version".to_string()],
        cwd: root.to_path_buf(),
        label: format!("Check {tool}"),
    }
}

fn task_script(root: &Path, label: &str, script: &str, dry_run: bool, time: Option<String>, day: Option<String>) -> CommandSpec {
    let mut args = vec![
        "-NoProfile".to_string(),
        "-ExecutionPolicy".to_string(),
        "Bypass".to_string(),
        "-File".to_string(),
        format!(".claude/scripts/{script}"),
    ];
    if dry_run {
        args.push("-DryRun".to_string());
    }
    if let Some(day) = day {
        args.push("-DayOfWeek".to_string());
        args.push(day);
    }
    if let Some(time) = time {
        args.push("-Time".to_string());
        args.push(time);
    }
    CommandSpec {
        program: "powershell.exe".to_string(),
        args,
        cwd: root.to_path_buf(),
        label: label.to_string(),
    }
}

fn task_status(root: &Path, task_name: &str) -> CommandSpec {
    powershell_args(
        root,
        format!("Get task {task_name}"),
        vec![
            "-NoProfile".to_string(),
            "-Command".to_string(),
            format!("Get-ScheduledTask -TaskName '{}' | Select-Object TaskName,State,TaskPath | ConvertTo-Json -Compress", task_name),
        ],
    )
}

fn task_run(root: &Path, task_name: &str) -> CommandSpec {
    powershell_args(
        root,
        format!("Run task {task_name}"),
        vec![
            "-NoProfile".to_string(),
            "-Command".to_string(),
            format!("Start-ScheduledTask -TaskName '{}'", task_name),
        ],
    )
}

fn task_unregister(root: &Path, task_name: &str) -> CommandSpec {
    powershell_args(
        root,
        format!("Unregister task {task_name}"),
        vec![
            "-NoProfile".to_string(),
            "-Command".to_string(),
            format!("Unregister-ScheduledTask -TaskName '{}' -Confirm:$false", task_name),
        ],
    )
}

fn normalize_vault_path(path: &str) -> Result<PathBuf, String> {
    let trimmed = path.trim();
    if trimmed.is_empty() {
        return Err("vault path is empty".to_string());
    }
    let root = PathBuf::from(trimmed);
    if !root.exists() {
        return Err(format!("vault path does not exist: {trimmed}"));
    }
    root.canonicalize()
        .map_err(|err| format!("canonicalize vault path failed: {err}"))
}

fn adapter_config_path(root: &Path) -> PathBuf {
    root.join(".local").join("desktop-adapter").join("config.json")
}

fn ensure_adapter_dir(root: &Path) -> Result<(), String> {
    fs::create_dir_all(root.join(".local").join("desktop-adapter"))
        .map_err(|err| format!("create .local/desktop-adapter failed: {err}"))
}

fn default_config(root: &Path) -> AdapterConfig {
    AdapterConfig {
        vault_path: root.display().to_string(),
        daily_time: "12:00".to_string(),
        codex_time: "16:30".to_string(),
        weekly_day: "Sunday".to_string(),
        weekly_time: "20:00".to_string(),
        enabled_modules: vec![
            "base".to_string(),
            "obsidian".to_string(),
            "zotero".to_string(),
            "arxiv".to_string(),
            "ai".to_string(),
            "automation".to_string(),
        ],
    }
}

fn normalize_time(value: &str) -> Result<String, String> {
    let re = Regex::new(r"^([01]\d|2[0-3]):([0-5]\d)$").unwrap();
    if re.is_match(value) {
        Ok(value.to_string())
    } else {
        Err(format!("time must be HH:mm, got {value}"))
    }
}

fn normalize_day(value: &str) -> Result<String, String> {
    let allowed = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    ];
    allowed
        .iter()
        .find(|day| day.eq_ignore_ascii_case(value))
        .map(|day| day.to_string())
        .ok_or_else(|| format!("invalid weekday: {value}"))
}

fn run_setx(name: &str, value: &str) -> Result<(), String> {
    match name {
        "ZOTERO_USER_ID" | "ZOTERO_API_KEY" | "ZOTERO_COLLECTION_KEY" => {}
        _ => return Err(format!("environment variable is not allowed: {name}")),
    }
    let status = Command::new("setx")
        .args([name, value])
        .status()
        .map_err(|err| format!("failed to call setx: {err}"))?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("setx {name} exited with {:?}", status.code()))
    }
}

fn log_path(root: &Path, log_id: &str) -> Result<PathBuf, String> {
    let rel = match log_id {
        "daily_arxiv" => "projects/arxiv-daily/scheduled-task.log",
        "codex_review" => "projects/research-agenda/reviews/daily-codex-seed-review-task.log",
        "weekly_review" => "projects/research-agenda/reviews/weekly-agenda-review-task.log",
        _ => return Err(format!("log id is not allowed: {log_id}")),
    };
    Ok(root.join(rel))
}

fn tail_file(path: &Path, limit: usize) -> Result<String, String> {
    if !path.exists() {
        return Err(format!("log does not exist: {}", path.display()));
    }
    let text = fs::read_to_string(path).map_err(|err| format!("read log failed: {err}"))?;
    let mut lines = text.lines().rev().take(limit).collect::<Vec<_>>();
    lines.reverse();
    Ok(redact(&lines.join("\n")))
}

fn stream_reader<R: std::io::Read + Send + 'static>(
    app: AppHandle,
    run_id: String,
    stream: &'static str,
    reader: R,
) {
    thread::spawn(move || {
        let reader = BufReader::new(reader);
        for line in reader.lines().map_while(Result::ok) {
            let payload = CommandOutput {
                run_id: run_id.clone(),
                stream: stream.to_string(),
                line: redact(&line),
            };
            let _ = app.emit("command-output", payload);
        }
    });
}

fn classify_exit(exit_code: Option<i32>) -> String {
    match exit_code {
        Some(0) => "success".to_string(),
        Some(_) => "failed".to_string(),
        None => "unverified".to_string(),
    }
}

fn redact(input: &str) -> String {
    let mut out = input.to_string();
    let patterns = [
        (r"(?i)(ZOTERO_API_KEY|GEMINI_API_KEY|OPENAI_API_KEY|ANTHROPIC_AUTH_TOKEN|Zotero-API-Key)(\s*[:=]\s*)[^\s,;]+", "$1$2<redacted>"),
        (r"(?i)(api[_-]?key|token|password|secret)(\s*[:=]\s*)[^\s,;]+", "$1$2<redacted>"),
        (r"sk-[A-Za-z0-9_-]{20,}", "<redacted-token>"),
        (r"gh[pousr]_[A-Za-z0-9_]{20,}", "<redacted-token>"),
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<redacted-email>"),
        (r#"[A-Za-z]:\\[^\s\r\n\t`"']+"#, "<local-path>"),
        (r"[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+", "<current-user>"),
    ];
    for (pattern, replacement) in patterns {
        let re = Regex::new(pattern).unwrap();
        out = re.replace_all(&out, replacement).to_string();
    }
    out
}

fn now_millis() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_millis())
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn redacts_common_sensitive_values() {
        let input = format!(
            "{} C:\\Users\\Alice\\vault alice@example.com {}",
            "ZOTERO_".to_string() + "API_KEY=abc123",
            "sk-".to_string() + "abcdefghijklmnopqrstuvwxyz"
        );
        let output = redact(&input);
        assert!(output.contains("ZOTERO_API_KEY=<redacted>"));
        assert!(output.contains("<local-path>"));
        assert!(output.contains("<redacted-email>"));
        assert!(output.contains("<redacted-token>"));
        assert!(!output.contains("Alice"));
    }

    #[test]
    fn rejects_non_whitelisted_command() {
        let root = PathBuf::from(".");
        let result = build_command_spec(&root, "cmd /c whoami", None);
        assert!(result.is_err());
    }

    #[test]
    fn builds_kb_search_command_without_shell() {
        let root = PathBuf::from(".");
        let spec = build_command_spec(&root, "kb_search", None).expect("kb command");
        assert_eq!(spec.program, "python");
        assert_eq!(spec.args[0], ".claude/scripts/kb_search.py");
        assert!(spec.args.contains(&"diffusion policy DLO".to_string()));
    }

    #[test]
    fn validates_time_and_day_options() {
        assert_eq!(normalize_time("16:30").unwrap(), "16:30");
        assert!(normalize_time("99:00").is_err());
        assert_eq!(normalize_day("sunday").unwrap(), "Sunday");
        assert!(normalize_day("Funday").is_err());
    }

    #[test]
    fn test_mode_blocks_state_changing_commands() {
        assert!(is_blocked_in_test_mode("task_daily_register"));
        assert!(is_blocked_in_test_mode("task_daily_run_now"));
        assert!(is_blocked_in_test_mode("task_daily_unregister"));
        assert!(is_blocked_in_test_mode("arxiv_incremental"));
        assert!(is_blocked_in_test_mode("zotero_collections"));
        assert!(!is_blocked_in_test_mode("task_daily_dry_run"));
        assert!(!is_blocked_in_test_mode("audit_kb"));
    }
}
