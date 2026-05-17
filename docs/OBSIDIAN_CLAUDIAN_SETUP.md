# Obsidian And Claudian Setup

本页解释这个仓库里已经包含哪些 Obsidian / Claudian 配置，以及 clone 后还需要使用者自己做什么。

## 先说结论

这个仓库已经带了 **vault 级配置**，并打包了一个本地插件 `paper-reading-workbench`。其它社区插件只保留配置示例，不包含任何个人账号、API key、CLI 绝对路径或会话记录。

也就是说：

- 你 clone 后可以直接用 Obsidian 打开仓库根目录。
- Graph、Smart Connections 排除规则、模板路径、部分插件设置已经预置。
- Claudian 的行为规则和 system prompt 已经预置在 `.claudian/claudian-settings.json`。
- 公开包默认只启用已打包本体的 `paper-reading-workbench`，避免第一次打开 Obsidian 时出现缺 `main.js` 的插件报错。
- 你仍然需要在 Obsidian 里安装 Claudian、Dataview、Smart Connections、Templater、Zotero Desktop Connector 等第三方插件，然后按需启用。
- 你仍然需要在自己的机器上配置 Claude/Codex/Gemini/Zotero 登录或环境变量。

## 配置文件地图

| 路径 | 作用 | 是否含个人秘密 |
| --- | --- | --- |
| `.obsidian/community-plugins.json` | 默认只启用已打包的 `paper-reading-workbench` | 否 |
| `.obsidian/graph.json` | Graph 默认过滤为 `path:wiki` | 否 |
| `.obsidian/templates.json` | 模板目录配置 | 否 |
| `.obsidian/plugins/obsidian-smart-connections/data.json` | Smart Connections 排除非知识源路径 | 否 |
| `.obsidian/plugins/dataview/data.json` | Dataview 配置 | 否 |
| `.obsidian/plugins/templater-obsidian/data.json` | Templater 配置 | 否 |
| `.obsidian/plugins/claudian/manifest.json` | Claudian 插件元信息 | 否 |
| `.obsidian/plugins/claudian/data.json` | Claudian UI tab 状态，公开包已清空 | 否 |
| `.claudian/claudian-settings.json` | Claudian provider、权限、system prompt 和 vault 规则 | 已脱敏 |
| `.claude/commands/*.md` | 项目命令，如 `/read-paper`、`/search-kb` | 否 |
| `.claude/scripts/*.py` | Zotero、检索、审计和自动化脚本 | 否 |

## 推荐插件

在 Obsidian 中打开：

```text
Settings -> Community plugins -> Browse
```

推荐安装：

| 插件 | 用途 |
| --- | --- |
| Claudian | 在 Obsidian 里运行 Claude Code / Codex 类 agent |
| Dataview | Dashboard 和结构化查询 |
| Smart Connections | 语义检索；本 vault 建议只索引 `wiki/` |
| Templater | 使用 `templates/` 创建标准笔记 |
| Zotero Desktop Connector | 从 Zotero 读取 metadata/fulltext |
| Paper Reading Workbench | 已打包本地插件；从精读笔记回跳 Zotero item/PDF，并生成阅读工作台 |
| Excalidraw | 可选绘图；公开包不含个人绘图内容 |

注意：公开包只提交了 `paper-reading-workbench` 的 `main.js` / `styles.css`，因此默认只启用这个插件。其它插件没有提交 `main.js`，需要安装后再手动启用；保留在 `.obsidian/plugins/*/data.json` 的配置会作为参考配置使用。

### Paper Reading Workbench：从 Obsidian 回到 Zotero PDF

这个插件解决的是人类阅读时的回跳路径：你在 Obsidian 看到一篇精读笔记后，可以回到 Zotero 条目和 PDF 原文对照阅读。

使用方式：

1. 打开一个带 `zotero_key` frontmatter 的 `wiki/topics/*.md` 文献笔记。
2. 确认 Zotero Desktop 正在运行，并且该 item 下已有 stored PDF 或 linked PDF 附件。
3. 在命令面板运行 `Paper Reading Workbench: Open paper reading workbench for current note`，也可以点左侧 ribbon / status bar 的 `Paper Workbench`。
4. 插件会读取 `zotero_key`，查询本机 Zotero Connector API `http://localhost:23119`，并生成或更新 `projects/reading-workbench/<ZOTERO_KEY>-zotero-source.md`。
5. 工作台会提供 `Open Zotero item`、`Open Zotero PDF attachment`、`Open arXiv PDF fallback`、精读笔记、Gemini idea、翻译缓存和知识图入口。PDF 附件会优先使用 Zotero 的 `zotero://open-pdf/...` URI 打开；非 PDF 附件会回退到 Zotero item selection。

