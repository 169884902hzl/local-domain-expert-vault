---
title: "Contact-Rich Manipulation"
tags: [concept, manipulation, control]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "需要精确调控外部接触力的机器人操控任务，成功不仅依赖几何碰撞避免，还取决于对接触力的主动管理。"
---

## Definition

Contact-Rich Manipulation is maintained here as an evidence-linked concept. 需要精确调控外部接触力的机器人操控任务，成功不仅依赖几何碰撞避免，还取决于对接触力的主动管理。

## Key Ideas

- Direct local evidence currently comes from [[iek2026coral]].
- The concept is tracked with local tags: concept, manipulation, control.
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

- [[iek2026coral]] (direct evidence): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...

## Evidence Map

- Direct evidence papers: [[iek2026coral]].
- Broader local evidence context: [[iek2026coral]], [[zhou2025oneshot]], [[zhao2025polytouch]], [[zhang2026touchguide]], [[zhang2026prts]].
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
- [[mppi]]
- [[tactile-sensing]]
- [[force-control]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[iek2026coral]]
- [[zhou2025oneshot]]
- [[zhao2025polytouch]]
- [[zhang2026touchguide]]
- [[zhang2026prts]]
- [[yan2026tac2real]]
- [[xue2026tube]]
- [[sun2026maniparena]]
