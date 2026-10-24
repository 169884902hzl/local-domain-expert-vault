---
title: "Novel View Synthesis"
tags: [manipulation, diffusion, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Novel View Synthesis 从有限观测合成新视角，在机器人操控中用于缓解相机视角变化导致的策略失效。"
---

## Definition

Novel View Synthesis (NVS) 指从已有图像或视频观测中合成未见相机视角下的图像或潜表示。机器人操控中的 NVS 不只是视觉生成任务，还必须保持几何、时序和任务状态一致，否则会把错误视觉证据传给闭环策略。

## Key Ideas

- NVS 可把测试时任意视角投影回训练视角，降低固定相机训练策略的视角 OOD 问题。
- 几何方法提供相机位姿、深度或点云约束，生成方法补全遮挡和未观测区域。
- [[gu2026vistabot]] 不直接用合成图像执行控制，而是提取 VDM 潜空间特征给 ACT/π₀ 策略。
- NVS 的机器人价值需要用任务成功率和 view generalization，而不只是 PSNR/FID 评价。
- 对 DLO 和接触任务，NVS 必须保持物体几何、遮挡边界和接触状态一致，否则会误导闭环策略。

## Method Families

- Geometry-based NVS: 依赖深度、相机位姿、点云或 3DGS 重建，几何一致性强但遮挡补全弱。
- Diffusion-based NVS: 用图像/视频扩散模型补全未观测区域，生成能力强但可能产生物理不一致。
- Hybrid geometry-generation NVS: 先用几何投影建立约束，再用扩散模型修复和插值。
- Latent NVS for control: 直接使用生成模型潜特征作为策略输入，避免解码和再编码损失。

## Key Papers

- [[gu2026vistabot]]: 将 VGGT 几何估计和 CogVideoX 视频扩散结合，实现跨视角闭环操控。
- [[jia2026gsplayground]]: 用 3DGS/Real2Sim 生成 photorealistic 训练环境，属于重建式视角/场景生成路线。
- [[keunknowndiffuser]]: 说明 3D scene representation 与扩散策略结合可提升多视角操控泛化。
- [[chi2024diffusion]]: 提供 visuomotor diffusion policy 基线，可用于评估 NVS 特征接入策略后的增益。
- [[chen2025benchmarking]]: 提供多任务双臂 benchmark 背景，可作为视角鲁棒操控的扩展评估场景。

## Evidence Map

- [[gu2026vistabot]] 给出 NVS 直接提升操控策略 view robustness 的证据，并提出 View Generalization Score。
- [[gu2026vistabot]] 的 ablation 显示几何、memory 和潜空间策略设计都会影响跨视角表现。
- [[jia2026gsplayground]] 提供另一条路线：不在测试时合成新视角，而是在训练前构造高保真可渲染环境。

## Open Problems

- NVS 生成错误如何在闭环控制中累积并导致动作偏移。
- 如何让 NVS 对 DLO、绳索、布料等形变对象保持几何和接触一致性。
- 如何在高速操控中降低视频扩散模型推理延迟。
- 如何把 VGS 这类视角鲁棒指标扩展到多相机、移动相机和手眼相机设置。

## Related Concepts

- [[vision-language-model]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]
## Related Papers

- [[yang2026physforge]]