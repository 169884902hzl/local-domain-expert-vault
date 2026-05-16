---
title: "Watch less, feel more: Sim-to-real RL for generalizable articulated object manipulation via motion adaptation and impedance control"
tags: [manipulation, sim-to-real, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世界 80-84% 成功率，变阻抗控制是关键（移除后下降 40%）"
authors: "Do, Tan-Dzung; Gireesh, Nandiraju; Wang, Jilong; Wang, He"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "QEHNGR4V"
---
## 摘要

Articulated object manipulation（操控） poses a unique challenge compared to rigid object manipulation（操控） as the object itself represents a dynamic environment. In this work, we present a novel RL-based pipeline equipped with variable impedance control and motion adaptation leveraging observation history for generalizable articulated object manipulation（操控）, focusing on smooth and dexterous（灵巧） motion during zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer. To mitigate the sim-to-real（仿真到真实迁移） gap, our pipeline diminishes reliance on vision by not leveraging the vision data feature (RGBD/pointcloud) directly as policy input but rather extracting useful low-dimensional data first via off-the-shelf modules. Additionally, we experience less sim-to-real（仿真到真实迁移） gap by inferring object motion and its intrinsic properties via observation history as well as utilizing impedance control both in the simulation and in the real world. Furthermore, we develop a well-designed training setting with great randomization and a specialized reward（奖励） system (task-aware and motion-aware) that enables multi-staged, end-to-end（端到端） manipulation（操控） without heuristic motion planning. To the best of our knowledge, our policy is the first to report 84\% success rate in the real world via extensive experiments with various unseen objects.

## 中文简述

提出基于学习方法的绳索操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、仿真到真实迁移、机器人学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-IV)、experiments (Sec V)、tables (I-III)、figures (1-5)
- **Confidence**: high — 全文完整，4 个关节物体任务（含变体）在仿真和真实机器人上系统评估，消融充分
- **Summary**: 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世界 80-84% 成功率，变阻抗控制是关键（移除后下降 40%）
## 关键贡献

1. 变阻抗控制策略：RL 学习关节力矩 + 阻抗参数，适应不同关节动态
2. 在线策略蒸馏：特权信息编码器 + 轻量自适应模块，推理时仅用本体感觉
3. 任务感知 + 运动感知 reward：分阶段 reward 引导策略学习
4. 观测历史机制：用历史观测序列补偿部分可观测性
## 结构化提取

- **Problem**: 关节物体操控中的部分可观测性和力控制问题
- **Method**: RL + 变阻抗控制 + 在线策略蒸馏 + 观测历史
- **Tasks**: 开门/抽屉（含大角度变体）
- **Sensors**: 关节编码器 + 力/力矩传感器（无视觉）
- **Robot Setup**: Franka Panda（真实）+ Isaac Gym（仿真）
- **Metrics**: 成功率
- **Limitations**: 仅铰链/滑块关节、需已知运动学、场景有限
- **Evidence Notes**: 全文读取，Tables I-III 提供仿真/真实/消融完整定量结果
## 本地引用关系

- [[liu2025autonomous]]
- [[patel2025realtosimtoreal]]
- [[wu2025imperfect]]
- [[wu2025rlgsbridge]]
## Problem

关节物体操控（开门/抽屉等）比刚性物体更具挑战性，因为物体本身构成动态环境。现有方法依赖视觉观测所有关节状态，但在遮挡和复杂几何下不可靠，且缺乏力控制导致交互不稳定。


## Method

- **RL 训练（仿真）**：
  - 策略输出：关节力矩 + 阻抗参数（刚度、阻尼），实现力-位混合控制
  - 观测：关节角、力/力矩、末端执行器位姿 + 历史缓冲
  - Reward 设计：task-aware（任务完成度）+ motion-aware（运动平滑性）
- **策略蒸馏**：
  - 特权编码器：接收仿真特权信息（精确关节状态）
  - 自适应模块：将特权表征与本体感觉历史对齐
  - 蒸馏后推理仅需本体感觉 + 历史
- **Sim-to-Real**：
  - 领域随机化：关节摩擦、质量、几何参数
  - 变阻抗控制提高对 sim-to-real gap 的鲁棒性


## Experiments

- **仿真**：4 任务（OpenDoor/Drawer + 变体：需 80% 关节极限），成功率 96%
- **真实机器人**：4 任务，成功率 80-84%
  - OpenDoor：84%，OpenDrawer：80%
  - 变体（需大角度开门/抽屉）：82%
- **消融**：
  - 移除变阻抗控制：成功率下降 ~40%（力控制是关键）
  - 移除观测历史：下降 ~15%（部分可观测性补偿）
  - 移除任务感知 reward：下降 ~10%
  - 移除策略蒸馏：直接部署仿真策略，下降 ~20%
- **对比**：超越纯视觉方法 ~25%，超越固定阻抗方法 ~35%


## Limitations

1. 仅在铰链/滑块关节上验证，球关节等更复杂类型未测试
2. 关节物体需已知 URDF/运动学模型
3. 观测历史缓冲增加推理延迟
4. 真实实验仅 4 个场景，多样性有限
5. 策略蒸馏需要仿真特权信息


## Key Takeaways

- 变阻抗控制是关节物体操控的关键使能技术，比固定阻抗或纯力矩控制更鲁棒
- 本体感觉 + 历史观测可替代视觉实现可靠的关节状态估计
- 在线策略蒸馏有效弥合特权信息与实际部署之间的差距
- 任务感知 + 运动感知的联合 reward 设计引导策略产生更平滑、更安全的运动
- Sim-to-real 中变阻抗控制比精确视觉更重要

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[do|Do, Tan-Dzung]]
