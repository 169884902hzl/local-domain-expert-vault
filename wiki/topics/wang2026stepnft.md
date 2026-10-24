---
title: "$π$-StepNFT: Wider space needs finer steps in online RL for flow-based VLAs"
tags: [VLM, RL, robot-learning, flow-matching]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO few-shot 和 ManiSkill OOD 泛化上超越 PPO 等基线。"
authors: "Wang, Siting; Wang, Xiaofeng; Zhu, Zheng; Pei, Minnan; Cui, Xinyu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QGVPKBGU"
---
## 摘要

Flow-based vision-language-action (VLA) models excel in embodied control but suffer from intractable likelihoods during multi-step sampling, hindering online reinforcement learning（强化学习）. We propose \textbf{\textit{$\boldsymbolπ$-StepNFT}} (Step-wise Negative-aware Fine-Tuning), a critic-and-likelihood-free framework that requires only a single forward pass per optimization step and eliminates auxiliary value networks. We identify that wider exploration spaces necessitate finer-grained, step-wise guidance for alignment. Empirically, $π$-StepNFT unlocks latent potential on LIBERO with competitive few-shot（少样本） robustness. Moreover, it achieves superior generalization on ManiSkill, outperforming value-based baselines in OOD scenarios by preventing overfitting to multimodal（多模态） features. This property offers a scalable solution promising for complex real-world applications.

## 中文简述

提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 扩展探索空间并以逐步对比排序损失精调 flow-based VLA，在 LIBERO 和 ManiSkill 上展现少样本学习能力和 OOD 泛化优势。

**研究方向**: 视觉-语言模型、强化学习、机器人学习、flow-matching 策略优化

## 关键贡献

1. **π-StepNFT 框架**：首个无需 critic 和 likelihood 的在线 RL 方法，专为 flow-based VLA 设计。每步仅需一次 forward pass，无需辅助 value network。
2. **逐步监督 (Step-wise Supervision)**：将监督目标从 terminal 输出 x₀ 移至即时下一步去噪状态 x_{t-}，配合方差归一化，提供精确的低方差局部梯度。
3. **Logistic Contrastive Ranking Loss**：替代 weighted-MSE，消除"隐式分离惩罚"，实现 push-pull 双向信号——成功轨迹拉近正分支、推开负分支。
4. **实验验证**：LIBERO few-shot 提升 32.9%；ManiSkill OOD 场景比 PPO 高 11.1%，证明 critic-free 方法在视觉多样性场景下的泛化优势。
## 结构化提取

- Problem: Flow-based VLA 的多步 ODE 采样导致 likelihood 不可计算，无法直接应用在线 RL；SDE 扩展探索空间后 terminal supervision 信号不匹配
- Method: π-StepNFT — SDE 采样扩展探索 + step-wise mirror error + logistic contrastive ranking loss；critic-and-likelihood-free，单次 forward pass
- Tasks: 桌面物体操控（LIBERO: 4 suites × 10 sub-tasks；ManiSkill: PutOnPlateInScene, 4352 组合任务）
- Sensors: 双目 224×224 RGB（LIBERO）/ 单目 480×640 第三人称视角（ManiSkill）+ 语言指令 + 本体感知（关节角度）
- Robot Setup: 仿真环境中的机械臂（LIBERO: 7-DoF end-effector action；ManiSkill: joint-space commands）；action chunk H=5-10，denoise steps K=4
- Metrics: 成功率（success rate %），500 episodes per suite（LIBERO）；IND/OOD 分场景评估（ManiSkill）
- Limitations: 长时任务 credit assignment 弱于 PPO；未在真实机器人验证；稀疏奖励为主；超参敏感
- Evidence Notes:

  - LIBERO few-shot: π₀ SFT 57.6% → π-StepNFT 90.5%（+32.9%），π₀.₅ 77.1% → 94.0%（+16.9%）
  - ManiSkill OOD: π₀ OOD avg 50.4% vs PPO 39.3%（+11.1%）；π₀.₅ OOD avg 59.5% vs PPO 49.3%（+10.2%）
  - Semantic OOD 提升最大：π₀ 从 25.4%（PPO）→ 49.1%（π-StepNFT），近 2 倍
  - 消融确认 SDE > ODE、step-wise > terminal、ranking > wMSE、binary reward 足够
  - 理论证明：小步假设下梯度方向与 oracle mean-gap 对齐（Theorem 4.4）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（正文 6 节 + 附录 A-D，含完整证明、消融实验、超参分析）
