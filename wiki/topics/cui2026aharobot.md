---
title: "AhaRobot: A Low-Cost Open-Source Bimanual Mobile Manipulator for Embodied AI"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出 $1000 开源双臂移动操作平台 AhaRobot，SCARA 式水平臂+升降导轨+双电机消间隙控制实现 0.7mm 重复定位精度，配套 26 面标记手柄 RoboPilot 实现 $50 全远程遥操作，数据质量与 VR 相当。"
authors: "Cui, Haiqin; Yuan, Yifu; Zheng, Yan; Hao, Jianye"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QVNG528R"
---
## 摘要

Scaling Vision-Language-Action models for embodied manipulation（操控） demands large volumes of diverse manipulation（操控） data, yet the high cost of commercial mobile manipulators and teleoperation interfaces that are difficult to deploy at scale remain key bottlenecks. We present AhaRobot, a low-cost, fully open-source bimanual（双臂） mobile manipulator tailored for Embodied-AI. The system contributes: (1) a SCARA-like dual-arm（双臂） hardware design that reduces motor torque demands while maintaining a large vertical reachable workspace, (2) an optimized control stack that improves precision via dual-motor backlash mitigation and static-friction compensation through dithering, and (3) RoboPilot, a teleoperation interface featuring a novel 26-faced marker handle for precise, long-horizon（长时序） remote data collection. Experimental results show that our hardware-control co-design achieves 0.7 mm repeatability at a total hardware cost of only $1,000. The proposed 26-faced handle reduces tracking error by 80% over a 6-faced baseline and improves data-collection efficiency by 30%, while robustly handling singularities and supporting extremely long-horizon（长时序） tasks in fully remote settings. Despite its low cost, AhaRobot enables imitation learning（模仿学习） of complex household behaviors involving bimanual（双臂） coordination, upper-body mobility, and contact-rich（接触丰富） interaction, with data quality comparable to VR-based collection. All software, CAD files, and documentation are available at https://aha-robot.github.io.

## 中文简述

提出基于模仿学习的双臂方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **硬件设计**：SCARA 式水平双臂 + 升降导轨，消除关节抗重力扭矩需求，全部使用现成零件，总成本 $1,000，垂直工作空间 1250mm，可触达地面。
2. **控制优化**：双电机对抗消间隙 + 抖动摩擦补偿 + 梯形运动剖面，在低成本舵机上实现 0.7mm 重复定位精度，可跟踪最小 2 个编码器分辨率的增量目标。
3. **RoboPilot 遥操作**：26 面多面体标记手柄，$50 成本，跟踪误差比 6 面手柄降低 80%，支持全远程操作，数据质量与 VR（Meta Quest Pro）相当。
4. **开源生态**：完整 CAD、控制软件、部署文档，三天可从零组装。
## 结构化提取

- Problem: 双臂移动操作平台成本过高（$30,000+）且遥操作难以大规模部署，限制了 VLA 模型数据 scaling
- Method: SCARA 式水平双臂 + 升降导轨消除抗重力需求 + 双电机消间隙控制 + 26 面标记手柄 RoboPilot 遥操作 + WebRTC 全远程界面
- Tasks: 6 类 — 空间搬运(Box Transfer)、双臂协调(Pen Insertion)、全身操控(Floor-to-table Pick)、接触丰富(Can Pressing)、长时序接触(Table Cleaning)、双臂长时序(Pan Sweeping)；2 个长时序远程任务(送咖啡200m+、取食物+微波炉)
- Sensors: 3× 640×360@30Hz 摄像头（头部 2-DoF 云台 + 左右手腕）；光电开关（升降归零）；编码器（关节位置）
- Robot Setup: 双臂 4-DoF SCARA 式 + 升降导轨 + 差速底盘；Feetech STS3215 舵机×8（双电机/关节）；BLDC×2（底盘）；Mini-ITX(i5-12700KF+RTX4060)+5×ESP32+ODrive3.6；ROS 2 Humble；总成本 $1,000（不含计算）/$1,800（含 RTX4060）
- Metrics: 重复定位精度 0.72mm(±3σ)；手柄跟踪误差（旋转↓80%、平移↓79%）；空间分辨率~1mm；遥操作成功率 100%（3 任务平均）；IL 成功率 50%-100%（按任务）；RoboPilot vs VR 73% vs 70%
- Limitations: 机身 51kg 缺碰撞感知；网络延迟限制动态任务；π0 无时序记忆；action chunking 不连续；单臂负载 1.5kg 有限；未集成自主导航
- Evidence Notes: (1) 双电机消间隙+抖动补偿使低成本舵机达到 0.7mm 重复定位精度；(2) 26 面手柄任意视角保持≥3 个非共面标记可见，消除 PnP 歧义，旋转误差降至 1.094°；(3) RoboPilot 数据质量与 Meta Quest Pro 相当（73% vs 70% SR），成本仅 1/30；(4) 位置控制显著优于速度控制用于底盘策略学习；(5) Floor-to-table Pick 任务展示了升降能力的独特价值，Mobile ALOHA 无法完成
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文 22 页，涵盖硬件设计、控制、遥操作、6 组实验、imitation learning）
- Confidence: high
- Summary: 提出 $1000 开源双臂移动操作平台 AhaRobot，SCARA 式水平臂+升降导轨+双电机消间隙控制实现 0.7mm 重复定位精度，配套 26 面标记手柄 RoboPilot 实现 $50 全远程遥操作，数据质量与 VR 相当。

