---
title: "Semantic Scene Graph"
tags: [scene-understanding, representation, graph]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "将场景中的物体和关系编码为图结构（节点=实体，边=关系），用于结构化场景理解和任务推理。"
---

## Definition

Semantic Scene Graph is maintained here as an evidence-linked concept. 将场景中的物体和关系编码为图结构（节点=实体，边=关系），用于结构化场景理解和任务推理。

## Key Ideas

- Direct local evidence currently comes from [[vo2026codegraphvlp]].
- The concept is tracked with local tags: scene-understanding, representation, graph.
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

- [[vo2026codegraphvlp]] (direct evidence): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[xie102multiview]] (broader context): 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[wang2023hierarchical]] (broader context): 提出 HCLM（Hierarchical policy for Cluttered-scene Long-horizon Manipulation），视觉层次化策略协调 pu...

## Evidence Map

- Direct evidence papers: [[vo2026codegraphvlp]].
- Broader local evidence context: [[vo2026codegraphvlp]], [[zhi102unifying]], [[zheng2026pokevla]], [[zhang2026visionlanguageaction]], [[zeng2026recapa]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[robotic-manipulation]]
- [[task-and-motion-planning]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]

## Related Papers

- [[vo2026codegraphvlp]]
- [[zhi102unifying]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
- [[zeng2026recapa]]
- [[xie102multiview]]
- [[wu2025rlgsbridge]]
- [[wang2023hierarchical]]