边界：

- 插件不会把 PDF 复制进 vault。
- Zotero 仍然是原文 PDF 的 source of truth。
- 如果 Zotero Desktop 没打开，或者该 item 没有 PDF 附件，插件会显示 Zotero local API unavailable 或回退到 Zotero item / arXiv PDF URL。
- 插件会在 `projects/reading-workbench/`、`projects/translations/`、`projects/knowledge-diagrams/` 生成本地工作台文件；这些运行产物默认不提交 Git。
- 这是随仓库打包的本地可执行插件。打开工作台只读取当前 note 和 Zotero local API；点击翻译、知识图等动作时，插件会启动本机 Python helper script。首次使用前可以先读 `.obsidian/plugins/paper-reading-workbench/main.js`。

## Smart Connections 配置

目标：让语义索引只服务正式知识层，不把脚本、原始材料、附件、项目日志混入回答。

当前公开包预置：

```json
{
  "excluded_paths": "templates/**,.claude/**,.agents/**,.claudian/**,.obsidian/**,.smart-env/**,raw/**,output/**,archive/**,exports/**,attachments/**,projects/**,AGENTS.md,CLAUDE.md,SCHEMA.md,Dashboard.md",
  "language": "zh"
}
```

首次启用 Smart Connections 后建议：

1. 打开 Smart Connections 设置。
2. 确认 exclusion / ignored paths 包含上面的非知识源路径。
3. 删除旧索引或点击 rebuild。
4. 等待索引重建完成。
5. 搜索时优先确认结果来自 `wiki/`。

如果 Smart Connections 仍显示 `raw/`、`.claude/`、`projects/` 等内容，通常是旧索引没有重建，不一定是配置文件错误。

## Graph 配置

`.obsidian/graph.json` 已设置：

```json
{
  "search": "path:wiki"
}
```

这意味着默认 graph 只展示正式知识层：

- `wiki/topics/`
- `wiki/concepts/`
- `wiki/entities/`

如果你想看全 vault，可以在 Obsidian graph 里临时清空 search filter；但正式知识源建议仍以 `wiki/` 为准。

## Claudian 配置

Claudian 的主配置在：

```text
.claudian/claudian-settings.json
```

公开包里保留了这些关键行为：

| 配置 | 当前值/含义 |
| --- | --- |
| `locale` | `zh-CN` |
| `permissionMode` | `normal`，公开包默认保守权限 |
| `model` | `opus` |
| `effortLevel` | `max` |
| `mediaFolder` | `attachments` |
| `systemPrompt` | 本地证据优先、Zotero 脚本化导入、精读 finalize、维护后审计 |
| `providerConfigs.claude.safeMode` | `acceptEdits`，Claudian provider 级行为；首次使用前请在 UI 中确认 |
| `providerConfigs.codex.safeMode` | `workspace-write`，Codex provider 级行为；首次使用前请在 UI 中确认 |
| `providerConfigs.claude.cliPath` | 已清空，用户自己配置 |
| `providerConfigs.codex.cliPath` | 已清空，用户自己配置 |
| `sharedEnvironmentVariables` | 已清空 |
| `envSnippets` | 已清空 |

### 重要安全提醒

公开配置默认使用 `permissionMode = normal`。这个 vault 的完整自动化流程原本可以在更高自治权限下运行，但新用户第一次打开仓库时不应该默认继承高权限写入和命令执行边界。

如果你已经理解 `.claude/commands/` 和 `.claude/scripts/` 会做什么，并且愿意让 agent 自动读写 vault 文件，可以在 Claudian UI 里手动切到更高权限模式。不要把高权限配置直接提交到公开仓库。

Claude CLI 的 `--dangerously-skip-permissions` 也不再是公开默认值。发布版脚本只有在你显式传入 `--allow-dangerous-claude`，或设置 `LOCAL_FIRST_VAULT_ALLOW_DANGEROUS_CLAUDE=1` 时，才会把该参数传给 Claude。这个 opt-in 只适合你完全理解本机权限边界并愿意承担自动读写风险的本地环境。

不管使用什么权限模式，都不要让 agent 看到真实 API key 文本；用系统环境变量或本机 CLI 登录状态提供凭据。