## Problem

VLA 模型 scaling 需要大量多样化操控数据，但现有双臂移动操作平台存在两大瓶颈：(1) 工业级平台成本 $30,000+，绝大多数实验室无法承担；(2) 现有遥操作方案（VR 头显笨重不适长时远程、Leader-Follower 需现场操作、SpaceMouse 坐标系混乱）难以大规模部署。低成本平台则在精度和工作空间上做妥协，无法完成精细家务操控。

## Method

### 硬件架构
- **形态**：升降导轨（同时作为上身结构）+ 水平 SCARA 式双臂 + 差速驱动底盘
- **核心设计思想**：通过结构消除抗重力需求，使低成本舵机（Feetech STS3215，$15/个）即可胜任
- **双电机关节**：每个关节两个舵机对向施加预紧力，模拟拮抗肌对，消除齿轮间隙
- **升降**：皮带传动滑台（比丝杠快、比气缸精），两根导轨同时作为上身框架
- **底盘**：前置两个 BLDC + 后万向轮，零转弯半径，扫过半径 50cm
- **传感/计算**：3 个 640×360@30Hz 摄像头（头部云台 + 左右手腕）；Mini-ITX（i5-12700KF + RTX4060）；5 个 ESP32 分布式低层控制 + ODrive 3.6 驱动底盘；ROS 2 Humble
- **供电**：24V/20Ah 锂电池（驱动器）+ 1kWh 便携 AC（计算），续航 4-5h
- **参数**：单臂负载 1.5kg，臂展 750mm，总重 51kg，尺寸 550×500×1550mm

### 双关节控制
- **消间隙**：双电机施加对向偏置电压 V_b，保持齿轮齿面常接触（公式：V₁ = V_c + V_b, V₂ = V_c - V_b）
- **摩擦补偿**：高频抖动前馈项 V_d，使电机始终处于接近静摩擦阈值的微振动状态，消除稳态误差
- **梯形剖面**：将参考位置转换为加-匀-减速三段平滑轨迹，限制加速度和巡航速度，抑制振动

### RoboPilot 遥操作
- **26 面标记手柄**：基于立方体的 26-连通邻域设计，任意视角至少 3 个非共面 AprilTag 可见，消除平面 PnP 歧义
- **位姿估计**：Levenberg-Marquardt 最小化重投影误差求解 SE(3)
- **运动学映射**：手柄 6-DoF 位姿 → 逆运动学优化（SE(3) log 距离最小化）→ 关节空间
- **脚踏板**：4 个霍尔效应踏板，行走模式（底盘移动/旋转）和操作模式（夹爪开合/升降控制）可切换
- **Web 界面**：WebRTC 视频流 + DataChannel 控制指令，客户端 OpenCV.js 本地检测，支持蜂窝网络远程

## Experiments

### RQ1 控制精度
- 抖动启用后成功跟踪 0.175°（2 倍编码器分辨率）阶梯目标；禁用时完全无法跟踪
- 消间隙启用后方波跟踪无振荡；禁用时目标点附近持续振荡
- **重复定位精度**：15 次单方向接近，均值 5.79mm，标准差 0.12mm，±3σ = 0.72mm

