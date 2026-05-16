---
title: "DiT (Diffusion Transformer)"
tags: [architecture, diffusion, transformer]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "以 Transformer 替代 U-Net 作为去噪主干的扩散模型架构，通过 AdaLN 注入时间条件。"
---

## Definition

DiT (Diffusion Transformer) is maintained here as an evidence-linked concept. 以 Transformer 替代 U-Net 作为去噪主干的扩散模型架构，通过 AdaLN 注入时间条件。

## Key Ideas

- Direct local evidence currently comes from [[chen2026elasticflow]].
- The concept is tracked with local tags: architecture, diffusion, transformer.
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

- [[chen2026elasticflow]] (direct evidence): 基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...

## Evidence Map

- Direct evidence papers: [[chen2026elasticflow]].
- Broader local evidence context: [[chen2026elasticflow]], [[zhu2024scaling]], [[zhang2026touchguide]], [[zhang2026handx]], [[zhang2026generative]].
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
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[chen2026elasticflow]]
- [[zhu2024scaling]]
- [[zhang2026touchguide]]
- [[zhang2026handx]]
- [[zhang2026generative]]
- [[yang2026hivla]]
- [[xue2026tube]]
- [[xia2024cage]]
