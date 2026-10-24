---
title: "Learning from imperfect demonstrations with self-supervision for robotic manipulation"
tags: [manipulation, RL, imitation, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监督预训练（Masked Transition Prediction + Transition Reconstruction + Action Autoregression）学习轨迹特征；(2) 基于特征相似度计算失败轨迹片段的质量分数（与专家数据 L2 距离），筛选高质量片段；(3) 加权行为克隆，质量分数作为 BC 损失权重。ManiSkill2 5 任务全面超越 SOTA，真实 Franka 5 任务 SSDF+ACT 平均 45% vs ACT 39%"
authors: "Wu, Kun; Liu, Ning; Zhao, Zhen; Qiu, Di; Li, Jinming et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "IE8SS48X"
---
## 摘要

Improving data utilization, especially for imperfect data from task failures, is crucial for robotic manipulation（机器人操控） due to the challenging, time-consuming, and expensive data collection process in the real world. Current imitation learning（模仿学习） (IL) typically discards imperfect data, focusing solely on successful expert data. While reinforcement learning（强化学习） (RL) can learn from explorations and failures, the sim2real gap and its reliance on dense reward（奖励） and online exploration make it difficult to apply effectively in real-world scenarios. In this work, we aim to conquer the challenge of leveraging imperfect data without the need for reward（奖励） information to improve the model performance for robotic manipulation（机器人操控） in an offline manner. Specifically, we introduce a Self-Supervised（自监督） Data Filtering framework (SSDF) that combines expert and imperfect data to compute quality scores for failed trajectory segments. High-quality segments from the failed data are used to expand the training dataset. Then, the enhanced dataset can be used with any downstream policy learning method for robotic manipulation（机器人操控） tasks. Extensive experiments on the ManiSkill2 benchmark built on the high-fidelity Sapien simulator and real-world robotic manipulation（机器人操控） tasks using the Franka robot arm demonstrated that the SSDF can accurately expand the training dataset with high-quality imperfect data and improve the success rates for all robotic manipulation（机器人操控） tasks.


## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、模仿学习、仿真到真实迁移

## 关键贡献

1. SSDF 自监督数据过滤框架：从失败轨迹中筛选高质量片段扩展训练集
2. 三种自监督预训练任务：MTP/TR/AA 使 Transformer 同时学习正向动力学、逆向动力学和行为克隆
3. 质量分数计算方法：基于特征 L2 距离的相似度度量
4. 加权行为克隆：质量分数作为损失权重区分高低质量片段
## 结构化提取

- **Problem**: 从失败轨迹中无监督筛选高质量片段扩展 IL 训练数据
- **Method**: SSDF — Transformer 自监督预训练 (MTP+TR+AA) + 特征相似度质量分数 + 加权 BC
- **Tasks**: ManiSkill2 5 任务 + 真实 Franka 5 任务
- **Sensors**: RGB-D 相机（双视角：手眼+固定）
- **Robot Setup**: Franka Panda 7-DoF + parallel gripper
- **Metrics**: 任务成功率（仿真 85.6%/88.0%/50.4%/29.6%/28.4%，真实平均 45%）
- **Limitations**: 需专家数据、计算开销大、仅桌面任务
- **Evidence Notes**: 全文读取，Tables I-V 提供完整对比和消融
## 本地引用关系

- [[chen2025effective]]
- [[gao2024prime]]
- [[hartz2024art]]
- [[lee2025diffdagger]]
- [[liu2025forcemimic]]
- [[wu2025discrete]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-V)、figures (1-4)
- **Confidence**: high — 全文完整，arXiv 2025，Syracuse University + Beijing Innovation Center of Humanoid Robotics，ManiSkill2 基准 5 任务（PickCube 85.6%/StackCube 88.0%/PickYCB 50.4%/Fill 29.6%/Hang 28.4%）+ 真实 Franka 5 任务平均 45%，SSDF 全面超越 BC/TF-BC/DemoDICE/DWBC/ISW-BC
- **Summary**: 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监督预训练（Masked Transition Prediction + Transition Reconstruction + Action Autoregression）学习轨迹特征；(2) 基于特征相似度计算失败轨迹片段的质量分数（与专家数据 L2 距离），筛选高质量片段；(3) 加权行为克隆，质量分数作为 BC 损失权重。ManiSkill2 5 任务全面超越 SOTA，真实 Franka 5 任务 SSDF+ACT 平均 45% vs ACT 39%


## Problem

机器人操控中数据采集成本高昂，但现有 IL 方法通常丢弃失败数据（如 SayCan 仅保留 12k/276k = 4.3% 成功数据）。如何在不使用奖励函数和在线交互的情况下，利用失败轨迹中的高质量片段提升策略性能？


## Method

- **问题设定**：
  - 专家数据集 De + 不完美数据集 Di
  - 无奖励函数、无在线交互
  - 目标：利用 De ∪ Di 训练策略
- **Step 1：Transformer 自监督预训练**：
  - 多模态 Transformer：输入 (RGB-D, 本体感觉, 动作) 轨迹片段
  - MTP（Masked Transition Prediction）：随机掩蔽输入元素并预测 → 学习正向/逆向动力学
  - TR（Transition Reconstruction）：重建未掩蔽元素 → 学习压缩关键信息
  - AA（Action Autoregression）：因果掩码预测下一步动作 → 与 BC 目标一致
  - 联合损失：L_pretrain = L_MTP + L_TR + L_AA
- **Step 2：质量分数计算**：
  - 用预训练 Transformer 提取专家和不完美片段的特征
  - 相似度：sim(τ_imp, τ_exp) = -||z_imp - z_exp||_2（最后时间步特征）
  - 质量分数：q(τ_imp) = norm(max_sim(τ_imp, ∀τ_exp ∈ De)) ∈ [0,1]
  - 阈值 β 过滤：仅保留 q > β 的片段
- **Step 3：加权行为克隆**：
  - L_full = L_policy(De) - λ·E[τ~Df][q(τ)·logP(a|τ)]
  - λ 平衡专家和不完美数据训练


## Experiments

- **ManiSkill2 仿真（5 任务）**：
  - PickCube: SSDF 85.6% vs ISW-BC 79.2% vs BC 82.6%
  - StackCube: SSDF 88.0% vs ISW-BC 82.4% vs BC 80.0%
  - PickYCB: SSDF 50.4% vs ISW-BC 45.4% vs BC 43.6%
  - Fill: SSDF 29.6% vs ISW-BC 26.2% vs BC 24.8%
  - Hang: SSDF 28.4% vs ISW-BC 18.8% vs BC 14.4%
  - 全面超越 DemoDICE、DWBC、DT、C-BeT 等基线
- **真实 Franka（5 任务）**：
  - SSDF+ACT 平均 45% vs ACT 39% vs Diffusion Policy 35%
- **消融**：
  - 3 种自监督任务组合最优：88.0%（vs 单任务 72-79%）
  - β=0.9 最优（16k 保留数据）
  - Last+L2 优于 Seg+L2/Cosine
  - 低质量和高质量不完美数据均有益：低质量提供丰富探索（预训练阶段），高质量直接辅助微调


## Limitations

1. 仍需一定量的专家数据（300 条仿真）作为参考基准
2. Transformer 预训练计算开销较大
3. 仅在桌面操控任务验证，未扩展到移动操控或双臂任务
4. 质量分数基于 L2 距离，可能忽略语义相似性
5. 真实世界评估仅 5 任务，样本量有限


## Key Takeaways

- 失败轨迹中有价值数据：失败任务的许多步骤仍是高质量的
- 自监督预训练是关键：MTP+TR+AA 三任务组合使特征表示更鲁棒
- 基于特征相似度的质量评分有效：无需奖励函数即可区分高低质量片段
- 加权 BC 优于直接混合训练：质量分数作为权重避免低质量数据干扰
- 低质量数据也有价值：丰富的探索信息在预训练阶段提供正向贡献

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wu-kun|Wu, Kun]]
