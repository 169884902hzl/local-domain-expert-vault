---
title: "Betting for sim-to-real performance evaluation"
tags: [imitation, RL, sim-to-real]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算法，用合成分布推断机械臂 pick-and-place 精度和人形机器人步态跟踪性能"
authors: "Mahboob, Zaid; Chen, Yujia; Weng, Bowen"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "56NH6KB5"
---
## 摘要

This paper studies the problem of robot performance evaluation, focusing on how to obtain accurate and efficient estimates of real-world behavior under severe constraints on physical experimentation. Such estimates are essential for benchmarking algorithms, comparing design alternatives, validating controllers, and supporting certification or regulatory decision-making, yet real-world testing with physical robots is often expensive, time-consuming, and safety-limited. To mitigate the scarcity of real-world trials, sim-to-real（仿真到真实迁移） methodologies are commonly employed, using low-cost simulators to inform, supplement, or prioritize physical experiments. Departing from (and complementary to) existing approaches in variance reduction (e.g., importance-sampling variants) or bias-correction (e.g., through prediction-powered inference or learned control variates), we examine this performance-evaluation problem through the lens of betting. We establish theoretical conditions under which a betting mechanism can yield accurate and efficient estimates (provably outperforming the Monte Carlo estimator) and we characterize how such bets should be constructed. We further develop theoretically grounded yet practically implementable approximations of the ideal bet, and we provide concrete decision rules that diagnose when these approximate betting strategies are working as intended. We demonstrate the effectiveness of the proposed methods using both synthetic examples and cross-fidelity computational simulators. Notably, we also showcase an illustrative case in which a group of synthetic distributions are used to infer the real-world pick-and-place accuracy of a robotic manipulator, a seemingly unconventional sim-to-real（仿真到真实迁移） transfer that becomes natural and feasible under the proposed betting perspective. Programs for reproducing empirical results are available at https://github.com/ISUSAIL/Bet4Sim2Real.

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移

## 关键贡献

1. **首次将 sim-to-real 性能评估形式化为序贯赌博问题**（Algorithm 1）：仿真器引导下注，产生 bet-weighted estimator
2. **证明 Kelly 准则与统计最优估计策略近似等价**（Theorems 1 & 2）：最大化财富增长的策略恰好实现最优逆方差加权
3. **提出基于 Cover universal portfolio 原则的实用算法**（Algorithm 2）：维护 K 个仿真器专家，用 Gaussian log-score 自适应重加权
4. **证明财富增长本身就是诊断信号**（Theorem 3）：财富是 no-edge 零假设下的 supermartingale，财富增长意味着方法有效
5. **三个实验场景验证**：合成分布、SO-ARM101 pick-and-place、Unitree G1 步态跟踪
## 结构化提取

- Problem: 在真实实验稀缺条件下，高效准确估计固定策略的真实世界期望性能 μ = E_P[ψ(x)]
- Method: 序贯 Kelly 赌博框架 + Cover universal portfolio 近似，用仿真器银行提供预测信号，bet-weighted estimator 替代 MC estimator
- Tasks: 机器人性能评估（pick-and-place 精度评估、步态速度跟踪误差评估）
- Sensors: OptiTrack 动捕系统（pick-and-place），MuJoCo 内部状态（步态）
- Robot Setup: SO-ARM101 低成本机械臂（imitation learning 策略），Unitree G1 人形机器人（RL 步态策略）
- Metrics: 均方误差（MSE）、win rate（相对 MC）、财富增长、95% 置信区间相对半宽
- Limitations: i.i.d. 假设、仅标量均值、近似算法无理论保证、超参数未系统刻画、未测试视觉仿真器
- Evidence Notes:

  - 合成实验中 ideal Kelly 70-100% win rate vs MC，approx Kelly 60-80%
  - 真实 pick-and-place 中 ideal Kelly 主导，Sim_172 最佳近似
  - 步态跟踪中 domain-randomized 仿真器后期收敛后主导
  - vs 最优 IS oracle：Kelly 显著胜出（IS 仅 ~50-55% win rate）
  - vs PPI/SureSim：在公平预算下 Kelly 优于 SureSim
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文抓取）
- Evidence Coverage: complete（涵盖理论、算法、三个实验场景及补充材料）
- Confidence: high
- Summary: 将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算法，用合成分布推断机械臂 pick-and-place 精度和人形机器人步态跟踪性能


