---
title: "Recurrent Reasoning"
tags: [VLM, reasoning, embodied-ai]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "模型对输入序列进行迭代推理，每轮基于上轮推理结果更新输出，适用于长时序任务。"
---

## Definition

Recurrent Reasoning is maintained here as an evidence-linked concept. 模型对输入序列进行迭代推理，每轮基于上轮推理结果更新输出，适用于长时序任务。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026recurrent]].
- The concept is tracked with local tags: VLM, reasoning, embodied-ai.
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

- [[zhang2026recurrent]] (direct evidence): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...

## Evidence Map

- Direct evidence papers: [[zhang2026recurrent]].
- Broader local evidence context: [[zhang2026recurrent]], [[xiao2026avavla]], [[iek2026coral]], [[zhi2025closedloop]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[chain-of-thought]]
- [[task-progress-estimation]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhang2026recurrent]]
- [[xiao2026avavla]]
- [[iek2026coral]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
- [[zhang2026prts]]
- [[zhang2026handx]]
- [[yuan2026embodiedr1]]
