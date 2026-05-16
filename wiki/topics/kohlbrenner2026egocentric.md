---
title: "Egocentric tactile and proximity sensors as observation priors for humanoid collision avoidance"
tags: [RL, collision-avoidance, tactile-sensing, proximity-sensing]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于密集方向性信号"
authors: "Kohlbrenner, Carson; Pudasaini, Niraj; Xie, William; Sivagnanadasan, Naren; Correll, Nikolaus et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "G359SK7J"
---
## 摘要

Collision-free motion is often aided by tactile（触觉） and proximity sensors distributed on the body of the robot due to their resistance to occlusion as opposed to external cameras. However, how to shape the sensor's properties, such as sensing coverage; type; and range, to enable avoidant behavior remains unclear. In this work, we present a reinforcement learning（强化学习） framework for whole-body collision avoidance on a humanoid H1-2 robot and use it to characterize how sensor properties shape learned avoidance behavior. Using dodgeball as a benchmark task, we ablate the properties of sensors distributed across the upper body of the robot and find that raw proximity measurements can substitute for explicit object localization provided the sensing range is sufficient and that sparse non-directional proximity signals outpace dense directional alternatives in sample efficiency.

## 中文简述

提出基于强化学习的绳索操控方法。

**研究方向**: 强化学习、可变形物体操控、触觉感知

## 关键贡献

1. **RL 碰撞规避框架**：提出基于 PPO 的全身碰撞规避框架，利用分布式自我中心传感器引导 H1-2 人形机器人学习躲避行为
2. **传感器属性系统性消融**：对比了覆盖几何（field vs. ray）、信号类型（localization, proximity, binary）和感知距离（0.2-2m）对学习效果的影响，揭示了关键设计洞察
## 结构化提取

- Problem: 人形机器人分布式自我中心传感器（触觉/近觉）的信号属性如何影响 RL 策略学习全身碰撞规避行为
- Method: PPO + 非对称 actor-critic（32 units × 2 layers），PD 控制器输出力矩，GenTact 管线随机布置 64 个传感器
- Tasks: Dodgeball 碰撞规避（球以 4-8 m/s 投掷，成功 = 3 秒无接触站立）
- Sensors: 分布式触觉（binary contact）+ 近觉（field/ray，localization/proximity/binary，0.2-2m 范围）
- Robot Setup: H1-2 人形机器人，21 个关节，上半身 64 个传感器，仿真环境（未指定仿真器）
- Metrics: 累积奖励（生存时间 + 正则项），IQR 均值（10 seeds），收敛 epoch 数
- Limitations: 仅仿真、理想化传感器（无噪声/延迟）、无时序观测、单一任务、未真实验证
- Evidence Notes: (1) Field proximity ≥1m 可替代 localization（Fig.4-a）；(2) 稀疏 field 信号采样效率远高于密集 ray depth image（Fig.4-a vs 4-b）；(3) Ray 压缩为 min distance 后性能接近 localization 上界；（4）Field proximity >1m 在 <1000 epoch 收敛（RTX 4090 ≈20min）；（5）Ray proximity/binary 多数未在 3000 epoch 内收敛
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv MCP 获取完整论文文本，包含全部章节和参考文献）
- Evidence Coverage: complete（涵盖 Introduction、Methods、Results、Discussion、Conclusion 全部内容）
- Confidence: high
- Summary: 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于密集方向性信号


## Problem

人形机器人在动态环境中（如拥挤走廊、体育运动）需要全身碰撞规避能力。分布式触觉和近觉传感器相比外部相机具有抗遮挡、低观测复杂度、自我中心布局的优势。然而，传感器的属性（覆盖几何、信号类型、感知距离）如何塑造可学习的规避行为，这一问题尚未系统研究。经典控制方法依赖预定义约束来响应传感器信号，而 RL 方法让策略自己学习如何反应——但传感器的信号表示作为"观测先验"（observation prior）如何影响学习效果尚不清楚。


## Method

### 核心框架
- **策略**：PPO 算法，策略网络输出关节目标位置 q*_t ∈ R^21，通过 PD 控制器转换为力矩
- **网络架构**：actor 和 critic 各为两层前馈网络（32 units/层），刻意选择低容量架构使性能差异归因于传感器形态而非模型表达能力
- **非对称 actor-critic**：critic 获得额外的线速度特权观测，提升训练稳定性

### 传感器建模
- **64 个传感器**分布在机器人上半身，位置通过 GenTact 设计管线随机生成
- **覆盖几何**：
  - Field 传感器：球形感知范围（模拟电容式/声学传感器），返回非方向性信号
  - Ray 传感器：8×8 光束网格，63° 方形视场角（模拟 ToF 传感器），返回方向性信号
