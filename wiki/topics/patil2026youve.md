---
title: "You've got a golden ticket: Improving generative robot policies with a single noise vector"
tags: [manipulation, imitation, RL, diffusion, flow-matching]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需训练任何额外网络"
authors: "Patil, Omkar; Biza, Ondrej; Weng, Thomas; Schmeckpeper, Karl; Thomason, Wil et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "9E5ACJUA"
---
## 摘要

What happens when a pretrained generative robot policy is provided a constant initial noise as input, rather than repeatedly sampling it from a Gaussian? We demonstrate that the performance of a pretrained, frozen diffusion（扩散） or flow matching policy can be improved with respect to a downstream reward（奖励） by swapping the sampling of initial noise from the prior distribution (typically isotropic Gaussian) with a well-chosen, constant initial noise input -- a golden ticket. We propose a search method to find golden tickets using Monte-Carlo policy evaluation that keeps the pretrained policy frozen, does not train any new networks, and is applicable to all diffusion（扩散）/flow matching policies (and therefore many VLAs). Our approach to policy improvement makes no assumptions beyond being able to inject initial noise into the policy and calculate (sparse) task rewards of episode rollouts, making it deployable with no additional infrastructure or models. Our method improves the performance of policies in 38 out of 43 tasks across simulated and real-world robot manipulation（机器人操控） benchmarks, with relative improvements in success rate by up to 58% for some simulated tasks, and 60% within 50 search episodes for real-world tasks. We also show unique benefits of golden tickets for multi-task（多任务） settings: the diversity of behaviors from different tickets naturally defines a Pareto frontier for balancing different objectives (e.g., speed, success rates); in VLAs, we find that a golden ticket optimized for one task can also boost performance in other related tasks. We release a codebase with pretrained policies and golden tickets for simulation benchmarks using VLAs, diffusion（扩散） policies, and flow matching policies.

## 中文简述

提出基于扩散模型的线缆操控方法，具有多任务特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、Flow Matching

## 关键贡献

1. **提出机器人控制的 Lottery Ticket Hypothesis**：预训练扩散/Flow Matching策略中存在特殊的固定初始噪声向量（golden ticket），替换高斯采样即可显著提升下游任务表现
2. **设计基于随机搜索的 golden ticket 搜索方法**：使用 Monte-Carlo 策略评估，保持预训练策略权重冻结，不训练任何新网络，适用于所有扩散/Flow Matching策略
3. **大规模验证**：在4个仿真benchmark（40个任务）和3个真实世界任务上验证，43个任务中38个获得性能提升
4. **与 SOTA latent steering 方法对比**：在5个 DexMimicGen 任务上与 DSRL 竞争，无需训练额外网络且性能相当甚至更优
5. **多任务泛化与多目标 Pareto 前沿**：VLA 中一个任务的 golden ticket 可迁移到相关任务；不同 ticket 自然形成多目标（速度 vs 成功率）的 Pareto 前沿
6. **开源代码和预训练模型**：包含 VLA、扩散策略、Flow Matching 策略的 golden ticket
## 结构化提取

- Problem: 如何在不修改权重、不训练额外网络、不做额外假设的前提下提升预训练扩散/Flow Matching机器人策略的性能
- Method: Golden Ticket——用固定优化的初始噪声向量替代高斯采样，通过随机搜索（Monte-Carlo 策略评估）寻找最优噪声向量
- Tasks: 单臂抓取、双臂操控（5种任务）、物体推动、VLA 多任务（30个 LIBERO 任务）
- Sensors: RGB 图像、点云、低维状态、本体感受数据、语言指令（VLA）
- Robot Setup: Franka 单臂（仿真+真实）、Franka 双臂（DexMimicGen 仿真）、LIBERO 环境
- Metrics: 成功率（主要）、速度（Pareto分析）、累积折扣奖励
- Limitations: 策略变确定性、5/43任务无效、无离线评估指标、跨任务平均性能可能下降、空间泛化有限
- Evidence Notes: 全文证据充分，4个仿真benchmark（40任务）+ 3个真实任务，与DSRL对比实验，DDIM步数消融，跨任务迁移实验，Pareto前沿分析。DDIM步数分析显示 golden ticket 在少步采样时提升更大。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含摘要、方法、4个仿真benchmark + 3个真实任务、消融实验、DDIM步数分析、局限性讨论）
- Confidence: high
- Summary: 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需训练任何额外网络


