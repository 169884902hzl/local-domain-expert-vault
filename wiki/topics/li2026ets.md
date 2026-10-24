---
title: "ETS: Energy-guided test-time scaling for training-free RL alignment"
tags: [RL, diffusion, test-time-scaling]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出训练无关的推理时采样方法 ETS，通过在线 Monte Carlo 估计能量项直接从 RL 最优策略采样，统一覆盖自回归模型和扩散语言模型，在推理/编码/科学基准上超越 GRPO 等训练后方法。"
authors: "Li, Xiuyu; Zhang, Jinkai; Yi, Mingyang; Li, Yu; Wang, Longqiang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TSGAJF8E"
---
## 摘要

Reinforcement Learning（强化学习） (RL) post-training alignment for language models is effective, but also costly and unstable in practice, owing to its complicated training process. To address this, we propose a training-free inference method to sample directly from the optimal RL policy. The transition probability applied to Masked Language Modeling (MLM) consists of a reference policy model and an energy term. Based on this, our algorithm, Energy-Guided Test-Time Scaling (ETS), estimates the key energy term via online Monte Carlo, with a provable convergence rate. Moreover, to ensure practical efficiency, ETS leverages modern acceleration frameworks alongside tailored importance sampling estimators, substantially reducing inference latency while provably preserving sampling quality. Experiments on MLM (including autoregressive models and diffusion（扩散） language models) across reasoning, coding, and science benchmarks show that our ETS consistently improves generation quality, validating its effectiveness and design. The code is available at https://github.com/sheriyuo/ETS.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 强化学习、扩散模型、推理时扩展

## 关键贡献

1. **推导了统一的反向转移核**（Proposition 2）：在 MLM 框架下，最优反向转移 p(x_s | x_t, y) 可分解为参考模型的转移核与一个能量项（条件期望的指数奖励）的乘积。该结果同时适用于 ARMs 和 DLMs
2. **提出了 ETS 算法**（Algorithm 1）：通过在线 Monte Carlo 估计能量项，结合自归一化重要性采样从候选集中采样。证明了收敛速率（Proposition 3）：TV 距离为 O(I/√M + Iε)
3. **设计了加速方法**（Algorithm 2 / ETS-IS）：用轻量级 proposal model（ARMs 用 Qwen3 小模型，DLMs 用 Fast-dLLM）配合重要性采样校正，大幅降低延迟，同时给出含加速的完整误差界（Theorem 1）
4. **设计了训练无关的奖励**：通过 self-consistency（多数投票一致性）作为 proxy reward，无需 ground truth，并证明了投票错误的指数衰减率（Theorem 2）
5. **广泛实验验证**：在 Qwen3-1.7B/8B 和 LLaDA-8B 上覆盖 MATH500、GSM8K、GPQA、HumanEval，ETS 持续超越 GRPO 等训练后方法
## 结构化提取

- Problem: LLM RL post-training 训练成本高、不稳定、不可复用；虽有闭式最优解但现有方法仅通过梯度优化近似
- Method: ETS — 在 MLM 框架下推导反向转移核的参考模型+能量项分解；在线 Monte Carlo 估计能量；自归一化重要性采样选择候选；轻量模型 + IS 加速
- Tasks: 数学推理（MATH500, GSM8K）、代码生成（HumanEval）、科学推理（GPQA）
- Sensors: N/A（纯语言模型任务）
- Robot Setup: N/A
- Metrics: Accuracy（pass@1），推理延迟（相对 base 的倍数）
- Limitations: 高延迟、self-consistency 仅限可验证任务、proposal model 依赖、缺少大规模模型验证、DLM 加速有限
- Evidence Notes: 全文精读（正文 8 页 + 附录 A-D 约 12 页），包括完整理论推导、4 个 benchmark 的主实验、多个消融实验。论文发表于 ICML 2026，理论完整，实验充分
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 100%（正文 + 附录 A-D 均已阅读）
- Confidence: high
- Summary: 提出训练无关的推理时采样方法 ETS，通过在线 Monte Carlo 估计能量项直接从 RL 最优策略采样，统一覆盖自回归模型和扩散语言模型，在推理/编码/科学基准上超越 GRPO 等训练后方法。


## Problem

LLM 的 RL post-training alignment（如 RLHF、PPO、DPO、GRPO）虽有效，但存在根本性局限：
1. **训练成本高**：需要大规模人类偏好数据和昂贵的奖励建模
2. **训练不稳定**：对超参数敏感，训练动态不稳定
3. **不可复用**：奖励设计变化时必须重新训练
4. **理论已知最优解**：KL-regularized RL 目标已有闭式解（Proposition 1），但现有训练方法仅通过迭代梯度优化近似该解

核心问题：既然最优 RL 分布有闭式表达，能否在推理时直接从中采样，完全跳过训练过程？


## Method

### 统一 MLM 框架
将自回归模型（ARMs）和扩散语言模型（DLMs）统一到 Masked Language Modeling (MLM) 框架下：
- 生成过程是从全掩码序列 x_T 到干净序列 x_0 的反向马尔可夫链
- ARMs：固定从左到右的去掩码路径
- DLMs：灵活的非顺序去掩码（每步揭开 top-K 概率的 token）

### 核心理论推导
KL-regularized RL 目标的最优解为闭式（Proposition 1）：
p*(x_0|y) ∝ p_ref(x_0|y) · exp(r(y, x_0)/λ)

关键推导（Proposition 2）：反向转移核分解为：
p(x_s|x_t,y) ∝ p_ref(x_s|x_t,y) · E_{p_ref(x_0|y,x_s)}[exp(-r(y,x_0)/λ)] / E_{p_ref(x_0|y,x_t)}[exp(-r(y,x_0)/λ)]

