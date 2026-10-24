param(
  [switch]$PrepareOnly,
  [switch]$SkipCodex,
  [switch]$DangerouslyBypassSandbox,
  [switch]$IgnorePauseGuard
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$ReviewDir = Join-Path $VaultRoot "projects\research-agenda\reviews"
$LogPath = Join-Path $ReviewDir "daily-codex-seed-review-task.log"
$ProviderMatrixPath = Join-Path $VaultRoot "projects\research-agenda\workflow-contracts\provider-matrix.json"

New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null
Set-Location $VaultRoot

$Python = (Get-Command python).Source
$RunDate = Get-Date -Format "yyyy-MM-dd"
$StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $Utf8NoBom
$OutputEncoding = $Utf8NoBom

"[$StartedAt] START DailyCodexSeedReview" | Out-File -FilePath $LogPath -Append -Encoding utf8
"[$StartedAt] PROVIDER_MATRIX $ProviderMatrixPath" | Out-File -FilePath $LogPath -Append -Encoding utf8

function Resolve-CodexCliPath {
  $candidates = New-Object System.Collections.Generic.List[string]

  if ($env:CODEX_CLI_PATH) {
    $candidates.Add($env:CODEX_CLI_PATH)
  }

  $CodexConfigPath = Join-Path $env:USERPROFILE ".codex\config.toml"
  if (Test-Path $CodexConfigPath) {
    $ConfigMatch = Select-String -Path $CodexConfigPath -Pattern 'CODEX_CLI_PATH\s*=\s*[''"](?<path>[^''"]+)[''"]' -Encoding UTF8 | Select-Object -First 1
    if ($ConfigMatch -and $ConfigMatch.Matches.Count -gt 0) {
      $candidates.Add($ConfigMatch.Matches[0].Groups["path"].Value)
    }
  }

  $LocalCliRoot = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
  if (Test-Path $LocalCliRoot) {
    $LocalCli = Get-ChildItem -Path $LocalCliRoot -Recurse -Filter codex.exe -File -ErrorAction SilentlyContinue |
      Sort-Object LastWriteTime -Descending |
      Select-Object -ExpandProperty FullName -First 1
    if ($LocalCli) {
      $candidates.Add($LocalCli)
    }
  }

  $FallbackCommand = Get-Command codex.exe -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty Source -First 1
  if ($FallbackCommand) {
    $candidates.Add($FallbackCommand)
  }

  foreach ($Candidate in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
    if (Test-Path $Candidate) {
      return $Candidate
    }
  }
  return $null
}

. (Join-Path $ScriptPath "automation_pause_guard.ps1")
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName "DailyCodexSeedReview" -LogPath $LogPath)) {
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FinishedAt] END exit_code=0 status=paused_by_pause_guard" | Out-File -FilePath $LogPath -Append -Encoding utf8
  exit 0
}
if ($IgnorePauseGuard) {
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD ignored_by_switch task=DailyCodexSeedReview" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
}

function ConvertFrom-MixedJsonOutput {
  param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$Label
  )

  try {
    return $Text | ConvertFrom-Json
  }
  catch {
    $Start = $Text.IndexOf("{")
    $End = $Text.LastIndexOf("}")
    if ($Start -ge 0 -and $End -gt $Start) {
      $JsonText = $Text.Substring($Start, $End - $Start + 1)
      return $JsonText | ConvertFrom-Json
    }
    throw "$Label output did not contain a JSON object"
  }
}

