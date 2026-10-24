---
title: "Synthesizing grasps and regrasps for complex manipulation tasks"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于常螺旋运动分解和点云的抓取/重抓取合成算法。将复杂操控任务表示为常螺旋运动序列（如 pivot-slide-pivot），使用任务导向抓取度量 η 计算每段螺旋的抓取区域，通过区域重叠度 γ 确定最小抓取次数和重抓取时机。48 仿真试验正确预测最小抓取数。真实 Franka Panda 抓取+运动规划成功率 75%（15/20），失败主要因为关节极限"
authors: "Patankar, Aditya; Mahalingam, Dasharadhan; Chakraborty, Nilanjan"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "QMVS7LUS"
---
## 摘要

In complex manipulation（操控） tasks, e.g., manipulation（操控） by pivoting, the motion of the object being manipulated has to satisfy path constraints that can change during the motion. Therefore, a single grasp may not be sufficient for the entire path, and the object may need to be regrasped. Additionally, geometric data for objects from a sensor are usually available in the form of point clouds. The problem of computing grasps and regrasps from point-cloud representation of objects for complex manipulation（操控） tasks is a key problem in endowing robots with manipulation（操控） capabilities beyond pick-and-place. In this paper, we formalize the problem of grasping（抓取）/regrasping for complex manipulation（操控） tasks with objects represented by (partial) point clouds and present an algorithm to solve it. We represent a complex manipulation（操控） task as a sequence of constant screw motions. Using a manipulation（操控） plan skeleton as a sequence of constant screw motions, we use a grasp metric to find graspable regions on the object for every constant screw segment. The overlap of the graspable regions for contiguous screws are then used to determine when and how many times the object needs to be regrasped. We present experimental results on point cloud（点云） data collected from RGB-D sensors to illustrate our approach.

## 中文简述

提出基于点云的抓取方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、preliminaries (Sec III)、problem formulation (Sec IV)、method (Sec V)、experiments (Sec VI)、tables (I)、figures (1-4)
- **Confidence**: high — 全文完整，arXiv 2025 预印本，Stony Brook University，Franka Panda 真实机器人，4 物体×4 姿态×3 骨架 = 48 仿真试验 + 20 真实试验，75% 成功率
- **Summary**: 提出基于常螺旋运动分解和点云的抓取/重抓取合成算法。将复杂操控任务表示为常螺旋运动序列（如 pivot-slide-pivot），使用任务导向抓取度量 η 计算每段螺旋的抓取区域，通过区域重叠度 γ 确定最小抓取次数和重抓取时机。48 仿真试验正确预测最小抓取数。真实 Franka Panda 抓取+运动规划成功率 75%（15/20），失败主要因为关节极限
## 关键贡献

1. 首次形式化点云表示下复杂操控任务的重抓取问题
2. 常螺旋运动作为运动约束的统一表示：适用于 pivoting、sliding、pouring 等任务
3. 抓取区域重叠度量 γ：自动确定何时重抓取以及最小抓取次数
4. 点云到抓取区域的完整流程：无需完整 CAD 模型
## 结构化提取

- **Problem**: 点云表示物体的复杂操控任务抓取/重抓取合成
- **Method**: 常螺旋运动分解 + 任务导向抓取度量 η + 区域重叠度 γ
- **Tasks**: pivoting、sliding、pouring（3 骨架 × 4 物体）
- **Sensors**: Intel RealSense D415（眼在手配置）
- **Robot Setup**: Franka Emika Panda
- **Metrics**: 最小抓取数 α 预测正确率 + 真实执行成功率
- **Limitations**: 无关节极限约束、无碰撞检测、简单物体仅
- **Evidence Notes**: 全文读取，Table I 提供真实实验结果
## 本地引用关系

- [[huang2025match]]
- [[nasiriany2025rtaffordance]]
- [[nie820smaller]]
## Problem

复杂操控任务（如 pivoting、pouring）的运动路径约束会变化，单个抓取可能无法完成整个路径。现有重抓取方法主要针对 pick-and-place 任务，缺乏运动约束和抓取的统一数学表示。如何从点云表示的物体出发，给定运动计划骨架，自动计算最小抓取次数和每次抓取的区域？


## Method

- **任务表示**：运动计划 G = {g₁, ..., gₖ} 为 SE(3) 中的位姿序列，相邻位姿对 (gᵢ, gᵢ₊₁) 构成常螺旋运动
- **任务导向抓取度量 η**：
  - 对于 pivoting：η = 绕螺旋轴的最大力矩（满足摩擦锥约束）
  - 对于 sliding：η = 沿螺旋轴的最大力
  - 二阶锥规划（CVXPY）求解
- **抓取区域计算**：
  - 对每个常螺旋段，计算 η ≥ η_th 的点云区域 Igᵢ
  - 使用 3D 包围盒 + 神经网络（pouring 任务）从点云提取抓取区域
- **重抓取判定**：
  - 顺序比较相邻抓取区域的重叠度 γ = |∩Cu|/|Igᵢ|
  - γ ≥ γ_th → 同一抓取可用于连续段
  - γ < γ_th → 需要重抓取
  - 最小化 α（抓取子集数）= 最小抓取次数
- **运动规划**：ScLERP 插值 + Jacobian 伪逆生成关节空间轨迹


## Experiments

- **仿真评估**（4 物体 × 4 姿态 × 3 骨架 = 48 试验）：
  - {pivot, pivot, pivot}：所有物体 α=2
  - {slide, pivot, slide}：所有物体 α=2
  - {slide, pivot, pickup}：CheezIt/Domino α=1 或 2，Ritz/Pringles α=2
  - γ_th=0.25, η_th=0.75，计算时间约 30 秒/计划
- **真实机器人实验**（Franka Panda + RealSense D415）：
  - CheezIt/Ritz: 6 试验各，成功率 4/6
  - Spam/Pringles pouring: 4 试验各，成功率 4/4 和 3/4
  - 总体：15/20 = 75% 成功率
  - 失败原因：运动规划生成失败（关节极限），非抓取规划问题
  - Pouring 任务中 α=1（单次抓取），γ=0.890


## Limitations

1. 未考虑机器人关节极限约束
2. 未考虑 gripper/机械臂与环境的碰撞
3. 仅验证简单几何物体（盒子、圆柱）
4. 点云自遮挡影响抓取区域计算
5. 运动计划骨架需人工指定或从演示提取


## Key Takeaways

- 常螺旋运动是运动约束的优雅表示：统一了旋转、平移和复合运动
- 重抓取由运动约束而非仅由 pick/place 不兼容驱动
- 抓取区域重叠度是重抓取决策的关键指标
- 任务导向抓取度量 η 比通用抓取质量更适合复杂操控
- 单次抓取有时就够了：通过 γ 分析发现部分任务无需重抓取

## 相关概念

- [[robotic-manipulation]]
- [[grasping]]

## 相关研究者

- [[patankar|Patankar, Aditya]]
