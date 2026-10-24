param(
  [switch]$DryRun,
  [switch]$ShowLocalPaths,
  [switch]$IgnorePauseGuard,
  [string]$TaskName = "MonthlyFrontierReview",
  [int]$DayOfMonth = 1,
  [string]$Time = "21:00"
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$LogDir = Join-Path $VaultRoot "projects\research-agenda\reviews"
$WrapperPath = Join-Path $ScriptPath "run_monthly_frontier_review_task.ps1"

$TaskArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$WrapperPath`""
$CurrentUser = "$env:USERDOMAIN\$env:USERNAME"

if ($DryRun) {
  $DisplayUser = if ($ShowLocalPaths) { $CurrentUser } else { "<current-user>" }
  $DisplayWrapperPath = if ($ShowLocalPaths) { $WrapperPath } else { "<vault-root>\.claude\scripts\run_monthly_frontier_review_task.ps1" }
  Write-Host "DRY-RUN schtasks /Create /TN $TaskName /SC MONTHLY /D $DayOfMonth /ST $Time"
  Write-Host "WrapperPath: $DisplayWrapperPath"
  Write-Host "ActionArguments: $TaskArguments"
  Write-Host "Tip: add -ShowLocalPaths to print real local paths."
  exit 0
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
if (-not (Test-Path -LiteralPath $WrapperPath)) {
  throw "Missing task wrapper: $WrapperPath"
}
. (Join-Path $ScriptPath "automation_pause_guard.ps1")
$LogPath = Join-Path $LogDir "monthly-frontier-review-task.log"
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName $TaskName -LogPath $LogPath)) {
  throw "scheduled_task_pause_active_refusing_register:$TaskName"
}

$TaskRun = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$WrapperPath`""

try {
  $Result = & schtasks.exe /Create /TN $TaskName /SC MONTHLY /D $DayOfMonth /ST $Time /TR $TaskRun /F 2>&1
  $ExitCode = $LASTEXITCODE
  $Result | ForEach-Object { Write-Host $_ }
  if ($ExitCode -ne 0) {
    throw "schtasks.exe /Create failed with exit code $ExitCode"
  }
  & schtasks.exe /Query /TN $TaskName /FO LIST
}
catch {
  Write-Warning "schtasks registration failed: $($_.Exception.Message)"
  throw
}
