---
title: "Steering Policy"
tags: [concept, diffusion-policy, latent-control]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "通过控制预训练生成策略的潜在噪声输入来偏置生成行为的策略，不修改原策略权重。"
---

## Definition

Steering Policy is maintained here as an evidence-linked concept. 通过控制预训练生成策略的潜在噪声输入来偏置生成行为的策略，不修改原策略权重。

## Key Ideas

- Direct local evidence currently comes from [[longhini2026behavioral]].
- The concept is tracked with local tags: concept, diffusion-policy, latent-control.
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

- [[longhini2026behavioral]] (direct evidence): 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[lu2026unified]] (broader context): UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[longhini2026behavioral]].
- Broader local evidence context: [[longhini2026behavioral]], [[zhang2026touchguide]], [[xu2026expertgen]], [[lu2026unified]], [[ziakas2026aligning]].
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
- [[diffusion-steering]]
- [[behavioral-mode-discovery]]
- [[behavior-prior]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[longhini2026behavioral]]
- [[zhang2026touchguide]]
- [[xu2026expertgen]]
- [[lu2026unified]]
- [[ziakas2026aligning]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
