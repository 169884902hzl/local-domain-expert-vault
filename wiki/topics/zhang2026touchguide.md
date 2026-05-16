---
title: "TouchGuide: Inference-time steering of visuomotor policies via touch guidance"
tags: [manipulation, imitation, diffusion, robot-learning, tactile]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空间级别的视觉-触觉融合；同时提出低成本高精度手持数据采集系统 TacUMI"
authors: "Zhang, Zhemeng; Ma, Jiahua; Yang, Xincheng; Wen, Xin; Zhang, Yuzhi et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CFRKAFIM"
---
## 摘要

Fine-grained and contact-rich（接触丰富） manipulation（操控） remain challenging for robots, largely due to the underutilization of tactile（触觉） feedback. To address this, we introduce TouchGuide, a novel cross-policy visuo-tactile（触觉） fusion paradigm that fuses modalities within a low-dimensional action space. Specifically, TouchGuide operates in two stages to guide a pre-trained diffusion（扩散） or flow-matching visuomotor policy at inference time. First, the policy produces a coarse, visually-plausible action using only visual inputs during early sampling. Second, a task-specific Contact Physical Model (CPM) provides tactile（触觉） guidance to steer and refine the action, ensuring it aligns with realistic physical contact conditions. Trained through contrastive learning on limited expert demonstrations, the CPM provides a tactile（触觉）-informed feasibility score to steer the sampling process toward refined actions that satisfy physical contact constraints. Furthermore, to facilitate TouchGuide training with high-quality and cost-effective data, we introduce TacUMI, a data collection system. TacUMI achieves a favorable trade-off between precision and affordability; by leveraging rigid fingertips, it obtains direct tactile（触觉） feedback, thereby enabling the collection of reliable tactile（触觉） data. Extensive experiments on five challenging contact-rich（接触丰富） tasks, such as shoe lacing and chip handover, show that TouchGuide consistently and significantly outperforms state-of-the-art（现有最优方法） visuo-tactile（触觉） policies.

## 中文简述

提出基于扩散模型的操控方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习、触觉感知

## 关键贡献

1. **TouchGuide 范式**：一种 novel cross-policy 视触觉融合范式，在低维动作空间中通过推理时引导（inference-time steering）融合视觉和触觉模态，无需重训练底层策略
2. **Contact Physical Model (CPM)**：任务特定的触觉物理模型，通过对比学习训练，输出触觉约束下的动作可行性分数，引导去噪/flow-matching 采样过程
3. **TacUMI 数据采集系统**：基于 Vive Tracker 定位的手持式低成本（$720）高精度数据采集系统，刚性指尖提供直接触觉反馈，540g 轻量化
4. **Classifier Guidance 推广到 Flow Matching**：推导了 flow matching 的 classifier guidance 公式，提出 Proposition 1：û_θ(x_t) = u_θ(x_t) - η · t/(1-t) · ∇log p_φ(y|x_t)
## 结构化提取

