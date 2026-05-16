---
title: "过程感知推理"
tags: [concept, reasoning, perception]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "将视觉推理显式分解为感知（perception）和推理（reasoning）两个独立过程，分别建模、监督和优化。"
---

## Definition

过程感知推理 is maintained here as an evidence-linked concept. 将视觉推理显式分解为感知（perception）和推理（reasoning）两个独立过程，分别建模、监督和优化。

## Key Ideas

- Direct local evidence currently comes from [[jiang2026videop2r]].
- The concept is tracked with local tags: concept, reasoning, perception.
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

- [[jiang2026videop2r]] (direct evidence): 提出 VideoP2R 框架，将视频推理显式分解为感知和推理两个独立过程，通过三步 CoT 管线构建 162K 过程感知数据集，并设计 PA-GRPO 算法为两个过程分别提供...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...

## Evidence Map

- Direct evidence papers: [[jiang2026videop2r]].
- Broader local evidence context: [[jiang2026videop2r]], [[zhang2026prts]], [[tu2026embody4d]], [[zhou2026rcnf]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-fine-tuning]]
- [[grpo]]
- [[chain-of-thought]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jiang2026videop2r]]
- [[zhang2026prts]]
- [[tu2026embody4d]]
- [[zhou2026rcnf]]
- [[zheng2026pokevla]]
- [[zhang2026recurrent]]
- [[xu2026roboagent]]
- [[xiao2026avavla]]
