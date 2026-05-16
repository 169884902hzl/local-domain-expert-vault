---
title: "The art of imitation: Learning long-horizon manipulation tasks from few demonstrations"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 TPGMM 的三重改进用于长时序操控的少样本模仿学习：(1) Riemannian 速度因式分解，将末端执行器速度分解为方向（流形上的 von Mises-Fisher）和幅度（高斯），分别在 Riemannian 空间建模；(2) 利用速度因式分解实现自动技能分割和序列化，通过分割对齐轨迹并利用时间作为归纳偏置；(3) 自动检测相关任务参数（从 RGB-D 观测中推断哪些帧/视角对每个技能相关）。在 RLBench 上仅需 5 条演示即达到 SOTA 性能（20x 样本效率提升），且学到的技能可复用"
authors: "Hartz, Jan Ole von; Welschehold, Tim; Valada, Abhinav; Boedecker, Joschka"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "34FRSU3E"
---
## 摘要

Task Parametrized Gaussian Mixture Models (TPGMM) are a sample-efficient method for learning object-centric robot manipulation（机器人操控） tasks. However, there are several open challenges to applying TP-GMMs in the wild. In this work, we tackle three crucial challenges synergistically. First, end-effector velocities are non-Euclidean and thus hard to model using standard GMMs. We thus propose to factorize the robot’s end-effector velocity into its direction and magnitude, and model them using Riemannian GMMs. Second, we leverage the factorized velocities to segment and sequence skills from complex demonstration（示范数据） trajectories. Through the segmentation, we further align skill trajectories and hence leverage time as a powerful inductive bias. Third, we present a method to automatically detect relevant task parameters per skill from visual observations. Our approach enables learning complex manipulation（操控） tasks from just five demonstrations while using only RGB-D observations. Extensive experimental evaluations on RLBench demonstrate that our approach achieves state-of-the-art（现有最优方法） performance with 20fold improved sample efficiency. Our policies generalize across different environments, object instances, and object positions, while the learned skills are reusable.

## 中文简述

提出基于模仿学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-V)、experiments (Sec VI)、tables/figures
- **Confidence**: high — 全文完整，arXiv 2024 预印本，RLBench 上 7 个长时序任务系统评估，5 条演示即达 SOTA
- **Summary**: 提出 TPGMM 的三重改进用于长时序操控的少样本模仿学习：(1) Riemannian 速度因式分解，将末端执行器速度分解为方向（流形上的 von Mises-Fisher）和幅度（高斯），分别在 Riemannian 空间建模；(2) 利用速度因式分解实现自动技能分割和序列化，通过分割对齐轨迹并利用时间作为归纳偏置；(3) 自动检测相关任务参数（从 RGB-D 观测中推断哪些帧/视角对每个技能相关）。在 RLBench 上仅需 5 条演示即达到 SOTA 性能（20x 样本效率提升），且学到的技能可复用
## 关键贡献

1. Riemannian 速度因式分解：方向（von Mises-Fisher on S²）和幅度（Gaussian on R⁺）分别建模
2. 自动技能分割：利用速度变化点检测技能边界，从复杂演示中自动分割出基本技能
3. 自动任务参数检测：从 RGB-D 观测中推断每个技能的相关帧/视角
4. 技能可复用性：分割后的技能可在不同任务间共享和组合
## 结构化提取

- **Problem**: TPGMM 的速度建模、技能分割和任务参数检测三大挑战
- **Method**: Riemannian TPGMM — 速度因式分解 + 自动分割 + 自动参数检测
- **Tasks**: RLBench 7 个长时序操控任务
- **Sensors**: RGB-D 相机（多视角）+ 机器人本体感觉
- **Robot Setup**: RLBench 仿真（Franka Panda）
- **Metrics**: 成功率、样本效率
- **Limitations**: 仅刚性物体、独立性假设、分割精度、需要 RGB-D
- **Evidence Notes**: 全文读取，arXiv 2024 预印本，RLBench 7 任务系统评估
## 本地引用关系

- [[chen2025effective]]
- [[gao2024prime]]
- [[gao2025must]]
- [[wang2025oneshot]]
## Problem

TPGMM（任务参数化高斯混合模型）在物体中心操控任务中样本效率高，但存在三大挑战：(1) 末端执行器速度是非欧几里得的，标准 GMM 难以建模；(2) 长时序任务需要手动分割和序列化技能；(3) 需要手动指定任务参数。


## Method

- **速度因式分解**：
  - 速度向量分解为方向 v̂ = v/‖v‖ ∈ S² 和速度标量 ‖v‖ ∈ R⁺
  - 方向用 von Mises-Fisher (vMF) 分布建模（S² 流形上的高斯类似物）
  - 速度标量用对数正态/高斯分布建模
  - 联合概率 P(v) = P(v̂) · P(‖v‖)，因式分解后各自在合适空间建模
- **自动技能分割**：
  - 基于速度变化检测：计算速度大小和方向的变化率
  - 变化率峰值对应技能边界
  - 分割后对齐各技能段的时间轴
- **自动任务参数检测**：
  - 对每个技能段，计算每个视角（RGB-D 相机）与末端执行器运动的互信息
  - 选择互信息最高的 K 个视角作为该技能的任务参数
  - 避免手动指定哪些帧是相关的
- **TPGMM 核心**：
  - 每个任务参数定义一个概率模型（GMM on 位置 + vMF on 方向 + Gaussian on 速度）
  - 多个任务参数的概率通过乘积融合（Product of Experts）
  - 从融合分布中采样生成动作轨迹


## Experiments

- **RLBench 7 个任务**（5 条演示）：
  - 相比标准 TPGMM、BC-RNN、BC-Transformer、Diffusion Policy 等
  - 20x 样本效率提升（5 demos vs 100 demos baseline）
  - 多数任务达到与 100 demos baseline 相当的性能
- **技能复用**：学到的技能（如 reach、grasp、place）可跨任务组合
- **泛化**：跨不同环境、物体实例和物体位置
- **消融**：因式分解 vs 联合建模、自动 vs 手动分割、自动 vs 手动参数检测


## Limitations

1. 仅处理刚性物体操控，可变形物体未涉及
2. 速度因式分解假设方向和速度独立，可能丢失耦合信息
3. 自动分割依赖速度变化检测，对缓慢过渡的任务可能不够准确
4. 需要 RGB-D 观测进行任务参数检测
5. 技能序列化仍需一定的结构化假设


## Key Takeaways

- 在 Riemannian 流形上分别建模速度方向和幅度是处理非欧几里得动作空间的有效方法
- 自动技能分割 + 对齐使 TPGMM 能处理长时序任务而无需手动标注
- 利用时间归纳偏置（分割后对齐时间轴）是少样本学习的关键
- 互信息驱动的任务参数检测避免了手动特征工程
- TPGMM 框架在少样本场景下优于深度学习方法（20x 效率）

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[hartz|Hartz, Jan Ole von]]
- [[valada|Valada, Abhinav]]
