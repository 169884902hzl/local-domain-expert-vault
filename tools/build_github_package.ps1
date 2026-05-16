param(
    [string]$PackageName = "github-ready-vault-$(Get-Date -Format yyyyMMdd)",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ExportRoot = Join-Path $Root "exports"
$PackageRoot = Join-Path $ExportRoot $PackageName

function Assert-UnderPath {
    param(
        [Parameter(Mandatory=$true)][string]$Child,
        [Parameter(Mandatory=$true)][string]$Parent
    )
    $parentFull = (Resolve-Path $Parent).Path.TrimEnd('\')
    $childFull = if (Test-Path $Child) {
        (Resolve-Path $Child).Path
    } else {
        [System.IO.Path]::GetFullPath($Child)
    }
    if (-not $childFull.StartsWith($parentFull + "\", [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to operate outside export root: $childFull"
    }
}

function Copy-FileIfExists {
    param(
        [Parameter(Mandatory=$true)][string]$RelativePath
    )
    $src = Join-Path $Root $RelativePath
    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
        return
    }
    $dst = Join-Path $PackageRoot $RelativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
}

function Copy-Tree {
    param(
        [Parameter(Mandatory=$true)][string]$RelativePath,
        [string[]]$ExcludeDirs = @(),
        [string[]]$ExcludeFiles = @()
    )
    $src = Join-Path $Root $RelativePath
    if (-not (Test-Path -LiteralPath $src -PathType Container)) {
        return
    }
    $dst = Join-Path $PackageRoot $RelativePath
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    $args = @($src, $dst, "/E", "/MT:32", "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS", "/NP")
    if ($ExcludeDirs.Count -gt 0) {
        $args += "/XD"
        $args += $ExcludeDirs
    }
    if ($ExcludeFiles.Count -gt 0) {
        $args += "/XF"
        $args += $ExcludeFiles
    }
    & robocopy @args | Out-Null
    if ($LASTEXITCODE -ge 8) {
        throw "robocopy failed for $RelativePath with exit code $LASTEXITCODE"
    }
}

function Copy-ObsidianPluginConfig {
    param(
        [Parameter(Mandatory=$true)][string]$PluginName
    )
    $src = Join-Path $Root ".obsidian\plugins\$PluginName"
    if (-not (Test-Path -LiteralPath $src -PathType Container)) {
        return
    }
    $dst = Join-Path $PackageRoot ".obsidian\plugins\$PluginName"
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    foreach ($file in @("manifest.json", "data.json")) {
        $path = Join-Path $src $file
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            Copy-Item -LiteralPath $path -Destination (Join-Path $dst $file) -Force
        }
    }
    if ($PluginName -eq "claudian") {
        $dataPath = Join-Path $dst "data.json"
        @{
            tabManagerState = @{
                openTabs = @()
                activeTabId = $null
            }
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $dataPath -Encoding UTF8
    }
}

function Sanitize-ClaudianSettings {
    $src = Join-Path $Root ".claudian\claudian-settings.json"
    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
        return
    }
    $dst = Join-Path $PackageRoot ".claudian\claudian-settings.json"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
    $settings = Get-Content -LiteralPath $src -Encoding UTF8 -Raw | ConvertFrom-Json
    $settings.userName = ""
    if ($settings.PSObject.Properties.Name -contains "permissionMode") {
        $settings.permissionMode = "normal"
    }
    if ($settings.PSObject.Properties.Name -contains "systemPrompt") {
        $settings.systemPrompt = [string]$settings.systemPrompt -replace "vault owner 的本地文献知识库专家", "这个 Obsidian vault 的本地文献知识库专家"
    }
    $settings.persistentExternalContextPaths = @()
    $settings.sharedEnvironmentVariables = ""
    $settings.envSnippets = @()
    foreach ($providerName in @("claude", "codex")) {
        if ($settings.providerConfigs.PSObject.Properties.Name -contains $providerName) {
            $provider = $settings.providerConfigs.$providerName
            if ($provider.PSObject.Properties.Name -contains "cliPath") { $provider.cliPath = "" }
            if ($provider.PSObject.Properties.Name -contains "cliPathsByHost") { $provider.cliPathsByHost = @{} }
            if ($provider.PSObject.Properties.Name -contains "environmentVariables") { $provider.environmentVariables = "" }
            if ($provider.PSObject.Properties.Name -contains "environmentHash") { $provider.environmentHash = "" }
            if ($provider.PSObject.Properties.Name -contains "installationMethodsByHost") { $provider.installationMethodsByHost = @{} }
            if ($provider.PSObject.Properties.Name -contains "wslDistroOverridesByHost") { $provider.wslDistroOverridesByHost = @{} }
        }
    }
    $settings | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $dst -Encoding UTF8
}

function Sanitize-PublicInstructionFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )
    $path = Join-Path $PackageRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return
    }
    $text = Get-Content -LiteralPath $path -Encoding UTF8 -Raw
    $text = $text -replace "你正在 vault owner 的 Obsidian 文献知识库中工作。", "你正在这个 Obsidian 文献 vault 中工作。"
    $text = $text -replace "- 姓名：vault owner", "- 姓名：<your-name>"
    $text = $text -replace "- 身份：<private-researcher-role>", "- 身份：机器人操控方向研究者"
    $text | Set-Content -LiteralPath $path -Encoding UTF8
}

