---
title: "3D Diffuser Actor: Policy Diffusion with 3D Scene Representations"
tags: [imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 3D Diffuser Actor，统一 3D 场景表示与扩散目标用于模仿学习。核心是 3D 相对去噪 Transformer：将 RGB-D 图像提升为 3D 场景 token，与语言 token、本体感知 token 通过 3D 相对注意力（rotary position embedding）融合，预测加噪 3D 末端执行器轨迹的噪声。RLBench 多视角 81.3%（+18.1% SOTA），单视角 69.6%（+13.1%），CALVIN +9% 相对提升。真实 12 任务少量演示即成功"
authors: "Ke, Tsung-Wei; Gkanatsios, Nikolaos; Fragkiadaki, Katerina"
year: "2024"
venue: "CoRL 2024"
zotero_key: "GQ9BVK8N"
---
## 摘要

Diffusion（扩散） policies are conditional diffusion（扩散） models that learn robot action distributions conditioned on the robot and environment state. They have recently shown to outperform（优于） both deterministic and alternative action distribution learning formulations. 3D robot policies use 3D scene feature representations aggregated from a single or multiple camera views using sensed depth. They have shown to generalize better than their 2D counterparts across camera viewpoints. We unify these two lines of work and present 3D Diffuser Actor, a neural policy equipped with a novel 3D denoising transformer that fuses information from the 3D visual scene, a language instruction and proprioception to predict the noise in noised 3D robot pose trajectories. 3D Diffuser Actor sets a new state-of-the-art（现有最优方法） on RLBench with an absolute performance gain of 18.1% over the current SOTA on a multi-view setup and an absolute gain of 13.1% on a single-view setup. On the CALVIN benchmark, it improves over the current SOTA by a 9% relative increase. It also learns to control a robot manipulator in the real world from a handful of demonstrations. Through thorough comparisons with the current SOTA policies and ablations of our model, we show 3D Diffuser Actor’s design choices dramatically outperform（优于） 2D representations, regression and classification objectives, absolute attentions, and holistic non-tokenized 3D scene embeddings.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec 2)、method (Sec 3)、experiments (Sec 4)、tables (1-4)、figures (1-5)、appendix 架构图
- **Confidence**: high — 全文完整，CoRL 2024 论文，RLBench 18 任务多视角 + 10 任务单视角 + CALVIN benchmark + 真实 12 任务系统评估
- **Summary**: 提出 3D Diffuser Actor，统一 3D 场景表示与扩散目标用于模仿学习。核心是 3D 相对去噪 Transformer：将 RGB-D 图像提升为 3D 场景 token，与语言 token、本体感知 token 通过 3D 相对注意力（rotary position embedding）融合，预测加噪 3D 末端执行器轨迹的噪声。RLBench 多视角 81.3%（+18.1% SOTA），单视角 69.6%（+13.1%），CALVIN +9% 相对提升。真实 12 任务少量演示即成功
## 关键贡献

1. 首次统一 3D 场景表示 + 扩散目标用于操控策略学习
2. 3D 相对去噪 Transformer：场景/动作 token 共享 3D 空间，rotary position embedding 实现平移等变
3. Tokenized 3D 场景表示（vs 池化 1D 嵌入），场景变化仅影响对应 token 子集
4. RLBench 新 SOTA：多视角 81.3%（vs Act3D 63.2%），单视角 69.6%
5. CALVIN +9% 相对提升，真实世界 12 任务验证
## 结构化提取

- **Problem**: 操控策略的多模态动作分布 + 3D 场景表示的统一
- **Method**: 3D Diffuser Actor — 3D 相对去噪 Transformer，扩散模型预测 3D 轨迹噪声
- **Tasks**: RLBench 18+10 任务 + CALVIN + 真实 12 任务
- **Sensors**: 多视角/单视角 RGB-D 相机
- **Robot Setup**: RLBench（Franka Panda 仿真）+ 真实 Franka
- **Metrics**: 成功率（多任务平均）
- **Limitations**: 计算成本高、依赖深度/标定、关键帧启发式、手动噪声调度
- **Evidence Notes**: 全文读取，Tables 1-4 提供完整 RLBench/CALVIN/消融结果
## 本地引用关系

