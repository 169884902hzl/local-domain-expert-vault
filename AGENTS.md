# Vault Operating Manual

你正在这个 Obsidian 文献 vault 中工作。请用中文交流。

## 用户信息

- 姓名：<your-name>
- 身份：机器人操控方向研究者
- 研究方向：双臂机器人 DLO 操控、视觉-语言模型、Sim-to-Real

## Structure

三层架构（Karpathy Wiki 模式）：

```
raw/              → Layer 1: 原始材料（只追加，不可修改）
wiki/             → Layer 2: 结构化知识（AI 维护为主）
  concepts/       → 概念页（如 DLO、Sim-to-Real）
  entities/       → 实体页（如研究者、实验室）
  topics/         → 主题页（如文献综述、方法对比）
output/           → Layer 3: 查询产品（报告、分析）
projects/         → 活跃项目
daily/            → 每日笔记，文件名 YYYY-MM-DD
archive/          → 已完成的项目和过时笔记
templates/        → 笔记模板（不要修改）
attachments/      → PDF 和图片附件
```

主数据流: Zotero → wiki → output。raw/ 用于手工材料、长综述分块和非 Zotero 原始材料。

## Frontmatter Specification

每个笔记必须包含:
```yaml
---
title: 标题
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: literature | concept | entity | permanent
status: stub | reading | done | archived
summary: 一句话摘要（30-80 字）
---
```

type 取值说明:
- `literature`: 文献笔记、阅读笔记
- `concept`: 概念页
- `entity`: 研究者、实验室或数据集等实体页
- `permanent`: Dashboard、项目页等长期维护页面

status 取值说明:
- `stub`: 待精读（AI 生成的初始笔记）
- `reading`: 精读中
- `done`: 精读完成
- `archived`: 已归档

## Glossary

- 用 "DLO" 而非 "Deformable Linear Object"
- 用 "VLM" 而非 "Vision-Language Model"
- 用 "RL" 而非 "Reinforcement Learning"
- 用 "vault" 而非 "知识库"
- 用 "Sim-to-Real" 而非 "仿真到真实迁移"

## Operating Rules

### 文件操作
- raw/ 下的文件是原始材料，只追加不修改
- wiki/ 下的文件主要由 AI 维护，人类可修正
- output/ 下的文件由 AI 从 wiki 生成
- templates/ 下的文件不要修改
- 创建新笔记时使用对应模板
- 新笔记必须包含完整 frontmatter

### 链接和标签
- 引用概念/文献/实体时用 `[[wikilink]]`
- 提及的概念如果没有 wiki 页面，主动创建 stub
- 标签不超过 5 个，顶级标签参见 SCHEMA.md

### 文献笔记流程
1. 从 Zotero 导入 → `wiki/topics/`
2. 自动补摘要格式、相关概念、相关研究者
3. 自动补 `## 结构化提取` 和 `## 本地引用关系`
4. 自动更新 `wiki/concepts/` 反向链接和概念间链接
5. 自动生成/补全 `wiki/entities/`
6. 精读后用 `finalize_reading.py` 写回分析，并把 `status` 从 `stub` 改为 `done`

一键导入优先使用：
```powershell
python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
```

回答领域问题前必须先查本地：
```powershell
python .claude/scripts/kb_search.py "问题" --limit 12
```
只有本地没有证据且用户同意时，才使用 web/arXiv/PubMed 等外部工具。

### 强制工作流触发

Claudian 必须把用户的自然语言请求路由到项目级命令或脚本，不得只靠自由发挥生成内容。

如果用户只是给出一句很短的自然语言请求，优先使用 `/expert 用户原话` 作为总控入口，让它先分类再执行下表中的具体工作流。

| 用户意图 | 必须执行 |
|---------|---------|
| “导入/新增/加入/import/ingest + Zotero key 或论文名” | 先确认 Zotero key，再运行 `/ingest-paper ZOTERO_KEY` |
| “精读/read-paper/读这篇/详细读” | 运行 `/read-paper ZOTERO_KEY`，必须写 analysis、finalize、后处理、审计 |
| “问领域问题/比较进展/有哪些工作” | 运行 `/search-kb 问题`，打开本地结果后回答 |
| “比较两篇论文/方法差异” | 优先运行 `/compare-papers PAPER_A PAPER_B`，再打开两篇本地笔记核对 |
| “更新概念/修复概念页/让概念页不是 stub” | 运行 `/update-concepts` |

完成定义：
- 文献导入完成 = topic note 已创建，frontmatter 完整，相关概念/研究者/本地引用关系已补全，并通过 `audit_kb.py`。
- 文献精读完成 = `finalize_reading.py` 成功写回，`status: done`，没有“待精读补充”、通用 summary、空 Evidence Notes，并通过 `audit_kb.py --strict-reading`。
- 概念页完成 = `status: done`，不是论文列表堆砌；必须包含 Definition、Key Ideas、Method Families、Key Papers、Evidence Map、Open Problems、Related Concepts、Related Papers。
- 批量任务完成 = 每篇都有成功/失败记录，后处理脚本已运行，最终审计结果已汇报。

禁止事项：
- 不得把摘要或通用介绍当作精读。
- 不得在没有本地证据时直接外搜。
- 不得编造 Zotero key、实验数字、本地引用关系或论文间联系。
- 不得在批量精读时并行抓多个 fulltext；必须逐篇处理，防止上下文爆掉。

