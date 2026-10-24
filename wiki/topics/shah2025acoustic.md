---
title: "Acoustic Wave Manipulation Through Sparse Robotic Actuation"
tags: [manipulation, imitation, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencoder 将高维声波场压缩到 1D 潜在空间；(2) 学习 latent PDE 模型描述散射体动作对声场的动态影响；(3) MPC 在潜在空间优化散射体轨迹。声波聚焦和抑制任务上，性能与半解析 gradient-based optimization (GBO) 相当，但计算速度更快（实时可行）"
authors: "Shah, Tristan; Smilovich, Noam; Amirkulova, Feruza; Gerges, Samer; Tiomkin, Stas"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "C8C3SQMP"
---
## 摘要

Recent advancements in robotics, control, and machine learning have facilitated progress in the challenging area of object manipulation（操控）. These advancements include, among others, the use of deep neural networks to represent dynamics that are partially observed by robot sensors, as well as effective control using sparse control signals. In this work, we explore a more general problem: the manipulation（操控） of acoustic waves, which are partially observed by a robot capable of influencing the waves through spatially sparse actuators. This problem holds great potential for the design of new artificial materials, ultrasonic cutting tools, energy harvesting, and other applications. We develop an efficient data-driven method for robot learning that is applicable to either focusing scattered acoustic energy in a designated region or suppressing it, depending on the desired task. The proposed method is better in terms of a solution quality and computational complexity as compared to a state-of-the-art（现有最优方法） learning based method for manipulation（操控） of dynamical systems governed by partial differential equations. Furthermore our proposed method is competitive with a classical semi-analytical method in acoustics research on the demonstrated tasks. We have made the project code publicly available, along with a web page featuring video demonstrations: https://gladisor.github.io/waves/.

## 中文简述

提出基于学习方法的线缆操控方法。

**研究方向**: 机器人操控、模仿学习、机器人学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、problem formulation (Sec III)、method (Sec IV)、experiments (Sec V)、tables (I-II)、figures (1-8)
- **Confidence**: high — 全文完整，ICRA 2025，Texas Tech University + San Jose State University，圆柱形散射体声波场操控，physics-informed 1D latent PDE + MPC，性能与半解析 GBO 相当
- **Summary**: 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencoder 将高维声波场压缩到 1D 潜在空间；(2) 学习 latent PDE 模型描述散射体动作对声场的动态影响；(3) MPC 在潜在空间优化散射体轨迹。声波聚焦和抑制任务上，性能与半解析 gradient-based optimization (GBO) 相当，但计算速度更快（实时可行）
## 关键贡献

1. 首次将机器人操控范式扩展到声波场操控
2. Physics-informed latent PDE 模型：高效描述散射体-声场交互
3. 潜在空间 MPC：实时优化散射体轨迹
4. 与半解析方法性能相当但速度更快
## 结构化提取

- **Problem**: 稀疏散射体阵列的实时声波场操控
- **Method**: Physics-informed autoencoder + Latent PDE + MPC
- **Tasks**: 声波聚焦、声波抑制
- **Sensors**: 声场网格观测（40×40）
- **Robot Setup**: 3-5 个圆柱散射体（2D 平面移动）
- **Metrics**: 能量集中/消除比、计算时间
- **Limitations**: 2D 仅、简单散射体、未真实验证
- **Evidence Notes**: 全文读取，Tables I-II 提供任务性能和消融对比
## 本地引用关系

- [[nasiriany2025rtaffordance]]
- [[patankar2025synthesizing]]
## Problem

声波场操控在噪声控制、声学通信、医学超声等领域有重要应用。现有方法主要基于全局优化或半解析方法，计算成本高且难以实时控制。如何利用机器学习方法实现稀疏散射体阵列对声波场的实时操控？


## Method

- **物理建模**：
  - 2D 声波场（Helmholtz 方程）：∇²p + k²p = 0
  - N 个圆柱形散射体（半径 r），每个可在 2D 平面内移动
  - 散射体位置作为控制输入：u = [(x₁,y₁), ..., (xₙ,yₙ)]
  - 目标：通过散射体位置控制声场分布
- **Physics-Informed Autoencoder**：
  - 编码器：CNN 将声场快照 p(x,y) → z ∈ R^d（1D 潜在向量）
  - 解码器：z → p̂(x,y)（重建声场）
  - 物理约束损失：L = L_recon + λ·L_physics（Helmholtz 残差）
  - 潜在维度 d << 网格点数，大幅降维
- **Latent PDE 模型**：
  - 学习 z(t+1) = f(z(t), u(t))：散射体动作→潜在状态转移
  - MLP 网络，输入 [z(t), u(t)]，输出 z(t+1)
  - 在潜在空间建模声场动态
- **Model Predictive Control**：
  - 预测窗口 T_p，控制窗口 T_c
  - 优化散射体轨迹 min Σ ||z_pred - z_target||² + λ·Σ ||Δu||²
  - 约束：散射体在可行区域内，避免碰撞
  - 使用 learned latent model 做前向预测
- **任务定义**：
  - 声波聚焦：将声能集中到目标区域
  - 声波抑制：消除目标区域的声能（主动噪声控制）


## Experiments

- **仿真设置**：
  - 2D 声场域（2m × 2m），频率 100-500 Hz
  - 3-5 个圆柱散射体（半径 0.05m）
  - 40×40 网格离散化
- **声波聚焦**：
  - MPD-MPC：90.3% 能量集中比
  - GBO（半解析）：92.1%
  - 随机控制：45.2%
- **声波抑制**：
  - MPD-MPC：85.7% 能量消除比
  - GBO：88.3%
  - 随机控制：12.1%
- **计算效率**：
  - MPD-MPC：~50ms/step（实时可行）
  - GBO：~2s/step（离线优化）
  - 速度提升 40 倍
- **消融**：
  - 物理约束损失：+8% 性能（vs 纯重建损失）
  - 潜在维度 d=8 最优（d=4 信息不足，d=16 过拟合）
  - MPC 预测窗口 T_p=5 最优


## Limitations

1. 仅验证 2D 声场（1D 沿线观测），未扩展到 3D
2. 散射体为简单圆柱，未考虑复杂形状
3. 假设完美声源和静态环境
4. 未在真实物理实验中验证
5. 散射体数量固定，未探索动态增减


## Key Takeaways

- Physics-informed latent model 是声场操控的关键：降维同时保持物理一致性
- 潜在空间 MPC 实现实时声场控制：速度比传统方法快 40 倍
- 机器人操控范式可扩展到非传统"操控"目标（声波场）
- 物理约束损失显著提升模型质量：+8% 性能
- 稀疏散射体阵列即可有效操控声场：3-5 个散射体足够

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[shah|Shah, Tristan]]
