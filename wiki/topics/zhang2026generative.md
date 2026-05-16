---
title: "Generative control as optimization: Time unconditional flow matching for adaptive and robust robotic control"
tags: [imitation, VLM, diffusion]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head"
authors: "Zhang, Zunzhe; Huang, Runhan; Liu, Yicheng; Zhu, Shaoting; Mou, Linzhan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CNUPDFGC"
---
## 摘要

Diffusion（扩散） models and flow matching have become a cornerstone of robotic imitation learning（模仿学习）, yet they suffer from a structural inefficiency where inference is often bound to a fixed integration schedule that is agnostic to state complexity. This paradigm forces the policy to expend the same computational budget on trivial motions as it does on complex tasks. We introduce Generative Control as Optimization (GeCO), a time-unconditional framework that transforms action synthesis from trajectory integration into iterative optimization. GeCO learns a stationary velocity field in the action-sequence space where expert behaviors form stable attractors. Consequently, test-time inference becomes an adaptive process that allocates computation based on convergence--exiting early for simple states while refining longer for difficult ones. Furthermore, this stationary geometry yields an intrinsic, training-free safety signal, as the field norm at the optimized action serves as a robust out-of-distribution (OOD) detector, remaining low for in-distribution states while significantly increasing for anomalies. We validate GeCO on standard simulation benchmarks and demonstrate seamless scaling to pi0-series Vision-Language-Action (VLA) models. As a plug-and-play replacement for standard flow-matching heads, GeCO improves success rates and efficiency with an optimization-native mechanism for safe deployment. Video and code can be found at https://hrh6666.github.io/GeCO/

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、扩散模型

## 关键贡献

1. **Time-unconditional 速度场**：学习驻定速度场 fθ(x, st)，通过 velocity rescaling mechanism（c(γ)衰减调度）使专家动作成为稳定吸引子
2. **自适应推理**：基于收敛性的迭代优化替代固定步数积分，简单状态早停，复杂状态深度优化
3. **内在 OOD 检测**：驻定场的梯度范数作为零样本异常分数，无需额外训练
4. **即插即用 VLA 集成**：直接替换 π0 系列模型中的 time-conditioned flow head，仅固定时间输入 t=0 微调
## 结构化提取

- Problem: 基于时间条件化 flow matching 的模仿学习方法推理效率低且缺乏 OOD 检测机制
- Method: Time-unconditional 驻定速度场 + velocity rescaling + 基于收敛的迭代优化推理
- Tasks: 语言条件桌面操作（LIBERO）、双臂操作（RoboTwin 2.0）、长视野操作（VLABench）、高精度真实世界操作（Nut Assembly, Tube Arrangement）
- Sensors: 多视角 RGB 图像、本体感知（关节状态）、语言指令
- Robot Setup: 仿真：单臂 Franka（LIBERO）、双臂（RoboTwin）；真实：Galaxea R1 Lite 移动操作器
- Metrics: 任务成功率（%）、平均 NFE（Number of Function Evaluations）、推理时间（ms）、AUROC（OOD 检测）
- Limitations: 理论界未严格推导；细粒度双臂协调仍有瓶颈；跨类别泛化改进有限；真实实验样本量小
- Evidence Notes: 全文证据来自 arXiv HTML 完整读取。Table 1-7 和 Figure 1-4 均有详细数据支持。消融实验确认 velocity rescaling（α<1）的关键作用。OOD 检测通过 AUROC 0.93 和 44.3% time saved 量化验证。真实世界实验在 Galaxea R1 Lite 上验证了 Sim-to-Real 有效性。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: 完整覆盖摘要、方法、实验、消融、真实世界实验和结论；附录 A-F 未逐段读取，但关键细节已在正文中引用
- Confidence: high
- Summary: 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head


## Problem

基于 diffusion/flow matching 的模仿学习方法使用时间条件化的速度场，推理时必须沿固定时间表积分。这带来两个结构性问题：
1. **计算效率低**：无论状态复杂度如何，都使用相同步数的积分，简单状态浪费算力，复杂状态可能不够
2. **缺乏内在安全性**：时变场没有静态能量景观，无法直接判断动作有效性或检测 OOD 状态


## Method

### 核心思想
将动作生成从"沿时间轴积分"重构为"在驻定场上做梯度优化"。

### 3.1 Time-Conditioned Baseline 回顾
标准方法：vθ(xγ, γ, st)，γ 是时间变量，推理需要沿 γ∈[0,1] 完成积分。停太早 = 欠积分；超过 1 = 超出训练域。

### 3.2 Time-Unconditional Velocity Field
- 不向模型提供 γ，学习 fθ(x, st)
- 训练时 γ 仅用于构造插值 xγ = γa + (1-γ)ε 和缩放目标 g*(a,ε,γ) = (ε-a)c(γ)
- c(γ) 在 γ→1 时衰减为 0，使 xγ=a 处场消失 → 专家动作成为自然平衡点
- Loss: L(θ) = E‖fθ(xγ, st) - g*(a,ε,γ)‖²

