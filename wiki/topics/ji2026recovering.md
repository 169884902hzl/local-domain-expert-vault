---
title: "Recovering Hidden Reward in Diffusion-Based Policies"
tags: [manipulation, imitation, RL, diffusion, neural-potential-function]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆强化学习的统一。"
authors: "Ji, Yanbiao; Li, Qiuchang; Hu, Yuting; Wu, Shaokai; Xie, Wenyuan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GCITIGK9"
---
## 摘要

This paper introduces EnergyFlow, a framework that unifies generative action modeling with inverse reinforcement learning（强化学习） by parameterizing a scalar energy function whose gradient is the denoising field. We establish that under maximum-entropy optimality, the score function learned via denoising score matching recovers the gradient of the expert's soft Q-function, enabling reward（奖励） extraction without adversarial training. Formally, we prove that constraining the learned field to be conservative reduces hypothesis complexity and tightens out-of-distribution generalization bounds. We further characterize the identifiability of recovered rewards and bound how score estimation errors propagate to action preferences. Empirically, EnergyFlow achieves state-of-the-art（现有最优方法） imitation performance on various manipulation（操控） tasks while providing an effective reward（奖励） signal for downstream reinforcement learning（强化学习） that outperforms both adversarial IRL methods and likelihood-based alternatives. These results show that the structural constraints required for valid reward（奖励） extraction simultaneously serve as beneficial inductive biases for policy generalization. The code is available at https://github.com/sotaagi/EnergyFlow.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、神经势函数

## 关键贡献

1. **EnergyFlow框架**：参数化标量能量函数 E_φ(o,a,t)，通过自动微分获得去噪向量场 ∇_a E_φ，构造性地保证保守场约束（integrability），同时推导完整的概率流ODE连接训练和采样。
2. **理论证明：保守约束降低假设复杂度**：证明保守向量场的经验Rademacher复杂度为 O(ΛL/√n)，而非保守场为 O(ΛB√d/√n)，在高维动作空间中保守约束提供更紧的泛化界。
3. **鲁棒性分析**：刻画了恢复奖励的可辨识性（within-state精确，cross-state模糊），并证明score估计误差传播到动作偏好的误差上界为 η·‖a-a'‖₂。
4. **实证验证**：在10个操控任务上达到SOTA模仿性能（RoboMimic 93.8%, Meta-World 92.5%），同时提供有效的下游RL奖励信号，并在OOD扰动下展现更优鲁棒性。
## 结构化提取

- **Problem**: 扩散策略仅模仿轨迹不建模奖励意图，限制OOD泛化和下游策略优化
- **Method**: 能量参数化（标量E_φ → 自动微分梯度作为score）+ 去噪score matching训练 + centered shaping奖励提取
- **Tasks**: RoboMimic（Lift/Can/Square/Transport/ToolHang）、Meta-World（Button/Drawer/Assembly/Bin/Hammer）、真实机器人（Bottle/Drawer）
- **Sensors**: 低维状态（关节角、速度、物体位姿）；真实机器人使用RGB摄像头（226×226，ResNet-18编码器）
- **Robot Setup**: 仿真：单臂/双臂夹持器；真实：AGIBOT G1（7-DoF臂+平行爪夹持器），10Hz控制
- **Metrics**: 成功率（%），OOD扰动下的鲁棒性，SAC训练曲线，推理延迟（ms）
- **Limitations**: 跨状态奖励模糊性；主要在低维状态评估；未测DLO/长时域任务；最大熵假设限制；训练需double backprop
- **Evidence Notes**:

  - [fulltext] Table 1: RoboMimic 5任务成功率，EnergyFlow avg 93.8% > DP 91.2%
  - [fulltext] Table 2: Meta-World 5任务成功率，EnergyFlow avg 92.5% > DP 90.7%
  - [fulltext] 真实机器人：Bottle和Drawer均100%成功率，20次rollout × 3种初始位置
  - [fulltext] Figure 4: Centered Energy+Sparse奖励训练SAC效果接近oracle dense reward
  - [fulltext] Figure 5: OOD扰动下EnergyFlow退化最平缓
  - [fulltext] Table 3: γ∈[10⁻⁴,10⁻²]稳定，γ=10⁻³最优
  - [fulltext] Table 4: 推理延迟~8ms（A100, 10Hz），与Flow Policy相当
  - [fulltext] Theorem 3.3: Score-Reward等价性证明
  - [fulltext] Theorem 3.6: 保守场Rademacher复杂度 O(ΛL/√n) vs 非保守 O(ΛB√d/√n)
  - [fulltext] Theorem 3.11: 偏好误差上界 η·‖a-a'‖₂
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖论文主体（理论、方法、实验、附录）
- Confidence: high
- Summary: 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆强化学习的统一。


