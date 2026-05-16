---
title: "Offline policy evaluation for manipulation policies via discounted liveness formulation"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "将离线策略评估重新定义为折扣 liveness 问题，通过两阶段 bootstrapping 机制在稀疏奖励操控任务中捕获非单调任务进展并显著降低截断偏差。"
authors: "Wang, Hao; Bowden, Joshua; Crosby, Colton; Bansal, Somil"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "57IREV2I"
---
## 摘要

Policy evaluation is a fundamental component of the development and deployment pipeline for robotic policies. In modern manipulation（操控） systems, this problem is particularly challenging: rewards are often sparse, task progression of evaluation rollouts are often non-monotonic as the policies exhibit recovery behaviors, and evaluation rollouts are necessarily of finite length. This finite length introduces truncation bias, breaking the infinite-horizon assumptions underlying standard methods relying on Bellman equations/principle of optimality. In this work, we propose a framework for offline policy evaluation from sparse rewards based on a liveness-based Bellman operator. Our formulation interprets policy evaluation as a task-completion problem and yields a conservative fixed-point value function that is robust to finite-horizon truncation. We analyze the theoretical properties of the proposed operator, including contraction guarantees, and show how it encodes task progression while mitigating truncation bias. We evaluate our method on two simulated manipulation（操控） tasks using both a Vision-Language-Action model and a diffusion policy（扩散策略）, and a cloth folding task using human demonstrations. Empirical results demonstrate that our approach more accurately reflects task progress and substantially reduces truncation bias, outperforming classical baselines such as TD(0) and Monte Carlo policy evaluation.

## 中文简述

将离线策略评估定义为折扣 liveness 问题，用 min 算子和两阶段 bootstrapping 减少截断偏差，在稀疏奖励操控任务中显著优于 TD(0) 和 MC。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. **Liveness 公式化**：首次将操控策略的离线评估重新定义为折扣 liveness 问题，用 min 算子替代经典 Bellman 方程中的求和，使值函数反映状态到目标集的语义距离而非累积奖励
2. **两阶段 bootstrapping 算法**：第一阶段从成功回合的目标状态反向计算 well-defined 值作为锚点；第二阶段用这些锚点修正超时回合中与成功状态相似的状态的值，有效减少截断偏差
3. **理论保证**：证明了折扣 Bellman 算子（Eq. 7）在 supremum 范数下是压缩映射（Proposition 2），且 liveness 值函数是真实值的一个保守/悲观估计（Proposition 1）
## 结构化提取

- Problem: 稀疏奖励下机器人操控策略的离线评估，面临截断偏差和非单调任务进展
- Method: 折扣 liveness Bellman 算子 + 两阶段 bootstrapping 机制
- Tasks: LIBERO-Spatial 拾取放置、Square 方形插孔插入、布料折叠（硬件）
- Sensors: 基座和腕部 RGB 相机（仿真），基座 RGB 相机（硬件）
- Robot Setup: Franka Panda 机械臂，仿真环境 LIBERO/Robomimic + 硬件实验平台
- Metrics: Success Metric（成功回合中步数估计准确率）、Failure Metric（超时回合中不可达预测准确率）、Composite Metric（二者均值）
- Limitations: 视觉相似状态的过度乐观；数据集依赖；不适用于无恢复行为的策略；未验证 DLO 等复杂任务
- Evidence Notes: 全文精读完成。核心贡献是 liveness 公式化和 bootstrapping 机制的理论分析（Prop 1-2 有完整证明）和三个 case study 的实验验证。数据集大小消融和编码器消融提供额外证据。统计显著性通过 Alexander-Govern + Welch's t-test 验证。
## 本地引用关系

