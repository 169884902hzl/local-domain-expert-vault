---
title: "HP-edit: A human-preference post-training framework for image editing"
tags: [imitation, VLM, RL, diffusion, diffusion-model]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "提出 HP-Edit 框架，利用 VLM 训练的 HP-Scorer 作为任务感知奖励函数，结合 Flow-GRPO 对扩散模型图像编辑器进行人类偏好对齐的后训练，在 8 个编辑任务上显著提升 Qwen-Image-Edit-2509 的输出质量（HP-Score 4.472→4.667）。"
authors: "Li, Fan; Wang, Chonghuinan; Lei, Lina; Qiu, Yuping; Xu, Jiaqi et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "NVF3U5DE"
---
## 摘要

Common image editing tasks typically adopt powerful generative diffusion（扩散） models as the leading paradigm for real-world content editing. Meanwhile, although reinforcement learning（强化学习） (RL) methods such as Diffusion（扩散）-DPO and Flow-GRPO have further improved generation quality, efficiently applying Reinforcement Learning（强化学习） from Human Feedback (RLHF) to diffusion（扩散）-based editing remains largely unexplored, due to a lack of scalable human-preference datasets and frameworks tailored to diverse editing needs. To fill this gap, we propose HP-Edit, a post-training framework for Human Preference-aligned Editing, and introduce RealPref-50K, a real-world dataset across eight common tasks and balancing common object editing. Specifically, HP-Edit leverages a small amount of human-preference scoring data and a pretrained visual large language model（大语言模型） (VLM) to develop HP-Scorer--an automatic, human preference-aligned evaluator. We then use HP-Scorer both to efficiently build a scalable preference dataset and to serve as the reward（奖励） function for post-training the editing model. We also introduce RealPref-Bench, a benchmark for evaluating real-world editing performance. Extensive experiments demonstrate that our approach significantly enhances models such as Qwen-Image-Edit-2509, aligning their outputs more closely with human preference.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、扩散模型、扩散模型

## 关键贡献

1. **HP-Edit 框架**：一个三阶段后训练框架，统一了 VLM-based HP-Scorer、高效 hard-case 数据构建管线和任务感知 RL 后训练。
2. **RealPref-50K 数据集**：55,795 个真实世界编辑案例，覆盖 8 个编辑子任务（添加、移除、背景替换、物体交换、颜色变换、散景、重光照、风格迁移），在 MS-COCO 类别上实现平衡分布。
3. **RealPref-Bench 基准**：1,638 个案例的评估基准，使用真实世界图像和人工验证的偏好指令。
4. **HP-Scorer**：基于 VLM（Qwen3-VL-32B-Instruct）的任务感知自动评分器，仅需 50-100 条人工标注即可训练，与人类评分的 Pearson 相关系数达 0.89。
## 结构化提取

- Problem: 如何高效地将 RLHF 应用于基于扩散模型的图像编辑，解决缺乏可扩展偏好数据集和任务特定奖励模型的问题
- Method: 三阶段框架——(1) VLM-based HP-Scorer 用少量人工标注训练；(2) Hard-case 过滤构建偏好数据集；(3) Flow-GRPO 用 HP-Scorer 作奖励进行任务感知 RL 后训练
- Tasks: 图像编辑（8 个子任务：物体添加、移除、交换、背景替换、颜色变换、散景、重光照、风格迁移）
- Sensors: 图像输入（RGB），文本指令
- Robot Setup: 不涉及机器人
- Metrics: HP-Score（0-5 分 VLM 评分）、User Score、Pearson 相关系数（PCC）
- Limitations: 中英文混合文本编辑失败（继承自基座模型）；评分 prompt 需手动迭代优化；仅覆盖 8 个编辑任务
- Evidence Notes: 全文精读，包含主文 + 补充材料。主要实验结果来自 RealPref-Bench（1,638 案例）、GEdit-Bench（EN/CN）、DreamBench++。Ablation 验证了 hard-case 过滤和任务感知评分器的独立贡献。User study（5 标注者，1000+ 编辑对）验证了 HP-Scorer 对齐度（PCC 0.89）。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete (main paper + supplementary materials via arXiv HTML)
- Confidence: high
- Summary: 提出 HP-Edit 框架，利用 VLM 训练的 HP-Scorer 作为任务感知奖励函数，结合 Flow-GRPO 对扩散模型图像编辑器进行人类偏好对齐的后训练，在 8 个编辑任务上显著提升 Qwen-Image-Edit-2509 的输出质量（HP-Score 4.472→4.667）。


## Problem

扩散模型已成为图像编辑的主流范式，但如何将 RLHF 高效应用于基于扩散的编辑任务仍缺乏探索。核心挑战包括：(1) 缺乏可扩展的人类偏好数据集来覆盖多样的编辑需求；(2) 现有编辑数据来源混杂（卡通、合成图像等），与真实世界人类偏好不对齐；(3) 构建偏好对齐的编辑数据集需要昂贵的人工标注。此外，现有 RL 方法（Diffusion-DPO、Flow-GRPO）主要针对 T2I 生成，而 I2I 编辑需要同时满足任务准确性（如忠实移除对象）和偏好对齐（如自然的结果）双重目标。


## Method

### 三阶段框架

