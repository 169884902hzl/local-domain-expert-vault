---
title: "Diffusion Steering Reinforcement Learning (DSRL)"
tags: [reinforcement-learning, diffusion-model, policy-optimization]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "一种 offline-to-online RL 方法，冻结预训练扩散策略权重，仅通过优化扩散模型的初始噪声来提升任务表现，同时保持人类似行为流形。"
---

## Definition

Diffusion Steering Reinforcement Learning (DSRL) is maintained here as an evidence-linked concept. 一种 offline-to-online RL 方法，冻结预训练扩散策略权重，仅通过优化扩散模型的初始噪声来提升任务表现，同时保持人类似行为流形。

## Key Ideas

- Direct local evidence currently comes from [[xu2026expertgen]].
- The concept is tracked with local tags: reinforcement-learning, diffusion-model, policy-optimization.
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

- [[xu2026expertgen]] (direct evidence): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...

## Evidence Map

- Direct evidence papers: [[xu2026expertgen]].
- Broader local evidence context: [[xu2026expertgen]], [[zhang2026touchguide]], [[zhu2024scaling]], [[zhao2025polytouch]], [[zhao2023finegrained]].
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
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[diffusion-policy]]
- [[behavior-prior]]
- [[robotic-manipulation]]

## Related Papers

- [[xu2026expertgen]]
- [[zhang2026touchguide]]
- [[zhu2024scaling]]
- [[zhao2025polytouch]]
- [[zhao2023finegrained]]
- [[zhang2026generative]]
- [[xue2026tube]]
- [[xia2024cage]]
