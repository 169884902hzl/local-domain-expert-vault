---
title: "DLO Manipulation"
tags: [DLO, manipulation, deformable-object]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "可变形线性物体（Deformable Linear Object）操控，涉及绳索、线缆、布料等柔性物体的机器人抓取、弯折、缠绕等操作。"
---

## Definition

DLO Manipulation is maintained here as an evidence-linked concept. 可变形线性物体（Deformable Linear Object）操控，涉及绳索、线缆、布料等柔性物体的机器人抓取、弯折、缠绕等操作。

## Key Ideas

- Direct local evidence currently comes from [[yang2026rise]].
- The concept is tracked with local tags: DLO, manipulation, deformable-object.
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

- [[yang2026rise]] (direct evidence): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[team2024octo]] (broader context): UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持...
- [[moletta2026preference]] (broader context): 提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trouser...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[li2025routing]] (broader context): 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle...
- [[kuroki2025gendom]] (broader context): 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用...

## Evidence Map

- Direct evidence papers: [[yang2026rise]].
- Broader local evidence context: [[yang2026rise]], [[xu2026fingereye]], [[team2024octo]], [[moletta2026preference]], [[mitrano2024grasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[yang2026rise]]
- [[xu2026fingereye]]
- [[team2024octo]]
- [[moletta2026preference]]
- [[mitrano2024grasp]]
- [[missal2026ropedreamer]]
- [[li2025routing]]
- [[kuroki2025gendom]]
