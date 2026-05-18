# Deployment Checklist

这份清单给第一次 clone 的使用者用。它把“能浏览”“能检索”“能回跳 Zotero/PDF”“能自动跑每日 arXiv”分成可验证层级，避免把所有配置混在一起。

## 0. 先确定你要用到哪一层

| 层级 | 你想做什么 | 必需配置 | 成功信号 |
| --- | --- | --- | --- |
| Level 0 | 只浏览公开知识库 | Git；Obsidian 可选 | 能打开 `wiki/`、`Dashboard.md` |
| Level 1 | 本地证据检索 | Python 3.10+ | `audit_kb.py` 通过，`kb_search.py` 返回 `wiki/topics/...` |
| Level 2 | 从 Obsidian 笔记回到 Zotero/PDF 原文 | Zotero Desktop、PDF 附件、Paper Reading Workbench | 工作台能显示 `Open Zotero item` / `Open Zotero PDF attachment` |
| Level 3 | 从 Zotero 导入论文 metadata | Zotero API key、user id、collection key，或本机 Zotero Connector API | `zotero_import.py --preflight --json` 没有 `errors` |
| Level 4 | 使用 arXiv metadata mirror | 网络、本地 SQLite mirror | `arxiv_metadata_sync.py --status` 显示 `records_total > 0` |
| Level 5 | 每日自动跑 | Windows Task Scheduler 或自定义 cron/systemd | dry-run 路径正确，真实任务产生日志 |
| Level 6 | 完整 AI 工作流：Claudian / Gemini / DeepSeek / Codex | 本机 CLI 登录、权限确认 | Claudian 命令、Gemini idea、OpenCode DeepSeek battle、Codex review 分别能单独跑 |

建议按层级逐步启用。不要第一次就同时配置 Zotero、Claudian、Gemini、OpenCode/DeepSeek、Codex 和计划任务。

## 1. Fresh Clone Smoke Test

```powershell
git clone https://github.com/169884902hzl/local-domain-expert-vault.git
cd local-domain-expert-vault
python --version
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

期望输出：

- Python 是 `3.10+`。
- `audit_kb.py` 输出 `topic_issues=0 concept_issues=0 entity_issues=0`。
- `kb_search.py` 返回 `wiki/topics/...` 路径。

如果这一步失败，先不要配置 Zotero 或自动化。先确认你在仓库根目录运行命令，并且 Python 可以从当前 PowerShell 调用。

## 2. Obsidian First Open

1. 用 Obsidian 打开仓库根目录。
2. 打开 `Dashboard.md` 或 `wiki/INDEX.md`。
3. Graph 里建议使用 `path:wiki` 过滤。
4. 如果安装 Smart Connections，重建索引，并确认只索引 `wiki/`。

公开仓库默认只启用已经打包本体的 `paper-reading-workbench`。Claudian、Dataview、Smart Connections、Templater、Zotero Desktop Connector 需要你从 Obsidian Community Plugins 安装后手动启用。

## 3. Zotero Metadata And API

如果你只浏览和检索，可以跳过本节。

要让脚本读写 Zotero Web API：

1. 打开 [Zotero API Keys](https://www.zotero.org/settings/keys)。
2. 创建 private key。
3. 只读场景给 `Read` 权限即可。
4. 自动创建条目、写 collection、修复附件记录时才给 `Write` 权限。
5. 页面上的 numeric user id 写入 `ZOTERO_USER_ID`，不是邮箱或用户名。

PowerShell:

```powershell
setx ZOTERO_USER_ID "<your-zotero-user-id>"
setx ZOTERO_API_KEY "<your-zotero-api-key>"
setx ZOTERO_COLLECTION_KEY "<your-collection-key>"
```

重新打开 PowerShell 后验证：

```powershell
python .claude/scripts/zotero_import.py --preflight --json
```

常见结果：

| 输出 | 含义 | 下一步 |
| --- | --- | --- |
| `errors: []` | Zotero 配置可用 | 可以导入或运行自动化 |
| `missing_collection_key` | 没有设置目标 collection | 设置 `ZOTERO_COLLECTION_KEY` 或 `.claude/scripts/config.json` |
| `missing_ZOTERO_API_KEY` | 没有 Web API 写入 key | 只浏览可忽略；需要写 Zotero 时再配置 |
| `local_connector.reachable=false` | Zotero Desktop/Connector API 不可达 | 打开 Zotero Desktop，确认 `http://127.0.0.1:23119` 可访问 |

## 4. Zotero PDF / WebDAV

Zotero API key 管 metadata；WebDAV 管 PDF 附件同步。两者不是一回事。

当前公开示例使用 CSTCloud 数据胶囊：

- 服务入口：`https://data.cstcloud.cn/`
- Zotero WebDAV endpoint：`https://data.cstcloud.cn/dav`
- 公开资料和当前配置说明显示，实名认证后通常约 `20GB` 空间；实际额度以账号页面为准。

在 Zotero Desktop 里：

1. 打开 `Edit -> Settings -> Sync`。
2. 登录 Zotero 账号。
3. 文件同步选择 `WebDAV`。
4. URL 填 `https://data.cstcloud.cn/dav`，路径按 Zotero UI 显示补齐。
5. 用户名/密码使用数据胶囊里生成的 Zotero 专用 WebDAV 凭据。
6. 点击 Zotero 的验证按钮。

仓库不会保存 WebDAV 用户名、密码、PDF 或 Zotero 数据库。

## 5. Paper Reading Workbench

用途：人类在 Obsidian 精读笔记里看到结论后，可以回到 Zotero/PDF 原文对照。

前置条件：

