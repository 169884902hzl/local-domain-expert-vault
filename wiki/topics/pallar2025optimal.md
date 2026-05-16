---
title: "Optimal Trajectory Planning for Cooperative Manipulation with Multiple Quadrotors Using Control Barrier Functions"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 CBF 轨迹规划算法用于多四旋翼协作操控线缆悬挂刚体载荷。将载荷、线缆、四旋翼建模为凸多面体，利用对偶定理降低 CBF 约束的计算复杂度，确保全系统（载荷+线缆+四旋翼）6-DoF 避障。CasADi 优化器 25 步 horizon，每次迭代 9-15 秒。仿真 6 个环境中无全局规划器成功率 0-70%，有 A* 全局规划器 100%。真实 3 架四旋翼通过窄缝成功"
authors: "Pallar, Arpan; Li, Guanrui; Sarvaiya, Mrunal; Loianno, Giuseppe"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "GX2X396N"
---
## 摘要

In this paper, we present a novel trajectory planning algorithm for cooperative manipulation（操控） with multiple quadrotors using control barrier functions (CBFs). Our approach addresses the complex dynamics of a system in which a team of quadrotors transports and manipulates a cablesuspended rigid-body payload in environments cluttered with obstacles. The proposed algorithm ensures obstacle avoidance for the entire system, including the quadrotors, cables, and the payload in all six degrees of freedom (DoF). We introduce the use of CBFs to enable safe and smooth maneuvers, effectively navigating through cluttered environments while accommodating the system’s nonlinear dynamics. To simplify complex constraints, the system components are modeled as convex polytopes, and the Duality theorem is employed to reduce the computational complexity of the optimization problem. We validate the performance of our planning approach both in simulation and real-world environments using multiple quadrotors. The results demonstrate the effectiveness of the proposed approach in achieving obstacle avoidance and safe trajectory generation for cooperative transportation tasks.

## 中文简述

提出基于学习方法的线缆操控方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、system modeling (Sec III)、planning (Sec IV)、experiments (Sec V)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025，NYU Tandon，RotorTM 仿真（6 环境×10 起终点）+ Vicon 真实实验（3 架四旋翼），CBF+凸多面体+对偶定理完整推导
- **Summary**: 提出 CBF 轨迹规划算法用于多四旋翼协作操控线缆悬挂刚体载荷。将载荷、线缆、四旋翼建模为凸多面体，利用对偶定理降低 CBF 约束的计算复杂度，确保全系统（载荷+线缆+四旋翼）6-DoF 避障。CasADi 优化器 25 步 horizon，每次迭代 9-15 秒。仿真 6 个环境中无全局规划器成功率 0-70%，有 A* 全局规划器 100%。真实 3 架四旋翼通过窄缝成功
## 关键贡献

1. 全系统 6-DoF 避障：首次显式考虑载荷+线缆+四旋翼的完整系统避障
2. CBF 约束确保安全平滑导航：离散时间 CBF + 指数 CBF 降低计算量
3. 凸多面体建模 + 对偶定理：简化复杂碰撞约束，使优化问题可行
4. 仿真+真实验证：6 个仿真环境 + 3 架四旋翼真实实验
## 结构化提取

- **Problem**: 多四旋翼线缆悬挂载荷全系统避障轨迹规划
- **Method**: CBF + 凸多面体建模 + 对偶定理 + CasADi 优化
- **Tasks**: 线缆悬挂载荷运输（仿真 6 环境×10 组 + 真实窄缝穿越）
- **Sensors**: Vicon 动捕系统（100Hz）
- **Robot Setup**: 3 架定制四旋翼 + 三角载荷（196g，1m 边长）
- **Metrics**: 规划成功率 + 避障安全性
- **Limitations**: 非实时、仅刚性载荷、静态障碍物、需动捕
- **Evidence Notes**: 全文读取，Tables I-II 提供仿真成功率，Fig 6 展示真实轨迹
## 本地引用关系

- [[chen2025coordinated]]
- [[li2025routing]]
## Problem

多四旋翼通过线缆悬挂刚体载荷在杂乱环境中运输和操控时，需要同时避免载荷、线缆和四旋翼与障碍物碰撞。现有方法要么仅考虑载荷避障，要么假设固定编队/leader-follower 结构，要么仅在简单仿真中验证。如何在完整系统动力学约束下生成安全、平滑且全系统避障的轨迹？


## Method

- **系统建模**：
  - 载荷位姿 XL = (xL, qL)，速度 VL = (ẋL, ΩL)
  - 线缆力通过 μL = P†(PP†)⁻¹WL 分配到各四旋翼
  - 线缆方向 ξk 由张力方向决定，四旋翼位置 xk = xL + RL(ρk - lkξk)
  - 状态向量 X = [xL, qL, ẋL, ΩL, F, M]，输入 U = [Ḟ, Ṁ]
- **优化问题**：
  - N 步 horizon 的二次型代价函数（状态误差 + 输入误差 + 终端代价）
  - 可选 A* 全局规划器提供参考路径避免局部最优
- **CBF 约束**：
  - 凸多面体建模：载荷为三角柱体，线缆+四旋翼为长方体
  - 对偶定理：h(X) = min||yL - yobs||² - d²_safe → 对偶形式避免内层优化
  - 指数 CBF：h(X_{i+1}) ≥ αᵢ∏γⱼh(X₀) 进一步简化
- **求解**：CasADi 优化器，horizon=25 步，每步 9-15s（i7-8565U），忽略 >0.6m 障碍物


## Experiments

- **仿真实验**（RotorTM，3 四旋翼 + 三角载荷 196g）：
  - 6 个环境，每个 10 组随机起终点
  - 无全局规划器：ENV1-6 成功率分别为 60%/60%/50%/70%/0%/20%
  - 有 A* 全局规划器：所有环境 100%
  - 复杂/扭曲环境中无全局规划器容易陷入局部最优
- **真实实验**（Vicon 动捕 100Hz，10×6×4m³）：
  - 3 架四旋翼操控三角载荷通过聚苯乙烯泡沫箱构成的窄缝
  - 障碍物膨胀 7.5cm 补偿不确定性
  - 成功通过窄缝，四旋翼展示协调挤压和展开行为
  - 载荷显著旋转以通过障碍物


## Limitations

1. 计算速度慢（9-15s/步），非实时规划
2. 仅验证刚性载荷，未考虑柔性物体
3. 障碍物需预知（静态环境）
4. 需要运动捕捉系统（无自主定位）
5. 线缆假设始终张紧，松缆场景未处理


## Key Takeaways

- CBF 是多机器人安全规划的有效工具：比传统距离约束更高效
- 凸多面体+对偶定理是处理复杂碰撞约束的关键：将 NP-hard 问题转化为凸优化
- 全局规划器对复杂环境必不可少：局部优化器易陷入局部最优
- 线缆操控系统的核心挑战：间接驱动+紧耦合非线性动力学
- 仿真到真实迁移成功：但需要障碍物膨胀补偿不确定性

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[pallar|Pallar, Arpan]]