### RQ2 手柄跟踪精度
| 指标 | 6 面手柄 | 26 面手柄（本文） |
|------|---------|------------------|
| 平均旋转误差 | 5.391° | 1.094°（↓80%） |
| 平均平移误差 | 9.9 mm | 2.1 mm（↓79%） |

- 6 面手柄出现周期性误差尖峰（标记面接近平行于相机平面时 PnP 歧义）
- 26 面手柄全程平滑无尖峰
- **空间分辨率**：约 1mm（角点精化启用时）

### RQ3 远程长时序任务
- Task 1（送咖啡）：移动距离超 200m，完全远程完成
- Task 2（取食物+微波炉加热）：需地面拾取→桌面放置，Mobile ALOHA 无法完成
- 均通过蜂窝网络 WebRTC 远程操作，无需现场辅助

### RQ4 遥操作效率对比

| 任务 | RoboPilot SR/Time | SpaceMouse SR/Time | Leader-Follower SR/Time |
|------|-------------------|--------------------|-----------------------|
| 插盘入架 | 100%/36.6s | 44.4%/47.3s | 100%/57.4s |
| 开抽屉放橡皮 | 100%/72.6s | 100%/84.0s | 100%/82.7s |
| 试管插入 | 100%/26.4s | 100%/44.9s | 100%/55.9s |
| **平均** | **100%/45.2s** | **81.5%/58.7s** | **100%/65.3s** |
| **成本** | **$50** | $220 | $260 |

### RQ5 Imitation Learning（ACT + π0，每任务 10 次评估）

| 任务 | 类别 | 演示数 | ACT SR | π0 SR |
|------|------|--------|--------|-------|
| Box Transfer | 空间 | 50 | 100% | - |
| Pen Insertion | 双臂 | 50 | 60% | - |
| Floor-to-table Pick | 全身 | 80 | 70% | - |
| Can Pressing | 接触 | 50 | - | 60% |
| Table Cleaning | 接触/长 | 200 | 70% | - |
| Pan Sweeping | 双臂/长 | 200 | 50% | - |

- **Floor-to-table Pick**：Mobile ALOHA 无法完成（无升降能力），凸显垂直工作空间价值
- **位置 vs 速度控制消融**（底盘）：速度控制因训练数据尖峰导致策略无法移动；位置控制学习到平滑轨迹
- **RoboPilot vs VR 对比**（Can Pressing, Table Cleaning, Pan Sweeping）：平均 SR 73% vs 70%，差异在实验方差范围内；RoboPilot 成本 $50 vs VR $1,500

## Limitations

1. 机身较重（51 kg），缺少碰撞感知，移动中有安全隐患
2. 视觉遥操作受网络传输延迟影响，高动态任务响应受限
3. π0 无时序记忆，按压任务可能提前终止
4. Table Cleaning 和 Pan Sweeping 中 action chunking 导致指令不连续，工具错位或倾倒
5. 单臂负载仅 1.5 kg，限制了大物体操控
6. 仅测试了 ACT 和 π0 两种 IL 算法，未验证 RL 或 VLA 方法
7. 未集成自主导航能力

## Key Takeaways

### 对 DLO 操控的启示
- RoboPilot 的 26 面标记手柄方案可用于 DLO 数据采集的远程遥操作，低成本且精确
- 双电机消间隙 + 抖动补偿是低成本关节提升精度的有效手段，可用于 DLO 柔顺操控平台
- 位置控制优于速度控制（底盘移动）的发现，对 DLO 长时序全身操控策略有参考价值
- 升降导轨设计使平台可触达地面，对 DLO 拾取/悬挂等跨高度任务有直接价值

### 对 VLM-based control 的启示
- 平台设计目标即为 VLA 模型数据采集，与我们的 VLM 研究方向一致
- RoboPilot 收集的数据质量与 VR 相当，验证了低成本大规模数据采集的可行性
- 18 维机器人状态 + 3 路相机输入的策略输入格式可供参考

### 方法论价值
- 26 面多面体设计巧妙解决了 PnP 平面歧义问题，是 marker-based teleoperation 的重要改进
- 梯形运动剖面 + 分布式 ESP32 控制的架构简洁实用
- 全开源+三天组装的门槛极低，有利于社区复现和众包数据采集

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[cui-haiqin|Cui, Haiqin]]
- [[yuan|Yuan, Yifu]]
- [[zheng-yan|Zheng, Yan]]
- [[hao-jianye|Hao, Jianye]]