`.claude/settings.json` 是 Claude Code 的项目级 allow list。公开包默认只保留 `Read`、`Glob`、`Grep` 和少数明确的本地安全命令，例如 `audit_kb.py`、`kb_search.py`、`daily_arxiv_pipeline.py --dry-run`、`arxiv_metadata_sync.py --dry-run` 和脱敏 Zotero preflight。第三方 MCP、通用 `Write/Edit`、`curl`、`claude`、`gemini`、宽泛 `python *` 不在公开默认 allow list 中。

如果你要启用更完整的 Zotero、arXiv、Gemini 或 Codex 自动化，请先理解对应命令会读写哪些目录，再在自己的本地配置中手动放宽权限。不要把本机高权限 allow list 提交回公开仓库。

## Claudian system prompt 做了什么

公开配置中的 system prompt 约束 Claudian：

1. 回答领域问题前，必须先运行：

   ```powershell
   python .claude/scripts/kb_search.py "问题" --limit 12
   ```

2. 导入论文时走脚本：

   ```powershell
   python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
   ```

3. 精读论文不能只写摘要，必须获取全文、写 `raw/readings/ZOTERO_KEY-analysis.md`、运行 `finalize_reading.py`、再运行维护和审计脚本。

4. 批量处理必须一篇一篇抓 fulltext，不能并行抓多个全文。

5. 创建/更新笔记必须遵守 `.claude/scripts/schema.json`。

6. `raw/` 是原始材料区，默认只追加不改写。

这套约束的目的，是让 AI 不是自由发挥写一段“看似合理”的回答，而是被迫走本地证据和脚本化工作流。

## Claudian 项目命令

项目命令在 `.claude/commands/`。

| 命令 | 作用 |
| --- | --- |
| `/expert` | 总控入口，把自然语言请求路由到具体 workflow |
| `/ask-kb` 或 `/search-kb` | 先查本地 wiki，再回答领域问题 |
| `/ingest-paper` | 单篇 Zotero 论文导入 |
| `/read-paper` | 查找 stub，获取全文，精读并 finalize |
| `/compare-papers` | 比较两篇本地论文 |
| `/update-concepts` | 升级概念页 |
| `/maintain-kb` | 运行结构维护和审计 |
| `/graph-help` | 解释 Obsidian graph 使用方式 |
| `/kb-help` | 显示 vault 命令用法 |

## 首次配置 Claudian

1. 安装 Claudian 插件。
2. 打开这个 vault。
3. 打开 Claudian 设置页。
4. 检查 provider：
   - Claude provider：选择你本机可用的 Claude Code / Claude CLI。
   - Codex provider：如果需要 Codex review，选择你本机可用的 Codex CLI。
5. 确认 `.claudian/claudian-settings.json` 已加载。
6. 根据自己的风险偏好调整权限模式。
7. 在 Claudian 里运行：

   ```text
   /kb-help
   ```

8. 再试：

   ```text
   /search-kb diffusion policy DLO
   ```

如果命令能返回 `wiki/topics/...` 路径，说明本地检索工作流已经接上。

## Zotero Desktop Connector 配置

如果你要从 Zotero 读 metadata/fulltext：

1. 安装 Zotero Desktop。
2. 安装 Obsidian Zotero Desktop Connector。
3. 保持 Zotero Desktop 打开。
4. 确认本地 connector API 可用：

   ```powershell
   python .claude/scripts/zotero_import.py --preflight --json
   ```

如果使用 Zotero Web API，按 README 设置：

```powershell
setx ZOTERO_USER_ID "<your-zotero-user-id>"
setx ZOTERO_API_KEY "<your-zotero-api-key>"
setx ZOTERO_COLLECTION_KEY "<your-collection-key>"
```

重新打开 PowerShell 后再测试。

## 常见配置问题

### 插件列表里有 Claudian，但 Obsidian 没有显示 Claudian

公开包只打包了 Paper Reading Workbench。本节说的是 Claudian：去 Community Plugins 安装 Claudian 后，再手动启用。

### Claudian 打开后没有项目命令

确认 vault 根目录下存在：

```text
.claude/commands/
AGENTS.md
CLAUDE.md
```

然后重启 Obsidian 或重载 Claudian。

### Claudian 找不到 Claude/Codex CLI

公开包清空了 `cliPath` 和 host-specific path。请在 Claudian 设置 UI 中重新选择本机 CLI，或确保命令行里能运行：

```powershell
claude --version
codex --version
```

### Smart Connections 结果污染

重建 Smart Connections 索引。只改配置文件不足以删除旧索引。

### 自动化写了很多 `projects/` 内容

这是正常的。`projects/` 是运行产物和研究议程目录，默认被 `.gitignore` 忽略，不会上传 GitHub。
