param(
  [switch]$DryRun,
  [switch]$ShowLocalPaths,
  [switch]$IgnorePauseGuard,
  [string]$TaskName = "DailyCodexSeedReview",
  [string]$Time = "16:30"
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$LogDir = Join-Path $VaultRoot "projects\research-agenda\reviews"
$WrapperPath = Join-Path $ScriptPath "run_daily_codex_seed_review_task.ps1"

$TaskArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$WrapperPath`""
$CurrentUser = "$env:USERDOMAIN\$env:USERNAME"
$TimeParts = $Time.Split(":")
if ($TimeParts.Count -ne 2) {
  throw "Time must be HH:mm, got: $Time"
}
$At = [datetime]::Today.AddHours([int]$TimeParts[0]).AddMinutes([int]$TimeParts[1])

if ($DryRun) {
  $DisplayUser = if ($ShowLocalPaths) { $CurrentUser } else { "<current-user>" }
  $DisplayVaultRoot = if ($ShowLocalPaths) { $VaultRoot } else { "<vault-root>" }
  $DisplayWrapperPath = if ($ShowLocalPaths) { $WrapperPath } else { "<vault-root>\.claude\scripts\run_daily_codex_seed_review_task.ps1" }
  $DisplayTaskArguments = if ($ShowLocalPaths) { $TaskArguments } else { "-NoProfile -ExecutionPolicy Bypass -File `"<vault-root>\.claude\scripts\run_daily_codex_seed_review_task.ps1`"" }
  $DisplayLogDir = if ($ShowLocalPaths) { $LogDir } else { "<vault-root>\projects\research-agenda\reviews" }
  Write-Host "DRY-RUN Register-ScheduledTask -TaskName $TaskName -UserId $DisplayUser -Daily $Time"
  Write-Host "VaultRoot: $DisplayVaultRoot"
  Write-Host "WrapperPath: $DisplayWrapperPath"
  Write-Host "ActionExecute: powershell.exe"
  Write-Host "ActionArguments: $DisplayTaskArguments"
  Write-Host "LogDir: $DisplayLogDir"
  Write-Host "Tip: add -ShowLocalPaths to print real local paths for private debugging."
  exit 0
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
if (-not (Test-Path -LiteralPath $WrapperPath)) {
  throw "Missing task wrapper: $WrapperPath"
}
. (Join-Path $ScriptPath "automation_pause_guard.ps1")
$LogPath = Join-Path $LogDir "daily-codex-seed-review-task.log"
if (-not $IgnorePauseGuard -and (Test-VaultAutomationPaused -VaultRoot $VaultRoot -TaskName $TaskName -LogPath $LogPath)) {
  throw "scheduled_task_pause_active_refusing_register:$TaskName"
}

try {
  $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $TaskArguments
  $Trigger = New-ScheduledTaskTrigger -Daily -At $At
  $Settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)
  $Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Limited
  $Task = Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force
  if (-not $Task) {
    throw "Register-ScheduledTask returned no task object"
  }
  Get-ScheduledTask -TaskName $TaskName | Format-Table -AutoSize
}
catch {
  Write-Warning "Register-ScheduledTask failed: $($_.Exception.Message)"
  Write-Host "Falling back to schtasks.exe /Create for the current user."
  $LaunchScript = "& `"$WrapperPath`""
  $EncodedLaunchScript = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($LaunchScript))
  $TaskRun = "powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand $EncodedLaunchScript"
  $Result = & schtasks.exe /Create /TN $TaskName /SC DAILY /ST $Time /TR $TaskRun /F 2>&1
  $ExitCode = $LASTEXITCODE
  $Result | ForEach-Object { Write-Host $_ }
  if ($ExitCode -ne 0) {
    throw "schtasks.exe /Create failed with exit code $ExitCode"
  }
  & schtasks.exe /Query /TN $TaskName /FO LIST
}
