---
title: "Video Language Model"
tags: [concept, VLM, video]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "能够理解和推理视频内容的大规模视觉-语言模型，是 VLM 在视频模态上的扩展。"
---

## Definition

Video Language Model is maintained here as an evidence-linked concept. 能够理解和推理视频内容的大规模视觉-语言模型，是 VLM 在视频模态上的扩展。

## Key Ideas

- Direct local evidence currently comes from [[jiang2026videop2r]].
- The concept is tracked with local tags: concept, VLM, video.
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

- [[jiang2026videop2r]] (direct evidence): 提出 VideoP2R 框架，将视频推理显式分解为感知和推理两个独立过程，通过三步 CoT 管线构建 162K 过程感知数据集，并设计 PA-GRPO 算法为两个过程分别提供...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[li2026h2r]] (broader context): H2R 通过 HaMeR+SAM+LaMa 管线将第一人称人类手部视频替换为机器人手臂渲染帧，缩小人机视觉域差异，在仿真和真实双臂/灵巧手操控任务上实现 1.3%-23.3%...
- [[garcia2025generalizable]] (broader context): 提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任...

## Evidence Map

- Direct evidence papers: [[jiang2026videop2r]].
- Broader local evidence context: [[jiang2026videop2r]], [[zhang2026recurrent]], [[zhang2026joyaira]], [[zhang2026generative]], [[xie2026humanintention]].
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
- [[visual-reinforcement-learning]]
- [[reinforcement-fine-tuning]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[jiang2026videop2r]]
- [[zhang2026recurrent]]
- [[zhang2026joyaira]]
- [[zhang2026generative]]
- [[xie2026humanintention]]
- [[wang2026visionlanguageaction]]
- [[li2026h2r]]
- [[garcia2025generalizable]]
