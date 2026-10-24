---
title: "Peg-in-Hole Assembly"
tags: [manipulation, tactile, RL]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Peg-in-hole 是典型接触丰富装配任务，常用于检验视觉、触觉、力控和 Sim-to-Real 策略。"
---

## Definition

Peg-in-hole (PiH) assembly 是将刚性 peg 精确插入匹配孔位的机器人装配任务。它要求接近、对准、接触调整和插入四个阶段协同完成，是评估接触感知、力控、RL 探索效率和 Sim-to-Real 的标准任务之一。

## Key Ideas

- PiH 的难点不在自由空间运动，而在接触后的微小错位、摩擦、卡滞和过大接触力。
- 触觉和力觉能补充视觉在遮挡和微小偏差上的不足。
- [[zhao2026visualtactile]] 利用 peg-out-of-hole 逆向任务生成示教，降低直接 RL 训练 PiH 的探索成本。
- PiH 对 DLO 操控有方法启发：某些任务存在“正向难、逆向容易”的结构不对称。
- PiH 评价不应只看成功率，还需要关注最大接触力、泛化到 unseen geometry 和硬件安全性。

## Method Families

- Force-control insertion: 以力/力矩反馈和阻抗控制为核心，适合高精度装配。
- Visual-tactile RL: 结合视觉定位和触觉局部反馈，通过 RL 学习接触调整。
- Inverse-task demonstration: 从拆卸或拔出任务反转轨迹，构造装配示教。
- Diffusion/IL insertion: 用扩散策略或模仿学习从演示中学习插入动作。

## Key Papers

- [[zhao2026visualtactile]]: 用 PooH 逆向拆卸轨迹和视觉-触觉观测学习 PiH 装配。
- [[wu2025tacdiffusion]]: 用 force-domain diffusion policy 学习高精度触觉插入。
- [[lee2025diffdagger]]: 在 plugging 等操控任务中用 diffusion loss 做不确定性估计和专家请求。
- [[zhao2025polytouch]]: 多模态触觉传感和 tactile-diffusion policy 为接触丰富装配提供相邻证据。
- [[liu2025forcemimic]]: force-centric imitation learning 说明力信息对接触丰富操作的重要性。

## Evidence Map

- [[zhao2026visualtactile]] 记录了 PiH 中视觉-触觉融合、PooH 轨迹反转、动作随机化和 Sim-to-Real 迁移的完整证据。
- [[zhao2026visualtactile]] 的 ablation 表明去除触觉或视觉都会显著降低成功率，说明 PiH 是多模态感知任务。
- [[wu2025tacdiffusion]] 提供 force-domain diffusion 的相邻证据，强调力域动作对高精度插入的价值。

## Open Problems

- 如何从刚性 PiH 扩展到柔性连接器、线缆插拔和 DLO 穿孔。
- 如何在减少硬件磨损的同时让策略探索足够多接触状态。
- 如何统一视觉、触觉、力和本体信息的时序对齐。
- 如何把逆向任务示教自动推广到缠绕、解缠、穿线等 DLO 任务。

## Related Concepts

- [[robotic-manipulation]]
- [[tactile-sensing]]
- [[sim-to-real]]
- [[visual-tactile-fusion]]

## Related Papers

- [[zhao2026visualtactile]]
- [[wu2025tacdiffusion]]
- [[lee2025diffdagger]]
