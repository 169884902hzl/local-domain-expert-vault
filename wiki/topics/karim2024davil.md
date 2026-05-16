---
title: "DA-VIL: Adaptive dual-arm manipulation with reinforcement learning and variable impedance control"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver 最小化阻抗误差+姿态误差，满足关节/力矩/距离约束。MuJoCo 双臂 Franka 仿真，6 个物体（chair/stool/stockpot/laptop/monitor/crate），0.5-5kg 变质量。平均轨迹跟踪误差 0.031m（chair）至 0.043m（monitor），全面优于 OIC/IC/RL+IC"
authors: "Karim, Md Faizal; Bollimuntha, Shreya; Hashmi, Mohammed Saad; Das, Autrio; Singh, Gaurav et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "H29VIISZ"
---
## 摘要

Dual-arm manipulation（双臂操控） is an area of growing interest in the robotics community. Enabling robots to perform tasks that require the coordinated use of two arms, is essential for complex manipulation（操控） tasks such as handling large objects, assembling components, and performing human-like interactions. However, achieving effective dual-arm manipulation（双臂操控） is challenging due to the need for precise coordination, dynamic adaptability, and the ability to manage interaction forces between the arms and the objects being manipulated. We propose a novel pipeline that combines the advantages of policy learning based on environment feedback and gradient-based optimization to learn controller gains required for the control outputs. This allows the robotic system to dynamically modulate its impedance in response to task demands, ensuring stability and dexterity in dual-arm（双臂） operations. We evaluate our pipeline on a trajectory-tracking task involving a variety of large, complex objects with different masses and geometries. The performance is then compared to three other established methods for controlling dual-arm（双臂） robots, demonstrating superior results.

## 中文简述

提出基于强化学习的双臂方法。

**研究方向**: 机器人操控、强化学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、results (Sec V)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，arXiv 2024 预印本，6 个物体（0.5-5kg）×4 种质量 ×100 个目标位置系统评估，消融实验完备
- **Summary**: 提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver 最小化阻抗误差+姿态误差，满足关节/力矩/距离约束。MuJoCo 双臂 Franka 仿真，6 个物体（chair/stool/stockpot/laptop/monitor/crate），0.5-5kg 变质量。平均轨迹跟踪误差 0.031m（chair）至 0.043m（monitor），全面优于 OIC/IC/RL+IC
## 关键贡献

1. 无需示教的协同双臂操控框架：结合 RL + QP 变阻抗控制
2. RL 预测刚度 K（离散分类目标，6 维对角刚度），QP 优化关节加速度
3. 距离约束（双臂末端执行器距离 = 物体抓取距离 WG）
4. 全面优于 OIC/IC/RL+IC 基线，适应 0.5-5kg 变质量
## 结构化提取

- **Problem**: 双臂操控的力协调和变阻抗控制，固定参数无法适应变质量/几何
- **Method**: DA-VIL — RL（PPO 预测 K）+ QP 变阻抗控制器，距离约束保证协同
- **Tasks**: 双臂 pick-and-place（6 物体 ×4 质量 ×100 目标位置）
- **Sensors**: 关节编码器 + 末端力/力矩传感器
- **Robot Setup**: MuJoCo 仿真双臂 Franka Panda
- **Metrics**: 轨迹跟踪误差（m）
- **Limitations**: 仅仿真、已知抓取、离散刚度、需完整动力学模型
- **Evidence Notes**: 全文读取，Tables I-II 提供完整跟踪误差和消融结果
## 本地引用关系

- [[chen2025coordinated]]
- [[do2025watch]]
- [[liu2025autonomous]]
## Problem

双臂操控需要精确协调、动态适应和力管理。传统阻抗控制需要手动调参，固定参数无法适应变化的质量和几何。单臂变阻抗方法无法处理双臂约束（耦合力、共享工作空间、动态交互力）。


## Method

- **策略网络**：
  - PPO 算法，4 层 MLP 特征提取器 + 5 层 MLP 策略/价值网络
  - 观察空间：双臂末端位姿变化 ∆x、物体位姿、关节位置、末端力/力矩、前一步动作 K、时间/质量正弦嵌入
  - 动作空间：6 维对角刚度 K 的离散分类（20 倍数 bin）
  - 奖励：轨迹跟踪误差 + 目标到达 + EMA 平滑惩罚 + 不可行解惩罚
- **QP 控制器**：
  - 阻抗任务：eimp = ẍ − Λ⁻¹f，其中 f = D(ẋr-ẋ) + K(xr-x)，D 保证临界阻尼
  - 姿态任务：epos 保持关节配置接近接触时状态
  - 约束：关节位置/速度/力矩限制 + 末端执行器距离约束 ‖xL-xR‖² ≤ WG+tol
  - 关节加速度 → 力矩：τ = M(q)q̈* + h(q,q̇)
- **轨迹生成**：五次多项式（笛卡尔位置）+ SLERP（姿态），waypoint 在 x/y 中点 + 随机 z 高度


## Experiments

- **MuJoCo 仿真**：双臂 Franka Panda，6 物体
- **轨迹跟踪误差（m）**：
  - Chair: 0.0131 vs OIC 0.0166, IC 0.0598, RL+IC 0.0612
  - Monitor: 0.0428 vs OIC 0.0712, IC 0.1413, RL+IC 0.1085
  - Laptop: 0.0406 vs OIC 0.0555, IC 0.1564, RL+IC 0.0696
  - Stockpot: 0.0277 vs OIC 0.0384, IC 0.2201, RL+IC 0.0642
  - Stool: 0.0172 vs OIC 0.2547, IC 0.1451, RL+IC 0.1074
  - Crate: 0.0310 vs OIC 0.0378, IC 0.1415, RL+IC 0.0760
- **多物体（1kg）**：0.0367 vs OIC 0.0554, IC 0.1375, RL+IC 0.0835
- **消融（无 EMA）**：大物体跟踪误差显著增加（Monitor 0.1189, Stockpot 0.1153）
- **刚度自适应**：搬运重物（5kg chair）时 K 值在 Stage 2（抬升）显著增大


## Limitations

1. 仅在 MuJoCo 仿真验证，未涉及真实机器人
2. 抓取位姿假设已知且稳定，不处理抓取规划
3. 离散化刚度空间（20 倍数）可能限制精细调节
4. 需要完整的动力学模型（M(q), h(q,q̇)）用于 QP 求解
5. 未考虑碰撞避障的轨迹生成


## Key Takeaways

- RL+QP 分层架构是双臂力控的有效范式：RL 调节刚度，QP 保证物理约束
- 离散分类目标比回归更稳定，EMA 约束保证刚度平滑过渡
- 距离约束（‖xL-xR‖=WG）是双臂协同的关键约束，防止物体滑落
- 自适应刚度在搬运重物时表现出阶段性行为：启动低刚→抬升高刚→放置低刚
- QP solver 利用 7-DOF 冗余同时执行阻抗和姿态任务

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[karim|Karim, Md Faizal]]
- [[bollimuntha|Bollimuntha, Shreya]]
- [[das|Das, Autrio]]
