---
title: "ACG: Action Coherence Guidance for Flow-based Vision-Language-Action models"
tags: [manipulation, imitation, VLM, diffusion]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造\"不一致向量场\"，再沿反方向引导 flow matching VLA 策略生成时序连贯的动作序列，在 RoboCasa/DexMG/SO-101 上平均提升 9.6% 成功率。"
authors: "Park, Minho; Kim, Kinam; Hyung, Junha; Jang, Hyojin; Jin, Hoiyeong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "2QBPMATZ"
---
## 摘要

Diffusion（扩散） and flow matching models have emerged as powerful robot policies, enabling Vision-Language-Action (VLA) models to generalize across diverse scenes and instructions. Yet, when trained via imitation learning（模仿学习）, their high generative capacity makes them sensitive to noise in human demonstrations: jerks, pauses, and jitter which reduce action coherence. Reduced action coherence causes instability and trajectory drift during deployment, failures that are catastrophic in fine-grained manipulation（操控） where precision is crucial. In this paper, we present Action Coherence Guidance (ACG) for VLA models, a training-free test-time guidance algorithm that improves action coherence and thereby yields performance gains. Evaluated on RoboCasa, DexMimicGen, and real-world SO-101 tasks, ACG consistently improves action coherence and boosts success rates across diverse manipulation（操控） tasks. Code and project page are available at https://github.com/DAVIAN-Robotics/ACG and https://DAVIAN-Robotics.github.io/ACG , respectively.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型

## 关键贡献

1. **ACG 算法**：首个将 perturbation guidance 引入机器人控制的方法，无需训练，仅在推理时通过构造"不一致向量场"并沿反方向引导，提升 flow-based VLA 模型的动作连贯性
2. **Incoherent Attention 构造**：将 self-attention 的 attention map 替换为单位矩阵（identity），打破 token 间时序通信，生成不连贯动作序列作为"反面教材"
3. **跨模型泛化**：在 GR00T-N1、π0、SmolVLA 三种 DiT 架构 flow-based VLA 上均有效，即插即用
4. **实验验证**：在仿真（RoboCasa、DexMimicGen）和真实世界（SO-101）上一致提升成功率，精细任务提升尤为显著（按钮按压 +23.1%，插入 +11.8%，草莓抓取 +30.8%）
## 结构化提取

- Problem: Flow matching VLA 模型记忆人类示教噪声，生成时序不连贯的动作序列，导致精细操控失败
- Method: Test-time perturbation guidance；将 self-attention 图替换为单位矩阵构造不一致向量场，沿反方向引导采样
- Tasks: 多任务桌面操控（抓取、放置、按钮按压、插入、开合）+ 双臂灵巧操控 + 真实世界抓取放置
- Sensors: 多视角 RGB 图像 + 关节状态
- Robot Setup: GR00T-N1 (主要)、π0、SmolVLA 作为 VLA backbone；仿真在 RoboCasa 和 DexMimicGen；真实世界用 SO-101 机械臂
- Metrics: 成功率（%）、ATV (rad/s)、JerkRMS (rad/s³)
- Limitations: 1.5× 推理开销；仅处理块内连贯性；深度网络适用性未验证；超参需调整
- Evidence Notes: 全文覆盖完整，所有定量结果直接引自 Table I/II/III 和 Figure 5/6/7；无缺失证据
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 版本，含全部正文、公式、表格、算法和参考文献）
- Evidence Coverage: 高（方法、实验、消融、跨模型泛化均有完整数据）
- Confidence: high
- Summary: 提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造"不一致向量场"，再沿反方向引导 flow matching VLA 策略生成时序连贯的动作序列，在 RoboCasa/DexMG/SO-101 上平均提升 9.6% 成功率。


## Problem

Flow matching / diffusion VLA 模型通过模仿学习训练时，其强大的生成能力会记忆人类示教中的噪声（顿挫、停顿、抖动），导致生成的动作序列缺乏时序连贯性（action coherence）。这种不一致性在部署时引发两类故障：(1) 关键时刻（如抓取）动作不稳定；(2) 微小噪声累积导致轨迹漂移。精细操控任务对此尤为敏感。


## Method

### 核心思想
受图像生成中 perturbation guidance（PAG/SAG）启发，ACG 不修改训练过程，而是在推理时构造一个"故意变差"的模型变体，利用其输出作为引导方向的反面。

### 数学框架
1. **引导分布**：π^ACG(λ)(A_t|o_t,l_t) ∝ π_θ(A_t|o_t,l_t) · [π_θ(A_t|o_t,l_t) / π_θ^IC(A_t|o_t,l_t)]^λ
2. **引导向量场**：v_θ^ACG(λ) = (1+λ)·v_θ - λ·v_θ^IC
   - v_θ：原始条件向量场
   - v_θ^IC：不一致向量场（通过 identity attention 构造）
   - λ：引导强度（默认 3.0）
