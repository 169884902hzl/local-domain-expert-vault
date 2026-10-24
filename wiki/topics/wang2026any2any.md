---
title: "Any2Any 3D diffusion models with knowledge transfer: A radiotherapy planning study"
tags: [imitation, RL, diffusion, diffusion-model, planning]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出DiffKT3D框架，将预训练视频扩散模型(Wan 2.1)迁移至放疗3D剂量预测，通过Any2Any条件范式支持7种模态的灵活输入输出组合，并引入基于临床Scorecard的RL后训练(ScardNFT)对齐机构偏好，在GDP-HMM挑战上将MAE从2.07降至1.93。"
authors: "Wang, Yuhan; Li, Zihan; Liu, Han; Arberet, Simon; Kraus, Martin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VA2G5AGS"
---
## 摘要

Voxel-wise dose prediction is a critical yet challenging task in practical radiotherapy (RT) planning, as bespoke models trained from scratch often struggle to generalize across diverse clinical settings. Meanwhile, generative models trained on billion-scale datasets from vision domains have achieved impressive performance. Herein, we propose DiffKT3D, a unified Any2Any 3D diffusion（扩散） framework that leverages prior knowledge from pretrained video diffusion（扩散） models for efficient and clinically meaningful dose prediction. To enable flexible conditioning across multiple clinical modalities (CT, anatomical structures, body, beam settings, etc.), we introduce an Any2Any conditional paradigm utilizing modality-specific embeddings without cross-attention overhead. Further, we design a novel reinforcement learning（强化学习） (RL) post-training mechanism guided by a clinically-informed Scorecard explicitly tailored to institutional treatment preferences. Compared with winner of GDP-HMM challenge, DiffKT3D sets a new state-of-the-art（现有最优方法） in dose prediction by reducing voxel-level MAE from 2.07 to 1.93. In addition, DiffKT3D achieves superior image quality and preference match. These results demonstrate that transferring diffusion（扩散） priors via modality-aware conditioning and clinically aligned RL post-training can provide a robust and generalizable solution for RT planning across various clinical scenarios.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 模仿学习、强化学习、扩散模型、扩散模型、运动规划

## 关键贡献

1. **扩散先验跨域迁移**：首次将预训练视频扩散模型(Wan 2.1)和CT扩散模型(MAISI)适配用于3D剂量预测，证明通用域扩散先验可有效迁移至专业医学生成任务，且性能显著优于从头训练
2. **Any2Any条件范式**：提出模态感知的Any2Any条件生成框架，支持7种模态的任意组合作为输入条件或生成目标，通过模态特定嵌入和角色嵌入(role embedding)实现，无需cross-attention开销
3. **ScardNFT临床对齐**：设计基于临床Scorecard的RL后训练机制，将机构治疗偏好转化为奖励信号，在保持体素级精度的同时显著改善临床偏好对齐
## 结构化提取

- **Problem**: 放疗3D剂量预测——从多模态患者数据(CT、解剖结构、射束配置)生成精确的3D剂量分布，现有模型泛化性差且缺乏临床偏好对齐
- **Method**: DiffKT3D = 预训练视频扩散先验(Wan 2.1 DiT) + Any2Any多模态条件范式(角色嵌入+模态特定patch嵌入+4D RoPE) + v-parameterization + ScardNFT RL后训练(LoRA适配器+临床Scorecard奖励)
- **Tasks**: 放疗剂量预测(3D voxel-wise dose prediction)、跨模态补齐(Any2Any prediction)
- **Sensors**: CT扫描、解剖结构勾画(PTV/OAR masks)、体轮廓(body mask)、射束配置(beam plate + angle plate)
- **Robot Setup**: 不涉及机器人（医学影像任务）
- **Metrics**: MAE(Gy)、临床Scorecard(PTV覆盖+OAR保护综合评分)、PSNR、SSIM、LPIPS、Dice、FID
- **Limitations**: 推理效率(~10s/case)、未整合DVH专用损失、缺乏临床验证、MAISI noise-pred参数化崩溃
- **Evidence Notes**: 完整全文精读，包含主实验(GDP-HMM + REQUITE)、消融实验(7个组件)、扩展基线(ControlNet/2D/LoRA)、统计显著性分析(p<10⁻³)、VAE适配策略对比、参数化对比(x₀/ε/v-pred)
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整（正文+补充材料，含消融实验、统计显著性分析、扩展基线对比）
- Confidence: high
- Summary: 提出DiffKT3D框架，将预训练视频扩散模型(Wan 2.1)迁移至放疗3D剂量预测，通过Any2Any条件范式支持7种模态的灵活输入输出组合，并引入基于临床Scorecard的RL后训练(ScardNFT)对齐机构偏好，在GDP-HMM挑战上将MAE从2.07降至1.93。


