---
title: "Discrete flow matching for offline-to-online reinforcement learning"
tags: [RL, diffusion, diffusion-model, flow-matching]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow matching、path-space KL 正则化和 candidate-set 近似实现稳定微调，在 Jericho 文字游戏上取得最高平均归一化分数。"
authors: "Khan, Fairoz Nower; Nahim, Nabuat Zaman; Ju, Peizhong"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "KDTMUMCR"
---
## 摘要

Many reinforcement learning（强化学习） (RL) tasks have discrete action spaces, but most generative policy methods based on diffusion（扩散） and flow matching are designed for continuous control. Meanwhile, generative policies usually rely heavily on offline datasets and offline-to-online RL is itself challenging, as the policy must improve from new interaction without losing useful behavior learned from static data. To address those challenges, we introduce DRIFT, an online fine-tuning method that updates an offline pretrained continuous-time Markov chain (CTMC) policy with an advantage-weighted discrete flow matching loss. To preserve useful pretrained knowledge, we add a path-space penalty that regularizes the full CTMC trajectory distribution, rather than only the final action distribution. For large discrete action spaces, we introduce a candidate-set approximation that updates the actor over a small subset of actions sampled from reference-policy rollouts and uniform exploration. Our theoretical analysis shows that the candidate-set error is controlled by missing target probability mass, and the induced CTMC generator error decreases as the candidate set covers more high-probability actions. Experiments on prevailing discrete action RL task show that our method provides stable offline-to-online improvement across all tasks, achieving the highest average score on Jericho with a simple GRU encoder while outperforming methods that use pretrained language models. Controlled experiments further confirm that the path-space penalty remains bounded during fine-tuning and that the CTMC generator adapts to shifted rewards faster than deterministic baselines. The candidate-set mechanism is supported by a stability analysis showing that the generator error decreases exponentially with candidate coverage.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 强化学习、扩散模型、扩散模型、Flow Matching

## 关键贡献

1. **DRIFT 方法**：首个面向离散动作空间的 CTMC 策略 offline-to-online 微调框架，结合 advantage-weighted discrete flow matching actor 更新与 path-space KL 正则化。
2. **Path-space trust region**：正则化整个 CTMC 轨迹分布（包含跳转目的地和驻留时间），而非仅约束终端动作分布，提供更完整的遗忘防护。
3. **Candidate-set 近似**：通过参考策略 rollout + 均匀采样构建候选动作集，在大动作空间中高效更新 actor，并有理论覆盖保证。
4. **理论分析**：Proposition 4.1（覆盖误差随 Nroll/Nrand 指数衰减）、Proposition 4.2（质量守恒）、Theorem 4.3（生成器稳定性——误差随候选集覆盖指数衰减）。
## 结构化提取

- Problem: 离散动作空间中，如何从离线预训练的生成式策略出发，通过在线交互持续改进而不遗忘
- Method: DRIFT = advantage-weighted discrete flow matching + path-space KL 正则化 + candidate-set 近似；CTMC 作为策略表示
- Tasks: Jericho 文字游戏、MinAtar (5 games)、D4RL 离散化 MuJoCo (Hopper/Walker2d/HalfCheetah × medium/expert)、Gridworld toy tasks
- Sensors: MinAtar: 10×10×nch 二值张量；Jericho: 文本观测（GRU 编码）；D4RL: MuJoCo 状态向量
- Robot Setup: 无物理机器人，纯仿真基准
- Metrics: 归一化分数、平均奖励、目标覆盖率（多模态）、冷目标发现率、适应速度（steps to goal）
- Limitations: path-space KL 在差参考下限制探索；候选集未在真正大规模动作空间验证；Macro-MinAtar |A|=216 时失败；计算开销约为 baseline 的 2×；Jericho 仅 1 seed
- Evidence Notes:

  - Jericho: DRIFT 23.2% > CALM 12.6% > KG-A2C 19.2%，且用简单 GRU 编码器超越 GPT-2
  - MinAtar: 3/5 最佳，所有游戏均改进（AWAC/SPA 在 4/5 游戏崩溃）
  - D4RL: 平均 +24.0 改进（最强），但离线初始化弱（0.4 vs baseline 8.0）
  - Toy 3: DQN mode collapse 到单一目标，DRIFT 保持双模态
  - Toy 4: 候选集 16% 覆盖率处相变，验证 Prop 4.1
  - Goal-Switch: DRIFT 1.9× 更快适应奖励变化
  - Macro-MinAtar: DRIFT 失败（4.08 vs PPO 9.86），离线初始化弱是主因
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high
- Confidence: high
- Summary: 提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow matching、path-space KL 正则化和 candidate-set 近似实现稳定微调，在 Jericho 文字游戏上取得最高平均归一化分数。


