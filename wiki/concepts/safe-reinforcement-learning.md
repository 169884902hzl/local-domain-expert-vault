---
title: "Safe Reinforcement Learning"
tags: [reinforcement-learning, safety, constrained-optimization]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "在满足安全约束的前提下进行策略优化的强化学习范式，通常基于 CMDP 框架和 Lagrangian 方法实现安全-性能权衡。"
---

## Definition

Safe Reinforcement Learning is maintained here as an evidence-linked concept. 在满足安全约束的前提下进行策略优化的强化学习范式，通常基于 CMDP 框架和 Lagrangian 方法实现安全-性能权衡。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: reinforcement-learning, safety, constrained-optimization.
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

- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[jiang2026world4rl]] (broader context): 提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-Worl...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...
- [[chen2026adacleargrasp]] (broader context): 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zhang2026safevla]], [[zhang2021dair]], [[yang2026asyncshield]], [[xu2026expertgen]], [[jiang2026world4rl]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[vision-language-action]]
- [[collision-avoidance]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[zhang2026safevla]]
- [[zhang2021dair]]
- [[yang2026asyncshield]]
- [[xu2026expertgen]]
- [[jiang2026world4rl]]
- [[jeong2026your]]
- [[chen2026adacleargrasp]]
- [[zhu2026nsvla]]
