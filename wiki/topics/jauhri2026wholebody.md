---
title: "Whole-body mobile manipulation using offline reinforcement learning on sub-optimal controllers"
tags: [manipulation, imitation, RL, diffusion, bimanual]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "WHOLE-MoMa 利用次优 WBC 作为结构先验生成仿真演示数据，结合 Q-chunked IQL 离线 RL 和 Diffusion Policy 在 TiAGo++ 上实现无需遥操作数据的全身移动操控，sim-to-real 直接迁移在双臂柜门任务上达到 68% 成功率。"
authors: "Jauhri, Snehal; Prasad, Vignesh; Chalvatzaki, Georgia"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "5WK2AZPR"
---
## 摘要

Mobile Manipulation（移动操控） (MoMa) of articulated objects, such as opening doors, drawers, and cupboards, demands simultaneous, whole-body coordination between a robot's base and arms. Classical whole-body controllers (WBCs) can solve such problems via hierarchical optimization, but require extensive hand-tuned optimization and remain brittle. Learning-based methods, on the other hand, show strong generalization capabilities but typically rely on expensive whole-body teleoperation data or heavy reward（奖励） engineering. We observe that even a sub-optimal WBC is a powerful structural prior: it can be used to collect data in a constrained, task-relevant region of the state-action space, and its behavior can still be improved upon using offline reinforcement learning（强化学习）. Building on this, we propose WHOLE-MoMa, a two-stage pipeline that first generates diverse demonstrations by randomizing a lightweight WBC, and then applies offline RL to identify and stitch together improved behaviors via a reward（奖励） signal. To support the expressive action-chunked diffusion（扩散） policies needed for complex coordination tasks, we extend offline implicit Q-learning with Q-chunking for chunk-level critic evaluation and advantage-weighted policy extraction. On three tasks of increasing difficulty using a TIAGo++ mobile manipulator in simulation, WHOLE-MoMa significantly outperforms WBC, behavior cloning, and several offline RL baselines. Policies transfer directly to the real robot without finetuning, achieving 80% success in bimanual（双臂） drawer manipulation（操控） and 68% in simultaneous cupboard opening and object placement, all without any teleoperated or real-world training data.

## 中文简述

提出基于扩散模型的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、双臂操控

## 关键贡献

1. **WHOLE-MoMa 两阶段管线**：使用多目标层次化 WBC（HQP）生成结构化全身演示数据，无需任何遥操作——WBC 作为解空间的**结构先验**而非最终解
2. **离线 RL 改进次优 WBC**：通过奖励信号从次优演示中识别并拼接更优行为，无需最优演示
3. **Q-chunking 适配离线 RL**：将 IQL 扩展为 chunk-level critic 评估 + AWR 策略提取，使离线 RL 兼容 action-chunked Diffusion Policy，实现时间一致的序列预测
4. **直接 Sim-to-Real 迁移**：在 TiAGo++ 移动操控平台上，策略从仿真直接迁移到真实机器人，双臂抽屉任务 80% 成功率，柜门开+放物任务 68% 成功率，无真实世界微调
## 结构化提取

- **Problem**: 移动操控中关节化物体的全身协调操作，需要底盘和双臂同步运动，现有方法依赖遥操作数据或大量手动调参
- **Method**: WHOLE-MoMa — 两阶段管线：(1) HQP-based WBC 参数随机化生成 3k 次优演示；(2) Q-chunked IQL 离线 RL + Transformer Diffusion Policy + AWR 策略提取
- **Tasks**: Door push-open-and-pass-through (L1), Bimanual drawer close-one-open-another (L2), Cupboard open-and-place-object (L3)
- **Sensors**: 关节本体感知（关节角度、速度）+ 关节化物体关节角度（通过 6D pose tracking ICG 或动捕标记）
- **Robot Setup**: TiAGo++ 全向移动操控机器人，2×7 arm joints + 2×2 gripper joints + 3 base (x,y,θ)，21D 关节速度动作空间，Isaac Sim 仿真，40Hz 控制
- **Metrics**: 成功率（50 episodes 仿真, 25 trials 真实）、部分成功率、成功耗时；真实世界额外记录抓取成功率和操作成功率
- **Limitations**: 操作精度对位姿估计敏感；依赖显式位姿跟踪；仅离线训练无在线改进；任务特定状态机设计；真实物体非完全刚性
- **Evidence Notes**: 仿真三任务 WHOLE-MoMa 一致最优（98%/80%/78%）；真实抽屉 80% 与仿真一致；真实橱柜 68% 存在 sim-to-real gap；消融证明 Transformer Diffusion Policy、Q-chunking 和 AWR 是关键组件；状态估计消融揭示 pose-tracking 在高精度任务上的不足
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML, 75KB)
- Evidence Coverage: complete — abstract, all sections, tables, figures descriptions, references
- Confidence: high
- Summary: WHOLE-MoMa 利用次优 WBC 作为结构先验生成仿真演示数据，结合 Q-chunked IQL 离线 RL 和 Diffusion Policy 在 TiAGo++ 上实现无需遥操作数据的全身移动操控，sim-to-real 直接迁移在双臂柜门任务上达到 68% 成功率。


