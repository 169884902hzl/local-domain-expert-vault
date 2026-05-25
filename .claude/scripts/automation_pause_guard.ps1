function ConvertTo-DateTimeOffsetOrNull {
  param([string]$Value)
  if ([string]::IsNullOrWhiteSpace($Value)) {
    return $null
  }
  try {
    return [DateTimeOffset]::Parse($Value)
  }
  catch {
    return $null
  }
}

function Write-AutomationPauseGuardLog {
  param(
    [string]$LogPath,
    [string]$Message
  )
  if ([string]::IsNullOrWhiteSpace($LogPath)) {
    return
  }
  $LogDir = Split-Path -Parent $LogPath
  if (-not [string]::IsNullOrWhiteSpace($LogDir)) {
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
  }
  $Message | Out-File -FilePath $LogPath -Append -Encoding utf8
}

function Test-PauseRecordSuperseded {
  param(
    [string]$VaultRoot,
    [string]$PausePath,
    [DateTimeOffset]$PausedAt
  )
  $PauseDir = Join-Path $VaultRoot "projects\arxiv-daily\pauses"
  if (-not (Test-Path -LiteralPath $PauseDir)) {
    return $false
  }
  $PauseLeaf = Split-Path -Leaf $PausePath
  foreach ($ResumeFile in Get-ChildItem -LiteralPath $PauseDir -Filter "resume-*.json" -File -ErrorAction SilentlyContinue) {
    try {
      $Resume = Get-Content -LiteralPath $ResumeFile.FullName -Encoding UTF8 -Raw | ConvertFrom-Json
    }
    catch {
      continue
    }
    $Prior = [string]$Resume.prior_pause_record
    if ([string]::IsNullOrWhiteSpace($Prior)) {
      continue
    }
    if (($Prior -ne $PausePath) -and (-not $Prior.EndsWith($PauseLeaf))) {
      continue
    }
    $ResumedAt = ConvertTo-DateTimeOffsetOrNull ([string]$Resume.resumed_at)
    if ($null -ne $ResumedAt -and $ResumedAt -gt $PausedAt) {
      return $true
    }
  }
  return $false
}

function Test-VaultAutomationPaused {
  param(
    [string]$VaultRoot,
    [string]$TaskName,
    [string]$LogPath
  )
  if ([Environment]::GetEnvironmentVariable("VAULT_AUTOMATION_IGNORE_PAUSE_GUARD", "Process") -eq "1") {
    Write-AutomationPauseGuardLog -LogPath $LogPath -Message "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD ignored_by_env task=$TaskName"
    return $false
  }
  $PauseDir = Join-Path $VaultRoot "projects\arxiv-daily\pauses"
  if (-not (Test-Path -LiteralPath $PauseDir)) {
    return $false
  }
  $Now = [DateTimeOffset](Get-Date)
  $Today = $Now.ToString("yyyy-MM-dd")
  $PauseFiles = Get-ChildItem -LiteralPath $PauseDir -Filter "pause-*.json" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending
  foreach ($PauseFile in $PauseFiles) {
    try {
      $Pause = Get-Content -LiteralPath $PauseFile.FullName -Encoding UTF8 -Raw | ConvertFrom-Json
    }
    catch {
      continue
    }
    if ([string]$Pause.schema_version -ne "vault_automation_pause.v1") {
      continue
    }
    if (@($Pause.disabled_tasks) -notcontains $TaskName) {
      continue
    }
    $PausedAt = ConvertTo-DateTimeOffsetOrNull ([string]$Pause.paused_at)
    if ($null -eq $PausedAt) {
      continue
    }
    if (Test-PauseRecordSuperseded -VaultRoot $VaultRoot -PausePath $PauseFile.FullName -PausedAt $PausedAt) {
      continue
    }
    $DateActive = @($Pause.paused_dates) -contains $Today
    $ResumeAt = ConvertTo-DateTimeOffsetOrNull ([string]$Pause.intended_resume_not_before)
    $TimeActive = $null -ne $ResumeAt -and $Now -lt $ResumeAt
    if ($DateActive -or $TimeActive) {
      Write-AutomationPauseGuardLog -LogPath $LogPath -Message "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")] PAUSE_GUARD active task=$TaskName pause_record=$($PauseFile.FullName) reason=$($Pause.pause_reason) intended_resume_not_before=$($Pause.intended_resume_not_before)"
      return $true
    }
  }
  return $false
}
