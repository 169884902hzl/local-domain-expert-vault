---
title: "Break the block: Dynamic-size reasoning blocks for diffusion large language models via monotonic entropy descent with reinforcement learning"
tags: [diffusion, RL]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "提出 b1 框架，通过 RL 学习动态大小的推理块并施加单调熵下降约束，解决扩散语言模型中固定大小分块破坏推理连贯性的问题，在数学推理基准上相比固定分块基线最高提升 19.53%。"
authors: "Jiang, Yan; Qiu, Ruihong; Huang, Zi"
year: "2026"
venue: "ICML 2026"
zotero_key: "N4VBXFZ3"
---
## 摘要

Recent diffusion（扩散） large language models (dLLMs) have demonstrated both effectiveness and efficiency in reasoning via a block-based semi-autoregressive generation paradigm. Despite their progress, the fixed-size block generations remain a critical bottleneck for effective and coherent reasoning. 1. From a global perspective, different reasoning tasks would correspond to different optimal decoding block sizes, which makes a ``one-size-fits-all'' assumption ineffective. 2. Even within a single reasoning task, the rigid block partitioning would break the logical flow and reduce reasoning coherence. Through empirical observations, we reveal that for block-wise entropy, incorrect reasoning exhibits a fluctuating and unsteady trend between blocks, whereas the correctly generated tasks follow a consistent descending trend. Therefore, this paper proposes b1, a novel post-training framework for dLLMs that learns dynamic-size reasoning blocks via a Monotonic Entropy Descent objective with reinforcement learning（强化学习） to enhance reasoning coherence.b1 integrates seamlessly as a plug-and-play module with existing dLLM's post-training algorithms. Extensive experiments across various reasoning benchmarks showcase b1's consistent improvement over existing fixed-size block baselines. Our code has been released at https://github.com/YanJiangJerry/Block-R1.

## 中文简述

提出 b1 框架，通过 RL 学习动态大小推理块并施加单调熵下降（MED）约束，解决扩散语言模型固定分块破坏推理连贯性的问题。在 Countdown 上相比固定分块基线提升最高 19.53%。

**研究方向**: 扩散语言模型、强化学习、推理、动态分块

## 关键贡献

1. **Dynamic Reasoning Blocks**：首个针对 dLLM 的 RL 驱动动态分块框架，通过学习 block ending indicator token `\block` 让每个块对齐一个完整推理步骤。
2. **Monotonic Entropy Descent (MED)**：提出基于 block 熵的单调递减 RL 奖励 $R_{ent}$，理论证明其全局最优等价于最大化负 Spearman 秩相关系数（Theorem 1，基于排序不等式证明）。
3. **理论洞察**：证明局部逐对熵下降代理奖励与全局 Spearman 系数共享同一全局最优解（Appendix D 完整证明）。
4. **Plug-and-Play**：b1 可无缝叠加到现有 dLLM RL 框架（Diffu-GRPO、GDPO、d1、wd1），统一权重 α=β=γ=1，无需超参调优。
## 结构化提取

- Problem: 扩散语言模型的固定大小分块生成策略破坏推理连贯性，不同任务需要不同最优分块大小
- Method: b1 框架，通过 RL 学习动态大小推理块，引入 Monotonic Entropy Descent 奖励和 block ending indicator 奖励
- Tasks: 数学推理（GSM8K, MATH500, Countdown, Sudoku 4×4）
- Sensors: N/A（纯语言模型，无传感器输入）
- Robot Setup: N/A（纯计算实验，4× AMD Mi300x GPU）
- Metrics: Test accuracy (pass@1), r_SCC（Spearman 秩相关系数）, r_MED（正 r_SCC 比例）, 训练时间/step, 推理吞吐 tokens/s
- Limitations: 单一基座模型（LLaDA-8B）；仅数学推理领域；仅 256/512 token 长度；mean-field 假设忽略块内 token 依赖；K_target=10 未针对任务复杂度调优
- Evidence Notes: 全文包含完整实验（Table 1-4）、消融实验（Table 2）、MED 与推理的相关性分析（Figure 5）、困难样本改善分析（Figure 6）、case study（Figure 7, Appendix E.2）、超参敏感性（Appendix E.1）、理论证明（Appendix D）、伪代码（Algorithm 1-2）、完整复现细节（Appendix C）
## 本地引用关系

