# Getting Started

## 目标

让新用户可以把这个 vault 当作机器人操控文献工作台使用：

- 用 Obsidian 浏览 `wiki/` 知识网络。
- 用本地检索脚本回答领域问题。
- 用模板新增文献、概念和项目笔记。
- 在完整配置完成后接入 Zotero、Claudian、Gemini、OpenCode/DeepSeek 与 Codex 自动流程。

如果你不确定自己应该配置到哪一层，先看 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)。它把浏览、检索、Zotero/PDF、arXiv mirror、计划任务、Claudian/Gemini/OpenCode DeepSeek/Codex 分成可验证层级。

## 最小可用路径

```powershell
git clone https://github.com/169884902hzl/local-domain-expert-vault.git
cd local-domain-expert-vault
python --version
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "VLM robot manipulation" --limit 5
```

需要 Python 3.10+。核心审计和检索脚本只依赖 Python 标准库；Zotero、Claudian、Gemini、OpenCode/DeepSeek、Codex 不影响最小检索路径，但它们是完整本地领域专家工作流需要逐步配置的核心层。
如果 `audit_kb.py` 和 `kb_search.py` 能运行，说明本地知识层和检索入口可用。

## Obsidian 设置

完整 Obsidian / Claudian 配置说明见 [OBSIDIAN_CLAUDIAN_SETUP.md](OBSIDIAN_CLAUDIAN_SETUP.md)。

推荐插件：

- Claudian
- Dataview
- Smart Connections
- Templater
- Zotero Desktop Connector

Smart Connections 建议只索引 `wiki/`。当前配置已经排除 `.claude/`、`.obsidian/`、`raw/`、`output/`、`archive/`、`attachments/`、`projects/` 等非正式知识源。
首次打开后如果启用 Smart Connections，建议重建一次索引，确保只索引 `wiki/`。

Claudian 的公开配置在 `.claudian/claudian-settings.json`，已经清空个人路径和环境变量；使用者需要在自己的机器上重新配置 Claude/Codex CLI 和账号。

## Zotero 设置

Zotero 不是浏览和 `kb_search.py` 的前置条件；但它是完整论文导入、PDF 对照阅读、附件同步和自动化写回的核心层。没有 Zotero 时仍可浏览、检索和手工维护笔记。

启用 Zotero 自动导入时：

1. 复制 `.claude/scripts/config.example.json` 为 `.claude/scripts/config.json`。
2. 填入自己的 `collection_key`。
3. 如果要写入 Zotero Web API，在本机环境变量里设置 `ZOTERO_API_KEY` 和 `ZOTERO_USER_ID`。
4. 不要提交 `.claude/scripts/config.json`。

## 自动化设置

每日 arXiv scout、Gemini idea 生成、OpenCode/DeepSeek battle、Codex seed review 和 Windows 计划任务的完整说明见 [AUTOMATION.md](AUTOMATION.md)。

daily arXiv 主路线是 local SQLite metadata mirror first：先用 arXiv OAI-PMH 同步 metadata，再用 `mirror-first` 从本地库排序候选。公开仓库不自带 SQLite mirror，也不保存 PDF 全文；Search API 只作为 fallback / troubleshooting。

完整本机节奏默认是：

| 时间 | 任务 | 作用 |
| --- | --- | --- |
| 每天 12:00 | `DailyArxivEmbodiedAIScout` | 同步 arXiv mirror，跑每日候选、Zotero/Claudian/Gemini/OpenCode-DeepSeek 和质量审计。 |
| 每天 16:30 | `DailyCodexSeedReview` | 对当天 seed packet、DeepSeek battle 和本地 evidence 做 Codex 二审。 |
| 每周日 20:00 | `WeeklyResearchAgendaReview` | 汇总一周 agenda、审计和 top-tier idea pressure test，生成周报。 |

第一次启用自动化时建议按这个顺序：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
python .claude/scripts/zotero_import.py --preflight --json
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -DryRun -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun -DayOfWeek Sunday -Time "20:00"
```

`--status` 在 fresh clone 中可能显示 `missing=true`，这是正常的；`--incremental --max-pages 1` 会建立一个小规模本地 SQLite mirror，文件位于 `projects/arxiv-daily/metadata/` 且默认不提交 Git。确认 dry run、Zotero preflight 和计划任务路径都正确后，再注册真实任务。

## 日常维护

```powershell
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py --strict-reading
```

这些命令用于维护 wikilink、概念反链、本地引用关系和精读质量。
