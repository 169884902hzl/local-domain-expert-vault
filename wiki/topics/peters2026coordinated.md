---
title: "Coordinated diffusion: Generating multi-agent behavior without multi-agent demonstrations"
tags: [manipulation, imitation, RL, diffusion, DLO]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-and-place 任务上超越多 Agent 数据训练的基线方法。"
authors: "Peters, Lasse; Ferranti, Laura; Alonso-Mora, Javier; Bajcsy, Andrea"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VJDRUURZ"
---
## 摘要

Imitation learning（模仿学习） powered by generative models has proven effective for modeling complex single-agent behaviors. However, teaching multi-agent systems, like multiple arms or vehicles, to coordinate through imitation learning（模仿学习） is hindered by a fundamental data bottleneck: as the joint state-action space grows exponentially with the number of agents, collecting a sufficient amount of coordinated multi-agent demonstrations becomes extremely costly. In this work, we ask: how can we leverage single-agent demonstration（示范数据） data to learn multi-agent policies? We present Coordinated Diffusion（扩散） (CoDi), a framework that couples independently trained single-agent diffusion（扩散） policies through a user-defined multi-agent cost function, without requiring any coordinated demonstrations. We derive a new diffusion（扩散）-based sampling scheme wherein the diffusion（扩散） score function decomposes into independent, single-agent pre-trained base policies plus a cost-driven guidance term that coordinates these base policies into cohesive multi-agent behavior. We show that this guidance term can be estimated in a gradient-free manner, making CoDi applicable to black-box, non-differentiable cost functions without additional training. Theoretically and empirically, we analyze the conditions under which this composition can faithfully approximate a target multi-agent behavior. We find a complementary role for demonstration（示范数据） data versus the cost function: single-agent demonstrations must cover the support of the desired multi-agent behavior, while the cost function must promote desired behavior from this product of single-agent policies. Our results in simulation and hardware experiments of a two-arm manipulation（操控） task show that CoDi discovers robust coordinated behavior from single-agent data, is more data-efficient（数据高效） than multi-agent baselines, and highlights the importance of joint guidance, base policy support, and cost design.

## 中文简述

提出基于扩散模型的线缆操控方法，具有数据高效特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、可变形物体操控

## 关键贡献

1. **CoDi 框架**：提出三阶段流程（单 Agent 预训练 → 代价函数设计 → 集中式引导采样），将独立的单 Agent 扩散策略组合为协调的多 Agent 行为，无需任何多 Agent 示范数据
2. **KL 正则化合作博弈公式**：将多 Agent 策略合成为 KL 正则化合作博弈的闭式解 π(a|s) = (1/Z) · exp(-J/λ) · ∏p_θ^(i)，其中单 Agent 策略乘积作为先验，代价函数指数项作为耦合项
3. **梯度无关引导分数估计器**：基于 Tweedie 公式和 Monte Carlo 采样的引导分数估计，适用于黑盒、不可微代价函数，无需额外训练
4. **理论分析**：基于 copula 理论和 KL 散度分解，揭示单 Agent 示范数据和代价函数的互补角色——示范数据覆盖目标行为的 support，代价函数补偿协调间隙
5. **硬件验证**：在两台 Franka Research 3 机械臂上成功部署，展示协调 pick-and-place 策略的自发涌现
## 结构化提取

