---
title: "A Real-to-Sim-to-Real Approach to Robotic Manipulation with VLM-Generated Iterative Keypoint Rewards"
tags: [manipulation, VLM, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 IKER（Iterative Keypoint Reward），VLM（GPT-4o）生成基于关键点的 Python 奖励函数用于机器人操控。关键点从 RGB-D 观测中采样，VLM 生成代码将关键点位置映射为标量奖励。Real-to-Sim-to-Real 循环：BundleSDF 重建物体 → FoundationPose 位姿估计 → IsaacGym PPO 训练 → 真实部署。4 任务（Shoe Place/Push, Book Push/Reorient），IKER 自动模式仿真 0.716-0.858，显著优于 pose-based 方法（0.265-0.374）。多步链式任务优于 VoxPoser（4/10 vs 0/10 最后一步）"
authors: "Patel, Shivansh; Yin, Xinchen; Huang, Wenlong; Garg, Shubham; Nayyeri, Hooshang et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "IGDPMPAU"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025，UIUC/Stanford/Columbia，XArm7 真实机器人，4 任务×1280 仿真试验+真实验证，多步链式任务对比 VoxPoser
- **Summary**: 提出 IKER（Iterative Keypoint Reward），VLM（GPT-4o）生成基于关键点的 Python 奖励函数用于机器人操控。关键点从 RGB-D 观测中采样，VLM 生成代码将关键点位置映射为标量奖励。Real-to-Sim-to-Real 循环：BundleSDF 重建物体 → FoundationPose 位姿估计 → IsaacGym PPO 训练 → 真实部署。4 任务（Shoe Place/Push, Book Push/Reorient），IKER 自动模式仿真 0.716-0.858，显著优于 pose-based 方法（0.265-0.374）。多步链式任务优于 VoxPoser（4/10 vs 0/10 最后一步）
## 关键贡献

1. IKER：视觉接地的 Python 奖励函数，基于关键点实现精确 SE(3) 控制
2. 迭代精化机制：VLM 根据执行历史和环境反馈更新奖励函数
3. Real-to-Sim-to-Real 完整循环：无需真实世界演示即可学习新任务
4. 多步任务链式执行：支持错误恢复和策略调整
## 结构化提取

- **Problem**: 开放世界操控的灵活任务规约 + VLM 精确 3D 控制
- **Method**: IKER — VLM 生成关键点奖励函数 + Real-to-Sim-to-Real + PPO
- **Tasks**: Shoe Place/Push, Book Push/Reorient（4 单步 + 1 多步链式）
- **Sensors**: 4× RealSense 静态 + 1× 腕部相机
- **Robot Setup**: XArm7 + IsaacGym 仿真
- **Metrics**: 成功率（关键点距离 < 5cm）
- **Limitations**: 需全方位扫描、单物体仅、VLM 空间推理受限
- **Evidence Notes**: 全文读取，Table I 提供完整对比
## 本地引用关系

- [[dey2025revla]]
- [[garcia2025generalizable]]
- [[liu2025kuda]]
- [[marougkas2025integrating]]
## Problem

开放世界机器人操控的任务规约需要灵活、自适应的目标。现有 VLM 方法缺乏精确 3D 目标位置指定能力，且无法随任务进展适应环境变化。如何利用 VLM 生成既精确（SE(3) 控制）又灵活（迭代调整）的任务规约？


## Method

- **IKER 定义**：f^(i): R^(K×3) → R，将 K 个关键点位置映射为标量奖励
- **关键点采样**：
  - 可操作物体：沿轴极端位置放置关键点（相对于物体中心）
  - 静态物体：表面均匀分布关键点
  - 过近关键点移除（投影距离阈值）
- **VLM 生成奖励函数**：
  - 输入：RGB 观测（带编号关键点标记）+ 语言指令 + 执行历史
  - 输出：Python 代码，包含物体选择、抓取模式、目标关键点坐标
  - GPT-4o 生成，支持任意算术运算
- **奖励函数组合**：
  - r = α_dist·r_dist + α_dir·r_dir + α_align·r_align + α_bonus·r_bonus + α_penalty·r_penalty
  - 距离奖励：接近目标物体；方向奖励：关键点向目标移动
  - 对齐奖励：接近最终位置；成功奖励：持续在阈值内；惩罚：过度运动/掉落
- **Real-to-Sim 转换**：
  - BundleSDF 从视频重建物体 3D mesh
  - FoundationPose 估计物体位姿用于仿真放置
  - 桌面等静态物体用点云重建
- **RL 训练**：
  - IsaacGym + PPO，MLP（256-128-64）+ ELU + actor-critic 共享骨干
  - 状态：末端位姿 + 物体位姿 + 关键点位置 + 目标关键点位置
  - 动作：末端 Δpose（6-DoF），10Hz
  - 训练时间约 5 分钟/任务
  - Domain randomization 桥接 sim-to-real 差距
- **部署**：
  - FoundationPose 实时位姿估计 → 关键点计算
  - AnyGrasp 检测抓取（VLM 预测抓取时）
  - IK 求解关节角度


## Experiments

- **单步任务**（4 任务 × 1280 仿真试验 / 10 真实配置）：
  - 仿真 IKER（标注）：Shoe Place 0.945, Shoe Push 0.871, Book Push 0.901, Book Reorient 0.848
  - 仿真 IKER（自动）：0.778, 0.716, 0.679, 0.858
  - 仿真 Pose-based（自动）：0.353, 0.289, 0.374, 0.265（远低于 IKER）
  - 真实 IKER（自动）：0.7, 0.6, 0.6, 0.7
  - 关键点 vs 位姿：VLM 难以处理 SO(3) 旋转，关键点仅需笛卡尔空间推理
- **多步链式任务**（推鞋盒 → 放右鞋 → 放左鞋，10 配置）：
  - IKER：8/10, 5/10, 4/10（逐步递减）
  - VoxPoser（增强版，有 GT 目标位置+完整计划）：5/10, 1/10, 0/10
- **鲁棒性演示**：
  - 人为干扰恢复：鞋子被碰掉后重新抓取完成
  - 策略调整：放偏后 VLM 生成推动修正动作
  - 抓取失败重规划：大书无法抓取 → 改为推动策略
- **失败分析**：主要来自仿真-真实抓取差异和 VLM 选择错误关键点


## Limitations

1. 需要物体全方位视频扫描获取 mesh
2. Real-to-Sim 未建模动力学参数
3. 仅处理单物体交互（每步）
4. 5 分钟训练时间虽短但仍有改进空间
5. VLM 空间推理能力限制关键点选择精度


## Key Takeaways

- 关键点优于位姿作为 VLM 任务规约：避免 SO(3) 推理困难
- 迭代精化使闭环操控成为可能：VLM 根据执行反馈更新策略
- Real-to-Sim-to-Real 无需真实演示：仅靠 VLM 生成奖励+仿真训练
- Python 代码作为奖励函数表达力强：支持任意算术和条件逻辑
- 多步任务链式执行展示实用性：但成功率逐步递减需改进

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[patel-shivansh|Patel, Shivansh]]
- [[huang|Huang, Wenlong]]
