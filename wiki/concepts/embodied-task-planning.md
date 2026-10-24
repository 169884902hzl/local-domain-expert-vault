---
title: "Embodied Task Planning"
tags: [planning, embodied-ai, VLM]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "具身任务规划：智能体通过视觉观察和原子动作与环境交互，完成用户指定复杂任务的规划问题。"
---

## Definition

Embodied Task Planning is maintained here as an evidence-linked concept. 具身任务规划：智能体通过视觉观察和原子动作与环境交互，完成用户指定复杂任务的规划问题。

## Key Ideas

- Direct local evidence currently comes from [[xu2026roboagent]].
- The concept is tracked with local tags: planning, embodied-ai, VLM.
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

- [[xu2026roboagent]] (direct evidence): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...

## Evidence Map

- Direct evidence papers: [[xu2026roboagent]].
- Broader local evidence context: [[xu2026roboagent]], [[zhang2026prts]], [[zeng2026recapa]], [[sakamoto2026e3vsbench]], [[liu2026longhorizon]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[task-and-motion-planning]]
- [[vision-language-model]]
- [[planning]]
- [[chain-of-thought]]
- [[dagger]]
- [[robotic-manipulation]]

## Related Papers

- [[xu2026roboagent]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[sakamoto2026e3vsbench]]
- [[liu2026longhorizon]]
- [[vo2026codegraphvlp]]
- [[luijkx2026llmguided]]
- [[iek2026coral]]
