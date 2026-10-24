---
title: "3D Gaussian Splatting"
tags: [3D-reconstruction, neural-rendering, simulation]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "基于 3D 高斯点的神经渲染技术，用显式高斯基元表示场景，实现实时高质量新视角合成。"
---

## Definition

3D Gaussian Splatting is maintained here as an evidence-linked concept. 基于 3D 高斯点的神经渲染技术，用显式高斯基元表示场景，实现实时高质量新视角合成。

## Key Ideas

- Direct local evidence currently comes from [[li2026affordsim]].
- The concept is tracked with local tags: 3D-reconstruction, neural-rendering, simulation.
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

- [[li2026affordsim]] (direct evidence): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[wang2026phys2real]] (broader context): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[qureshi2025splatsim]] (broader context): 提出 SplatSim，用 3D Gaussian Splatting (3DGS) 替代传统 mesh 作为仿真渲染原语，实现 RGB manipulation polic...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...

## Evidence Map

- Direct evidence papers: [[li2026affordsim]].
- Broader local evidence context: [[li2026affordsim]], [[yang2026twintrack]], [[wu2025rlgsbridge]], [[wang2026phys2real]], [[sun2026maniparena]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[domain-randomization]]
- [[sim-to-real]]
- [[point-cloud]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026affordsim]]
- [[yang2026twintrack]]
- [[wu2025rlgsbridge]]
- [[wang2026phys2real]]
- [[sun2026maniparena]]
- [[sakamoto2026e3vsbench]]
- [[qureshi2025splatsim]]
- [[jia2026gsplayground]]
