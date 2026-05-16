---
title: "CTS Framework (Concurrent Teacher-Student)"
tags: [RL, teacher-student, locomotion]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "同时优化教师和学生网络的 actor-critic 的强化学习训练框架，比传统 teacher-student distillation 性能更好。"
---

## Definition

CTS Framework (Concurrent Teacher-Student) is maintained here as an evidence-linked concept. 同时优化教师和学生网络的 actor-critic 的强化学习训练框架，比传统 teacher-student distillation 性能更好。

## Key Ideas

- Direct local evidence currently comes from [[wu2026reliable]].
- The concept is tracked with local tags: RL, teacher-student, locomotion.
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

- [[wu2026reliable]] (direct evidence): 提出 MoE-CTS 统一框架，将 Mixture-of-Experts 集成到学生编码器以增强多地形表征，并设计 RoboGauge 预测评估套件，通过 sim-to-si...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...

## Evidence Map

- Direct evidence papers: [[wu2026reliable]].
- Broader local evidence context: [[wu2026reliable]], [[zhu2026nsvla]], [[zhou2026ego]], [[zhong2026vlaopd]], [[zhao2026visualtactile]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[mixture-of-experts]]
- [[sim-to-real]]
- [[domain-randomization]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wu2026reliable]]
- [[zhu2026nsvla]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[zhang2026recurrent]]
- [[yuan2026prefmoe]]
