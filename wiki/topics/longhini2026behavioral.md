---
title: "Behavioral mode discovery for fine-tuning multimodal generative policies"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。"
authors: "Longhini, Alberta; Emukpere, David; Renders, Jean-Michel; Kim, Seungsu"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "UM594DM5"
---
## 摘要

We address the problem of fine-tuning pre-trained generative policies with reinforcement learning（强化学习） (RL) while preserving the multimodality of their action distributions. Existing methods for RL fine-tuning of generative policies (e.g., diffusion（扩散） policies) improve task performance but often collapse diverse behaviors into a single reward（奖励）-maximizing mode. To mitigate this issue, we propose an unsupervised mode discovery framework that uncovers latent behavioral modes within generative policies. The discovered modes enable the use of mutual information as an intrinsic reward（奖励）, regularizing RL fine-tuning to enhance task success while maintaining behavioral diversity. Experiments on robotic manipulation（机器人操控） tasks demonstrate that our method consistently outperforms conventional fine-tuning approaches, achieving higher success rates and preserving richer multimodal（多模态） action distributions.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. 提出基于互信息的代理指标 I(W; S)，用于度量噪声条件生成策略的多模态性，证明了多模态性蕴含 I(W; A|S) > 0（附录 D 给出严格证明）
2. 设计无监督模式发现机制 BMD：通过对 steering policy 引入潜变量 z ∈ Z 的重参数化，从冻结的预训练策略潜在噪声空间中提取轨迹级行为模式
3. 提出模式保持的 RLFT 目标：以变分下界作为内在奖励正则化微调，防止模式坍缩；采用两阶段训练（先模式发现，再任务微调）+ 短到长轨迹课程学习
4. 在 5 个机器人任务（2D 导航、ManiSkill Reach/Lift/Avoid、ANYmal 运动、Franka Kitchen）上验证，证明 BMD 在保持或提升任务成功率的同时保留多模态性
## 结构化提取

- Problem: RL微调预训练生成式策略时保持多模态行为分布
- Method: BMD——无监督模式发现 + 互信息内在奖励正则化
- Tasks: 2D导航、机械臂操控（Reach/Lift/Avoid）、四足运动（ANYmal）、顺序操控（Franka Kitchen）
- Sensors: 关节位置/速度、末端执行器位姿、目标/物体位姿、本体感受观测
- Robot Setup: Franka Emika Panda（6-DoF EE控制）、ANYmal 四足机器人（12关节控制）
- Metrics: SR（成功率）、SRM（模式加权成功率）、mc@0.8（模式覆盖率）、H(π)（模式熵）
- Limitations: λ调参敏感；推理模型不稳定；任务级模式提取，不适合多任务异构数据；离散潜变量偶发冗余映射；未验证真实机器人
- Evidence Notes:

  - 互信息随模式数单调递增（Table 1，1/2/4-mode：0.00/0.58/1.06）
  - 标准微调在奖励偏移时系统性坍缩（Tables 2-3, G2场景 DPPO 从4模式坍至1）
  - BMD在5个任务中一致性地保持更多模式（Tables 5-7）
  - RES[BMD]移除steering后退化最小，模式内化（Table 10）
  - 跨种子模式分配一致但编码顺序不固定（Tables 11-12, NMI=1.0）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv 全文，含附录 A-J，共约 25 页)
- Evidence Coverage: high（方法细节、实验表格、消融实验、附录完整）
- Confidence: high
- Summary: 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。


## Problem

预训练的生成式策略（如 diffusion policy）通过模仿学习能捕获多模态行为分布，但 RL 微调（RLFT）往往会将这些多样行为坍缩为单一奖励最大化模式。核心问题：如何在 RL 微调预训练生成式策略时保持从演示中习得的多模态性？


## Method

### 核心思想
预训练的 diffusion policy πθ(a|s,w) 的噪声变量 w 空间隐式编码了多种行为模式，但 w 是逐步采样的，无法直接组织为轨迹级模式。BMD 通过引入 steering policy πψ_W(w|s,z) 用潜变量 z 来组织 w 空间。

### 三组件架构
1. **多模态性度量**：I(W; S) > 0 作为多模态性的必要条件，通过 I(Z; S) 的变分下界近似
2. **模式发现**：
   - Latent reparameterization：πψ_W(w|s,z)，z 为离散分类变量
   - 推理模型 qϕ(z|s) 估计后验，与 steering policy 联合训练
   - 变分下界：I(Z;S) ≥ E_{p(s,z)}[log qϕ(z|s) - log p(z)]（Eq. 1）
3. **正则化微调**：
   - 增强奖励：r_total(s,z) = r_env(s,a) + λ(log qϕ(z|s) - log p(z))（Eq. 2）
   - 两阶段：E_wp 轮纯内在奖励模式发现 → 之后加入环境奖励
   - 短到长课程学习：从短轨迹 H_0 逐步增加到最大 T

