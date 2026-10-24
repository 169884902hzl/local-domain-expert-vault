---
title: "Hand-Object Interaction (HOI)"
tags: [concept, 3d-vision, manipulation]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "手-物体交互，研究手与物体之间的 3D 几何关系、接触状态和运动轨迹的建模与重建"
---

## Definition

Hand-Object Interaction (HOI) is maintained here as an evidence-linked concept. 手-物体交互，研究手与物体之间的 3D 几何关系、接触状态和运动轨迹的建模与重建

## Key Ideas

- Direct local evidence currently comes from [[shi2026agile]].
- The concept is tracked with local tags: concept, 3d-vision, manipulation.
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

- [[shi2026agile]] (direct evidence): 提出 VLM 引导的 agentic 生成管线，从单目视频重建手-物体交互的水密网格和 6D 轨迹，用 anchor-and-track 策略替代脆弱的 SfM 初始化，实现...
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[wang2026ocra]] (broader context): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[singh2025handobject]] (broader context): 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目...
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[karim2024davil]] (broader context): 提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[huang2026kinder]] (broader context): 提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP...

## Evidence Map

- Direct evidence papers: [[shi2026agile]].
- Broader local evidence context: [[shi2026agile]], [[yang2026twintrack]], [[wang2026ocra]], [[singh2025handobject]], [[li2026affordsim]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[DLO-manipulation]]
- [[contact-rich-manipulation]]
- [[sim-to-real]]
- [[3d-generation]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[shi2026agile]]
- [[yang2026twintrack]]
- [[wang2026ocra]]
- [[singh2025handobject]]
- [[li2026affordsim]]
- [[karim2024davil]]
- [[iek2026coral]]
- [[huang2026kinder]]
