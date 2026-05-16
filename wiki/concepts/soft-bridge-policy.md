---
title: "Soft Bridge Policy"
tags: [reinforcement-learning, generative-model, policy-optimization]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "在 pre-tanh 潜空间中用 K 步轻量高斯残差转移构建随机桥的生成式策略，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，实现单次前向通过的动作生成。"
---

## Definition

Soft Bridge Policy is maintained here as an evidence-linked concept. 在 pre-tanh 潜空间中用 K 步轻量高斯残差转移构建随机桥的生成式策略，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，实现单次前向通过的动作生成。

## Key Ideas

- Direct local evidence currently comes from [[he2026generative]].
- The concept is tracked with local tags: reinforcement-learning, generative-model, policy-optimization.
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

- [[he2026generative]] (direct evidence): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[yang2026automated]] (broader context): 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...

## Evidence Map

- Direct evidence papers: [[he2026generative]].
- Broader local evidence context: [[he2026generative]], [[moroncelli2026jumpstart]], [[zhou2026sim1]], [[yuan2026prefmoe]], [[you2026dotsim]].
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
- [[diffusion-policy]]
- [[flow-matching]]
- [[max-entropy-rl]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[he2026generative]]
- [[moroncelli2026jumpstart]]
- [[zhou2026sim1]]
- [[yuan2026prefmoe]]
- [[you2026dotsim]]
- [[yang2026rise]]
- [[yang2026automated]]
- [[xue2026tube]]
