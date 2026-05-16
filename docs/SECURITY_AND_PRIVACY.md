# Security And Privacy

## 不要公开的内容

以下内容默认不应上传 GitHub：

- `.claude/backups/`、`.claude/scripts/backups/`、`.claude/logs/`、`.claude/tmp/`
- `.claude/settings.local.json`
- `.claudian/sessions/`
- `.smart-env/`、`.omx/`、`.sisyphus/`
- `.obsidian/workspace.json`
- `attachments/`
- `projects/arxiv-daily/zotero-pdf-cache/`
- `projects/arxiv-daily/metadata/*.sqlite`
- 任何 `.env`、key、token、cookie、credential 文件

本地体检发现旧备份目录里有疑似真实 API key。发布包不会包含这些文件，但已经暴露在本机文件系统里的 key 建议立即轮换。

## 公开前检查

```powershell
rg -n --hidden --glob '!exports/**' --glob '!archive/**' --glob '!.git/**' "(OPENAI_API_KEY|ANTHROPIC_AUTH_TOKEN|ZOTERO_API_KEY|GEMINI_API_KEY|sk-[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z_]{20,})" .
```

如果命中的是文档里对环境变量名的说明，可以保留；如果命中真实 key 值，必须移除并轮换。

## GitHub 上传建议

如果你是从 GitHub clone 的使用者，不需要执行本节；仓库根目录已经是脱敏发布包。

如果你是原维护者，并且手上还有完整本地工作目录，优先上传脱敏发布包：

```powershell
cd exports/github-ready-vault-YYYYMMDD
git init
git add .
git status --short
git commit -m "chore: publish literature vault workflow"
```

不要在原始工作目录里直接执行 `git add -A` 后上传。原始目录包含个人运行状态和历史备份，风险更高。
