---
title: "Reward Shaping"
tags: [rl, reward-engineering]
created: "2026-05-05"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "通过修改奖励函数来引导 RL 智能体学习的技术，基于势函数的方法可保证不改变最优策略"
---

## Definition

Reward Shaping is maintained here as an evidence-linked concept. 通过修改奖励函数来引导 RL 智能体学习的技术，基于势函数的方法可保证不改变最优策略

## Key Ideas

- Direct local evidence currently comes from [[ye2026reinforcement]].
- The concept is tracked with local tags: rl, reward-engineering.
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

- [[ye2026reinforcement]] (direct evidence): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[ryu2025curricullm]] (broader context): 提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curr...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[chen2025vegetable]] (broader context): 提出约束灵巧操控框架，用 Allegro 手在 Franka 臂上通过 RL 学习可控停止的蔬菜重定向策略，实现重定向→牢固握持→削皮的多步骤循环，4 种蔬菜上 90% 牢固...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...

## Evidence Map

- Direct evidence papers: [[ye2026reinforcement]].
- Broader local evidence context: [[ye2026reinforcement]], [[ryu2025curricullm]], [[ji2026recovering]], [[chen2025vegetable]], [[zhu2026nsvla]].
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
- [[visual-reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[ye2026reinforcement]]
- [[ryu2025curricullm]]
- [[ji2026recovering]]
- [[chen2025vegetable]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhang2026prts]]
- [[zhang2021dair]]
