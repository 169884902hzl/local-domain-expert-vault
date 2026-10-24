---
title: "Pushing in the Dark: A Reactive Pushing Strategy for Mobile Robots Using Tactile Feedback"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出仅依赖触觉反馈的响应式推动策略（RPS），使移动机器人在无视觉和物体模型的情况下推动未知物体到目标位置。电容触觉传感器覆盖机器人底盘，通过接触位置自适应调整底盘运动。Logistic 函数控制自适应率（中心→边缘渐进增加横向速度），Realignment 状态防止接触丢失。仿真 88.19% vs NPS 15.97%/APS 5.56%，真实 100%（25kg 盒+12kg 圆柱）"
authors: "Ozdamar, Idil; Sirintuna, Doganay; Arbaud, Robin; Ajoudani, Arash"
year: "2020"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "J39RTRNA"
---
## 摘要

For mobile robots, navigating cluttered or dynamic environments often necessitates non-prehensile manipulation（操控）, particularly when faced with objects that are too large, irregular, or fragile to grasp. The unpredictable behavior and varying physical properties of these objects signiﬁcantly complicate manipulation（操控） tasks. To address this challenge, this manuscript proposes a novel Reactive Pushing Strategy. This strategy allows a mobile robot to dynamically adjust its base movements in real-time to achieve successful pushing maneuvers towards a target location. Notably, our strategy adapts the robot motion based on changes in contact location obtained through the tactile（触觉） sensor covering the base, avoiding dependence on object-related assumptions and its modeled behavior. The effectiveness of the Reactive Pushing Strategy was initially evaluated in the simulation environment, where it signiﬁcantly outperformed the compared baseline approaches. Following this, we validated the proposed strategy through real-world experiments, demonstrating the robot capability to push objects to the target points located in the entire vicinity of the robot. In both simulation and real-world experiments, the object-speciﬁc properties (shape, mass, friction, inertia) were altered along with the changes in target locations to assess the robustness of the proposed method comprehensively.

## 中文简述

提出基于触觉感知的绳索操控方法，具有接触丰富特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、method (Sec II)、experiments (Sec III-IV)、tables (I-II)、figures (1-7)
- **Confidence**: high — 全文完整，IEEE RA-L 2024，IIT Genoa，Gazebo 仿真 + Kairos 真实移动操控器，3 物体×2 摩擦集×24 目标点，全面对比 NPS/APS baseline
- **Summary**: 提出仅依赖触觉反馈的响应式推动策略（RPS），使移动机器人在无视觉和物体模型的情况下推动未知物体到目标位置。电容触觉传感器覆盖机器人底盘，通过接触位置自适应调整底盘运动。Logistic 函数控制自适应率（中心→边缘渐进增加横向速度），Realignment 状态防止接触丢失。仿真 88.19% vs NPS 15.97%/APS 5.56%，真实 100%（25kg 盒+12kg 圆柱）
## 关键贡献

1. 纯触觉响应式推动策略：无需物体模型、视觉、训练或先验经验
2. 自适应率机制：Logistic 函数根据接触横向距离调整横向/纵向速度比
3. Realignment 状态：接触点进入边缘危险区时优先对齐，防止丢失
4. 全方位推动能力：包括机器人后方和侧面目标（此前方法做不到）
5. 自制电容触觉皮肤：42 个 taxel 覆盖底盘三面，无盲区
## 结构化提取

- **Problem**: 未知物体推动 + 无视觉 + 全方位目标
- **Method**: RPS — 电容触觉反馈 + Logistic 自适应率 + Realignment 状态
- **Tasks**: 移动机器人物体推动（仿真 24 目标 + 真实 8 目标）
- **Sensors**: 自制电容触觉传感器（42 taxel）+ 底盘里程计
- **Robot Setup**: Kairos 移动操控器（全向轮底盘）
- **Metrics**: 目标到达成功率（0.05m 阈值）+ 完成时间
- **Limitations**: 无朝向控制、不避障、仅准静态、无后方传感器
- **Evidence Notes**: 全文读取，Tables I-II + Figs 5-7 提供完整评估
## 本地引用关系

- [[funk2024evetac]]
- [[george2024vital]]
- [[han2025upvital]]
- [[liu2025forcemimic]]
- [[zhao2025polytouch]]
## Problem

移动机器人在杂乱/动态环境中推动物体时，物体形状、质量、摩擦等属性未知且难以建模。现有方法要么依赖物体模型/摩擦假设（实验室限制），要么依赖视觉（遮挡/精度问题），要么仅限前方目标。如何仅用触觉反馈实现全方位目标推动？


## Method

- **硬件平台**：Kairos 移动操控器（全向轮底盘 + UR16e 臂，仅用底盘）
- **电容触觉传感器**：
  - 14 PCB × 3 电极 = 42 taxel，覆盖前/左/右三面
  - 聚氨酯泡沫 + 导电墨水，电容变化检测接触位置
  - 判定接触类型：单 taxel=点接触，多 taxel=线接触（取边界平均）
- **响应式推动策略（RPS）**：
  - 自行车运动学模型避免急转导致失接触
  - 线速度：v_x, v_y 由自适应率 ar 和速度幅值 v* 决定
  - v* = K_v ||d||（距目标距离比例）
  - ar = Logistic(|l|)：接触点在中心时≈0（仅前进），接近边缘时→10（高横向）
  - 角速度：ω = v_x/L · tan(γ)，γ 为转向角
  - 距离阈值内 ar=0 取消横向运动（避免接近目标时偏离）
- **Realignment 状态**：
  - 接触进入危险区（|l| > l_cr）时激活
  - 最大横向速度优先对齐
  - ω 按 σ = 1-|l|/l_cr 缩放（越偏离中心角速度越小）


## Experiments

- **仿真实验**（Gazebo，3 物体 × 2 摩擦集 × 24 目标点 = 144 组合 × 每组重复）：
  - RPS: 88.19%，NPS: 15.97%，APS: 5.56%
  - RPS 是唯一能推动到后方目标的方法
  - 圆柱成功率略低（滚动行为+仅点接触）
  - 失败案例主要为非均匀盒子后方目标
- **真实实验**（25kg 盒 + 12kg 圆柱，各 8 目标点）：
  - 100% 成功率，所有方向目标均达到
  - 平均完成时间：盒子 89s，圆柱 88s
  - 接触点偏离中心平均：盒子 0.032m，圆柱 0.059m
- **关键特性**：
  - 点/线接触类型切换鲁棒
  - 准静态推动假设满足
  - 消除"flat bumper 问题"（全向轮底盘解决）


## Limitations

1. 仅控制物体位置，不控制朝向（需要物体形状/视觉信息）
2. 不避障（需要额外传感器）
3. 仅适用于准静态推动（低速限制）
4. 未在杂乱环境中验证
5. 传感器仅覆盖底盘三面（后方无传感器）


## Key Takeaways

- 触觉反馈足以实现精确推动：无需视觉或物体模型
- 自适应率是核心机制：接触点位置→横向/纵向速度比
- 全向轮底盘是关键使能器：消除非完整约束限制
- Realignment 状态防止接触丢失：从失败中恢复
- 仿真到真实迁移零成本：策略是纯几何/运动学的

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[ozdamar|Ozdamar, Idil]]