## Problem

机器人性能评估的核心问题：给定一个**固定的**策略/控制器，如何在真实世界实验极其有限的条件下（昂贵、耗时、安全受限），高效且准确地估计其在真实环境中的期望性能 $\mu = \mathbb{E}_{x \sim P}[\psi(x)]$？

现有方法分两类：
1. **方差缩减**（如 importance sampling）：需要构造好的提案分布，实际效果受限于 sim-real 匹配度
2. **偏差校正**（如 PPI/prediction-powered inference）：需要学习偏差修正函数，同样依赖仿真保真度

两类方法都暗示"好仿真器 = 接近真实"，这与 policy transfer 中 domain randomization "故意失配"的成功经验矛盾。

**核心洞察**：仿真器不需要忠实还原现实，只需要提供"预测优势"（predictive edge）。


## Method

### 1. 抽象序贯赌博算法（Algorithm 1）
- 每轮 t：先从仿真器 $Q_\theta$ 采样积累信息 $S_t$，再决定下注 $b_t$（方向+大小）
- 下注方向：双赌机制——判断真实样本 $\psi(x_t)$ 相对当前 running mean $\tau_{t-1}$ 的偏移方向
- 如果 $b_t > 0$，则采样真实样本，计算收益 $Y_t$，更新财富 $W \leftarrow W(1 + b_t Y_t)$
- 输出 bet-weighted estimator：$\hat{\mu}_{BW} = \sum w_t \psi(x_t)$，其中 $w_t = b_t / \sum b_j$

### 2. 理论基础
- **Theorem 1**：Bet-weighted estimator 优于 MC 当且仅当 方差缩减 > 偏差惩罚
- **Theorem 2**：Kelly 下注 $b_t \propto \kappa_{t-1}/\sigma_t^2$，诱导的权重等价于逆方差加权 $w_t \propto 1/\sigma_t^2$
- **Theorem 3**：在 no-edge 零假设下，$\mathbb{P}_{H_0}(W_T \geq 1/\alpha) \leq \alpha$（基于 Ville 不等式的 supermartingale 界）

### 3. 实用近似算法（Algorithm 2）
- 维护 K 个仿真器专家 $\{Q_{\theta^{(k)}}\}_{k=1}^K$，各提出预测分布 $(\mu^{(k)}, (\sigma^{(k)})^2)$
- 加权混合：$m_t = \sum \pi_t^{(k)} \mu^{(k)}$，$v_t = \sum \pi_t^{(k)} (\sigma^{(k)})^2$
- 下注大小：$b_t = \lambda |m_t - \tau_{t-1}| / v_t \wedge 1$，方向 $\text{sign}(m_t - \tau_{t-1})$
- 观测真实结果后，用 Gaussian log-score 更新专家权重：$s_t^{(k)} = s_{t-1}^{(k)} - \eta \ell(y_t; \mu^{(k)}, (\sigma^{(k)})^2)$
- Softmax 归一化得新权重 $\pi_t^{(k)}$

### 4. 与现有方法的关系
- **非替代**而是互补 IS 和 PPI
- 关键差异：不要求仿真器匹配真实，容忍偏差以换取预测信号
- 只有两个超参数：学习率 $\eta$ 和 Kelly fraction $\lambda$


## Experiments

### III-A 合成分布实验
- **设置**：3 组 Real 分布（6/20/40 个），4 组 Sim 专家库（17/35/94/172 个），性能函数 $\psi(x) = x$
- **指标**：win rate（在相同随机种子下，betting 估计误差 < MC 估计误差的比例），100 次独立重复
- **结果**：
  - Ideal Kelly：70-100% win rate，全面优于 MC
  - Approx Kelly（Sim_172）：60-80% win rate
  - 更多专家不一定更好（Sim_35 常优于 Sim_94）
  - 财富增长验证 Theorem 3（图 2b）
