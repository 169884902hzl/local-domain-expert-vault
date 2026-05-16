---
title: "AdaGamma: State-dependent discounting for temporal adaptation in reinforcement learning"
tags: [manipulation, VLM, RL, DLO, planning]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error collapse，可即插即用集成到 SAC/PPO 中，在连续控制基准和京东物流在线 A/B 测试中取得显著提升。"
authors: "Wang, Yaomin; Pan, Jianting; Tian, Ran; Li, Xiaoyang; Zhang, Yu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZEI9GNXS"
---
## 摘要

The discount factor in reinforcement learning（强化学习） controls both the effective planning horizon and the strength of bootstrapping, yet most deep RL methods use a single fixed value across all states. While state-dependent discounting is conceptually appealing, naive deep actor--critic implementations can become unstable and degenerate toward TD-error collapse. We propose AdaGamma, a practical deep actor--critic method for state-dependent discounting that learns a state-dependent discount function together with a return-consistency objective to regularize the induced backup structure. On the theory side, we analyze the Bellman operator induced by state-dependent discounting and establish its basic well-posedness properties under suitable conditions. Empirically, AdaGamma integrates into both SAC and PPO, yielding consistent improvements on continuous-control benchmarks, and achieves statistically significant gains in an online A/B test on the JD Logistics platform. These results suggest that state-dependent discounting can be made effective in deep RL when coupled with a return-consistency objective that prevents degenerate target manipulation（操控）.

## 中文简述

提出基于强化学习的绳索操控方法。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、可变形物体操控、运动规划

## 关键贡献

1. **方法**：提出 AdaGamma，一种实用的深度 actor-critic 状态依赖折扣方法，通过 return-consistency 目标防止退化 TD-target manipulation
2. **理论**：分析状态依赖折扣诱导的 Bellman 算子，在合适条件下建立其 well-posedness、soft policy evaluation 收敛性、soft policy improvement 单调性和误差界
3. **灵活集成**：分别通过 off-policy adapter（SAC）和 on-policy adapter（PPO 的 modified GAE）实现即插即用
4. **真实世界验证**：在京东物流平台进行 4 周在线 A/B 测试，取得统计显著的订单增量提升
## 结构化提取

- Problem: 深度 RL 中固定折扣因子无法适应状态异构的时间结构，而朴素的状态依赖折扣学习会导致 TD-error collapse
- Method: AdaGamma — 轻量级 Gamma Network (2层MLP, 256隐藏) 学习 γ_ϕ(s)，通过 return-consistency 目标训练（让单步 bootstrap 匹配 n-step return），正则化防止退化；分别适配 SAC（修改 Q-target）和 PPO（修改 GAE）
- Tasks: 连续控制（SafetyPointGoal1-v0, Humanoid-v4, Ant-v4, 经典 Gymnasium 任务），推荐系统（京东物流目标营销）
- Sensors: 无传感器直接相关；环境状态向量（MuJoCo 状态），用户行为特征（JD Logistics）
- Robot Setup: 无真实机器人实验；MuJoCo 仿真 locomotion 任务
- Metrics: Reward（任务奖励），Cost（安全约束成本），推荐诱导订单量（A/B 测试），学到的平均 γ 值
- Limitations: 增益在时间同构任务上有限；理论仅覆盖 tabular 有限动作空间；PPO 集成无理论支撑；多超参数需调优；未验证高维感知输入场景
- Evidence Notes: 完整阅读全文及附录。Table 1-12 具体数值未能从 HTML 文本中提取（以图片/HTML 表格形式呈现），描述基于正文文字叙述。JD Logistics A/B 测试结果来自 Figure 1 的文字描述，未获取原始数值数据。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（完整阅读 22 页正文及附录，但 Table 1-12 的具体数值以 HTML 表格/图片形式呈现，文本中仅保留表头描述）
- Confidence: high
- Summary: 提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error collapse，可即插即用集成到 SAC/PPO 中，在连续控制基准和京东物流在线 A/B 测试中取得显著提升。


