---
title: "Generative actor-critic with soft bridge policies"
tags: [VLM, RL, diffusion, diffusion-model, flow-matching]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBench 高维连续控制任务上取得更优的 compute-return 权衡。"
authors: "He, Ke; He, Le; Tang, Shunpu; Wang, Yafei; Fan, Lisheng"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GIFQ8VTC"
---
## 摘要

Expressive generative policies such as diffusion（扩散） and flow models are appealing for MaxEnt online reinforcement learning（强化学习） because of their ability to model multimodal（多模态） and highly non-Gaussian action distributions. However, training effective soft generative policies faces two obstacles that often arise together. First, marginal action densities are often unavailable, so existing methods typically rely on entropy bounds, heuristic proxies or approximations. Second, iterative shared-parameter samplers raise inference cost and require backpropagation through time over repeated network evaluations, increasing memory cost and destabilizing policy optimization. These obstacles motivate us to seek a generative policy that exposes a tractable MaxEnt objective while requiring only a single sampled actor forward pass for action generation. To this end, we propose soft generative actor-critic (SoftGAC), whose actor defines a stochastic bridge from a fixed base latent to a terminal action latent in pre-tanh space. This structured bridge allows us to lift the MaxEnt objective as an analytically tractable path-wise relative-entropy objective against a high-entropy reference process. In practical finite-step implementation, this relative entropy reduces exactly to sampled transition control energy and thus provides principled soft regularization. Moreover, we keep the single-pass actor lightweight by using small step-specific bridge transitions, each evaluated only once per sampled action, while maintaining a parameter budget comparable to strong actor baselines. Extensive experiments on challenging continuous-control benchmarks show that SoftGAC attains higher or competitive returns than strong generative policy baselines, including diffusion（扩散） and flow-matching policies, while staying in the low-latency regime of one-pass actors and showing considerable improvements in the compute-return tradeoff.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 视觉-语言模型、强化学习、扩散模型、扩散模型、Flow Matching

## 关键贡献

1. **路径空间软目标公式化**：将 MaxEnt RL 的端点 KL 正则化器提升到完整生成路径空间，证明路径 KL 包含端点 KL 作为其边际分量，并刻画了无限制和固定基两种情况下的最优解。
2. **软桥策略架构**：设计 K=6 步轻量高斯残差转移构成 pre-tanh 潜空间中的随机桥，路径正则化器精确化为采样的转移控制能量，无需端点熵估计。
3. **实证验证 compute-return 权衡**：在 12 个高维连续控制任务上（DMC + HumanoidBench），SoftGAC 在保持单次前向通过推理延迟（61-75 μs）的同时，取得优于或持平强生成式基线（FLAC, DIME, FlowRL, QSM, QVPO）的回报。
## 结构化提取

- Problem: MaxEnt 在线 RL 中表达性生成式策略（扩散、flow）面临端点密度不可得和迭代采样器开销大的双重障碍
- Method: SoftGAC——路径空间 MaxEnt 目标 + K=6 步轻量高斯桥转移 + 控制能量正则化
- Tasks: DMC Humanoid (Run/Walk/Stand), DMC Dog (Run/Trot/Walk/Stand), HumanoidBench H1 (Walk/Run/Hurdle/Stair/Maze)
- Sensors: 向量观测（本体感受+任务相关状态）
- Robot Setup: 仿真环境（MuJoCo 物理引擎）：双足人形、四足犬形、19-DOF 人形
- Metrics: IQM return (88 seeds), 95% bootstrap CI, per-action inference time (μs), actor parameter count
- Limitations: 有限步参考的端点偏差；架构超参数（K, 基分布, ρ_ctrl）需选择；未验证视觉输入和真实机器人
- Evidence Notes:

  - 路径 KL 分解为端点 KL + 条件路径 KL（Proposition 1，完整证明 Appendix A.1）
  - 无限制/固定基最优桥的完整刻画（Theorem 1-2，Appendix A.2-A.3）
  - 控制能量消融 α=0 导致高维任务一致退化（Figure 4）
  - 桥深度 K=6 为 H1 Hurdle 上最优深度（Figure 14）
  - 推理延迟 61-75 μs，与单步 flow 同量级（Figure 3, Apple M3 Pro）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: full
- Confidence: high
- Summary: 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBench 高维连续控制任务上取得更优的 compute-return 权衡。


## Problem

MaxEnt 在线 RL 中使用表达性生成式策略（扩散模型、flow matching）面临两个核心障碍：
1. **边际动作密度不可得**：扩散/flow 策略的动作分布是通过隐式生成过程得到的，端点密度需要积分所有可能的潜变量路径，通常不可解析。现有方法只能用熵界、启发式代理或近似。
2. **迭代共享参数采样器开销大**：高 NFE 的扩散/flow 采样器在推理时需要多次网络评估，训练时还需要通过这些步骤做 BPTT，增加内存消耗和训练不稳定性。降低 NFE 又会导致性能急剧下降。


## Method

### 核心思路
将 MaxEnt RL 从端点动作分布提升到完整潜变量生成路径。路径空间目标：
- 𝒥_path(P_θ|s) = E_τ~P_θ[Q(s, T(z_K))] - α·D_KL(P_θ(·|s) || R)

