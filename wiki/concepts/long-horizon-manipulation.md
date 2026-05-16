---
title: "Long-Horizon Manipulation"
tags: [manipulation, planning, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "长时序操控，需要机器人执行多步、状态依赖且对累积误差鲁棒的复杂任务序列。"
---

## Definition

Long-Horizon Manipulation is maintained here as an evidence-linked concept. 长时序操控，需要机器人执行多步、状态依赖且对累积误差鲁棒的复杂任务序列。

## Key Ideas

- Direct local evidence currently comes from [[liu2026longhorizon]].
- The concept is tracked with local tags: manipulation, planning, robot-learning.
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

- [[liu2026longhorizon]] (direct evidence): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[feng2026demystifying]] (broader context): 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真...
- [[dai2024racer]] (broader context): 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GP...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...

## Evidence Map

- Direct evidence papers: [[liu2026longhorizon]].
- Broader local evidence context: [[liu2026longhorizon]], [[vo2026codegraphvlp]], [[feng2026demystifying]], [[dai2024racer]], [[aida2026cortex]].
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
- [[planning]]
- [[imitation-learning]]
- [[vision-language-action]]
- [[visual-trace]]
- [[robot-learning]]

## Related Papers

- [[liu2026longhorizon]]
- [[vo2026codegraphvlp]]
- [[feng2026demystifying]]
- [[dai2024racer]]
- [[aida2026cortex]]
- [[gu2026vistabot]]
- [[zhao2025polytouch]]
- [[zeng2026recapa]]
