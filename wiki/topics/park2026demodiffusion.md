---
title: "DemoDiffusion: One-Shot Human Imitation using pre-trained Diffusion Policy"
tags: [manipulation, imitation, RL, diffusion]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。"
authors: "Park, Sungjae; Bharadhwaj, Homanga; Tulsiani, Shubham"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "W9C7EMSU"
---
## 摘要

We propose DemoDiffusion, a simple method for enabling robots to perform manipulation（操控） tasks by imitating a single human demonstration（示范数据）, without requiring task-specific training or paired human-robot data. Our approach is based on two insights. First, the hand motion in a human demonstration（示范数据） provides a useful prior for the robot's end-effector trajectory, which we can convert into a rough open-loop（开环） robot motion trajectory via kinematic retargeting. Second, while this retargeted motion captures the overall structure of the task, it may not align well with plausible robot actions in-context. To address this, we leverage a pre-trained generalist diffusion policy（扩散策略） to modify the trajectory, ensuring it both follows the human motion and remains within the distribution of plausible robot actions. Unlike approaches based on online reinforcement learning（强化学习） or paired human-robot data, our method enables robust adaptation to new tasks and scenes with minimal effort. In real-world experiments across 8 diverse manipulation（操控） tasks, DemoDiffusion achieves 83.8\% average success rate, compared to 13.8\% for the pre-trained policy and 52.5\% for kinematic retargeting, succeeding even on tasks where the pre-trained generalist policy fails entirely. Project page: https://demodiffusion.github.io/

## 中文简述

提出基于扩散策略的操控方法，具有单样本学习特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型

## 关键贡献

1. 提出 DemoDiffusion 框架：将人体示范的运动学重定向轨迹作为初始化，通过预训练扩散策略的中间步去噪（SDEdit 式）进行闭环修正，兼具人体示范的高层结构和扩散策略的动作可行性
2. 无需任务特定训练、配对数据或在线 RL，可即插即用于任意预训练扩散/流匹配策略
3. 在仿真灵巧抓取和 8 项真实世界操控任务上全面超越基线，平均成功率 83.8%（vs. Pi-0 的 13.8% 和运动学重定向的 52.5%）
## 结构化提取

- Problem: 通用机器人策略 zero-shot 部署困难，现有单次人体模仿方法或因开环执行脆弱，或需大量在线交互
- Method: 运动学重定向 + SDEdit 式扩散去噪（从中间步 s* 开始去噪），闭环执行
- Tasks: 灵巧抓取（仿真）、抓取放置、拖拽、推动、关闭、擦拭（真实世界）
- Sensors: 多相机 RGBD（4 外部 + 1 腕部），使用 Hamer 提取 3D 手部关键点
- Robot Setup: Franka Emika Panda + Robotiq 二指夹爪（真实）；16-DOF Allegro 灵巧手（仿真）
- Metrics: 成功率（每任务 10 trials），按物体尺寸分组统计
- Limitations: 假设人机动作相似性；不产生可复用策略；依赖 3D 手部估计精度；未处理时序对齐；s*/S 需启发式选择
- Evidence Notes:

  - 仿真灵巧抓取：DemoDiffusion 在所有尺寸组优于运动学重定向和纯策略，s*/S=0.2 为最优
  - 真实世界 8 任务：平均成功率 83.8%，Pi-0 仅 13.8%，运动学重定向 52.5%
  - 消融表明对关键点噪声（5cm 偏移）和重定向方式变化有一定鲁棒性
  - 零样本物体泛化实验表明同类目不同物体上可自适应
  - s*/S 选择指导：基线策略成功率非零时用 0.4，完全失败时用 0.2
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 完整获取）
- Evidence Coverage: high（摘要、方法、实验结果、消融、限制、附录均完整覆盖）
- Confidence: high
- Summary: 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。


## Problem

通用机器人操控策略（如 Pi-0）在大规模数据集上预训练后，仍难以在新环境或新任务上 zero-shot 部署。现有的人体示范模仿方案存在两类缺陷：(1) 运动学重定向（kinematic retargeting）因形态差异和开环执行而脆弱；(2) 在线 RL 方法需要数小时交互和重置。DemoDiffusion 旨在不使用配对人体-机器人数据、不需要在线训练或微调的情况下，仅凭单次人体视频示范即可让机器人可靠执行新任务。


## Method

### 核心思路
两个关键洞察：(1) 人体示范中手部轨迹提供了机器人末端执行器运动的有用先验；(2) 运动学重定向后的轨迹虽捕获了任务高层结构，但不一定符合当前场景下合理的机器人动作分布。扩散策略建模了该分布，可用于修正轨迹。

### 步骤
1. **手部姿态提取**：使用 Hamer（单目手部重建模型）从人体示范视频逐帧提取 3D 手部关键点轨迹 {h_t}
2. **运动学重定向**：将手部关键点映射为机器人末端执行器位姿 â_t = f_retarget(h_t)。手腕位置作为末端位置，拇指尖与其它指尖方向定义末端朝向。对二指夹爪用指间距推断二值抓取，对灵巧手用逆运动学匹配指尖
3. **SDEdit 式扩散去噪**：
   - 对重定向轨迹添加中间步噪声：ã_t^(s*) = √α_{s*} · â_t + √(1-α_{s*}) · ε_t
   - 从扩散步 s* 开始，用预训练策略 π̄_θ 逐步去噪至步 0
   - s* 是关键超参数：s*/S=0 退化为纯重定向，s*/S=1 退化为纯策略输出