## Problem

Offline RL 训练的策略受限于离线数据的覆盖和质量，无法发现数据中缺失的高奖励动作。Offline-to-online 微调可以让策略从在线交互中持续改进，但面临两个核心挑战：

1. **离散动作空间的生成式策略缺失**：现有基于 diffusion 和 flow matching 的生成式策略均为连续动作空间设计，无法直接应用于推荐系统、文本游戏、组合优化等离散决策场景。
2. **灾难性遗忘**：在线微调时策略容易丢失离线预训练学到的有用行为结构，而传统 RL 方法（DQN、PPO）在多模态动作分布下容易发生 mode collapse。


## Method

### 核心架构

DRIFT 分两个阶段：

**Stage 1: 离线预训练**
- 训练双 critic 网络 Q1, Q2 和 value 网络 V
- 构造 advantage-weighted 目标策略 π̃_pre(a|s) ∝ exp(Ā_off(s,a)/β)
- 训练 CTMC 生成器从 Uniform(A) 流向 π̃_pre（标准 DFM + independent coupling）

**Stage 2: 在线微调（DRIFT 核心贡献）**

每次迭代包含四步：
1. **环境交互**：从 Uniform(A) 出发，M 步 Euler 离散化模拟 CTMC，执行终端动作，存入 replay buffer
2. **Critic/Value 更新**：从混合 buffer（(1-ρ)B 在线 + ρB 离线）更新双 critic 和 value 网络；value 使用 lagged target policy π̃⁻
3. **候选集构造与目标策略**：
   - 候选集 = Nroll 次参考策略 rollout + Nrand 均匀采样
   - 平滑参考分布 π̂_ref(a|s) ∝ count(a) + ε
   - 目标策略 π̃(a|s) ∝ π̂_ref(a|s) · exp(Ā(s,a)/β)
4. **Actor 更新**：DFM loss + path-space KL penalty

### 关键技术细节

- **Linear bridge**：p_t(a|s) = (1-t)·p₀(a) + t·π̃(a|s)，p₀ = Uniform(A)
- **Independent coupling**：将每个"失量"动作的概率质量按比例分配给所有"增量"动作
- **Path-space KL**：比较两个 CTMC 路径测度的 KL 散度，包含跳转率和驻留时间
- **Rate network**：2 层 MLP (256 hidden)，softplus 保证非负率，对角线由守恒条件确定
- **参考策略周期性刷新**：每 K 步将 u_ref ← u_θ

### 理论保证

- **Proposition 4.1**：候选集排除的目标策略质量 ε(s) 随 Nroll 和 Nrand 指数衰减
- **Proposition 4.2**：Independent coupling 生成器满足 Kolmogorov 前向方程
- **Theorem 4.3**：候选集限制下的生成器误差以常数 C/(p²Z²) · ∥π̃_cand - π̃∥₁ 为界


## Experiments

### 数据集与基准

| 基准 | 动作空间规模 | 离线数据量 | 在线步数 |
|------|-------------|-----------|---------|
| Jericho 文字游戏 | 3-10 valid actions/state | 200 episodes/game | 300K |
| MinAtar (5 games) | 3-6 actions | 100K transitions | 300K |
| D4RL 离散化 MuJoCo | k=22 clusters | ~1M transitions | 300K |
| Macro-Action MinAtar | 216 macro actions | 100K transitions | 300K |

