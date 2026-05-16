---
title: "Soft Actor-Critic"
tags: [concept, RL, off-policy]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "基于最大熵RL的off-policy actor-critic算法，兼具稳定性和样本效率"
---

## Definition

Soft Actor-Critic is maintained here as an evidence-linked concept. 基于最大熵RL的off-policy actor-critic算法，兼具稳定性和样本效率

## Key Ideas

- Direct local evidence currently comes from [[ji2026recovering]].
- The concept is tracked with local tags: concept, RL, off-policy.
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

- [[ji2026recovering]] (direct evidence): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[kohlbrenner2026egocentric]] (broader context): 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于...
- [[jin2026grounding]] (broader context): 系统性实证研究VLA模型零样本Sim-to-Real迁移的四维因子（域随机化、渲染保真度、物理真实度、RL微调），基于10k+真实世界试验得出五个关键结论：空间随机化主导迁移...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[ji2026recovering]].
- Broader local evidence context: [[ji2026recovering]], [[ye2026reinforcement]], [[xu2026token]], [[wu2025rlgsbridge]], [[kohlbrenner2026egocentric]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[maximum-entropy-rl]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[ji2026recovering]]
- [[ye2026reinforcement]]
- [[xu2026token]]
- [[wu2025rlgsbridge]]
- [[kohlbrenner2026egocentric]]
- [[jin2026grounding]]
- [[jeong2026your]]
- [[zhu2026nsvla]]
