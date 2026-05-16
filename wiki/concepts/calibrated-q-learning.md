---
title: "Calibrated Q-Learning (Cal-QL)"
tags: [concept, RL, offline-rl]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "在 CQL 基础上添加校准下界，防止过度悲观导致在线微调不稳定"
---

## Definition

Calibrated Q-Learning (Cal-QL) is maintained here as an evidence-linked concept. 在 CQL 基础上添加校准下界，防止过度悲观导致在线微调不稳定

## Key Ideas

- Direct local evidence currently comes from [[choi2026rankq]].
- The concept is tracked with local tags: concept, RL, offline-rl.
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

- [[choi2026rankq]] (direct evidence): RankQ 通过自监督多排序损失在离线-在线 RL 中对动作施加结构化排序（成功 > 噪声 > 随机），取代 CQL/Cal-QL 的均匀 OOD 惩罚，在 D4RL 稀疏奖...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...

## Evidence Map

- Direct evidence papers: [[choi2026rankq]].
- Broader local evidence context: [[choi2026rankq]], [[zhou2026ego]], [[ziakas2026aligning]], [[zhu2026nsvla]], [[zhong2026vlaopd]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[conservative-q-learning]]
- [[offline-rl]]
- [[offline-to-online-rl]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[choi2026rankq]]
- [[zhou2026ego]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[zhang2026safevla]]