4. **闭环执行**：每步利用实时相机观测进行去噪，补偿形态差异和外部扰动

### 策略选择
- 仿真实验：3D Diffusion Policy 变体（层次化策略：高层规划器 + 低层控制器）
- 真实实验：Pi-0（Physical Intelligence 发布的 flow-matching 策略，在 DROID 数据集上训练）

### 关键超参数
- 噪声水平 s*/S：Pi-0 成功率非零时选 0.4，Pi-0 完全失败时选 0.2
- 动作分块长度 H=10（与 Pi-0 一致）


## Experiments

### 仿真实验：灵巧抓取
- **设置**：16-DOF Allegro 四指灵巧手，RaiSim 仿真器
- **训练**：985 条抓取轨迹，58 个物体（ShapeNet 26 + PartNet 32）
- **测试**：1220 个 Objaverse 物体，按大小分为 small(3-5cm)、medium(5-7cm)、large(7-9cm)
- **结果**（s*/S=0.2, S=1000）：

| 方法 | Small | Medium | Large |
|------|-------|--------|-------|
| DemoDiffusion | 32.0% | 50.3% | 63.4% |
| Kinematic Retargeting | 9.3% | 29.3% | 53.3% |
| Robot Policy | 16.7% | 33.7% | 51.1% |

- DemoDiffusion 在所有尺寸组均优于两个基线，小物体提升最大
- 推理速度提升 S/s* 倍

### 真实世界实验：8 项操控任务
- **硬件**：Franka Emika Panda + Robotiq 二指夹爪，5 相机（4 Realsense 外部 + 1 Zed-Mini 腕部）
- **策略**：Pi-0（未微调），输入为语言指令 + 2 相机，输出关节速度
- **任务**：pick & place banana、drag basket、pick up teddy bear、pick & place bowl、iron curtain、shut down laptop、close microwave、wipe table（涵盖抓取、推动、关闭、擦拭、放置等预抓取和非预抓取操控）
- **总体结果**：DemoDiffusion 83.8%，Kinematic Retargeting 52.5%，Pi-0 13.8%
- **关键观察**：
  - 精确接触任务提升最大：shut laptop 60% vs. 10-20%，wipe table 100% vs. 0-50%
  - Pi-0 在多数任务上只能做通用到达动作，无法识别正确物体或执行具体操控
  - 运动学重定向有合理运动但常在关键接触点失败

### 消融实验
1. **噪声水平 s*/S 分析**（仿真）：
   - s*/S 从 1→0.2 持续提升性能，表明对超参数选择有一定鲁棒性
2. **带噪人体示范**（真实）：
   - 3D 关键点随机偏移 5cm 后 DemoDiffusion 仍保持高质量表现
3. **不同重定向方式**（真实）：
   - 使用拇指+食指距离（vs. 全手指）替代重定向，DemoDiffusion 仍一致提升性能
4. **零样本物体泛化**：
   - 同类目不同物体上使用相同人体示范，DemoDiffusion 能自适应行为


## Limitations

1. 假设机器人应与人类做出相似动作——当形态或环境要求不同策略时可能不成立
2. 仅实现单次模仿，不产生可跨场景泛化的可复用任务策略
3. 重定向质量依赖准确的 3D 人体运动捕捉，手部估计误差会影响下游性能（虽有一定鲁棒性）
4. 隐式假设人体和机器人动作的时序和速度一致，未处理时序对齐
5. s*/S 需根据基线策略表现启发式选择，尚未完全自动化


## Key Takeaways

1. **SDEdit 式中间步去噪是优雅的轨迹修正范式**：不修改预训练策略本身，仅在推理时通过噪声注入-去噪实现轨迹调整，对 DLO 操控中的轨迹先验融合有启发意义
2. **闭环去噪优于开环重定向**：利用扩散策略的闭环观测反馈能补偿形态差异和外部扰动，对可变形物体操控中的接触不确定性处理同样有价值
3. **预训练策略作为动作先验的有效性**：即使在策略 zero-shot 失败的任务上，策略仍能作为去噪器提供合理的动作修正，说明策略内部编码了丰富的操控知识
4. **对 DLO 操控的启发**：人体示范中处理绳/线/布等 DLO 的手部轨迹可作为运动学先验，结合扩散策略的闭环修正可能适应 DLO 的可变形特性；但需解决 DLO 变形引起的更大状态空间不确定性
5. **flow-matching 兼容性**：方法不仅限于 DDPM，也适用于 flow-matching（如 Pi-0），扩大了实际应用范围

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[park|Park, Sungjae]]
- [[bharadhwaj-homanga|Bharadhwaj, Homanga]]
- [[tulsiani-shubham|Tulsiani, Shubham]]
