---
title: "Semantic Scene Completion"
tags: [3d-vision, scene-understanding]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "同时完成 3D 场景的几何补全和语义标注，是占据预测的关联任务。"
---

## Definition

Semantic Scene Completion is maintained here as an evidence-linked concept. 同时完成 3D 场景的几何补全和语义标注，是占据预测的关联任务。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026world2minecraft]].
- The concept is tracked with local tags: 3d-vision, scene-understanding.
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

- [[zhang2026world2minecraft]] (direct evidence): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...

## Evidence Map

- Direct evidence papers: [[zhang2026world2minecraft]].
- Broader local evidence context: [[zhang2026world2minecraft]], [[wu2025rlgsbridge]], [[vo2026codegraphvlp]], [[zhi102unifying]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[3d-occupancy-prediction]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhang2026world2minecraft]]
- [[wu2025rlgsbridge]]
- [[vo2026codegraphvlp]]
- [[zhi102unifying]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
