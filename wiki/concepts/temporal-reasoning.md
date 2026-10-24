---
title: "Temporal Reasoning（时序推理）"
tags: [concept, temporal]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "机器人策略中利用历史和未来信息进行跨时间步推理的能力，解决 VLA 的时序近视问题"
---

## Definition

Temporal Reasoning（时序推理） is maintained here as an evidence-linked concept. 机器人策略中利用历史和未来信息进行跨时间步推理的能力，解决 VLA 的时序近视问题

## Key Ideas

- Direct local evidence currently comes from [[lin2026hifvla]].
- The concept is tracked with local tags: concept, temporal.
- Treat this page as a map into local readings, not as external ground truth.
- Claims should be checked against the linked `status: done` topic notes before use in proposals.
- When evidence is sparse, use the broader-context papers below only for comparison, not as proof of the concept.

## Method Families

- Direct paper-specific method: inspect the direct evidence papers listed below.
- Robot learning context: compare how the concept changes policy learning, evaluation, or deployment.
- Planning/control context: check whether the concept affects temporal abstraction, constraints, or execution feedback.
- Representation context: check whether the concept changes visual, language, tactile, or geometric state representation.
- Evaluation context: prefer papers with explicit baseline, metric, ablation, and failure analysis.

## Key Papers

- [[lin2026hifvla]] (direct evidence): HiF-VLA 利用 MPEG-4 运动向量作为紧凑时序表示，通过后视先验编码、前视推理和后视调制联合专家实现双向时序推理，在 LIBERO-Long（96.4%）和 CAL...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[kang2026coenv]] (broader context): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...

## Evidence Map

- Direct evidence papers: [[lin2026hifvla]].
- Broader local evidence context: [[lin2026hifvla]], [[zhang2026recurrent]], [[zhang2026prts]], [[xiao2026avavla]], [[wang2026beyond]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[world-model]]
- [[long-horizon-manipulation]]
- [[motion-vector]]
- [[action-chunking]]
- [[robotic-manipulation]]

## Related Papers

- [[lin2026hifvla]]
- [[zhang2026recurrent]]
- [[zhang2026prts]]
- [[xiao2026avavla]]
- [[wang2026beyond]]
- [[tu2026embody4d]]
- [[kang2026coenv]]
- [[jeong2026your]]
