---
title: "Visual Reinforcement Learning"
tags: [RL, robot-learning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Visual RL 直接从视觉观测学习机器人控制策略，核心瓶颈是样本效率、仿真吞吐和 Sim-to-Real 泛化。"
---

## Definition

Visual Reinforcement Learning 指以 RGB、深度、点云或视觉特征作为主要状态观测，通过 RL 训练机器人策略。它减少了人工状态设计，但会显著提高样本需求，因此通常依赖高吞吐仿真、视觉域随机化、真实数据混合或表征预训练。

## Key Ideas

- 视觉观测提供全局几何和语义上下文，但对光照、视角和遮挡变化敏感。
- Visual RL 的训练成本高度依赖仿真吞吐；[[jia2026gsplayground]] 的动机正是解决 photorealistic rendering 成本过高的问题。
- 在接触丰富任务中，单纯视觉通常不足，需要和触觉、力或本体状态融合。
- 对 DLO 操控而言，Visual RL 需要同时处理可变形状态估计、接触不确定性和长时序任务分解。
- Visual RL 的可信评价应覆盖 seen/unseen objects、视角变化、真实机器人迁移和失败状态分析。

## Method Families

- End-to-end pixel RL: 直接从图像训练策略，通常需要大量交互。
- Representation-first RL: 先用自监督、MAE、视频或三维表征学习视觉特征，再接 RL。
- Sim-to-Real visual RL: 在仿真中用 domain randomization、photorealistic rendering 或 Real2Sim 降低视觉差距。
- Hybrid RL + imitation: 用演示或专家片段约束探索，降低直接 RL 的试错成本。

## Key Papers

- [[jia2026gsplayground]]: 提供高吞吐视觉仿真基础设施，用于视觉 RL、导航和操控。
- [[li2025routing]]: DLO routing 中使用 RL 训练 rope insertion/pulling，再蒸馏到扩散策略。
- [[zhao2026visualtactile]]: 用 PooH 逆向任务和视觉-触觉观测降低 PiH 装配中 RL 探索成本。
- [[han2025upvital]]: 用视觉和触觉自监督表征辅助 RL 灵巧操控。
- [[chen2025vividex]]: 从人类视频提取轨迹并用 RL 训练灵巧手策略，是 vision-based manipulation policy 的相邻路线。

## Evidence Map

- [[jia2026gsplayground]] 表明视觉 RL 的系统瓶颈来自真实感渲染吞吐和 sim-ready 资产构建。
- [[zhao2026visualtactile]] 表明在 PiH 这类接触丰富任务中，视觉需要与触觉结合才能显著提升成功率和降低接触力。
- [[li2025routing]] 表明 DLO 任务可先用 RL 获得专家 rollouts，再训练闭环扩散策略提升鲁棒性。
- [[han2025upvital]] 表明自监督触觉/视觉表征可提升 RL 泛化，但部署时传感器依赖仍需权衡。

## Open Problems

- 如何让视觉 RL 在 DLO、布料等高维可变形状态中稳定学习。
- 如何用少量真实交互校正仿真视觉和接触物理的双重 gap。
- 如何评价视觉策略是否学到了可泛化几何，而不是记住背景或视角。
- 如何把 VLM/VLA 的语义先验和底层 RL 的接触控制结合起来。

## Related Concepts

- [[sim-to-real]]
- [[tactile-sensing]]
- [[diffusion-policy]]
- [[deformable-linear-object]]

## Related Papers

- [[jia2026gsplayground]]
- [[li2025routing]]
- [[zhao2026visualtactile]]
- [[han2025upvital]]
