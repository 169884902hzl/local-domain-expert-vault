---
title: "Characterizing vision-language-action models across XPUs: Constraints and acceleration for on-robot deployment"
tags: [VLM, RL, diffusion]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于扩散模型的操控方法。"
authors: "Zhou, Kaijun; Chen, Qiwei; Peng, Da; Li, Zhiyang; Li, Xijun et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QZCXJMFK"
---
## 摘要

Vision-Language-Action (VLA) models are promising for generalist robot control, but on-robot deployment is bottlenecked by real-time inference under tight cost and energy budgets. Most prior evaluations rely on desktop-grade GPUs, obscuring the trade-offs and opportunities offered by heterogeneous edge accelerators (GPUs/XPUs/NPUs). We present a systematic analysis for low-cost VLA deployment via model-hardware co-characterization. First, we build a cross-accelerator leaderboard and evaluate model-hardware pairs under CET (Cost, Energy, Time), showing that right-sized edge devices can be more cost-/energy-efficient than flagship GPUs while meeting control-rate constraints. Second, using in-depth profiling, we uncover a consistent two-phase inference pattern: a compute-bound VLM backbone followed by a memory-bound Action Expert, which induces phase-dependent underutilization and hardware inefficiency. Finally, guided by these insights, we propose DP-Cache and V-AEFusion to reduce diffusion（扩散） redundancy and enable asynchronous pipeline parallelism, achieving up to 2.9x speedup on GPUs and 6x on edge NPUs with only marginal success degradation. The example leaderboard website is available at: https://vla-leaderboard-01.vercel.app/.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 视觉-语言模型、强化学习、扩散模型

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 QZCXJMFK" 即可生成完整分析）

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

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]

## 相关研究者

- [[zhou-kaijun|Zhou, Kaijun]]
