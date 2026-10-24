---
title: "Adjoint Matching (QAM)"
tags: [RL, flow-matching, policy-extraction]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "通过伴随方法将 critic 梯度转化为 flow policy 的分步局部回归目标，避免多步去噪反向传播的不稳定性。"
---

## Definition

Adjoint Matching (QAM) is maintained here as an evidence-linked concept. 通过伴随方法将 critic 梯度转化为 flow policy 的分步局部回归目标，避免多步去噪反向传播的不稳定性。

## Key Ideas

- Direct local evidence currently comes from [[wang2026while]].
- The concept is tracked with local tags: RL, flow-matching, policy-extraction.
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

- [[wang2026while]] (direct evidence): 提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...

## Evidence Map

- Direct evidence papers: [[wang2026while]].
- Broader local evidence context: [[wang2026while]], [[zhang2026prts]], [[jie2026omnivlarl]], [[ji2026recovering]], [[zhu2026nsvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[flow-matching-policy]]
- [[offline-to-online-rl]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wang2026while]]
- [[zhang2026prts]]
- [[jie2026omnivlarl]]
- [[ji2026recovering]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhang2026world2minecraft]]
