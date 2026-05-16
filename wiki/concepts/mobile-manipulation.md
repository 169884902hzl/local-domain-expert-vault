---
title: "Mobile Manipulation"
tags: [concept, mobile-manipulation]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "移动操控——机器人同时执行导航和操控任务的能力，要求长时序、全身控制和空间记忆"
---

## Definition

Mobile Manipulation is maintained here as an evidence-linked concept. 移动操控——机器人同时执行导航和操控任务的能力，要求长时序、全身控制和空间记忆

## Key Ideas

- Direct local evidence currently comes from [[sun2026maniparena]].
- The concept is tracked with local tags: concept, mobile-manipulation.
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

- [[sun2026maniparena]] (direct evidence): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[ozdamar820pushing]] (broader context): 提出仅依赖触觉反馈的响应式推动策略（RPS），使移动机器人在无视觉和物体模型的情况下推动未知物体到目标位置。电容触觉传感器覆盖机器人底盘，通过接触位置自适应调整底盘运动。Lo...
- [[huang2026kinder]] (broader context): 提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP...

## Evidence Map

- Direct evidence papers: [[sun2026maniparena]].
- Broader local evidence context: [[sun2026maniparena]], [[zhi2025closedloop]], [[zhao2023finegrained]], [[zhang2026safevla]], [[xiao2026avavla]].
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
- [[loco-manipulation]]
- [[whole-body-control]]
- [[long-horizon-manipulation]]
- [[sim-to-real]]
- [[robot-learning]]

## Related Papers

- [[sun2026maniparena]]
- [[zhi2025closedloop]]
- [[zhao2023finegrained]]
- [[zhang2026safevla]]
- [[xiao2026avavla]]
- [[qiu2025wildlma]]
- [[ozdamar820pushing]]
- [[huang2026kinder]]
