---
title: "Gauss Code"
tags: [topology, knot-theory, evaluation-metric]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "基于交叉点的有符号整数序列，用于量化 DLO 拓扑一致性的数值表示方法。"
---

## Definition

Gauss Code is maintained here as an evidence-linked concept. 基于交叉点的有符号整数序列，用于量化 DLO 拓扑一致性的数值表示方法。

## Key Ideas

- Direct local evidence currently comes from [[missal2026ropedreamer]].
- The concept is tracked with local tags: topology, knot-theory, evaluation-metric.
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

- [[missal2026ropedreamer]] (direct evidence): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[giacomuzzo2024blackbox]] (broader context): 提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagr...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...

## Evidence Map

- Direct evidence papers: [[missal2026ropedreamer]].
- Broader local evidence context: [[missal2026ropedreamer]], [[giacomuzzo2024blackbox]], [[zheng2026pokevla]], [[zhao2026visualtactile]], [[zhao2023finegrained]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[missal2026ropedreamer]]
- [[giacomuzzo2024blackbox]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhao2023finegrained]]
- [[zhang2026generative]]
- [[xu2026fingereye]]
- [[wu2025rlgsbridge]]
