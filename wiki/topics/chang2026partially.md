---
title: "Partially equivariant reinforcement learning in symmetry-breaking environments"
tags: [manipulation, imitation, VLM, RL]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 ICLR 2026。"
authors: "Chang, Junwoo; Park, Minwoo; Seo, Joohwan; Horowitz, Roberto; Lee, Jongmin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "R7TN2JD4"
---
## 摘要

Group symmetries provide a powerful inductive bias for reinforcement learning（强化学习） (RL), enabling efficient generalization across symmetric states and actions via group-invariant Markov Decision Processes (MDPs). However, real-world environments almost never realize fully group-invariant MDPs; dynamics, actuation limits, and reward（奖励） design usually break symmetries, often only locally. Under group-invariant Bellman backups for such cases, local symmetry-breaking introduces errors that propagate across the entire state-action space, resulting in global value estimation errors. To address this, we introduce Partially group-Invariant MDP (PI-MDP), which selectively applies group-invariant or standard Bellman backups depending on where symmetry holds. This framework mitigates error propagation from locally broken symmetries while maintaining the benefits of equivariance, thereby enhancing sample efficiency and generalizability. Building on this framework, we present practical RL algorithms -- Partially Equivariant (PE)-DQN for discrete control and PE-SAC for continuous control -- that combine the benefits of equivariance with robustness to symmetry-breaking. Experiments across Grid-World, locomotion, and manipulation（操控） benchmarks demonstrate that PE-DQN and PE-SAC significantly outperform（优于） baselines, highlighting the importance of selective symmetry exploitation for robust and sample-efficient RL. Project page: https://pranaboy72.github.io/perl_page/

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习

## 关键贡献

1. **理论分析**：推导了局部对称破缺如何通过单步 Bellman 备份误差 δ(s,a) = ε_R(s,a) + 2γV_max ε_P(s,a) 引发全局值函数偏差（Lemma 1, Proposition 1）
2. **PI-MDP 框架**：引入 Partially Group-Invariant MDP，通过门控函数 λ(s,a) ∈ {0,1} 在每个状态-动作对选择等变或标准 Bellman 备份，理论上证明其最优算子是 γ-收缩的，固定点与真实最优 Q* 的偏差有界（Corollary 1: ∥Q*_H − Q*_N∥_∞ ≤ (1−γ)^−1 ∥(1−λ̄)δ∥_∞）
3. **实用算法**：PE-DQN（离散控制）和 PE-SAC（连续控制），通过等变/非等变单步预测器的分歧（disagreement）自动检测对称破缺区域，无需人工标注
## 结构化提取

- Problem: 等变 RL 在局部对称破缺环境下，单步 Bellman 误差全局传播导致值估计偏差和训练失败
- Method: PI-MDP 框架 + 门控混合值函数（等变/非等变双头）+ 预测器分歧自动检测对称破缺
- Tasks: Grid-World 目标到达（离散）、Hopper/Ant/Swimmer 运动（连续）、Fetch Reach 和 UR5e Reach 操控（连续）
- Sensors: 关节角度/角速度、末端执行器位置/速度/朝向、目标位置/朝向（状态向量，无视觉）
- Robot Setup: Fetch 机器人（末端受限于垂直方向）、UR5e 机械臂（自由末端执行器朝向、SE(3) 目标）
- Metrics: Average Return（累计奖励），5-8 个随机种子取标准误差
- Limitations: 训练时间增加（辅助网络）、全局对称破缺时退化为标准 RL、未验证视觉输入
- Evidence Notes:

  - Lemma 1 和 Proposition 1 给出了局部对称破缺到全局值偏差的理论界
  - Theorem 1 证明 PI-MDP 最优算子是 γ-收缩的
  - Corollary 1 给出 PI-MDP 固定点与真实最优 Q 的偏差界
  - Fig. 3-5 展示 6 个环境下的性能对比，PE-DQN/PE-SAC 在对称破缺严重时显著优于 baselines
  - Fig. 10 可视化了等变误差从局部到全局的传播模式
  - 消融实验（Fig. 6-9）验证了硬门控、独立 trunk、κ 参数的鲁棒性
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: full（全文 103k 字符，涵盖正文、附录、超参数表）
- Confidence: high
- Summary: 提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 ICLR 2026。


## Problem

群对称性为 RL 提供了强归纳偏置，但真实环境几乎不存在完全群不变的 MDP。动力学、执行器限制、奖励设计等因素在局部破坏对称性后，等变 Bellman 备份引入的单步误差会通过收缩映射放大并传播到整个状态-动作空间（全局值估计偏差，见 Proposition 1: ∥Q*_N − Q*_E∥_∞ ≤ (1−γ)^−1 ∥δ∥_∞）。现有近似等变方法（RPP、Approximately Equivariant RL）在表示层全局放松等变性，但无法阻止局部误差的全局传播。


## Method

### 核心思想
PI-MDP 定义了一个插值 MDP：R_H(s,a) = (1−λ)R_E(s,a) + λR_N(s,a)，P_H 同理。门控函数 λ(s,a) 决定在每个状态-动作对上使用等变代理 MDP M_E 还是真实 MDP M_N 的奖励和转移核。

### 门控函数学习（λ_ω）
训练两个单步预测器：
- P̂_E：等变预测器，约束遵循 M_E 的群对称性
- P̂_N：非等变预测器，可逼近真实 M_N 的动力学