**Stage 1: HP-Scorer 训练**
- 每个编辑子任务收集 50-100 条三元组（输入图像 A，编辑图像 B，指令 T），人工标注 0-5 分偏好评分
- 使用预训练 VLM（Qwen3-VL-32B-Instruct）作为评分器，每个子任务设计独立的评分 prompt
- 评分 prompt 从基础评分标准开始，逐步加入任务特定推理问题（如物体交换任务："替换是否可行且明确？"、"原物体是否完全替换？"），迭代优化直到与人类评分对齐

**Stage 2: 偏好数据构建**
- 从高质量开源数据集（Pixabay、LSDIR、DIV2K）收集真实世界图像
- VLM 自动生成编辑指令，CLIP score 按 MS-COCO 类别计算相似度以实现类别平衡
- 预训练编辑模型生成编辑输出，形成三元组 (A, B, T)
- **关键过滤**：移除 HP-Scorer 评分 5 分的简单样本，只保留低分 hard case，构造训练集 D†

**Stage 3: 任务感知 RL 后训练**
- 基于 Flow-GRPO 框架，将 Flow Matching 的确定性 ODE 转换为等价 SDE 以支持随机策略采样
- HP-Scorer 作为奖励函数，奖励通过 sigmoid 归一化到 [0,1]：r = 1/(1+exp(-α*s+β))，α=2, β=5
- 使用 LoRA rank 32 微调，AdamW 优化器，学习率 3e-4
- 基座模型为 Qwen-Image-Edit-2509

### Flow-GRPO 技术细节
- 将 Flow Matching 采样过程建模为 MDP：(S, A, ρ₀, P, R)
- 策略 π_θ 即 flow model，对同一 prompt 生成 G 个样本组
- 优势函数通过组内奖励标准化计算：Â^i = (R(x_T^i, c) - mean) / std
- 目标函数使用 clipped surrogate + KL 散度惩罚


## Experiments

### 主要定量结果（RealPref-Bench）
| 方法 | Overall HP-Score |
|------|-----------------|
| Qwen-Image-Edit-2509 (baseline) | 4.472 |
| FLUX.1-Kontext-Dev | 4.421 |
| Step1X-Edit | 3.715 |
| BAGEL | 4.313 |
| **HP-Edit (Ours)** | **4.667** |

HP-Edit 在所有 8 个子任务上均排名第一，尤其在颜色变换、散景、重光照、背景替换等需要细粒度外观一致性或强真实感先验的任务上提升最显著。

### GEdit-Bench 结果
HP-Edit 在 GEdit-Bench-EN 和 GEdit-Bench-CN 上均达到 SOTA，超越了 Step1X-Edit 等方法。

### DreamBench++ 结果
在概念保持（CP）和提示跟随（PF）两个维度上均优于 Qwen-Image-Edit-2509 baseline。

### Ablation Study
| 配置 | HP-Score |
|------|----------|
| BaseData + BaseScorer | 4.391（低于 baseline） |
| RealPref-50K + BaseScorer | 4.577 |
| RealPref-50K + HP-Scorer (HP-Edit) | **4.667** |

关键发现：
- 未过滤数据 + 简单评分器导致性能下降（4.391 vs baseline 4.472），因简单样本导致奖励饱和
- 过滤 hard case 提供了更有信息量的梯度
- 任务感知评分器是关键提升因素

### User Study
5 名标注者评估 1000+ 编辑对，评分标准与 HP-Scorer 一致（0-5 分），用户评分分布与 HP-Score 高度一致，验证了 HP-Scorer 的评分准确性。

### HP-Scorer 与人类评分对齐
在 GEdit-Bench-EN 上的相关性分析显示，HP-Scorer 评分与用户评分的 Pearson 相关系数（PCC）平均为 0.89。


## Limitations

1. **中英文混合文本编辑**：在中英文切换（code-switching）场景下表现不佳（如"将英文文本翻译成中文"），这一局限主要继承自基座模型
2. **HP-Scorer 依赖性**：评分器质量直接影响训练信号，需要每个子任务精心设计评分 prompt
3. **数据集覆盖**：8 个编辑任务虽然涵盖常见场景，但未包含更复杂的组合编辑


## Key Takeaways

### 对 DLO 操控的启示
1. **VLM 作为自动评分器的范式**：HP-Scorer 证明仅需少量人工标注（50-100 条/任务）即可训练高质量 VLM 评分器，这一范式可迁移到机器人操控中——例如训练 VLM 评分器评估 DLO 操控质量，替代昂贵的人工评估
2. **Hard-case 过滤策略**：移除"简单样本"（高分样本）以提高训练效率的思路，可直接应用于机器人 RL 训练——在模拟器中优先采样失败案例
3. **任务感知奖励设计**：每个子任务独立设计评分 prompt 的做法，启发了对不同 DLO 任务（打结、缠绕、折叠）设计专门奖励函数的思路

### 对 VLM-based 控制的启示
1. **VLM 评分与人类偏好对齐的可行性**：PCC 0.89 的高对齐度表明 VLM 可以作为可靠的偏好代理，这对 VLM-based 机器人控制中的奖励设计有直接参考价值
2. **Flow-GRPO 的通用性**：将 Flow Matching 与 GRPO 结合的框架在视觉生成中验证了效果，理论上可扩展到基于 flow 的机器人策略学习

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[li-fan|Li, Fan]]
- [[wang-chonghuinan|Wang, Chonghuinan]]