try {
  $PrepOutput = & $Python ".claude/scripts/codex_seed_review.py" prepare --run-date $RunDate --catch-up --catch-up-days 7 --json 2>&1
  $PrepExit = $LASTEXITCODE
  $PrepText = $PrepOutput -join [Environment]::NewLine
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PREP exit_code=$PrepExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
  $PrepText | Out-File -FilePath $LogPath -Append -Encoding utf8
  if ($PrepExit -ne 0) {
    throw "codex_seed_review.py prepare failed with exit code $PrepExit"
  }
  $Prep = $PrepText | ConvertFrom-Json
  $ReviewRunDate = if ($Prep.selected_run_date) { [string]$Prep.selected_run_date } else { $RunDate }
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PREP selected_run_date=$ReviewRunDate selection_reason=$($Prep.selection_reason)" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
  if ($Prep.status -eq "skipped_waiting_for_daily_pipeline") {
    $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
    "[$FinishedAt] END exit_code=0 status=skipped_waiting_for_daily_pipeline reason=$($Prep.reason)" |
      Out-File -FilePath $LogPath -Append -Encoding utf8
    exit 0
  }
  if ($PrepareOnly) {
    $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
    "[$FinishedAt] END exit_code=0 prepare_only=true" | Out-File -FilePath $LogPath -Append -Encoding utf8
    exit 0
  }

  $PromptPath = Join-Path $VaultRoot $Prep.prompt_path
  $RawOutputPath = Join-Path $VaultRoot $Prep.raw_output_path
  $CodexExit = 9009

  if ($SkipCodex) {
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX skipped_by_flag" | Out-File -FilePath $LogPath -Append -Encoding utf8
    $CodexExit = 98
  }
  else {
    $CodexModel = "gpt-5.5"
    $CodexCommandSource = Resolve-CodexCliPath
    if (-not $CodexCommandSource) {
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX not_found" | Out-File -FilePath $LogPath -Append -Encoding utf8
      $CodexExit = 9009
    }
    else {
      $PromptText = [System.IO.File]::ReadAllText($PromptPath, [System.Text.Encoding]::UTF8)
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX model=$CodexModel command=$CodexCommandSource raw_output=$RawOutputPath" | Out-File -FilePath $LogPath -Append -Encoding utf8
      $CodexInputPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review-input.md"
      [System.IO.File]::WriteAllText($CodexInputPath, $PromptText, [System.Text.Encoding]::UTF8)
      $CodexEventsPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review.events.log"
      $CodexErrorPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review.err.log"
      $CodexTimeoutSeconds = 7200
      $CodexMaxAttempts = 3
      $CodexTransientRetryDelaySeconds = 600
      $CodexArgs = @(
        "exec",
        "--model",
        "$CodexModel",
        "--skip-git-repo-check",
        "--ephemeral",
        "--cd",
        "$VaultRoot",
        "--output-last-message",
        "$RawOutputPath",
        "-"
      )
      if ($DangerouslyBypassSandbox) {
        $CodexArgs = @(
          "exec",
          "--model",
          "$CodexModel",
          "--skip-git-repo-check",
          "--ephemeral",
          "--cd",
          "$VaultRoot",
          "--dangerously-bypass-approvals-and-sandbox",
          "--output-last-message",
          "$RawOutputPath",
          "-"
        )
      }
      for ($Attempt = 1; $Attempt -le $CodexMaxAttempts; $Attempt++) {
        if (Test-Path $CodexEventsPath) { Remove-Item -LiteralPath $CodexEventsPath -Force -ErrorAction SilentlyContinue }
        if (Test-Path $CodexErrorPath) { Remove-Item -LiteralPath $CodexErrorPath -Force -ErrorAction SilentlyContinue }
        if (Test-Path $RawOutputPath) { Remove-Item -LiteralPath $RawOutputPath -Force -ErrorAction SilentlyContinue }
        "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX attempt=$Attempt/$CodexMaxAttempts" | Out-File -FilePath $LogPath -Append -Encoding utf8
        $CodexProcess = Start-Process -FilePath $CodexCommandSource -ArgumentList $CodexArgs -WorkingDirectory $VaultRoot -NoNewWindow -PassThru -RedirectStandardInput $CodexInputPath -RedirectStandardOutput $CodexEventsPath -RedirectStandardError $CodexErrorPath
        if (-not $CodexProcess.WaitForExit($CodexTimeoutSeconds * 1000)) {
          Stop-Process -Id $CodexProcess.Id -Force -ErrorAction SilentlyContinue
          $CodexExit = 124
          "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX timeout=${CodexTimeoutSeconds}s attempt=$Attempt" | Out-File -FilePath $LogPath -Append -Encoding utf8
        }
        else {
          $CodexProcess.Refresh()
          $CodexExit = if ($null -eq $CodexProcess.ExitCode) { 1 } else { $CodexProcess.ExitCode }
        }
        $CodexEvents = @()
        if (Test-Path $CodexEventsPath) {
          $CodexEvents += Get-Content -Encoding UTF8 $CodexEventsPath -ErrorAction SilentlyContinue
        }
        if (Test-Path $CodexErrorPath) {
          $CodexEvents += Get-Content -Encoding UTF8 $CodexErrorPath -ErrorAction SilentlyContinue
        }
        if ($CodexExit -eq 0) { break }
        $OutputStatus = $null
        if (Test-Path $RawOutputPath) {
          $OutputStatusOutput = & $Python ".claude/scripts/codex_seed_review.py" output-status --run-date $ReviewRunDate --codex-output $Prep.raw_output_path --codex-exit-code $CodexExit --json 2>&1
          $OutputStatusExit = $LASTEXITCODE
          $OutputStatusText = $OutputStatusOutput -join [Environment]::NewLine
          "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] OUTPUT_STATUS exit_code=$OutputStatusExit attempt=$Attempt" | Out-File -FilePath $LogPath -Append -Encoding utf8
          $OutputStatusText | Out-File -FilePath $LogPath -Append -Encoding utf8
          if ($OutputStatusExit -eq 0) {
            $OutputStatus = $OutputStatusText | ConvertFrom-Json
          }
        }
        if ($OutputStatus -and $OutputStatus.output_complete -eq "true") {
          "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX nonzero_exit_output_complete exit_code=$CodexExit nonblocking=$($OutputStatus.codex_exit_nonblocking) reason=$($OutputStatus.codex_nonblocking_exit_reason)" | Out-File -FilePath $LogPath -Append -Encoding utf8
          break
        }
        $TransientFailure = ($CodexEvents -join "`n") -match '503 Service Unavailable|Service temporarily unavailable|Reconnecting|temporarily unavailable|cf-ray|/v1/responses'
        if (-not $TransientFailure -or $Attempt -eq $CodexMaxAttempts) { break }
        $DelaySeconds = $CodexTransientRetryDelaySeconds
        "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX transient_failure_retry delay=${DelaySeconds}s exit_code=$CodexExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
        Start-Sleep -Seconds $DelaySeconds
      }
      $CodexEvents |
        Select-Object -Last 120 |
        ForEach-Object {
          $Line = $_.ToString()
          if ($Line.Length -gt 1000) {
            $Line.Substring(0, 1000) + " ...[truncated]"
          }
          else {
            $Line
          }
        } |
        Out-File -FilePath $LogPath -Append -Encoding utf8
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX exit_code=$CodexExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
    }
  }

  $WrapOutput = & $Python ".claude/scripts/codex_seed_review.py" wrap --run-date $ReviewRunDate --codex-output $Prep.raw_output_path --codex-exit-code $CodexExit --json 2>&1
  $WrapExit = $LASTEXITCODE
  $WrapText = $WrapOutput -join [Environment]::NewLine
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] WRAP exit_code=$WrapExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
  $WrapText | Out-File -FilePath $LogPath -Append -Encoding utf8
  if ($WrapExit -ne 0) {
    throw "codex_seed_review.py wrap failed with exit code $WrapExit"
  }

  $Wrap = $WrapText | ConvertFrom-Json
  $RefineExit = 0
  $RefineStatus = "not_started"
  $RefineReportPath = ""
  $DebateExit = 0
  $DebateStatus = "not_checked"
  $DebateReportPath = ""
  if ($Wrap.status -eq "done" -and $Prep.packet_path) {
    try {
      $RefineOutput = & $Python ".claude/scripts/refine_gemini_after_codex.py" --input-packet $Prep.packet_path --codex-report $Wrap.report_path --actions "rewrite,park,rewrite_once_more,needs_codex_recheck" --max-items 2 --json 2>&1
      $RefineExit = $LASTEXITCODE
      $RefineText = $RefineOutput -join [Environment]::NewLine
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] REFINE exit_code=$RefineExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
      $RefineText | Out-File -FilePath $LogPath -Append -Encoding utf8
      if ($RefineExit -eq 0) {
        $Refine = ConvertFrom-MixedJsonOutput -Text $RefineText -Label "REFINE"
        $RefineStatus = [string]$Refine.status
        $RefineReportPath = [string]$Refine.review_path
      }
      else {
        $RefineStatus = "failed_nonblocking"
      }
    }
    catch {
      $RefineExit = 1
      $RefineStatus = "failed_nonblocking"
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] REFINE ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
    }
  }
  else {
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] REFINE skipped wrap_status=$($Wrap.status)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  }
  try {
    $BattleOutput = & $Python ".claude/scripts/codex_seed_review.py" mandatory-battle-status --run-date $ReviewRunDate --json 2>&1
    $BattleExit = $LASTEXITCODE
    $BattleText = $BattleOutput -join [Environment]::NewLine
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE_CHECK exit_code=$BattleExit" | Out-File -FilePath $LogPath -Append -Encoding utf8
    $BattleText | Out-File -FilePath $LogPath -Append -Encoding utf8
    if ($BattleExit -ne 0) {
      throw "codex_seed_review.py mandatory-battle-status failed with exit code $BattleExit"
    }
    $Battle = $BattleText | ConvertFrom-Json
    $DebateStatus = [string]$Battle.status
    $DebateReportPath = [string]$Battle.report_path
    $DebateExit = if ($Battle.allow_for_codex_completion -eq "true") { 0 } else { 2 }
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE status=$DebateStatus effective_mode=$($Battle.effective_mode) allowed=$($Battle.allow_for_codex_completion) evidence=$($Battle.effective_evidence_path) packet=$($Battle.packet_path) report=$DebateReportPath reason=$($Battle.reason)" |
      Out-File -FilePath $LogPath -Append -Encoding utf8
  }
  catch {
    $DebateExit = 2
    $DebateStatus = "mandatory_battle_status_check_failed"
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  }
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  $ExitCode = if ($Wrap.status -eq "done" -and $DebateExit -eq 0) { 0 } else { 1 }
  "[$FinishedAt] END exit_code=$ExitCode report=$($Wrap.report_path) status=$($Wrap.status) codex_raw_exit_code=$($Wrap.codex_raw_exit_code) codex_exit_nonblocking=$($Wrap.codex_exit_nonblocking) codex_nonblocking_exit_reason=$($Wrap.codex_nonblocking_exit_reason) refine_status=$RefineStatus refine_exit_code=$RefineExit refine_report=$RefineReportPath debate_status=$DebateStatus debate_exit_code=$DebateExit debate_report=$DebateReportPath" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
  exit $ExitCode
}
catch {
  $FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FailedAt] ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  throw
}
