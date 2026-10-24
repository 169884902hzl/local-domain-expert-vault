---
title: "Point Bridge"
tags: [concept, sim-to-real, point-cloud, manipulation]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "利用 VLM 引导的自动化 3D 点云提取实现零样本 Sim-to-Real 策略迁移的框架"
---

## Definition

Point Bridge is maintained here as an evidence-linked concept. 利用 VLM 引导的自动化 3D 点云提取实现零样本 Sim-to-Real 策略迁移的框架

## Key Ideas

- Direct local evidence currently comes from [[chi2024diffusion]], [[haldar2026point]].
- The concept is tracked with local tags: concept, sim-to-real, point-cloud, manipulation.
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

- [[chi2024diffusion]] (direct evidence): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[haldar2026point]] (direct evidence): 利用 VLM 引导的自动化点云提取管线和统一的 3D 点表示，实现零样本 Sim-to-Real 策略迁移，在 6 个真实世界操控任务中比图像基线提升最高 66%。
- [[qureshi2025splatsim]] (broader context): 提出 SplatSim，用 3D Gaussian Splatting (3DGS) 替代传统 mesh 作为仿真渲染原语，实现 RGB manipulation polic...
- [[lips2024keypoints]] (broader context): 提出合成数据管线用于训练衣物关键点检测器。三阶段流程：程序化生成单层 mesh → Nvidia Flex 变形（模拟展开后状态）→ Blender Cycles 渲染。Ma...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[röfer2025pseudotouch]] (broader context): 提出 PseudoTouch，从深度图像预测低维触觉信号（ReSkin 15D），构建视觉-触觉跨模态映射。用 8 个基本几何体（球、圆柱、盒等）采集配对深度-触觉数据训练...

## Evidence Map

- Direct evidence papers: [[chi2024diffusion]], [[haldar2026point]].
- Broader local evidence context: [[chi2024diffusion]], [[haldar2026point]], [[qureshi2025splatsim]], [[lips2024keypoints]], [[yang2026ultradexgrasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[sim-to-real]]
- [[point-cloud]]
- [[pointing-representation]]
- [[vision-language-model]]
- [[sam2]]
- [[demonstration-synthesis]]

## Related Papers

- [[chi2024diffusion]]
- [[haldar2026point]]
- [[qureshi2025splatsim]]
- [[lips2024keypoints]]
- [[yang2026ultradexgrasp]]
- [[wu2025rlgsbridge]]
- [[sun2026maniparena]]
- [[röfer2025pseudotouch]]