### 实现细节
- 预训练策略：标准 diffusion BC，MLP backbone (512,512,512)，20 步去噪训练，2 步 DDIM 推理
- Steering policy：Gaussian MLP (256,256,256)，离散潜变量 z ∈ {0,...,K-1}，K ∈ {4,8,16}
- 推理模型：分类分类器 MLP (256,256,256)，Mish 激活，输入注入高斯噪声防过拟合
- RL 算法：PPO，clip ε=0.2，GAE λ=0.95，γ=0.99，lr=3e-4

### 正交性
BMD 可与 DPPO（直接微调）、Policy Decorator（残差策略）、DSRL（steering）三种微调策略组合，记为 X[BMD]。


## Experiments

### 环境
| 任务 | 机器人 | 模式数 | 状态空间 | 动作空间 | 最大步数 |
|------|--------|--------|----------|----------|----------|
| 2D Gaussian Mixture | 点智能体 | 4 | 位置 (x,y) | 位移 (Δx,Δy) | - |
| Reach | Franka Panda | 2 | 关节+末端+目标 | 6-DoF EE delta pose | 100 |
| Lift | Franka Panda | 2 | 关节+末端+物体 | 6-DoF EE delta pose | 200 |
| Avoid | Franka Panda | 24 | 末端位置 | (Δx,Δy) 速度 | 300 |
| ANYmal | ANYmal 四足 | 4 | 关节+基座+目标 | 12 关节增量 | 200 |
| Franka Kitchen | Franka Panda | ~24 | 关节+末端+物体 | 9 维动作 | 280 |

### 评价指标
- SR：总体成功率
- SRM：模式加权成功率 = (1/K)ΣSR_i，防止单模式退化
- mc@τ=0.8：成功率 ≥ 0.8 的模式比例
- H(π)：模式分布熵，衡量多模态使用均衡度
- 所有指标基于 1024 评估 episodes，3 个随机种子取均值±标准差

### 主要结果
1. **互信息有效性验证**（Table 1）：M 值随模式数单调递增（1-mode: 0.00, 2-mode: 0.58, 4-mode: 1.06）
2. **2D Gaussian**（Tables 2-3）：标准微调在奖励偏移时坍缩到更少模式；BMD 变体（RES[BMD]、DPPO[BMD]）保持全模式覆盖
3. **Manipulation**（Tables 4-5）：
   - Reach：所有方法表现良好，BMD 不牺牲性能
   - Lift：BMD 使策略保留两种解决方案模式
   - Avoid（24 模式）：标准微调消除多模态性，BMD 保留部分模式子集
4. **ANYmal**（Table 6）：BMD 保持全部 4 个模式
5. **Franka Kitchen**（Table 7）：所有 baseline 坞缩到单一序列，BMD 恢复多种成功序列

### 消融实验
- **λ 正则化系数**（Fig. 11）：λ 过大导致内在奖励主导，任务成功率下降
- **关键设计选择**（Table 9）：禁用推理模型微调灾难性下降；省略预训练或课程学习也负向影响
- **|Z| 维度**（Table 8）：|Z|=4 不够捕获全部模式；|Z|=8,16 更好但过大效率降低
- **移除 steering policy**（Table 10）：RES[BMD] 移除后退化最小，说明残差更新将模式内化到策略中
- **模式稳定性**（Figs. 12-13, Tables 11-12）：跨种子 NMI=1.00, ARI=1.00（seed 1 vs 2），但潜变量编码顺序不固定
- **噪声和动力学扰动**（Tables 13-14）：观测噪声下保持多模态；动力学偏移（锁定一个关节）仍保留 2/4 模式


## Limitations

1. 内在奖励正则化需仔细调参 λ，过大会降低任务成功率
2. 推理模型在微调期间需要追踪策略变化的状态分布，可能不稳定
3. 当前 BMD 是任务级模式提取器，扩展到大规模异构多任务数据集需要更丰富的潜变量参数化（如层次化潜空间）
4. 离散潜变量 z 使用分类分布，有时不同 z 映射到相同环境模式（互信息对微小状态变化敏感）
5. 未探索连续或混合潜空间
6. 假设预训练策略已编码多模态性；若预训练策略本身是单模态的，BMD 无法发现不存在的模式


## Key Takeaways

1. **RL 微调扩散策略的模式坍缩问题**：这是一个被忽视但重要的问题。标准微调（DPPO、DSRL）在奖励偏移时都会丢失模式，特别是在 Avoid（24 模式）和 Kitchen（组合模式）中表现明显
2. **Steering policy 作为模式提取器**：不修改预训练策略权重，仅通过控制噪声输入发现模式——这与 Sim-to-Real 场景中保持预训练行为不变的需求一致
3. **正交性设计**：BMD 可以叠加到任何现有微调方法上（DPPO[BMD]、RES[BMD]、DSRL[BMD]），这使其具有很强的实用性
4. **对 DLO 操控的启发**：DLO 操控天然存在多模态性（不同抓取策略、不同弯曲路径），BMD 的思路可用于微调 DLO 操控策略时保持多种操控策略
5. **RES[BMD] 移除 steering 后仍保持多模态**：说明正则化可以将模式内化到策略权重中，这对于部署（不需要额外 steering head）有实际意义

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[longhini|Longhini, Alberta]]