## Problem

预训练的扩散/Flow Matching机器人策略在下游任务上的开箱即用性能仍有提升空间。现有策略改进方法存在三大限制：
1. 直接微调模型权重——对VLA等大模型计算代价高，且容易灾难性遗忘
2. 训练额外网络（如残差策略、噪声策略）——需要复杂的模型设计选择
3. 依赖外部模型（如世界模型、critic网络）或特殊训练方案——限制适用范围

核心问题：能否在不修改权重、不训练额外网络、不做额外假设的前提下，提升预训练生成式策略的性能？


## Method

### 核心思路
扩散/Flow Matching 策略在推理时，通常从各向同性高斯分布 $N(0, I)$ 采样初始噪声 $z_1$，然后通过去噪模型迭代生成动作。本文提出用**固定的、经过优化的初始噪声向量** $w^*$（golden ticket）替代随机采样。

### Golden Ticket 搜索（Algorithm 1: Random Search）
1. 从 $N(0, I)$ 采样 $n$ 个候选噪声向量（lottery tickets）$\{w_i\}_{i=1}^n$
2. 对每个 ticket $w_i$，在一组搜索环境 $\mathcal{E}$ 中执行策略 rollout，计算平均累积折扣奖励 $\bar{R}_i$
3. 选择 $\bar{R}_i$ 最大的 ticket 作为 golden ticket $w^*$

### 关键设计决策
- **不修改策略权重**：预训练策略完全冻结
- **不训练额外网络**：与 DSRL 不同，不需要训练观察条件化的噪声策略
- **观察无关**：golden ticket 是一个固定向量，不随观察变化，因此不受观察分布偏移影响
- **仅要求**：(1) 能注入初始噪声到策略中；(2) 能计算（稀疏）任务奖励

### 超参数
- 主要超参数：ticket 数量 $n$
- 搜索预算权衡：ticket 数量 vs 搜索环境数量
- 最小实验：franka sim 约100个ticket × 50环境；最大：robomimic 5000个ticket × 100环境
- 真实世界：6-10个ticket × 5-25个episode即可找到golden ticket

### 验证方法
使用 held-out 环境评估，避免搜索/测试污染。如果 ticket 在 held-out 环境上表现差于搜索环境，说明过拟合。


## Experiments

### 仿真 Benchmark 结果

| Benchmark | 模型 | 观察输入 | 任务数 | Golden Ticket 提升 | 最大提升 |
|-----------|------|---------|--------|-------------------|---------|
| franka sim | Flow Matching MLP | 低维状态 | 1 | 38.5% → 96% | +57.5% 绝对 |
| robomimic | DPPO (Diffusion) | 低维状态 | 4 | 3/4任务提升 | can: 42.8% → 80.8% (+38%) |
| LIBERO | SmolVLA | RGB + 状态 + 语言 | 30 (3 suites × 10) | 全部3个suite提升 | SPATIAL +13%, GOAL +12.8%, OBJECT +8% |
| DexMimicGen | Diffusion (U-Net) | RGB + 状态 | 5 (双臂) | 4/5任务提升 | Box Cleanup: 87.6% → 97.8% |

### 真实世界实验结果

| 任务 | 策略类型 | 基线成功率 | Golden Ticket 成功率 | 相对提升 | 搜索 episode 数 |
|------|---------|-----------|-------------------|---------|---------------|
| Franka 方块抓取 | RGB Diffusion | 80% | 98% | +18% | 150 |
| 香蕉抓取 | Pointcloud Diffusion | 50% (跨位置平均) | 68% | +18% | 50 |
| 杯子推动 | Pointcloud Diffusion | 40% | 100% | +60% | 50 |

