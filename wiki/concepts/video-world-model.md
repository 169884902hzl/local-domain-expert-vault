---
title: "Video World Model"
tags: [concept, world-model, video-generation]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "基于视频扩散模型学习环境动力学，通过生成未来视频帧预测动作结果，用于策略优化和规划。"
---

## Definition

Video World Model is maintained here as an evidence-linked concept. 基于视频扩散模型学习环境动力学，通过生成未来视频帧预测动作结果，用于策略优化和规划。

## Key Ideas

- Direct local evidence currently comes from [[jia2026dreamplan]].
- The concept is tracked with local tags: concept, world-model, video-generation.
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

- [[jia2026dreamplan]] (direct evidence): 通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwe...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[yokomizo2026physquantagent]] (broader context): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[luo2026selfimproving]] (broader context): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...

## Evidence Map

- Direct evidence papers: [[jia2026dreamplan]].
- Broader local evidence context: [[jia2026dreamplan]], [[zhang2026recurrent]], [[zhang2026joyaira]], [[yokomizo2026physquantagent]], [[xie2026humanintention]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[world-model]]
- [[video-diffusion-model]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jia2026dreamplan]]
- [[zhang2026recurrent]]
- [[zhang2026joyaira]]
- [[yokomizo2026physquantagent]]
- [[xie2026humanintention]]
- [[wang2026visionlanguageaction]]
- [[tu2026embody4d]]
- [[luo2026selfimproving]]
