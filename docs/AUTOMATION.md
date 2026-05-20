# Automation Guide

本页说明如何启动、配置和排查这个 vault 的自动化流程。所有 API key 都必须由使用者在自己的机器上配置；仓库不会包含任何真实 key。

## 自动化分层

| 层级 | 能力 | 必需条件 | 适合谁 |
| --- | --- | --- | --- |
| Level 0 | 本地检索和审计 | Python 3.10+ | 所有人 |
| Level 1 | arXiv metadata mirror smoke test | Python + 网络 | 想确认 OAI-PMH metadata 同步入口可用 |
| Level 2 | mirror-first daily pipeline dry-run | Python + metadata mirror | 想看每日候选但不写库 |
| Level 3 | optional Search API fallback troubleshooting | Python + 网络 | 只在 mirror 缺失、过旧或候选不足时排错 |
| Level 4 | Zotero + Claudian + Gemini + DeepSeek + Codex full workflow | Zotero / Claudian / Gemini / OpenCode DeepSeek / Codex 逐步配置 | 想复现完整导入、精读、raw candidate 生成和 v0.2 pre-publish gates |
| Level 5 | Windows 定时运行 | Windows Task Scheduler | 想每天自动跑 |

建议按层级逐步启用。不要第一次使用就直接注册计划任务。

## 默认定时节奏

完整本地领域专家工作流默认拆成三个计划任务，而不是把所有事情塞进一个脚本：

| 默认时间 | 任务名 | 入口脚本 | 输出位置 | 边界 |
| --- | --- | --- | --- | --- |
| 每天 12:00 | `DailyArxivEmbodiedAIScout` | `.claude/scripts/run_daily_arxiv_task.ps1` | `projects/arxiv-daily/scheduled-task.log` | 负责 arXiv mirror sync、daily pipeline、Gemini raw candidates、novelty/baseline scan、survival decision、默认 `seed-candidates-only` publish gate 和质量审计；默认 provider-free。DeepSeek/Codex provider-backed gates 只有显式 provider 参数后才完成；否则会 fail-closed / `partial`，不写 formal seed。 |
| 每天 16:30 | `DailyCodexSeedReview` | `.claude/scripts/run_daily_codex_seed_review_task.ps1` | `projects/research-agenda/reviews/daily-codex-seed-review-task.log` 和 `YYYY-MM-DD-codex-seed-review.md` | 对当天或最近 7 天未审 seed packet 做 Codex execution review；不删除、不晋升、不声明 novelty，也不自动发布 formal seed。 |
| 每周日 20:00 | `WeeklyResearchAgendaReview` | `.claude/scripts/run_weekly_agenda_review_task.ps1` | `projects/research-agenda/reviews/weekly-agenda-review-task.log`、`YYYY-MM-DD-weekly-agenda-review.md`、`YYYY-MM-DD-weekly-top-tier-review.md` | 汇总一周 agenda 状态、审计结果和 top-tier pressure test；不会自动移动 idea 文件夹。 |

