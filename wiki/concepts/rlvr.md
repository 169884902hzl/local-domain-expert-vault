---
title: "RLVR (Reinforcement Learning with Verifiable Rewards)"
tags: [concept, RL, LLM]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "使用任务内在的可验证标准提供客观奖励信号，替代学习型奖励模型的强化学习范式。"
---

## Definition

RLVR (Reinforcement Learning with Verifiable Rewards) is maintained here as an evidence-linked concept. 使用任务内在的可验证标准提供客观奖励信号，替代学习型奖励模型的强化学习范式。

## Key Ideas

- Direct local evidence currently comes from [[li2026realvlgr1]].
- The concept is tracked with local tags: concept, RL, LLM.
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

- [[li2026realvlgr1]] (direct evidence): 构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...

## Evidence Map

- Direct evidence papers: [[li2026realvlgr1]].
- Broader local evidence context: [[li2026realvlgr1]], [[zhu2026nsvla]], [[zhong2026vlaopd]], [[zhao2026visualtactile]], [[zhang2026world2minecraft]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grpo]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[li2026realvlgr1]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhang2026world2minecraft]]
- [[zhang2026safevla]]
- [[zhang2026prts]]
- [[zhang2021dair]]