## Problem

放疗(RT)计划中的体素级剂量预测(Dose Prediction)是一个关键且具挑战性的任务。现有从头训练的定制模型难以在不同临床场景间泛化。具体问题包括：

1. **数据规模瓶颈**：放射治疗数据通常仅有数百至数千例，远小于视觉领域的十亿级数据集
2. **多模态异构输入**：需要处理CT、PTV、OAR、body mask、beam plate、angle plate、dose等7种异构模态
3. **临床偏好对齐**：不同机构遵循不同的计划协议，需要在PTV覆盖与OAR保护间做复杂权衡
4. **跨域迁移可行性未知**：自然视频/CT预训练的扩散先验能否有效迁移到放疗剂量生成领域


## Method

### 整体架构
DiffKT3D采用VAE-DiT混合架构：
- **编码器**：冻结的3D VAE编码器（来自Wan 2.1）将各模态体数据编码至共享潜空间
- **主干网络**：DiT (Diffusion Transformer) backbone，1.3B参数，初始化自Wan 2.1
- **解码器**：冻结的3D VAE解码器恢复原始分辨率体数据

### 核心设计

**Patchify Head**：每个模态有独立的3D patch embedding，将潜空间网格映射到token序列，保持DiT主干架构不变。

**角色感知条件(Role-aware conditioning)**：
- 二元角色嵌入 `e_role ∈ {e_tar, e_cond}` 标记每个token为目标(target)或条件(condition)
- 条件角色嵌入通过加法调制注入timestep embedding，经共享AdaLayerNorm作用于所有DiT block
- 无需额外的cross-attention或池化模块

**Slot-aware 4D RoPE**：
- 扩展标准3D RoPE，增加slot轴形成4D位置编码
- 维度分配：d = d_S + d_H + d_W + d_D
- Slot轴为每个模态提供独立的旋转相位，空间轴跨slot共享
- 保持统一的全注意力计算，但鼓励结构化的跨slot交互

**v-parameterization**：采用v-预测目标而非噪声预测，提供更好的信噪比平衡：
- v(x₀, ε, t) = α_t·ε - σ_t·x₀
- 在flow-matching框架下比x₀-pred和ε-pred更稳定

### 训练流程（三阶段）
- **阶段A**：Any2Any预训练，均匀目标采样+课程掩码
- **阶段B**：仅剂量目标微调
- **阶段C**：ScardNFT后训练，用LoRA(rank-64)适配器+调制网络

### ScardNFT后训练
- 从临床Scorecard定义标量奖励r_raw，包含DVH指标、平均剂量、环形约束
- 每个患者采样K个候选剂量，计算奖励并转换为最优概率r ∈ [0,1]
- 包含hinge penalty（硬约束）和MAE anchor（防止reward hacking）
- 优化DiffusionNFT风格的双损失：增加高奖励样本似然，惩罚低奖励样本

### 训练配置
- 8×B200 GPU，batch size 1/GPU（有效batch=8）
- Adam优化器，lr=1e-4，100 epochs
- 1000训练步，flow-shift=3.0
- bfloat16混合精度，梯度裁剪0.1
- 输入裁剪：97×128×160 3D ROI


## Experiments

### 数据集
- **GDP-HMM Grand Challenge**：头颈+肺癌，训练2878例，验证356例，测试498例
- **REQUITE**：前列腺癌，训练5100例，测试256例

### 主要结果（GDP-HMM Test）