推荐启用顺序：先完成 Level 0-4 的手动验证，再注册 12:00 每日任务；确认每天有 seed packet 后，再启用 16:30 Codex execution review；最后启用周日 20:00 周审。

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
  --deepseek-provider opencode `
  --codex-execution-provider codex-cli `
  --v2-publish-policy seed-candidates-only `
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
- `projects/research-agenda/seed-candidates/...`，默认 `seed-candidates-only` rollout 下的 accepted-but-not-formal 候选
- `projects/research-agenda/parked/...` 或 `projects/research-agenda/rescue/...`，用于 blocked、non-accepted 或需要 rescue mutation 的候选
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

### v0.2.0/v0.2.1 research-seed 状态机和 publish policy

v0.2.0 的 daily automation 不再把 Gemini/local score 的输出直接当成正式 idea seed。它把每轮候选放进一个 transactional research-seed state machine：

```text
Zotero/arXiv
-> paper intake triage
-> Claudian deep reading
-> paper primitives
-> research claim graph
-> tension map
-> Gemini raw candidates
-> portfolio selection
-> DeepSeek scientific review
-> novelty/baseline scan
-> Codex execution review
-> survival_decision.py
-> publish_research_run.py
```

v2 相关 CLI flags：

| Flag | 取值 | 用途 |
| --- | --- | --- |
| `--deepseek-provider` | `json`, `opencode`, `none` | DeepSeek scientific review 的 provider；正式 v2 gate 需要 provider-backed review。 |
| `--deepseek-provider-json PATH` | path | 读取已有 `deepseek_review.v1` JSON，适合复现或 CI fixture。 |
| `--codex-execution-provider` | `json`, `codex-cli`, `none` | Codex execution review 的 provider；正式 v2 gate 需要 provider-backed review。 |
| `--codex-execution-provider-json PATH` | path | 读取已有 `codex_execution_review.v1` JSON，适合复现或 CI fixture。 |
| `--v2-publish-policy` | `disabled`, `seed-candidates-only`, `formal` | v2 rollout publish policy；默认是 `seed-candidates-only`。 |
| `--allow-formal-seed-publish` | flag | formal seed publish 的第二道显式确认。仅设置 `--v2-publish-policy formal` 不够。 |
| `--target-deep-read` | integer | v2 daily deep-read target；默认 3。 |
| `--max-deep-read` | integer | v2 daily deep-read hard cap；默认 4。 |
| `--legacy-import-fill` | flag | 手动恢复旧的 import fill 行为。默认关闭，所以 `min_new_imports=10` 不会强制 v2 import/read 10 篇。 |
| `--allow-test-provider-for-formal` | flag | 仅限手动测试。允许 formal mode 使用 JSON provider fixture，并记录 test-provider risk；scheduled wrappers 不得设置。 |

Scheduled daily wrapper 另有 PowerShell 参数：

| Wrapper 参数 | 取值 | 用途 |
| --- | --- | --- |
| `-DeepSeekProvider` | `none`, `opencode` | 默认为 `none`。只有显式设为 `opencode` 时，wrapper 才向 pipeline 传 `--deepseek-provider opencode`。 |
| `-CodexExecutionProvider` | `none`, `codex-cli` | 默认为 `none`。只有显式设为 `codex-cli` 时，wrapper 才向 pipeline 传 `--codex-execution-provider codex-cli`。 |

默认 scheduled wrapper 不传 provider 参数，因此 provider-backed DeepSeek/Codex gates 不会被误报为完成。没有 provider 参数时，v2 fail-closed / `partial` 是预期安全行为，不是 silent success。

默认 publish policy 是 `seed-candidates-only`：通过 pre-publish gates 的候选写入 `projects/research-agenda/seed-candidates/`，不会写入 `projects/research-agenda/idea_bank/seed/`。formal seed publish 默认关闭，必须同时满足：

- `--v2-publish-policy formal`
- `--allow-formal-seed-publish`
- novelty verification scope 不是 `local_only`，v0.2.1 最低接受 `local_plus_arxiv_api`
- DeepSeek provider mode 是 `opencode`，Codex execution provider mode 是 `codex-cli`，除非显式手动设置 `--allow-test-provider-for-formal`
- DeepSeek scientific review、novelty/baseline scan、Codex execution review、survival decision、artifact hash 等 hard gates 全部通过

v0.2.1 里，`paper_intake_triage.py` 会输出 `selected_for_deep_read`，daily pipeline 用这些 stable `arxiv_id` 同时控制 Zotero import attempts 和 Claudian deep-read attempts。默认 target 是 3 篇，hard cap 是 4 篇；除非显式启用 `--legacy-import-fill`，旧的 `min_new_imports=10` 不再把 v2 import/read 数量拉回 10。

Formal novelty verification 不能只依赖 local claim graph 或 local arXiv mirror。`novelty_scan.v1` 会记录 `verification_scope`、`external_providers_used` 和 `formal_promotion_allowed`。v0.2.1 的最低外部 scope 是 `local_plus_arxiv_api`；如果只用了 arXiv API，会记录 `formal_publish_risk=external_scope_arxiv_only_not_full_prior_art`。这只是最低 external arXiv probe，不是完整 prior-art verification。无人值守 scheduled formal publish 仍应要求更广的 prior-art artifact，例如 Semantic Scholar、OpenAlex 或人工 prior-art review。

Formal provider provenance 也更严格：`provider=json` 可以继续用于 seed-candidates-only fixture 和 CI，但 formal mode 默认拒绝它。只有手动传入 `--allow-test-provider-for-formal` 才能继续测试 formal path，并且 manifest / publish result / audit 会记录 `test_provider_used_for_formal=true` 和 `formal_publish_risk=test_provider_not_production_provenance`。

backfill 运行的默认操作策略应是 `ingest-only`：只补齐 intake / reading / metadata，不生成 formal seed。做 backfill 时请显式传入：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py `
  --once `
  --source mirror-first `
  --backfill-mode ingest-only `
  --v2-publish-policy seed-candidates-only
```

backfill 不能 formal-publish；即使高级 backfill 允许生成 raw candidates，也只能走 `disabled` 或 `seed-candidates-only` rehearsal。

Provider-backed 要求：

- DeepSeek / opencode 必须产出 `deepseek_review.v1`，并且 `provider_backed=true`。
- Codex CLI 必须产出 `codex_execution_review.v1`，并且 `provider_backed=true`。
- deterministic fallback、字段存在、模板输出或本地规则结果都不能算 provider-backed success。

Publish outcomes：

- `projects/research-agenda/idea_bank/seed/` 只能由 `publish_research_run.py` 写入。
- `projects/research-agenda/seed-candidates/` 保存 accepted-but-not-formal rollout 候选。
- `projects/research-agenda/parked/` 和 `projects/research-agenda/rescue/` 保存 blocked、non-accepted 或需要 rescue mutation 的候选。
- `research_agenda_ideate.py` 只生成 raw candidates；`research_agenda_update.py` 不写 formal seeds。