## Problem

扩散策略（Diffusion Policy）通过迭代去噪生成动作，能建模多模态专家行为分布，但本质上是行为克隆（BC）目标——仅模仿轨迹而不建模"为什么"某个动作是好的（底层意图/奖励）。当测试场景偏离演示分布时，仅匹配动作似然无法提供可靠的动作选择信号。现有的逆强化学习（IRL）方法虽能从演示中学习奖励，但计算开销大且训练不稳定。


## Method

### 核心思想

标准扩散策略学习噪声向量场 ε_θ(s,a) 用于去噪，但不具备显式能量表示。EnergyFlow改为参数化标量能量 E_φ(a,s,t)，通过自动微分获得score：S_φ = -∇_a E_φ。这构造性地保证 ∇_a × S_φ ≡ 0（保守场），使学习到的偏好具有传递性。

### 理论基础

- **Theorem 3.3 (Score-Reward等价性)**：在最大熵最优性假设下，最优策略的score函数与soft Q函数梯度成正比：∇_a Q*(s,a) = α·S*(a,s)。积分后 E_φ(a,s) = -Q*(s,a)/α + c(s)。
- **Theorem 3.6 (复杂度降低)**：保守场的Rademacher复杂度为 O(ΛL/√n)，远低于非保守场的 O(ΛB√d/√n)。
- **Lemma 3.8 (OOD泛化)**：保守场在分布偏移下的目标域风险上界更紧，随维度增长不发散。
- **Theorem 3.11 (偏好Lipschitz连续性)**：|ΔE_φ(a,a') - ΔE*(a,a')| ≤ η·‖a-a'‖₂，score误差线性传播。

### 网络架构

- **Backbone**：1D Conditional U-Net（与Diffusion Policy相同的backbone），但关键修改：
  - **标量输出头**：Global Average Pooling + MLP(256→128→1) 输出单个标量能量值
  - **Mish激活**：替代ReLU，保证C²可微（训练需要计算能量的二阶导数）
  - **谱归一化**：线性层施加谱归一化以鼓励Lipschitz连续性
- **条件编码**：状态通过2层MLP(128, Mish)编码，时间步通过正弦位置嵌入编码，通过FiLM注入每个卷积块

### 训练

去噪score matching目标：L(φ) = E_{t,a₀,ε}[σ²(t)‖-∇_{a_t} E_φ(a_t,s,t) + ε/σ(t)‖²]
噪声调度：σ(t) = σ_min^(1-t/T) · σ_max^(t/T)，σ_min=0.01, σ_max=10.0, T=1.0

### 奖励提取（Centered Shaping）

r̃_φ(a,s) = -[E_φ(a,s,γ) - E_{a'~N(0,I)}[E_φ(a',s,γ)]]
通过减去参考分布下的期望能量消除状态依赖偏移c(s)，M=16个Monte Carlo样本估计基线。

### 推理

ODE积分（Euler法，K=20步），从高斯噪声采样开始，沿概率流ODE去噪到最终动作。


## Experiments

### 数据集/任务

- **RoboMimic**（5任务）：Lift, Can, Square, Transport, ToolHang
- **Meta-World**（5任务）：ButtonPress, DrawerOpen, Assembly, BinPicking, Hammer
- **真实机器人**：AGIBOT G1（7-DoF臂+平行爪夹持器），RGB摄像头（226×226），Bottle和Drawer任务

### 主要结果

**RoboMimic成功率（%）**：

