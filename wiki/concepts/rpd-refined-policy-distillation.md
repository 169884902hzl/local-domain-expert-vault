---
title: "Refined Policy Distillation (RPD)"
tags: [distillation, VLA, RL, policy-transfer]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "从 VLA 通用模型到 RL 专家的策略蒸馏方法，通过持续动作匹配损失将 VLA 知识迁移到 RL 策略。"
---

## Definition

Refined Policy Distillation (RPD) is maintained here as an evidence-linked concept. 从 VLA 通用模型到 RL 专家的策略蒸馏方法，通过持续动作匹配损失将 VLA 知识迁移到 RL 策略。

## Key Ideas

- Direct local evidence currently comes from [[moroncelli2026jumpstart]].
- The concept is tracked with local tags: distillation, VLA, RL, policy-transfer.
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

- [[moroncelli2026jumpstart]] (direct evidence): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。

## Evidence Map

- Direct evidence papers: [[moroncelli2026jumpstart]].
- Broader local evidence context: [[moroncelli2026jumpstart]], [[zhong2026vlaopd]], [[zhou2026ego]], [[zhao2026visualtactile]], [[zhao2026rosclaw]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[ppo]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[moroncelli2026jumpstart]]
- [[zhong2026vlaopd]]
- [[zhou2026ego]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[zhang2026recurrent]]
- [[yuan2026prefmoe]]
- [[yu2026atrs]]
