---
title: Knowledge Graph Guide
tags: [meta, dashboard]
created: 2026-04-27
updated: 2026-04-27
type: index
status: done
summary: 知识图谱使用入口：说明 Obsidian 图谱、概念页、论文页和本地证据检索如何配合使用。
---

# Knowledge Graph Guide

## 这套图谱是什么

本 vault 的知识图谱不是一张单独的图片，而是由 `wiki/` 下的三类页面组成：

- `wiki/topics/`：论文节点，每篇论文一页。
- `wiki/concepts/`：概念节点，例如 [[diffusion-model]]、[[deformable-linear-object]]、[[vision-language-model]]。
- `wiki/entities/`：研究者或机构节点。

Obsidian Graph View 会把这些 wiki links 画成图。

## 推荐用法

1. 打开 Obsidian 的 Graph View。
2. 在过滤框使用：`path:wiki`
3. 从核心概念开始看：
   - [[robotic-manipulation]]
   - [[diffusion-model]]
   - [[deformable-linear-object]]
   - [[vision-language-model]]
   - [[tactile-sensing]]
   - [[bimanual-manipulation]]
4. 点开一个概念页，看 `Related Papers` 找代表论文。
5. 点开论文页，看：
   - `## 相关概念`
   - `## 相关研究者`
   - `## 本地引用关系`

## 和 Claudian 怎么配合

如果你不知道该点哪里，直接在 Claudian 里用：

```text
/expert 我想理解扩散策略和双臂操控的关系
/ask-kb DLO 操控中 VLM 和触觉分别解决什么问题？
/graph-help
```

Claudian 应先查本地 wiki，再用路径作为证据回答。

## 图谱过滤建议

全局图谱建议只看 `wiki/`：

```text
path:wiki
```

不要默认把 `raw/`、`output/`、`.claude/`、`.obsidian/` 放进图谱。那些目录包含草稿、分析中间产物或配置说明，会产生不属于正式知识图谱的链接。

当前配置已经做了两层收敛：

- Obsidian Graph View 默认过滤：`path:wiki`
- Obsidian Excluded files 与 Smart Connections excluded paths 排除 `raw/`、`output/`、`archive/`、`exports/`、配置目录和附件目录

如果需要查原始精读分析，用文件浏览器直接打开 `raw/readings/`；不要把它作为正式图谱或语义检索来源。

## 当前核心概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[tactile-sensing]]
- [[planning]]
- [[grasping]]
