---
title: "Latent Diffusion Model"
tags: [concept, diffusion]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "在潜空间中进行去噪扩散的生成模型，通过自编码器压缩表示提高计算效率。"
---

## Definition

Latent Diffusion Model is maintained here as an evidence-linked concept. 在潜空间中进行去噪扩散的生成模型，通过自编码器压缩表示提高计算效率。

## Key Ideas

- Direct local evidence currently comes from [[wu2026affordgrasp]].
- The concept is tracked with local tags: concept, diffusion.
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

- [[wu2026affordgrasp]] (direct evidence): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...

## Evidence Map

- Direct evidence papers: [[wu2026affordgrasp]].
- Broader local evidence context: [[wu2026affordgrasp]], [[gu2026vistabot]], [[zhu2024scaling]], [[zhao2025polytouch]], [[zhang2026touchguide]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-policy]]
- [[classifier-guidance]]
- [[grasp-synthesis]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wu2026affordgrasp]]
- [[gu2026vistabot]]
- [[zhu2024scaling]]
- [[zhao2025polytouch]]
- [[zhang2026touchguide]]
- [[zhang2026handx]]
- [[zhang2026generative]]
- [[xue2026tube]]
