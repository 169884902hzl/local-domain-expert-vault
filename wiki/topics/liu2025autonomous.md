---
title: "Autonomous Bimanual Manipulation of Deformable Objects Using Deep Reinforcement Learning Guided Adaptive Control"
tags: [manipulation, RL, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL 策略快速接近目标（但不精确），利用其动作估计初始 Jacobian Ĵ₀，经缩放调整后切换为 AC 完成精确收敛。仿真成功率 RLAC > RL > AC，真实 91/100（RLAC）vs 84/100（AC）vs 75/100（RL），路径效率 RLAC 显著最优"
authors: "Liu, Jiayi; Yang, Sihang; Wang, Yiwei; Zhao, Huan; Ding, Han"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "69YGIHG5"
---
## 摘要

Deformable object（可变形物体） manipulation（操控） (DOM) which is a common subtask in various surgical procedures represents an inevitable challenge in robot-assisted surgery (RAS) due to complex nonlinear deformation. This paper proposes a deep reinforcement learning（强化学习） guided adaptive control (RLAC) modelfree framework, which combines learning-based and Jacobianbased methods. To complement each other for optimized performance, we harness the sampling of deep reinforcement learning（强化学习） (DRL) policy explored in simulations to solve a reasonable estimation of the initial deformation Jacobian. In early control iterations, the actions suggested by the DRL agent are adopted until the estimated real-time Jacobian approximates the actual deformation model. Subsequently, the independent Jacobianbased adaptive control (AC) with sufficient initial deformation awareness begins execution to achieve precise internal feature manipulation（操控） on deformable objects. Experimental results demonstrate that our method enables more efficient positioning and exhibits near-optimal positioning paths. RLAC with robust sim-to-real（仿真到真实迁移） performance provides a feasible approach for the complex autonomous DOM in the real world.

## 中文简述

提出基于强化学习的双臂方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec II)、experiments (Sec III)、tables (I-II)、figures (1-7)、算法伪代码 (Algorithm 1)
- **Confidence**: high — 全文完整，ICRA 2025 论文，仿真 1000 组 + 真实双臂 UR5 100 组实验，SOFA 仿真器 + sim-to-real 验证
- **Summary**: 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL 策略快速接近目标（但不精确），利用其动作估计初始 Jacobian Ĵ₀，经缩放调整后切换为 AC 完成精确收敛。仿真成功率 RLAC > RL > AC，真实 91/100（RLAC）vs 84/100（AC）vs 75/100（RL），路径效率 RLAC 显著最优
## 关键贡献

1. RLAC 框架：DRL 指导 AC 初始化，解决 Jacobian 估计不收敛问题
2. 利用 RL actor 网络输出构造初始 Jacobian 估计（高斯采样 + 最小二乘求解）
3. 缩放调整机制：指数缩放 + 误差补偿，使 Ĵ 快速进入 AC 收敛范围
4. 双臂真实 UR5 实验，sim-to-real 成功率 91/100
## 结构化提取

- **Problem**: 可变形物体内部点操控的精确收敛 + sim-to-real 鲁棒性
- **Method**: RLAC — PPO 训练 actor → 初始化 Jacobian → 缩放调整 → AC 精确收敛
- **Tasks**: 双臂可变形物体内部点定位（SOFA 仿真 + 真实双臂 UR5）
- **Sensors**: RGB 相机（特征点定位）
- **Robot Setup**: SOFA 仿真 + 双臂 UR5
- **Metrics**: 成功率、PER（路径效率比）
- **Limitations**: 单一任务、2D、固定接触、手动参数
- **Evidence Notes**: 全文读取，Tables I-II 提供完整参数和真实实验结果
## 本地引用关系

- [[do2025watch]]
- [[karim2024davil]]
- [[li2025routing]]
- [[scheikl620movement]]
## Problem

可变形物体操控（DOM）中，Jacobian-based adaptive control 从随机初始 Jacobian 开始可能不收敛；DRL 策略 sim-to-real 性能下降且精确定位困难。如何结合两者优势——RL 的快速接近能力和 AC 的精确收敛能力？


## Method

- **Offline DRL 训练（PPO）**：
  - 仿真环境：SOFA simulator，100×100mm² 组织，50×50 质点-弹簧系统（k=90N/m, d=0.3N·s/m）
  - 状态：抓取点位置 + 特征点位置 + 特征-目标向量
  - 动作：抓取点增量位移（离散控制）
  - 奖励：rt = ρ₁(dt-1-dt) + ρ₂·sgn(dt-1-dt) - ρ₃（距离变化 + 方向奖励 - 步惩罚）
  - Actor-Critic：3 层 MLP（256-512-256），1500-4000 回合即可收敛
- **Jacobian 初始化（利用 RL）**：
  - 初始状态 s₀ 下，actor 输出动作 δx₀，假设对应变形方向 δp₀ = ptarg - p₀
  - 高斯采样 l 个目标方向 P̂₀ → actor 网络得到对应 X₀
  - 最小二乘求解：Ĵ₀ = P̂₀·X₀ᵀ·(X₀·X₀ᵀ)⁻¹
- **缩放调整阶段**：
  - Ĵt = Ĵt-1·exp(λ·log(‖pt-pt-1‖₂/‖Ĵt-1·δxt-1‖₂)) - γ·e·δxᵀt-1
  - 当 ‖Ĵt-1·δxt-1 - δpt-1‖₂ ≤ εJ 时切换为纯 AC
- **Adaptive Control**：
  - 估计器：梯度下降更新 Ĵ（Ĵt = Ĵt-1 - γ·e·δxᵀt-1）
  - 控制器：ut = κ(ptarg-pt)·Ĵt，速度饱和约束


## Experiments

- **仿真（SOFA，1000 组/距离阈值）**：
  - 成功率：RLAC 大部分距离阈值下最高，d=5mm ~100%，d=15mm ~85%
  - AC 在大距离阈值下表现差（初始 Ĵ 不准确导致不收敛）
  - RL 在训练域内表现好但超出后下降
  - PER（路径效率比）：RLAC 显著低于 RL 和 AC（更接近直线路径）
- **真实（双臂 UR5，100 组）**：
  - RLAC：91/100，AC：84/100，RL：75/100
  - RL sim-to-real 性能下降严重（感知噪声 + 材料差异）
  - RLAC 继承 AC 的收敛性，无 RLAC 失败而其他方法成功的情况
  - Levene's test：RLAC 的 PER 方差显著小于 RL（更稳定）
- **训练效率**：~2 小时（Intel i9-14900K），RLAC 仅需 1500 回合（vs RL 完整训练 4000 回合）


## Limitations

1. 仅测试单一任务设置（内部点操控）
2. 2D 平面约束，未扩展到 3D
3. 固定接触配置（抓取点固定），不支持动态接触调整
4. DRL 训练依赖仿真环境质量
5. 缩放参数（λ, γ, εJ, κ, s）需要手动调参


## Key Takeaways

- RL+AC 互补是有效范式：RL 提供合理的初始 Jacobian 估计，AC 提供精确收敛
- DRL 不需要完全训练到收敛——粗略的策略足以指导 AC 初始化
- 缩放调整是关键：RL 给出的 Jacobian 方向正确但尺度偏差大
- 近直线路径是 RLAC 的重要优势：减少不必要的变形和组织损伤
- Sim-to-real 中 AC 比 RL 更鲁棒（不依赖精确的感知-控制映射）

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[liu|Liu, Jiayi]]
