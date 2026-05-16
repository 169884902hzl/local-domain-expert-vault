param(
  [switch]$PrepareOnly,
  [switch]$SkipCodex,
  [switch]$DangerouslyBypassSandbox
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
    $CodexCommand = Get-Command codex.exe -CommandType Application -ErrorAction SilentlyContinue |
      Select-Object -First 1
    if (-not $CodexCommand) {
      $CodexCommand = Get-Command codex -CommandType Application -ErrorAction SilentlyContinue |
        Where-Object { $_.Source -match '\.exe$|\.cmd$' } |
        Select-Object -First 1
    }
    if (-not $CodexCommand) {
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX not_found" | Out-File -FilePath $LogPath -Append -Encoding utf8
      $CodexExit = 9009
    }
    else {
      $PromptText = [System.IO.File]::ReadAllText($PromptPath, [System.Text.Encoding]::UTF8)
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] CODEX start raw_output=$RawOutputPath" | Out-File -FilePath $LogPath -Append -Encoding utf8
      $CodexInputPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review-input.md"
      [System.IO.File]::WriteAllText($CodexInputPath, $PromptText, [System.Text.Encoding]::UTF8)
      $CodexEventsPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review.events.log"
      $CodexErrorPath = Join-Path $ReviewDir "$ReviewRunDate-codex-seed-review.err.log"
      $CodexTimeoutSeconds = 7200
      $CodexMaxAttempts = 3
      $CodexTransientRetryDelaySeconds = 600
      $CodexArgs = @(
        "exec",
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
        $CodexProcess = Start-Process -FilePath $CodexCommand.Source -ArgumentList $CodexArgs -WorkingDirectory $VaultRoot -NoNewWindow -PassThru -RedirectStandardInput $CodexInputPath -RedirectStandardOutput $CodexEventsPath -RedirectStandardError $CodexErrorPath
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
        $Refine = $RefineText | ConvertFrom-Json
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
  $BattlePacketPath = Join-Path $VaultRoot "projects\research-agenda\model-debates\$ReviewRunDate-gemini-deepseek-debate-packet.json"
  $BattleReportPath = Join-Path $VaultRoot "projects\research-agenda\reviews\$ReviewRunDate-gemini-deepseek-debate.md"
  if (Test-Path $BattlePacketPath) {
    try {
      $BattlePacket = Get-Content -Encoding UTF8 $BattlePacketPath -Raw | ConvertFrom-Json
      $DebateStatus = [string]$BattlePacket.status
      $DebateReportPath = "projects/research-agenda/reviews/$ReviewRunDate-gemini-deepseek-debate.md"
      if ($DebateStatus -ne "success") {
        $DebateExit = 2
      }
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE status=$DebateStatus packet=$BattlePacketPath report=$BattleReportPath" |
        Out-File -FilePath $LogPath -Append -Encoding utf8
    }
    catch {
      $DebateExit = 2
      $DebateStatus = "invalid_mandatory_battle_packet"
      "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
    }
  }
  else {
    $DebateExit = 2
    $DebateStatus = "missing_mandatory_battle"
    "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] MANDATORY_DEBATE missing packet=$BattlePacketPath report_exists=$(Test-Path $BattleReportPath)" |
      Out-File -FilePath $LogPath -Append -Encoding utf8
  }
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  $ExitCode = if ($Wrap.status -eq "done") { 0 } else { 1 }
  "[$FinishedAt] END exit_code=$ExitCode report=$($Wrap.report_path) status=$($Wrap.status) codex_raw_exit_code=$($Wrap.codex_raw_exit_code) codex_exit_nonblocking=$($Wrap.codex_exit_nonblocking) codex_nonblocking_exit_reason=$($Wrap.codex_nonblocking_exit_reason) refine_status=$RefineStatus refine_exit_code=$RefineExit refine_report=$RefineReportPath debate_status=$DebateStatus debate_exit_code=$DebateExit debate_report=$DebateReportPath" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
  exit $ExitCode
}
catch {
  $FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FailedAt] ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  throw
}