- Problem: 接触丰富细粒度操控中触觉反馈利用不足，现有视触觉融合方法（特征级/策略级）在动作空间缺乏有效融合
- Method: TouchGuide — 两阶段推理时引导范式；CPM（DINOv2 编码 + Transformer 融合 + 对比学习）；classifier guidance 推广到 flow matching
- Tasks: Shoe Lacing（双臂）、Chip Handover（双臂）、Cucumber Peeling（双臂）、Vase Wiping（单臂）、Lock Opening（单臂）
- Sensors: Xense 触觉传感器（触觉图像 200×350×3 + 力场 20×35×3）；RGB 相机 640×480×3 @30Hz；Vive Tracker 定位
- Robot Setup: Bi-ARX5 双臂机器人 + Flexiv Rizon4 单臂机器人；末端执行器配备刚性指尖夹爪
- Metrics: 成功率（Shoe Lacing, Chip Handover, Lock Opening）；评分 0-1（Cucumber Peeling, Vase Wiping）；平均成功率/评分
- Limitations: CPM 需任务特定训练；Shoe Lacing 任务难度极高（DP 底层 0%）；仅在 5 个任务验证；未探索通用 CPM
- Evidence Notes:

  - Table I 完整报告 5 任务 × 2 底层策略 × 7+ 方法的对比结果
  - Table II 噪声预训练消融：39.17% → 62.50%
  - Table III CPM 模态消融：确认视觉和触觉同等重要
  - Table IV-V 数据采集系统对比和用户研究
  - 附录包含 encoder 对比、引导参数消融、推导细节
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML, 128K chars, 9 chunks, 正文+附录引用均完整)
- Evidence Coverage: 完整覆盖摘要、引言、相关工作、TacUMI 系统、TouchGuide 方法（CPM 架构、contrastive learning、classifier guidance 推广到 flow matching）、实验（5 任务、2 机器人、2 底层策略、6 基线）、消融、系统对比、用户研究、局限性
- Confidence: high
- Summary: 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空间级别的视觉-触觉融合；同时提出低成本高精度手持数据采集系统 TacUMI


## Problem

细粒度接触丰富操控（如系鞋带、薯片传递）对机器人仍然困难。核心问题在于触觉反馈利用不足。现有视触觉策略采用特征级或策略级融合：特征级拼接易受模态主导问题影响，策略级融合难以捕获跨模态相关性。关键问题：如何在低维动作空间中有效融合视觉和触觉信息以提升操控策略性能？


## Method

### 整体架构：两阶段推理时引导
- **阶段一（早期采样）**：预训练的扩散/flow-matching 视觉运动策略 π_θ 仅用视觉输入生成粗粒度视觉可行动作
- **阶段二（后期采样）**：CPM 注入触觉引导，通过可行性分数调整动作使其满足真实物理接触约束

### Contact Physical Model (CPM) 架构
- **编码器**：DINOv2 同时编码触觉图像 T_t 和视觉观测 V_t，得到嵌入 T_t^emb 和 V_t^emb
- **融合**：N 层 Transformer Encoder 融合触觉和视觉嵌入 → L2 Norm → 潜在观测 O_t
- **动作编码**：1D CNN + MLP → L2 Norm → 潜在动作 a_t
- **可行性分数**：s = O_t^⊤ · a_t（余弦相似度）

### 训练策略：对比学习
- **正样本**：同一时间步的 (O_t, a_t) 对
- **负样本**：不同时间步的 (O_{t+Δt}, a_t) 和 (O_t, a_{t+Δt})
- **损失**：标准双向对比损失（对称 CLIP-style），温度参数 τ 可学习
- **噪声增强**：训练时对 GT 动作添加几何分布噪声（diffusion）/线性插值噪声（flow matching），使 CPM 适应推理时的噪声动作空间

### 推理时引导公式
- **Diffusion**：ê_θ = ε_θ(A_t^k, V_t) - η√(1-ᾱ_k) · ∇_{A_t^k} s_φ(V_t, T_t, A_t^k)
- **Flow Matching**：û_θ = u_θ(A_t^k, V_t) - η · k/(1-k) · ∇_{A_t^k} s_φ(V_t, T_t, A_t^k)
- 引导仅在后期 K_TouchGuide 步生效，前期策略自由采样

### TacUMI 系统
- 定位：Vive Tracker + 2 个 Lighthouse 基站（~$720 基础成本）
- 触觉传感器：Xense 传感器，提供触觉图像（200×350×3）和力场（20×35×3）
- 视觉：640×480×3 @ 30Hz
- 板载 RK3576 CPU 实时计算力场
- 重量：540g
- 数据格式：LeRobot 兼容，统一时间戳流


## Experiments

