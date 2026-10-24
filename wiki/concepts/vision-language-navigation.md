---
title: "Vision-Language Navigation"
tags: [vlm, embodied-ai, navigation]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "智能体根据自然语言指令在视觉环境中进行导航，是具身 AI 核心任务。"
---

## Definition

Vision-Language Navigation is maintained here as an evidence-linked concept. 智能体根据自然语言指令在视觉环境中进行导航，是具身 AI 核心任务。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026world2minecraft]].
- The concept is tracked with local tags: vlm, embodied-ai, navigation.
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
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...

## Evidence Map

- Direct evidence papers: [[zhang2026world2minecraft]].
- Broader local evidence context: [[zhang2026world2minecraft]], [[zhi2025closedloop]], [[yang2026asyncshield]], [[jeong2026your]], [[zheng2026pokevla]].
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
- [[minecraft-simulation]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhang2026world2minecraft]]
- [[zhi2025closedloop]]
- [[yang2026asyncshield]]
- [[jeong2026your]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
