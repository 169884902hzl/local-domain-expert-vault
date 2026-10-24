---
title: "Diffusion policy: Visuomotor policy learning via action diffusion"
tags: [manipulation, imitation, VLM, diffusion, robot-learning]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9%，核心贡献包括闭环动作序列预测、视觉条件化和时序扩散 Transformer"
authors: "Chi, Cheng; Xu, Zhenjia; Feng, Siyuan; Cousineau, Eric; Du, Yilun et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "4UWTSSQ8"
---
## 摘要

This paper introduces Diffusion Policy（扩散策略）, a new way of generating robot behavior by representing a robot's visuomotor policy as a conditional denoising diffusion（扩散） process. We benchmark Diffusion Policy（扩散策略） across 12 different tasks from 4 different robot manipulation（机器人操控） benchmarks and find that it consistently outperforms existing state-of-the-art（现有最优方法） robot learning methods with an average improvement of 46.9%. Diffusion Policy（扩散策略） learns the gradient of the action-distribution score function and iteratively optimizes with respect to this gradient field during inference via a series of stochastic Langevin dynamics steps. We find that the diffusion（扩散） formulation yields powerful advantages when used for robot policies, including gracefully handling multimodal（多模态） action distributions, being suitable for high-dimensional action spaces, and exhibiting impressive training stability. To fully unlock the potential of diffusion（扩散） models for visuomotor policy learning on physical robots, this paper presents a set of key technical contributions including the incorporation of receding horizon control, visual conditioning, and the time-series diffusion（扩散） transformer. We hope this work will help motivate a new generation of policy learning techniques that are able to leverage the powerful generative modeling capabilities of diffusion（扩散） models. Code, data, and training details is publicly available diffusion（扩散）-policy.cs.columbia.edu

## 中文简述

提出基于扩散策略的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、机器人学习

## 关键贡献

1. **Diffusion Policy 概念**：将机器人视觉运动策略表示为条件去噪扩散过程（DDPM），通过学习动作分布的 score function 梯度场进行推理
2. **闭环动作序列预测**：结合预测时域控制（receding horizon），策略预测 Tp 步动作但仅执行 Ta 步后重新规划，平衡时序一致性与响应性
3. **视觉条件化**：将视觉观测作为条件而非联合分布的一部分，视觉编码器只需前向传播一次，大幅降低推理延迟
4. **时序扩散 Transformer**：提出基于 Transformer 的去噪网络，减少 CNN 的过度平滑效应，适合高频动作变化和速度控制任务
5. **位置控制优势**：发现 Diffusion Policy 在位置控制模式下显著优于速度控制，与已有方法相反
## 结构化提取

- Problem: 行为克隆中的多模态动作分布建模、高维动作空间采样和训练稳定性
- Method: DDPM 条件扩散策略 + 闭环动作序列预测 + 视觉条件化 + 时序扩散 Transformer
- Tasks: 15 个任务（Robomimic 5 + Push-T + Block Push + Kitchen + 4 真实单臂 + 3 双臂）
- Sensors: RGB 图像（1-4 相机），proprioception（关节位置）
- Robot Setup: UR5（单臂），Franka Panda（单臂+双臂），2-14 DOF 动作空间
- Metrics: 任务成功率、IoU（Push-T）、覆盖率（Sauce）
- Limitations: 继承行为克隆局限（需充足演示数据）；推理延迟高于简单方法（如 LSTM-GMM）；不适合极高频控制任务
- Evidence Notes: Diffusion Policy 是扩散策略用于机器人操控的开山之作；被 Octo、Mobile ALOHA 等后续工作广泛采用；证明了位置控制+扩散策略的优越组合
## 本地引用关系

- [[fu2024mobile]]
- [[team2024octo]]
## 证据元数据

- Fulltext Quality: full (from Zotero PDF, IJRR journal version, ~14418 words)
- Evidence Coverage: complete (full text including all 15 tasks, 4 benchmarks, ablations, bimanual extension)
- Confidence: high (full text read, architecture details, hyperparameters, and all experiments verified)
- Summary: Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9%，核心贡献包括闭环动作序列预测、视觉条件化和时序扩散 Transformer


## Problem

行为克隆中的机器人策略学习面临三大挑战：(1) 人类演示数据中的多模态动作分布难以建模；(2) 高维动作空间（如长时域动作序列）难以有效采样；(3) 隐式策略（如 IBC）训练不稳定。如何设计一种既能表达多模态分布、又训练稳定的策略表示？


## Method

