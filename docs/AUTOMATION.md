# Automation Guide

本页说明如何启动、配置和排查这个 vault 的自动化流程。所有 API key 都必须由使用者在自己的机器上配置；仓库不会包含任何真实 key。

## 自动化分层

| 层级 | 能力 | 必需条件 | 适合谁 |
| --- | --- | --- | --- |
| Level 0 | 本地检索和审计 | Python 3.10+ | 所有人 |
| Level 1 | arXiv 候选预览 | Python + 网络 | 想看每日候选但不写库 |
| Level 2 | Zotero 导入 | Zotero Desktop 或 Zotero Web API | 想把候选论文写入 Zotero/wiki |
| Level 3 | Claudian 精读 | Claudian / Claude Code 可用 | 想自动生成精读笔记 |
| Level 4 | Gemini idea 生成 | Gemini CLI 已登录 | 想做发散研究 idea |
| Level 5 | Codex seed review | Codex CLI 已登录 | 想做每日 idea 二次审查 |
| Level 6 | Windows 定时运行 | Windows Task Scheduler | 想每天自动跑 |

建议按层级逐步启用。不要第一次使用就直接注册计划任务。

## 0. 基础健康检查

在仓库根目录运行：

```powershell
python --version
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "VLM robot manipulation" --limit 5
```

预期：

- `audit_kb.py` 输出 `topic_issues=0 concept_issues=0 entity_issues=0`。
- `kb_search.py` 返回 `wiki/topics/...` 等本地路径。

这一步不需要 Zotero、Gemini、Codex 或 API key。

## 1. arXiv 候选预览

只抓取和排序，不写文件、不写 Zotero：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source search-api --max-candidates 30 --days-back 14
```

如果 arXiv 网络不稳定，可以降低候选数量：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source search-api --max-candidates 10 --days-back 7 --fetch-timeout 20 --fetch-retries 1
```

如果你已经同步过本地 arXiv metadata mirror，可以用：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30
```

## 2. 同步 arXiv metadata mirror

每日包装器会自动做这一步；也可以手动运行。

小规模测试：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
```

正式增量同步：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 60 --overlap-days 3
python .claude/scripts/arxiv_metadata_sync.py --status
```

非 dry-run 的 metadata 同步会写入 `projects/arxiv-daily/metadata/`，该目录内容默认不提交 Git。`--dry-run` 使用内存数据库，不创建 SQLite 或 lock 文件。

## 3. 配置 Zotero

### 本机 Zotero 路径

默认脚本会尝试访问：

- `http://localhost:23119/api/users/0`
- `http://127.0.0.1:23119`

这要求 Zotero Desktop 正在运行，并启用了本地 connector API。

### Web API 路径

如果要写入 Zotero Web API，设置环境变量：

```powershell
setx ZOTERO_USER_ID "<your-zotero-user-id>"
setx ZOTERO_API_KEY "<your-zotero-api-key>"
setx ZOTERO_COLLECTION_KEY "<your-collection-key>"
```

重新打开 PowerShell 后检查：

```powershell
python .claude/scripts/zotero_import.py --preflight --json
```

默认 `--json` 会脱敏 collection key、library id、collection name 和本机 collection tree id，适合贴到 issue 或审计报告。只有私下排障时才使用 `--unsafe-json`，不要把该输出公开。

可选环境变量：

| 变量 | 用途 |
| --- | --- |
| `ZOTERO_API_KEY` | Zotero Web API 写入 |
| `ZOTERO_USER_ID` / `ZOTERO_LIBRARY_ID` | Zotero library id |
| `ZOTERO_COLLECTION_KEY` | 默认导入 collection |
| `ZOTERO_LOCAL_API` | 覆盖本机 Zotero API URL |
| `ZOTERO_CONNECTOR_API` | 覆盖 Zotero connector URL |
| `ZOTERO_DATA_DIR` | 指向本机 Zotero 数据目录 |
| `ZOTERO_LOCAL_PDF_CACHE` | 本地 PDF cache 目录 |
| `ZOTERO_IMPORT_MODE` | 导入模式，默认 `local_connector_first` |
| `ZOTERO_UPLOAD_PDF_FILES` | 是否上传 PDF 文件 |
| `ZOTERO_LINKED_PDF_FALLBACK` | 是否允许 linked PDF fallback |
| `ZOTERO_REQUIRE_STORED_PDF` | 是否要求 stored PDF |

不要把这些值写入仓库。

附件同步、WebDAV、linked attachment、本地附件目录迁移和 Zotero 存储扩展见 [ZOTERO_STORAGE.md](ZOTERO_STORAGE.md)。本 vault 当前使用 CSTCloud 数据胶囊 WebDAV 路线，但 WebDAV 用户名和密码只保存在 Zotero 客户端里，公开仓库不会内置个人 Zotero 存储配置。

## 4. 导入单篇论文

```powershell
python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
python .claude/scripts/audit_kb.py
```

如果要通过 Claudian 完成精读，使用项目命令：

```text
/read-paper ZOTERO_KEY
```

或者手动走 finalize：

```powershell
python .claude/scripts/finalize_reading.py ZOTERO_KEY --analysis raw/readings/ZOTERO_KEY-analysis.md
python .claude/scripts/audit_kb.py --strict-reading
```

## 5. 手动运行每日 pipeline

### 低依赖模式

适合第一次真实写入前试跑。使用模板 idea，跳过精读：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py `
  --once `
  --source search-api `
  --idea-mode template `
  --skip-read `
  --max-candidates 40 `
  --days-back 14