即参考模型转移 × 能量比。能量项衡量当前部分序列 x_s 有多大概率通向高奖励完整序列。

### ETS 算法流程
1. 在 I 个 guidance step 上迭代
2. 每步：从参考模型采样 M 个候选 x_{t_{i-1}}^(m)
3. 对每个候选，采样 K 个完整补全，用 Monte Carlo 估计能量
4. 按能量自归一化权重进行多项式采样选择最佳候选
5. 当 I=1, λ→0 时退化为 Best-of-N

### 加速方法（ETS-IS）
- ARMs：用 Qwen3 小模型（scale-aligned, 共享 tokenizer）作为 proposal
- DLMs：用 Fast-dLLM（KV cache + 置信度感知并行解码）作为 proposal
- 重要性采样校正：E_small(y,x_s) = (1/K) Σ p_ref/p_small · exp(-r/λ)
- Theorem 1 保证加速后的收敛性：O(I/√M + I/√K)

### 奖励设计
Self-consistency reward：对 K 个补全提取最终答案，与多数投票一致的得 1 分，否则 0 分。理论保证（Theorem 2）：投票错误率指数衰减。


## Experiments

### 实验设置
- **模型**：Qwen3-1.7B、Qwen3-8B（ARMs）、LLaDA-8B-Instruct（DLM）
- **基准**：MATH500（数学）、GSM8K（初等数学）、HumanEval（编程）、GPQA Diamond（科学）
- **硬件**：4 × H20-3e-141GB GPUs
- **评估方式**：单次（pass@1）

### 主结果（Table 1 关键数据）

**Qwen3-8B：**
| 方法 | MATH500 | GSM8K | GPQA | HumanEval | 平均 | 延迟倍数 |
|------|---------|-------|------|-----------|------|----------|
| Base | 60.0 | 89.39 | 34.34 | 58.54 | 60.57 | 1× |
| Best-of-N | 65.2 | 94.09 | 38.89 | 67.07 | 66.31 | 5.16× |
| ETS | **72.4** | **94.24** | 38.38 | **71.34** | **69.34** | 7.35× |
| ETS-IS | 66.2 | 91.81 | 38.89 | 68.90 | 66.45 | 5.26× |
| GRPO（训练后） | 69.2 | 90.98 | 37.88 | 65.85 | 65.98 | 1× |

**Qwen3-1.7B：** ETS 平均 54.76%，超过 GRPO 的 48.08%
**LLaDA-8B：** ETS 平均 51.01%，超过 VRPO 的 46.40%

关键发现：
- ETS 在所有模型族和任务上持续超越 GRPO（训练后 RL 策略），无需任何参数更新
- ETS-IS 以约 5× 延迟达到与 GRPO 相当的水平
- Baseline TTS 方法（Best-of-N, Beam Search）在增加计算量时性能反而下降（verification noise），而 ETS 通过同时扩展 M 和 K 避免此问题

### 消融实验
1. **总样本数 M×K**：增加 M 比增加 K 更有效；K=3 是良好的精度-效率平衡点
2. **Guidance steps I**：I 越大精度越高但延迟越高；建议 I=4 或 8
3. **延迟-精度权衡**：ETS 在可比延迟下显著优于其他 TTS 方法
4. **奖励设计**：self-consistency 在所有候选（logits、entropy、self-certainty、self-consistency）中与 ground-truth 奖励相关性最强

### 未提供的实验证据
- 在更大规模模型（如 70B+）上的结果
- 在非推理任务（对话、创意写作）上的表现
- 真实 ground-truth 奖励 vs self-consistency 的量化差距
- 不同 proposal model 选择对 IS 方差的影响分析


## Limitations

1. **推理延迟高**：即使有 ETS-IS 加速，延迟仍为标准推理的 5-30×，不适合实时交互场景
2. **Self-consistency 奖励的局限**：仅适用于有明确最终答案的任务（数学、编程），难以推广到开放式生成或人类偏好对齐
3. **Proposal model 依赖**：ARMs 的加速依赖同系列的轻量模型（Qwen3 小模型），换模型族可能需重新选择 proposal
4. **奖励设计受限**：需要"可验证"的奖励函数（verifiable reward），论文仅用 self-consistency 作为 proxy，缺少对非可验证奖励场景的讨论
5. **理论界的实用性**：TV 距离界在实际中难以计算，O(I/√M + Iε) 的常数项可能很大
6. **DLM 加速有限**：LLaDA 的并行解码速度本质上受限，TTS 延迟远高于 ARMs


## Key Takeaways

1. **训练无关对齐的可行性**：ETS 证明通过直接从 RL 最优分布采样，可以在不训练的情况下超越训练后方法。这对资源受限场景（无力做 RL 训练）有重要意义
2. **MLM 统一框架的价值**：将 ARMs 和 DLMs 统一处理的理论框架简洁优雅，Proposition 2 的分解形式清晰揭示了最优策略的结构
3. **推理时扩展的范式**：ETS 将 test-time scaling 的核心归结为"能量估计"，与 MCTS、Best-of-N 等方法形成统一的 Monte Carlo 视角
4. **对 DLO 操控的间接启发**：能量引导生成的思想（在部分状态估计未来奖励的期望）与 model-predictive control 和 trajectory optimization 有结构相似性。扩散策略（diffusion policy）中的 guidance 机制本质上也是能量引导

## 相关概念

- [[reinforcement-learning]]
- [[diffusion-model]]
- [[test-time-scaling]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[li-xiuyu|Li, Xiuyu]]
