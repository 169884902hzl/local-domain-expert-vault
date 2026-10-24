---
title: "Robotic Sim-to-Real Transfer for Long-Horizon Pick-and-Place Tasks in the Robotic Sim2Real Competition"
tags: [sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算法修改条件下实现仿真-现实一致性能，获第一名。"
authors: "Yang, Ming; Cao, Hongyu; Zhao, Lixuan; Zhang, Chenrui; Chen, Yaran"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "NEIAF6Q9"
---
## 摘要

This paper presents a fully autonomous robotic system that performs sim-to-real（仿真到真实迁移） transfer in complex longhorizon tasks involving navigation, recognition, grasping（抓取）, and stacking in an environment with multiple obstacles.


## 中文简述

提出基于学习方法的抓取方法，具有仿真到真实迁移特点。

**研究方向**: 仿真到真实迁移

## 关键贡献

1. **SMMS（Sequential Motion-blur Mitigation Strategy）**：四步级联策略解决运动模糊——图像增强（RGB通道差分提升对比度）、数据增强（旋转+颜色抖动）、识别拒绝（阈值过滤误检）、数据平滑（外推+低通滤波），使真实环境召回率从50.5%恢复至70.0%
2. **Design Function（DF）+ 反馈线性化**：在全驱底盘模型上通过反馈线性化解耦位姿控制，设计三种衰减模式DF（Type I指数/Type II幂律/Type III PI），Type III消除速度死区导致的稳态误差
3. **模块化系统架构**：检测-分类-定位管线，轻量级CNN分类器（62.1k参数，11ms/帧），全程无需GPU
## 结构化提取

- Problem: 移动机器人长时序拾取-放置任务的Sim-to-Real差距（感知运动模糊 + 执行非线性）
- Method: SMMS运动模糊缓解（图像增强+数据增强+识别拒绝+数据平滑）+ 反馈线性化伺服控制（Type III PI Design Function）
- Tasks: 长时序拾取-放置（导航→识别→抓取→多层堆叠），ICRA 2024 RSC矿物搜索任务
- Sensors: 机载RGB相机（ArUco标记检测）
- Robot Setup: 全向移动底盘 + 机械臂 + 夹爪，Intel NUC11PAHi7（无GPU）
- Metrics: 召回率、错误率、位姿精度(S_pos/S_att)、伺服最终误差、对准时间、抓取/堆叠成功率
- Limitations: 依赖ArUco标记、竞赛特定环境、未在工业场景验证、仿真碰撞处理缺陷
- Evidence Notes: 全文5248词，3张实验表，7张图，完整公式推导，开源代码
## 本地引用关系

- [[do2025watch]]
- [[patel2025realtosimtoreal]]
- [[qureshi2025splatsim]]
- [[wang2023multistage]]
- [[wu2025rlgsbridge]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~5248 词），含所有实验表格（Table I-III）、公式推导、系统架构描述
- Confidence: high — 全文可读，实验数据完整，方法细节清晰
- Summary: 针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算法修改条件下实现仿真-现实一致性能，获第一名。


## Problem

移动机械臂在长时序拾取-放置（pick-and-place）任务中面临Sim-to-Real差距，主要表现为：
1. **感知差距（Sensing Discrepancies）**：移动相机运动模糊导致ArUco标记检测召回率从仿真96%骤降至真实50.5%，颜色/纹理差异、背景干扰
2. **执行差距（Actuation Discrepancies）**：仿真中不合理的抓取姿态（gripper穿透物体）、实际动力学中的未建模非线性（速度死区、传输延迟、饱和）
3. 现有方法的局限：域随机化难以处理运动模糊，迁移学习需要大量真实交互数据


## Method

### 视觉感知系统（SMMS管线）
1. **图像增强**：feature = R + k·max(R-B, 0) - G，提升红色标记边界对比度
2. **ArUco检测**：提取轮廓 → 透视变换 → CNN分类（类LeNet5架构，3层卷积-dropout-pooling + 3层全连接）
3. **数据增强**：±10度随机旋转 + 亮度/对比度/饱和度/色调扰动
4. **识别拒绝**：基于未缩放分类分数分布的阈值规则
5. **数据平滑**：低通滤波 p_n = a·p_{n-1} + (1-a)·p_obs_n + 外推未检测标记

### 伺服控制系统（反馈线性化 + DF）
1. 底盘运动学建模：全向底盘，状态(x, y, θ)，输入(vx, vy, ω)
2. 反馈线性化：ė = f(e, t)，通过逆动力学计算控制输入
3. 三种DF选择：
   - Type I: f(e,t) = -k_p·e → 指数衰减，稳态误差 e_ss = m/k_p（对死区敏感）
   - Type II: f(e,t) = -k_p·e^α, 0<α<1 → 幂律衰减，e_ss = (m/k_p)^{1/α}（比I优但仍不足）
   - Type III: f(e,t) = -k_p·e - k_i∫e → 二阶系统，消除稳态误差（最终选择）


## Experiments

### 视觉感知评估
- **对比方法**：Vanilla ArUco vs Ours w/o SMMS vs Ours w/ SMMS
- **仿真结果**：召回率96.0%→91.6%，错误率0%，位置精度0.8cm，姿态精度1.0°
- **真实结果**：召回率49.2%→50.5%→70.0%，错误率0%，位置精度0.6cm，姿态精度1.9°
- **运行速度**：检测6.68ms + 分类3.60ms + PnP 0.86ms = 11.14ms/帧

### 伺服控制评估（Type III, k_p=4, k_i=2）
- **对比方法**：Open-loop / PID / Ours(Type III)
- **仿真结果**：误差0.48cm(x), 0.40cm(y), 0.61°(θ)，对准时间4.06s
- **真实结果**：误差0.81cm(x), 0.63cm(y), 2.18°(θ)，对准时间4.12s
- Open-loop和PID在真实环境中均超时失败

### 完整系统评估（2024 RSC竞赛）
- **仿真**：抓取成功率30/30，堆叠成功率22/30（仿真碰撞抖动导致掉落）
- **真实**：抓取成功率6/6，堆叠成功率6/6（100%，唯一完成三层堆叠的队伍）
- **硬件**：Intel NUC11PAHi7, 8GB RAM，无独立GPU


## Limitations

1. 竞赛导向工程方案，依赖ArUco基准标记，不具备通用物体识别能力
2. 未在工业生产环境中验证，作者明确说明需进一步适配
3. 仿真中堆叠失败率约1/6，源于仿真器碰撞处理缺陷
4. CNN分类器训练仅需5-9个样本/类，泛化能力未在其他场景验证
5. 仅在全向底盘上验证，未扩展到其他机器人平台


## Key Takeaways

1. 不使用RL或域随机化，纯经典控制+轻量视觉即可实现Sim-to-Real一致性性能
2. 运动模糊是移动机械臂Sim-to-Real的核心感知差距，SMMS四步级联策略有效
3. 反馈线性化+PI型DF可消除执行器非线性（死区/延迟/饱和）的影响
4. 竞赛环境中100%成功率证明工程方案的可靠性，但泛化性待验证

## 相关概念

- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[yang|Yang, Ming]]
