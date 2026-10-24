---
title: "OpenVLA: An open-source vision-language-action model"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K episodes 上训练，动作即 token 方式输出，在 WidowX Bridge 上超越 RT-2-X 且参数仅其 1/40，支持低成本微调"
authors: "Kim, Moo Jin; Pertsch, Karl; Karamcheti, Siddharth; Xiao, Ted; Balakrishna, Ashwin et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "9I67RYEL"
---
## 摘要

Large policies pretrained on a combination of Internet-scale vision-language data and diverse robot demonstrations have the potential to change how we teach robots new skills: rather than training new behaviors from scratch, we can fine-tune such vision-language-action (VLA) models to obtain robust, generalizable policies for visuomotor control. Yet, widespread adoption of VLAs for robotics has been challenging as 1) existing VLAs are largely closed and inaccessible to the public, and 2) prior work fails to explore methods for efficiently fine-tuning VLAs for new tasks, a key component for adoption. Addressing these challenges, we introduce OpenVLA, a 7B-parameter open-source VLA trained on a diverse collection of 970k real-world robot demonstrations. OpenVLA builds on a Llama 2 language model combined with a visual encoder that fuses pretrained features from DINOv2 and SigLIP. As a product of the added data diversity and new model components, OpenVLA demonstrates strong results for generalist manipulation（操控）, outperforming closed models such as RT-2-X (55B) by 16.5% in absolute task success rate across 29 tasks and multiple robot embodiments, with 7x fewer parameters. We further show that we can effectively fine-tune OpenVLA for new settings, with especially strong generalization results in multi-task（多任务） environments involving multiple objects and strong language grounding abilities, and outperform（优于） expressive from-scratch imitation learning（模仿学习） methods such as Diffusion Policy（扩散策略） by 20.4%. We also explore compute efficiency; as a separate contribution, we show that OpenVLA can be fine-tuned on consumer GPUs via modern low-rank adaptation methods and served efficiently via quantization without a hit to downstream success rate. Finally, we release model checkpoints, fine-tuning notebooks, and our PyTorch codebase with built-in support for training VLAs at scale on Open X-Embodiment（具身） datasets.

## 中文简述

提出基于扩散策略的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. **开源 7B VLA**：首个完全开源的视觉-语言-动作模型（权重、代码、数据集）
2. **高效训练**：7B 参数 vs RT-2 的 55-305B，在多项基准上匹配或超越 RT-2-X
3. **LoRA 微调**：支持在单 GPU 上用 LoRA 高效微调到新任务
4. **动作即 token**：延续 RT-2 的动作 token 化范式（7-DOF 离散化为 256 bins）
## 结构化提取

- Problem: VLA 模型闭源、参数大、不可微调
- Method: 开源 7B VLA（Prismatic VLM + 动作 token）；Open X-Embodiment 训练；LoRA 微调
- Tasks: WidowX Bridge V2, Google Robot, Franka Kitchen 等多种操控任务
- Sensors: RGB 图像（单/多视角）
- Robot Setup: 多种（WidowX, Google Robot, Franka 等）
- Metrics: 任务成功率
- Limitations: 控制频率 ~6Hz；仅支持单臂；动作离散化损失精度；不支持双臂
- Evidence Notes: OpenVLA 是首个开源 VLA；证明了 7B 足以匹配 55B；LoRA 微调范式被后续工作广泛采用
## 本地引用关系

- [[brohan2023rt2]]
- [[collaboration2025open]]
- [[team2024octo]]
## 证据元数据

- Fulltext Quality: full (from Zotero PDF)
- Evidence Coverage: complete (full text including training, experiments, ablations)
- Confidence: high (full text read, architecture and results verified)
- Summary: Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K episodes 上训练，动作即 token 方式输出，在 WidowX Bridge 上超越 RT-2-X 且参数仅其 1/40，支持低成本微调
## Problem

RT-2 等 VLA 模型虽展示了强大的语义推理和泛化能力，但完全闭源、参数巨大（55-305B），社区无法复现或微调。需要开源、可微调的 VLA 模型。
## Method

- **基座模型**：Prismatic-7B VLM（SigLIP 视觉编码器 + 7B Llama-2 语言模型）
- **动作 token 化**：7 维关节动作（7-DOF 末端增量），每维 256 bins → 7 个 token
- **训练数据**：Open X-Embodiment 的 970K episodes（22 个数据集）
- **训练细节**：
  - 视觉编码器冻结，仅训练语言模型 + 投影层
  - 批大小 2048，学习率 2e-5，~1.5 epoch
  - 训练时间：~14 天 on 64 A100 GPUs
- **微调**：LoRA（rank 16），单 GPU（A100/4090）即可微调
- **推理**：~6Hz on A100（单步推理）
## Experiments

### WidowX Bridge V2（零样本）
- OpenVLA 79.5% vs RT-2-X 72.3% vs Octo 58.7%
- 在 24 个任务上的平均成功率

### Google Robot（零样本）
- OpenVLA 接近 RT-2-X 的性能（在已知任务上），参数仅其 1/40

### 微调评估
- 在 Bridge V2 上 LoRA 微调 20 demos：OpenVLA 预训练初始化 >> 从头训练
- 在 Franka Kitchen 上：OpenVLA + LoRA 接近完全微调的性能
- 单 GPU 微调即可部署到新机器人

### 消融
- 视觉编码器冻结 vs 全参数微调：冻结略好（避免过拟合）
- 动作分箱数：256 bins 足够
- 训练数据量：更多数据持续提升泛化性能
## Limitations

- 控制频率 ~6Hz，不适合精细操控
- 仅支持单臂 7-DOF 动作空间
- 动作离散化为 256 bins，精度受限
- 视觉编码器冻结可能限制视觉泛化
- 训练仍需 64xA100 的资源
## Key Takeaways

1. 7B VLM 足以在机器人操控上匹配 55B 模型，VLA 的关键在于训练数据而非模型规模
2. 开源 VLA 使社区可以在消费级硬件上微调部署
3. 动作 token 化（RT-2 范式）在大规模多机器人数据上有效
4. 视觉编码器冻结 + 语言模型微调是 VLA 训练的有效策略
5. Open X-Embodiment 数据集是 VLA 训练的关键基础设施

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]

## 相关研究者

- [[kim|Kim, Moo Jin]]
- [[pertsch|Pertsch, Karl]]
