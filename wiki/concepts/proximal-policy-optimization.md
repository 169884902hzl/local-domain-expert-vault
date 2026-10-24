---
title: "Proximal Policy Optimization"
tags: [concept, RL, on-policy]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "基于 trust-region 思想的 on-policy actor-critic 算法，通过 clipped surrogate objective 实现稳定策略更新"
---

## Definition

Proximal Policy Optimization is maintained here as an evidence-linked concept. 基于 trust-region 思想的 on-policy actor-critic 算法，通过 clipped surrogate objective 实现稳定策略更新

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: concept, RL, on-policy.
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

- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[liang2026vanim]] (broader context): VAnim 提出基于 Sparse State Update 的 LLM 框架实现文本驱动的 SVG 动画生成，通过 Identification-First Motion...
- [[karim2024davil]] (broader context): 提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[moroncelli2026jumpstart]], [[ziakas2026aligning]], [[zhou2026ego]], [[zhao2026rosclaw]], [[yu2026atrs]].
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
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[moroncelli2026jumpstart]]
- [[ziakas2026aligning]]
- [[zhou2026ego]]
- [[zhao2026rosclaw]]
- [[yu2026atrs]]
- [[wang2026evolvable]]
- [[liang2026vanim]]
- [[karim2024davil]]