Audit invariants：

- 不允许非 `publish_research_run.py` 的脚本创建、移动或修改 formal seed folder。
- seed folder 必须有 DeepSeek review、novelty scan、Codex execution review、survival decision 和 artifact hashes。
- formal publish 必须显式设置 formal policy 和 confirmation flag。
- formal publish 必须通过外部/混合 novelty verification，不能用 local-only `likely_open` 晋升 formal seed。
- scheduled wrapper 不得包含 `--v2-publish-policy formal`、`--allow-formal-seed-publish` 或 `--allow-test-provider-for-formal`。
- `quality_tier`、`sharpness_score`、`evidence_execution_score` 和 `ordinaryness_penalty` 是 potential / display 字段，不是 promotion gates。
- 没有 seed 是正常结果；未经审查就写 formal seed 是失败。

## 8. Gemini CLI

Gemini 是完整 workflow 的 raw candidate generator。我们使用它生成高方差、跨论文、机制级的 raw candidates；这类输出更活跃，也更容易产生 hallucination 或 A+B 拼接，所以它不能直接写成 formal seed。基础 smoke test 可以用 template mode 降级运行，但要复现本 vault 的研究 idea 生成链路，应先确认 CLI 可用：

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

## 9. OpenCode / DeepSeek scientific review gate

OpenCode / DeepSeek 是 Gemini raw candidates 后的 provider-backed scientific review gate。源码里由 `.claude/scripts/run_model_debate.py` 调用 `opencode run`，默认模型 selector 是 `deepseek/deepseek-v4-pro(max)`。

它的职责不是继续发散，而是攻击：

- idea 是否只是 A+B 拼接；
- 物理失败场景是否真实；
- interface / optimization / loss placement 是否有新机制；
- 最强 baseline 是否会直接杀死这个 idea；
- lab-fit 是否匹配 Franka、FlexiTac、wrist camera、DLO、本地日志等条件。

在 v0.2.0 里，DeepSeek / opencode 需要产出 `deepseek_review.v1` 且 `provider_backed=true`，才算通过 scientific review gate。失败时 raw candidates 仍会保留，但不能晋升为 accepted seed candidate，更不能写入 formal seed。

先确认 OpenCode 可用：

```powershell
opencode --version
```

如果你没有 OpenCode / DeepSeek，完整 daily idea 链路会降级为 `partial`；这不是 KB 或 arXiv mirror 损坏。

## 10. Codex execution review

Codex execution review 是完整 workflow 的 pre-publish execution gate。它会读取每日 pipeline 生成的 seed packet、DeepSeek scientific review 和本地 evidence packet，并输出 review 报告。计划任务默认每天 16:30 执行；如果当天 pipeline 还没有完成，包装器会在最近 7 天内 catch up 最新未审 run。没有 Codex 时可以先跳过，但这属于降级路径，不能视为 provider-backed success。

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

注意：当前包装器默认不绕过 Codex sandbox/approval。只有在你完全理解本机 CLI 权限边界时，才手动追加 `-DangerouslyBypassSandbox`。v0.2.0 的 formal publish gate 需要 `codex_execution_review.v1` 且 `provider_backed=true`；只有字段存在或 deterministic fallback 不足以 accept。

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

默认手动触发也是 provider-free，只会进入 v2 state machine，不会把 DeepSeek/Codex provider-backed gates 当成已完成。要做显式 provider-backed rehearsal：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_arxiv_task.ps1 -DeepSeekProvider opencode -CodexExecutionProvider codex-cli
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

真实每日任务示例会写入本地 `projects/` 运行产物，并继续执行导入、精读、raw candidate 生成和 v0.2 pre-publish gates。默认仍是 provider-free `seed-candidates-only`，不会发布 formal seed；没有 explicit provider flags 时会 fail-closed / `partial`：

```cron
0 12 * * * cd /path/to/local-domain-expert-vault && python3 .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 60 --overlap-days 3 && python3 .claude/scripts/daily_arxiv_pipeline.py --once --source mirror-first --idea-mode template --skip-read --max-candidates 40 --days-back 14 --v2-publish-policy seed-candidates-only >> projects/arxiv-daily/cron.log 2>&1
```

如果要手动 provider-backed rehearsal，pipeline 需要显式追加：

```bash
--deepseek-provider opencode --codex-execution-provider codex-cli
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
11. OpenCode / DeepSeek scientific review gate
12. `run_daily_arxiv_task.ps1`
13. `register_daily_arxiv_task.ps1`
14. Codex execution review
15. weekly agenda review

这样做的好处是每一步都有明确验收，不会把 Zotero、Gemini、OpenCode/DeepSeek、Codex、计划任务的问题混在一起。