- **信号函数**：
  - Perfect localization：返回球体在机器人中心坐标系下的笛卡尔坐标（上界）
  - Relative proximity：返回传感器范围内最近点距离（归一化）
  - Binary detection：返回布尔值，是否有物体在范围内
- **触觉传感器**：全身覆盖的二元接触检测，用于 episode 终止判定（奖励塑形）

### 训练设置
- 每个配置训练 10 个不同随机种子的模型
- 每次训练 4096 个 agent 并行，最多 3000 epoch（约 910 模拟小时）
- 低容量网络（32 units × 2 layers）确保性能差异来自传感器设计

### Dodgeball 基准任务
- 半径 15cm 的球以 4-8 m/s 从 4-6m 外投掷
- 每 1-2 秒追加新球
- 成功标准：保持站立且无接触 3 秒


## Experiments

### 主要结果（Fig. 4 消融实验）
| 传感器配置 | 2m 范围 | 1m 范围 | 0.5m 范围 | 0.2m 范围 |
|-----------|---------|---------|----------|----------|
| Field + Localization | 最优 | 最优 | 最优 | 最优 |
| Field + Proximity | ≈Localization | ≈Localization | 弱 | 弱 |
| Field + Binary | 弱 | 弱 | 中等 | 弱 |
| Ray + Localization | 优 | 优（略低于 Field） | 中 | 弱 |
| Ray + Proximity | 差 | 差 | 差 | 差 |
| Ray + Binary | 差 | 差 | 差 | 差 |

### 三个核心发现
1. **近距离替代**：当感知距离足够大（≥1m）时，relative proximity 测量可作为 explicit localization 的强替代方案，对 field 和 ray 传感器均成立
2. **短距离二值检测**：在近距离（0.5m）时，binary detection 信号优于 distance 测量，因为仅知道"附近有物体"对反应式控制已足够
3. **稀疏 > 密集**：sparse non-directional proximity 信号（field 传感器，1D 信号）在采样效率上显著优于 dense directional 信号（ray 传感器，64D depth image）。将 ray 传感器压缩为仅返回最小距离后，性能大幅提升，接近 localization 上界

### 训练效率
- Field-based proximity（>1m）在 <1000 epoch 收敛，RTX 4090 上约 20 分钟
- Ray-based proximity 和 binary 在 3000 epoch 内多数无法收敛
- 这表明合理设计传感器信号可大幅减少训练数据需求


## Limitations

1. **仅仿真验证**：所有实验在仿真中进行，传感器为理想化模型（无噪声、无延迟、无测量失败）
2. **无时序观测**：策略仅使用当前时刻传感器读数，未探索时序观测序列（可能帮助推断球体运动方向）
3. **模态特异性噪声未建模**：电容传感器受静电场影响、声学传感器受环境声音影响，但本文将二者统一归类为 field 传感器
4. **无真实部署**：尚未在真实人形机器人上验证（但作者引用其 ICRA 2026 工作 [10] 表明硬件已就绪）
5. **单一任务**：仅测试 dodgeball 场景，未验证泛化性（如拥挤室内导航）
6. **传感器定位假设**：假设传感器在机器人上的位置已知且精确


## Key Takeaways

### 对 DLO 操控的启示
1. **传感器作为表示偏置**：传感器信号不是被动输入，而是塑造策略学习空间的结构性先验。对 DLO 操控意味着——触觉/近觉传感器的信号设计直接影响 RL 策略能否学到有效的操控行为
2. **稀疏信号的优势**：在碰撞规避任务中，低维稀疏信号（field proximity）比高维密集信号（ray depth image）更高效。类比到 DLO 操控，可能简单的接触/距离信号比高分辨率触觉阵列更适合 RL 训练
3. **近距离 vs 远距离的差异**：不同距离范围最优信号类型不同，提示 DLO 操控中预接触（approach）和接触（contact）阶段可能需要不同的感知策略
4. **触觉作为奖励塑形**：binary tactile 用于 episode 终止的思路可迁移到 DLO 操控中——用触觉信号判断操控成功/失败

### 对 VLM 控制的启示
- 本文聚焦于物理传感器而非视觉输入，但"观测表示如何影响策略学习"的核心洞见同样适用：VLM 提供的语言-视觉表示也需要考虑如何作为有效的观测先验

### 对 Sim-to-Real 的启示
- 传感器理想化假设是典型的 sim-to-real gap 来源；作者明确指出需要真实传感器验证，这对我们的 sim-to-real 工作流有参考价值

## 相关概念

- [[reinforcement-learning]]
- [[collision-avoidance]]
- [[tactile-sensing]]
- [[proximity-sensing]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[kohlbrenner|Kohlbrenner, Carson]]
