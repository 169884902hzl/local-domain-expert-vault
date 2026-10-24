---
title: "Flow Matching Policy"
tags: [generative-model, flow-matching, policy]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "基于 flow matching 的生成式策略，通过学习向量场将噪声映射到动作分布，用于 VLA 的动作生成。"
---

## Definition

Flow Matching Policy is maintained here as an evidence-linked concept. 基于 flow matching 的生成式策略，通过学习向量场将噪声映射到动作分布，用于 VLA 的动作生成。

## Key Ideas

- Direct local evidence currently comes from [[wang2026while]].
- The concept is tracked with local tags: generative-model, flow-matching, policy.
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

- [[wang2026while]] (direct evidence): 提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[feng2026demystifying]] (broader context): 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...

## Evidence Map

- Direct evidence papers: [[wang2026while]].
- Broader local evidence context: [[wang2026while]], [[zhang2026touchguide]], [[zhang2026generative]], [[wang2026discretertc]], [[jie2026omnivlarl]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[adjoint-matching]]
- [[vla]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026while]]
- [[zhang2026touchguide]]
- [[zhang2026generative]]
- [[wang2026discretertc]]
- [[jie2026omnivlarl]]
- [[ji2026recovering]]
- [[feng2026demystifying]]
- [[aida2026cortex]]
