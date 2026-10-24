---
title: "Action Space Design"
tags: [manipulation, imitation-learning, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "定义机器人策略输出动作的表示方式，沿空间轴（joint vs task space）和时间轴（absolute vs delta）分解，直接影响策略可学习性和控制稳定性。"
---

## Definition

Action Space Design is maintained here as an evidence-linked concept. 定义机器人策略输出动作的表示方式，沿空间轴（joint vs task space）和时间轴（absolute vs delta）分解，直接影响策略可学习性和控制稳定性。

## Key Ideas

- Direct local evidence currently comes from [[feng2026demystifying]].
- The concept is tracked with local tags: manipulation, imitation-learning, robot-learning.
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

- [[feng2026demystifying]] (direct evidence): 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[huang2026kinder]] (broader context): 提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[team2024octo]] (broader context): UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持...

## Evidence Map

- Direct evidence papers: [[feng2026demystifying]].
- Broader local evidence context: [[feng2026demystifying]], [[zheng2026pokevla]], [[zhao2026visualtactile]], [[zhao2025polytouch]], [[smith2024steer]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-chunking]]
- [[imitation-learning]]
- [[flow-matching]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[feng2026demystifying]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[smith2024steer]]
- [[huang2026kinder]]
- [[chi2024diffusion]]
- [[team2024octo]]
