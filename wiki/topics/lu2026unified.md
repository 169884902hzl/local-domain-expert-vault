---
title: "Unified noise steering for efficient human-guided VLA adaptation"
tags: [manipulation, VLM, RL, diffusion, flow-matching]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分钟将成功率从 20% 提升至 90%"
authors: "Lu, Junjie; Qin, Xinyao; Jiang, Yuhua; Wang, Kaixin; Zhang, Chuheng et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "KQB3XUSA"
---
## 摘要

Diffusion（扩散）-based vision-language-action (VLA) models have emerged as strong priors for robotic manipulation（机器人操控）, yet adapting them to real-world distributions remains challenging. In particular, on-robot reinforcement learning（强化学习） (RL) is expensive and time-consuming, so effective adaptation depends on efficient policy improvement within a limited budget of real-world interactions. Noise-space RL lowers the cost by keeping the pretrained VLA fixed as a denoising generator while updating only a lightweight actor that predicts the noise. However, its performance is still limited due to inefficient autonomous exploration. Human corrective interventions can reduce this exploration burden, but they are naturally provided in action space, whereas noise-space finetuning requires supervision over noise variables. To address these challenges, we propose UniSteer, a Unified Noise Steering framework that combines human corrective guidance with noise-space RL through approximate action-to-noise inversion. Given a human corrective action, UniSteer inverts the frozen flow-matching decoder to recover a noise target, which provides supervised guidance for the same noise actor that is simultaneously optimized via reinforcement learning（强化学习）. Real-world experiments on diverse manipulation（操控） tasks show that UniSteer adapts more efficiently than strong noise-space RL and action-space human-in-the-loop baselines, improving the success rate from 20% to 90% in 66 minutes on average across four real-world adaptation tasks.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、扩散模型、Flow Matching

## 关键贡献

1. **UniSteer 框架**：首个统一噪声空间操控框架，将人类引导融入 noise-space 在线 RL，用于高效真实世界 VLA 适应
2. **近似 action-to-noise 反演方法**：基于固定点迭代的 flow-matching 解码器反演，在冻结生成器下提供一致的噪声监督（Proposition 1-2 保证双射性和收缩性）
3. **实验验证**：在 4 个多样化真实操控任务上，以更少人类干预和更短时间达到更高成功率，优于 noise-space RL 和 action-space IL 基线
## 结构化提取

- Problem: 预训练 flow-matching VLA 在真实部署时分布偏移，noise-space RL 探索低效，人类纠正在动作空间与噪声空间存在表示鸿沟
- Method: UniSteer — 冻结 flow-matching decoder + 轻量噪声 actor + action-to-noise 固定点反演 + SFT-then-RL 统一训练
- Tasks: Pick up Spoon, Stack Blocks, Insert Square, Fold Towel（4 个真实操控任务）
- Sensors: 侧面 RGB 相机 + 腕部 RGB 相机 + 6D 末端位姿 + 夹爪状态
- Robot Setup: AgileX Piper 单臂机器人，主从遥操作，30 Hz 控制，action horizon 16
- Metrics: 真实世界任务成功率（20 trials/任务），ID/OOD 分拆评估，适应时间
- Limitations: 反演依赖冻结 decoder 质量；仅 4 任务 1 平台验证；Fold Towel 成功率待提升；全局 Lipschitz 假设实际可能不完全成立
- Evidence Notes: Table 1（主结果）、Table 2（反演策略对比）、Table 3（迭代次数消融）、Table 4（训练调度消融）、Figure 4（效率曲线）、Figure 5-6（定性分析）、Appendix A（理论证明）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含方法、理论证明、4 个真实任务实验、消融实验、附录）
- Confidence: high
- Summary: UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分钟将成功率从 20% 提升至 90%


## Problem

基于 diffusion/flow-matching 的 VLA 模型在真实部署时面临分布偏移（场景、物体、视角、接触动力学）。在线 RL 适应代价高且交互预算有限。Noise-space RL 冻结预训练 VLA 解码器、仅训练轻量级噪声 actor，计算高效但自主探索效率低（尤其在稀疏奖励和低初始成功率下）。人类纠正干预可缓解探索瓶颈，但人类自然提供的纠正是在动作空间，而 noise-space 微调需要噪声变量上的监督——存在动作空间与噪声空间的表示鸿沟。


## Method

### 核心思想
冻结预训练 flow-matching VLA 解码器 G_θ，训练轻量级噪声 actor ψ_ϕ 预测初始噪声 z_0，解码器将噪声映射为动作 chunk。人类纠正动作 a^h 通过逐步反演 Euler 离散化的 flow decoder 反推回噪声空间目标 ẑ。

### Action-to-Noise Inversion（核心创新）
- 前向解码：K 步 Euler 积分，z_{k+1} = z_k + Δt · v_θ(z_k, t_k, s)
- 反演：从人类纠正动作 a^h 出发，对每步 Euler 进行固定点迭代反演
  - Inv_k(ẑ_{k-1}, s) := fix(z ↦ ẑ_{k-1} - Δt · v_θ(z, t_k, s))
  - M 步固定点迭代：z_k^{(m+1)} = ẑ_{k-1} - Δt · v_θ(z_k^{(m)}, t_k, s)
- 理论保证：
  - Proposition 1：全局 Lipschitz 速度场 → G_θ(s, ·) 是双射
  - Proposition 2：Δt·L < 1 时每步反演是压缩映射，固定点迭代收敛
  - Appendix A.3-A.4：有限步近似误差随 M 指数衰减

