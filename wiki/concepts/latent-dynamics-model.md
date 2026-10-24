---
title: "Latent Dynamics Model"
tags: [world-model, latent-representation, dynamics-learning]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "在隐空间中学习环境动力学模型，预测未来隐状态而非原始观测，降低计算成本并提高泛化能力。"
---

## Definition

Latent Dynamics Model is maintained here as an evidence-linked concept. 在隐空间中学习环境动力学模型，预测未来隐状态而非原始观测，降低计算成本并提高泛化能力。

## Key Ideas

- Direct local evidence currently comes from [[levy2026simulation]].
- The concept is tracked with local tags: world-model, latent-representation, dynamics-learning.
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

- [[levy2026simulation]] (direct evidence): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[chen2026lastr1]] (broader context): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...

## Evidence Map

- Direct evidence papers: [[levy2026simulation]].
- Broader local evidence context: [[levy2026simulation]], [[missal2026ropedreamer]], [[chen2026lastr1]], [[zhou2026sim1]], [[zhang2026handx]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[world-model]]
- [[model-predictive-control]]
- [[MPPI]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[levy2026simulation]]
- [[missal2026ropedreamer]]
- [[chen2026lastr1]]
- [[zhou2026sim1]]
- [[zhang2026handx]]
- [[yuan2026prefmoe]]
- [[you2026dotsim]]
- [[yang2026rise]]
