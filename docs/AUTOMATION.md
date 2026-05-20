# Automation Guide

本页说明如何启动、配置和排查这个 vault 的自动化流程。所有 API key 都必须由使用者在自己的机器上配置；仓库不会包含任何真实 key。

## 自动化分层

| 层级 | 能力 | 必需条件 | 适合谁 |
| --- | --- | --- | --- |
| Level 0 | 本地检索和审计 | Python 3.10+ | 所有人 |
| Level 1 | arXiv metadata mirror smoke test | Python + 网络 | 想确认 OAI-PMH metadata 同步入口可用 |
| Level 2 | mirror-first daily pipeline dry-run | Python + metadata mirror | 想看每日候选但不写库 |
| Level 3 | optional Search API fallback troubleshooting | Python + 网络 | 只在 mirror 缺失、过旧或候选不足时排错 |
| Level 4 | Zotero + Claudian + Gemini + DeepSeek + Codex full workflow | Zotero / Claudian / Gemini / OpenCode DeepSeek / Codex 逐步配置 | 想复现完整导入、精读、idea 发散、敌对审稿、二审 |
| Level 5 | Windows 定时运行 | Windows Task Scheduler | 想每天自动跑 |

建议按层级逐步启用。不要第一次使用就直接注册计划任务。

## 默认定时节奏

完整本地领域专家工作流默认拆成三个计划任务，而不是把所有事情塞进一个脚本：

| 默认时间 | 任务名 | 入口脚本 | 输出位置 | 边界 |
| --- | --- | --- | --- | --- |
| 每天 12:00 | `DailyArxivEmbodiedAIScout` | `.claude/scripts/run_daily_arxiv_task.ps1` | `projects/arxiv-daily/scheduled-task.log` | 负责 arXiv mirror sync、daily pipeline、Gemini greenhouse、OpenCode/DeepSeek battle 和质量审计；可能因为 Zotero/CLI/网络缺失返回 `partial`。 |
| 每天 16:30 | `DailyCodexSeedReview` | `.claude/scripts/run_daily_codex_seed_review_task.ps1` | `projects/research-agenda/reviews/daily-codex-seed-review-task.log` 和 `YYYY-MM-DD-codex-seed-review.md` | 对当天或最近 7 天未审 seed 做 Codex 二审；不删除、不晋升、不声明 novelty。 |
| 每周日 20:00 | `WeeklyResearchAgendaReview` | `.claude/scripts/run_weekly_agenda_review_task.ps1` | `projects/research-agenda/reviews/weekly-agenda-review-task.log`、`YYYY-MM-DD-weekly-agenda-review.md`、`YYYY-MM-DD-weekly-top-tier-review.md` | 汇总一周 agenda 状态、审计结果和 top-tier pressure test；不会自动移动 idea 文件夹。 |

推荐启用顺序：先完成 Level 0-4 的手动验证，再注册 12:00 每日任务；确认每天有 seed packet 后，再启用 16:30 Codex 二审；最后启用周日 20:00 周审。

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

这一步不需要 Zotero、Gemini、OpenCode/DeepSeek、Codex 或 API key。

## 1. arXiv metadata mirror smoke test

每日自动化的主叙事是 **local SQLite metadata mirror first**：先通过 arXiv 官方 OAI-PMH endpoint 同步或检查本地 arXiv metadata mirror，再让 pipeline 以 `mirror-first` 方式选候选。这样主路径不依赖 Search API 的实时可用性，也能减少 arXiv 429、timeout 或外部服务限流造成的误判。

先做 OAI-PMH mirror dry-run，不创建 SQLite 或 lock 文件：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
```

arXiv 数据层边界：

- OAI-PMH sync 写入 `projects/arxiv-daily/metadata/arxiv_metadata.sqlite`。
- SQLite mirror 只保存 metadata：title、authors、abstract、dates、categories、URL、PDF URL、DOI、journal reference、comments。
- 默认同步 OAI-PMH sets 是 `cs` 和 `stat`，不是全 arXiv，也不是 PDF 全文。
- 公开仓库不提交 SQLite mirror；clone 后需要自己运行 dry-run 或 incremental sync。
- Zotero import 后续使用选中的 metadata / PDF URL 创建 library item；PDF 由 Zotero 官方存储、WebDAV 或 linked attachment 管理，不由 arXiv mirror 保存。

查看本机 mirror 状态：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --status
```

`--status` 是只读命令。fresh clone 中如果还没有 SQLite mirror，它会输出 `missing=true`，不会创建 `projects/arxiv-daily/metadata/arxiv_metadata.sqlite`。

## 2. mirror-first daily pipeline dry-run

预览每日候选，不写 Zotero、不写 vault：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

