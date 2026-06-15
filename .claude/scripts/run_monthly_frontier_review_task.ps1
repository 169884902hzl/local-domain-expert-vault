param(
  [switch]$IgnorePauseGuard
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$ReviewDir = Join-Path $VaultRoot "projects\research-agenda\reviews"
$LogPath = Join-Path $ReviewDir "monthly-frontier-review-task.log"

New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null
Set-Location $VaultRoot

$Python = (Get-Command python).Source
$RunDate = Get-Date -Format "yyyy-MM-dd"
$StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$ReportMd = Join-Path $VaultRoot "output\$RunDate-frontier-research-map.md"
$RunMd = Join-Path $ReviewDir "$RunDate-monthly-frontier-review.md"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

"[$StartedAt] START MonthlyFrontierReview" | Out-File -FilePath $LogPath -Append -Encoding utf8

. (Join-Path $ScriptPath "automation_pause_guard.ps1")
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName "MonthlyFrontierReview" -LogPath $LogPath)) {
  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FinishedAt] END exit_code=0 status=paused_by_pause_guard" | Out-File -FilePath $LogPath -Append -Encoding utf8
  exit 0
}
if ($IgnorePauseGuard) {
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD ignored_by_switch task=MonthlyFrontierReview" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
}

try {
  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP index_rebuild" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/kb_embed.py" "build" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $IndexExit = $LASTEXITCODE

  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP topic_cluster" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/topic_cluster.py" "--k" "30" "--seed" "42" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $ClusterExit = $LASTEXITCODE

  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP cluster_gap_prep" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/cluster_gap_prep.py" "--min-main-score" "20" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $GapPrepExit = $LASTEXITCODE

  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP gap_distill" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/gap_distill.py" "--top-k" "40" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $DistillExit = $LASTEXITCODE

  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP frontier_prep" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/frontier_prep.py" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $FrontierExit = $LASTEXITCODE

  "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] STEP render_report" | Out-File -FilePath $LogPath -Append -Encoding utf8
  & $Python ".claude/scripts/render_frontier_report.py" 2>&1 | Out-File -FilePath $LogPath -Append -Encoding utf8
  $RenderExit = $LASTEXITCODE

  $Status = if (($IndexExit -eq 0) -and ($ClusterExit -eq 0) -and ($GapPrepExit -eq 0) -and ($DistillExit -eq 0) -and ($FrontierExit -eq 0) -and ($RenderExit -eq 0)) { "done" } else { "partial" }
  $SummaryLines = @(
    "---"
    "title: `"Monthly Frontier Review - $RunDate`""
    "tags: [research-agenda, frontier-review, automation]"
    "created: `"$RunDate`""
    "updated: `"$RunDate`""
    "type: `"permanent`""
    "status: `"$Status`""
    "summary: `"Monthly full-library frontier review: topic clustering, gap analysis, and frontier direction mapping.`""
    "---"
    ""
    "# Monthly Frontier Review - $RunDate"
    ""
    "- status: $Status"
    "- index_exit: $IndexExit"
    "- cluster_exit: $ClusterExit"
    "- gap_prep_exit: $GapPrepExit"
    "- distill_exit: $DistillExit"
    "- frontier_exit: $FrontierExit"
    "- render_exit: $RenderExit"
    "- report: ``$ReportMd``"
    "- topic_clusters: ``projects/research-agenda/evidence/topic_clusters.json``"
    "- distilled_gaps: ``projects/research-agenda/evidence/distilled_gaps.json``"
    "- frontier_directions: ``projects/research-agenda/evidence/frontier_directions.json``"
    "- boundary: deterministic pipeline only; frontier workflow (multi-agent deep read + synthesis) requires a separate claudian session."
  )
  [System.IO.File]::WriteAllText($RunMd, ($SummaryLines -join [Environment]::NewLine), $Utf8NoBom)

  $FinishedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  $ExitCode = [Math]::Max([Math]::Max([Math]::Max([Math]::Max([Math]::Max($IndexExit, $ClusterExit), $GapPrepExit), $DistillExit), $FrontierExit), $RenderExit)
  "[$FinishedAt] END exit_code=$ExitCode status=$Status report=$ReportMd" |
    Out-File -FilePath $LogPath -Append -Encoding utf8
  if ($ExitCode -ne 0) { exit 1 }
  exit 0
}
catch {
  $FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  "[$FailedAt] ERROR $($_.Exception.Message)" | Out-File -FilePath $LogPath -Append -Encoding utf8
  throw
}
