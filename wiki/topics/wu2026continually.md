---
title: "Continually evolving skill knowledge in vision language action model"
tags: [manipulation, imitation, VLM, bimanual, planning]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数增长的持续模仿学习，仅需 1% 数据回放即可在 LIBERO 和双臂真实平台上超越 π0.5 等大规模 VLA 基线。"
authors: "Wu, Yuxuan; Wang, Guangming; Yang, Zhiheng; Yao, Maoqing; Sheil, Brian et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PK97IPJP"
---
## 摘要

Vision-language-action (VLA) models show promising knowledge accumulation ability from pretraining（预训练）, yet continual learning in VLA remains challenging, especially for efficient adaptation. Existing continual imitation learning（模仿学习） (CIL) methods often rely on additional parameters or external modules, limiting scalability for large VLA models. We propose Stellar VLA, a knowledge-driven CIL framework without increasing network parameters.Two progressively extended variants are designed: T-Stellar for flat task-centric modeling and TS-Stellar for hierarchical task-skill structure.Stellar VLA enables self-evolving knowledge learning by jointly optimizing task representations and a learned knowledge space. We propose a knowledge-guided expert routing mechanism conditioned on knowledge relation and Top-K semantic embeddings, enabling task specialization without increasing model size. Experiments on the LIBERO benchmark show that Stellar VLAs achieve strong performance among both VLA and CIL baselines, using only 1 % data replay. Real-world evaluation on a dual-arm（双臂） platform with distinct embodiment（具身） and scene configurations validates effective knowledge transfer. TS-Stellar excels in hierarchical manipulation（操控）, and visualizations reveal robust knowledge retention and task discovery.Project Website: https://stellarvla.github.io/

## 中文简述

提出基于模仿学习的双臂方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、双臂操控、运动规划

## 关键贡献

1. **Dirichlet Process 知识空间**：提出基于 DPMM 的任务中心知识空间（T-Stellar）和基于 HDP 的层次化任务-技能知识空间（TS-Stellar），无需预定义聚类数量，支持知识自动生长。
2. **自进化学习机制**：VAE 编码的任务表征与 DP 知识空间通过 KL 正则项联合优化，交替迭代使表征和知识聚类相互促进。
3. **知识引导的 MoE 路由**：设计 Knowledge Relation Embedding（连续距离加权）和 Top-K Semantic Embedding（离散语义聚合）两种知识嵌入，替代 MoDE 的纯噪声级路由，实现任务特化的专家分配。
4. **极低回放的强性能**：在 LIBERO（10/10/30 任务）和真实双臂（7 任务）上，用 1% 数据回放和 ~1B 参数模型超越 π0.5（3.4B）、UniVLA（7.55B）等大规模基线。
## 结构化提取

- **Problem**: VLA 模型在持续模仿学习中如何不增加参数、仅用极少数据回放实现有效的任务知识积累和抗遗忘
- **Method**: 基于 Dirichlet Process 的非参数知识空间（DPMM/HDP）+ VAE 自进化任务表征 + 知识引导 MoE 路由
- **Tasks**: LIBERO-goal（10 任务）、LIBERO-long（10 长时序任务）、LIBERO-30*（30 任务）、真实双臂 7 任务（抓取、交接、双臂协同等）
- **Sensors**: 头部相机（224×224 或 240×320）、腕部相机（112×112 或 120×160）、本体感受（关节角度 + 夹爪状态）
- **Robot Setup**: 仿真：单臂 Franka Panda（7-DoF）；真实：双臂 AGIBOT G1（每臂 7-DoF 绝对关节位置 + 2 维夹爪）
- **Metrics**: FWT（前向迁移）、NBT（负向后向迁移/遗忘）、AUC（成功率曲线下面积）、Final SR（最终平均成功率）
- **Limitations**: 小型 VLM 容量限制；大规模预训练下简单任务退步；早期学习不稳定；行为过拟合风险；DP 超参数固定
- **Evidence Notes**: 全文已读。仿真实验有标准差（3 seed），真实实验 10 trials。消融实验覆盖 VAE、知识空间、路由组件三个维度。计算开销和存储分析完整。任务顺序鲁棒性、DP 超参数消融均有提供。可视化支持知识空间演化分析。
## 本地引用关系

- [[kim2024openvla]]
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML version, all sections including appendices read)
- Evidence Coverage: comprehensive (method, experiments on LIBERO simulation + real-world dual-arm, ablations, visualizations, limitations)
- Confidence: high
- Summary: 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数增长的持续模仿学习，仅需 1% 数据回放即可在 LIBERO 和双臂真实平台上超越 π0.5 等大规模 VLA 基线。


## Problem

