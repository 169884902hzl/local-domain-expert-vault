---
title: "ATRS: Adaptive trajectory re-splitting via a shared neural policy for parallel optimization"
tags: [imitation, RL, sim-to-real, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。"
authors: "Yu, Jiajun; Liu, Guodong; Wang, Li; Zhou, Pengxiang; Liu, Wentao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PMV7ICRU"
---
## 摘要

Parallel trajectory optimization via the Alternating Direction Method of Multipliers (ADMM) has emerged as a scalable approach to long-horizon（长时序） motion planning. However, existing frameworks typically decompose the problem into parallel subproblems based on a predefined fixed structure. Such structural rigidity often causes optimization stagnation in highly constrained regions, where a few lagging subproblems delay global convergence. A natural remedy is to adaptively re-split these stagnating segments online. Yet, deciding when, where, and how to split exceeds the capability of rule-based heuristics. To this end, we propose ATRS, a novel framework that embeds a shared Deep Reinforcement Learning（强化学习） policy into the parallel ADMM loop. We formulate this adaptive adjustment as a Multi-Agent Shared-Policy Markov Decision Process, where all trajectory segments act as homogeneous agents and share a unified neural policy network. This parameter-sharing architecture endows the system with size invariance, enabling it to handle dynamically changing segment counts during re-splitting and generalize to arbitrary trajectory lengths. Furthermore, our formulation inherently supports zero-shot（零样本） generalization to unseen environments, as our network relies solely on the internal states of the numerical solver rather than on the geometric features of the environment. To ensure solver stability, a Confidence-Based Election mechanism selects only the most stagnating segment for re-splitting at each step. Extensive simulations demonstrate that ATRS accelerates convergence, reducing the number of iterations by up to 26.0% and the computation time by up to 19.1%. Real-world experiments further confirm its applicability to both large-scale offline global planning and real-time onboard replanning within 35 ms per cycle, with no sim-to-real（仿真到真实迁移） degradation.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移、运动规划

## 关键贡献

1. **自适应轨迹再分割框架**：首次将并行轨迹优化的结构自适应调整建模为多智能体 RL 问题（MASP-MDP）。系统自主识别并解决优化瓶颈，防止滞后子问题拖慢全局收敛。
2. **Size-Invariant 共享策略网络**：所有轨迹段作为同质智能体共享同一策略网络（参数共享），使策略与段数无关，可处理动态变化的段数并泛化到任意轨迹长度。
3. **零样本泛化 + 真实世界验证**：状态表示仅依赖数值求解器内部状态（残差、对偶变量范数等），不依赖环境几何特征，因此可零样本迁移到未见环境。真实四旋翼验证离线全局规划（迭代减少 56.7%）和机载实时重规划（35ms/周期）。
## 结构化提取

- Problem: 并行 ADMM 轨迹优化中固定分段结构导致滞后段拖慢全局收敛，需自适应再分割
- Method: 共享 DRL 策略 (TD3) 嵌入 ADMM 循环，MASP-MDP 建模，参数共享实现 size-invariance，Confidence-Based Election 保证稳定性
- Tasks: 四旋翼运动规划（离线全局规划 + 在线实时重规划）
- Sensors: LiDAR (Livox MID360)，用于 FAST-LIO2 状态估计和建图
- Robot Setup: 定制四旋翼，NVIDIA Orin NX 机载计算机，最大速度 3.2 m/s
- Metrics: ADMM 迭代数、总计算时间、能量代价（jerk 积分）、成功率（2000 次迭代内收敛）
- Limitations: 线程上限约束限制大规模优势；密度泛化有退化；仅验证四旋翼；Heuristic 基线较弱
- Evidence Notes: 完整证据链：仿真 9 种设置 × 100 次试验 + 3 种未见地图泛化验证 + 消融实验 + 真实四旋翼离线/在线实验
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖方法、实验（仿真+真实世界）、消融实验
- Confidence: high
- Summary: 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。


## Problem

基于 ADMM 的并行轨迹优化方法（如 TOP）采用预定义的固定分段结构，由前端路径规划器决定分段数 N。然而不同段面临的约束复杂度差异巨大：开阔区域段快速收敛，高约束区域（窄安全走廊、紧动态约束）的段严重滞后，拖慢全局收敛。现有 L2O 方法仅能调参或热启动，无法动态改变问题结构（分段数和分段方式）。

核心问题三元组：
- **When**: 何时触发再分割
- **Where**: 在停滞段的哪个位置插入新分割点
- **How**: 如何分配空间/时间资源给新子段


## Method

### 整体框架
ATRS 嵌入在并行 CADMM 轨迹优化循环中。每步 ADMM 迭代后，共享策略网络判断是否需要再分割某段，若需要则执行分割后继续迭代。

### MASP-MDP 建模
将再分割决策建模为多智能体共享策略 MDP：
- **环境**：轨迹优化问题本身
- **智能体**：每段轨迹是一个同质智能体，共享同一策略网络 πθ
- **状态空间** (11 维)：
  - 局部状态 s_loc (6 维)：总残差 ε_i、对偶变量范数 ‖y_i‖、能量密度 J̄_i、残差趋势 τ_trend、段时长 T_i、边界偏差 δ_i
  - 全局状态 s_glo (5 维)：最差残差 ‖ε‖∞、最差对偶范数 ‖y‖∞、最差能量密度 ‖J̄‖∞、平均残差 ε̄、段数比 N/N_max
- **动作空间** (4 维连续)：
  - a_gate：分割倾向（触发阈值 δ_gate=0.3）
  - a_ratio：空间分割比例（映射到 [0.1, 0.9]）
  - a_bias：时间偏差（允许时空解耦）
  - a_inf：时长膨胀因子（最多膨胀 30%）
- **奖励函数**：系统级收敛奖励（进度奖励 r_prog + 步惩罚 r_step + 终止奖励 r_term）+ 动作级正则化（分割惩罚 + 能量平衡 + 膨胀惩罚 + 一致性引导）

### Confidence-Based Election 机制
每步仅选择 a_gate 最高且超过阈值的智能体执行分割（i* = argmax{a_gate_i > δ_gate}），保证同时最多一个结构变化，维护求解器稳定性。

### 策略网络
- **算法**：TD3（Twin Delayed DDPG），off-policy 保证样本效率
- **Actor**：共享编码器 + 4 个独立输出头，Tanh 激活绑定到 [-1, 1]
- **Critic**：Twin Critic 架构，取最小值避免过估计
- **实现**：LibTorch (C++)，训练约 10 分钟 / 10000 episodes

### 关键设计选择
- 对数量化映射（log10）处理数值指标的宽动态范围（10⁻⁶ ~ 10⁶）
- 多头输出解耦分割决策与时空调整，防止梯度干扰
- 几何无关状态设计 → 零样本泛化的根本原因


## Experiments

### 仿真环境
- 工作空间：200m × 200m × 5m
- 3 种地图：Map A（Perlin 噪声，训练用）、Map B（2500 立方体障碍物）、Map C（120 不规则多边形构成的 3D 迷宫）
- 3 种密度：Sparse (ρ=0.2, 训练用)、Medium (ρ=0.3)、Dense (ρ=0.4)
- 3 种尺度：Short (<50m)、Medium (50-150m)、Long (>150m)
- 每个设置 100 次独立试验

### Baselines
- TOP (Fixed-Structure)：Yu et al. 的 SOTA 并行 ADMM 优化器
- Heuristic：规则基线（选残差最高段，固定 0.5 比例分割）

### 主要结果（Map A，Table II）

| 设置 | 方法 | 迭代 | 时间(ms) | 能量 | 成功率 |
|------|------|------|---------|------|--------|
| Short/Sparse | TOP | 412.9 | 25.6 | 26.5 | 97% |
| Short/Sparse | **ATRS** | **305.4** | **20.7** | **23.5** | **100%** |
| Long/Sparse | TOP | 441.9 | 64.7 | 56.6 | 99% |
| Long/Sparse | **ATRS** | **392.2** | **61.5** | **53.6** | **100%** |

- 最佳情况：迭代减少 26.0%，时间减少 19.1%（Short/Sparse）
- 密度增加时优势收窄（Dense: 22.5%），但仍一致优于基线
- 大尺度场景下线程调度开销收窄时间优势，但迭代数仍显著更低

### 泛化验证（Fig. 5）
- 在 Map A-2、Map B、Map C 上零样本评估，ATRS 中位数迭代数均低于 TOP
- 方差显著更小，长尾离群值大幅减少
- 3D 迷宫（结构与训练分布完全不同）仍有效

### 消融实验（Fig. 6）
- ATRS w/o Inflation：迭代减少 5.1%，成功率 98.5% → 99.0%（vs TOP）
- ATRS Full：迭代减少 14.7%，成功率 99.5%
- 结论：再分割提供结构基础，时长膨胀提供时间灵活性，两者协同

### 真实世界实验
- **硬件**：定制四旋翼 + NVIDIA Orin NX + Livox MID360 LiDAR
- **定位/建图**：FAST-LIO2
- **离线全局规划**：85m 轨迹，迭代从 1007 降至 436（减少 56.7%）
- **在线局部规划**：80 次连续重规划，平均延迟 35ms/周期，最大速度 3.2m/s
- 稀疏区域不触发分割，密集障碍附近自适应分割，无需微调


## Limitations

1. **线程上限约束**：当分段数超过可用并行线程数时，额外分割无法完全并行执行，时间优势收窄。大规模场景下这一限制更显著。
2. **密度泛化退化**：训练于 Sparse 密度，在 Dense 条件下迭代优势从 26.0% 降至 22.5%（Short 尺度），说明分布偏移仍有影响。
3. **Heuristic 基线较弱**：仅与简单规则基线对比，缺少与更复杂自适应分割策略的比较。
4. **平台限定**：实验仅在四旋翼平台验证，未展示在其他机器人平台（如机械臂）上的适用性。
5. **软上限 N_max**：段数增长受软约束控制，极端情况下仍可能过度分割。
6. **仅四旋翼动力学**：利用了四旋翼的微分平坦性，泛化到其他动力学系统需重新设计状态表示。


## Key Takeaways

1. **Learning to Optimize 的新范式**：从学习求解器参数（L2O 传统方向）跃迁到学习问题结构（结构自适应），这一思路可迁移到其他带固定离散化的优化问题。
2. **参数共享 = Size Invariance**：将各段建模为同质智能体共享策略，天然解决了变维度输入问题，比 Transformer 等序列模型更轻量，适合实时部署。
3. **几何无关状态设计的价值**：仅用求解器内部数值状态（残差、对偶变量、能量密度）而非环境几何，实现了真正的零样本泛化。这一设计哲学值得在其他 sim-to-real 场景中推广。
4. **Confidence-Based Election**：单步单改的保守策略保证了稳定性，但可能限制收敛速度上限；在更鲁棒的求解器上可探索批量分割。
5. **与 DLO 操控的潜在关联**：DLO 轨迹规划同样面临长时序、多约束、固定分段的问题，ATRS 的自适应分段思路可启发 DLO 的轨迹优化方法。

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[planning]]
- [[deformable-linear-object]]

## 相关研究者

- [[yu|Yu, Jiajun]]