- [[jiang2026break]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（正文+附录，含定理证明、消融实验、超参敏感性分析、case study）
- Confidence: high
- Summary: 提出 b1 框架，通过 RL 学习动态大小的推理块并施加单调熵下降约束，解决扩散语言模型中固定大小分块破坏推理连贯性的问题，在数学推理基准上相比固定分块基线最高提升 19.53%。


## Problem

当前扩散语言模型（dLLM，如 LLaDA）采用固定大小的分块并行生成策略。这带来两个核心问题：

1. **全局层面**：不同推理任务对应不同的最优分块大小，"一刀切"的固定分块策略无法适应任务差异（Figure 1 实证）。
2. **局部层面**：即使在单次推理中，刚性分块边界会打断推理链的逻辑流（如在数字运算中间切断，如 "71−" 和 "6" 被分到相邻块），导致高熵异常和推理错误（Figure 2）。

**关键观察**：正确推理的 block-wise 熵呈单调递减趋势（模型置信度随推理推进逐步提高），而错误推理的 block 熵出现波动或停滞（Figure 3）。


## Method

### 核心架构

b1 由三个组件构成：

**（1）动态分块机制（Section 3.1）**
- 引入特殊 indicator token `τ_end`（默认为 `\block`）标记推理步骤边界
- 动态分块大小 d 由生成过程中首次出现 `τ_end` 的位置决定（Eq. 4）
- 若未生成 `τ_end`，则回退到最大剩余长度

**（2）Block Ending Indicator Reward（Eq. 5）**
- $R_{ind}$：对数缩放的块数量奖励，鼓励多步推理
- 当 $K \geq K_{target}$（默认10）时奖励为 1.0，否则按 log 尺度递增
- 防止模型生成过少推理步骤

**（3）Monotonic Entropy Descent（Section 3.2）**
- Block 熵定义：块内 token-wise Shannon 熵的均值（Eq. 6），基于 mean-field 假设（token 独立）
- 全局目标：最大化负 Spearman 秩相关系数 $r_{SCC}$（Eq. 7），但直接优化不可行（全局排序导致高方差）
- 代理奖励 $R_{ent}$（Eq. 8）：相邻块熵的逐对比较，$R_{ent} = \frac{1}{K-1} \sum_{k=2}^{K} \mathbb{I}(H(b_{k-1}) > H(b_k))$
- Theorem 1 证明：$\arg\max R_{ent} = \arg\max r_{SCC}$，即局部代理与全局目标共享最优解

**总奖励（Eq. 10）**：$R_{total} = \alpha R_{ent} + \beta R_{ind} + \gamma R_{task}$，默认 α=β=γ=1

**推理阶段（Algorithm 2）**：每个 block 的去噪过程中，搜索 `τ_end` token 确定动态边界，实现推理步骤对齐的并行生成。

**复杂度**：$O(K \cdot T \cdot L + L)$，相比 self-attention 的 $O(L^2)$ 可忽略。


## Experiments

### 数据集与基线
- **基座模型**：LLaDA-8B-Instruct
- **数据集**：GSM8K、MATH500、Sudoku (4×4)、Countdown
- **RL 框架基线**：Diffu-GRPO、GDPO、d1、wd1
- **推理时方法基线**：AdaBlock-dLLM（基于置信度阈值在换行符处截断）
- **其他基线**：SFT（标准去噪交叉熵）
- **硬件**：4× AMD Mi300x GPU（192GB），per-device batch size 12
- **序列长度**：256 和 512

### 主要结果（Table 1）

| 框架 + b1 | Sudoku | Countdown | GSM8K | MATH500 |
|-----------|--------|-----------|-------|---------|
| wd1 + b1 (256) | **+4.15** | **+19.53** | **+1.97** | **+3.20** |
| d1 + b1 (256) | +3.42 | +5.08 | +1.21 | +1.00 |
| Diffu-GRPO + b1 (256) | +3.44 | +8.99 | +2.04 | +1.00 |
| GDPO + b1 (256) | +2.41 | +6.25 | +1.14 | +1.60 |

- b1 在所有框架和数据集上一致提升性能
- Countdown 提升最显著（最高 +19.53%），说明动态分块对需要多步计算的推理任务最为关键
- 512 token 长度下趋势一致
- AdaBlock-dLLM 在 zero-shot 设置下未提升（因为推理步骤不一定在换行符处终止）

### 消融实验（Table 2）
- **w/o MED**（移除 $R_{ent}$）：性能显著下降，尤其在 Countdown 上
- **w/o $R_{ind}$**（移除 indicator reward）：性能也有下降
- 所有 b1 变体仍优于固定分块基线

### MED 与推理性能的相关性（Section 4.3, Figure 5）
- $r_{SCC}$ 越高（越单调递减），推理准确率越高
- b1 消除了 Countdown 中低 $r_{SCC}$ 的样本群（负 $r_{SCC} < -0.5$）

### b1 对 MED 的改善（Table 3）
- b1 在所有数据集上均提高 $r_{SCC}$ 和 $r_{MED}$（正 $r_{SCC}$ 的比例）
- 如 Countdown：$r_{SCC}$ 从 58.98% → 62.77%，$r_{MED}$ 从 91.41% → 97.66%

### 困难样本改善（Section 4.5, Figure 6）
- 对固定分块基线预测错误的"困难"样本，b1 一致提高其 $r_{SCC}$ 并减少错误数

### 效率（Table 4）
- 训练开销：每步从 2.76s → 2.82s（d1），1.31s → 1.68s（wd1），增加可忽略
- 推理吞吐：28.57 → 27.03 tokens/s，几乎不变
- b1 达到最优性能的步数显著少于基线（如 Countdown：2100 vs wd1 的 3000）

### 超参敏感性（Appendix E.1）
- 奖励权重在 0.5-2.0 范围内波动时 b1 稳定优于基线
- 默认权重 1.0 优于 0（即移除 b1 奖励），验证了 b1 奖励的有效贡献


## Limitations

1. **单一基座模型**：仅在 LLaDA-8B-Instruct 上验证，未测试 Dream 7B 等非 block-based dLLM 骨干（作者解释 Dream 不原生支持 block-based 生成）
2. **领域局限**：仅覆盖数学/逻辑推理任务，未涉及代码生成、对话等其他生成场景
3. **序列长度**：仅测试 256 和 512 token，未验证超长生成场景
4. **Mean-field 假设**：Block 熵计算假设 token 独立，忽略了块内 token 间依赖关系
5. **K_target 超参**：目标块数量默认 10，对不同复杂度的推理任务可能不是最优
6. **仅验证 zero-shot**：未测试 few-shot 场景


## Key Takeaways

1. **熵作为推理质量信号**：Block-wise 熵的单调递减趋势是推理质量的强指示信号。这一观察对 DLO 操控中 VLM 的推理链生成有启发——可以通过监控生成过程的熵来检测推理失败。
2. **动态分块 vs 固定分块**：对需要多步骤推理的任务，动态大小分块远优于固定分块。这一思想可能延伸到机器人任务规划中的步骤粒度控制。
3. **代理奖励设计**：将全局不可优化的目标（Spearman 系数）分解为局部逐对比较是一种有效的 RL 奖励设计策略，适用于需要全局单调性的场景。
4. **与 DLO 操控的关联较弱**：本文属于 NLP/LLM 领域的推理增强工作，与 DLO 操控、Sim-to-Real、VLM-based 控制等机器人方向无直接技术关联。关联点仅在于扩散模型和 RL 的通用方法论。

## 相关概念

- [[diffusion-model]]
- [[reinforcement-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[jiang-yan|Jiang, Yan]]
- [[qiu-ruihong|Qiu, Ruihong]]
- [[huang-zi|Huang, Zi]]
