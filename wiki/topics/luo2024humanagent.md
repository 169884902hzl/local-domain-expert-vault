---
title: "Human-agent joint learning for efficient robot manipulation skill acquisition"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出人机联合学习（HAJL）框架：人类操作员与学习型辅助 agent 共享控制机器人末端执行器，进行数据收集。控制比可调（human:agent），随数据积累 agent 逐渐学习，人类注意力需求降低。仿真+真实实验表明：数据收集效率提升，人类适应需求减少，下游策略性能不降。适用于灵巧手、夹爪等多种末端执行器"
authors: "Luo, Shengcheng; Peng, Quanquan; Lv, Jun; Hong, Kaiwen; Driggs-Campbell, Katherine Rose et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "FNCGX9QF"
---
## 摘要

Employing a teleoperation system for gathering demonstrations offers the potential for more efficient learning of robot manipulation（机器人操控）. However, teleoperating a robot arm equipped with a dexterous（灵巧） hand or gripper, via a teleoperation system presents inherent challenges due to the task’s high dimensionality, complexity of motion, and differences between physiological structures. In this study, we introduce a novel system for joint learning between human operators and robots, that enables human operators to share control of a robot end-effector with a learned assistive agent, simplifies the data collection process, and facilitates simultaneous human demonstration（示范数据） collection and robot manipulation（机器人操控） training. As data accumulates, the assistive agent gradually learns. Consequently, less human effort and attention are required, enhancing the efficiency of the data collection process. It also allows the human operator to adjust the control ratio to achieve a tradeoff between manual and automated control. We conducted experiments in both simulated environments and physical realworld settings. Through user studies and quantitative evaluations, it is evident that the proposed system could enhance data collection efficiency and reduce the need for human adaptation while ensuring the collected data is of sufficient quality for downstream tasks. For more details, please refer to our webpage https://norweig1an.github.io/HAJL.github.io/.

## 中文简述

提出基于学习方法的灵巧手方法。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method、experiments、tables、figures (1-9)
- **Confidence**: high — 全文完整，arXiv 2024 预印本（v4），SJTU + UIUC，仿真+真实用户研究+定量评估
- **Summary**: 提出人机联合学习（HAJL）框架：人类操作员与学习型辅助 agent 共享控制机器人末端执行器，进行数据收集。控制比可调（human:agent），随数据积累 agent 逐渐学习，人类注意力需求降低。仿真+真实实验表明：数据收集效率提升，人类适应需求减少，下游策略性能不降。适用于灵巧手、夹爪等多种末端执行器
## 关键贡献

1. 人机联合学习框架：数据收集与策略学习同时进行
2. 共享控制机制：人类意图 + 辅助 agent 自动填充细节
3. 可调控制比：初期人类主导→后期 agent 自动化
4. 数据质量保证：共享控制产生的数据适用于下游任务
## 结构化提取

- **Problem**: 遥操作数据收集效率低 + 人类适应成本高
- **Method**: HAJL — 共享控制（human+agent）+ 在线学习 + 可调控制比
- **Tasks**: 仿真操控 + 真实用户研究（灵巧手/夹爪）
- **Sensors**: 视觉手部追踪
- **Robot Setup**: 仿真 + 真实机械臂
- **Metrics**: 数据收集时间、下游策略成功率、用户主观评价
- **Limitations**: 初始无帮助、误差引入、手动控制比、有限任务
- **Evidence Notes**: 全文读取，仿真+真实用户研究
## 本地引用关系

- [[chen2025effective]]
- [[gao2024prime]]
- [[liu2025forcemimic]]
- [[wu2025imperfect]]
## Problem

遥操作数据收集面临高维度、复杂运动和生理结构差异的挑战。传统范式先收集数据后训练策略，效率低且需要人类大量适应。如何让数据收集和策略学习同步进行，减少人类工作量？


## Method

- **共享控制**：
  - 人类操作员：提供运动意图和主要框架（通过视觉遥操作）
  - 辅助 agent：学习人类操作模式，自动填充细节动作
  - 控制比 α：a = α·a_human + (1-α)·a_agent
  - α 从高（人类主导）逐渐降低（agent 自动化）
- **辅助 agent 训练**：
  - 从收集的数据中在线学习
  - 随数据量增长，agent 性能提升
  - 学习人类操作风格和任务结构
- **数据收集流程**：
  - 人类通过遥操作系统控制机器人
  - agent 同时辅助（减少人类工作量）
  - 收集的轨迹数据同时用于训练 agent 和下游策略
- **视觉遥操作**：
  - 手部姿态估计 → 机器人末端控制
  - 支持灵巧手和夹爪


## Experiments

- **仿真实验**：
  - 数据收集效率：联合学习显著减少人类操作时间
  - 下游策略质量：共享控制数据训练的策略性能与纯人类数据相当
  - 消融：不同控制比（0.3/0.5/0.7）的影响
- **真实用户研究**：
  - 参与者使用 HAJL vs 传统遥操作
  - 主观评价：工作量减少、操作更容易
  - 客观指标：任务完成时间、数据质量
- **下游任务**：
  - 使用收集数据训练的行为克隆策略
  - 联合学习数据训练的策略成功率不显著低于纯人类数据


## Limitations

1. 辅助 agent 初始阶段无帮助，需要一定数据量才能有效
2. 共享控制可能引入 agent 误差
3. 控制比调度策略需要手动设定
4. 仅在有限任务上验证
5. 视觉遥操作的精度受限


## Key Takeaways

- 数据收集和策略学习的同步是效率提升的关键
- 共享控制不降低数据质量：agent 填充细节而非改变意图
- 渐进式自动化（人类→agent）是自然的训练范式
- 人类意图+agent 细节是互补分工：人类负责高层规划，agent 负责低层执行
- 用户研究表明减少工作量而不牺牲数据质量

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[grasping]]

## 相关研究者

- [[luo|Luo, Shengcheng]]
- [[hong|Hong, Kaiwen]]
