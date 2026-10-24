---
title: "Recurrent State Space Model (RSSM)"
tags: [world-model, latent-dynamics, sequence-modeling]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "一种将确定性递归状态与随机潜状态结合的世界模型架构，支持长时序潜空间预测和'dreaming'。"
---

## Definition

Recurrent State Space Model (RSSM) is maintained here as an evidence-linked concept. 一种将确定性递归状态与随机潜状态结合的世界模型架构，支持长时序潜空间预测和'dreaming'。

## Key Ideas

- Direct local evidence currently comes from [[missal2026ropedreamer]].
- The concept is tracked with local tags: world-model, latent-dynamics, sequence-modeling.
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

- [[missal2026ropedreamer]] (direct evidence): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[wang2025vlaadapter]] (broader context): 提出 VLA-Adapter，系统分析 VLA 模型中 VL→A 桥接范式的有效性。发现中间层 Raw 特征优于深层（语义偏差）、深层 ActionQuery 最优、多层特征...
- [[dong2025vitavla]] (broader context): 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token...

## Evidence Map

- Direct evidence papers: [[missal2026ropedreamer]].
- Broader local evidence context: [[missal2026ropedreamer]], [[zheng2026pokevla]], [[zhang2026touchguide]], [[zhang2026prts]], [[zhang2026joyaira]].
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
- [[deformable-linear-object]]
- [[model-predictive-control]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[missal2026ropedreamer]]
- [[zheng2026pokevla]]
- [[zhang2026touchguide]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
- [[zhang2026generative]]
- [[wang2025vlaadapter]]
- [[dong2025vitavla]]