- Problem: 多 Agent 协调的模仿学习数据瓶颈——如何仅用单 Agent 示范学习多 Agent 协调策略
- Method: CoDi（Coordinated Diffusion）——KL 正则化合作博弈 + 梯度无关采样引导 + 单 Agent 扩散策略分解
- Tasks: 双臂协调 pick-and-place（硬件 + 仿真）
- Sensors: 腕部摄像头（ArUco 标记追踪物体位姿）+ 正运动学（末端位姿）
- Robot Setup: 两台 7-DoF Franka Research 3，桌面 1.8m×1.2m，单臂无法覆盖全桌面
- Metrics: manipulation accuracy（物体到目标最短距离）、task efficiency（完成时间）、task success rate（15cm 容差）、collision rate（安全距离违反）
- Limitations: 集中式执行、仅合作设定、代价函数设计依赖、未探索混合数据、任务单一（仅 pick-and-place）
- Evidence Notes: 全文可获取（fulltext），实验结果取自论文图表（Figure 3-7），精确数值为近似值。硬件实验为定性验证（视频），仿真实验为定量对比。所有 ablation 均在相同 50 episode 条件下进行，方法间差异显著。CoDi 的核心优势来自单 Agent 状态-动作空间缩减带来的技能学习提升，而非引导方案本身。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（通过 arXiv HTML 页面获取全文，含方法推导、仿真/硬件实验、ablation 和附录）
- Confidence: high
- Summary: 提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-and-place 任务上超越多 Agent 数据训练的基线方法。


## Problem

多 Agent 系统的模仿学习面临数据瓶颈：联合状态-动作空间随 Agent 数量指数增长，收集足够的多 Agent 协调示范数据极其昂贵。核心问题：如何仅利用单 Agent 示范数据学习多 Agent 协调策略？


## Method

### 核心思想
多 Agent 任务的成功主要依赖单 Agent 场景中也存在的低级技能；额外挑战来自高层协调。因此单 Agent 数据可作为多 Agent 策略的强先验。

### 三阶段流程
1. **Step 1 - 单 Agent 预训练**：用户为每个 Agent 提供单 Agent 示范（如 pick-and-place），训练 N 个独立的单 Agent 扩散策略 p_θ^(i)（base policy）
2. **Step 2 - 引导设计**：用户设计多 Agent 代价函数 J: S×A→R，激励期望的多 Agent 行为
3. **Step 3 - 部署**：通过逆时 SDE 采样，将单 Agent 分数与引导分数组合，生成协调的多 Agent 动作

### 数学框架
- **KL 正则化合作博弈**：π = argmin E[J(a,s)] - λ·D_KL(π || p_θ^{1:N})
- **闭式解**：π(a|s) = (1/Z(s)) · exp(-J(s,a)/λ) · p_θ^{1:N}(a|s)
- **分数分解**：∇log π_t = ∇log p_θ,t^{1:N} + g^J（单 Agent 分数 + 引导分数）
- **引导分数估计**：使用 Tweedie 后验近似 + Monte Carlo 积分，无需代价函数梯度

### 代价函数设计
J(s,a) = w_goal·J_goal + w_collision·J_collision + w_engage·J_engage
- J_goal：物体到目标的距离（通过 Isaac Gym 前向模拟预测联合动作效果）
- J_collision：末端执行器间安全距离的二值指标
- J_engage：惩罚较近机器人到物体的距离

### 关键设计选择
- 策略架构：Denoising UNet（与 chi2023diffusion 相同）
- 观测：自身末端位姿、速度、夹爪宽度 + 物体位姿
- 输出：末端平移/旋转速度 + 夹爪宽度，通过逆运动学转换为关节速度
- 仿真到硬件：ArUco 标记 + 腕部摄像头追踪物体位姿


## Experiments

### 硬件实验
- **平台**：两台 7-DoF Franka Research 3 机械臂
- **任务**：将 5cm 立方体从桌面左侧移至右侧目标（15cm 容差）
- **桌面尺寸**：1.8m × 1.2m，单个机器人无法覆盖全桌面
- **结果**：CoDi 自发发现协调策略——左臂抓取立方体放至中间位置，右臂接手完成放置
- **鲁棒性**：替换为其他物体仍能正常工作

### 仿真实验（Isaac Gym）
- **设置**：50 个 episode，初始配置随机采样
- **指标**：manipulation accuracy（物体到目标最短距离）、task efficiency（完成时间）
- **训练数据**：1k 单 Agent 示范 → 500k receding-horizon 段（16 动作预测，10 Hz）

#### 结果表格