### 3.3 Optimization-Based Inference
- 初始化 a(0) ~ N(0,I)
- 梯度更新：a(k+1) = a(k) - ηk·fθ(a(k), st)
- 收敛判据：‖fθ(a(k), st)‖ ≤ τ_opt 或 k ≥ K_max
- 无时间约束：总步长 ∑ηk 无需等于特定值，可以超过 1

### 3.4 OOD Detection
- Score(st) = ‖fθ(â(st), st)‖（优化后的场范数）
- ID 状态：场收敛到低范数平衡点 → Score 低
- OOD 状态：场本身不在训练分布内 → 梯度范数持续较大 → Score 高
- 零额外开销（与收敛检查共享计算）

### 3.5 VLA Plug-and-Play
- 替换 time-conditioned flow head 为 fθ(x, st)
- 保留 VLM 多模态融合管线
- 微调时固定时间输入 t=0，冻结时间通道
- π0/π0.5 均可直接集成


## Experiments

### 4.1 自适应效率（LIBERO, DiT backbone）
| Method | Max Steps | Success Rate (%) | Avg NFE |
|--------|-----------|------------------|---------|
| Diff. Policy | 100 (Fixed) | 86.5 | 100.0 |
| Rectified Flow | 20 (Fixed) | 90.0 | 20.0 |
| GeCO | 5 | **91.9** | 5.0 |
| GeCO | 10 | 92.4 | 8.7 |
| GeCO | 20 | **93.5** | **11.6** |
| GeCO | 30 | 93.1 | 12.8 |

关键发现：GeCO 仅用 5 步即超过 Rectified Flow 20 步（91.9% vs 90.0%）。20 步预算下平均 NFE 仅 11.6。

### 4.2 VLA 可扩展性

**RoboTwin 2.0（双臂操作）**：
- π0 + GeCO Hard 平均成功率从 0.18 提升至 0.28
- Adjust Bottle Hard: 0.56→0.66; Beat Block Hammer Hard: 0.21→0.36; Click Bell Hard: 0.03→0.21

**VLABench（长视野语言条件操作）**：
- π0 + GeCO 平均 36.0%（vs π0 的 29.4%）
- Track 1: 47.0→61.0; Track 6: 32.2→45.0

**LIBERO VLA**：
- 与标准 π0 微调基本持平（93.9% vs 94.2%）

### 4.3 OOD 检测（LIBERO Goal→Spatial）
| Method | AUROC | TNR(%) | TPR(%) | Time Saved |
|--------|-------|--------|--------|------------|
| Baseline (Moving Avg) | 0.53 | 14.4 | 27.8 | 10.3% |
| GeCO (Moving Avg) | **0.93** | **82.4** | **89.7** | **42.4%** |
| GeCO (Leaky Bucket) | **0.93** | **84.0** | **90.0** | **44.3%** |

### 4.4 消融（截断参数 α）
- α=0.0→0.8：性能稳定（avg 0.909-0.922）
- α=1.0（无截断）：性能骤降至 0.807，证实 velocity rescaling 的必要性
- 最优：α=0.8

### 4.5 真实世界实验（Galaxea R1 Lite）
| Task | Method | Success | Avg NFE | Avg Infer. Time |
|------|--------|---------|---------|-----------------|
| Nut Assembly | G0 Plus | 30% | 10.0 | 252.3ms |
| Nut Assembly | + GeCO | **70%** | **5.06** | **172.4ms** |
| Tube Arrangement | G0 Plus | 25% | 10.0 | 254.6ms |
| Tube Arrangement | + GeCO | **80%** | **3.82** | **150.3ms** |


## Limitations

1. **理论基础待加强**：优化收敛速度、性能增益的理论界、OOD 检测的理论保证尚未严格推导
2. **Blocks Ranking (Size)** 任务上所有方法接近零成功率，表明细粒度双臂协调仍是瓶颈
3. **Track 2 跨类别泛化**：GeCO 改进不明显，说明对纯类别迁移场景帮助有限
4. 真实世界实验样本量较小（每任务仅 10 次）


## Key Takeaways

1. **自适应推理的思路值得关注**：将推理从固定步数积分变为收敛驱动的优化，在 DLO 操控中可按任务阶段自动分配算力（接触阶段多优化，自由移动早停）
2. **内在 OOD 检测对安全部署有价值**：无需额外训练或集成即可检测分布偏移，适合 Sim-to-Real 场景中检测 sim gap
3. **即插即用设计降低了迁移成本**：作为 flow head 替换件可直接用于现有 VLA 架构，微调代价低
4. **对 DLO 操控的启示**：DLO 任务中接触与非接触阶段差异大，GeCO 的自适应计算可能特别适合；但论文未涉及可变形物体

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhang-zunzhe|Zhang, Zunzhe]]