## Problem

移动操控（MoMa）中对关节化物体（门、抽屉、橱柜）的操作需要机器人底盘和双臂的同步全身协调。现有方法面临两难：
- **经典 WBC/MPC**：通过层次化优化协调多体，但需要大量手动调参，且是近视的（无法跨交互阶段规划），适合抓取的配置可能导致后续操作阶段失败
- **学习方法**：泛化能力强，但依赖昂贵的全身遥操作数据或大量奖励工程，且在高维全身状态-动作空间中 RL 样本效率极低

核心矛盾：如何在不使用遥操作数据的情况下，学习超越近视 WBC 的全身协调策略？


## Method

### 架构概览
WHOLE-MoMa 是两阶段管线：

**Stage 1: WBC 数据生成**
- 使用 HQP（Hierarchical Quadratic Programming）框架，通过 TSID 库实现
- 三个优先级层次：
  - Priority 0（硬约束）：自碰撞避免、关节位置/速度/加速度限制
  - Priority 1（任务目标）：末端执行器 & 底盘跟踪
  - Priority 2（正则化）：默认姿态跟踪
- 每个任务设计状态机（reach → grasp → articulate），HQP 在每阶段生成运动
- **关键设计**：随机化 WBC 参数（姿态权重、抓取阈值、关节步骤大小、速度、初始关节噪声 σ=0.1 rad），每任务生成 3k 轨迹，确保运动风格和时序多样性

**Stage 2: 离线 RL + Q-chunking**
- **状态空间**：22-23D（机器人本体感知 + 关节化物体关节角度）
  - 2×(7 arm joints + 2 gripper joints) + 3 base (x, y, θ) = 21D 机器人状态 + 物体关节
- **动作空间**：21D 关节速度指令
- **奖励函数**：简单线性组合 rt = Σ wi·ri,t（任务成功 + 关节进展 Δqart + 末端/底盘距离缩减），所有权重 = 1.0
- **Q-chunking**：将 step-wise 数据集重新标记为 chunk-level 转换
  - 对每个起始时间 t，构建包含状态历史 st、关节速度 chunk at:t+H-1、chunk 内折扣奖励、t+H 时刻后继状态
  - Q 函数用 transformer 架构，以状态历史为条件
  - 保留 IQL 的核心优势：critic 和 value 学习完全 in-distribution
- **策略提取**：chunk-level AWR
  - 计算 chunk advantage: A(st, at:t+H-1) = Qθ(st, at:t+H-1) - Vψ(st)
  - 训练 Diffusion Policy: L_AWR_chunk = E[exp(β·A) · L_diff]
  - 选择 AWR 而非 IDQL/DDPG+BC 因为：高维全身动作空间中，加权 BC 更稳定，不需要在线动作优化或大候选集

### 关键实现细节
- Diffusion Policy 架构：Transformer-based（非 U-Net）
- Q 函数架构：Transformer-based（Q-transformer）
- Action chunk horizon H=16，状态历史 = 5 步
- 训练频率 40Hz，异步推理方案解决 Diffusion Policy 推理速度不足问题
- EMA 平滑跨 chunk 的动作输出
- 仿真环境：Isaac Sim，关节化物体来自 GAPartNet 数据集


## Experiments

### 仿真结果（50 episodes, 95% CI）

| 任务 | WHOLE-MoMa | WBC | BC | TD3 | IQL+DDPG_BC | IDQL | RISE |
|------|-----------|-----|-----|-----|-------------|------|------|
| Door (L1) | **98%** | 86% | 78% | 88% | 86% | 90% | 92% |
| Drawer (L2) | **80%** | 68% | 70% | 44% | 64% | 72% | 70% |
| Cupboard (L3) | **78%** | 52% | 48% | 0% | 6% | 64% | 64% |