VLA 模型在持续学习（Continual Imitation Learning, CIL）中面临两个核心矛盾：
1. **灾难性遗忘**：学习新任务时旧任务性能退化，现有 CIL 方法（adapter/skill expansion）需要增加参数或外部模块，在大规模 VLA 上可扩展性差。
2. **任务知识利用不足**：现有方法未能有效建模任务间关系来指导策略特化，单纯数据回放在小比例（如 1%）下不足以维持性能。

关键约束：不增加网络参数、仅用极少数据回放（1%）实现有效持续学习。


## Method

### 整体架构
Stellar VLA 由三部分组成：
- **Vision-Language Encoder**：FiLM-ResNet50 + CLIP ViT-B/32，将图像和语言指令编码为 1024 维 token
- **Task-Centric VAE**：MLP encoder 将 VL 特征映射到 10 维高斯潜空间 z，轻量 MLP decoder 重建 VL embedding
- **Diffusion-based MoE Action Head**：12 层 Transformer，4 个专家，Top-2 路由，基于 EDM 框架的去噪

### 3.1 CIL 问题设定
- 按序学习任务流 {T_j}，每个任务 N 条专家演示
- 使用 Experience Replay (ER)，q% 数据存入缓冲区 B
- 本工作 q=1%

### 3.2 Dirichlet Process 知识空间
- **T-Stellar (DPMM)**：每个任务的潜表征 z_j ~ F_task(θ_j)，θ_j ~ G，G ~ DP(α, G_0)。使用 Stick-Breaking Process 生成无限混合权重，Normal-Wishart 基分布保证每个组件是多元高斯。
- **TS-Stellar (HDP)**：层次化建模 z_ji ~ F_skill(θ_ji)，θ_ji ~ G_j，G_j ~ DP(γ, G)，G ~ DP(α, G_0)。每个任务分布 G_j 共享全局技能集合 G，技能参数 θ_i^skill = (μ, σ)。任务级参数 θ_j^task 由其技能组件聚合得到。

### 3.3 自进化学习
- VAE 学习任务表征 z，KL 项 L_KL = Σ_k p_jk * KL(N(z|μ_j,σ_j) || N(μ_k,σ_k))，其中 p_jk 是 z 分配给聚类 k 的后验概率
- TS-Stellar 的 KL 项同时正则化任务级和技能级潜变量
- 每 N_dp 步从知识空间缓冲区 B_know 采样 K_know 个样本，用 Memoized Variational Bayes (memoVB) 更新 DP 参数 Θ
- B_know 与 ER 缓冲区独立，每任务后清空，无额外全局存储开销

### 3.4 知识引导专家路由
- **Knowledge Relation Embedding** f_R = Σ_k p_k |z - μ_k|，加权距离度量 z 与各聚类中心的关联
- **Top-K Semantic Embedding** f_S = Σ_{k∈TopK} p_k * Embed(k)，聚合最近 K 个聚类的可学习嵌入
- 路由输入 f_know = [z || f_R || f_S]，与 e_lang、e_noise 拼接后送入 Router
- Router 选择 Top-2 专家处理所有 token，平衡参数共享与特化

### 训练损失
L_total = β_recon^lang * L_recon^lang + β_recon^obs * L_recon^obs + β_kl * L_kl + L_SM + β_bal * L_bal
- VAE 重建损失 + KL 散度 + Score Matching 去噪损失 + MoE 负载均衡损失


## Experiments

### 仿真实验（LIBERO）
三个 benchmark：LIBERO-goal（10 任务）、LIBERO-long（10 长时序任务）、LIBERO-30*（LIBERO-90 前 30 任务）

**Scratch 设置关键结果（Table 1, VLA 基线对比）：**

| Benchmark | Metric | MoDE | UniVLA | π0 | T-Stellar | TS-Stellar |
|-----------|--------|------|--------|-----|-----------|------------|
| LIBERO-goal | AUC (↑) | 39.7 | 0.4 | 45.5 | **61.7** | **60.7** |
| LIBERO-goal | Final SR | 33.1 | 0.0 | 35.7 | **67.9** | **64.2** |
| LIBERO-long | AUC (↑) | 34.3 | 0.9 | 22.2 | **41.2** | **43.6** |
| LIBERO-long | Final SR | 20.2 | 0.0 | 12.0 | **34.2** | **35.0** |

**Pretrained 设置关键结果（OXE 预训练后）：**

| Benchmark | Metric | MoDE | UniVLA | π0 | π0.5 | T-Stellar | TS-Stellar |
|-----------|--------|------|--------|-----|------|-----------|------------|
| LIBERO-goal | AUC | 46.8 | 35.2 | 55.6 | 55.4 | **57.5** | 47.5 |
| LIBERO-goal | Final SR | 41.6 | 20.5 | 41.1 | 43.8 | **57.0** | 47.7 |
| LIBERO-long | AUC | 32.9 | 43.6 | 35.6 | 29.8 | **48.6** | **51.4** |
| LIBERO-long | Final SR | 19.9 | 17.1 | 24.3 | 21.6 | 32.2 | **39.7** |

