---
title: "6-DoF Pose Tracking"
tags: [concept]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "对未知物体进行实时 6 自由度位姿追踪，融合视觉特征匹配与物理模型预测"
---

## Definition

6-DoF Pose Tracking is maintained here as an evidence-linked concept. 对未知物体进行实时 6 自由度位姿追踪，融合视觉特征匹配与物理模型预测

## Key Ideas

- Direct local evidence currently comes from [[yang2026twintrack]].
- The concept is tracked with local tags: concept.
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

- [[yang2026twintrack]] (direct evidence): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[steen2024quadratic]] (broader context): 提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impac...
- [[kumar122constraining]] (broader context): 提出 COGIS 方法，在部分可观测环境中在线学习障碍物几何模型（GPIS）并通过约束优化精化数据集。利用名义动力学模型预测与实际状态差异推断接触点，结合视觉预处理/后处理清...
- [[karim2024davil]] (broader context): 提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[yang2026twintrack]].
- Broader local evidence context: [[yang2026twintrack]], [[zhang2026visionlanguageaction]], [[yang2026asyncshield]], [[steen2024quadratic]], [[kumar122constraining]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[real-to-sim]]
- [[sim-to-real]]
- [[contact-rich-manipulation]]
- [[gaussian-splatting]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[yang2026twintrack]]
- [[zhang2026visionlanguageaction]]
- [[yang2026asyncshield]]
- [[steen2024quadratic]]
- [[kumar122constraining]]
- [[karim2024davil]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