## Problem

深度 RL 中折扣因子 γ 同时控制有效规划视界和 bootstrap 强度，但几乎所有主流算法（SAC、PPO、TD3 等）都使用单一固定 γ 值。在具有异构时间结构的环境中（某些状态需要长视界传播，某些状态应缩短视界以降低方差），固定 γ 限制了策略质量。然而，朴素地将 γ 替换为可学习的状态依赖函数 γ_ϕ(s) 会导致退化行为：gamma network 会将 γ 推至最小值以最小化 TD error，而非学习有意义的状态依赖结构（TD-error collapse 问题）。


## Method

### 核心架构
- **Gamma Network**：小型 MLP g_ϕ: S → R，输出经 sigmoid 后重标定到 [γ_min, γ_max]（实验中 γ_min=0.900, γ_max=0.999），两层 MLP，隐藏维度 256，不与 policy/value 网络共享参数

### SAC 集成（Off-Policy Adapter）
- 将标准 SAC 的 Q-target 中固定 γ 替换为 γ_ϕ(s_t)：Q^(s_t, a_t) = r_t + γ_ϕ(s_t)(1-d_t)[min Q_θ̄_i(s_{t+1}, a'_{t+1}) - α log π_ψ(a'_{t+1}|s_{t+1})]
- Policy 更新和 entropy tuning 不变

### PPO 集成（On-Policy Adapter）
- 修改 GAE 中的 TD residual：δ_t = r_t + γ_ϕ(s_t)V(s_{t+1}) - V(s_t)
- 修改 GAE 后向递推：Â_t = δ_t + γ_ϕ(s_t)·λ·Â_{t+1}，展开后为乘积权重形式
- PPO 多 epoch 优化时冻结 γ_ϕ(s)（防止违反 trust-region 假设）
- Advantage normalization 吸收因状态依赖 γ 带来的幅度变化

### Return-Consistency 目标（核心创新）
- 为每条 transition 计算两个估计：(1) 单步 bootstrap V̂_1(s_t) = r_t + γ_ϕ(s_t)V(s_{t+1})；(2) n-step MC return G_t^(n)（使用参考折扣 γ̄）
- Gamma network 训练目标：最小化 (r_t + γ_ϕ(s_t)·sg[V(s_{t+1})] - sg[G_t^(n)])²
- **关键**：将 γ→0 不会最小化此损失（因为 r_t ≠ G_t^(n)），从而避免了 collapse 问题
- 参考折扣 γ̄ 通过 EMA 缓慢追踪 replay 分布的均值折扣

### 正则化项
- Deviation penalty：锚定 γ_ϕ 接近 γ_target
- Variance penalty：鼓励平滑性
- Boundary penalty：避免 γ 值靠近上下界

### 理论结果（tabular 假设，finite actions）
1. **Soft Policy Evaluation**：β-contraction（β = sup_s γ(s) < 1），Banach 不动点定理保证收敛
2. **Soft Policy Improvement**：Q^{π_new}(s,a) ≥ Q^{π_old}(s,a) 单调提升
3. **Convergence**：重复 policy evaluation + improvement 收敛
4. **Error Bound**：‖Q_1^π - Q_2^π‖_∞ ≤ max_s|γ(s)-γ| / [(1-β)(1-γ)] · (R + α log(1/ε))，差距与 max|γ(s)-γ| 线性相关


## Experiments

### 环境和基线
- **算法**：SAC-AdaGamma, PPO-AdaGamma vs. fixed-γ SAC/PPO (γ=0.99), uncertainty-based adaptive-γ baseline, cross-validated adaptive-γ network
- **环境**：SafetyPointGoal1-v0（安全约束 + reward-cost tradeoff）, Humanoid-v4（高维 17-DoF）, Ant-v4（接触丰富动力学）, 经典 Gymnasium 任务, JD Logistics 真实推荐系统
- **种子**：5 seeds，每 10^4 步评估
- **AdaGamma 超参**：n=5 step returns, γ_init=0.98, warmup 10^5 steps, γ_ref 每 5 episodes 更新（EMA τ=0.1）