**CIL 基线对比：** Stellar VLA 在所有 CIL 基线（ER、SeqLoRA、LoTUS、IsCiL）上全面领先，AUC 在 LIBERO-goal pretrained 上达 66.7（T-Stellar）vs 60.9（最好 CIL 基线 ER）。

### 真实世界实验（双臂 AGIBOT G1）
7 个任务，包含单臂和双臂操作（抓取、交接、双臂协同等）

| Metric | ER | MoDE | UniVLA | π0 | π0.5 | T-Stellar | TS-Stellar |
|--------|-----|------|--------|-----|------|-----------|------------|
| AUC (↑) | 79.9 | 13.0 | 43.6 | 72.6 | 75.6 | **89.6** | **93.4** |
| Final SR | 70.0 | 10.0 | 21.4 | 57.1 | 72.9 | **84.3** | **90.0** |
| NBT (↓) | 21.9 | 3.2 | 37.1 | 34.6 | 25.8 | **12.4** | **7.4** |

TS-Stellar 在所有指标上均为最优，Final SR 90.0%，NBT 仅 7.4%（遗忘极低）。

### 消融实验（Table 4, scratch LIBERO-long）
- **w/o VAE**（即纯 ER）：FWT 70.8, AUC 31.0, Final SR 18.9
- **w/o KS**（标准高斯替代 DP）：FWT 74.5, AUC 35.3, Final SR 23.0
- **T-Stellar（完整）**：FWT 76.3, AUC 41.2, Final SR 34.2
- **TS-Stellar（完整）**：FWT 75.5, AUC 43.6, Final SR 35.0
- 知识引导路由消融：去掉 f_R 或 f_S 均导致 AUC 和 Final SR 下降，两者互补

### 计算开销
- 模型参数：0.98B（MoDE 0.89B，π0.5 3.40B，UniVLA 7.55B）
- 推理时间：27.2ms（MoDE 26.4ms），知识 token 计算仅 0.1ms
- 训练时间：16.22h（MoDE 14.65h），知识空间更新仅增加 ~2%

### 额外分析
- 任务顺序鲁棒性：在逆序、随机序和默认序上 AUC 和 Final SR 保持稳定
- 协方差尺度 s_F 消融：过大或过小均降低性能，最优在 1e-5
- 知识空间可视化：T-Stellar 形成清晰任务聚类，TS-Stellar 通过共享技能实现任务间重叠
- 通用性初步测试：在杂乱场景下 Stellar VLA 保持较高成功率


## Limitations

1. **模型容量限制**：~1B 参数的小型 VLM 难以捕捉 subgoal 级别的语言/视觉信息，限制了 few-shot 适应能力。
2. **大规模预训练下的退步**：在 1000+ 异构任务的 OXE 大规模预训练后，简单任务上可能不如从零训练，原因在于 10 维任务知识表征不足以覆盖如此多样的任务。
3. **早期学习不稳定**：TS-Stellar 在持续学习早期阶段性能有波动，知识空间尚未稳定时任务判别力不足。
4. **行为过拟合风险**：通用性测试中成功率集中在训练时常见的物体配置附近。
5. **未探索动态超参数适配**：DP 模型的 concentration 参数 α 等在持续学习过程中固定不变。


## Key Takeaways

1. **非参数贝叶斯 + 策略学习的结合是有效的**：DPMM/HDP 自动发现任务结构，避免了预定义聚类数量的需求，适合持续学习场景中任务数量不断增长的情况。
2. **知识引导的路由比噪声级路由更适合 CIL**：MoDE 的噪声级路由无法区分新旧任务，而知识嵌入能感知任务关系，实现有针对性的专家分配。
3. **模型规模不是持续学习的唯一决定因素**：Stellar VLA（0.98B）在持续学习指标上持续优于 π0.5（3.4B）和 UniVLA（7.55B），说明结构化的知识建模比单纯扩大参数更关键。
4. **层次化建模的优势在复杂操作中更明显**：TS-Stellar 在双臂真实任务上的优势（Final SR 90.0% vs T-Stellar 84.3%）表明任务-技能分解对长时序、多技能组合的操作有实际价值。
5. **与 DLO 操控的关联**：双臂交接操作（Handover Stick/Toy）本质涉及 DLO 的抓取和传递，TS-Stellar 的技能共享机制可迁移到 DLO 操控中的多阶段技能复用场景。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wu-yuxuan|Wu, Yuxuan]]
- [[wang-guangming|Wang, Guangming]]
- [[yao-maoqing|Yao, Maoqing]]
