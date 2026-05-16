---
title: Dashboard
tags: [dashboard, meta]
created: 2026-04-25
updated: 2026-04-25
type: permanent
summary: 文献知识库总览仪表盘
---

# Literature Dashboard

## Claudian Quick Commands

在 Claudian 输入框里输入 `/` 打开命令下拉菜单，然后选择命令并在后面补参数。

| Command | When to use | Example |
|---------|-------------|---------|
| `/expert` | 不确定该用哪个工作流时的默认入口 | `/expert 最近有哪些扩散策略做双臂操控的工作？` |
| `/ask-kb` | 只想基于本地 wiki 回答领域问题 | `/ask-kb DLO 操控中 VLM 和触觉分别解决什么问题？` |
| `/graph-help` | 不知道知识图谱怎么用时 | `/graph-help` |
| `/ingest-paper` | Zotero 已有论文，先创建/刷新笔记 | `/ingest-paper ABCD1234` |
| `/read-paper` | 对已导入论文做完整精读 | `/read-paper ABCD1234` |
| `/compare-papers` | 比较两篇本地论文 | `/compare-papers zhu2024scaling vs keunknowndiffuser` |
| `/update-concepts` | 更新概念页 | `/update-concepts diffusion-model` |
| `/maintain-kb` | 检查是否还有结构问题或 WARN | `/maintain-kb all` |
| `/kb-help` | 忘记怎么用时查看命令菜单 | `/kb-help` |

## Knowledge Graph

- 图谱入口：[[INDEX|wiki/INDEX]]
- 使用说明：[[GRAPH_GUIDE]]
- Obsidian Graph View 推荐过滤：`path:wiki`
- Smart Connections 和 Obsidian 全局排除已收敛到正式知识库，默认不索引 `raw/`、`output/`、`archive/`、`exports/`

## 阅读进度

```dataview
TABLE length(rows) AS "数量"
FROM "wiki/topics"
WHERE type = "literature"
GROUP BY status
SORT length(rows) DESC
```

## 按年份统计

```dataview
TABLE length(rows) AS "篇数"
FROM "wiki/topics"
WHERE type = "literature" AND year
GROUP BY year
SORT year DESC
```

## 按研究方向分组

```dataview
TABLE length(rows) AS "篇数"
FROM "wiki/topics"
WHERE type = "literature"
FLATTEN tags AS t
GROUP BY t
SORT length(rows) DESC
```

## 待精读 (stub)

```dataview
TABLE tags AS "标签", year AS "年份", summary AS "摘要"
FROM "wiki/topics"
WHERE type = "literature" AND status = "stub"
SORT year DESC
```

## 已精读 (done)

```dataview
TABLE tags AS "标签", year AS "年份", summary AS "摘要"
FROM "wiki/topics"
WHERE type = "literature" AND status = "done"
SORT year DESC
```

## Wiki — Concepts

```dataview
TABLE summary AS "定义", status AS "状态"
FROM "wiki/concepts"
WHERE type = "concept"
SORT title ASC
```

## Wiki — Entities

```dataview
TABLE summary AS "描述"
FROM "wiki/entities"
WHERE type = "entity"
SORT title ASC
```

## Active Projects

```dataview
TABLE tags, status, updated
FROM "projects"
SORT updated DESC
```
