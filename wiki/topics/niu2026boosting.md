---
title: "Boosting vision-language-action finetuning with feasible action neighborhood prior"
tags: [manipulation, imitation, VLM, DLO]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出Feasible Action Neighborhood (FAN)引导的正则化方法，用高斯先验约束VLA策略分布形状，在SFT和RFT（PPO）两种微调范式中均显著提升样本效率、成功率及OOD泛化能力。"
authors: "Niu, Haochen; Zhang, Kanyu; Yin, Shuyu; Guo, Qinghai; Liu, Peilin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "7XSPEKRV"
---
## 摘要

In real-world robotic manipulation（机器人操控）, states typically admit a neighborhood of near-equivalent actions. That is, for each state, there exist a feasible action neighborhood (FAN) rather than a single correct action, within which motions yield indistinguishable progress. However, prevalent VLA training methodologies are directly inherited from linguistic settings and do not exploit the FAN property, thus leading to poor generalization and low sample efficiency. To address this limitation, we introduce a FAN-guided regularizer that shapes the model's output distribution to align with the geometry of FAN. Concretely, we introduce a Gaussian prior that promotes locally smooth and unimodal predictions around the preferred direction and magnitude. In extensive experiments across both reinforced finetuning (RFT) and supervised finetuning (SFT), our method achieves significant improvement in sample efficiency, and success rate in both in-distribution and out-of-distribution (OOD) scenarios. By aligning with the intrinsic action tolerance of physical manipulation（操控）, FAN-guided regularization provides a principled and practical method for sample-efficient, and generalizable VLA adaptation.

## 中文简述

提出基于模仿学习的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、可变形物体操控

## 关键贡献

1. **形式化FAN概念**：定义了Feasible Action Neighborhood (FAN)来刻画物理动作的局部容差结构，揭示了标准语言式VLA训练与物理动作几何之间的本质错配。
2. **FAN引导正则化器**：提出一种适用于SFT和RFT的正则化项，通过KL散度引导策略分布逼近目标高斯分布，保持VLA模型的离散化和自回归特性不变。
3. **理论分析**：证明FAN-PPO的闭式最优策略是前策略、目标高斯和Q值的几何插值（Proposition 1），揭示了正则化的内在机制。
4. **广泛实验验证**：在ManiSkill和LIBERO基准上，覆盖SFT/RFT、OpenVLA/OpenVLA-OFT两种backbone、15种OOD扰动类型，以及真实世界JAKA机器人实验，一致证明方法有效性。
## 结构化提取

- **Problem**: VLA微调继承了语言模型的训练范式，忽略了物理动作的内在容差（FAN），导致SFT过拟合、RFT样本效率低。
- **Method**: FAN引导的高斯正则化器，通过KL散度约束策略分布形状，适用于SFT（自适应协方差）和RFT/PPO（固定协方差）。
- **Tasks**: pick-and-place（ManiSkill 25种变体）、桌面操控（LIBERO-Spatial 10种任务）、真实世界物体放置（4种任务）。
- **Sensors**: 第三人称RGB相机（224×224），OpenVLA-OFT额外使用腕部相机和本体感受信息。
- **Robot Setup**: ManiSkill仿真（默认机器人），LIBERO仿真（Franka Panda），真实世界JAKA 7-DoF机械臂+Intel RealSense D455。
- **Metrics**: 成功率（%），OOD泛化率，样本效率（达到目标成功率的训练步数）。
- **Limitations**: 超参数需要手动调优；未在复杂操控（DLO、双臂）上验证；固定$\sigma$是FAN大小的近似。
- **Evidence Notes**:

  - SFT: FAN-SFT在ManiSkill上ID提升+11.7%，OOD平均+5.2%（Table 1/8），15种OOD任务中14项正向提升。
  - RFT: FAN-PPO在OpenVLA上OOD平均+6.2%，OpenVLA-OFT上+7.9%（Table 2/14），样本效率提升约3倍（Fig. 7）。
  - LIBERO: OpenVLA-OFT从95.2%提升到98.8%（Table 10）。
  - 真实世界: Task-3（机械臂姿态扰动）从7/30提升到17/30（Table 3）。
  - 参数敏感性: $\alpha \in [0.001, 0.1]$均正向，$\alpha=0.05$最优（Table 11）。
  - Label smoothing对比: FAN全面优于label smoothing（Table 12）。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（正文7节+完整附录含ablation、参数敏感性、真实世界实验）
- Confidence: high
- Summary: 提出Feasible Action Neighborhood (FAN)引导的正则化方法，用高斯先验约束VLA策略分布形状，在SFT和RFT（PPO）两种微调范式中均显著提升样本效率、成功率及OOD泛化能力。

## Problem

VLA模型的微调方法（SFT和RFT）直接继承了语言模型的训练范式（one-hot交叉熵或PPO/GRPO），忽略了物理操控动作的内在容差特性：对于任意状态，存在一个"可行动作邻域"(FAN)而非单一正确动作，邻域内的动作产生不可区分的任务进展。这种范式错配导致SFT产生过拟合的"尖峰"分布（泛化差），RFT则需要大量探索才能隐式发现FAN结构（样本效率低）。

## Method

### 核心思想

利用FAN的三个关键性质（单峰性、平滑性、局部连续性），将策略分布引导为高斯形状。正则化项定义为策略分布与目标高斯之间的KL散度：

$$\mathcal{L}_{\text{FAN}} = \mathbb{E}_s[D_{\text{KL}}(\pi(\cdot|s) \| \mathcal{N}(\cdot|\mu(s), \Sigma(s)))]$$