- **DDPM 公式化**：动作生成建模为 K 步去噪过程，x_{k-1} = α(x_k - γε_θ(x_k, k) + N(0, σ²I))，其中 ε_θ 是噪声预测网络
- **训练目标**：L = MSE(ε_k, ε_θ(O_t, A_t^0 + ε_k, k))，标准 DDPM 噪声预测损失，条件化为视觉观测
- **两种网络架构**：
  - CNN-based：1D 时序 CNN + FiLM 条件化（Feature-wise Linear Modulation），观察特征注入每个卷积层
  - Transformer-based：minGPT 风格 decoder，动作 token 用 causal attention，观测 embedding 通过 cross-attention 注入
- **视觉编码器**：ResNet-18（无预训练），全局平均池化替换为 spatial softmax，BatchNorm 替换为 GroupNorm
- **推理加速**：DDIM 将推理去噪步数从 100 降至 10-16 步，实现在 RTX 3080 上 0.1s 推理延迟，10Hz 控制频率
- **关键超参数**：观测时域 To=2，动作执行时域 Ta=8，预测时域 Tp=16；动作空间归一化到 [-1, 1]


## Experiments

### 仿真评估（4 基准 15 任务）
- **Robomimic**（9 变体，5 任务）：Diffusion Policy 在所有任务上超越 LSTM-GMM、IBC、BET
  - Lift/Can/Square：接近 100% 成功率
  - Transport（双臂）：DiffusionPolicy-C 94%/82%（ph/mh）vs LSTM-GMM 95%/73%
  - ToolHang：DiffusionPolicy-T 100%/84% vs LSTM-GMM 76%/47%
- **Push-T**：DiffusionPolicy-C 95%/91%（state/vision），IBC 和 LSTM-GMM 几乎为 0%
- **Block Push**（多模态长时域）：DiffusionPolicy-T p2=0.94 vs BET 0.71 vs LSTM-GMM 0.01
- **Franka Kitchen**（多任务长时域）：DiffusionPolicy-C p4=0.99 vs BET 0.44

### 真实世界评估（4 单臂 + 3 双臂任务）
- **Push-T**（UR5）：95% 成功率，IoU 0.80 vs 人类 0.84，LSTM-GMM 0%，IBC 20%
- **Mug Flipping**（6-DOF，Franka）：90% 成功率，LSTM-GMM 0%
- **Sauce Pouring**（6-DOF，液体）：覆盖率 0.74 vs 人类 0.79
- **Sauce Spreading**（周期性动作）：覆盖率 0.77 vs 人类 0.79
- **Bimanual Egg Beater**（双臂+触觉反馈遥操作）：55% 成功率（210 demos）
- **Bimanual Mat Unrolling**：75% 成功率（162 demos）
- **Bimanual Shirt Folding**：75% 成功率（284 demos）

### 消融实验
- 位置控制 vs 速度控制：Diffusion Policy 位置控制显著优于速度控制，而基线方法相反
- 动作时域：Ta=8 最优（平衡一致性与响应性）
- 观测时域：To=2 是良好折中
- 视觉编码器：ViT-B/16 + CLIP 预训练 + 微调达 98% 成功率（Square 任务），端到端训练优于冻结预训练
- 数据效率：在所有数据规模下优于 LSTM-GMM
- 延迟鲁棒性：位置控制可容忍至 4 步延迟


## Limitations

- 继承行为克隆的固有局限：需要充足且高质量的演示数据
- 推理延迟（~0.1s/步）高于简单方法如 LSTM-GMM，不适合需要极高频控制的任务
- 双臂任务成功率有限（55%-75%），需要大量演示数据
- Transformer 架构训练不稳定，超参数敏感
- 仅在有限的机器人平台上验证


## Key Takeaways

1. 扩散模型是行为克隆中强大的策略表示，天然处理多模态分布、高维输出和训练稳定性
2. 闭环动作序列预测是关键设计：鼓励时序一致性同时保持响应性
3. 位置控制在 Diffusion Policy 下优于速度控制，因其更好的多模态表达和更低的累积误差
4. CNN 架构开箱即用且超参数一致，Transformer 架构在复杂任务上更强但需要更多调参
5. 扩散策略的推理延迟可通过 DDIM 有效降低，支持 10Hz 实时控制

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[robot-learning]]
- [[bimanual-manipulation]]

## 相关研究者

- [[chi|Chi, Cheng]]
- [[feng|Feng, Siyuan]]
- [[cousineau|Cousineau, Eric]]
