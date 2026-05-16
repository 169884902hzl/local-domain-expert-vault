---
title: "Observation Aliasing"
tags: [concept, pomdp, imitation-learning]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "POMDP 中不同隐状态产生相同观测的现象，导致纯观测策略无法区分，需要历史信息来消歧。"
---

## Definition

Observation Aliasing is maintained here as an evidence-linked concept. POMDP 中不同隐状态产生相同观测的现象，导致纯观测策略无法区分，需要历史信息来消歧。

## Key Ideas

- Direct local evidence currently comes from [[guan2026dssp]].
- The concept is tracked with local tags: concept, pomdp, imitation-learning.
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

- [[guan2026dssp]] (direct evidence): 提出基于 Mamba SSM 的全历史编码扩散策略 DSSP，通过因果历史编码器和动力学感知辅助损失压缩长时序观测历史，以层级前缀条件机制融合历史上下文与近期状态进行动作去噪...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: [[guan2026dssp]].
- Broader local evidence context: [[guan2026dssp]], [[zhu2024scaling]], [[zhou2026sim1]], [[zhou2026ego]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[long-horizon-manipulation]]
- [[recurrent-state-space-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[guan2026dssp]]
- [[zhu2024scaling]]
- [[zhou2026sim1]]
- [[zhou2026ego]]
- [[zhou2025oneshot]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[zhao2025polytouch]]
