---
title: "VITaL pretraining: Visuo-tactile pretraining for tactile and non-tactile manipulation policies"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 VITaL 预训练方法，通过时间感知的多模态对比损失将视觉和触觉编码器投影到共享潜在空间。关键发现：用触觉数据预训练的纯视觉策略性能大幅提升（USB 插入 20%→85%），达到与视觉-触觉策略相当的水平，甚至在某些任务上超越它。GelSight 磨损问题是部署触觉传感器的实际挑战"
authors: "George, Abraham; Gano, Selam; Katragadda, Pranav; Farimani, Amir Barati"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "YAM3HBNV"
---
## 摘要

Tactile（触觉） information is a critical tool for dexterous manipulation（灵巧操控）. As humans, we rely heavily on tactile（触觉） information to understand objects in our environments and how to interact with them. We use touch not only to perform manipulation（操控） tasks but also to learn how to perform these tasks. Therefore, to create robotic agents that can learn to complete manipulation（操控） tasks at a human or super-human level of performance, we need to properly incorporate tactile（触觉） information into both skill execution and skill learning. In this paper, we investigate how we can incorporate tactile（触觉） information into imitation learning（模仿学习） platforms to improve performance on manipulation（操控） tasks. We show that incorporating visuo-tactile（触觉） pretraining（预训练） improves imitation learning（模仿学习） performance, not only for tactile（触觉） agents (policies that use tactile（触觉） information at inference), but also for non-tactile（触觉） agents (policies that do not use tactile（触觉） information at inference). For these non-tactile（触觉） agents, pretraining（预训练） with tactile（触觉） information significantly improved performance (for example, improving the accuracy on USB plugging from 20% to 85%), reaching a level on par with visuo-tactile（触觉） agents, and even surpassing them in some cases. For demonstration（示范数据） videos and access to our codebase, see the project website: https://sites.google.com/andrew.cmu.edu/visuo-tactile-pretraining

## 中文简述

提出基于模仿学习的绳索操控方法。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、figures (1-7)
- **Confidence**: high — 全文完整，USB 线缆插入 + 两种堆叠任务系统评估，ACT 和 Diffusion Policy 两种框架
- **Summary**: 提出 VITaL 预训练方法，通过时间感知的多模态对比损失将视觉和触觉编码器投影到共享潜在空间。关键发现：用触觉数据预训练的纯视觉策略性能大幅提升（USB 插入 20%→85%），达到与视觉-触觉策略相当的水平，甚至在某些任务上超越它。GelSight 磨损问题是部署触觉传感器的实际挑战
## 关键贡献

1. 时间感知多模态对比预训练：视觉和触觉编码器通过 CLIP 风格对比损失对齐到共享潜在空间
2. 关键发现：触觉预训练对纯视觉策略的提升远大于对视觉-触觉策略的提升
3. 证明预训练降低策略施加的力（减少触觉传感器磨损）
4. 两种 IL 框架集成：ACT 和 Diffusion Policy
## 结构化提取

- **Problem**: 触觉数据在模仿学习中的有效利用和触觉传感器部署挑战
- **Method**: VITaL — 时间感知多模态对比预训练 + ACT/DP 框架集成
- **Tasks**: USB 线缆插入、矩形块堆叠、立方体堆叠
- **Sensors**: 6×RGB 相机 + GelSight Mini 触觉传感器
- **Robot Setup**: Franka Panda（真实）
- **Metrics**: 成功率（20 次试验）、平均应变
- **Limitations**: 任务特定预训练、传感器磨损、域偏移、任务有限
- **Evidence Notes**: 全文读取，Fig. 7 提供完整成功率对比
## 本地引用关系

- [[funk2024evetac]]
- [[liu2025forcemimic]]
- [[zhao2025polytouch]]
## Problem

触觉信息对灵巧操控至关重要，但部署触觉传感器面临磨损、成本和过拟合问题。如何有效利用触觉数据来提升（即使是纯视觉的）操控策略性能？


## Method

- **编码器**：ResNet-18 视觉编码器 + ResNet-18 触觉编码器，输出 R^512 特征
- **对比预训练**：
  - 从单条演示中采样 n=7 个观测对，最小时间间隔 Δt_min=10 步（1 秒）
  - 视觉投影头：MLP R^512→R^512
  - 触觉投影头：MLP（触觉特征 + 机器人位置）→R^512
  - 对比损失：同一时间步的视觉-触觉嵌入最大化相似度，不同时间步最小化
  - 多相机训练：分别计算每个相机视角的对比损失，隐式对齐多视角
- **IL 框架**：
  - ACT：替换视觉编码器为预训练编码器，触觉编码拼接到 transformer decoder
  - Diffusion Policy：预训练编码器 + CNN-based 噪声预测网络
- **触觉数据**：GelSight Mini，应变图（240×320×3），加装 1mm Ecoflex 保护层


## Experiments

- **USB 线缆插入**（100 演示）：
  - ACT 视觉-触觉+预训练：95%（vs 无预训练 90%）
  - ACT 纯视觉+预训练：85%（vs 无预训练 20%）
  - DP 纯视觉+预训练：75%（vs 无预训练 45%）
- **矩形块堆叠**：预训练视觉策略 ≈ 视觉-触觉策略
- **立方体堆叠**：预训练视觉策略在某些情况下超越视觉-触觉策略
- **力减少**：预训练降低策略施加的力（触觉应变减少 8-20%）
- **t-SNE 可视化**：预训练后视觉和触觉嵌入成功对齐，按时间步和抓取状态聚类


## Limitations

1. 预训练使用任务特定数据，限制了跨任务泛化
2. 触觉传感器磨损严重（30 次演示即撕裂，保护层后数百次）
3. 不同 GelSight pad 间存在域偏移，导致过拟合
4. 仅在 3 个任务上验证，多样性有限
5. 纯触觉策略在 DP 框架下完全失败


## Key Takeaways

- 触觉预训练的最大受益者是纯视觉策略（而非视觉-触觉策略）
- 对比预训练让视觉编码器学到隐式的接触理解
- 预训练减少策略施加的力，暗示更接触感知的控制
- GelSight 传感器磨损是实际部署的主要障碍
- 纯视觉策略 + 触觉预训练可能是比部署触觉传感器更实用的方案

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[george|George, Abraham]]