```

如果没有 Zotero 写入能力，结果可能是 `partial`。这时请看 `ERROR:` 行确认是缺少 Zotero 凭据还是网络问题。

### 完整模式

适合已经配置 Zotero、Claudian 和 Gemini CLI 的机器：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py `
  --once `
  --source mirror-first `
  --idea-mode gemini-divergent `
  --idea-timeout 1200 `
  --gemini-model gemini-3.1-pro-preview `
  --raw-candidate-limit 8 `
  --min-raw-candidates 6 `
  --max-generated 3 `
  --read-timeout 2700 `
  --read-retries 1 `
  --read-retry-delay 90
```

主要输出：

- `projects/arxiv-daily/YYYY-MM-DD-run.md`
- `projects/arxiv-daily/YYYY-MM-DD-candidates.jsonl`
- `projects/arxiv-daily/YYYY-MM-DD-review-queue.md`
- `projects/research-agenda/daily/YYYY-MM-DD-agenda-delta.md`
- `projects/research-agenda/idea_bank/seed/...`
- `raw/readings/...`
- `wiki/topics/...`

这些输出默认不提交 Git。

## 6. Gemini CLI

Gemini 是可选的发散 idea 层。先确认 CLI 可用：

```powershell
gemini --version
$env:GEMINI_CLI_NO_RELAUNCH = "true"
python .claude/scripts/gemini_idea_probe.py --dry-run
```

真正调用 Gemini：

```powershell
$env:GEMINI_CLI_NO_RELAUNCH = "true"
python .claude/scripts/gemini_idea_probe.py --timeout 1200
```

如果你不用 Gemini，把每日 pipeline 的参数改成：

```powershell
--idea-mode template
```

## 7. Codex seed review

Codex seed review 是可选二次审查层。它会读取每日 pipeline 生成的 seed packet，并输出 review 报告。

先只准备 packet，不调用 Codex：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_codex_seed_review_task.ps1 -PrepareOnly
```

跳过 Codex 调用但完整走包装逻辑：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_codex_seed_review_task.ps1 -SkipCodex
```

真正调用 Codex 前，确认：

```powershell
codex --version
```

注意：当前包装器默认不绕过 Codex sandbox/approval。只有在你完全理解本机 CLI 权限边界时，才手动追加 `-DangerouslyBypassSandbox`。

## 8. Windows 计划任务

所有注册脚本都支持 `-DryRun`。先 dry run，再注册。默认 dry-run 输出会把当前 Windows 用户名和本机绝对路径替换成占位符；如果你在自己机器上私下排障，可以追加 `-ShowLocalPaths`。

### 每日 arXiv scout

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -Time "12:00"
```

默认任务名：`DailyArxivEmbodiedAIScout`

手动触发：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_arxiv_task.ps1
```

日志：

```powershell
Get-Content -Encoding UTF8 projects/arxiv-daily/scheduled-task.log -Tail 100
```

### 每日 Codex seed review

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -DryRun -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -Time "16:30"
```

默认任务名：`DailyCodexSeedReview`

日志：

```powershell
Get-Content -Encoding UTF8 projects/research-agenda/reviews/daily-codex-seed-review-task.log -Tail 100
```

### 每周 research agenda review

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun -DayOfWeek Sunday -Time "20:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DayOfWeek Sunday -Time "20:00"
```

默认任务名：`WeeklyResearchAgendaReview`

## 9. 检查和删除计划任务

```powershell
Get-ScheduledTask -TaskName DailyArxivEmbodiedAIScout
Get-ScheduledTask -TaskName DailyCodexSeedReview
Get-ScheduledTask -TaskName WeeklyResearchAgendaReview
python .claude/scripts/audit_scheduled_tasks.py
```

删除：

```powershell
Unregister-ScheduledTask -TaskName DailyArxivEmbodiedAIScout -Confirm:$false
Unregister-ScheduledTask -TaskName DailyCodexSeedReview -Confirm:$false
Unregister-ScheduledTask -TaskName WeeklyResearchAgendaReview -Confirm:$false
```

## 10. macOS/Linux 自动化边界

Python 检索、审计和 arXiv dry-run 可以在 macOS/Linux 上运行，但本仓库只提供 Windows Task Scheduler 注册脚本。非 Windows 用户可以把同等命令放入 `cron`、`systemd timer` 或自己的 CI runner；注意不要把 API key 写入仓库。

示例 cron 只作结构参考：

```cron
0 12 * * * cd /path/to/local-first-research-vault && python3 .claude/scripts/daily_arxiv_pipeline.py --dry-run --source search-api --max-candidates 30 --days-back 14 >> projects/arxiv-daily/cron.log 2>&1
```

## 11. 状态解释

| 状态 | 含义 |
| --- | --- |
| `success` | 本轮 pipeline 关键步骤完成 |
| `partial` | 主流程部分完成，但有增强步骤失败或缺凭据 |
| `missing_ZOTERO_API_KEY` | 缺 Zotero 写入凭据 |
| `skipped_waiting_for_daily_pipeline` | Codex review 等待每日 pipeline 先产生候选 |
| `NO_LOCAL_MATCHES` | 本地 wiki 没有检索命中 |

`partial` 不一定是坏状态。先读日志里的 `ERROR:` 行，再决定是否要配置缺失能力。

## 11. 推荐启用顺序

1. `audit_kb.py`
2. `kb_search.py`
3. `daily_arxiv_pipeline.py --dry-run`
4. Zotero preflight
5. 单篇 `ingest_paper.py`
6. 手动 `daily_arxiv_pipeline.py --once --idea-mode template`
7. Gemini CLI
8. `run_daily_arxiv_task.ps1`
9. `register_daily_arxiv_task.ps1`
10. Codex seed review
11. weekly agenda review

这样做的好处是每一步都有明确验收，不会把 Zotero、Gemini、Codex、计划任务的问题混在一起。