### 与 DSRL 对比（DexMimicGen, 5任务）
- DDIM-8步：Golden Ticket **优于** DSRL
- DDIM-2步：DSRL 略优于 Golden Ticket，但 Golden Ticket 仍优于基线
- Golden Ticket 优势：不需要训练新网络，复杂度和计算量更低

### 跨任务迁移（LIBERO）
- LIBERO-GOAL：ticket #03c2 在3个任务上达100%成功率（基线仅1个任务100%）
- LIBERO-OBJECT：ticket #015a 在5个任务上达100%（基线仅2个）
- LIBERO-SPATIAL：ticket #a68f 在3个任务上优于基线（≥90%成功率）
- 注意：跨整个任务 suite 的平均性能不一定优于基线，因为某些任务需要不同的行为模式

### Pareto 前沿（franka sim）
400个 ticket 在"成功率 vs 速度"双目标下自然形成 Pareto 前沿，成功率从≈5%到近100%，速度从≈180步到220步。这提供了一种无需设计多个奖励函数即可在线切换行为的方法。

### DDIM 步数影响
- DDIM-2步的 Golden Ticket 提升幅度大于 DDIM-8步
- 部分任务中 DDIM-2 Golden Ticket 甚至超过 DDIM-8基线（如 robomimic lift 和 can）


## Limitations

1. **确定性策略**：用固定噪声替换后策略变为确定性（除非使用随机反向采样），可通过混合注入高斯噪声缓解
2. **并非所有任务都有效**：43个任务中有5个未找到优于基线的 golden ticket（如 robomimic square、DexMimicGen Threading）
3. **无离线评估指标**：无法在不与环境交互的情况下预测哪个 noise 是 golden ticket
4. **跨任务平均性能下降**：单个 golden ticket 可能提升特定任务但降低 suite 平均性能
5. **空间泛化有限**：真实世界实验中 golden ticket 在训练位置的凸包内泛化较好，但远距离位置表现可能下降
6. **搜索效率**：仅使用随机搜索，未来可结合 RL 方法提升


## Key Takeaways

### 对扩散策略理解的启示
1. **初始噪声携带行为信息**：扩散/Flow Matching策略的初始噪声不仅是随机种子，它直接决定了生成动作的模式，不同噪声向量引导策略产生截然不同的行为
2. **预训练策略存在未激活的能力**：即使在冻结权重的情况下，仅通过选择合适的噪声向量就能大幅提升性能，说明策略网络内部已编码了高质量行为模式
3. **低维噪声空间的有效性**：动作 chunk 的噪声维度（如 SmolVLA 的1600维）远低于图像生成的噪声维度（如49152维），但随机搜索仍能找到有效的 golden ticket

### 对机器人操控的启示
4. **部署时零成本优化**：一旦找到 golden ticket，推理时没有任何额外计算开销
5. **多目标行为切换**：不同 golden ticket 构成的 Pareto 前沿提供了一种简单的在线行为切换机制
6. **适用于双臂任务**：DexMimicGen 实验证实 golden ticket 在双臂操控中有效

### 与我们研究方向的关联
7. **DLO 操控中的应用潜力**：如果使用扩散策略进行 DLO 操控，golden ticket 方法可能直接适用——搜索一个能稳定产生有效 DLO 操作轨迹的初始噪声
8. **Sim-to-Real 辅助**：在 Sim-to-Real 迁移后，通过 golden ticket 搜索可以快速适配真实环境，且搜索成本极低（50-150 episode）
9. **VLA 上的应用**：方法已验证在 SmolVLA 上有效，对其他 VLA（如 π₀）理论上同样适用

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[patil|Patil, Omkar]]
- [[schmeckpeper-karl|Schmeckpeper, Karl]]
