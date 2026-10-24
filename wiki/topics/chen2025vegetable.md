---
title: "Vegetable Peeling: A Case Study in Constrained Dexterous Manipulation"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出约束灵巧操控框架，用 Allegro 手在 Franka 臂上通过 RL 学习可控停止的蔬菜重定向策略，实现重定向→牢固握持→削皮的多步骤循环，4 种蔬菜上 90% 牢固握持成功率"
authors: "Chen, Tao; Cousineau, Eric; Kuppuswamy, Naveen; Agrawal, Pulkit"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "87SRPM7J"
---
## 摘要

Recent studies have made significant progress in addressing dexterous manipulation（灵巧操控） problems, particularly in inhand object reorientation. However, there are few existing works that explore the potential utilization of developed dexterous manipulation（灵巧操控） controllers for downstream tasks. In this study, we focus on constrained dexterous manipulation（灵巧操控） for food peeling. Food peeling presents various constraints on the reorientation controller, such as the requirement for the hand to securely hold the object after reorientation for peeling. We propose a simple system for learning a reorientation controller that facilitates the subsequent peeling task. Videos are available at: https://taochenshh.github.io/projects/veg-peeling.

## 中文简述

提出基于学习方法的灵巧手方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、results (Sec IV)、ablation (Sec IV.E)、figures (1-7)、tables (I)
- **Confidence**: high — 全文完整，方法描述详尽，真实机器人实验充分
- **Summary**: 提出约束灵巧操控框架，用 Allegro 手在 Franka 臂上通过 RL 学习可控停止的蔬菜重定向策略，实现重定向→牢固握持→削皮的多步骤循环，4 种蔬菜上 90% 牢固握持成功率
## 关键贡献

1. 提出基于 stop signal 的重定向控制器，可按需停止并牢固握持物体
2. 使用 keyframe 演示简化 reward shaping（仅需一个关键帧姿态）
3. Teacher-student 学习框架：RL goal-conditioned teacher → stop-signal student (Transformer)
4. 完整的蔬菜削皮系统：Allegro 手重定向 + Franka 臂削皮（遥操作/视觉）
## 结构化提取

- **Problem**: 灵巧手重定向控制器的下游任务适配（削皮约束）
- **Method**: Teacher-student RL + stop-signal 策略 + keyframe reward
- **Tasks**: 蔬菜重定向 + 削皮（南瓜、甜瓜、萝卜、木瓜）
- **Sensors**: 本体感觉（关节位置+速度），无视觉
- **Robot Setup**: Allegro Hand + Franka Panda 双臂
- **Metrics**: 旋转距离、停止时间、牢固握持率（抬升 3s）
- **Limitations**: 盲控滑出、小物体困难、分割失败
- **Evidence Notes**: 全文读取，Fig 6 + Table I 提供定量结果，4 种蔬菜验证
## 本地引用关系

- [[han2025upvital]]
- [[liu2025forcemimic]]
- [[zhao2025polytouch]]
## Problem

灵巧手物体重定向控制器难以直接应用于下游任务（如削皮），因为需要满足多重约束：能停止运动、牢固握持抗外力、沿特定轴原地旋转、手指不遮挡削皮面。


## Method

- **Teacher 策略**：goal-conditioned RL（Isaac Gym），奖励 = 任务成功 + 旋转角度 + 关键帧姿态约束
- **Student 策略**：stop-signal conditioned，Transformer 架构，DAGGER 训练
- **关键创新**：成功准则添加时间约束（连续 T 步满足旋转+接触），解决振荡问题
- **动作插值**：用前一步命令而非当前位置作为参考，避免 PD 控制器抖动


## Experiments

- **硬件**：Allegro Hand (300Hz PD) + Franka Panda (削皮臂)，Isaac Gym 仿真
- **物体**：南瓜(827g)、甜瓜(623g)、萝卜(727g)、木瓜(848g)
- **重定向**：3.5s 命令时 90% 超过 4cm，7s 命令时 90% 超过 7.3cm
- **停止响应**：收到 stop signal 后平均 0.4s 停止
- **牢固握持**：90% 成功率（7s 命令时 92.5%）
- **消融**：keyframe reward 显著提升学习效率；Transformer 优于 RNN


## Limitations

1. 仅依赖本体感觉（盲控），物体可能滑出
2. 小物体时手指难以接触
3. Grounded SAM 分割偶尔失败
4. 视觉削皮仅沿最长轴，不够灵活


## Key Takeaways

- 下游任务约束可通过 reset 条件和 reward 塑形有效融入 RL 训练
- Keyframe 演示（单帧）是比复杂 reward shaping 更简单的方案
- Stop-signal 设计比 goal-conditioned 更适合下游集成
- Transformer 优于 RNN 用于 POMDP 灵巧操控

## 相关概念

- [[robotic-manipulation]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[chen-tao|Chen, Tao]]
- [[cousineau|Cousineau, Eric]]
- [[kuppuswamy|Kuppuswamy, Naveen]]