### 统一训练框架
- **RL buffer B_RL**：存储自主 rollout 和人类纠正（反演后）的 transition
- **Demo buffer B_demo**：仅存储人类纠正反演后的 noise target
- **两阶段训练**（SFT-then-RL）：
  1. L_demo = ||ψ_ϕ(s) - ẑ_h||²（从 demo buffer 采样）
  2. L_RL = -Q_ω(s, z)（从 RL buffer 采样，SAC 式优化）
- 噪声空间 critic Q_ω(s, z) 用标准 TD loss 训练

### 架构细节
- 基座模型：π₀ 架构 flow-matching action head，10 步去噪
- 噪声 actor：3 层 MLP [1024, 1024, 1024]，含 CNN 特征编码器
- 噪声维度：50（从原始动作维度 7 压缩）
- 控制频率：30 Hz，action horizon 16


## Experiments

### 实验设置
- **机器人**：AgileX Piper 单臂，主从遥操作采集人类纠正
- **传感器**：侧面 RGB 相机 + 腕部 RGB 相机 + 6D 末端位姿 + 夹爪状态
- **任务**：
  1. Pick up Spoon（拾取勺子）— pick-and-place
  2. Stack Blocks（堆叠积木）— 空间重排
  3. Insert Square（方形插入）— 精密接触丰富操作
  4. Fold Towel（折叠毛巾）— 可变形物体操控
- **初始策略**：π₀ checkpoint + 30 演示/任务 warm-start
- **评估**：每任务 20 trials（位置类任务 16 ID + 4 OOD），20% OOD 位置
- **基线**：DSRL（noise-space RL，无人类干预）、DAgger（action-space IL with 人类纠正）

### 主要结果（Table 1）
| 任务 | 训练时间 | Initial | UniSteer | DSRL | DAgger |
|------|---------|---------|----------|------|--------|
| Pick up Spoon | 45 min | 20.0% | **90.0%** | 50.0% | 70.0% |
| Stack Blocks | 60 min | 35.0% | **95.0%** | 60.0% | 70.0% |
| Insert Square | 60 min | 15.0% | **100.0%** | 70.0% | 55.0% |
| Fold Towel | 100 min | 10.0% | **75.0%** | 40.0% | 45.0% |
| **Average** | **66 min** | **20.0%** | **90.0%** | **55.0%** | **60.0%** |

- OOD 泛化：UniSteer 在所有位置类任务上实现 100% OOD 成功率（初始为 0%）
- DSRL 在 OOD 上几乎为 0%（Pick up Spoon 0%, Stack Blocks 0%, Insert Square 25%）

### 效率分析（Figure 4）
- UniSteer 平均每轮仅需 0.98 条纯人类轨迹（vs DAgger 的 8 条/轮）
- 适应曲线上升更快，时间效率显著优于两个基线

### Action-to-Noise 反演策略对比（Table 2）
- Fixed-point inversion vs Optimization-based inversion vs Direct action supervision
- 固定点反演：反演时间最短（23s vs 158s），重建误差最低（0.00122 vs 0.065），成功率 8/8
- 直接动作监督需要反向传播冻结解码器，训练时间最长且可能偏移噪声分布

### 固定点迭代次数消融（Table 3）
- M=4 已达低误差（mean 0.0025），M=16 接近饱和（mean 0.0020）
- 实际使用 M=16 作为权衡

### 训练调度消融（Table 4）
- SFT-then-RL > RL-then-SFT ≈ Only SFT > Only RL
- 先 SFT 提供更好的探索起点，再 RL 进一步优化
- Only RL 在 OOD 上表现最差（Pick up Spoon OOD 0%）


## Limitations

1. Action-to-noise 反演依赖冻结解码器质量，恢复的噪声目标可能偏离噪声 actor 的初始分布
2. 仅在 4 个任务、1 种机器人平台上验证，需要更广泛的跨机器人、长时序任务评估
3. 未与 HIL-SERL 对比（作者指出其在高频控制 + 稀疏奖励下不稳定）
4. Fold Towel 任务成功率仍有提升空间（75%），可变形物体操控仍是难点
5. 理论保证依赖全局 Lipschitz 假设，实际神经网络可能不完全满足


## Key Takeaways

1. **Noise-space adaptation 的潜力**：冻结大型生成模型、仅训练轻量级噪声 actor 是 VLA 适应的有效范式，计算成本低且稳定
2. **动作空间-噪声空间桥接是关键创新**：action-to-noise inversion 将人类直觉性的动作纠正转化为生成模型的噪声空间监督信号，是连接"人可提供的"和"模型需要的"的桥梁
3. **SFT-then-RL 的训练顺序很重要**：先用人类纠正引导探索方向，再用 RL 在奖励信号下精细化，比反向顺序或单独使用任一阶段都好
4. **对 DLO 操控的启示**：Fold Towel 任务（75%）表明可变形物体仍是挑战；noise-space 方法可能对 DLO 有价值，因为人类纠正可以提供形变过程中的关键纠正
5. **OOD 泛化的意外优势**：noise-space 人类引导不仅在 ID 上有效，还实现了完美的 OOD 泛化（100%），说明噪声空间的纠正比 action-space 更具泛化能力

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[lu-junjie|Lu, Junjie]]
- [[qin-xinyao|Qin, Xinyao]]
