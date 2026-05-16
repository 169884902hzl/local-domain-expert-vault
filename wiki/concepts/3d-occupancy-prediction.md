---
title: "3D Occupancy Prediction"
tags: [3d-vision, scene-understanding]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "从 2D 图像预测场景的 3D 体素级语义占据网格，用于场景理解和仿真重建。"
---

## Definition

3D Occupancy Prediction is maintained here as an evidence-linked concept. 从 2D 图像预测场景的 3D 体素级语义占据网格，用于场景理解和仿真重建。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026world2minecraft]].
- The concept is tracked with local tags: 3d-vision, scene-understanding.
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

- [[zhang2026world2minecraft]] (direct evidence): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...
- [[wang2025implicit]] (broader context): 提出 IPA（Implicit Physics-Aware Policy），用于通过柔性工具（软体绳索）动态操控刚性物体。核心创新是隐式物理感知：通过短时动作观测推断系统物理...

## Evidence Map

- Direct evidence papers: [[zhang2026world2minecraft]].
- Broader local evidence context: [[zhang2026world2minecraft]], [[zhang2026prts]], [[zhu2024scaling]], [[zeng2026recapa]], [[yang2026asyncshield]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[semantic-scene-completion]]
- [[sim-to-real]]
- [[minecraft-simulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhang2026world2minecraft]]
- [[zhang2026prts]]
- [[zhu2024scaling]]
- [[zeng2026recapa]]
- [[yang2026asyncshield]]
- [[xia2024cage]]
- [[wu2025imperfect]]
- [[wang2025implicit]]