分歧分数 d(s,a) = D(P̂_E(·|s,a), P̂_N(·|s,a)) 在对称区域小（两预测器一致），在对称破缺区域大（P̂_E 只能表示群平均代理 P_E，P̂_N 可逼近真实 P_N）。使用 Welford 算法维护分歧的运行统计量，通过 z-score 阈值化生成伪标签 y(s,a) ∈ {0,1}，用 BCE 损失训练门控网络 λ_ω。

### 评判器（Critic）
门控混合值函数：Q_θ(s,a) = (1−λ_ω(s,a)) Q_{E,θ}(s,a) + λ_ω(s,a) Q_{N,θ}(s,a)
硬门控实现为 Bernoulli 采样，实际退化为 Q_E 或 Q_N 的二选一切换。

### 策略（Actor）
状态级门控函数 λ_ζ(s) 通过 expectile regression 保守地逼近 max_a λ_ω(s,a)，确保只要任一动作存在对称破缺就激活非等变策略头。策略采用 PoE（Product-of-Experts）形式：
π_φ(·|s) ∝ π_{E,φ}(·|s)^{1−λ_ζ(s)} · π_{N,φ}(·|s)^{λ_ζ(s)}

### 训练细节
- 预测器、评判器、策略使用独立的网络 trunk（共享 trunk 会导致不稳定，见消融 Fig. 8）
- 等变网络：Grid-World 用 MDP-Homomorphic Networks，连续控制用 EMLP
- 门控网络训练与 RL 更新梯度隔离（stop-gradient）
- 使用 EMA 目标门控减少方差
- Warm-start 阶段禁用门控损失，使用先验偏置


## Experiments

### 环境
| 环境 | 对称群 | 类型 | 训练步数 | 种子数 |
|------|--------|------|----------|--------|
| Grid-World | C4 | 离散 | 100K | 5 |
| Hopper-v2 | Z2 | 连续-运动 | 1M | 8 |
| Ant-v2 | Z4 | 连续-运动 | 1M | 8 |
| Swimmer-v2 | Z2 | 连续-运动 | 1M | 8 |
| Fetch Reach | SO(3) | 连续-操控 | 30K | 5 |
| UR5e Reach | SO(3) | 连续-操控 | 500K | 5 |

### Baselines
1. Vanilla RL（标准 MLP）
2. Exact-Equivariant（严格等变 EMLP）
3. RPP（Finzi et al., 2021a，残差路径先验）
4. Approximately Equivariant RL（Park et al., 2025）

### 主要结果
**Grid-World**（Fig. 3）：
- 无障碍物时 PE-DQN 行为等同严格等变 DQN
- 随障碍物增加，严格等变 DQN 性能急剧下降，近似等变方法仅略优于 vanilla DQN
- PE-DQN 在所有障碍物数量下保持强性能

**Locomotion**（Fig. 5）：
- Hopper：PE-SAC 学习最快，但 vanilla SAC 渐近回报略高
- Ant：PE-SAC 在样本效率和最终性能上均占优
- Swimmer：对称性近乎精确，严格/近似等变 SAC 达到最高回报，PE-SAC 快速收敛至竞争水平

**Manipulation**（Fig. 5）：
- Fetch Reach：PE-SAC、严格等变 SAC、近似等变 SAC 性能相近
- UR5e Reach（自由末端执行器朝向，SE(3) 目标）：严格等变和近似等变 SAC 不稳定或崩溃，PE-SAC 保持稳定并取得最佳回报

### 消融实验
- **Actor 门控方案**（Fig. 6）：可训练状态门 λ_ζ(s) 与 sampled-max 方案（K=4,8）性能相近
- **硬 vs 软门控**（Fig. 7）：硬门控（Bernoulli 采样）比软门控（凸组合）更稳定
- **网络 trunk 共享**（Fig. 8）：独立 trunk 最优，共享 Q/策略 trunk 显著损害性能
- **κ 敏感性**（Fig. 9）：方法对 κ 不敏感，粗略估计对称破缺稀疏/密集即可选择鲁棒阈值


## Limitations

1. **计算开销**：辅助预测器和门控网络增加训练时间（每步需要额外的前向/反向传播）
2. **全局对称破缺**：当对称破缺无处不在（如重力）时，框架主要退化为非等变网络，相对于标准 RL 无明显优势
3. **视觉控制未覆盖**：当前仅验证了基于状态的 RL，尚未扩展到视觉输入


## Key Takeaways

1. **局部 vs 全局等变放松**：PI-MDP 的核心洞见是在 MDP 层面（而非表示层）进行局部选择——在对称区域严格使用等变归纳偏置获得样本效率，在破缺区域回退标准网络保持鲁棒性。这比全局放松等变性（RPP、Approximately Equivariant）更精确。

2. **DLO 操控相关性**：DLO 操控中，对称性通常被夹持位置、DLO 形变历史、重力等局部因素打破。PE-RL 的门控机制可以适应这种局部对称破缺模式。但 DLO 任务的对称性更复杂（不是简单的旋转/反射），需要设计合适的群表示。

3. **操控任务验证**：论文在 Fetch Reach 和 UR5e Reach 上验证了 SO(3) 对称性下的有效性。UR5e Reach 包含自由末端执行器朝向控制，更接近真实操控场景。PE-SAC 在这个任务上的优势（其他等变方法崩溃）尤其值得关注。

4. **门控检测的通用性**：基于预测器分歧的对称破缺检测不需要先验知识，可自动适应不同类型的对称破缺（动力学、奖励、接触力等），这对 Sim-to-Real 迁移有潜在价值。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[chang|Chang, Junwoo]]