- **vs IS**：最优 IS oracle 版本仅 ~50-55% win rate，Kelly 显著胜出（因 IS 的自归一化偏差和非自适应性）

### III-B Pick-and-Place（真实机械臂）
- **机器人**：SO-ARM101 低成本机械臂
- **策略**：基于 tele-op 数据的模仿学习策略（ACT 训练）
- **任务**：将绿色桶从固定位置移动到偏移 102mm 的目标位置，60s 超时
- **测量**：OptiTrack 动捕系统（5 个 Primex 22 相机，≤0.15mm 精度），Euclidean 距离
- **Ground truth**：119 次试验 MC 估计，95% CI 相对半宽 0.13
- **i.i.d. 保证**：每次试验全断电重启 + ≥60s 冷却
- **性能函数**：放置误差归一化至 [0,1]（单位 10cm，最大 30cm）
- **结果**：Ideal Kelly 主导，half-Kelly 前期更稳定，Sim_172 最佳近似版本，Sim_17_biased 因严重偏差而无效

### III-C 步态跟踪（Sim-to-Sim）
- **机器人**：Unitree G1 人形机器人
- **策略**：RL 步态策略（RSL-SDK 框架）
- **环境**：MuJoCo 仿真器
- **任务**：4s 试验，两段连续速度指令 $(v_x, v_y) \in [-1,1]^2$，速度跟踪误差归一化
- **仿真器银行**：10 个 domain-randomized MuJoCo 专家（质量、阻尼、摩擦、随机种子），外加合成 Sim 变体
- **Ground truth**：552 次试验，95% CI 相对半宽 < 0.02
- **结果**：合成分布在前期较好（"幸运"初猜），domain-randomized 仿真器后期快速收敛并主导

### vs PPI（SureSim）
- 在步态任务上，SureSim 在公平仿真预算下不如 MC 和 Kelly
- 允许更大仿真预算时 SureSim 可接近 Kelly 水平，但这不再是公平比较
- 两者互补：PPI 擅长置信区间保证，Kelly 擅长点估计精度


## Limitations

1. **实用算法缺乏近似保证**：Algorithm 2 对 ideal Kelly 的近似质量尚无理论刻画（可借助 Cover 的 regret bound 理论，但未在本文完成）
2. **i.i.d. 假设**：实际机器人实验可能不满足独立同分布，需要额外工程手段（如全断电重启）
3. **仅限标量性能度量**：目前仅适用于一维均值估计，未扩展到多维或分布估计
4. **超参数敏感性未系统刻画**：$\eta$ 和 $\lambda$ 的选择影响结果，但缺乏系统指导
5. **未测试大规模视觉仿真器**：理论适用于降维后的标量测量，但尚未在富含视觉感知的高维仿真中验证


## Key Takeaways

1. **全新视角**：sim-to-real 性能评估可以从"赌博"角度理解——仿真器是信息源而非拟真工具。这对我们的 DLO 操控研究有启发：可以用多个"不精确但多样"的绳索仿真器来预测真实操控精度
2. **Kelly 准则的妙用**：最大化财富增长 = 最优逆方差加权。bet size ∝ advantage/variance 是一个简洁且通用的启发式
3. **财富作为诊断信号**：如果财富在增长，方法就在工作。这是一个无需 ground truth 的在线诊断工具
4. **Domain randomization 的理论支持**：传统上 domain randomization 是"工程经验"，本文为其在性能评估中的作用提供了理论基础——多样性本身就是优势
5. **对 DLO 操控的潜在应用**：评估双臂绳索操控策略的 pick-and-place 精度时，可以用多个不同物理参数的绳索仿真器作为 expert bank，无需精确建模绳索动力学就能获得更好的性能估计

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[mahboob|Mahboob, Zaid]]
- [[chen-yujia|Chen, Yujia]]
- [[weng-bowen|Weng, Bowen]]