### 主要结果

**Jericho**（Table 1）：DRIFT 平均归一化分数 23.2%，超越所有 baseline：
- DRRN 15.3%、DQN 12.1%、CALM (GPT-2) 12.6%、KG-A2C 19.2%
- Deephome 上 35.8 vs 其他方法的 6.0（6× 提升）
- 唯一在所有游戏上均获得正分的方法

**MinAtar**（Table 2）：DRIFT 在 5 个游戏中 3 个取得最佳（Breakout 17.10、Asterix 1.17、Seaquest 1.84），所有游戏均有改进

**D4RL 离散化**（Table 3）：DRIFT 平均改进 +24.0（从 0.4 提升到 24.4），Hopper 上提升最显著（+47.8 medium, +46.7 expert）

**Macro-Action MinAtar**（|A|=216，Table 19）：DRIFT 在此 benchmark 表现不佳（平均 4.08 vs DQN 4.84, PPO 9.86），作者归因于弱离线初始化和 CTMC 生成器难以从少量状态吸收 216 动作的广度

### 消融实验

- **Path-space KL**：在 Goal-Switch 环境中有价值（防遗忘），但在无分布偏移时（Toy 5）可能阻碍探索
- **CTMC sub-steps**：M=10 是关键阈值，M<10 性能急剧下降
- **Temperature β**：0.4 为最佳平衡点
- **Offline mix ρ**：单调递增的改进（0% → 50%）
- **候选集相变**：Toy 4 (|A|=128) 中 16% 覆盖率处出现急剧相变，验证理论预测
- **Cold-start**：完整预训练提供最佳性能一致性

### 关键对比结果

| 环境 | DRIFT 优势 | 说明 |
|------|-----------|------|
| Toy 3 (多模态) | 双模态覆盖 vs DQN 单模态 | CTMC 保持分布 vs argmax mode collapse |
| Goal-Switch | 1.9× 更快适应 | CTMC 直接重分布概率 vs Bellman 备份 |
| Combinatorial Lock | 23.5% vs DQN 2.0% | 大动作空间+序列任务 |
| Macro-MinAtar | DRIFT 落后 | 弱离线初始化 + |A|=216 可被 DQN 枚举 |


## Limitations

1. **Path-space KL 在差参考策略下限制探索**：当离线数据质量差时，α 调度需要自适应，固定值可能过度约束
2. **Candidate-set 未在真正大规模动作空间验证**：如实时策略游戏（|A| 数千）或组合优化
3. **Macro-Action MinAtar 失败**：|A|=216 时 CTMC 生成器离线初始化弱，actor batch 只有 8 个状态无法吸收广度
4. **D4RL 离散化引入天花板**：k=22 太小，所有方法可枚举全部动作，DRIFT 的候选集优势消失
5. **计算开销**：~8.7h/run (MinAtar) vs baseline 平均 ~4h
6. **未扩展到多目标或多智能体场景**
7. **Jericho 只用了 1 seed**（计算成本高），统计可靠性有限


## Key Takeaways

1. **CTMC 生成式策略在离散动作空间有独特优势**：天然保持多模态分布，避免 DQN 类方法的 mode collapse
2. **Path-space KL > Terminal-action KL**：正则化整个 CTMC 轨迹比仅约束终端分布更有效地防止遗忘
3. **Candidate-set 机制的理论与实践**：16% 覆盖率相变是重要设计指导——不需要覆盖全部动作
4. **对机器人操控的启示**：
   - DLO 操控中的离散化动作选择（抓取点、缠绕策略）可借鉴 CTMC 生成式建模
   - Path-space 正则化思想可迁移到连续动作空间的 diffusion/flow policy 在线微调
   - Candidate-set 机制适用于大规模离散决策（如任务规划中的技能选择）

## 相关概念

- [[reinforcement-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[khan|Khan, Fairoz Nower]]
