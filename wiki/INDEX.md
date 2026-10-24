---
title: Wiki Index
type: index
created: 2026-04-25
updated: 2026-05-16
---

# Wiki Index

> 本索引按分类列出所有 wiki 页面。每次新增或修改 wiki 文章后更新此文件。

## Knowledge Graph Entry Points

- 使用说明：[[GRAPH_GUIDE]]
- 顶层领域：[[robotic-manipulation]]
- 关键对象：[[deformable-linear-object]]、[[grasping]]、[[tactile-sensing]]
- 学习方法：[[imitation-learning]]、[[reinforcement-learning]]、[[diffusion-model]]、[[robot-learning]]
- 系统能力：[[vision-language-model]]、[[sim-to-real]]、[[planning]]、[[bimanual-manipulation]]

## Concepts

```dataview
TABLE summary AS "定义", tags AS "标签"
FROM "wiki/concepts"
WHERE type = "concept"
SORT title ASC
```

## Entities

```dataview
TABLE summary AS "描述", tags AS "标签"
FROM "wiki/entities"
WHERE type = "entity"
SORT title ASC
```

## Topics

```dataview
TABLE year AS "年份", summary AS "中文简述", tags AS "标签"
FROM "wiki/topics"
WHERE type = "literature"
SORT year DESC
```

> 文献数量以 `wiki/topics/` 实际文件和 Dataview 查询结果为准；公开仓库不绑定任何私有 Zotero collection。
> 精读某篇论文：在 Claudian 中使用 `/read-paper <zotero_key>`。