其中均值$\mu(s)$取策略自身预测的最优动作（argmax），协方差控制FAN的大小。

### FAN-SFT

在SFT损失上加入正则化项：
- 协方差矩阵自适应：$\Sigma(s) = \text{diag}(\sum_{a \in A} \pi(a|s,l)(a - \mu(s))^2)$
- 正则化系数$\alpha=0.05$（ManiSkill）、$0.01$（LIBERO）
- 无需修改模型架构或自回归解码方案

### FAN-PPO

在trust-region优化目标上加入FAN正则化：
- 使用固定协方差$\Sigma = \sigma^2 I$以保证训练稳定性（$\sigma=0.3$ for OpenVLA, $0.2$ for OpenVLA-OFT）
- 正则化系数$\alpha=1.0$（OpenVLA）、$0.1$（OpenVLA-OFT）
- 最优策略的闭式解：$\pi_{t+1}(a|s,l) \propto \mathcal{N}(a|\mu(s),\Sigma)^{\alpha/(\alpha+\beta^*)} \pi_t(a|s,l)^{\beta^*/(\alpha+\beta^*)} \exp(Q^{\pi_t}(s,a,l)/(\alpha+\beta^*))$

### 关键区别
- FAN正则化 ≠ 熵正则化：熵正则化是未结构化的探索促进，FAN是受物理容差指导的结构化先验。
- FAN正则化 > label smoothing：论文对比表明label smoothing的提升有限且不稳定，FAN更有效。

## Experiments

### 数据集/Benchmark
- **ManiSkill**: PutOnPlateInScene25Main-v3，25种pick-and-place操控任务，16K SFT数据
- **LIBERO**: LIBERO-Spatial suite，10个任务，每任务50条人遥操作演示
- **真实世界**: JAKA 7-DoF机械臂，150条演示，4个评估任务

### 主要结果

#### SFT结果（Table 1/8）
| 方法 | In-Dist | Vision OOD | Semantic OOD | Execution OOD | OOD Avg |
|------|---------|------------|-------------|---------------|---------|
| OpenVLA+SFT | 78.1 | 76.6 | 57.4 | 40.4 | 58.1 |
| OpenVLA+FAN-SFT | **89.8** | **81.7** | **63.5** | **44.8** | **63.3** |
| △提升 | +11.7 | +5.1 | +6.1 | +4.4 | +5.2 |

#### RFT结果（Table 2）
| 方法 | In-Dist | OOD Avg |
|------|---------|---------|
| OpenVLA+PPO | 95.9 | 81.9 |
| OpenVLA+FAN-PPO | **97.4** | **88.1** (+6.2) |
| OpenVLA-OFT+PPO | 92.3 | 63.3 |
| OpenVLA-OFT+FAN-PPO | **97.3** | **71.2** (+7.9) |

#### 样本效率
FAN-PPO在OpenVLA上仅需约1/3训练步数即达到90%成功率（Fig. 7）。

#### LIBERO结果
- OpenVLA: 84.7% → 87.2%；OpenVLA-OFT: 95.2% → 98.8%
- 空间扰动下FAN-SFT显著更强（Fig. 4）

#### 真实世界（Table 3）
| 方法 | Task-1 | Task-2 | Task-3 | Task-4 |
|------|--------|--------|--------|--------|
| OpenVLA | 19/30 | 7/30 | 7/30 | 1/30 |
| +FAN-SFT | **22/30** | **12/30** | **17/30** | **7/30** |

### 消融实验
- **参数敏感性（Table 11）**：$\alpha$在[1e-3, 0.1]范围均有正向效果，$\alpha=0.05$最优；过大（>0.1）会损害训练。
- **Label smoothing对比（Table 12）**：FAN全面优于label smoothing。
- **数据规模影响（Fig. 3）**：在多种数据规模下FAN-SFT一致优于基线。
- **RFT参数敏感性**：$\sigma$和$\alpha$的影响在附录中讨论。

## Limitations

1. **超参数选择**：需要为不同backbone调整$\sigma$和$\alpha$（如OpenVLA用$\sigma=0.3, \alpha=1.0$，OpenVLA-OFT用$\sigma=0.2, \alpha=0.1$），缺乏自适应设置机制。
2. **FAN的精确大小未知**：实际FAN的几何结构依赖于具体任务和物理系统，论文用固定$\sigma$近似，未讨论如何从数据中估计真实FAN。
3. **任务类型局限**：实验主要涉及pick-and-place类任务，未在更复杂的DLO操控、双臂协作等场景验证。
4. **连续动作表示的适用性**：方法针对离散化action token设计，对flow matching等连续动作表示（如π₀）的适配未讨论。
5. **计算开销**：FAN正则化需要在每个动作维度计算KL散度，对于高维动作空间可能增加计算负担。

## Key Takeaways

1. **动作容差是VLA训练的关键insight**：物理操控动作不是"一对一"而是"一对多"，利用这一先验可以正则化策略分布。
2. **策略分布形状与泛化性能强相关**：尖峰分布→过拟合→泛化差；平滑高斯分布→鲁棒FAN→泛化强（Fig. 1的直观展示）。
3. **结构化正则化优于非结构化方法**：FAN > label smoothing，因为FAN利用了动作空间的局部几何结构。
4. **对DLO操控的启示**：DLO操控中动作容差可能更大（绳索形态连续变化），FAN正则化可能特别适合，值得探索。
5. **简单即有效**：不需要修改模型架构，只需加一个KL正则项即可在SFT和RFT中均获得显著提升。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[niu-haochen|Niu, Haochen]]