3. **Forward Euler 积分**：A_t^{τ+δ} = A_t^τ + δ·v_θ^ACG，共 16 步去噪

### Incoherent Attention 构造
- 标准自注意力：Attn(Q,K,V) = softmax(QK^T/√d) · V
- 不一致自注意力：Attn_IC(Q,K,V) = I · V = V（每个 action token 只关注自身）
- 效果：打破 token 间的时序协调，生成时序不一致的动作序列
- 默认修改第 4-6 层（共 8 层），中间和靠后层效果最好

### 计算开销
- 需要额外的 forward pass 计算 v_θ^IC
- 通过缓存前几层输出并仅扰动后几层 attention，开销降至约 1.5×


## Experiments

### 基准与设置
| 基准 | 类型 | 任务数 | 训练数据 | 评估方式 |
|------|------|--------|---------|---------|
| RoboCasa | 仿真 | 24（7 类技能） | 100 demos/task × multi-task | 3×24 trials |
| DexMimicGen | 仿真 | 多种双臂操控 | 100 demos/task × cross-embodiment | 3×24 trials |
| SO-101 Three Strawberries | 真实 | 抓取放置 | 50 demos | 3×10 trials |
| SO-101 Tic-Tac-Toe | 真实 | 抓取放置 | 40 demos | 3×10 trials |

### 主要结果（Table I，成功率 %）
| 方法 | RoboCasa | DexMG | Three Strawberries | Tic-Tac-Toe |
|------|----------|-------|-------------------|-------------|
| Vanilla GR00T-N1 | 54.2 | 67.4 | 56.7 | 70.0 |
| Ensemble×2 | 55.3 | 67.1 | 63.3 | 70.0 |
| Ensemble×5 | 55.4 | 68.3 | 70.0 | 68.3 |
| Smoothing (action) | 54.8 | 67.9 | 60.0 | 70.0 |
| Smoothing (feature) | 55.7 | 68.2 | 60.0 | 66.7 |
| CFG | 53.2 | 66.4 | 60.0 | 65.0 |
| WNG | 56.6 | 69.3 | 78.3 | 68.3 |
| **ACG (Ours)** | **60.9** | **70.8** | **87.5** | **75.0** |

**关键发现**：
- ACG 相比 Vanilla 平均提升 9.6%
- 精细任务提升最大：按钮按压 +23.1%，插入 +11.8%，草莓抓取 +30.8%
- Smoothing 方法提升有限（直接平滑会模糊细节）
- CFG 在操控任务上反而下降（强化语言条件 ≠ 提升动作连贯性）
- WNG 是次佳方法，但大噪声会侵蚀预训练知识

### 动作连贯性分析（Table II）
- **ATV（Action Total Variation）**：ACG 显著降低（更平滑）
- **JerkRMS**：ACG 最低（加速度变化最小）
- Ensemble 方法改善连贯性但损失精度（犹豫不决）
- v_θ^IC 的连贯性比 Vanilla 更差，验证了 ACG 的引导方向正确性

### 消融实验
1. **引导强度 λ**：增大 λ 提升性能，但过大会偏离预训练分布；默认 3.0
2. **扰动层数**：2-6 层均有效，对数量不敏感
3. **扰动层位置**：中间和靠后层效果最好，早期层偶尔有害
4. **与 Self-GAD 对比**：ACG（块内连贯性）> Self-GAD（块间连贯性）；两者互补可叠加
5. **跨模型泛化（Table III）**：在 π0 和 SmolVLA 上也有显著提升


## Limitations

1. **计算开销**：需要约 1.5× 推理时间（额外 forward pass）
2. **仅处理块内连贯性**：不解决 action chunk 之间的连贯性问题（需与 Self-GAD 等互补）
3. **深度网络适用性未知**：仅验证了 8 层 DiT，更深网络的扰动策略有待研究
4. **仅适用于 flow matching / diffusion 策略**：依赖 self-attention 结构，不适用于自回归策略
5. **默认超参在特定模型上选择**：不同模型/任务可能需要重新调参


## Key Takeaways

1. **Perturbation guidance 是即插即用的性能提升利器**：无需重新训练，直接应用于已有 flow-based VLA 模型，对资源受限的实验室特别有价值
2. **动作连贯性对精细操控至关重要**：DLO 操控涉及连续形变控制，对动作抖动高度敏感，ACG 的思路可直接迁移
3. **Identity attention 是优雅的"反例构造"**：比注入随机噪声（WNG）更精准，不会侵蚀预训练的任务知识
4. **块内连贯 > 块间连贯**：对于精细操控任务，单次 action chunk 内的连贯性比跨 chunk 一致性更关键
5. **双臂 DLO 操控的潜在应用**：DexMimicGen 上的实验已证明 ACG 对双臂操控有效，DLO 任务的精细控制需求与 ACG 优势高度匹配

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[park-minho|Park, Minho]]