`mirror-first` 会先查本地 SQLite metadata mirror。dry-run 会读取真实本地 SQLite；如果 mirror 不存在、为空或候选不足，它会快速输出 `arxiv_mirror_missing` / `arxiv_mirror_empty` / `arxiv_mirror_insufficient`，不会静默 fallback 到 Search API。这样可以确认你是否真的有本地 mirror，而不是把外部 Search API 结果误判成 mirror-first 成功。

如果你想看到真实候选，先运行一次小规模本地同步：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

完整非 dry-run 每日任务仍然允许在 mirror 过旧或候选不足时 fallback 到 Search API；那是排错和兜底路径，不是 first-run 成功标准。

## 3. optional Search API fallback troubleshooting

`search-api` 只作为 fallback / troubleshooting。外部 Search API 可能因为 429、timeout 或当天结果为空而返回 0 candidates；这不能单独说明 vault 或本地知识库坏了，也不应该作为发布可靠性的主路径。

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source search-api --max-candidates 10 --days-back 7 --fetch-timeout 20 --fetch-retries 1
```

## 4. 同步 arXiv metadata mirror

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

非 dry-run 的 metadata 同步会写入 `projects/arxiv-daily/metadata/`，该目录内容默认不提交 Git。`--dry-run` 使用内存数据库，不创建 SQLite 或 lock 文件；`--max-pages 1` 出现 `partial` / `resumption_token` 是预期 smoke-test 结果，表示只拉了第一页。不要在文档或 README 中写死本机 mirror 规模；如需查看规模，运行 `python .claude/scripts/arxiv_metadata_sync.py --status`。

## 5. 配置 Zotero

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

`ZOTERO_API_KEY` 需要由使用者在 [Zotero API Keys](https://www.zotero.org/settings/keys) 自己创建。只读导入给 `Read` 权限即可；如果自动化要创建条目、写入 collection 或修复附件记录，再给 `Write` 权限。页面上的数字 user id 写入 `ZOTERO_USER_ID`，不要使用用户名或邮箱。

如果还不知道 collection key，重新打开 PowerShell 后运行：

```powershell
$headers = @{
  "Zotero-API-Key" = $env:ZOTERO_API_KEY
  "Zotero-API-Version" = "3"
}
Invoke-RestMethod "https://api.zotero.org/users/$env:ZOTERO_USER_ID/collections?format=json&limit=100" -Headers $headers |
  ForEach-Object { "{0}`t{1}" -f $_.data.key, $_.data.name }
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

## 6. 导入单篇论文

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

## 7. 手动运行每日 pipeline

### 低依赖模式

适合第一次真实写入前试跑。使用模板 idea，跳过精读：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py `
  --once `
  --source mirror-first `
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

权限边界需要分两层看：`research_agenda_ideate.py` 的 Claude refinement 路径会直接使用 `claude --dangerously-skip-permissions`，这是当前 idea 发散工作流的高自治执行模式；运行它之前请确认你理解本机 vault 的读写边界。`daily_arxiv_pipeline.py` 的 Claude 精读 worker 仍是单独 opt-in，如果你确实要让 daily pipeline 也以高自治模式调用 Claude，可以显式传入：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --once --allow-dangerous-claude
```

或者只在当前终端会话中设置：

```powershell
$env:LOCAL_FIRST_VAULT_ALLOW_DANGEROUS_CLAUDE = "1"
```

这个开关只影响 `daily_arxiv_pipeline.py` 的本机运行，不应该写入公开仓库配置。

## 8. Gemini CLI

Gemini 是完整 workflow 的发散 idea 层。我们把它放在 greenhouse 位置，是为了生成高方差、跨论文、机制级的 raw candidates；这类输出更活跃，也更容易产生 hallucination 或 A+B 拼接，所以它不能直接写成结论。基础 smoke test 可以用 template mode 降级运行，但要复现本 vault 的研究 idea 生成链路，应先确认 CLI 可用：

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

如果暂时不用 Gemini，只做降级 smoke test，可以把每日 pipeline 的参数改成：

```powershell
--idea-mode template
```

## 9. OpenCode / DeepSeek adversarial battle

OpenCode / DeepSeek 是 Gemini greenhouse 后的敌对审稿层。源码里由 `.claude/scripts/run_model_debate.py` 调用 `opencode run`，默认模型 selector 是 `deepseek/deepseek-v4-pro(max)`。

它的职责不是继续发散，而是攻击：

- idea 是否只是 A+B 拼接；
- 物理失败场景是否真实；
- interface / optimization / loss placement 是否有新机制；
- 最强 baseline 是否会直接杀死这个 idea；
- lab-fit 是否匹配 Franka、FlexiTac、wrist camera、DLO、本地日志等条件。

