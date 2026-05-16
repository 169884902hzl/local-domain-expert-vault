---
title: "Semantic-Contact Fields (SCFields)"
tags: [concept, tactile-sensing, manipulation, sim-to-real]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "统一 3D 表示，将视觉语义与密集外在接触概率和力估计融合到工具点云上，通过两阶段 Sim-to-Real 管线学习，实现类别级工具操控泛化。"
---

## Definition

Semantic-Contact Fields (SCFields) is maintained here as an evidence-linked concept. 统一 3D 表示，将视觉语义与密集外在接触概率和力估计融合到工具点云上，通过两阶段 Sim-to-Real 管线学习，实现类别级工具操控泛化。

## Key Ideas

- Direct local evidence currently comes from [[ma2026semanticcontact]].
- The concept is tracked with local tags: concept, tactile-sensing, manipulation, sim-to-real.
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

- [[ma2026semanticcontact]] (direct evidence): 提出 Semantic-Contact Fields（SCFields），将视觉语义与密集外在接触概率和力估计融合为统一 3D 表示，通过仿真预训练+真实世界伪标签对齐的两阶...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[huang2026flexitac]] (broader context): 提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-...

## Evidence Map

- Direct evidence papers: [[ma2026semanticcontact]].
- Broader local evidence context: [[ma2026semanticcontact]], [[yan2026tac2real]], [[sun2026maniparena]], [[iek2026coral]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[visual-tactile-fusion]]
- [[sim-to-real]]
- [[tactile-sensing]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[ma2026semanticcontact]]
- [[yan2026tac2real]]
- [[sun2026maniparena]]
- [[iek2026coral]]
- [[zhou2025oneshot]]
- [[luijkx2026llmguided]]
- [[jia2026gsplayground]]
- [[huang2026flexitac]]