### 渐进式精读（长篇综述 30+ 页）
当论文超过 15000 字符时，使用 `read_survey.py` 分块处理：
1. `python .claude/scripts/read_survey.py prepare --key ZOTERO_KEY` → 切块存入 `raw/chunks/{key}/`
2. Claudian 逐块精读：读 `chunk_NNN.md`，写 `analysis_NNN.md` 回同一目录
3. 每 N 块（默认 5）写一次 `interval_NNN.md` 作为上下文锚点
4. `python .claude/scripts/read_survey.py status --key ZOTERO_KEY` → 查看进度
5. `python .claude/scripts/read_survey.py assemble --key ZOTERO_KEY` → 合并为 `assembled.md`
6. Claudian 将 assembled 内容整理到 `raw/readings/ZOTERO_KEY-analysis.md`
7. `python .claude/scripts/finalize_reading.py ZOTERO_KEY --analysis raw/readings/ZOTERO_KEY-analysis.md` → 写回最终笔记并更新 status

### 自定义 Skills
- 当用户说"处理今天的笔记"时：读取最新 daily 笔记，识别所有可链接的实体（人名、论文名、概念），搜索 vault 中是否有对应笔记，如有则替换为 [[wikilink]]，如无则创建 stub
- 当用户说"整理本周笔记"时：读取过去 7 天的 daily 笔记，生成本周总结，保存到 output/
- 当用户说"编译 raw"时：读取 raw/ 中所有文件，按 SCHEMA.md 规范生成 wiki 文章，更新 INDEX.md

## Tools & MCP

### 核心 MCP 工具（按场景选用）

| 场景 | 工具 |
|------|------|
| 搜索 arXiv 论文 | `mcp__arxiv__search_papers` |
| 读取论文全文 | `mcp__arxiv__read_paper` |
| 下载论文 PDF | `mcp__arxiv__download_paper` |
| 搜索 Zotero 文献 | `mcp__zotero__zotero_search_items` |
| 获取文献元数据 | `mcp__zotero__zotero_item_metadata` |
| 获取文献全文 | `mcp__zotero__zotero_item_fulltext` |
| 分析论文图表 | `mcp__zai-mcp-server__analyze_image` |
| 分析技术图表 | `mcp__zai-mcp-server__understand_technical_diagram` |
| 分析数据可视化 | `mcp__zai-mcp-server__analyze_data_visualization` |
| 从截图提取文字 | `mcp__zai-mcp-server__extract_text_from_screenshot` |
| 分析视频 | `mcp__zai-mcp-server__analyze_video` |
| 网页搜索 | `mcp__grok-search__web_search` |
| 抓取网页内容 | `mcp__web-reader__webReader` |
| PubMed 搜索 | `mcp__pubmed__search_pubmed_articles` |
| Codex 并行任务 | `mcp__codex__codex` |

### 全局 Skills（适用于本 vault 的）

| Skill | 用途 |
|-------|------|
| arxiv-search | 搜索 arXiv 论文 |
| literature-review | 系统性文献综述 |
| systematic-literature-review | 系统综述 |

### 全局 Commands（适用于本 vault 的）

| Command | 用途 |
|---------|------|
| /research-init | 初始化研究项目 |
| /writer | 学术写作 |
| /librarian | 开放图书馆搜索 |
| /looker | 多模态分析（论文图表） |
| /recall | 间隔复习检查 |
| /explore | 探索 vault 结构 |

### 项目级 Commands

| Command | 用途 |
|---------|------|
| /expert | 总控入口：把一句自然语言请求路由到导入、精读、检索、比较、概念维护或审计工作流 |
| /ask-kb | 本地证据优先回答领域问题，适合“有哪些/区别/进展/综述” |
| /graph-help | 解释如何使用 Obsidian 知识图谱、概念页、反链和 `path:wiki` 过滤 |
| /kb-help | 显示本 vault 的 Claudian 命令用法和可复制示例 |
| /maintain-kb | 运行结构维护、概念反链、引用抽取、严格审计和检索烟测 |
| /import-paper | 单篇导入 Zotero 论文（MCP Zotero） |
| /ingest-paper | 单篇一键导入并更新本地知识网络 |
| /compile-raw | 将 raw/ 编译为 wiki 文章 |
| /read-paper | 查找现有 stub，精读论文并原地更新（短文直接读，长综述走渐进式分块） |
| /weekly-review | 生成本周总结 |
| /link-notes | 自动为笔记添加 [[wikilinks]] |
| /search-kb | 先查本地 wiki，再回答领域问题 |
| /recall | 本地间隔复习检查 |
| /compare-papers | 基于本地结构化字段比较两篇论文 |

### 全局 Agents（适用于本 vault 的）

| Agent | 用途 |
|-------|------|
| literature-reviewer | 文献综述 |
| paper-miner | 论文挖掘 |
| websearch | 网络搜索 |

## 不适用的全局配置

以下全局规则在此 vault 中**不生效**，请忽略：
- Python 开发规范、ruff、uv、pytest
- Git 规范（本 vault 不是代码仓库）
- TDD、superpowers 自动调用
- 前端设计相关 skills
- 代码审查、重构相关 tools
