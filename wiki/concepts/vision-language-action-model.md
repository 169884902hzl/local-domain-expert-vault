---
title: "Vision-Language-Action Model (VLA)"
tags: [VLA, manipulation, robot-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "统一视觉感知、语言理解和机器人动作执行的端到端模型范式，是具身智能的核心架构方向。"
---

## Definition

Vision-Language-Action Model (VLA) is maintained here as an evidence-linked concept. 统一视觉感知、语言理解和机器人动作执行的端到端模型范式，是具身智能的核心架构方向。

## Key Ideas

- Direct local evidence currently comes from [[wang2026vlathinker]].
- The concept is tracked with local tags: VLA, manipulation, robot-learning.
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
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。

## Evidence Map

- Direct evidence papers: [[wang2026vlathinker]].
- Broader local evidence context: [[wang2026vlathinker]], [[zhong2026vlaopd]], [[zheng2026pokevla]], [[zhang2026visionlanguageaction]], [[zhang2026prts]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[chain-of-thought-reasoning]]
- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[robot-learning]]

## Related Papers

- [[wang2026vlathinker]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
- [[yuan2026embodiedr1]]
- [[xu2026token]]