- Confidence: high
- Summary: 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO few-shot 和 ManiSkill OOD 泛化上超越 PPO 等基线。


## Problem

Flow-based VLA 模型在 embodied control 中表现优异，但多步 ODE 采样的精确 likelihood 不可计算，阻碍了在线 RL 精调。现有方法要么通过 latent space value distillation 绕开 likelihood（如 GR-RL），要么用 SDE 近似 likelihood（如 π RL），但都面临探索宽度与监督粒度不匹配的问题。直接将 Diffusion-NFT 从图像生成迁移到具身控制存在 domain gap：SDE 扩展了探索空间但 terminal supervision 信号太粗糙，导致策略偏移。


## Method

### 核心架构
基于 OpenPi 的 π₀ 和 π₀.₅（PaliGemma-3B backbone + ~300M flow-matching action expert），冻结 VLM backbone，仅精调 action expert。

### 三大设计要素

**1. SDE 采样扩展探索（Wider Space）**
- 标准 ODE rollouts 在确定性轨迹上迅速坍缩到窄流形
- 改用 Flow-SDE（Euler-Maruyama 离散化），注入结构化噪声，迫使策略探索 expert 轨迹邻域
- SDE 转移产生高斯转移密度 q_{θ,t}(x_{t-}|x_t, c) = N(μ_{θ,t}, Σ_t)
- 均值是 velocity 的仿射变换：μ_{θ,t}(x_t, c) = U_t(x_t, t) + B_t(t)·v_θ(x_t, t, c)

**2. 逐步监督（Finer Steps）**
- 每步随机采样一个 solver step index j ~ U{0,...,K-1}
- 构造 mirror velocity candidates：v_θ⁺ = (1-β)v_old + βv_θ, v_θ⁻ = (1+β)v_old - βv_θ
- 计算方差归一化的 step errors：E_{θ,t}^± = ∥x_{t-} - μ_{θ,t}^±∥²_{Σ_t^{-1}}
- 监督目标为 x_{t-}（下一步去噪状态）而非 x₀（terminal 输出）

**3. Logistic Contrastive Ranking Loss**
- ℓ_t(θ) = softplus(½y(E^+ - E^-))，其中 y = 2r - 1
- 成功时(y>0)：拉近正分支，推开负分支
- 失败时(y<0)：反向操作
- 与 wMSE 对比：wMSE 含隐式 ∥d_t∥²_{Σ_t^{-1}} 惩罚项，抑制策略更新幅度；ranking loss 无此问题

### 理论保证
- **Lemma 4.2**：误差差等价于两个 mirror 分支的对数似然比
- **Proposition 4.3 (Bayes Monotonicity)**：增加 oracle 转移比严格增加成功后验概率
- **Theorem 4.4 (Gradient Alignment)**：小步假设下，π-StepNFT 的期望梯度方向与 oracle mean-gap 方向一致
- **Theorem 4.5**：wMSE = 对齐信号 + 隐式分离惩罚，解释了 ranking loss 的优越性

### 训练流程 (Algorithm 1)
1. 用 π_{θ_old} rollout H 步环境交互
2. 每步运行 K 步 Flow-SDE solver，随机选一步记录 transition
3. 获取 terminal 二元奖励 r ∈ {0,1}
4. 用 contrastive ranking loss 更新 θ
5. EMA 更新 θ_old：θ_old ← α_m·θ_old + (1-α_m)·θ


## Experiments

### 基准测试
**LIBERO**（4 个 suite: Spatial/Object/Goal/Long）
- 模型：π₀ 和 π₀.₅
- Few-shot SFT 初始化（π₀: 58-208 条轨迹；π₀.₅: 40 条统一轨迹）