从 2026-05-14 起，`gemini-divergent` 的 daily idea stage 要算 clean success，必须有 Gemini-DeepSeek battle 成功。失败时 greenhouse candidates 仍会保留，但 daily idea 状态应是 `partial`。

先确认 OpenCode 可用：

```powershell
opencode --version
```

如果你没有 OpenCode / DeepSeek，完整 daily idea 链路会降级为 `partial`；这不是 KB 或 arXiv mirror 损坏。

## 10. Codex seed review

Codex seed review 是完整 workflow 的二审层。它会读取每日 pipeline 生成的 seed packet、DeepSeek battle 报告和本地 evidence packet，并输出 review 报告。计划任务默认每天 16:30 执行；如果当天 pipeline 还没有完成，包装器会在最近 7 天内 catch up 最新未审 run。没有 Codex 时可以先跳过，但这属于降级路径。

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

## 11. Windows 计划任务

所有注册脚本都支持 `-DryRun`。先 dry run，再注册。默认 dry-run 输出会把当前 Windows 用户名和本机绝对路径替换成占位符；如果你在自己机器上私下排障，可以追加 `-ShowLocalPaths`。

默认节奏：

| 任务 | 默认触发 | 注册脚本 |
| --- | --- | --- |
| `DailyArxivEmbodiedAIScout` | 每天 12:00 | `register_daily_arxiv_task.ps1` |
| `DailyCodexSeedReview` | 每天 16:30 | `register_daily_codex_seed_review_task.ps1` |
| `WeeklyResearchAgendaReview` | 每周日 20:00 | `register_weekly_agenda_review_task.ps1` |

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

手动触发：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_codex_seed_review_task.ps1
```

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

手动触发：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_weekly_agenda_review_task.ps1
```

日志和周报：

```powershell
Get-Content -Encoding UTF8 projects/research-agenda/reviews/weekly-agenda-review-task.log -Tail 100
Get-ChildItem projects/research-agenda/reviews/*weekly*review* | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

## 12. 检查和删除计划任务

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

## 13. macOS/Linux 自动化边界

Python 检索、审计和 arXiv dry-run 可以在 macOS/Linux 上运行，但本仓库只提供 Windows Task Scheduler 注册脚本。非 Windows 用户可以把同等命令放入 `cron`、`systemd timer` 或自己的 CI runner；注意不要把 API key 写入仓库。

smoke-test cron 示例只作结构参考，不会写 Zotero 或 vault：

```cron
0 12 * * * cd /path/to/local-domain-expert-vault && python3 .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 60 --overlap-days 3 && python3 .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 >> projects/arxiv-daily/cron.log 2>&1
```

真实每日任务示例会写入本地 `projects/` 运行产物，并在你配置 Zotero / Claudian / Gemini / OpenCode DeepSeek 后继续执行导入、精读、idea 生成和敌对审稿：

```cron
0 12 * * * cd /path/to/local-domain-expert-vault && python3 .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 60 --overlap-days 3 && python3 .claude/scripts/daily_arxiv_pipeline.py --once --source mirror-first --idea-mode template --skip-read --max-candidates 40 --days-back 14 >> projects/arxiv-daily/cron.log 2>&1
```

## 14. 状态解释

| 状态 | 含义 |
| --- | --- |
| `success` | 本轮 pipeline 关键步骤完成 |
| `partial` | 主流程部分完成，但完整 AI 层缺凭据、CLI 或网络 |
| `missing_ZOTERO_API_KEY` | 缺 Zotero 写入凭据 |
| `skipped_waiting_for_daily_pipeline` | Codex review 等待每日 pipeline 先产生候选 |
| `NO_LOCAL_MATCHES` | 本地 wiki 没有检索命中 |

`partial` 不一定是坏状态。先读日志里的 `ERROR:` 行，再决定是否要配置缺失能力。

## 15. 推荐启用顺序

1. `audit_kb.py`
2. `kb_search.py`
3. `arxiv_metadata_sync.py --dry-run`
4. `arxiv_metadata_sync.py --status`
5. 小规模 `arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1`
6. `daily_arxiv_pipeline.py --dry-run --source mirror-first`
7. Zotero preflight
8. 单篇 `ingest_paper.py`
9. 手动 `daily_arxiv_pipeline.py --once --source mirror-first --idea-mode template`
10. Gemini CLI
11. OpenCode / DeepSeek battle
12. `run_daily_arxiv_task.ps1`
13. `register_daily_arxiv_task.ps1`
14. Codex seed review
15. weekly agenda review

这样做的好处是每一步都有明确验收，不会把 Zotero、Gemini、OpenCode/DeepSeek、Codex、计划任务的问题混在一起。
