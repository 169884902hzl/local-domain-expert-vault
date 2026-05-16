---
title: "3D Gaussian Splatting"
tags: [sim-to-real, robot-learning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "3DGS 用显式三维高斯表示场景，可在机器人仿真中兼顾真实感渲染、速度和 Real2Sim 资产生成。"
---

## Definition

3D Gaussian Splatting (3DGS) 是一种显式三维场景表示方法，用大量带位置、尺度、方向、颜色和透明度的高斯基元近似真实场景，并通过 splatting 实现高吞吐渲染。在本 vault 中，它主要作为视觉机器人学习的 photorealistic simulation 和 Real2Sim 资产构建工具出现。

## Key Ideas

- 显式高斯基元比传统 NeRF 更容易做实时渲染和批量并行渲染，适合大规模视觉策略训练。
- 机器人仿真需要渲染与物理状态同步；[[jia2026gsplayground]] 通过 Rigid-Link Gaussian Kinematics 将 3DGS 聚类绑定到刚体。
- 3DGS 可从真实图像重建可交互场景，降低手工建模 sim-ready 资产的成本。
- 当前 3DGS 方案仍偏刚体场景，对 DLO、布料等可变形对象的动态几何表达不足。
- 对操控策略而言，3DGS 的价值需要通过任务成功率、泛化和 Sim-to-Real 表现验证，而不只是渲染指标。

## Method Families

- Static scene reconstruction: 从多视角或单图先验恢复静态 3DGS，用于背景和物体建模。
- Dynamic rigid-body binding: 将 3DGS 聚类绑定到刚体 link，使渲染姿态跟随仿真物理状态。
- Real2Sim asset generation: 结合分割、3D 重建、点云剪枝和物理对齐，自动生成可训练环境。
- Compression and pruning: 通过 Gaussian pruning 降低显存和渲染成本，保持可接受的 PSNR/SSIM。

## Key Papers

- [[jia2026gsplayground]]: 将 batch 3DGS 渲染与自研物理引擎结合，面向视觉 RL、导航和操控任务。
- [[gu2026vistabot]]: 使用几何估计与生成式视角合成处理机器人跨视角泛化，属于相邻的 3D/视角鲁棒操控方向。
- [[keunknowndiffuser]]: 用 3D scene representation 结合扩散策略，说明三维表示对操控策略泛化的重要性。
- [[huang2026kinder]]: 提供物理推理 benchmark，可作为评估 3DGS 仿真是否支持真实物理泛化的参考。
- [[chen2025benchmarking]]: RoboTwin 双臂 benchmark 中包含真实/仿真差距，可作为 3DGS 仿真路线的下游评估场景。

## Evidence Map

- [[jia2026gsplayground]] 记录了 3DGS 在高吞吐仿真中的核心用法：batch 渲染、RLGK 姿态同步和 Image-to-Physics Real2Sim 流水线。
- [[jia2026gsplayground]] 的 Limitations 明确指出当前实现只支持刚体，不支持可变形物体，这是 DLO 仿真的直接 open problem。
- [[gu2026vistabot]] 和 [[keunknowndiffuser]] 提供相邻证据：机器人策略对三维几何、视角变化和潜空间表示高度敏感。

## Open Problems

- 如何把 3DGS 从刚体绑定扩展到 DLO、布料和软体物体的连续形变。
- 如何在保持高吞吐的同时支持随机光照、阴影和接触导致的外观变化。
- 如何让 3DGS 场景不仅真实可见，还能和接触力、摩擦、材料参数一致。
- 如何评估 3DGS-based simulator 对真实 DLO 操控策略的 Sim-to-Real 增益。

## Related Concepts

- [[sim-to-real]]
- [[robotic-manipulation]]
- [[novel-view-synthesis]]
- [[visual-reinforcement-learning]]

## Related Papers

- [[jia2026gsplayground]]
- [[gu2026vistabot]]
- [[keunknowndiffuser]]
