---
title: "Policy Regularization"
tags: [RL, policy-optimization, trust-region]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "在策略更新过程中通过 KL 散度、trust region 或其他约束限制策略变化幅度，防止灾难性遗忘和训练不稳定。"
---

## Definition

Policy Regularization is maintained here as an evidence-linked concept. 在策略更新过程中通过 KL 散度、trust region 或其他约束限制策略变化幅度，防止灾难性遗忘和训练不稳定。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: RL, policy-optimization, trust-region.
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

- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[ye2026reinforcement]], [[moroncelli2026jumpstart]], [[he2026generative]], [[ziakas2026aligning]], [[zhou2026ego]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[offline-rl]]
- [[reinforcement-learning]]
- [[discrete-flow-matching]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[ye2026reinforcement]]
- [[moroncelli2026jumpstart]]
- [[he2026generative]]
- [[ziakas2026aligning]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