- WHOLE-MoMa 在所有任务上一致最优
- TD3 在最难的 Cupboard 任务上完全失败（0%），证明从零学习全身协调极困难
- IQL+DDPG_BC 在高维空间中不稳定（Cupboard 仅 6%），critic 梯度通过 actor 传播不可靠
- IDQL/RISE 有竞争力但动作噪声更大，采样策略导致连续动作不一致

### 真实世界结果（25 trials/task）

**RealDrawerOpenOneCloseAnother**:
| 方法 | 成功率 | 抓取成功 | 操作成功(给定抓取) | 耗时 |
|------|--------|---------|-------------------|------|
| WBC | 13/25 (52%) | 22/25 | 13/22 | 24.5s |
| BC | 15/25 (60%) | 22/25 | 15/22 | 34.4s |
| WHOLE-MoMa | **20/25 (80%)** | 24/25 | 20/24 | 31.1s |

**RealCupboardOpenAndPlace**:
| 方法 | 成功率 | 抓取成功 | 操作成功(给定抓取) | 耗时 |
|------|--------|---------|-------------------|------|
| WBC | 4/25 (16%) | 17/25 | 4/17 | 45.5s |
| BC | 8/25 (32%) | 19/25 | 8/19 | 76.1s |
| WHOLE-MoMa | **17/25 (68%)** | 22/25 | 17/22 | 70.5s |

- WHOLE-MoMa 真实抽屉成功率与仿真一致（80%）
- 真实橱柜存在显著 sim-to-real gap（78% → 68%），主要瓶颈在操作精度

### 消融实验

| 变体 | Door | Drawer | Cupboard |
|------|------|--------|----------|
| Full model | **98%** | **80%** | **78%** |
| U-Net Diff. Policy | 86% | 42% | 24% |
| MLP Q function | 98% | 76% | 72% |
| no Q-chunking | 90% | 60% | 58% |

- Transformer Diffusion Policy 是关键：在 Cupboard 上 78% vs U-Net 24%
- Q-chunking 提供明显增益：Cupboard 78% vs 58%
- MLP Q 函数在 IQL 设定下差距较小（78% vs 72%），因 IQL 只评估 in-distribution 数据

### 状态估计消融（真实世界）

| 方法 | Drawer 成功 | Cupboard 成功 |
|------|-----------|--------------|
| Pose-tracking (ICG) | 18/25 | 10/25 |
| Marker-based | 20/25 | 17/25 |

- 抽屉任务差距小（单轴线性运动对位姿误差容忍度高）
- 橱柜任务差距大：ICG 在操作阶段精度不足，策略会中途停滞


## Limitations

1. **操作精度敏感性**：即使抓取成功，小的位姿估计误差也会导致策略在操作阶段停滞或失败，尤其在高精度要求的橱柜任务
2. **依赖显式位姿跟踪**：部署需要 6D pose tracker 或动捕标记，新环境中准确跟踪可能不可用
3. **仅离线训练**：当前管线止于离线训练，未利用在线交互进一步改进
4. **安全手柄设计**：真实世界使用可脱落安全手柄防止过大力量，但这也暴露了策略缺乏力控柔顺性
5. **任务特定状态机**：WBC 数据生成仍需为每个任务设计状态机，虽然比完整 WBC 简单但未完全消除手动设计
6. **仿真材质/刚性差异**：关节化物体在真实世界不完全刚体，sim-to-real gap 部分源于动力学差异


## Key Takeaways

1. **次优控制器是强有力的结构先验**：即使简单的 WBC 也能将数据收集聚焦于任务相关的状态-动作空间区域，使离线 RL 在高维全身操控空间中变得可行。这一范式可推广到其他需要结构化数据的操控问题
2. **Q-chunking 对 Diffusion Policy + 离线 RL 至关重要**：chunk-level critic 评估使 IQL 能有效评估 action chunk 的价值，解决了传统 step-wise critic 与 chunked policy 的不对齐问题
3. **AWR 在高维全身空间中优于采样策略**：IDQL/RISE 的采样-选择范式在高维动作空间中引入更多噪声，AWR 的重加权方式更稳定
4. **状态估计精度是真实部署的关键瓶颈**：从 marker-based 到 pose-tracking 的性能差距表明，视觉感知的精度直接影响操控成功率
5. **异步推理 + EMA 平滑是实用的 Diffusion Policy 部署技巧**：解决了 40Hz 全身控制要求与 Diffusion Policy 推理速度（10-12Hz）之间的矛盾

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[jauhri|Jauhri, Snehal]]
- [[prasad|Prasad, Vignesh]]
- [[chalvatzaki|Chalvatzaki, Georgia]]
