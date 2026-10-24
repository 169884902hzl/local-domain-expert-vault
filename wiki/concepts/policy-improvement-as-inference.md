---
title: "Policy Improvement as Inference"
tags: [reinforcement-learning, policy-optimization, inference]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "将策略优化问题重新表述为概率推断问题，通过 EM 过程实现稳定的策略改进。"
---

## Definition

Policy Improvement as Inference is maintained here as an evidence-linked concept. 将策略优化问题重新表述为概率推断问题，通过 EM 过程实现稳定的策略改进。

## Key Ideas

- Direct local evidence currently comes from [[chen2026posterior]].
- The concept is tracked with local tags: reinforcement-learning, policy-optimization, inference.
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

- [[chen2026posterior]] (direct evidence): POCO 将生成式策略改进建模为免似然的 chunk 级后验推断问题，通过 Implicit E-M 和裁剪代理目标实现离线到在线的稳定高效微调，7 仿真 + 6 真实任务上...
- [[kuroki2025gendom]] (broader context): 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用...
- [[gao2026driftbased]] (broader context): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...

## Evidence Map

- Direct evidence papers: [[chen2026posterior]].
- Broader local evidence context: [[chen2026posterior]], [[kuroki2025gendom]], [[gao2026driftbased]], [[chi2024diffusion]], [[zhu2024scaling]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[offline-to-online-rl]]
- [[temporal-action-chunking]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[chen2026posterior]]
- [[kuroki2025gendom]]
- [[gao2026driftbased]]
- [[chi2024diffusion]]
- [[zhu2024scaling]]
- [[zhao2026rosclaw]]
- [[zhang2026touchguide]]
- [[zhang2026recurrent]]
