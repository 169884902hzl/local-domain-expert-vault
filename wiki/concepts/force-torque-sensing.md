---
title: "Force/Torque Sensing"
tags: [sensing, manipulation, tactile]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "通过力/力矩传感器获取末端执行器与环境的接触力信息，用于接触丰富操控中的力反馈闭环控制。"
---

## Definition

Force/Torque Sensing is maintained here as an evidence-linked concept. 通过力/力矩传感器获取末端执行器与环境的接触力信息，用于接触丰富操控中的力反馈闭环控制。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: sensing, manipulation, tactile.
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

- [[zhang2026forceflow]] (broader context): 基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（V...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[he2026exploratory]] (broader context): 提出 Exploratory and Focused Manipulation (EFM) 问题定义，构建 10 任务基准 EFM-10，设计双臂主动感知策略 BAP——利用...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zhang2026forceflow]], [[xu2026fingereye]], [[zhao2026visualtactile]], [[niu2026versatile]], [[he2026exploratory]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[tactile-sensing]]
- [[contact-rich-manipulation]]
- [[modal-masking]]
- [[hybrid-force-position-control]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[zhang2026forceflow]]
- [[xu2026fingereye]]
- [[zhao2026visualtactile]]
- [[niu2026versatile]]
- [[he2026exploratory]]
- [[zhao2026vitactracing]]
- [[yan2026tac2real]]
- [[zheng120dottip]]
