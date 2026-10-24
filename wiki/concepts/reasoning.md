---
title: "Reasoning"
tags: [concept]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "模型执行多步骤逻辑推导以解决复杂问题的能力，涵盖数学推理、逻辑推理、规划推理等，是 LLM/dLLM 后训练的关键能力。"
---

## Definition

Reasoning is maintained here as an evidence-linked concept. 模型执行多步骤逻辑推导以解决复杂问题的能力，涵盖数学推理、逻辑推理、规划推理等，是 LLM/dLLM 后训练的关键能力。

## Key Ideas

- Direct local evidence currently comes from [[jiang2026break]].
- The concept is tracked with local tags: concept.
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

- [[jiang2026break]] (direct evidence): 提出 b1 框架，通过 RL 学习动态大小的推理块并施加单调熵下降约束，解决扩散语言模型中固定大小分块破坏推理连贯性的问题，在数学推理基准上相比固定分块基线最高提升 19.53%。
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...

## Evidence Map

- Direct evidence papers: [[jiang2026break]].
- Broader local evidence context: [[jiang2026break]], [[zhou2026ego]], [[zhi2025closedloop]], [[zheng2026pokevla]], [[zhao2026rosclaw]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-language-model]]
- [[reinforcement-learning]]
- [[chain-of-thought]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jiang2026break]]
- [[zhou2026ego]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
- [[zhao2026rosclaw]]
- [[zhang2026recurrent]]
- [[zhang2026prts]]
- [[zhang2026handx]]
