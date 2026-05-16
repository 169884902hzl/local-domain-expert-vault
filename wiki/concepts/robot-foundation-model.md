---
title: "Robot Foundation Model"
tags: [foundation-model, robot-learning, generalist-policy]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "通用机器人策略，在大规模多任务数据上预训练，支持多种机器人和任务的灵活操控。"
---

## Definition

Robot Foundation Model is maintained here as an evidence-linked concept. 通用机器人策略，在大规模多任务数据上预训练，支持多种机器人和任务的灵活操控。

## Key Ideas

- Direct local evidence currently comes from [[wu2026contrastive]].
- The concept is tracked with local tags: foundation-model, robot-learning, generalist-policy.
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

- [[wu2026contrastive]] (direct evidence): 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...

## Evidence Map

- Direct evidence papers: [[wu2026contrastive]].
- Broader local evidence context: [[wu2026contrastive]], [[zhou2026ego]], [[zheng2026pokevla]], [[zhang2026prts]], [[zhang2026joyaira]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[openvla]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[spurious-correlation]]
- [[robot-learning]]
- [[robotic-manipulation]]

## Related Papers

- [[wu2026contrastive]]
- [[zhou2026ego]]
- [[zheng2026pokevla]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
- [[ye2026reinforcement]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