- Zotero Desktop 正在运行。
- 当前 `wiki/topics/*.md` 有 `zotero_key`。
- Zotero item 下已有 stored PDF 或 linked PDF 附件。

操作：

1. 打开一篇 `wiki/topics/*.md`。
2. 运行命令 `Paper Reading Workbench: Open paper reading workbench for current note`。
3. 使用 `Open Zotero item` 或 `Open Zotero PDF attachment`。

如果没有 PDF 附件，工作台仍可能显示 Zotero item 或 arXiv fallback，但不能保证直接打开本地 PDF。

## 6. arXiv Mirror-First

先做零写入检查：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 5 --days-back 14 --idea-mode template --skip-read
```

fresh clone 的正常状态：

- `--status` 可能显示 `missing=true`。
- pipeline dry-run 可能显示 `source=mirror_missing`。
- 这不是失败，表示本机还没有 SQLite metadata mirror。

创建小规模本地 mirror：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
```

说明：

- mirror 保存 metadata，不保存 PDF 全文。
- 默认同步 arXiv OAI-PMH 的 `cs` 和 `stat` set。
- SQLite 位于 `projects/arxiv-daily/metadata/`，默认不提交 Git。
- Search API 只是 fallback/troubleshooting，不是主可靠路径。

## 7. Windows Scheduled Tasks

完整定时节奏有三个任务：

| 任务 | 默认时间 | 验收信号 |
| --- | --- | --- |
| `DailyArxivEmbodiedAIScout` | 每天 12:00 | `projects/arxiv-daily/scheduled-task.log` 有当天 START/END；daily pipeline 没有被 Search API first-run 误导。 |
| `DailyCodexSeedReview` | 每天 16:30 | `projects/research-agenda/reviews/daily-codex-seed-review-task.log` 有 PREP/WRAP；有 `YYYY-MM-DD-codex-seed-review.md` 或清楚的 waiting/partial 状态。 |
| `WeeklyResearchAgendaReview` | 每周日 20:00 | `weekly-agenda-review-task.log` 有 END；生成 `YYYY-MM-DD-weekly-agenda-review.md` 和 top-tier review artifacts。 |

先 dry run：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -DryRun -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun -DayOfWeek Sunday -Time "20:00"
```

确认输出里的任务名、时间和脚本路径符合预期后，再注册真实任务：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -Time "12:00"
Get-ScheduledTask -TaskName DailyArxivEmbodiedAIScout
```

常用日志：

```powershell
Get-Content -Encoding UTF8 projects/arxiv-daily/scheduled-task.log -Tail 100
Get-Content -Encoding UTF8 projects/research-agenda/reviews/daily-codex-seed-review-task.log -Tail 100
```

如果任务没有执行，先检查 Windows 用户权限、当前工作目录、PowerShell ExecutionPolicy 和日志路径。

## 8. Claudian / Gemini / DeepSeek / Codex

这些不是打开仓库和运行 `kb_search.py` 的前置条件，但它们是完整本地领域专家工作流的核心层：Claudian 负责 Obsidian 内问答、精读和项目命令；Claude Code / Claude CLI 是底层执行 worker；Gemini 负责 idea 发散；OpenCode / DeepSeek 负责敌对审稿；Codex 负责 seed review。

最小顺序：

1. 先用 `audit_kb.py` / `kb_search.py` 确认基础 vault 可用。
2. 安装 Obsidian Claudian 插件。
3. 在 Claudian 设置里选择本机 Claude/Codex CLI。
4. 用 `permissionMode = normal` 起步。
5. 如果要跑完整 idea battle，确认 `opencode --version` 可运行，并且 OpenCode provider 能调用 DeepSeek。
6. 先运行只读命令，例如 `/search-kb diffusion policy DLO`。
7. 理解项目命令会读写哪些目录后，再启用更高权限。

没有这些 CLI 时，基础 vault、Zotero 导入、KB 检索和 arXiv mirror smoke test 仍然可用；但这只是降级路径，不是本仓库想展示的完整研究工作流。

## 9. 什么时候算部署成功

按你的目标判断：

| 目标 | 成功标准 |
| --- | --- |
| 只看知识库 | Obsidian 能打开，`wiki/` 可浏览 |
| 本地问答 | `kb_search.py` 返回本地 evidence |
| Zotero 导入 | `zotero_import.py --preflight --json` 无 errors，`ingest_paper.py ZOTERO_KEY` 能生成 topic note |
| PDF 对照阅读 | Paper Reading Workbench 能打开 Zotero item/PDF |
| arXiv 自动化 | mirror status 有记录，daily dry-run 不再是 `mirror_missing` |
| Windows 定时 | Task Scheduler 中有任务，日志按时间更新 |
| AI 精读/idea | Claudian/Gemini/OpenCode DeepSeek/Codex 分别能单独跑，并且失败时有日志 |

## 10. 不要提交这些东西

- `.env`
- `.claude/scripts/config.json`
- API key、cookie、token
- Zotero 数据库
- PDF 文件
- SQLite mirror
- 日志、缓存、`projects/` 运行产物
- 本机绝对路径、用户名、截图中的账号信息

发布前可以运行：

```powershell
git status --short
git ls-files | Select-String -Pattern '(?i)(\.pdf$|\.sqlite$|\.sqlite3$|\.db$|\.log$|\.pyc$|__pycache__/|\.env$)'
rg -n --hidden --glob '!.git/**' "(OPENAI_API_KEY|ANTHROPIC_AUTH_TOKEN|ZOTERO_API_KEY|GEMINI_API_KEY|sk-[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z_]{20,})" .
```

如果你只是在本机使用，不需要把 `projects/`、`raw/`、`attachments/` 里的运行产物提交回公开仓库。