- [[wang2026offline]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文来自 arXiv PDF，含所有章节、附录、完整实验表格）
- Confidence: high
- Summary: 将离线策略评估重新定义为折扣 liveness 问题，通过两阶段 bootstrapping 机制在稀疏奖励操控任务中捕获非单调任务进展并显著降低截断偏差。


## Problem

机器人操控策略的离线评估面临三大挑战：
1. **稀疏奖励**：仅有二元任务完成信号（成功/超时），缺乏密集奖励
2. **有限回合截断偏差**：实际评估回合有固定时长上限，超时被悲观地等价于策略失败，违反经典 Bellman 方程的无限时域假设
3. **非单调任务进展**：策略具有恢复行为（如物体滑落后重新抓取），导致任务进展非单调，经典方法无法正确建模

现有方法（TD(0)、Monte Carlo）在稀疏奖励、有限时域设置下表现不佳：MC 方差大，TD 无法长距离反向传播稀疏成功信号。


## Method

### 核心思想：Liveness 公式化
将经典 MDP 中的奖励函数 R(·) 替换为目标函数 l(·)（有符号距离函数），策略评估变为：V^π(s) = E[min_k l(ξ(k))]，即从状态 s 出发的所有轨迹中最低目标值的期望。

**折扣 Bellman 算子**：
```
Ṽ^π(s) = (1 - γ) + γ · min{l(s), Ṽ^π(s')}
```

**目标函数定义**（稀疏奖励形式）：
- l(s) = 1，若 s 不是目标状态
- l(s) = -1，若 s 是目标状态

值函数与任务完成步数的关系：Ṽ^π(s_{N-k}) = 1 - 2γ^k，因此 k = log_γ((1 - Ṽ^π(s)) / 2)

### 两阶段 Bootstrapping（Algorithm 1）
1. **阶段一**：仅用成功子集 D'，从目标状态反向计算 well-defined 值 V^π(s)
2. **Bootstrap 目标函数**：用 V^π 替换 l(s)，对于没有 well-defined 值的状态保持 l(s) = 1
3. **阶段二**：用 bootstrapped 目标函数和折扣 Bellman 算子（Eq. 11）在整个数据集 D 上计算最终值函数 Ṽ^π

关键机制：min 算子充当"修正滤波器"——当超时回合中的状态与成功回合中的状态相似时，其悲观值会被更乐观的已知成功值覆盖。

### 值函数学习
- 输入：SigLIP2 图像潜空间嵌入 + 本体感知状态的拼接
- 网络结构：5 层 MLP，512 隐藏单元，GELU 激活，LayerNorm
- 训练：prioritized experience replay，5000 epochs


## Experiments

### 评估任务
| 任务 | 策略类型 | 机器人 | 训练/测试回合 | 时域 |
|------|---------|--------|-------------|------|
| LIBERO-Spatial Pick&Place | VLA (π₀ 0.5) | Franka Panda | 200/100 | 250 |
| Square Peg-Hole Insertion | Diffusion Policy | Franka Panda | 200/100 | 200 |
| Cloth Folding (硬件) | Human Teleop | Franka Panda | 150/20 | 300 |

### Baselines
- **Ours-NB**：本文方法的消融版（无 bootstrapping）
- **TD(0)**：标准时序差分
- **MC**：Monte Carlo
- **MC-D**：Distributional Monte Carlo（来自 π₀* .6）

### 主要结果（完整数据集，5 seeds）
| 任务 | 方法 | Success↑ | Failure↑ | Composite↑ |
|------|------|----------|----------|-----------|
| LIBERO-Spatial | Ours | **0.8550±0.0174** | 0.9870±0.0044 | **0.9210±0.0092** |
| LIBERO-Spatial | TD(0) | 0.7667±0.0101 | 0.9974±0.0005 | 0.8821±0.0048 |
| LIBERO-Spatial | MC | 0.7012±0.0117 | **0.9993±0.0003** | 0.8502±0.0057 |
| Square | Ours | **0.6190±0.0128** | 0.8840±0.0197 | **0.7515±0.0111** |
| Square | TD(0) | 0.5937±0.0081 | 0.9267±0.0024 | 0.7602±0.0032 |
| Cloth Folding | Ours | **0.5778±0.0246** | 0.8341±0.0179 | **0.7060±0.0158** |
| Cloth Folding | TD(0) | 0.2392±0.0082 | 0.0641±0.0090 | 0.1516±0.0036 |
| Cloth Folding | MC | 0.1995±0.0106 | **0.9911±0.0019** | 0.5953±0.0059 |

注：Ours 在所有任务的 success metric 和 composite metric 上均为最优（经 Alexander-Govern + Welch's t-test 统计显著性验证，p < 0.05），failure metric 略低于 MC 系（bootstrapping 的预期代价）。

### 消融实验
1. **Bootstrapping 消融**：Ours-NB 在 success 和 composite 上低于 Ours，在 failure 上略高，证实 bootstrapping 提升成功预测准确率但略牺牲失败识别
2. **数据集大小消融**（50/100/150/200 episodes）：Ours 在所有数据规模下保持优势；小数据集下 Ours 的 success metric 仍优于 baselines 的完整数据集结果
3. **编码器消融**（Cloth Folding，SigLIP2/CLIP/DINOv2）：三种编码器性能相近，方法对编码器选择不敏感

### 定性分析
- LIBERO：值函数能正确识别碗滑落后的状态回退（值上升）和恢复后的进展（值下降），与语义任务进展高度吻合
- Square：值函数能预测性地识别不良抓取（值接近 1 预示后续失败），但对"意外"滑落只能反应而非预判
- Cloth Folding：操作员挣扎阶段值在零附近振荡，建立良好抓取后值急剧下降


## Limitations

1. **过度乐观**：bootstrapping 通过神经网络学习状态相似性，没有明确边界来判断哪些超时状态应该被视为与成功状态重叠；视觉线索少的任务（如 Square）中问题更严重
2. **数据集依赖**：方法性能依赖训练分布外的泛化能力，数据集组成会导致值函数偏向乐观或悲观，目前无法系统性地刻画这种偏差
3. **恢复行为依赖**：对于不具备恢复行为的策略（如 Square 的 diffusion policy），bootstrapping 效果减弱，因为超时和成功状态在视觉空间中几乎不可区分
4. **仅限稀疏奖励**：未探索密集奖励设置下的适用性
5. **未验证 DLO 操控或更复杂的多步任务**


## Key Takeaways

1. **策略评估≠策略训练**：这篇论文关注的是"如何评估一个已有策略的好坏"而非训练策略本身，这在部署前的安全性和可靠性评估中至关重要
2. **Liveness 范式对 DLO 操控有价值**：DLO 操控中同样存在稀疏奖励（成功/失败）、非单调进展（绳索缠绕/解开）和截断偏差问题，该 liveness 公式化可以直接迁移
3. **Bootstrapping 的核心洞察**：利用成功和超时回合之间的状态重叠来修正悲观值，这个思路可以扩展到任何需要从有限回合数据中估计长期性能的场景
4. **VLA + Diffusion Policy 评估**：论文同时在 VLA（π₀）和 Diffusion Policy 上验证，表明方法与策略架构无关
5. **值函数的可解释性**：值可以直接转化为"到成功的步数估计"（k = log_γ((1-V)/2)），具有明确的物理含义

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wang-hao|Wang, Hao]]
- [[bansal-somil|Bansal, Somil]]
