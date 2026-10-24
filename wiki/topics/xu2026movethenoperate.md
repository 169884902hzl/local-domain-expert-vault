---
title: "Move-then-operate: Behavioral phasing for human-like robotic manipulation"
tags: [manipulation, imitation, VLM]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于学习方法的操控方法，具有接触丰富特点。"
authors: "Xu, Haoming; Lei, Lei; Gu, Jie; Tang, Chu; Chen, Jingmin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "N7WZ8IDG"
---
## 摘要

We present Move-Then-Operate, a Vision language action framework that explicitly decouples robotic manipulation（机器人操控） into two distinct behavioral phases: coarse relocation (move) and contact-critical interaction (operate). Unlike monolithic policies that conflate these heterogeneous regimes, our architecture employs a dual-expert policy routed by a learnable phase selector, introducing a structural inductive bias that isolates phase-specific dynamics. Phase labels are automatically generated via an MLLM-based pipeline conditioned on lightweight contextual cues such as end-effector velocity and subtask decomposition to ensure alignment with human motor patterns. Evaluated on the RoboTwin2 benchmark, our method achieves an average success rate of $68.9\%$, outperforming the monolithic $π_0$ baseline by $24\%$. It matches or exceeds models trained on $10\times$ more data and reaches peak performance in $40\%$ fewer training steps, demonstrating that architectural disentanglement of move and operate phases is a highly effective and efficient strategy for mastering high-precision manipulation（操控）.

## 中文简述

提出基于学习方法的操控方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 N7WZ8IDG" 即可生成完整分析）

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
- [[imitation-learning]]
- [[vision-language-model]]

## 相关研究者

- [[xu-haoming|Xu, Haoming]]