- [[chen2025coordinated]]
- [[lee2025diffdagger]]
- [[xia2024cage]]
- [[zhu2024scaling]]
## Problem

操控任务中动作分布天然多模态（多种抓取方式），扩散策略优于确定性方法但通常用 2D 表示；3D 策略具有更好的视角泛化性但用分类/回归目标。两者尚未统一：如何结合 3D 场景表示的视角鲁棒性与扩散模型的多模态处理能力？


## Method

- **3D Tokenization**：
  - CLIP ResNet50 提取 2D 特征图 F ∈ R^{H×W×c}
  - 利用深度图 + 相机内外参 → 每个 patch 的 3D 坐标
  - 多视角聚合：合并所有视角的 3D scene token
  - 轨迹 token：加噪 3D 位姿 → MLP embedding + 3D position
  - 本体感知 token：当前末端位姿 + 可学习 embedding
  - 语言 token：CLIP 语言编码器
- **3D 相对去噪 Transformer**：
  - 3D self-attention 用 rotary position embedding 编码相对 3D 位置
  - eq,k ∝ xq^T M(pq-pk)xk，M 仅依赖相对位置 → 平移等变
  - Cross-attention 到语言 token（无 3D 位置）
  - 输出：平移噪声 ε^loc、旋转噪声 ε^rot、开关状态 f^open
- **扩散过程**：
  - 前向：τ^i = √ᾱ_i τ^0 + √(1-ᾱ_i) ε
  - 反向：迭代去噪 N 步，平移用 scaled-linear 调度器，旋转用 square cosine
- **训练**：L1 loss（平移+旋转噪声）+ BCE（开关状态）
- **推理**：关键帧检测（速度/加速度极值点或开关状态变化）→ 轨迹分段


## Experiments

- **RLBench 多视角（18 任务）**：
  - 3D Diffuser Actor: 81.3%（avg），vs Act3D 63.2%, RVT 62.9%, PerAct 49.4%
  - 具体任务：open drawer 89.6%, slide block 97.6%, sweep dustpan 84.0%
  - stack cups 98.4%, push buttons 82.4%, place wine 97.6%
- **RLBench 单视角（10 任务）**：
  - 69.6%（vs Act3D 56.4%, RVT 55.8%）
- **CALVIN benchmark**：
  - Zero-shot unseen scene: +9% 相对提升 vs SOTA
- **真实世界**：
  - 12 个操控任务（stack cups、open drawer 等），少量演示
  - 捕捉演示中的多模态行为
- **消融**：
  - 3D 表示 > 2D 表示（+15% avg）
  - 扩散目标 > 分类/回归目标
  - 相对注意力 > 绝对注意力
  - Tokenized 3D > 池化 1D 嵌入（vs 3D Diffusion Policy）


## Limitations

1. 计算成本：3D tokenization 和扩散去噪过程较慢
2. 依赖精确的深度图和相机标定
3. 关键帧检测依赖启发式（速度/加速度极值）
4. 分离的噪声调度器（平移/旋转）需要手动设计
5. 大规模预训练（CLIP）仍需要大量数据


## Key Takeaways

- 3D 场景表示 + 扩散目标是操控策略学习的最佳组合：3D 提供视角不变性，扩散处理多模态
- Tokenized 3D 场景表示优于池化 1D 嵌入：空间解耦使场景变化仅影响对应 token
- 3D 相对注意力（rotary position embedding）实现平移等变，提升泛化
- 分离的噪声调度器（平移/旋转各自最优）是性能提升的关键细节
- 关键帧检测 + 轨迹分段是有效的长时序任务分解策略

## 相关概念

- [[imitation-learning]]
- [[diffusion-model]]
- [[vision-language-model]]
- [[grasping]]

## 相关研究者

- [[ke|Ke, Tsung-Wei]]
