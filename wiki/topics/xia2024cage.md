---
title: "CAGE: Causal attention enables data-efficient generalizable robotic manipulation"
tags: [manipulation, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心架构：(1) DINOv2 冻结视觉骨干 + LoRA 微调提取鲁棒环境特征；(2) Causal Perceiver 对 DINOv2 输出 token 进行压缩，利用因果注意力保留任务相关信息；(3) 扩散动作预测头在压缩 token 上进行条件去噪生成动作。50 演示从单一训练环境即可泛化到物体、背景和视角的大分布变化。相似环境任务完成率提升 42%，完全未见环境仍达 43% 完成/51% 成功率（所有基线在未见环境均失败）"
authors: "Xia, Shangning; Fang, Hongjie; Lu, Cewu; Fang, Hao-Shu"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "B54Q8K5Q"
---
## 摘要

Generalization in robotic manipulation（机器人操控） remains a critical challenge, particularly when scaling to new environments with limited demonstrations. This paper introduces CAGE, a novel robotic manipulation（机器人操控） policy designed to overcome these generalization barriers by integrating a causal attention mechanism. CAGE utilizes the powerful feature extraction capabilities of the vision foundation model DINOv2, combined with LoRA fine-tuning for robust environment understanding. The policy further employs a causal Perceiver for effective token compression and a diffusion（扩散）-based action prediction head with attention mechanisms to enhance task-specific fine-grained conditioning. With as few as 50 demonstrations from a single training environment, CAGE achieves robust generalization across diverse visual changes in objects, backgrounds, and viewpoints. Extensive experiments validate that CAGE significantly outperforms existing state-of-the-art（现有最优方法） RGB/RGB-D approaches in various manipulation（操控） tasks, especially under large distribution shifts. In similar environments, CAGE offers an average of 42% increase in task completion rate. While all baselines fail to execute the task in unseen environments, CAGE manages to obtain a 43% completion rate and a 51% success rate in average, making a huge step towards practical deployment of robots in real-world settings. Project website: cage-policy.github.io.


## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 关键贡献

1. 因果注意力机制用于操控泛化：Causal Perceiver 保留任务相关特征、过滤无关变化
2. DINOv2 + LoRA 鲁棒视觉特征：冻结基础模型 + 轻微微调实现高效适应
3. 单环境 50 演示即可泛化：无需多环境或多物体训练数据
4. 完全未见环境仍有合理成功率：43% 完成率（所有基线均失败）
## 结构化提取

- **Problem**: 单环境少样本训练泛化到未见物体/背景/视角
- **Method**: CAGE — DINOv2+LoRA + Causal Perceiver + 扩散动作预测头
- **Tasks**: 桌面操控任务（pick-place 等，多环境评估）
- **Sensors**: RGB-D 相机
- **Robot Setup**: 桌面机器人（具体型号见原文）
- **Metrics**: 任务完成率/成功率（相似环境 +42%，未见环境 43%）
- **Limitations**: 仅桌面任务、因果假设、演示需求、未见环境成功率有限
- **Evidence Notes**: 全文读取，Tables 提供完整多环境泛化对比
## 本地引用关系

- [[chen2025vividex]]
- [[garcia2025generalizable]]
- [[lee2025diffdagger]]
- [[tang2025uad]]
- [[wu2025discrete]]
- [[zhu2024scaling]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables、figures
- **Confidence**: high — 全文完整，arXiv 2024，Shanghai Jiao Tong University，DINOv2 冻结 + LoRA 微调 + Causal Perceiver token 压缩 + 扩散动作预测头，50 演示单环境训练即可泛化到未见物体/背景/视角，相似环境成功率 +42%，完全未见环境 43% 完成/51% 成功
- **Summary**: 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心架构：(1) DINOv2 冻结视觉骨干 + LoRA 微调提取鲁棒环境特征；(2) Causal Perceiver 对 DINOv2 输出 token 进行压缩，利用因果注意力保留任务相关信息；(3) 扩散动作预测头在压缩 token 上进行条件去噪生成动作。50 演示从单一训练环境即可泛化到物体、背景和视角的大分布变化。相似环境任务完成率提升 42%，完全未见环境仍达 43% 完成/51% 成功率（所有基线在未见环境均失败）


## Problem

机器人操控的泛化性是关键挑战，特别是在只有有限演示的单一环境中训练时，如何泛化到新物体、新背景和新视角？现有方法在大分布变化下性能急剧下降。


## Method

- **视觉编码**：
  - DINOv2（冻结）+ LoRA 微调（rank 4-8）
  - 输入 RGB-D 图像 → DINOv2 patch token + LoRA 调制
  - LoRA 仅微调少量参数，保留预训练特征泛化性
- **Causal Perceiver**：
  - 输入：DINOv2 输出的大量 patch token
  - 输出：少量压缩 latent token
  - 因果注意力：仅关注当前和历史 token，过滤无关视觉变化
  - 关键：保留任务相关特征（如物体位姿），忽略干扰（如背景、光照）
- **扩散动作预测头**：
  - 条件去噪：以压缩 latent token 为条件
  - 注意力机制增强任务特定细粒度调节
  - 输出：7D 动作（6D 位姿 + gripper）
- **训练**：
  - 50 演示，单一训练环境
  - 端到端训练（LoRA + Perceiver + 扩散头）


## Experiments

- **相似环境泛化**：
  - CAGE 平均成功率 +42%（vs 基线）
  - 超越 ACT、Diffusion Policy、RVT 等
- **完全未见环境**：
  - CAGE：43% 完成率，51% 成功率
  - 所有基线：基本 0%（无法执行任务）
- **消融**：
  - 去除 Causal Perceiver → 性能大幅下降
  - 去除 LoRA → 泛化性下降
  - DINOv2 预训练权重至关重要
- **泛化维度**：
  - 物体变化：新形状、新纹理
  - 背景变化：不同桌面、不同光照
  - 视角变化：相机位姿偏移


## Limitations

1. 仅验证了桌面 pick-place 类任务，未扩展到复杂操控
2. 因果注意力的因果性假设可能不适用于所有任务
3. 50 演示仍需人工数据采集
4. 完全未见环境成功率（43-51%）仍有较大提升空间
5. 推理速度受扩散头去噪步骤影响


## Key Takeaways

- 因果注意力是泛化的关键：Causal Perceiver 过滤无关变化，保留任务相关特征
- DINOv2 预训练特征提供强基础：冻结 + LoRA 兼顾泛化和适应
- 单环境训练即可泛化：数据效率极高，50 演示足够
- 扩散头提供细粒度动作生成：注意力条件增强任务特定性
- 泛化到完全未见环境是可能的：CAGE 首次在基线全失败时仍有效

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[xia|Xia, Shangning]]
- [[fang|Fang, Hongjie]]
- [[lu|Lu, Cewu]]
- [[fang-hao-shu|Fang, Hao-Shu]]