其中 R 是高熵参考路径律。

### 关键理论结果
- **Proposition 1**：路径 KL 分解为端点 KL + 条件路径 KL，前者正是 SAC 的均匀先验正则化器。
- **Theorem 1**（无限制最优）：最优路径律是值倾斜的参考律，端点动作分布恢复 Boltzmann 策略。
- **Theorem 2**（固定基最优）：给定固定基分布，最优解约束在所选基族内，Corollary 1 量化了与无限制最优的偏差。

### 软桥策略架构
- **基分布**：logistic 参考密度（arctanh(Uniform(-1,1)^da)），tanh 映射后在有界动作空间为均匀分布。
- **K=6 步高斯残差转移**：每步用小型单层 MLP 产生 drift 和正对角方差，z_{k+1} = z_k + h·u_θ,k + sqrt(2h)·σ_θ,k·ε。
- **参考桥**：基于 q_ref(z) 的 score (−2tanh(z)) 构造的 Euler 高斯核，r_k(z_{k+1}|z_k) = N(z_k − 2h·tanh(z_k), 2hI)。
- **控制能量**：局部 KL 的求和，对高斯转移有闭式解：
  C_k = (1/2) Σ_i [σ²_{θ,k,i} + (μ_{θ,k,i} - μ_{R,k,i})²/(2h) - 1 - log σ²_{θ,k,i}]

### 训练
- **Actor 更新**：最小化 α·C_θ(s,τ) - Q_φ^min(s, T(z_K))。
- **Critic**：twin C51 categorical critic + CrossQ-style 更新。
- **温度调节**：SAC-style dual update，目标控制能量预算 ρ_ctrl·K·da，默认 ρ_ctrl=0.2。
- **推理**：单次前向通过 K 个桥块，丢弃控制能量簿记。


## Experiments

### 基准设置
- **任务**：12 个连续控制任务
  - DMC Humanoid: Run, Walk, Stand
  - DMC Dog: Run, Trot, Walk, Stand
  - HumanoidBench H1: Walk, Run, Hurdle, Stair, Maze (19 自由度人形)
- **基线**：FLAC, DIME, FlowRL, QSM, QVPO, CrossQ-SAC
- **评估**：88 seeds 的四分位均值 (IQM)，95% bootstrap 置信区间
- **统一框架**：所有方法在 StableBaselines3 + JAX 统一代码库中重实现，共享相同 critic 更新

### 主要结果
- **性能**：在高维长时域运动任务（Humanoid Run, Dog Run, H1 Hurdle, H1 Stair）上优势最大。在 CrossQ-SAC 已强的任务（Humanoid Walk, H1 Maze）上保持竞争。
- **推理延迟**：61-75 μs/action（Apple M3 Pro CPU），与单步 flow 基线同量级，远低于高 NFE 扩散基线。
- **参数量**：Actor 参数预算与强基线可比（512 宽度，Dog 任务用 256）。

### 消融实验
- **软正则化器消融**（α=0）：移除路径空间正则后 Humanoid Run/Walk, Dog Run, H1 Hurdle 一致退化，说明增益不仅来自桥参数化。
- **桥深度消融**：K=2→4 明显提升，K=6 最优，K>6 收益边际/不稳定。
- **Actor 宽度消融**：所选尺寸非脆弱点，更宽可能进一步提升但目标是在可比参数预算下验证。
- **控制预算敏感性**：ρ_ctrl=0.2 是跨任务的稳定中间值，非针对单一任务调优。


## Limitations

1. **有限步参考的端点偏差**：实际使用有限步高斯桥转移，端点与均匀先验的连接依赖参考离散化和基律选择（Appendix D 讨论了此偏差）。
2. **架构超参数**：引入桥深度 K、基分布、目标控制能量预算等选择。
3. **仅验证连续控制 benchmark**：未涉及视觉输入、真实机器人或部分可观测环境。
4. **固定基分布**：不能以状态依赖方式重新加权初始潜变量分布，Corollary 1 量化了此偏差但未提出缓解方案。


## Key Takeaways

1. **路径空间视角的价值**：将 MaxEnt RL 从端点提升到路径空间，使隐式生成式策略的正则化器变为可解析计算的路径相对熵，绕开了端点密度不可得的根本困难。
2. **单次前向通过的设计原则**：通过小步特定转移块（而非迭代重用共享参数），保持推理效率的同时允许桥结构进行值引导的传输。
3. **与 DLO/机器人操控的关联**：SoftGAC 的多模态动作生成能力对 DLO 操控等多模态策略场景有潜力，但目前只在 MuJoCo 风格的运动控制任务上验证，未涉及视觉或真实机器人。桥策略的多模态表达力是否在操控任务中同样有效需要进一步研究。
4. **Flow matching 在 RL 中的新思路**：不同于直接将 diffusion/flow matching 用于行为克隆或离线 RL，SoftGAC 在在线 RL 框架中将生成过程结构化为桥，提供了一个理论优雅的替代方案。

## 相关概念

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[deformable-linear-object]]

## 相关研究者

- [[he-ke|He, Ke]]
- [[fan-lisheng|Fan, Lisheng]]