| 方法 | 数据类型 | 成功率 | 操控精度 | 任务效率 |
|------|---------|--------|---------|---------|
| **CoDi (Ours)** | 单 Agent | ~96% | 最好 | 最好 |
| CG-Joint | 多 Agent | ~92% | 较差 | 较差 |
| DPMD-Joint | 多 Agent | ~80% | 较差 | 较差 |
| SDAC-Joint | 多 Agent | ~85% | 较差 | 较差 |
| EXPO-Joint | 多 Agent | ~88% | 较差 | 较差 |
| CoDi-Joint | 多 Agent | ~90% | 中等 | 中等 |

**注**：精确数值取自论文图表，此处为近似值。

#### 数据效率对比（20% 数据）
| 方法 | 数据量 | 成功率 |
|------|--------|--------|
| CoDi (20%) | 200 单 Agent | 88% |
| CG-Joint (20%) | 200 多 Agent | 54% |
| CG-Joint (100%) | 1000 多 Agent | 92% |

#### Ablation 结果
1. **联合引导 vs 独立引导**：独立引导导致两臂同时抓取物体，引发碰撞和任务失败
2. **采样引导 vs 分类器引导**：CG-Product（分类器引导 + 单 Agent 先验）成功率显著低于 CoDi 的采样引导
3. **Base policy support**：简化代价函数（仅 J_goal）下，单 Agent 先验性能大幅下降，而联合先验保持稳定

### 关键 Claim 验证
- (C1) CoDi 从单 Agent 示范发现协调策略 ✓（硬件验证）
- (C2) 鲁棒性足以硬件部署 ✓（12 分钟硬件视频 + 多物体测试）
- (C3) 比多 Agent 基线更数据高效 ✓（20% 数据 CoDi 88% vs CG-Joint 54%）
- (C4) 联合引导对安全协调至关重要 ✓（独立引导引发碰撞）
- (C5) 采样引导估计器是必要的 ✓（CG-Product 显著更差）
- (C6) 引导行为依赖 base policy support ✓（简化代价函数 ablation）


## Limitations

1. **集中式执行**：当前版本要求集中式执行来协调单 Agent 策略，未探索去中心化方案
2. **仅合作设定**：假设所有 Agent 共享同一代价函数、联合动作分布相关，未扩展到非合作场景
3. **代价函数设计依赖**：当 base policy 缺乏协调信息时，代价函数设计变得至关重要（见 C6 ablation）
4. **未利用混合数据**：未探索结合少量多 Agent 示范与单 Agent 数据的可能性
5. **任务局限**：仅在 pick-and-place 任务上验证，未涉及 DLO 操控、装配等更复杂场景
6. **仿真到硬件迁移**：依赖 Isaac Gym 高保真仿真和 ArUco 标记定位，限制了更广泛的适用性


## Key Takeaways

### 对 DLO 操控的启示
- CoDi 的框架天然适用于需要双臂协调的 DLO 操控任务（如线缆拉直、打结），因为 DLO 操控同样面临多臂协调的数据瓶颈
- 梯度无关引导方案允许使用基于仿真的代价函数（如 DLO 形状匹配误差），无需代价函数可微
- 单 Agent 示范（单臂抓取、移动 DLO 段）远比协调的双臂 DLO 操控示范容易收集

### 对 VLM-based 控制的启示
- 代价函数设计可由 VLM 提供（如"将线缆拉直并放到桌边"），将语言指令转化为引导信号
- 分层架构：VLM 提供高层代价函数，CoDi 处理底层协调执行

### 方法论启示
- "去中心化训练 + 集中式执行"反转了传统 CTDE 范式，在数据稀缺场景下有实际优势
- Copula 理论为分解多 Agent 分布提供了理论基础，可推广到其他多 Agent 推理问题
- 采样引导（gradient-free）比分类器引导在单 Agent 先验下更有效，因为 base policy 和目标分布之间的 tilt 更大

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[peters-lasse|Peters, Lasse]]
- [[ferranti-laura|Ferranti, Laura]]
- [[alonso-mora-javier|Alonso-Mora, Javier]]
- [[bajcsy-andrea|Bajcsy, Andrea]]