### 实验设置
- **机器人**：Bi-ARX5（双臂）、Flexiv Rizon4（单臂）
- **触觉传感器**：Xense（触觉图像 + 力场两种模态）
- **底层策略**：DP（Diffusion Policy）和 π0.5（Flow Matching）
- **5 个任务**：
  - Shoe Lacing（系鞋带，100 demos，双臂，成功率指标）
  - Chip Handover（薯片传递，50 demos，双臂，成功率指标）
  - Cucumber Peeling（黄瓜削皮，50 demos，双臂，评分 0-1）
  - Vase Wiping（花瓶擦拭，30 demos，单臂，评分 0-1）
  - Lock Opening（开锁，20 demos，单臂，成功率指标）
- **基线**：DP、DP w/ Tactile、SafeDiff、RDP、PolicyConsensus、Tactile Dynamics
- **评估**：每基线 20 trials，适度随机化初始条件

### 主要结果（Table I）
| 方法 | 底层 | Shoe Lace | Chip | Cucum. | Vase | Lock | Average |
|------|------|-----------|------|--------|------|------|---------|
| DP | DP | 0% | 5% | 0.500 | 0.265 | 0% | 16.3% |
| RDP | DP | 0% | 20% | 0.740 | 0.475 | 10% | 30.3% |
| TouchGuide (Force) | DP | 0% | 30% | 0.805 | 0.510 | 15% | 35.3% |
| TouchGuide (Tactile Img.) | DP | 0% | 25% | 0.810 | 0.550 | 20% | 36.2% |
| π0.5 | π0.5 | 20% | 25% | 0.785 | 0.360 | 20% | 35.9% |
| TouchGuide (Force) | π0.5 | 25% | 40% | 0.955 | 0.590 | 30% | 49.9% |
| TouchGuide (Tactile Img.) | π0.5 | **35%** | **60%** | **0.975** | **0.675** | **30%** | **58.0%** |

- TouchGuide 在 DP 上从 16.3% 提升至 36.2%（+19.9%）
- TouchGuide 在 π0.5 上从 35.9% 提升至 58.0%（+22.1%）
- 在所有基线中表现最优

### 消融实验
1. **噪声预训练**（Table II）：无噪声 39.17% → 有噪声 62.50%（+23.33%），显著提升
2. **CPM 模态**（Table III）：无视觉 43.33%，无触觉 43.50%，两者并用 62.50%，视觉和触觉同等重要
3. 引导尺度 η 和引导步数 K_TouchGuide 消融见附录

### 系统对比（Table IV-V）
- TacUMI vs UMI (SLAM) vs VR Teleop（Lock Opening 任务）
- TacUMI：π0.5 成功 20%，TouchGuide 成功 30%
- UMI (SLAM)：π0.5 成功 0%，TouchGuide 成功 5%
- VR Teleop：π0.5 成功 5%，TouchGuide 成功 15%
- 用户研究（5人）：TacUMI 满意度 9.6/10，100% 有效率，13.5 min


## Limitations

1. CPM 仍需任务特定训练，增加训练时间和成本
2. 未来方向：学习更有效的触觉表征，开发非任务特定的通用 CPM
3. Shoe Lacing 任务在 DP 底层策略上所有方法均 0% 成功，说明任务难度极高
4. 仅在 5 个任务上验证，泛化性有待更多任务验证


## Key Takeaways

1. **动作空间融合思路**：不同于特征级拼接或策略级组合，在动作空间中通过 classifier guidance 式的引导实现多模态融合，是一种新的融合范式
2. **推理时引导而非重训练**：CPM 作为外部模块引导已有策略，无需修改底层策略权重，可跨策略（DP、π0.5）、跨机器人、跨触觉模态使用
3. **对比学习训练 CPM**：仅用有限专家示教通过对比学习训练，数据需求低
4. **对 DLO 操控的启示**：触觉引导对细粒度接触操控至关重要；TouchGuide 的推理时引导框架理论上可适配任何需要精确接触控制的场景，包括 DLO 操控中的线缆接触约束
5. **数据采集系统设计**：TacUMI 展示了低成本高精度触觉数据采集的可行性，Vive Tracker 方案优于 SLAM 和 VR 方案

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[tactile-sensing]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhang-zhemeng|Zhang, Zhemeng]]
