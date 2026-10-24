---
title: "Equivariant Reinforcement Learning"
tags: [RL, equivariance, symmetry]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "利用群对称性作为归纳偏置提升 RL 样本效率的方法族，通过等变网络结构约束策略/值函数。"
---

## Definition

Equivariant Reinforcement Learning is maintained here as an evidence-linked concept. 利用群对称性作为归纳偏置提升 RL 样本效率的方法族，通过等变网络结构约束策略/值函数。

## Key Ideas

- Direct local evidence currently comes from [[chang2026partially]].
- The concept is tracked with local tags: RL, equivariance, symmetry.
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

- [[chang2026partially]] (direct evidence): 提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 IC...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...

## Evidence Map

- Direct evidence papers: [[chang2026partially]].
- Broader local evidence context: [[chang2026partially]], [[zhu2026nsvla]], [[zhong2026vlaopd]], [[zhao2026visualtactile]], [[zhang2026safevla]].
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
- [[robotic-manipulation]]
- [[Sim-to-Real]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[chang2026partially]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhang2026safevla]]
- [[zhang2026recurrent]]
- [[zhang2026prts]]
- [[zhang2021dair]]
