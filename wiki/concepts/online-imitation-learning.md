---
title: "Online Imitation Learning"
tags: [imitation-learning, online-learning]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "在线模仿学习通过策略与环境交互采集 on-policy 数据并以专家标签监督，缓解离线模仿学习的分布偏移问题。"
---

## Definition

Online Imitation Learning is maintained here as an evidence-linked concept. 在线模仿学习通过策略与环境交互采集 on-policy 数据并以专家标签监督，缓解离线模仿学习的分布偏移问题。

## Key Ideas

- Direct local evidence currently comes from [[wei2026navol]].
- The concept is tracked with local tags: imitation-learning, online-learning.
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

- [[wei2026navol]] (direct evidence): 基于 DAgger 框架在 IsaacLab 中实现导航扩散策略的在线模仿学习，通过全局规划器提供在线专家轨迹监督，以 rollout-update 循环消除奖励工程、缓解分...
- [[wu2026large]] (broader context): 将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器（时序对比/绝对进度/任务完成），在 ManiSkill3 零样本长时序操控和真实世界 pick-and...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...
- [[park2026demodiffusion]] (broader context): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[jiang2026world4rl]] (broader context): 提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-Worl...
- [[gao2026driftbased]] (broader context): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...

## Evidence Map

- Direct evidence papers: [[wei2026navol]].
- Broader local evidence context: [[wei2026navol]], [[wu2026large]], [[wu2025imperfect]], [[park2026demodiffusion]], [[moroncelli2026jumpstart]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[dagger]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robotic-manipulation]]

## Related Papers

- [[wei2026navol]]
- [[wu2026large]]
- [[wu2025imperfect]]
- [[park2026demodiffusion]]
- [[moroncelli2026jumpstart]]
- [[jie2026omnivlarl]]
- [[jiang2026world4rl]]
- [[gao2026driftbased]]
