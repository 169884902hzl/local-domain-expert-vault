param(
  [ValidateSet("none", "opencode", "openai-compatible")]
  [string]$DeepSeekProvider = "none",

  [ValidateSet("none", "codex-cli")]
  [string]$CodexExecutionProvider = "none",

  [switch]$IgnorePauseGuard
)

$ErrorActionPreference = "Stop"
if ($args.Count -gt 0) {
  throw "scheduled_governance_forbidden_arg: $($args -join ' ')"
}

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$LogDir = Join-Path $VaultRoot "projects\arxiv-daily"
$LogPath = Join-Path $LogDir "scheduled-task.log"
$LockPath = Join-Path $LogDir "daily_arxiv_pipeline.lock"
$LockStaleSeconds = [int](6.5 * 60 * 60)
$LockAcquired = $false

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Location $VaultRoot

function Write-TaskLog {
  param([string]$Message)
  $Message | Out-File -FilePath $LogPath -Append -Encoding utf8
}

. (Join-Path $ScriptPath "automation_pause_guard.ps1")

$StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
Write-TaskLog "[$StartedAt] START DailyArxivEmbodiedAIScout"
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName "DailyArxivEmbodiedAIScout" -LogPath $LogPath)) {
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  Write-TaskLog "[$FinishedAt] END exit_code=0 status=paused_by_pause_guard"
  exit 0
}
if ($IgnorePauseGuard) {
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD ignored_by_switch task=DailyArxivEmbodiedAIScout"
}

function Assert-NoGovernanceMutationArgs {
  param([string[]]$Arguments)
  $Forbidden = @(
    "--target-policy " + "formal",
    "--v2-publish-policy " + "formal",
    "--allow-formal" + "-seed-publish",
    "--allow-human" + "-override",
    "--commit-active" + "-seed",
    "formal_rehearsal" + "_packet.py",
    "governance" + "_review.py",
    "active_seed" + "_commit.py",
    "strategy" + "_ledger.py",
    "--apply" + "-strategy",
    "--active-seed" + "-id",
    "--human" + "-confirmed",
    "--governance" + "-signature"
  )
  $Joined = $Arguments -join " "
  foreach ($Token in $Forbidden) {
    if ($Joined.Contains($Token)) {
      throw "scheduled_governance_forbidden_arg: $Token"
    }
  }
}

function Test-ExistingLockIsActive {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    return $false
  }
  $Now = Get-Date
  $AgeSeconds = ($Now - (Get-Item -LiteralPath $Path).LastWriteTime).TotalSeconds
  $LockPid = $null
  $LockStarted = ""
  try {
    $LockInfo = Get-Content -LiteralPath $Path -Encoding UTF8 -Raw | ConvertFrom-Json
    $LockPid = $LockInfo.pid
    $LockStarted = $LockInfo.started_at
    if ($LockStarted) {
      $AgeSeconds = ($Now - ([datetime]::Parse($LockStarted))).TotalSeconds
    }
  }
  catch {
    $LockStarted = "unreadable"
  }
  $ProcessAlive = $false
  if ($LockPid) {
    $ProcessAlive = [bool](Get-Process -Id $LockPid -ErrorAction SilentlyContinue)
  }
  if ($AgeSeconds -gt $LockStaleSeconds -or ($LockPid -and -not $ProcessAlive)) {
    Remove-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] WARN stale_daily_pipeline_lock_removed pid=$LockPid started_at=$LockStarted age_seconds=$([int]$AgeSeconds)"
    return $false
  }
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] SKIP skipped_existing_run lock_pid=$LockPid lock_started_at=$LockStarted age_seconds=$([int]$AgeSeconds)"
  return $true
}

if (Test-ExistingLockIsActive -Path $LockPath) {
  exit 0
}

$LockPayload = @{
  pid = $PID
  started_at = (Get-Date).ToString("o")
  command = $MyInvocation.Line
} | ConvertTo-Json -Compress
try {
  $LockBytes = (New-Object System.Text.UTF8Encoding($false)).GetBytes($LockPayload)
  $LockStream = [System.IO.File]::Open($LockPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
  try {
    $LockStream.Write($LockBytes, 0, $LockBytes.Length)
  }
  finally {
    $LockStream.Close()
  }
  $LockAcquired = $true
}
catch [System.IO.IOException] {
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] SKIP skipped_existing_run lock_create_race=true"
  exit 0
}