| 模型 | 方法 | Spatial | Object | Goal | Long | Avg | ΔAvg |
|------|------|---------|--------|------|------|-----|------|
| π₀ | SFT | 65.3 | 64.4 | 49.8 | 51.2 | 57.6 | - |
| π₀ | π RL (PPO) | 98.4 | 99.4 | 96.2 | 90.2 | 96.0 | +38.4 |
| π₀ | π RL (GRPO) | 97.8 | 97.8 | 83.2 | 81.4 | 90.0 | +32.4 |
| π₀ | **π-StepNFT** | 93.5 | 98.0 | 83.7 | 86.7 | 90.5 | **+32.9** |
| π₀.₅ | SFT | 84.6 | 95.4 | 84.6 | 43.9 | 77.1 | - |
| π₀.₅ | π RL (PPO) | 99.6 | 100 | 98.8 | 93.0 | 97.9 | +20.8 |
| π₀.₅ | **π-StepNFT** | 97.8 | 100 | 98.2 | 79.8 | 94.0 | **+16.9** |

**ManiSkill** PutOnPlateInScene（4352 组合任务，IND + 3 类 OOD）

| 模型 | 方法 | IND | OOD Vision | OOD Semantic | OOD Execution | OOD Avg |
|------|------|-----|-----------|-------------|--------------|---------|
| π₀ | Full SFT | 38.4 | 32.6 | 8.4 | 13.2 | 18.1 |
| π₀ | PPO | 78.8 | 61.1 | 25.4 | 31.5 | 39.3 |
| π₀ | **π-StepNFT** | 79.2 | **69.1** | **49.1** | 33.1 | **50.4** |
| π₀.₅ | PPO | 90.9 | 68.0 | 34.5 | 45.4 | 49.3 |
| π₀.₅ | **π-StepNFT** | 85.4 | **76.9** | **56.6** | 45.1 | **59.5** |

### 消融实验
1. **随机探索**：ODE plateau 早期；SDE + noise-aware correction 显著提升（Figure 2a）
2. **回归目标**：terminal x₀ 监督不稳定，需要过于保守的同步；step-wise x_{t-} 更稳定（Figure 2b）
3. **损失函数**：单分支 Positive/Negative 部分有效；wMSE 退化为单分支拟合；ranking loss push-pull 最优（Figure 3a）
4. **Value estimation**：sparse binary reward 与 dense advantage 竞争力相当，且训练更稳定（Figure 3b）
5. **超参敏感性**（Figure 4）：σ ≈ 0.2, β ∈ [1.0, 2.0], 动态 α decay（0.1→0.995）最优
6. **Step selection**：随机采样 solver step 优于固定 step（Figure 5）

### 硬件
- 主实验：8×H100 (80GB)
- 消融实验：8×RTX 4090 (48GB)


## Limitations

1. **长时任务 temporal credit assignment 不足**：PPO 在 Long 任务上仍有优势（π₀: 90.2% vs 86.7%），因为 critic 能做更精细的时间信用分配
2. **未在真实机器人上验证**：仅在仿真环境 LIBERO 和 ManiSkill 上测试
3. **稀疏奖励依赖**：虽然理论上支持密集奖励，但主要实验用 binary reward
4. **超参敏感性**：噪声水平 σ、trust region β、EMA decay α 需要调节
5. **与 SOTA 有差距**：在 LIBERO Long 等任务上 PPO 仍然更强（90.2% vs 86.7%）


## Key Takeaways

1. **Critic-free 避免多模态过拟合**：在视觉多样的 OOD 场景下，value-based 方法（PPO）的 critic 容易过拟合于视觉特征和语言 prompt；π-StepNFT 直接用环境 ground-truth 二元结果，泛化更好。这对 DLO 操控的多样化视觉场景有启发。
2. **逐步监督优于 terminal 监督**：当策略通过 SDE 探索更宽空间时，terminal x₀ 监督方差太大，step-wise x_{t-} 监督提供精确局部梯度。这一原则可能适用于其他需要 stochastic exploration 的操控场景。
3. **Push-pull 动态信号更强**：ranking loss 的双向信号比 wMSE 的单分支拟合产生更强梯度，加速收敛。
4. **计算效率高**：单次 forward pass 即可更新，无需 critic network 和 likelihood 计算，降低硬件门槛。
5. **对 DLO 的间接相关性**：本文未涉及 DLO 任务，但其方法可直接应用于任何 flow-based VLA 策略的在线 RL 精调，包括 DLO 操控场景。OOD 泛化优势对 DLO 真实部署有参考价值。

## 相关概念

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[flow-matching]]
- [[deformable-linear-object]]

## 相关研究者

- [[wang-siting|Wang, Siting]]
- [[zhu-zheng|Zhu, Zheng]]
