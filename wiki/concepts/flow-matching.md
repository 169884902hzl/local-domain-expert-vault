---
title: "Flow Matching"
tags: [generative-model, diffusion, imitation-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "通过学习概率路径的速度场将噪声分布变换为目标分布的生成建模方法，在机器人模仿学习中用作动作生成器。"
---

## Definition

Flow Matching is maintained here as an evidence-linked concept. 通过学习概率路径的速度场将噪声分布变换为目标分布的生成建模方法，在机器人模仿学习中用作动作生成器。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026generative]].
- The concept is tracked with local tags: generative-model, diffusion, imitation-learning.
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

- [[zhang2026generative]] (direct evidence): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[chen2025deformpam]] (broader context): 提出 DeformPAM 框架，通过偏好学习训练隐式 reward 模型，在推理时对扩散策略采样的多个候选动作进行 reward-guided 选择，在颗粒堆塑形、绳子塑形、...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[feng2026demystifying]] (broader context): 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[zhang2026generative]].
- Broader local evidence context: [[zhang2026generative]], [[wang2026discretertc]], [[xue2026tube]], [[chen2025deformpam]], [[jie2026omnivlarl]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[deformable-linear-object]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[grasping]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[planning]]
- [[sim-to-real]]
- [[tactile-sensing]]
## Related Papers

- [[chen2026elasticflow]]
- [[deshpande2026molmob0t]]
- [[he2026generative]]
- [[khan2026discrete]]
- [[lu2026unified]]
- [[patil2026youve]]
- [[wang2026stepnft]]
- [[yang2026hivla]]
- [[zhang2026forceflow]]
- [[ziakas2026aligning]]