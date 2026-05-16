---
title: "Libra-VLA: Achieving learning equilibrium via asynchronous coarse-to-fine dual-system"
tags: [manipulation, VLM, planning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于视觉-语言的操控方法。"
authors: "Wei, Yifei; Zhong, Linqing; Liu, Yi; Lu, Yuxiang; He, Xindong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZV6NPX4T"
---
## 摘要

Vision-Language-Action (VLA) models are a promising paradigm for generalist robotic manipulation（机器人操控） by grounding high-level semantic instructions into executable physical actions. However, prevailing approaches typically adopt a monolithic generation paradigm, directly mapping visual-linguistic features to high-frequency motor commands in a flat, non-hierarchical fashion. This strategy overlooks the inherent hierarchy of robotic manipulation（机器人操控）, where complex actions can be naturally modeled in a Hybrid Action Space, decomposing into discrete macro-directional reaching and continuous micro-pose alignment, severely widening the semantic-actuation gap and imposing a heavy representational burden on grounding high-level semantics to continuous actions. To address this, we introduce Libra-VLA, a novel Coarse-to-Fine Dual-System VLA architecture. We explicitly decouple the learning complexity into a coarse-to-fine hierarchy to strike a training equilibrium, while simultaneously leveraging this structural modularity to implement an asynchronous execution strategy. The Semantic Planner predicts discrete action tokens capturing macro-directional intent, while the Action Refiner conditions on coarse intent to generate high-frequency continuous actions for precise alignment. Crucially, our empirical analysis reveals that performance follows an inverted-U curve relative to action decomposition granularity, peaking exactly when the learning difficulty is balanced between the two sub-systems. With the asynchronous design, our approach offers a scalable, robust, and responsive solution for open-world manipulation（操控）.

## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 机器人操控、视觉-语言模型、运动规划

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 ZV6NPX4T" 即可生成完整分析）

## 结构化提取

- Problem: 待精读补充
- Method: 待精读补充
- Tasks: 待精读补充
- Sensors: 待精读补充
- Robot Setup: 待精读补充
- Metrics: 待精读补充
- Limitations: 待精读补充
- Evidence Notes: 待精读补充

## 本地引用关系

-
## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[planning]]

## 相关研究者

- [[wei|Wei, Yifei]]
