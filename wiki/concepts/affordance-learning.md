---
title: "Affordance Learning"
tags: [manipulation, vision, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "学习物体可供性（如可抓取点）的能力，对机器人操控中的动作选择和稳定性至关重要。"
---

## Definition

Affordance Learning is maintained here as an evidence-linked concept. 学习物体可供性（如可抓取点）的能力，对机器人操控中的动作选择和稳定性至关重要。

## Key Ideas

- Direct local evidence currently comes from [[zheng2026pokevla]].
- The concept is tracked with local tags: manipulation, vision, robot-learning.
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

- [[zheng2026pokevla]] (direct evidence): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...

## Evidence Map

- Direct evidence papers: [[zheng2026pokevla]].
- Broader local evidence context: [[zheng2026pokevla]], [[smith2024steer]], [[zhu2024scaling]], [[zhao2026visualtactile]], [[zhao2025polytouch]].
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
- [[imitation-learning]]
- [[spatial-grounding]]
- [[goal-aware-segmentation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zheng2026pokevla]]
- [[smith2024steer]]
- [[zhu2024scaling]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[xue2026tube]]
- [[wang2026evolvable]]
- [[shah2025acoustic]]