foreach ($Name in @("ZOTERO_API_KEY", "ZOTERO_USER_ID")) {
  if (-not [Environment]::GetEnvironmentVariable($Name, "Process")) {
    $Value = [Environment]::GetEnvironmentVariable($Name, "User")
    if (-not $Value) {
      $Value = [Environment]::GetEnvironmentVariable($Name, "Machine")
    }
    if ($Value) {
      [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
    }
  }
}

$VaultDrive = [System.IO.Path]::GetPathRoot((Get-Location).Path)
$PreferredZoteroDataDir = Join-Path $VaultDrive "zotero"
$PreferredZoteroDb = Join-Path $PreferredZoteroDataDir "zotero.sqlite"
$PreferredZoteroStorage = Join-Path $PreferredZoteroDataDir "storage"
if ($VaultDrive -and (Test-Path -LiteralPath $PreferredZoteroDb) -and (Test-Path -LiteralPath $PreferredZoteroStorage)) {
  if (-not [Environment]::GetEnvironmentVariable("ZOTERO_DATA_DIR", "Process")) {
    [Environment]::SetEnvironmentVariable("ZOTERO_DATA_DIR", $PreferredZoteroDataDir, "Process")
  }
  if (-not [Environment]::GetEnvironmentVariable("LOCAL_FIRST_VAULT_ZOTERO_DB", "Process")) {
    [Environment]::SetEnvironmentVariable("LOCAL_FIRST_VAULT_ZOTERO_DB", $PreferredZoteroDb, "Process")
  }
  if (-not [Environment]::GetEnvironmentVariable("LOCAL_FIRST_VAULT_ZOTERO_STORAGE", "Process")) {
    [Environment]::SetEnvironmentVariable("LOCAL_FIRST_VAULT_ZOTERO_STORAGE", $PreferredZoteroStorage, "Process")
  }
}

$Python = (Get-Command python).Source
$SyncTimeoutSeconds = 900
$WrapperTestMode = [Environment]::GetEnvironmentVariable("DAILY_ARXIV_WRAPPER_TEST_MODE", "Process") -eq "1"

try {
  if ($WrapperTestMode) {
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] TEST_MODE skip metadata sync"
  }
  else {
    $SyncOutput = Join-Path $LogDir "metadata-sync-last.log"
    $SyncError = Join-Path $LogDir "metadata-sync-last.err.log"
    $SyncProcess = Start-Process -FilePath $Python -ArgumentList @(
      ".claude/scripts/arxiv_metadata_sync.py",
      "--incremental",
      "--days-back",
      "60",
      "--overlap-days",
      "3"
    ) -WorkingDirectory $VaultRoot -NoNewWindow -PassThru -RedirectStandardOutput $SyncOutput -RedirectStandardError $SyncError
    if (-not $SyncProcess.WaitForExit($SyncTimeoutSeconds * 1000)) {
      Stop-Process -Id $SyncProcess.Id -Force -ErrorAction SilentlyContinue
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] WARN arxiv_metadata_sync_timeout=${SyncTimeoutSeconds}s; continuing with existing mirror/search fallback" |
        Out-File -FilePath $LogPath -Append -Encoding utf8
    }
    else {
      $SyncProcess.Refresh()
      if (Test-Path $SyncOutput) {
        Get-Content -Encoding UTF8 $SyncOutput | Out-File -FilePath $LogPath -Append -Encoding utf8
      }
      if (Test-Path $SyncError) {
        Get-Content -Encoding UTF8 $SyncError | Out-File -FilePath $LogPath -Append -Encoding utf8
      }
      $SyncExitCode = $SyncProcess.ExitCode
      if ($null -eq $SyncExitCode) {
        $SyncExitCode = 0
      }
      if ($SyncExitCode -ne 0) {
        "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] WARN arxiv_metadata_sync_exit_code=$SyncExitCode; continuing with existing mirror/search fallback" |
          Out-File -FilePath $LogPath -Append -Encoding utf8
      }
    }
  }
  $PipelineArgs = @(
    ".claude/scripts/daily_arxiv_pipeline.py",
    "--once",
    "--source",
    "mirror-first",
    "--idea-mode",
    "gemini-divergent",
    "--idea-timeout",
    "1200",
    "--gemini-model",
    "gemini-3.1-pro-preview",
    "--raw-candidate-limit",
    "8",
    "--min-raw-candidates",
    "3",
    "--max-generated",
    "3",
    "--target-deep-read",
    "4",
    "--max-deep-read",
    "4",
    "--read-timeout",
    "4200",
    "--read-mode",
    "codex-controlled",
    "--read-retries",
    "1",
    "--read-retry-delay",
    "90"
  )
  if ($DeepSeekProvider -ne "none") {
    $PipelineArgs += @("--deepseek-provider", $DeepSeekProvider)
  }
  if ($CodexExecutionProvider -ne "none") {
    $PipelineArgs += @("--codex-execution-provider", $CodexExecutionProvider)
  }
  Assert-NoGovernanceMutationArgs -Arguments $PipelineArgs
  if ($WrapperTestMode) {
    $PipelineExitText = [Environment]::GetEnvironmentVariable("DAILY_ARXIV_WRAPPER_TEST_PIPELINE_EXIT", "Process")
    if ([string]::IsNullOrWhiteSpace($PipelineExitText)) {
      $PipelineExitText = "0"
    }
    $ExitCode = [int]$PipelineExitText
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] TEST_MODE pipeline_exit_code=$ExitCode"
  }
  else {
    & $Python @PipelineArgs 2>&1 |
      ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
    $ExitCode = $LASTEXITCODE
  }
  if ($ExitCode -ne 0) {
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] RECOVERY start resume_backlog exit_code=$ExitCode"
    $RecoveryArgs = $PipelineArgs + @("--resume-backlog")
    if ($WrapperTestMode) {
      $RecoveryExitText = [Environment]::GetEnvironmentVariable("DAILY_ARXIV_WRAPPER_TEST_RECOVERY_EXIT", "Process")
      if ([string]::IsNullOrWhiteSpace($RecoveryExitText)) {
        $RecoveryExitText = "1"
      }
      $RecoveryExitCode = [int]$RecoveryExitText
      Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] TEST_MODE recovery_exit_code=$RecoveryExitCode"
    }
    else {
      & $Python @RecoveryArgs 2>&1 |
        ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
      $RecoveryExitCode = $LASTEXITCODE
    }
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] RECOVERY end exit_code=$RecoveryExitCode"
    if ($RecoveryExitCode -eq 0) {
      $ExitCode = 0
    }
  }
  $RunDate = Get-Date -Format "yyyy-MM-dd"
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] INDEX_SWEEP start run_date=$RunDate"
  if ($WrapperTestMode) {
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] TEST_MODE skip index sweep"
  }
  else {
    & $Python ".claude/scripts/kb_embed.py" "build" 2>&1 |
      ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
    $SweepExitCode = $LASTEXITCODE
    if ($SweepExitCode -ne 0) {
      Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] WARN index_sweep_exit_code=$SweepExitCode; continuing"
    }
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] INDEX_SWEEP end exit_code=$SweepExitCode"
  }
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] QUALITY_AUDIT start run_date=$RunDate"
  if ($WrapperTestMode) {
    $QualityExitText = [Environment]::GetEnvironmentVariable("DAILY_ARXIV_WRAPPER_TEST_QUALITY_EXIT", "Process")
    if ([string]::IsNullOrWhiteSpace($QualityExitText)) {
      $QualityExitText = "0"
    }
    $QualityExitCode = [int]$QualityExitText
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] TEST_MODE quality_exit_code=$QualityExitCode"
  }
  else {
    & $Python @(
      ".claude/scripts/audit_daily_automation_quality.py",
      "--run-date",
      $RunDate,
      "--scheduled-deepseek-provider",
      $DeepSeekProvider,
      "--scheduled-codex-execution-provider",
      $CodexExecutionProvider
    ) 2>&1 |
      ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
    $QualityExitCode = $LASTEXITCODE
  }
  Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] QUALITY_AUDIT end exit_code=$QualityExitCode"
  if ($QualityExitCode -ne 0) {
    Write-TaskLog "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] QUALITY_AUDIT_FAILED exit_code=$QualityExitCode"
    $ExitCode = $QualityExitCode
  }
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  Write-TaskLog "[$FinishedAt] END exit_code=$ExitCode"
  exit $ExitCode
}
catch {
  $FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  Write-TaskLog "[$FailedAt] ERROR $($_.Exception.Message)"
  throw
}
finally {
  if ($LockAcquired) {
    Remove-Item -LiteralPath $LockPath -Force -ErrorAction SilentlyContinue
  }
}
