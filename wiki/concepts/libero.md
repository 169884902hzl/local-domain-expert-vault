---
title: "LIBERO"
tags: [benchmark, manipulation, lifelong-learning]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "基于仿真器的机器人操控 benchmark，聚焦终身学习和知识迁移，包含 Spatial、Object、Goal、Long 四个任务套件。"
---

## Definition

LIBERO is maintained here as an evidence-linked concept. 基于仿真器的机器人操控 benchmark，聚焦终身学习和知识迁移，包含 Spatial、Object、Goal、Long 四个任务套件。

## Key Ideas

- Direct local evidence currently comes from [[xiao2026worldenv]].
- The concept is tracked with local tags: benchmark, manipulation, lifelong-learning.
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

- [[xiao2026worldenv]] (direct evidence): 提出用扩散世界模型替代物理交互环境对 VLA 策略进行 RL 后训练，通过 VGGT 几何感知特征注入保证物理一致性，用 VLM 即时反射器提供连续奖励信号和动态终止检测，仅...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...

## Evidence Map

- Direct evidence papers: [[xiao2026worldenv]].
- Broader local evidence context: [[xiao2026worldenv]], [[zhu2026nsvla]], [[zhou2026rcnf]], [[zhong2026vlaopd]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-action]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[xiao2026worldenv]]
- [[zhu2026nsvla]]
- [[zhou2026rcnf]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhang2026prts]]
- [[xiao2026avavla]]
- [[wu2026continually]]
