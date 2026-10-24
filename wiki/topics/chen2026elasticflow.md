---
title: "ElasticFlow: One-step physics-consistent policy with elastic time horizons for language-guided manipulation"
tags: [manipulation, imitation, diffusion, flow-matching, robot-learning]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编码控制粒度以克服频谱偏差，在 LIBERO/CALVIN/RoboTwin 上达到 SOTA。"
authors: "Chen, Kewei; Long, Yayu; Li, Shuai; Shang, Mingsheng"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "9TPUXCAM"
---
## 摘要

Diffusion（扩散） policies have demonstrated exceptional performance in embodied AI. However, their iterative denoising process results in high latency, and existing acceleration methods often sacrifice physical consistency. To address this, we propose ElasticFlow, a distillation-free, physics-consistent one-step policy framework. We reconstruct the Mean Field Theory by directly modeling the average velocity field, enabling a direct single-step mapping from noise to action. Addressing the Temporal Heterogeneity of robotic tasks, we introduce the Elastic Time Horizons mechanism. This mechanism effectively overcomes Spectral Bias by explicitly encoding control granularity, achieving efficient alignment between semantic instructions and physical execution horizons. Experiments on benchmarks such as LIBERO, CALVIN, and RoboTwin demonstrate that ElasticFlow achieves efficient 1-NFE inference (approximately 71Hz). Furthermore, it outperforms state-of-the-art（现有最优方法） methods, including OpenVLA and $π_0$, on long-horizon（长时序） tasks, highlighting its potential for efficient, robust, and semantically aligned control.

## 中文简述

提出基于扩散模型的操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、Flow Matching、机器人学习

## 关键贡献

1. **ElasticFlow 策略框架**：将机器人动作生成建模为平均速度场学习问题，基于 MeanFlow Identity 实现无需蒸馏的单步策略（1-NFE），无需迭代求解即可保证轨迹平滑。
2. **Elastic Time Abstraction 机制**：提出双参数时间编码策略 (r, t)，赋予模型对控制时域的显式感知能力，单一网络可自适应处理从毫秒级瞬态控制到秒级宏观规划的不同粒度需求。
3. **SOTA 性能和效率**：在 LIBERO（98.5% 平均成功率）、CALVIN（4.37 平均链长）、RoboTwin（70.1%）基准上达到 SOTA，推理频率约 71Hz（14ms/步，RTX 4090），比 Diffusion Policy 快 5x，比 OpenVLA 快 14x。
## 结构化提取

- Problem: 扩散策略推理延迟高（<20Hz），现有加速方法牺牲物理一致性，自回归 VLA 量化误差大且频率受限
- Method: ElasticFlow — 基于平均速度场和 MeanFlow Identity 的单步生成策略（1-NFE），配合 Elastic Time Horizons 双参数时间编码 (r, t) 克服频谱偏差
- Tasks: 语言引导机器人操控——空间/物体/目标/长时序泛化，包含桌面操控和厨房任务
- Sensors: 第三人称 RGB 相机、腕部 RGB 相机（RealSense D435i）
- Robot Setup: 仿真（LIBERO/CALVIN/RoboTwin2.0/RoboCasa）+ 真机（UFACTORY xArm6 + Robotiq 2F-85 + 2× RealSense D435i），训练用 4× A100，推理用 1× RTX 4090
- Metrics: 成功率（SR%）、平均链长（CALVIN Chain Length）、Trajectory Jerk（末端执行器位置三阶导数均方值 ↓）、推理延迟（ms/Hz）
- Limitations: 仅在百万级数据验证 Scaling Laws、未集成闭环 MPC/在线 RL、语言引导深度有限（仅 cross-attention）、材料属性泛化不足
- Evidence Notes: 全文可获取，含完整数学推导（Appendix C）、4 个基准定量实验（LIBERO/CALVIN/RoboTwin/RoboCasa）、7 个真机任务 280 次定量试验、3 组消融实验（Time Horizon / Training Objective / CFG）、CFG 敏感性分析、RoboTwin 时域分组分析、LIBERO-Long 逐任务分解
## 本地引用关系

