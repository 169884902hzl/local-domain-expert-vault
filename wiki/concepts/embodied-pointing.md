---
title: "Embodied Pointing"
tags: [manipulation, VLM, pointing]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "具身指向能力：REG、RRG、OFG、VTG 四种基于点坐标的机器人操控感知能力。"
---

## Definition

Embodied Pointing is maintained here as an evidence-linked concept. 具身指向能力：REG、RRG、OFG、VTG 四种基于点坐标的机器人操控感知能力。

## Key Ideas

- Direct local evidence currently comes from [[yuan2026embodiedr1]].
- The concept is tracked with local tags: manipulation, VLM, pointing.
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

- [[yuan2026embodiedr1]] (direct evidence): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...

## Evidence Map

- Direct evidence papers: [[yuan2026embodiedr1]].
- Broader local evidence context: [[yuan2026embodiedr1]], [[zheng2026pokevla]], [[zhang2026prts]], [[zhang2026joyaira]], [[xiao2026avavla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[pointing-representation]]
- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[yuan2026embodiedr1]]
- [[zheng2026pokevla]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
- [[xiao2026avavla]]
- [[wang2026evolvable]]
- [[smith2024steer]]
- [[liu2026longhorizon]]
