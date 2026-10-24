---
title: "Diffusion Transformer (DiT)"
tags: [diffusion, transformer, action-generation]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "将扩散模型与 Transformer 架构结合的生成模型，广泛用于图像生成和机器人动作序列生成。"
---

## Definition

Diffusion Transformer (DiT) is maintained here as an evidence-linked concept. 将扩散模型与 Transformer 架构结合的生成模型，广泛用于图像生成和机器人动作序列生成。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: diffusion, transformer, action-generation.
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

- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[keunknowndiffuser]] (broader context): 提出 3D Diffuser Actor，统一 3D 场景表示与扩散目标用于模仿学习。核心是 3D 相对去噪 Transformer：将 RGB-D 图像提升为 3D 场景...
- [[han2026stereopolicy]] (broader context): 提出 StereoPolicy 框架，通过 Stereo Transformer 融合双目图像对实现隐式 3D 几何推理，无需显式 3D 重建，在扩散策略和 VLA 模型上均...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[chen2026craft]] (broader context): 提出 CRAFT 框架，利用 Canny 边缘引导视频扩散模型（Wan2.1）从仿真轨迹生成七维度多样化的双臂操控训练数据（物体位姿/光照/颜色/背景/跨具身/视角/腕部+第...
- [[chen2026abotphysworld]] (broader context): 基于 Wan2.1 的 14B Diffusion Transformer，通过 300 万物理标注操控视频 SFT + VLM 解耦判别器 DPO 后训练，实现物理一致的可...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zhu2024scaling]], [[yang2026hivla]], [[keunknowndiffuser]], [[han2026stereopolicy]], [[chi2024diffusion]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[flow-matching]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhu2024scaling]]
- [[yang2026hivla]]
- [[keunknowndiffuser]]
- [[han2026stereopolicy]]
- [[chi2024diffusion]]
- [[chen2026craft]]
- [[chen2026abotphysworld]]
- [[zhou2026sim1]]
