---
title: "Domain Randomization"
tags: [sim-to-real, robot-learning, RL]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Domain randomization 通过随机化仿真物理和视觉参数提升 Sim-to-Real 鲁棒性，也可用于性能评估中的仿真多样性建模。"
---

## Definition

Domain Randomization 是一种 Sim-to-Real 技术：在仿真训练或评估中随机化质量、摩擦、阻尼、光照、纹理、相机、几何等参数，使策略或评估器不依赖单一仿真配置。

## Key Ideas

- 核心思想是用仿真多样性覆盖真实世界不确定性，而不是追求单一仿真器完全真实。
- 对策略训练，domain randomization 可提升视觉、动力学和接触参数变化下的鲁棒性。
- 对性能评估，[[mahboob2026betting]] 将多个随机化仿真器视为专家 bank，用自适应加权估计真实性能。
- 对 DLO 操控，摩擦、刚度、阻尼和长度的随机化比刚体任务更关键。
- 随机化过宽可能导致训练分布不真实，过窄则不能覆盖现实 gap。

## Method Families

- Visual randomization: 改变纹理、光照、相机、背景和遮挡。
- Dynamics randomization: 改变质量、摩擦、阻尼、刚度和接触参数。
- Geometry randomization: 改变物体尺寸、形状、初始姿态和场景布局。
- Evaluation randomization: 用多个仿真分布辅助估计真实性能，而不仅训练策略。

## Key Papers

- [[mahboob2026betting]]: 用 domain-randomized simulators 做 sim-to-real performance evaluation。
- [[li2025routing]]: DLO routing 中随机化摩擦以提升真实绳索 routing 泛化。
- [[zhao2026visualtactile]]: PiH 中用视觉域随机化和触觉校准做 Sim-to-Real。
- [[jia2026gsplayground]]: 高保真 Real2Sim 与视觉仿真提供 domain randomization 的相邻基础设施。
- [[wu2025rlgsbridge]]: 3DGS Real2Sim2Real 中讨论仿真到真实视觉差距。

## Evidence Map

- [[mahboob2026betting]] 说明随机化仿真不仅能训练策略，也能作为真实性能估计的 proposal/expert source。
- [[li2025routing]] 说明 DLO 摩擦变化会显著影响策略，因此物理随机化是 DLO 方向的必要因素。
- [[zhao2026visualtactile]] 说明触觉/视觉 Sim-to-Real 需要校准和随机化组合。
- [[jia2026gsplayground]] 与 [[wu2025rlgsbridge]] 提供 photorealistic/3DGS 路线，与随机化路线形成互补。

## Open Problems

- 如何为 DLO 自动选择合理的摩擦、刚度、阻尼随机化范围。
- 如何判断随机化带来的 robustness 是否来自真实物理覆盖，而非策略过度保守。
- 如何把 domain randomization 与高保真 3DGS/Real2Sim 结合。
- 如何用少量真实 rollouts 校正随机化分布。

## Related Concepts

- [[sim-to-real]]
- [[performance-evaluation]]
- [[visual-reinforcement-learning]]
- [[deformable-linear-object]]

## Related Papers

- [[mahboob2026betting]]
- [[li2025routing]]
- [[zhao2026visualtactile]]
- [[jia2026gsplayground]]
- [[wu2025rlgsbridge]]
