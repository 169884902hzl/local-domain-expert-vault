# Wiki Schema

本文件定义 wiki 层的命名规范、标签体系、链接规则和文章模板。
AI 维护 wiki 时必须严格遵循此规范。

## 命名规范

- 概念页: `wiki/concepts/concept-name.md`（小写英文，连字符分隔）
  - 例: `wiki/concepts/sim-to-real.md`
  - 例: `wiki/concepts/deformable-linear-object.md`
- 实体页: `wiki/entities/lastname-firstname.md`（人名用英文全名；旧的单姓页面仅保留兼容）
  - 例: `wiki/entities/sergey-levine.md`
  - 例: `wiki/entities/hust-robotics-lab.md`
- 主题页: `wiki/topics/topic-description.md`
  - 例: `wiki/topics/dual-arm-dlo-manipulation-survey.md`

## Frontmatter 模板

每个 wiki 文章必须包含:

```yaml
---
title: 文章标题
type: literature | concept | entity
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: stub | reading | done | archived
summary: 一句话摘要（30-80 字）
---
```

## 标签体系

- 领域标签: `#manipulation`, `#DLO`, `#VLM`, `#RL`, `#imitation`, `#diffusion`, `#sim-to-real`, `#robot-learning`, `#tactile`, `#tactile-sensing`, `#bimanual`, `#planning`, `#grasping`, `#LfD`, `#dynamical-systems`, `#neural-potential-function`, `#phase-variable`, `#reactive-control`, `#collision-avoidance`, `#proximity-sensing`, `#test-time-scaling`, `#MPC`, `#contact-implicit`, `#physical-reasoning`, `#trajectory-optimization`
- 状态标签: `#stub`（待扩展）, `#mature`（完整）
- 不要随意创建新顶级标签；如需新增，先更新此文件

## Wikilink 规则

- 首次提及已有 wiki 页面的概念时，使用 [[链接]]
- 同一篇文章内，同一概念只链接第一次出现
- 提及的概念如果没有 wiki 页面，创建 stub 页面
- 文献笔记中引用其他文献时用 [[wikilink]]

## 文章结构

- **概念页**: 定义 → 核心要点 → 与其他概念的关系 → 来源
- **实体页**: 简介 → 主要贡献/特点 → 相关概念/实体 → 来源
- **文献页**: 摘要 → 中文简述 → 关键贡献 → 结构化提取 → 本地引用关系 → 相关概念 → 相关研究者
- **结构化提取字段**: Problem, Method, Tasks, Sensors, Robot Setup, Metrics, Limitations, Evidence Notes
- **本地引用关系**: 只记录正文或精读分析中有证据的本地论文链接；没有证据时写 `-`，不要臆造引用关系
- **主题页**: 概述 → 多角度分析 → 结论 → 来源

## 全局索引

新增或修改 wiki 文章后，优先运行：

```powershell
python .claude/scripts/gen_entity_stubs.py --include-first-authors
python .claude/scripts/ensure_literature_structure.py
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py
```

`wiki/INDEX.md` 使用 Dataview 动态列出页面；只有静态统计文字需要人工更新。
