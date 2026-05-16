---
title: "Integrating Model-Based Control and RL for Sim2Real Transfer of Tight Insertion Policies"
tags: [RL, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖励）。自适应课程（噪声+动作幅度递增），2-3 小时训练（vs IndustReal 8-10h）。仿真 96.25%（5mm noise），真实 48/50（已知物体）+ 39/50（未知家居物体），全面超越 IndustReal"
authors: "Marougkas, Isidoros; Ramesh, Dhruv Metha; Doerr, Joe H.; Granados, Edgar; Sivaramakrishnan, Aravind et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "XK9G844G"
---
## 摘要

Object insertion under tight tolerances (< 1mm) is an important but challenging assembly（装配） task as even small errors can result in undesirable contacts. Recent efforts focused on Reinforcement Learning（强化学习） (RL), which often depends on careful definition of dense reward（奖励） functions. This work proposes an effective strategy for such tasks that integrates traditional modelbased control with RL to achieve improved insertion accuracy. The policy is trained exclusively in simulation and is zero-shot（零样本） transferred to the real system. It employs a potential field-based controller to acquire a model-based policy for inserting a plug into a socket given full observability in simulation. This policy is then integrated with residual RL, which is trained in simulation given only a sparse, goal-reaching reward（奖励）. A curriculum scheme over observation noise and action magnitude is used for training the residual RL policy. Both policy components use as input the SE(3) poses of both the plug and the socket and return the plug’s SE(3) pose transform, which is executed by a robotic arm using a controller. The integrated policy is deployed on the real system without further training or fine-tuning, given a visual SE(3) object tracker. The proposed solution and alternatives are evaluated across a variety of objects and conditions in simulation and reality. The proposed approach outperforms recent RL-based methods in this domain and prior efforts with hybrid policies. Ablations highlight the impact of each component of the approach. For more information please refer to the corresponding website.

## 中文简述

提出基于强化学习的插入方法，具有仿真到真实迁移特点。

**研究方向**: 强化学习、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、results (Sec IV)、tables (I-II)、figures (1-9)
- **Confidence**: high — 全文完整，ICRA 2025 论文，IsaacGym 仿真 + Kuka iiwa 真实机器人，3 类物体（NIST Taskboard+自定义+家居物体），零样本迁移，与 IndustReal 对比
- **Summary**: 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖励）。自适应课程（噪声+动作幅度递增），2-3 小时训练（vs IndustReal 8-10h）。仿真 96.25%（5mm noise），真实 48/50（已知物体）+ 39/50（未知家居物体），全面超越 IndustReal
## 关键贡献

1. 势场模型策略 + 残差 RL 的混合架构：模型策略提供强先验，RL 补偿噪声
2. 仅用稀疏目标奖励训练残差 RL：势场提供密集指导，无需手工奖励工程
3. 自适应课程学习：噪声和动作幅度递增，按成功率自动调节难度
4. 零样本 sim-to-real 迁移：不同机器人（Franka→Kuka）间迁移成功
5. 训练效率：2-3h vs IndustReal 8-10h，成功率更高
## 结构化提取

- **Problem**: 紧公差插入（<1mm）+ 感知噪声 + sim-to-real 迁移
- **Method**: 势场模型策略 + 残差 RL（PPO）+ 自适应噪声课程
- **Tasks**: Peg-in-hole（3 类物体，0.1-2mm tolerance）
- **Sensors**: RGB-D（RealSense D435）+ M3T 位姿跟踪
- **Robot Setup**: IsaacGym（Franka）→ Kuka iiwa 14 + Robotiq 3-finger
- **Metrics**: 插入成功率（仿真+真实）
- **Limitations**: 需 3D 模型、仅 top-down、小物体跟踪
- **Evidence Notes**: 全文读取，Tables I-II 提供完整仿真+消融结果
## 本地引用关系

- [[do2025watch]]
- [[karim2024davil]]
- [[liu2025autonomous]]
## Problem

紧公差插入（<1mm）面临感知噪声、接触动力学不确定和 sub-mm 精度要求。纯 RL 方法需要精心设计密集奖励，纯模型方法在噪声下性能急剧下降。如何结合模型控制的结构化优势与 RL 的适应性？


## Method

- **势场策略**：
  - 吸引力：沿 nominal 路径（插座中轴直线）吸引插头向目标
  - 排斥力：最近点对距离 < 阈值时推开插头避免碰撞
  - 综合：at = wTr·(aAtt + aRep)_Tr + wRot·(aAtt + aRep)_Rot
  - 无噪声下 ~100% 成功率
- **残差 RL（PPO）**：
  - atT = atPF + β·atRL（β 从 0→1 课程化）
  - Actor：3 层 MLP + 2 层 LSTM
  - Critic：3 层 MLP（+特权信息：真实位姿）
  - 奖励：稀疏（成功+正，穿透-负）
  - 观察：插头和插座的 SE(3) 位姿估计（含噪声）
- **课程学习**：
  - 噪声：0→nmax（5mm/5°），步长 0.1mm
  - β：0→1（模型策略→RL 主导）
  - 自适应：成功率 >75% 增加难度，<50% 降低难度
- **训练随机化**：
  - 插座：±10cm(x-y), ±5cm(z), ±5°(yaw)
  - 插头：±10mm(x-y), ±15°(roll/yaw/pitch)
  - 噪声：插头 ±5mm/5°，插座 ±1mm/1°
- **Sim-to-Real**：
  - IsaacGym 仿真 → Kuka iiwa 14 + Robotiq 3-finger gripper
  - M3T RGB-D 位姿跟踪器（30Hz）
  - 任务阻抗控制器


## Experiments

- **仿真（IsaacGym）**：
  - NIST 物体（0.5-0.6mm tolerance）：100%/96.1%/96.25%（0/1/5mm noise）
  - 自定义物体（0.1-2mm tolerance）：99.09%/98.28%/95.88%
  - vs IndustReal：92.4%/88.6%（仅 1mm）vs 100%/96.1%
  - vs 时间课程 [12]：97.5%/33.87%（5mm）vs 96.25%/95.88%
- **真实（Kuka iiwa）**：
  - 已知物体：与 IndustReal 对比，全面超越（2-prong 10/10 vs 10/10，3-prong 10/10 vs 7/10）
  - 自定义物体：圆柱 10/10（Easy/Medium/Hard），矩形 10/10/3/10（Easy/Medium/Hard）
  - 未知家居物体：2-prong 10/10、3-prong 10/10、cups 10/10、marker 10/10、HAN 9/10
- **消融**：
  - 仅 PF：无噪声 98.91%，5mm 噪声 3.28%
  - PF+RL（无课程）：5mm 噪声 61.09%±45.18%（不稳定）
  - PF+RL+课程：5mm 噪声 95.88%


## Limitations

1. 推理时需要 3D 物体模型（位姿跟踪器需要）
2. 排斥力计算基于最近点对，对复杂几何可能不够
3. 仅验证 top-down 插入
4. 小物体跟踪精度下降（遮挡）
5. 非工业场景可能缺乏 3D 模型


## Key Takeaways

- 模型策略+残差 RL 是高精度操控的有效范式：模型提供结构化先验，RL 补偿不确定性
- 稀疏奖励在模型策略辅助下可行：避免了密集奖励工程
- 自适应课程是关键：按成功率调节难度比固定时间表更有效
- SE(3) 动作空间促进跨机器人迁移（Franka→Kuka）
- 势场的物理直觉（吸引+排斥）提供了比纯 RL 更好的初始化

## 相关概念

- [[reinforcement-learning]]
- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[marougkas|Marougkas, Isidoros]]
