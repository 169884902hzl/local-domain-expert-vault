param(
  [switch]$IgnorePauseGuard
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$ReviewDir = Join-Path $VaultRoot "projects\research-agenda\reviews"
$LogPath = Join-Path $ReviewDir "weekly-agenda-review-task.log"

New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null
Set-Location $VaultRoot

$Python = (Get-Command python).Source
$RunDate = Get-Date -Format "yyyy-MM-dd"
$StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$ReviewJson = Join-Path $ReviewDir "$RunDate-weekly-agenda-review.json"
$AuditJson = Join-Path $ReviewDir "$RunDate-weekly-agenda-audit.json"
$TopTierJson = Join-Path $ReviewDir "$RunDate-weekly-top-tier-review.json"
$StrategyJson = Join-Path $ReviewDir "$RunDate-weekly-strategy-review.json"
$RunMd = Join-Path $ReviewDir "$RunDate-weekly-agenda-review.md"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

"[$StartedAt] START WeeklyResearchAgendaReview" | Out-File -FilePath $LogPath -Append -Encoding utf8

. (Join-Path $ScriptPath "automation_pause_guard.ps1")
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName "WeeklyResearchAgendaReview" -LogPath $LogPath)) {
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FinishedAt] END exit_code=0 status=paused_by_pause_guard" | Out-File -FilePath $LogPath -Append -Encoding utf8
  exit 0
}
if ($IgnorePauseGuard) {
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD ignored_by_switch task=WeeklyResearchAgendaReview" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
}

try {
  $ReviewOutput = & $Python ".claude/scripts/research_agenda_review.py" --json 2>&1
  $ReviewExit = $LASTEXITCODE
  [System.IO.File]::WriteAllText($ReviewJson, ($ReviewOutput -join [Environment]::NewLine), $Utf8NoBom)

  $AuditOutput = & $Python ".claude/scripts/audit_research_agenda.py" --json 2>&1
  $AuditExit = $LASTEXITCODE
  [System.IO.File]::WriteAllText($AuditJson, ($AuditOutput -join [Environment]::NewLine), $Utf8NoBom)

  $TopTierOutput = & $Python ".claude/scripts/codex_seed_review.py" top-tier-weekly --end-date $RunDate --days 7 --json 2>&1
  $TopTierExit = $LASTEXITCODE
  [System.IO.File]::WriteAllText($TopTierJson, ($TopTierOutput -join [Environment]::NewLine), $Utf8NoBom)

  & $Python ".claude/scripts/enrich_seed_gates.py" --all 2>&1 |
    ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
  $EnrichExit = $LASTEXITCODE
  & $Python ".claude/scripts/review_seed_gates.py" --all 2>&1 |
    ForEach-Object { $_ | Out-File -FilePath $LogPath -Append -Encoding utf8 }
  $GateReviewExit = $LASTEXITCODE
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] SEED_GATE enrich_exit=$EnrichExit gate_review_exit=$GateReviewExit" |
    Out-File -FilePath $LogPath -Append -Encoding utf8

  $StrategyOutput = & $Python ".claude/scripts/weekly_strategy_review.py" --run-date $RunDate 2>&1
  $StrategyExit = $LASTEXITCODE
  [System.IO.File]::WriteAllText($StrategyJson, ($StrategyOutput -join [Environment]::NewLine), $Utf8NoBom)
  $TopTier = $null
  try {
    $TopTier = ($TopTierOutput -join [Environment]::NewLine) | ConvertFrom-Json
  }
  catch {
    $TopTier = $null
  }
  $TopTierReport = if ($TopTier -and $TopTier.report_path) { $TopTier.report_path } else { "unavailable" }
  $TopTierStatus = if ($TopTier -and $TopTier.status) { $TopTier.status } else { "unknown" }
  $StrategyStatus = if ($StrategyExit -eq 0) { "done" } elseif ($StrategyExit -eq 2) { "warn" } else { "partial" }

  $Status = if (($ReviewExit -eq 0) -and ($AuditExit -eq 0) -and ($TopTierExit -eq 0) -and ($TopTierStatus -eq "done") -and ($StrategyExit -in @(0, 2)) -and ($GateReviewExit -in @(0, 2))) { "done" } else { "partial" }
  $Summary = "Weekly research agenda review status: $Status."
  $SummaryLines = @(
    "---"
    "title: `"Weekly Research Agenda Review - $RunDate`""
    "tags: [research-agenda, weekly-review, automation]"
    "created: `"$RunDate`""
    "updated: `"$RunDate`""
    "type: `"permanent`""
    "status: `"$Status`""
    "summary: `"$Summary`""
    "---"
    ""
    "# Weekly Research Agenda Review - $RunDate"
    ""
    "- status: $Status"
    "- review_exit_code: $ReviewExit"
    "- audit_exit_code: $AuditExit"
    "- top_tier_exit_code: $TopTierExit"
    "- strategy_exit_code: $StrategyExit"
    "- top_tier_status: $TopTierStatus"
    "- strategy_status: $StrategyStatus"
    "- review_json: ``projects/research-agenda/reviews/$RunDate-weekly-agenda-review.json``"
    "- audit_json: ``projects/research-agenda/reviews/$RunDate-weekly-agenda-audit.json``"
    "- top_tier_json: ``projects/research-agenda/reviews/$RunDate-weekly-top-tier-review.json``"
    "- strategy_json: ``projects/research-agenda/reviews/$RunDate-weekly-strategy-review.json``"
    "- top_tier_report: ``$TopTierReport``"
    "- boundary: no idea folders are moved automatically; use ``research_agenda_review.py --apply`` only after human approval."
  )
  [System.IO.File]::WriteAllText($RunMd, ($SummaryLines -join [Environment]::NewLine), $Utf8NoBom)

  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  $BlockingStrategyExit = if ($StrategyExit -eq 2) { 0 } else { $StrategyExit }
  $ExitCode = [Math]::Max([Math]::Max([Math]::Max($ReviewExit, $AuditExit), $TopTierExit), $BlockingStrategyExit)
  if ($TopTierStatus -ne "done") {
    $ExitCode = [Math]::Max($ExitCode, 1)
  }
  "[$FinishedAt] END exit_code=$ExitCode review_json=$ReviewJson audit_json=$AuditJson top_tier_json=$TopTierJson strategy_json=$StrategyJson top_tier_report=$TopTierReport top_tier_status=$TopTierStatus strategy_status=$StrategyStatus" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
  if ($ExitCode -ne 0) {
    exit 1
  }
  exit 0
}
catch {
  $FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FailedAt] ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  throw
}
