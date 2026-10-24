---
title: "Visual Token Pruning"
tags: [VLA, efficiency, token-reduction]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "视觉 token 剪枝是通过减少视觉编码器输出的 token 数量来加速 VLA 推理的技术，包括语义剪枝、动态剪枝和连续采样等方法。"
---

## Definition

Visual Token Pruning is maintained here as an evidence-linked concept. 视觉 token 剪枝是通过减少视觉编码器输出的 token 数量来加速 VLA 推理的技术，包括语义剪枝、动态剪枝和连续采样等方法。

## Key Ideas

- Direct local evidence currently comes from [[feng2026see]].
- The concept is tracked with local tags: VLA, efficiency, token-reduction.
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

- [[feng2026see]] (direct evidence): GridS 提出可微双线性网格采样模块，将 VLA 视觉 token 从 256 压缩至 16（甚至 1），通过端到端优化的连续坐标预测保留亚 patch 级空间精度，在 7...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...

## Evidence Map

- Direct evidence papers: [[feng2026see]].
- Broader local evidence context: [[feng2026see]], [[zhu2026nsvla]], [[zhong2026vlaopd]], [[zheng2026pokevla]], [[zhang2026visionlanguageaction]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action-model]]
- [[grid-sampler]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[feng2026see]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[xu2026token]]
- [[xiao2026avavla]]
