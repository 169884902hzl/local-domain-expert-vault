# Local Domain Expert Vault

[![Smoke](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml/badge.svg)](https://github.com/169884902hzl/local-domain-expert-vault/actions/workflows/smoke.yml)
[![Release](https://img.shields.io/github/v/release/169884902hzl/local-domain-expert-vault?label=release)](https://github.com/169884902hzl/local-domain-expert-vault/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#clone-后能直接做什么)

> 把 Obsidian + Zotero 文献库变成一个本地领域专家：基于 `wiki/` 证据回答问题，用 Claudian 精读论文，回跳 Zotero/PDF 原文，生成可审阅 research idea 草案，并通过 mirror-first arXiv 自动化持续补充新论文。

[English README](README_EN.md)

这是一个面向领域研究者的 **Obsidian + Zotero + Claudian research vault**。更准确地说，它是一个 **本地领域专家 vault**：不是把所有问题丢给泛用 AI，而是把一个专业方向的论文、概念、实体、精读报告、本地检索和研究 idea 草案组织成可追踪的判断依据。

这里的“领域专家”不是指仓库里训练了一个新模型，而是指 LLM 的每次精读、比较、发散和实验草案，都被本地 `wiki/` 证据、Zotero 来源、概念网络和人工 review 边界约束。它可以像一个长期读过你文献库的研究同伴一样工作，但所有结论都要能回到本地证据。

公开版本以机器人操控文献为示例，覆盖 DLO、VLM/VLA、RL、Sim-to-Real 和 embodied AI。你可以把它迁移到其他学科，但需要替换论文集合、概念页、实体页、Claudian prompt 和 arXiv 过滤规则。

适合对象：需要长期追踪一个专业方向的研究生、PI / 实验室知识库维护者，以及希望把 LLM 变成“有本地文献记忆的领域专家”的研究者。

当前公开版本：`v0.1.0`。这是首个可发行版本，覆盖本地浏览、知识库审计、`kb_search.py` 检索、Zotero/Obsidian 配置说明、Paper Reading Workbench、arXiv mirror-first 自动化文档和 Windows 计划任务入口。完整 AI 自动化仍需要使用者在本机配置 Zotero、Claudian / Claude Code、Gemini / Codex 和权限边界。

## 它是什么 / 不是什么

这是：

- 一个 **本地领域专家 vault**：长期保留本地文献记忆，而不是一次性 AI 对话。
- 一个 **evidence-grounded workflow**：回答领域问题前先检索 `wiki/topics/`、`wiki/concepts/` 和 `wiki/entities/`，让答案从证据里长出来。
- 一个 Zotero / Obsidian / Claudian 工作流模板：支持导入、精读、finalize、audit、比较和概念页维护。
- 一个 research-agenda seed system：把本地证据整理成可审阅 idea seed、baseline、风险和实验方案草案。
- 一个可脱敏发布的公开包：不包含 API key、PDF、SQLite mirror、Zotero 缓存、日志和个人路径。

这不是：

- 不是 clone 后即可完整运行的全自动科研系统。
- 不是已验证创新点或实验结果生成器。
- 不是 PDF 全文仓库；PDF 仍由 Zotero、WebDAV 或 linked attachment 管理。
- 不是只适用于机器人方向的代码库；机器人只是公开示例领域。

## Clone 后能直接做什么

无需 Zotero、Claudian、Gemini 或 Codex，你可以直接运行：

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

这会验证本地知识库结构，并返回可追溯到 `wiki/` 的论文、概念和实体路径。Obsidian 是可选的，但推荐用它浏览 graph、backlinks、dashboard 和精读笔记。

## 需要额外配置后才能做什么

| 功能 | 需要 |
| --- | --- |
| 从 Zotero 导入论文 metadata | Zotero API key、user ID、collection key，或本机 Zotero Desktop |
| 从 Obsidian 精读笔记回跳 Zotero item / PDF | Zotero Desktop、PDF 附件、Paper Reading Workbench |
| Claudian / Claude Code 精读、比较、问答 | 本机 CLI、模型账号、权限确认 |
| daily arXiv scout 和 idea seed | 本地 arXiv SQLite metadata mirror、网络；完整模式需要 Zotero / Gemini / Codex |
| PDF 同步 | Zotero 官方存储、WebDAV 或 linked attachment；仓库不提交 PDF |

详细配置入口：

- Obsidian / Claudian: [docs/OBSIDIAN_CLAUDIAN_SETUP.md](docs/OBSIDIAN_CLAUDIAN_SETUP.md)
- Zotero API、WebDAV、附件同步: [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md)
- 自动化、计划任务、arXiv mirror-first: [docs/AUTOMATION.md](docs/AUTOMATION.md)
- Paper Reading Workbench 安全边界: [docs/SECURITY_PLUGIN_WORKBENCH.md](docs/SECURITY_PLUGIN_WORKBENCH.md)

## 电脑上怎么每天自动跑

`daily_arxiv_pipeline.py` 是每日 arXiv 工作流的核心引擎，但它不是推荐的 Windows 定时任务入口。电脑上每天自动跑时，建议走这条链路：

```text
Windows Task Scheduler
    -> register_daily_arxiv_task.ps1      注册计划任务
    -> run_daily_arxiv_task.ps1           每日包装器
    -> arxiv_metadata_sync.py             先同步本地 arXiv metadata mirror
    -> daily_arxiv_pipeline.py            再执行 mirror-first pipeline
```

先 dry run，确认时间、路径和任务名：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
```

确认无误后注册真实任务：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -Time "12:00"
Get-ScheduledTask -TaskName DailyArxivEmbodiedAIScout
```

完整的 Codex seed review、weekly agenda review、日志查看和删除任务命令见 [docs/AUTOMATION.md](docs/AUTOMATION.md) 的 `Windows 计划任务` 小节。

## 本地领域专家如何工作

这套 vault 的目标不是替代研究者，而是让 LLM 在一个专业方向里持续积累上下文，并把严谨研究者已经在做的工作固定成可检查流程：

- **长期记忆**：论文、概念、作者、系统和数据集沉淀在 `wiki/`，让系统记住一个方向，而不是每次从空白对话开始。
- **证据约束**：领域回答先跑本地检索；没有本地证据时，明确标出 evidence gap，不把猜测包装成结论。
- **精读归纳**：Zotero 条目可以进入 topic note，再经过 Claudian 精读、finalize 和 audit，形成可复用证据层。
- **知识网络**：论文连接到概念页和实体页，后续问题可以沿论文、方法、作者、数据集和系统追踪。
- **假设生成**：research-agenda 只生成可审阅 idea seed，不把局部证据包装成已验证创新。
- **实验草案**：idea seed 会被展开为 baseline、关键区分实验、no-hardware pilot、失败条件和人工 review 字段，让发散想法继续落到可讨论的研究计划。

## 工作流概览

这个仓库把流程收束成一个闭环：

```text
Zotero / arXiv
    ↓
wiki/topics/        论文笔记：每篇论文一个结构化页面
    ↓
wiki/concepts/      概念页：DLO、VLM、Sim-to-Real、diffusion policy 等
    ↓
wiki/entities/      实体页：作者、实验室、数据集、系统
    ↓
kb_search.py        回答问题前先查本地证据
    ↓
output/ projects/   综述、比较、研究 idea、每日 arXiv 日志
```

核心原则是 **local-first answerability**：任何领域回答都先查本地 `wiki/`，结论必须能回到具体论文、概念页或实体页；本地没有证据时，才明确说明缺口并考虑外部检索。

## 工作流展示

### 1. Local-first answerability

Claudian 在 Obsidian 中回答“有关 RL token 的论文有哪些？怎么做才可能形成创新点？”时，会先基于本地 `wiki/` 列出相关论文和笔记路径，再从精读笔记中抽取技术点、open problems 和面向 DLO 操控的研究空白。

![Claudian local-first RL Token research answer](docs/assets/claudian-rl-token-result.png)

### 2. Deep reading report

精读报告是 `paper -> local evidence -> KB answer -> research idea` 的中间层。它把论文从摘要变成可审计的 evidence metadata、method、experiment、limitation 和 local citation notes。

![Deep reading report example](docs/assets/deep-reading-report-example.png)

完整示例见 [docs/examples/deep-reading-report-example.md](docs/examples/deep-reading-report-example.md)。

### 3. Paper -> concept/entity knowledge network

每篇论文进入 `wiki/topics/` 后，会被连接到 `wiki/concepts/` 和 `wiki/entities/`。这让后续问题可以沿着“论文、概念、作者/数据集/系统”三层结构检索，而不是只在 PDF 摘要里关键词匹配。

### 4. Research idea seed

research-agenda 工作流会把本地证据沉淀成待审阅研究 idea seed。下面示例展示了从本地证据、方法改进主张、baseline、关键区分实验、novelty pressure 到 no-hardware pilot 的结构化研究设想草案；这些研究主张仍需要人工审阅和实验验证。

![Gemini-assisted research idea seed with local evidence and review fields](docs/assets/gemini-research-idea-seed-example.png)

## 其他专业怎么迁移

如果你不是机器人方向，也可以把这个仓库当成一套研究系统模板来用。建议保留 Obsidian + Zotero + Claudian + local retrieval + automation 的整体结构，然后重点替换这些地方：

| 文件或目录 | 需要替换什么 |
| --- | --- |
| `wiki/topics/` | 换成你自己领域的论文笔记 |
| `wiki/concepts/` | 换成你自己领域的核心概念、方法和任务 |
| `wiki/entities/` | 换成你自己领域的作者、实验室、数据集、系统或机构 |
| `.claude/commands/` | 调整导入、精读、检索、比较等命令的领域假设 |
| `.claudian/claudian-settings.json` | 调整 Claudian 的 system prompt、口吻和安全策略 |
| `.claude/scripts/daily_arxiv_pipeline.py` | 调整 arXiv 检索 query、关键词、评分规则和候选过滤 |

## 这个仓库包含什么

| 模块 | 作用 | 直接可用吗 |
| --- | --- | --- |
| `wiki/topics/` | 文献笔记层，每篇论文一个结构化 topic note | 是 |
| `wiki/concepts/` | 概念层，把方法、任务、理论组织成可复用知识 | 是 |
| `wiki/entities/` | 作者、实验室、数据集、系统等实体页 | 是 |
| `kb_search.py` | 本地优先检索入口，回答问题前先跑它 | 是 |
| `audit_kb.py` | 检查 frontmatter、heading、精读质量和概念页结构 | 是 |
| `.claude/commands/` | Claudian / Claude Code 项目命令 | 需要 Claudian 或 Claude Code |
| `.claudian/claudian-settings.json` | 已脱敏的 Claudian 行为配置和 system prompt | 需要用户本机配置 CLI |
| `.obsidian/` | Graph、Smart Connections、Dataview 等插件配置；Paper Reading Workbench 已打包 | 插件本体可直接用；Zotero/PDF 回跳需 Zotero Desktop 和 PDF 附件 |
| `daily_arxiv_pipeline.py` | 每日 arXiv 检索、排序、导入、idea 生成流水线 | 需要网络；完整模式需要 Zotero/CLI |
| `docs/AUTOMATION.md` | 自动化启动、计划任务、日志和排错说明 | 是 |

## 典型使用方式

### 1. 只当文献知识库用

打开 Obsidian，浏览 `wiki/`，用 graph 和反链看机器人操控相关论文、概念和研究者关系。

### 2. 当本地问答资料库用

```powershell
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

先读返回的本地路径，再写回答。这样可以避免“看起来合理但没有本地证据”的总结。

### 3. 当 Zotero -> Obsidian 导入工具用

配置自己的 Zotero 后：

```powershell
python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
python .claude/scripts/audit_kb.py
```

### 4. 当 Claudian 精读工作流用

安装 Claudian 后，在 Obsidian 里调用：

```text
/read-paper ZOTERO_KEY
/search-kb 你的问题
/compare-papers PAPER_A PAPER_B
```

### 5. 当每日 arXiv 自动化系统用

daily arXiv 工作流是 **local metadata mirror first**：先通过 arXiv 官方 OAI-PMH endpoint 增量同步 metadata 到本地 SQLite，再从本地 mirror 排序候选；真实每日任务中，Search API 只作为 mirror 过旧或候选不足时的 fallback / troubleshooting 路径。

先做零写入检查：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

如果 `--status` 显示 `missing=true`，说明本机还没有 SQLite mirror；此时 pipeline dry-run 会快速提示 `arxiv_mirror_missing`，不会静默兜底 Search API。即使本地 mirror 太小导致候选不足，dry-run 也只报告 `arxiv_mirror_insufficient`。要真实预览候选，先运行一次小规模本地同步：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

再按 [docs/AUTOMATION.md](docs/AUTOMATION.md) 配置 Zotero、Gemini/Codex 和 Windows 计划任务。

## 仓库状态

| 项目 | 状态 |
| --- | --- |
| 基础浏览 | 可直接使用 |
| 本地检索 | 可直接使用，Python 标准库即可 |
| 结构审计 | 可直接使用，Python 标准库即可 |
| Obsidian 插件配置 | Paper Reading Workbench 已打包；PDF 回跳需 Zotero Desktop 和附件；其它插件需用户安装 |
| Claudian 配置 | 已包含脱敏配置；CLI 路径和账号需用户本机配置 |
| Zotero 导入 | 需要用户自己的 Zotero 或 Zotero API 配置 |
| 每日 arXiv 自动化 | 需要网络；写入 Zotero 时需要 Zotero 配置 |
| Gemini / Codex 自动化 | 可选；需要用户本机 CLI 已登录 |
| API key | 不包含在仓库中，必须由使用者自己配置 |

## 目录结构

```text
wiki/                         # 结构化知识层
  topics/                     # 文献笔记
  concepts/                   # 概念页
  entities/                   # 研究者、实验室、数据集等实体页
raw/                          # 原始材料区，默认只追加；公开包只保留目录
output/                       # 生成报告和查询产品；默认不提交内容
projects/                     # 活跃研究项目、自动化日志、研究议程；默认不提交内容
attachments/                  # PDF 和图片附件；默认不提交内容
templates/                    # Obsidian 笔记模板
docs/                         # 使用、自动化、安全说明
.claude/commands/             # Claudian / Claude Code 项目命令
.claude/scripts/              # 本地维护、检索、Zotero、arXiv 自动化脚本
.claudian/claudian-settings.json
.obsidian/                    # 最小 Obsidian 配置和插件配置
```

公开仓库默认不包含 PDF、SQLite 数据库、Zotero 缓存、会话日志、API key、个人运行状态。`raw/`、`attachments/`、`output/`、`projects/` 中的本地内容会被 `.gitignore` 忽略。

## 快速开始

如果你是从 GitHub clone 这个仓库，仓库根目录就是可打开的 Obsidian vault。

```powershell
git clone https://github.com/169884902hzl/local-domain-expert-vault.git
cd local-domain-expert-vault
python --version
python .claude/scripts/audit_kb.py
python .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

macOS/Linux 可用同样的 Python 命令：

```bash
git clone https://github.com/169884902hzl/local-domain-expert-vault.git
cd local-domain-expert-vault
python3 --version
python3 .claude/scripts/audit_kb.py
python3 .claude/scripts/kb_search.py "diffusion policy DLO" --limit 5
```

要求：

- Python 3.10+
- PowerShell 5+ 或 PowerShell 7+（Windows 自动化脚本需要）
- Obsidian 可选，但推荐安装

基础审计和检索脚本只依赖 Python 标准库。你不配置 Zotero、不安装 Gemini、不登录 Codex，也能浏览 `wiki/`、运行 `audit_kb.py` 和 `kb_search.py`。

## Obsidian 设置

详细配置见 [docs/OBSIDIAN_CLAUDIAN_SETUP.md](docs/OBSIDIAN_CLAUDIAN_SETUP.md)。

最短步骤：

1. 用 Obsidian 打开仓库根目录。
2. 打开 `Settings -> Community plugins`，安装并启用推荐插件。
3. 重启 Obsidian。
4. 如果启用 Smart Connections，重建索引并确认只索引 `wiki/`。
5. 如果启用 Claudian，检查 `.claudian/claudian-settings.json`，按自己的机器配置 Claude/Codex CLI 路径和账号。

推荐插件：

| 插件 | 用途 | 本仓库是否带配置 |
| --- | --- | --- |
| Claudian | 在 Obsidian 内调用 Claude Code / Codex 类 agent | 是，见 `.claudian/claudian-settings.json` |
| Dataview | Dashboard 和结构化查询 | 是 |
| Smart Connections | 语义检索；建议只索引 `wiki/` | 是 |
| Templater | 笔记模板 | 是 |
| Zotero Desktop Connector | 从 Zotero 取 metadata/fulltext | 部分配置 |
| Paper Reading Workbench | 从 Obsidian 精读页回跳 Zotero item/PDF，并生成阅读工作台 | 已打包并默认启用；PDF 回跳依赖 Zotero Desktop 和附件 |

注意：公开包只默认启用已随仓库提供 `main.js` / `styles.css` 的 `paper-reading-workbench`。Claudian、Dataview、Smart Connections、Templater、Zotero Desktop Connector 等社区插件仍需要从 Obsidian Community Plugins 安装后手动启用。

Paper Reading Workbench 的用途是给人类对照阅读：打开带 `zotero_key` 的 `wiki/topics/*.md` 精读笔记后，运行命令 `Paper Reading Workbench: Open paper reading workbench for current note`，插件会读取 Zotero key、查询本机 Zotero Connector API、生成 `projects/reading-workbench/<ZOTERO_KEY>-zotero-source.md`，并提供 `Open Zotero item`、`Open Zotero PDF attachment` 和 arXiv PDF fallback 链接。Zotero Desktop 必须打开，且该条目需要已有 stored PDF 或 linked PDF 附件；插件不会把 PDF 复制进 vault。这个插件是随仓库打包的本地可执行插件；只有在你点击翻译、知识图等工作台动作时，才会调用本机 Python 脚本生成本地工作文件。

插件读取范围、写入目录、Python helper 调用边界和禁用方法见 [docs/SECURITY_PLUGIN_WORKBENCH.md](docs/SECURITY_PLUGIN_WORKBENCH.md)。

## 核心命令

### 本地检索

```powershell
python .claude/scripts/kb_search.py "VLM robot manipulation" --limit 12
python .claude/scripts/kb_search.py "DLO diffusion policy" --type literature --limit 10
python .claude/scripts/kb_search.py "Sim-to-Real" --must-tag sim-to-real --limit 8
```

领域问答建议先运行本地检索，再基于返回的 `wiki/topics/`、`wiki/concepts/`、`wiki/entities/` 回答。

### 结构审计

```powershell
python .claude/scripts/audit_kb.py
python .claude/scripts/audit_kb.py --strict-reading
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
```

基础审计检查 frontmatter、必需 heading、概念/实体结构。严格模式会进一步检查精读质量和概念页是否只是论文列表。

### 维护链接和本地引用

```powershell
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py --strict-reading
```

这些命令会维护 wikilink、概念反链、本地引用关系，并再次审计结果。

### 比较论文

```powershell
python .claude/scripts/compare_papers.py li2025routing peters2026coordinated
```

参数可以是 topic 文件名 stem、Zotero key 或路径。

## 配置 Zotero

Zotero 是可选增强能力。没有 Zotero 时仍可浏览、检索和手工维护笔记。

### 1. 复制配置示例

```powershell
Copy-Item .claude/scripts/config.example.json .claude/scripts/config.json
notepad .claude/scripts/config.json
```

`config.json` 不会被 Git 提交。示例内容：

```json
{
  "collection_key": "",
  "limit": 500
}
```

把 `collection_key` 改成你自己的 Zotero collection key。如果你不需要固定 collection，也可以通过环境变量或命令参数传入。

公开脚本不会内置任何预设私有 collection key。缺少 collection 配置时，Zotero 导入会明确返回 `missing_collection_key`，而不是默认写入某个私有 collection。

### 2. 选择 Zotero 连接方式

| 场景 | 需要什么 | 说明 |
| --- | --- | --- |
| 本机 Zotero 已打开 | Zotero Desktop + Zotero Connector API | 默认访问 `http://localhost:23119` |
| 无本机 Zotero，但要读写 Web API | `ZOTERO_API_KEY` + `ZOTERO_USER_ID` 或 `ZOTERO_LIBRARY_ID` | 适合服务器或自动化 |
| 只浏览本地 wiki | 不需要 Zotero | 可跳过本节 |

如果选择 Web API 路线，先创建自己的 Zotero API key：

1. 登录 Zotero 官网，打开 [Zotero API Keys](https://www.zotero.org/settings/keys)。
2. 选择 `Create new private key`。
3. 如果只需要读取自己的库，给 `Read` 权限即可。
4. 如果要让自动化创建 Zotero 条目、写入 collection 或修复附件记录，需要给 `Write` 权限。
5. 页面上的数字 user id 不是用户名或邮箱，后面要写入 `ZOTERO_USER_ID`。
6. 不要把生成的 key 放进 README、issue、commit、截图、`config.json` 或任何公开日志。

PowerShell 示例：

```powershell
setx ZOTERO_USER_ID "<your-zotero-user-id>"
setx ZOTERO_API_KEY "<your-zotero-api-key>"
setx ZOTERO_COLLECTION_KEY "<your-collection-key>"
```

`setx` 写入的是后续新终端环境；设置后重新打开 PowerShell 再运行脚本。不要把真实 key 写进 README、issue、commit、截图或 `config.json`。

如果还不知道 collection key，可以在重新打开 PowerShell 后列出自己的 Zotero collections：

```powershell
$headers = @{
  "Zotero-API-Key" = $env:ZOTERO_API_KEY
  "Zotero-API-Version" = "3"
}
Invoke-RestMethod "https://api.zotero.org/users/$env:ZOTERO_USER_ID/collections?format=json&limit=100" -Headers $headers |
  ForEach-Object { "{0}`t{1}" -f $_.data.key, $_.data.name }
```

把目标 collection 左侧的 key 写入 `ZOTERO_COLLECTION_KEY`。本公开脚本当前默认面向个人 user library；group library 需要按自己的 Zotero group 路径改脚本或包装命令。

### 3. 预检 Zotero

```powershell
python .claude/scripts/zotero_import.py --preflight --json
```

`--json` 默认会脱敏本机 Zotero collection 和 library 信息；私下排障才使用 `--unsafe-json`。

常见结果：

- `PASS Zotero local read`：本机 Zotero connector 可读。
- `PASS Zotero write credentials`：Web API 写入凭据可用。
- `missing_collection_key`：还没有配置自己的 Zotero collection key。
- `FAIL missing ZOTERO_API_KEY`：不能写入 Zotero Web API，但本地浏览和本地检索仍可用。

### 4. 导入单篇论文

```powershell
python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
python .claude/scripts/audit_kb.py
```

`ZOTERO_KEY` 是 Zotero item key。导入完成后会在 `wiki/topics/` 生成或更新文献笔记，并补齐本地知识网络字段。

### 5. Zotero 附件和存储扩展

Zotero 附件同步有多种路线：Zotero 官方存储、WebDAV、linked attachment、本地附件目录迁移，或配合 Better BibTeX / ZotFile / Attanger 等插件。这个公开仓库不内置任何个人存储账号、服务器地址或附件目录。

本 vault 当前采用的是 **CSTCloud 数据胶囊 WebDAV + Zotero 应用专用账号** 路线。服务入口是 `https://data.cstcloud.cn/`，Zotero WebDAV 使用的非敏感 endpoint 是 `https://data.cstcloud.cn/dav`。公开资料和当前配置说明显示，实名认证后通常可获得约 20GB 空间，并支持 WebDAV / S3；实际额度以账号页面为准。可复现配置说明见 [docs/ZOTERO_STORAGE.md](docs/ZOTERO_STORAGE.md)。

![CSTCloud 数据胶囊 WebDAV client settings for Zotero](docs/assets/cstcloud-webdav-zotero.png)

上图展示的是裁剪后的数据胶囊 WebDAV 客户端访问管理页，只保留 WebDAV endpoint 和 Zotero 应用条目，凭据和个人账号区域不随仓库发布。

Zotero Desktop 里对应的文件同步设置如下，展示 WebDAV 同步方式和服务器地址。

<img src="docs/assets/zotero-desktop-webdav-settings.png" alt="Zotero Desktop WebDAV file sync settings" width="720">

## Claudian / Claude Code 工作流

如果你安装了 Claudian 或使用 Claude Code，可以直接调用项目命令：

| 命令 | 用途 |
| --- | --- |
| `/search-kb 问题` | 先查本地 wiki，再回答领域问题 |
| `/ingest-paper ZOTERO_KEY` | 从 Zotero 导入单篇论文 |
| `/read-paper ZOTERO_KEY` | 获取全文、写精读分析、finalize、审计 |
| `/compare-papers A B` | 基于本地结构化字段比较两篇论文 |
| `/update-concepts` | 把概念页从 stub 升级为证据驱动页面 |
| `/maintain-kb` | 执行链接、概念、引用和严格审计维护 |

项目规则写在 `AGENTS.md` 和 `CLAUDE.md`。最重要的规则是：回答领域问题前先查本地；不要把摘要当精读；不要编造 Zotero key、实验数字或论文关系。

Claudian 的公开配置已经放在：

```text
.claudian/claudian-settings.json
.obsidian/plugins/claudian/manifest.json
.obsidian/plugins/claudian/data.json
```

其中 `.claudian/claudian-settings.json` 包含本 vault 的核心 system prompt：本地证据优先、Zotero 导入走脚本、精读必须 finalize、批量处理要写进度、`raw/` 默认只追加。公开包已经清空个人用户名、CLI 绝对路径、环境变量和 host-specific 配置。你需要在自己的 Claudian 设置里重新选择 provider、登录账号并确认权限模式。

公开脚本默认不绕过 Claude 权限。高自治模式需要你在本机显式传入 `--allow-dangerous-claude`，或临时设置 `LOCAL_FIRST_VAULT_ALLOW_DANGEROUS_CLAUDE=1`；不要把这个开关写进公开配置。

## 自动化流程

详细说明见 [docs/AUTOMATION.md](docs/AUTOMATION.md)。下面是最常用的启动路径。

### 1. 零写入检查 arXiv 入口

```powershell
python .claude/scripts/arxiv_metadata_sync.py --dry-run --days-back 14 --max-pages 1
python .claude/scripts/arxiv_metadata_sync.py --status
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

这组命令适合第一次零写入检查。metadata sync 的 dry-run 使用内存数据库；`--status` 只读检查本机 mirror，不会创建 SQLite；pipeline dry-run 会读取已有 SQLite metadata mirror。如果 mirror 不存在、为空或候选不足，它会提示 `arxiv_mirror_missing` / `arxiv_mirror_empty` / `arxiv_mirror_insufficient`，不会把 Search API fallback 伪装成 mirror-first 成功。要看到真实候选，需要先运行一次非 dry-run metadata sync。

arXiv 数据层边界：

- OAI-PMH sync 写入 `projects/arxiv-daily/metadata/arxiv_metadata.sqlite`。
- SQLite mirror 只保存 metadata：title、authors、abstract、dates、categories、URL、PDF URL、DOI、journal reference、comments。
- 默认同步 OAI-PMH sets 是 `cs` 和 `stat`，不是全 arXiv，也不是 PDF 全文。
- 公开仓库不提交 SQLite mirror；使用者可以通过 `python .claude/scripts/arxiv_metadata_sync.py --status` 查看自己本机 mirror 的规模和更新时间。
- Zotero 后续用选中的 metadata / PDF URL 创建 library item；PDF 同步由 Zotero 官方存储、WebDAV 或 linked attachment 负责，不由 arXiv mirror 保存。

小规模建立本机 mirror 后再预览候选：

```powershell
python .claude/scripts/arxiv_metadata_sync.py --incremental --days-back 14 --max-pages 1
python .claude/scripts/daily_arxiv_pipeline.py --dry-run --source mirror-first --max-candidates 30 --days-back 14 --idea-mode template --skip-read
```

### 2. 手动运行一次每日 pipeline

如果你还没有 Gemini CLI 或 Claudian，可以先用模板 idea，并跳过精读：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py --once --source mirror-first --idea-mode template --skip-read --max-candidates 40 --days-back 14
```

如果你已经配置 Zotero、Claudian 和 Gemini CLI，可以使用更完整的模式：

```powershell
python .claude/scripts/daily_arxiv_pipeline.py `
  --once `
  --source mirror-first `
  --idea-mode gemini-divergent `
  --idea-timeout 1200 `
  --gemini-model gemini-3.1-pro-preview `
  --read-timeout 2700
```

输出通常写入：

- `projects/arxiv-daily/`
- `projects/research-agenda/`
- `raw/readings/`
- `wiki/topics/`

这些运行产物默认被 `.gitignore` 忽略。

### 3. 手动运行每日包装器

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/run_daily_arxiv_task.ps1
```

包装器会：

1. 通过 OAI-PMH 增量同步 arXiv `cs/stat` metadata mirror。
2. 运行 `daily_arxiv_pipeline.py --once --source mirror-first`。
3. 使用 Gemini divergent idea 生成。
4. 写入每日日志。
5. 运行自动化质量审计。

注意：包装器默认会调用 Gemini CLI，并尝试 Zotero/Claudian 路径。没有相关配置时，运行结果可能是 `partial`，这不等于基础 vault 坏了。

### 4. 注册 Windows 计划任务

先 dry run，确认路径和时间：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun -Time "12:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -DryRun -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DryRun -DayOfWeek Sunday -Time "20:00"
```

确认无误后注册：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -Time "12:00"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_codex_seed_review_task.ps1 -Time "16:30"
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_weekly_agenda_review_task.ps1 -DayOfWeek Sunday -Time "20:00"
```

检查任务：

```powershell
Get-ScheduledTask -TaskName DailyArxivEmbodiedAIScout
Get-ScheduledTask -TaskName DailyCodexSeedReview
Get-ScheduledTask -TaskName WeeklyResearchAgendaReview
python .claude/scripts/audit_scheduled_tasks.py
```

删除任务：

```powershell
Unregister-ScheduledTask -TaskName DailyArxivEmbodiedAIScout -Confirm:$false
Unregister-ScheduledTask -TaskName DailyCodexSeedReview -Confirm:$false
Unregister-ScheduledTask -TaskName WeeklyResearchAgendaReview -Confirm:$false
```

## 可选 CLI 集成

| 工具 | 用途 | 是否必需 |
| --- | --- | --- |
| Zotero Desktop | 本机读取 item metadata 和 fulltext | 可选 |
| Zotero Web API | 写入 Zotero 或无桌面端时同步 | 可选 |
| Claudian / Claude Code | 精读论文、执行项目命令 | 可选 |
| Gemini CLI | 发散研究 idea、图谱/翻译等增强流程 | 可选 |
| Codex CLI | 对每日 seed 做二次审查 | 可选 |
| OpenCode/DeepSeek CLI | 模型辩论和 idea refinement 的增强项 | 可选 |

建议先跑通基础本地检索，再逐个启用 Zotero、Claudian、Gemini、Codex。不要一开始就把所有自动化打开。

## 常见问题

### `NO_LOCAL_MATCHES`

本地 `wiki/` 没有足够匹配。先换关键词，或确认对应论文是否已经导入。

### `Cannot connect to Zotero on localhost:23119`

打开 Zotero Desktop，并确认 Zotero Connector API 可用。也可以改用 Web API，设置 `ZOTERO_API_KEY` 和 `ZOTERO_USER_ID`。

### `missing ZOTERO_API_KEY`

这表示脚本不能写入 Zotero Web API。基础浏览、本地检索、结构审计仍可用。需要自动导入或写回 Zotero 时再配置 key。

### Smart Connections 显示了 `raw/` 或 `.claude/` 内容

重启 Obsidian，并在 Smart Connections 中重建索引。当前配置已经排除非 `wiki/` 路径，但旧索引不会自动消失。

### 计划任务没有执行

先跑 dry run：

```powershell
powershell -ExecutionPolicy Bypass -File .claude/scripts/register_daily_arxiv_task.ps1 -DryRun
```

再检查日志：

```powershell
Get-Content -Encoding UTF8 projects/arxiv-daily/scheduled-task.log -Tail 80
Get-Content -Encoding UTF8 projects/research-agenda/reviews/daily-codex-seed-review-task.log -Tail 80
```

### 自动化返回 `partial`

`partial` 通常表示某个增强步骤缺少凭据、CLI 或网络，而不是整个 vault 不可用。查看运行日志中的 `ERROR:` 行，先区分是 Zotero、Gemini、Codex、arXiv 网络还是精读步骤失败。

## 安全和发布边界

请阅读 [docs/SECURITY_AND_PRIVACY.md](docs/SECURITY_AND_PRIVACY.md)。核心规则：

- 不提交 API key、token、cookie、credential。
- 不提交 `.claude/backups/`、`.claudian/sessions/`、`.obsidian/workspace.json`。
- 不提交 PDF、SQLite、Zotero 缓存和本地自动化产物。
- 不把真实 key 粘到 issue、README、截图或日志里。

## License

This repository is released under the [MIT License](LICENSE). Third-party papers, figures, datasets, product names, and external tools remain governed by their own authors, publishers, and licenses.

公开包已经带有 `.gitignore`，但上传前仍建议运行：

```powershell
rg -n --hidden --glob '!.git/**' "(OPENAI_API_KEY|ANTHROPIC_AUTH_TOKEN|ZOTERO_API_KEY|GEMINI_API_KEY|sk-[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z_]{20,})" .
```

命中环境变量名说明可以保留；命中真实 key 值必须移除并轮换。

## 重新生成公开包（可选）

如果你是从 GitHub clone 的使用者，不需要 `exports/`。仓库根目录就是 vault。

只有从完整本地工作目录重新生成公开包时，才需要运行：

```powershell
powershell -ExecutionPolicy Bypass -File tools/build_github_package.ps1 -PackageName github-ready-vault-YYYYMMDD-public -Force
```

然后只上传 `exports/github-ready-vault-YYYYMMDD-public/`，不要直接上传完整本地工作目录。