| 方法 | MAE↓ | Score↑ | PSNR↑ | SSIM↑ | LPIPS↓ |
|------|------|--------|-------|-------|--------|
| Challenge Top1 (Yasin, MedNeXt) | 2.07 | 134.81 | 32.06 | 0.974 | 0.033 |
| Ours (MAISI+Ours) | 1.95 | 135.23 | 32.13 | 0.976 | 0.026 |
| Ours (Conditional DiT) | 2.12 | 134.60 | 32.01 | 0.974 | 0.029 |
| Ours (Any2Any) | **1.93** | 135.36 | 32.60 | 0.978 | 0.023 |
| Ours (Any2Any+NFT) | **1.93** | **137.55** | **32.73** | **0.980** | **0.020** |

### REQUITE前列腺结果

| 方法 | MAE↓ | PSNR↑ | SSIM↑ | LPIPS↓ |
|------|------|-------|-------|--------|
| Top baseline (tyxiong123) | 1.37 | 34.74 | 0.957 | 0.023 |
| Ours (Any2Any) | **1.01** | **36.80** | **0.963** | **0.012** |
| Ours (best-of-n) | **0.97** | **37.09** | **0.965** | **0.011** |

### 关键消融实验
1. **预训练 vs 从头训练**：MAE 2.58 → 2.07（验证集），确认跨域迁移价值
2. **Conditional vs Any2Any**：Any2Any将MAE从2.12降至1.93（测试集）
3. **移除角色嵌入**：MAE退化至2.01
4. **移除全注意力（改因果注意力）**：MAE退化至2.15
5. **移除模态特定patch嵌入**：MAE退化至2.02
6. **移除4D RoPE**：MAE退化至1.96
7. **v-pred vs ε-pred vs x₀-pred**：v-pred最优（10步：1.91 vs 1.93 vs 2.45）
8. **VAE策略**：冻结VAE最优；全VAE微调导致灾难性退化（MAE 2.54）
9. **ScardNFT**：Score从136.22提升至138.17，MAE不变（1.91→1.91）

### 扩展基线对比
- 3D ControlNet：MAE 2.42（多模态异构条件下性能差）
- 2D逐片扩散：MAE 2.14，GPU内存32.4GB（缺乏3D空间一致性）
- LoRA-only：MAE 2.26（全参数微调对弥合域差距至关重要）

### 统计显著性
- MAE改善(2.07→1.93)和Scorecard改善(134.81→137.55)均p < 10⁻³


## Limitations

1. **计算效率**：Wan 1.3B主干+全3D注意力，10步推理约10s/GPU/case，虽远快于优化系统(15-30min)，但仍需改进
2. **训练目标局限**：未整合DVH损失函数和加权MAE等剂量专用损失
3. **临床验证缺失**：尚未在真实临床设置中验证有效性
4. **模型规模**：仅探索了1.3B参数量级，更大/更小模型的scaling behavior未研究
5. **MAISI噪声预测失败**：在冻结VAE解码器下，噪声预测参数化导致性能崩溃(MAE>10)，暴露了特定backbone+参数化的脆弱性


## Key Takeaways

### 对扩散模型设计的启示
1. **预训练扩散先验的跨域迁移是可行的**：即使在自然视频→放疗剂量这样巨大的域差距下，预训练backbone仍显著优于从头训练
2. **Any2Any统一框架优于专用条件化**：将多模态统一在单一扩散空间中联合建模，比拼接式条件化更有效
3. **冻结VAE编码器至关重要**：修改编码器破坏预训练潜空间结构，导致灾难性退化；冻结VAE+微调DiT是最优策略

### 对机器人领域的潜在参考
1. **RL后训练对齐范式可迁移**：将领域专家偏好（临床Scorecard）转化为RL奖励信号进行后训练的思路，可推广至机器人任务偏好对齐
2. **多模态Any2Any设计模式**：异构输入(视觉、语言、状态)的灵活条件化方案对多模态机器人控制有参考价值
3. **角色嵌入+4D RoPE的位置编码策略**：在统一注意力中区分不同信息来源的设计对多传感器融合有启发

### 局限性（对本vault研究方向的适用性）
- 本文属于医学影像/放疗计划领域，与DLO操控、VLM控制等机器人核心方向不直接相关
- 扩散模型用于3D体数据生成（非动作序列生成），技术栈差异较大
- 方法论启发（知识迁移、RL对齐、多模态条件化）可间接参考

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[planning]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[wang-yuhan|Wang, Yuhan]]
- [[li-zihan|Li, Zihan]]
