---
title: "Optimize and Coordinate Multiple DMPs Under Constraints to Achieve a Collaborative Manipulation Task"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于 CCMA-ES（约束 CMA-ES）优化协调多个 DMP 完成协同操控任务的方法。从单臂示教运动出发，构建双臂联合 DMP（共享 canonical system 保证同步），CCMA-ES 优化 DMP 权重满足固定距离约束（搬运刚体）。在仿真和真实 Baxter 机器人上验证，能在窄通道中协调双臂搬运物体并避障"
authors: "Kordia, Ali H.; Melo, Francisco S."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "9JEXTY7V"
---
## 摘要

This paper addresses a significant challenge in achieving collaborative tasks; how can a robot or multiple robots, endowed with a library of pre-learned primitive movements, generate multiple simultaneous coordinated robotic movements, adapting and optimizing those in the library, to complete one collaborative task? This work can thus be seen as a follow-up to the work with a motion presented as dynamic movement primitive (DMP) that now considers collaborative tasks and the existence of multiple robots/manipulators. Specifically, we start with a simple task using one DMP and extend it to accommodate the coordinated execution of multiple DMPs in robots with multiple manipulators or—alternatively—multiple robots with a single manipulator. We investigate mechanisms to jointly optimize multiple DMPs to perform one task in a coordinated fashion. The joint trajectory is built from initial DMPs learned for a single manipulator, and its optimization must comply with task-specific constraints. We illustrate the application of our approach both in a simulated environment and in a simulated and real Baxter robot.

## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、background (Sec II)、method (Sec III)、experiments (Sec IV)、figures (1-9)
- **Confidence**: high — 全文完整，ICRA 2025 论文，仿真 + Baxter 仿真器 + 真实 Baxter 机器人验证
- **Summary**: 提出基于 CCMA-ES（约束 CMA-ES）优化协调多个 DMP 完成协同操控任务的方法。从单臂示教运动出发，构建双臂联合 DMP（共享 canonical system 保证同步），CCMA-ES 优化 DMP 权重满足固定距离约束（搬运刚体）。在仿真和真实 Baxter 机器人上验证，能在窄通道中协调双臂搬运物体并避障
## 关键贡献

1. CCMA-ES 优化协调多 DMP：同时优化双臂 DMP 权重满足任务约束
2. 从单臂示教构建联合 DMP，共享 canonical system 保证同步
3. 约束处理：CCMA-ES 在约束违反时调整协方差矩阵并重采样
4. 仿真 + 真实 Baxter 验证，包括窄通道场景
## 结构化提取

- **Problem**: 多臂协同操控的协调运动生成，需同时满足任务约束和环境约束
- **Method**: CCMA-ES 优化联合 DMP — 单臂示教→双臂联合 DMP→约束优化
- **Tasks**: 双臂搬运刚体（仿真 + Baxter 真实机器人）
- **Sensors**: 关节编码器（无视觉传感器用于控制）
- **Robot Setup**: Baxter 机器人（双 7-DOF 臂）
- **Metrics**: 任务成功率、约束满足度
- **Limitations**: 仅固定距离约束、黑盒优化慢、动态障碍物未充分验证
- **Evidence Notes**: 全文读取，ICRA 2025 论文，仿真+真实验证
## 本地引用关系

- [[chen2025deformpam]]
- [[kumar122constraining]]
- [[li2025routing]]
- [[scheikl620movement]]
## Problem

协同操控任务（如搬运刚体）需要多个机械臂同时执行协调运动，保持任务约束（如固定距离）同时适应环境（障碍物）。现有方法需要领导者-跟随者标注（Gams et al.）或无法融入环境信息（ILC），难以同时处理协调约束和环境约束。


## Method

- **单臂示教 → 联合 DMP**：
  - 人类示教单臂运动 → 学习 DMP 权重
  - 为双臂各创建 DMP，共享 canonical system（ẋ = -αx·x）保证时间同步
  - 调制目标位置生成双臂运动
- **CCMA-ES 优化**：
  - 目标函数：J = Σ(c_goal‖y(t)-y*‖² + c_vel‖ẏ(t)‖² + c_obst Σ I(y(t)∈o_m))
  - 约束：‖y₁(t)-y₂(t)‖ = D（固定距离，搬运刚体）
  - 约束违反时：更新 fading record vj，调整协方差矩阵 Σi 减去违反方向的分量
  - 迭代：采样 → 检查约束 → 调整+重采样 → 评估 → 更新均值/协方差
- **动态障碍物**：调制矩阵 M 应用于最近的 DMP 并同步应用到两个 DMP


## Experiments

- **几何仿真**：
  - 宽通道：成功通过，保持距离约束
  - 窄通道：轨迹平滑度降低但约束满足
  - 复杂环境：多障碍物，协调状态自适应
- **Baxter 仿真器**：
  - 垂直障碍物布局，双臂搬运棒状物体成功
- **真实 Baxter 机器人**：
  - 宽通道：几乎不改 DMP 即可完成
  - 窄通道：需显著调整联合 DMP，改变物体朝向穿过通道
- **对比**：
  - vs 无约束优化 [22]：约束被违反，距离不保持
  - vs Gams et al. [7]：无法加入环境信息，需人工标注 leader/follower


## Limitations

1. 仅处理固定距离约束，未涉及力约束或更复杂的协同约束
2. CCMA-ES 为黑盒优化，收敛速度可能较慢
3. 动态障碍物方案仅简述，未充分验证约束保持
4. 仅 2D 平面验证（ Baxter 仿真/实体验证为 3D 但环境较简单）
5. 未考虑关节限制和力约束


## Key Takeaways

- CCMA-ES 的约束处理机制（协方差矩阵调整+重采样）是保证协调约束的关键
- 共享 canonical system 是 DMP 同步的简洁方案，避免时钟同步问题
- 从单臂示教构建双臂运动降低了示教复杂度
- 黑盒优化（CCMA-ES）的优势：不需线性/二次近似，直接处理非线性约束
- 固定距离约束是搬运刚体任务的最基本约束，扩展到力约束是重要方向

## 相关概念

- [[robotic-manipulation]]
- [[bimanual-manipulation]]

## 相关研究者

- [[kordia|Kordia, Ali H.]]