function Sanitize-PackageTextFiles {
    $textExtensions = @(".json", ".md", ".ps1", ".py", ".toml", ".txt", ".yaml", ".yml")
    $files = Get-ChildItem -LiteralPath $PackageRoot -Recurse -File | Where-Object {
        $textExtensions -contains $_.Extension.ToLowerInvariant()
    }
    foreach ($file in $files) {
        $text = Get-Content -LiteralPath $file.FullName -Encoding UTF8 -Raw
        $updated = $text
        $updated = $updated.Replace("<private-vault-path>", "<local-vault-path>")
        $updated = $updated.Replace("<private-zotero-cache>", ".local\zotero-pdf-cache")
        $updated = $updated.Replace("<private-researcher-role>", "机器人操控方向研究者")
        $updated = $updated.Replace("<private-zotero-collection>", "<your-zotero-collection>")
        if ($updated -ne $text) {
            $updated | Set-Content -LiteralPath $file.FullName -Encoding UTF8
        }
    }
}

New-Item -ItemType Directory -Force -Path $ExportRoot | Out-Null
Assert-UnderPath -Child $PackageRoot -Parent $ExportRoot
if (Test-Path -LiteralPath $PackageRoot) {
    if (-not $Force) {
        throw "Package already exists: $PackageRoot. Re-run with -Force to replace it."
    }
    Assert-UnderPath -Child $PackageRoot -Parent $ExportRoot
    Remove-Item -LiteralPath $PackageRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $PackageRoot | Out-Null

foreach ($file in @(
    ".gitignore",
    ".gitattributes",
    "README.md",
    "LICENSE",
    "AGENTS.md",
    "CLAUDE.md",
    "SCHEMA.md",
    "Dashboard.md"
)) {
    Copy-FileIfExists $file
}
Sanitize-PublicInstructionFile "AGENTS.md"
Sanitize-PublicInstructionFile "CLAUDE.md"

Copy-Tree "docs"
Copy-Tree "templates"
Copy-Tree "wiki"
Copy-Tree ".claude\agents"
Copy-Tree ".claude\commands"
Copy-Tree ".claude\skills"
Copy-Tree ".claude\scripts" -ExcludeDirs @("backups", "__pycache__") -ExcludeFiles @("config.json", "*.pyc", "*.bak", "re-audit-prompt.md")
Copy-FileIfExists "tools\build_github_package.ps1"

foreach ($file in @(
    ".claude\settings.json",
    ".claude\scripts\config.example.json",
    ".obsidian\app.json",
    ".obsidian\appearance.json",
    ".obsidian\community-plugins.json",
    ".obsidian\core-plugins.json",
    ".obsidian\daily-notes.json",
    ".obsidian\graph.json",
    ".obsidian\templates.json"
)) {
    Copy-FileIfExists $file
}

foreach ($plugin in @(
    "claudian",
    "dataview",
    "obsidian-smart-connections",
    "obsidian-zotero-desktop-connector",
    "paper-reading-workbench",
    "templater-obsidian"
)) {
    Copy-ObsidianPluginConfig $plugin
}

Sanitize-ClaudianSettings
Sanitize-PackageTextFiles

foreach ($dir in @("raw", "raw\readings", "output", "projects", "attachments")) {
    $directory = Join-Path $PackageRoot $dir
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    "# Keep this directory in Git; local contents are ignored by default." |
        Set-Content -LiteralPath (Join-Path $directory ".gitkeep") -Encoding UTF8
}

$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$manifest = @"
# Package Manifest

Generated: $generatedAt
Source: local working copy (path omitted from public package)

## Included

- wiki/ structured knowledge layer
- .claude/commands/, .claude/scripts/, .claude/agents/, .claude/skills/
- sanitized .claudian/claudian-settings.json
- minimal .obsidian/ settings and plugin config files
- templates/, SCHEMA.md, Dashboard.md, AGENTS.md, CLAUDE.md
- root GitHub documentation, license boundary, safety docs, and tools/build_github_package.ps1

## Excluded

- .claude/backups/, .claude/scripts/backups/, .claude/logs/, .claude/tmp/
- .claude/settings.local.json
- .claudian/sessions/
- .smart-env/, .omx/, .sisyphus/
- attachments/ contents
- raw/ contents
- output/ contents
- projects/ contents
- daily/, archive/, exports/, projectsideas/, Excalidraw/
- PDFs, SQLite databases, local caches, and machine-specific credentials

## Verify

    python .claude/scripts/audit_kb.py
    python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
"@
$manifest | Set-Content -LiteralPath (Join-Path $PackageRoot "PACKAGE_MANIFEST.md") -Encoding UTF8

Write-Host "PACKAGE_READY: $PackageRoot"