### 主要结果
- **SafetyPointGoal1-v0**：AdaGamma 在 SAC 和 PPO 上均取得最佳 reward-cost tradeoff；uncertainty-based baseline 已优于 fixed-γ，AdaGamma 进一步提升
- **Humanoid-v4**：AdaGamma 在 SAC 和 PPO 上均为最佳，SAC 上增益最大；cross-validated baseline 在此任务上表现弱（collapse）
- **Ant-v4**：AdaGamma 在 SAC/PPO 上均为最佳，接触丰富动力学中状态自适应时间权重的价值突出
- **JD Logistics A/B 测试**：10% 生产流量，4 周在线测试，AdaGamma-SAC vs. 标准 SAC，推荐诱导订单量持续优于基线，统计显著
- **经典控制**：CartPole-v1 达到满分 500（降低方差），Pendulum/MountainCarContinuous/Acrobot 上与基线持平或略优

### 消融实验
- **训练目标比较**：cross-validated baseline 在所有环境 collapse 到 γ_min；uncertainty-based 选择不那么极端但仍是全局折扣；AdaGamma 学习任务依赖的平均折扣
- **Fixed-γ 匹配测试**：将 fixed-γ 设为 AdaGamma 学到的均值，仍然不如 AdaGamma → 增益来自状态依赖性而非更好的全局 γ
- **网络架构**：隐藏维度 {8,16,32,64,128,256,512}，256 后饱和，开销极低
- **Return horizon n**：n=5 最佳 reward-cost tradeoff，n=10/20 稳定性下降（尤其 PPO）
- **跨算法一致性**：SAC-AdaGamma 和 PPO-AdaGamma 在 SafetyPointGoal1、Humanoid、Pendulum 上的平均学习 γ 高度一致，说明 γ_ϕ(s) 反映环境级时间结构

### Table 数据说明
论文 Table 1-12 的具体数值以 HTML 表格和图片形式呈现，文本提取中未捕获精确数字。上描述基于正文文字叙述。


## Limitations

1. **增益依赖于异构时间结构**：在时间同构的任务上增益可能有限（Appendix J 明确承认）
2. **理论局限**：仅提供 tabular/finite action 下的算子级分析，不是完整的 deep RL + 函数逼近收敛保证
3. **PPO 集成缺少理论支撑**：PPO 的 modified GAE 和 clipping 没有对应的理论分析
4. **超参数敏感**：γ_min/γ_max、n、warmup 长度、λ_dev/λ_var/λ_bound 等多个超参数需要调优
5. **实验环境偏传统**：主要在 MuJoCo 连续控制和推荐系统上验证，未涉及高维感知输入（图像）或复杂机器人操控任务
6. **参考折扣 γ̄ 设计**：EMA 追踪机制引入额外超参数 τ_ref 和更新频率 M


## Key Takeaways

1. **对 DLO 操控的启示**：DLO 任务中不同阶段（接近、接触、操控、释放）具有明显不同的时间结构，AdaGamma 的状态依赖折扣思想可能有助于改善长视界 DLO 操控中的 credit assignment
2. **Return-consistency 设计思路**：通过让单步估计匹配多步 return 来训练辅助模块的思路，可推广到其他需要学习辅助信号（如 termination、option duration）的场景
3. **即插即用性**：仅修改 bootstrap target 的接口设计，使得该方法容易集成到现有 RL pipeline 中
4. **Gamma Network 轻量性**：2 层 256 维 MLP 即可，计算开销可忽略
5. **Sim-to-Real 相关性有限**：该方法不直接解决 sim-to-real gap，但可能通过自适应时间传播改善仿真训练的策略质量

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[wang-yaomin|Wang, Yaomin]]