- [[chi2024diffusion]]
- [[kim2024openvla]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high
- Confidence: high
- Summary: 基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编码控制粒度以克服频谱偏差，在 LIBERO/CALVIN/RoboTwin 上达到 SOTA。


## Problem

扩散策略在具身 AI 中表现优异，但其迭代去噪过程导致推理延迟高（通常 <20Hz）。现有加速方法（Consistency Models、Progressive Distillation）需要复杂的蒸馏管线且往往牺牲物理一致性（轨迹平滑度）。自回归 VLA 模型依赖离散 token 预测，引入量化误差且频率受限。核心矛盾：如何在不牺牲物理一致性的前提下实现高频实时策略推理？


## Method

### 核心思想：从瞬时速度到平均速度场
传统 Flow Matching 通过回归瞬时速度场 v(z_τ, τ) 驱动 ODE，需要多次数值积分（多 NFE）。ElasticFlow 引入**平均速度场** u(z_t, r, t)，定义为流在弹性时间区间 [r, t] 上的归一化位移：

u(z_t, r, t) = 1/(t-r) ∫_r^t v(z_τ, τ) dτ

若能精确预测 r=0 到 t=1 的平均速度，则可通过单步映射 x̂ = z₁ - u(z₁, 0, 1) 直接恢复目标动作。

### ElasticFlow Identity
基于微积分基本定理推导的内在微分约束：

u(z_t, r, t) = v(z_t, t) - (t-r) · d/dt u(z_t, r, t)

第二项 (t-r) · d/dt u 作为**流形曲率修正项**，显式建模轨迹弯曲，抑制高频抖动。这使得策略网络被迫学习动作轨迹的全局几何特征而非局部梯度。

### 训练目标
采用 Classifier-Free Guidance 策略，训练时以概率 p_drop 将条件 ℓ 置为 null。损失函数利用 Forward-mode AD 高效计算 Jacobian-Vector Product（JVP），避免计算昂贵的 Hessian 矩阵：

L(θ) = E_{t,r,x₁,ε,c} ||u_θ(z_t, r, t, o, c) - sg(T_target)||²

T_target = v(z_t, t) - (t-r)(v(z_t, t)·∇_z u_θ + ∂_t u_θ)

### Elastic Time Abstraction
- **双参数时间编码**：Emb(r,t) = MLP([FF(t), FF(t-r)])，其中 FF 为 Gaussian Fourier Feature Encoding
- Δt = t-r 赋予模型"控制时域"感知：Δt 小 → 高频瞬态调整；Δt 大 → 长程规划
- 推理时连续流按控制频率离散化为 N 步，有效物理步长 δt = T/N
- 这一机制如同"频谱变焦镜头"（Spectral Zoom Lens），自适应调节控制粒度

### 网络架构
- 视觉：SigLIP 编码器提取视觉特征
- 语言：T5 文本编码器
- 主干：DiT（Diffusion Transformer，150M 参数），通过 Cross-Attention 注入视觉和语言条件
- 时间编码通过 AdaLN 调制注入 DiT 主干

### 推理（1-NFE）
给定高斯噪声 z₁ ~ N(0,I)，设 r=0, t=1，单次前向传播：

x̂ = z₁ - (u_θ(·, ∅) + w · (u_θ(·, ℓ) - u_θ(·, ∅)))

其中 w 为 CFG Guidance Scale（默认 2.0），在 [1.5, 2.5] 区间内性能稳健。


## Experiments

### LIBERO 基准（Table 1）
| 套件 | ElasticFlow | HiF-VLA | π₀ | Octo |
|------|------------|---------|-----|------|
| Spatial | 98.4 | **98.8** | 96.8 | 78.9 |
| Object | **99.3** | 99.4 | 98.8 | 85.7 |
| Goal | **98.7** | 97.4 | 95.8 | 84.6 |
| Long | **97.6** | 96.4 | 85.2 | 51.1 |
| **Average** | **98.5** | 98.0 | 94.2 | 75.1 |

LIBERO-Long 逐任务分析（Table 10）：10 个长时序任务平均 95.6%（第三人称）/97.6%（多视角），其中"Put both pots on stove"相对 MemoryVLA 提升 +19.0%，验证 Elastic Time Horizon 在多阶段任务中的结构一致性优势。

### CALVIN ABC-D（Table 2）
- 多视角：平均链长 **4.37**（第4/5指令成功率 83.6%/72.7%）
- 单视角：平均链长 **4.15**
- 在第4和第5指令上维持高成功率，说明 MeanFlow Identity 强制的全局一致性使策略能在不同语义目标间平滑切换。

### RoboTwin2.0 时域分析（Table 9）
- Short (100-130步): 65.4% (vs SimpleVLA 64.9%, π₀ 45.5%)
- Medium (150-230步): **73.7%** (vs SimpleVLA 72.5%, π₀ 58.8%)
- Long & Extra Long (280-650步): **71.1%** (vs SimpleVLA 69.0%, π₀ 43.3%)
- **Overall: 70.1%** (vs SimpleVLA 68.8%, π₀ 49.2%)
- 显式编码 Δt 使网络在长时域上衰减最小，而 π₀ 和 RDT 随时域增长显著退化。

### 真机实验（xArm6, Table 8）
- 7 个任务，每个 seen/unseen 各 20 次试验（共 280 次）
- Seen 场景平均 91.4%，Unseen 场景平均 76.4%
- Cable Routing：85% seen, 70% unseen（换更硬线材时下降）
- Dynamic Interception：95% seen, 85% unseen（拦截速度 ≤10cm/s 滚动圆柱体）
- Long-Horizon Kitchen：100% seen, 75% unseen（"打开微波炉→放入碗→关门→按开关"）

### 消融实验（RoboTwin Long Horizon）
1. **Elastic Time Horizon 必要性**（Table 3）：
   - w/o Horizon Input：长时序 52.7%（下降 18.4%）
   - Fixed Horizon Δt=10：长时序 58.2%（无法处理长程）
   - Fixed Horizon Δt=50：短时序 55.4%（响应迟钝）
   - Mismatch Test：强制小 Δt 在长任务上仅 45.3%（近视），强制大 Δt 在短任务上仅 55.7%（迟缓）

2. **MeanFlow Identity vs 标准 CFM**（Table 4）：
   - 标准 CFM 1-NFE：12.4% SR，Jerk 8.5×10⁻²
   - 标准 CFM 10-NFE：68.5% SR，Jerk 3.2×10⁻³
   - **ElasticFlow 1-NFE：71.1% SR，Jerk 1.1×10⁻³**
   - 单步 ElasticFlow 的轨迹平滑度优于 10 步 CFM，证明曲率修正项的有效性。

3. **CFG 敏感性**（Figure 6）：
   - w=1.0：32.5%（指令跟随弱）
   - w=2.0：71.1%（峰值）
   - w>3.0：急剧下降（过度引导导致高频抖动）

### 推理延迟（Table 5，RTX 4090）
| 方法 | NFE | 延迟 | 频率 |
|------|-----|------|------|
| OpenVLA (7B) | Auto-reg | 200ms | ~5Hz |
| Diffusion Policy (300M) | 16 (DDIM) | 120ms | ~8Hz |
| π₀ (300M) | 10 (Euler) | 85ms | ~12Hz |
| Consistency Policy (300M) | 2 | 28ms | ~35Hz |
| **ElasticFlow (150M)** | **1** | **14ms** | **~71Hz** |


## Limitations

1. **规模限制**：实验主要在百万级数据上进行，未在十亿级跨具身数据集（如 Open X-Embodiment）上验证 Scaling Laws。
2. **闭环控制**：虽推理频率高（71Hz），但未集成 MPC 或在线 RL 进行闭环纠正，仅以生成轨迹作为开环执行。
3. **语义对齐深度**：当前语言引导仅通过 cross-attention 注入，未探索与 MLLM 的深度融合，长复杂指令的语义解析能力受限。
4. **材料泛化**：Cable Routing 任务中换用更硬线材时性能下降 15%，说明模型对材料属性的泛化不足。


## Key Takeaways

1. **平均速度场是替代多步 ODE 的有效途径**：MeanFlow Identity 中的曲率修正项隐式保证了轨迹平滑，单步 ElasticFlow（Jerk 1.1×10⁻³）的物理一致性优于 10 步 CFM（Jerk 3.2×10⁻³）。
2. **弹性时域对 DLO 操控有直接启示**：DLO 任务天然需要不同控制粒度（精细接触 vs 粗粒度搬运），Δt 编码机制可直接迁移；ElasticFlow 作为单一生成头即可处理这种多粒度需求。
3. **Cable Routing 实验证明变形体操控潜力**：85% seen / 70% unseen 的线缆布线结果显示了对非刚性物体的初步操控能力，但材料变化时性能下降暗示需要材料感知条件输入。
4. **模型规模小（150M）但效果强**：比 OpenVLA（7B）参数少 ~50 倍但推理快 14 倍、LIBERO-Long 成功率高 43.6 个百分点，说明生成头设计比参数规模更关键。
5. **频谱偏差问题是操控策略的共性问题**：通过 Fourier Feature 编码 Δt 来解决，这一技巧可推广到其他需要多粒度控制的场景。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[robot-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[chen-kewei|Chen, Kewei]]
- [[long-yayu|Long, Yayu]]
- [[li-shuai|Li, Shuai]]
- [[shang-mingsheng|Shang, Mingsheng]]
