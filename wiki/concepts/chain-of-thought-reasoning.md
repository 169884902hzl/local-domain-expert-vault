---
title: "Chain-of-Thought Reasoning"
tags: [reasoning, LLM, VLM]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "通过显式的中间推理步骤引导模型逐步解决问题的推理范式，广泛应用于 LLM 和 VLM 的复杂任务中。"
---

## Definition

Chain-of-Thought Reasoning is maintained here as an evidence-linked concept. 通过显式的中间推理步骤引导模型逐步解决问题的推理范式，广泛应用于 LLM 和 VLM 的复杂任务中。

## Key Ideas

- Direct local evidence currently comes from [[wang2026vlathinker]].
- The concept is tracked with local tags: reasoning, LLM, VLM.
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

- [[wang2026vlathinker]] (direct evidence): 首个\"thinking-with-image\"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRP...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[chen2026lastr1]] (broader context): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[brohan2023rt2]] (broader context): Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[li2026gazevla]] (broader context): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...

## Evidence Map

- Direct evidence papers: [[wang2026vlathinker]].
- Broader local evidence context: [[wang2026vlathinker]], [[zhang2026recurrent]], [[chen2026lastr1]], [[brohan2023rt2]], [[xu2026roboagent]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action-model]]
- [[GRPO]]
- [[thinking-with-image]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026vlathinker]]
- [[zhang2026recurrent]]
- [[chen2026lastr1]]
- [[brohan2023rt2]]
- [[xu2026roboagent]]
- [[li2026gazevla]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
