param(
  [switch]$DryRun,
  [string]$TaskName = "DailyArxivEmbodiedAIScout",
  [string]$Time = "12:00"
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Resolve-Path (Join-Path $ScriptPath "..\..")
$LogDir = Join-Path $VaultRoot "projects\arxiv-daily"
$WrapperPath = Join-Path $ScriptPath "run_daily_arxiv_task.ps1"

$TaskArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$WrapperPath`""
$CurrentUser = "$env:USERDOMAIN\$env:USERNAME"
$TimeParts = $Time.Split(":")
if ($TimeParts.Count -ne 2) {
  throw "Time must be HH:mm, got: $Time"
}
$At = [datetime]::Today.AddHours([int]$TimeParts[0]).AddMinutes([int]$TimeParts[1])

if ($DryRun) {
  Write-Host "DRY-RUN Register-ScheduledTask -TaskName $TaskName -UserId $CurrentUser -DailyAt $Time"
  Write-Host "VaultRoot: $VaultRoot"
  Write-Host "WrapperPath: $WrapperPath"
  Write-Host "ActionExecute: powershell.exe"
  Write-Host "ActionArguments: $TaskArguments"
  Write-Host "LogDir: $LogDir"
  exit 0
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
if (-not (Test-Path -LiteralPath $WrapperPath)) {
  throw "Missing task wrapper: $WrapperPath"
}
try {
  $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $TaskArguments
  $Trigger = New-ScheduledTaskTrigger -Daily -At $At
  $Settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 6)
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
