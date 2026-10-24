---
title: "Discrete Policy: Learning Disentangled Action Space for Multi-Task Robotic Manipulation"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 Discrete Policy，将连续动作空间解耦为离散潜空间用于多任务机器人操控。三步流程：(1) VQ-VAE 编码器将连续动作序列量化为离散码序列（codebook 学习有限原子动作集合）；(2) DDIM 扩散模型在离散潜空间（而非连续动作空间）进行去噪生成；(3) VQ-VAE 解码器将离散码解码回连续动作。关键优势：离散表示天然适合多模态动作分布（不同码代表不同动作模式）、离散去噪比连续去噪更高效、codebook 提供可解释的动作词汇。MT-5 基准 84%，MT-12 基准 66.3%，全面超越 Diffusion Policy（提升 25-32.5%）"
authors: "Wu, Kun; Zhu, Yichen; Li, Jinming; Wen, Junjie; Liu, Ning et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "UHCLSYRQ"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于学习方法的操控方法，具有多任务特点。

**研究方向**: 机器人操控

## 关键贡献

1. 动作空间解耦：VQ-VAE 将连续动作量化为离散码，学习紧凑动作词汇
2. 离散潜空间扩散：DDIM 在离散码空间而非连续动作空间进行去噪
3. Codebook 作为可解释动作词汇：每个码代表一种原子动作模式
4. 多任务优势：离散表示天然缓解多任务干扰
## 结构化提取

- **Problem**: 多任务操控中连续动作空间的多模态分布和任务干扰
- **Method**: Discrete Policy — VQ-VAE 动作量化 + DDIM 离散潜空间扩散 + VQ-VAE 解码
- **Tasks**: MT-5/MT-12 多任务基准 + 真实 Franka/UR5 任务
- **Sensors**: RGB 或 RGB-D 相机
- **Robot Setup**: Franka Emika Panda（单臂）+ UR5（双臂）
- **Metrics**: 任务成功率（MT-5 84%/MT-12 66.3%）
- **Limitations**: 量化误差、固定 codebook、两阶段训练
- **Evidence Notes**: 全文读取，Tables I-III 提供完整多任务对比和消融
## 本地引用关系

- [[chen2025coordinated]]
- [[lee2025diffdagger]]
- [[scheikl620movement]]
- [[wu2025tacdiffusion]]
- [[xia2024cage]]
- [[zhu2024scaling]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-7)
- **Confidence**: high — 全文完整，ICRA 2025，Syracuse University + Beijing Innovation Center，VQ-VAE 将连续动作编码为离散码 + DDIM 在离散潜空间去噪 + 解码器重建动作，MT-5 84%/MT-12 66.3%，Franka 单臂 + UR5 双臂，超越 Diffusion Policy 25-32.5%
- **Summary**: 提出 Discrete Policy，将连续动作空间解耦为离散潜空间用于多任务机器人操控。三步流程：(1) VQ-VAE 编码器将连续动作序列量化为离散码序列（codebook 学习有限原子动作集合）；(2) DDIM 扩散模型在离散潜空间（而非连续动作空间）进行去噪生成；(3) VQ-VAE 解码器将离散码解码回连续动作。关键优势：离散表示天然适合多模态动作分布（不同码代表不同动作模式）、离散去噪比连续去噪更高效、codebook 提供可解释的动作词汇。MT-5 基准 84%，MT-12 基准 66.3%，全面超越 Diffusion Policy（提升 25-32.5%）


## Problem

多任务机器人操控中动作分布高度多模态——同一观察下可能存在多种合理动作。现有扩散策略（Diffusion Policy）在连续动作空间去噪，面临模式坍缩、去噪效率低和多任务干扰等问题。如何设计更好的动作表示和生成方法？


## Method

- **VQ-VAE 动作量化**：
  - 编码器：将连续动作序列 a ∈ R^{T×D} 编码为离散码序列 z ∈ {1,...,K}^T
  - Codebook：K 个可学习码向量（如 K=512）
  - 解码器：将离散码序列解码回连续动作
  - 损失：重建损失 + commitment 损失 + codebook 更新
- **离散潜空间扩散（DDIM）**：
  - 前向过程：对离散码添加分类噪声（而非高斯噪声）
  - 反向过程：DDIM 在离散空间去噪，预测干净离散码
  - 条件输入：图像观察 + 语言指令（可选）
- **训练流程**：
  - 阶段 1：训练 VQ-VAE（动作量化）
  - 阶段 2：冻结 VQ-VAE，训练 DDIM（离散扩散）
  - 阶段 3：推理时 DDIM 生成离散码 → VQ-VAE 解码为动作
- **网络架构**：
  - 视觉编码器：ResNet18 或 ViT
  - VQ-VAE：1D 卷积编码器/解码器
  - DDIM：Transformer 去噪网络


## Experiments

- **多任务基准**（仿真）：
  - MT-5（5 任务）：Discrete Policy 84% vs Diffusion Policy 58.5% (+25.5%)
  - MT-12（12 任务）：Discrete Policy 66.3% vs Diffusion Policy 33.8% (+32.5%)
  - MT-12 上超越所有基线（BC-RNN, ACT, Diffusion Policy）
- **真实机器人验证**：
  - Franka 单臂：4 任务（拾取-放置/堆叠/倒入/抽屉开合）
  - UR5 双臂：2 任务（双侧拾取/传递）
  - 成功率全面优于 Diffusion Policy
- **消融**：
  - Codebook 大小 K：K=512 最优，太小（64）或太大（2048）均下降
  - 离散 vs 连续扩散：离散在各规模任务上均优于连续
  - DDIM 步数：5 步即可达到较好性能（vs Diffusion Policy 100 步）
  - VQ-VAE 重建质量对最终性能影响大


## Limitations

1. VQ-VAE 量化误差导致动作精度损失（特别是精细操控）
2. Codebook 容量固定，大规模任务可能需要更大 K
3. 两阶段训练增加复杂度
4. 仅在桌面操控任务验证，未扩展到导航或移动操控
5. 未与其他离散方法（如 VQ-BeT）进行详细对比


## Key Takeaways

- 离散动作空间优于连续空间处理多模态：VQ-VAE 天然将动作聚类为模式
- 离散扩散比连续扩散更高效：5 步 DDIM vs 100 步连续扩散
- Codebook 提供可解释动作词汇：可视化和分析动作模式
- 多任务场景优势最大：任务越多，离散解耦的增益越显著
- 动作表示设计比网络架构更重要：同一 Transformer 架构，离散表示大幅提升

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[bimanual-manipulation]]

## 相关研究者

- [[wu-kun|Wu, Kun]]
- [[zhu|Zhu, Yichen]]
- [[li|Li, Jinming]]
- [[wen|Wen, Junjie]]
