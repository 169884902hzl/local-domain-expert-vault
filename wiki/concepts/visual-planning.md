---
title: "Visual Planning"
tags: [concept, planning, video-generation, robotics]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "利用视频生成模型合成未来帧序列作为机器人任务规划，通过逆动力学模型将视觉规划转化为可执行动作。"
---

## Definition

Visual Planning is maintained here as an evidence-linked concept. 利用视频生成模型合成未来帧序列作为机器人任务规划，通过逆动力学模型将视觉规划转化为可执行动作。

## Key Ideas

- Direct local evidence currently comes from [[luo2026selfimproving]].
- The concept is tracked with local tags: concept, planning, video-generation, robotics.
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

- [[luo2026selfimproving]] (direct evidence): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...

## Evidence Map

- Direct evidence papers: [[luo2026selfimproving]].
- Broader local evidence context: [[luo2026selfimproving]], [[zhang2026prts]], [[zeng2026recapa]], [[xu2026roboagent]], [[vo2026codegraphvlp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[video-generation]]
- [[imitation-learning]]
- [[planning]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[luo2026selfimproving]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[xu2026roboagent]]
- [[vo2026codegraphvlp]]
- [[sakamoto2026e3vsbench]]
- [[liu2026longhorizon]]
- [[iek2026coral]]