| Method | Lift | Can | Square | Transport | ToolHang | Avg |
|--------|------|-----|--------|-----------|----------|-----|
| LSTM-GMM | 97.8 | 71.4 | 64.3 | 65.6 | 46.0 | 69.0 |
| Diffusion Policy | 100.0 | 99.2 | 93.5 | 85.9 | 77.2 | 91.2 |
| Flow Policy | 99.6 | 98.4 | 91.8 | 83.6 | 74.8 | 89.6 |
| EBT-Policy | 96.2 | 88.6 | 78.4 | 72.4 | 58.6 | 78.8 |
| IQ-Learn | 95.2 | 82.6 | 68.8 | 58.4 | 44.2 | 69.8 |
| **Ours** | **100.0** | **100.0** | **95.3** | **89.4** | **84.2** | **93.8** |

**Meta-World成功率（%）**：

| Method | Button | Drawer | Assembly | Bin | Hammer | Avg |
|--------|--------|--------|----------|-----|--------|-----|
| Diffusion Policy | 100.0 | 93.6 | 76.4 | 89.6 | 94.0 | 90.7 |
| Flow Policy | 100.0 | 92.8 | 74.8 | 87.6 | 92.2 | 89.5 |
| **Ours** | **100.0** | **94.2** | **82.6** | **90.9** | **94.6** | **92.5** |

**真实机器人**：Bottle和Drawer任务均100%成功率（3种初始位置变化，每种20次rollout）。

### 奖励质量（RQ3）

- 使用EnergyFlow的centered shaping奖励训练SAC（200K步）
- Centered Energy + Sparse 表现最佳，接近oracle dense reward
- Raw energy奖励虽密集但不可靠地推动agent走向目标
- Sparse奖励训练早期缓慢

### OOD泛化（RQ4）

- 在初始位置扰动（Level 0/S/M/L）下，EnergyFlow退化最平缓
- 扩散策略和Flow Policy在中大扰动下显著退化
- 确认保守约束（curl-free）作为几何正则化器的有效性

### 消融/敏感性

- 奖励提取时间参数 γ ∈ [10⁻⁴, 10⁻²] 表现稳定，γ=10⁻³最优（95.3%），γ≥0.1退化
- 推理延迟：~8ms（10Hz控制，A100），与Flow Policy相当


## Limitations

1. **跨状态奖励模糊性**：恢复的能量函数包含未知状态偏移c(s)，在序贯MDP设置中可能不满足potential-based reward shaping（PBRS）条件，可能改变最优策略。
2. **仿真实验局限**：主要在低维状态空间的仿真平台上评估，视觉输入仅在真实机器人实验中使用（10个demo，ResNet-18 backbone）。
3. **未测试的场景**：未在可变形物体（DLO）操控、长时域任务或高维视觉-语言策略上验证。
4. **假设限制**：最大熵最优性假设（Assumption 3.1）可能不适用于所有真实专家行为。
5. **训练开销**：需要通过自动微分计算能量的梯度（create_graph=True），训练时计算量高于标准扩散策略。


## Key Takeaways

1. **能量参数化作为归纳偏置**：将扩散策略的向量场输出替换为标量能量+自动微分梯度，不仅不损失性能，反而通过保守约束提升OOD泛化——这是一个重要的设计启示。
2. **模仿学习与IRL的统一**：不需要对抗训练的min-max优化，score matching本身就隐含了奖励信号。这显著简化了从演示中提取奖励的流程。
3. **对DLO操控的潜在价值**：EnergyFlow在contact-rich操控任务上表现出色，其能量函数可作为RL奖励信号用于DLO等需要密集反馈的复杂操控任务。但论文未涉及连续形变状态空间的挑战。
4. **Sim-to-Real可行性**：在AGIBOT G1上用少量demo（10个）即实现100%成功率，且策略运行在10Hz，具有实际部署可行性。
5. **保守场约束的普遍意义**：curl-free约束的思想可推广到其他需要从向量场恢复标量势函数的场景（如力场建模、流场估计）。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[dynamical-systems]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[ji|Ji, Yanbiao]]
