# 文献知识库二次审计 Prompt

你是一个 Obsidian + Claudian + Zotero 知识库的审计专家。这是一个**二次审计**——上一轮审计发现了 10 个维度的问题，团队已完成修复。你的任务是验证每项修复是否到位，并发现新引入的问题。

## 审计规则

- **只读检查**，不修改任何文件
- 对每个原始问题，给出判定：✅ 已修复 / ⚠️ 部分修复 / ❌ 未修复
- 发现的新问题标注为 🆕
- 每项附上文件路径和行号证据
- 最后给出总体评分和下一步建议

---

## 上一轮发现的 10 个问题（逐项验证）

### 问题 1：架构一致性
原问题：`projects/文献阅读工作流.md` 仍写 `00-Inbox/01-Literature/02-Concepts/05-Attachments`，且描述 ZotLit 插件。两套架构并存。
验证点：
- [ ] `projects/文献阅读工作流.md` 已改为 `raw/wiki/output` 三层架构
- [ ] 删除了所有 ZotLit 引用
- [ ] `wiki/INDEX.md` 的 Concepts/Entities 段落不再显示 "(empty)"
- [ ] Dashboard.md 和模板字段全部对齐同一套架构

### 问题 2：模板与实际数据一致性
原问题：模板有 `doi/url/sources`，但实际 stub 用 `authors/year/venue/zotero_key`。
验证点：
- [ ] `templates/文献笔记模板.md` 的字段与实际 `wiki/topics/*.md` frontmatter 一致
- [ ] 模板包含 `zotero_key`、`venue`、`status`、`updated` 字段
- [ ] 存在统一的 schema 定义文件（如 `.claude/scripts/schema.json`），模板和脚本共享

### 问题 3：标签体系一致性
原问题：标签来源分裂，83 篇 topic 全部没有 status/updated 字段。
验证点：
- [ ] 所有 82 篇 topic 都有 `status` 字段（应为 "stub"）
- [ ] 所有 82 篇 topic 都有 `updated` 字段
- [ ] 标签来自受控词汇表，没有漂移

### 问题 4：工作流闭环性
原问题：`batch_index.py` 硬编码 collection key、无鉴权、覆盖写入、没有单篇导入命令。`read-paper.md` 总是"创建新 note"而非更新现有 stub。
验证点：
- [ ] `batch_index.py` 的 collection key 可配置（从 config.json 读取）
- [ ] `batch_index.py` 有 Zotero 连接失败的错误处理（try/except + 清晰错误信息）
- [ ] `batch_index.py` 的年份解析使用正则而非 `date[:4]`
- [ ] 存在 `/import-paper` 命令支持单篇导入
- [ ] `/read-paper` 命令已改为"查找现有 stub 并原地更新"模式

### 问题 5：知识库查询能力
原问题：83 篇 topic 的 wikilink 数量为 0；Dashboard 查询空目录；Smart Connections 配置冲突（language: en vs zh，exclusions 不一致）。
验证点：
- [ ] `wiki/topics/*.md` 中有 `[[wikilinks]]`（统计总数 > 0）
- [ ] `wiki/concepts/` 目录有概念页文件（> 0 个）
- [ ] `wiki/entities/` 目录有研究者页文件（> 0 个）
- [ ] Smart Connections 配置 `.smart-env/smart_env.json` 的 `language` 为 `"zh"`
- [ ] Smart Connections 配置的 `folder_exclusions` 排除了 `templates,.claude,.claudian,.obsidian,.smart-env`
- [ ] Dashboard.md 有阅读进度、年份统计等有意义的查询

### 问题 6：脚本质量
原问题：`batch_index.py:113` 用 `date[:4]` 导致 year 坏数据；`fix_abstracts.py` 标注通用词；`add_cn_abstract.py` 是死代码。
验证点：
- [ ] 所有 82 篇 topic 的 `year` 字段均为 4 位数字（`"20XX"` 格式），无 `"8/20"` 等损坏值
- [ ] `fix_abstracts.py` 已移除 `experiment/benchmark/significant/challenging` 等通用词
- [ ] `add_cn_abstract.py` 已删除

### 问题 7：Claudian 配置
原问题：systemPrompt 为空；mediaFolder 为 `05-Attachments`（与 app.json 的 `attachments` 冲突）；excludedTags 只有 `template`；permissionMode 为 yolo。
验证点：
- [ ] `.claudian/claudian-settings.json` 的 `systemPrompt` 非空，包含文献分析专用规则
- [ ] `mediaFolder` 为 `"attachments"`
- [ ] `excludedTags` 包含 `["template", "meta", "dashboard"]`
- [ ] （可选）`permissionMode` 已从 `"yolo"` 收紧

### 问题 8：Zotero 集成
原问题：Zotero Desktop Connector 未配置；没有 MCP 配置文件；工作流文档描述模糊。
验证点：
- [ ] `/import-paper` 命令明确使用 `mcp__zotero__zotero_item_metadata` 获取元数据
- [ ] `/read-paper` 命令明确使用 `mcp__zotero__zotero_item_fulltext` 获取全文
- [ ] `projects/文献阅读工作流.md` 清晰描述了单篇导入路径（MCP Zotero）

### 问题 9：冗余与冲突
原问题：ZotLit 未安装但仍被引用；大量全局 skills 不可用；.smart-env 缓存未清理。
验证点：
- [ ] `projects/文献阅读工作流.md` 无 ZotLit 引用
- [ ] `.claude/commands/` 中的命令均为可执行的实际命令（非空壳）

### 问题 10：用户体验模拟
原问题：三个用户场景均无法完成——单篇导入、语义问答、关系图。
验证点：
- [ ] 场景 1："帮我导入最新论文" → 有 `/import-paper <key>` 命令可用
- [ ] 场景 2："可变形物体操控的扩散策略" → wiki/concepts/ 有 DLO、diffusion 等概念页；wikilinks 存在
- [ ] 场景 3："找某论文所有笔记关系" → 研究者实体页有 [[wikilinks]] 到论文；论文笔记有 [[wikilinks]] 到概念

---

## 额外检查项（新增）

### 🆕 11. Schema 一致性
- [ ] `.claude/scripts/schema.json` 定义的 literature/concept/entity 三种类型的 required 字段
- [ ] 实际文件 frontmatter 与 schema 定义一致
- [ ] frontmatter 字段按 `canonical_order` 排列

### 🆕 12. 数据完整性
- [ ] 82 篇 topic 没有重复的 `zotero_key`
- [ ] 没有重复的 frontmatter 键（如两个 `title:` 行）
- [ ] 所有 frontmatter 的 `---` 分隔符正确闭合

### 🆕 13. 脚本健壮性
- [ ] `.claude/scripts/` 中的所有脚本可以 dry-run（至少有 `print` 输出确认操作）
- [ ] 新增脚本（`gen_concept_stubs.py`、`gen_entity_stubs.py`、`fix_wikilinks.py`）的幂等性（重复运行不会产生重复数据）

---

## 输出格式

```
## 二次审计结果

### 问题 1：架构一致性
判定：✅/⚠️/❌
证据：（文件路径:行号 + 引用片段）
备注：（如有未尽事宜）

...（对每个问题重复）...

### 新发现的问题
（如有）

### 总体评分
上次评分：X/10
本次评分：Y/10
改善幅度：+Z

### 遗留风险
（仍需手动完成的事项）

### 下一步建议
（优先级排序的 3-5 条行动项）
```

---

请现在开始审计。使用 Read/Grep/Glob 工具检查文件，不要修改任何文件。
