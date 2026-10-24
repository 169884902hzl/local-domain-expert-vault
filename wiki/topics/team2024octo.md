---
title: "Octo: An open-source generalist robot policy"
tags: [manipulation, imitation, DLO]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持多机器人微调，93M 参数即可跨机器人迁移"
authors: "Team, Octo Model; Ghosh, Dibya; Walke, Homer; Pertsch, Karl; Black, Kevin et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "J8RCVJNT"
---
## 摘要

Large policies pretrained on diverse robot datasets have the potential to transform robotic learning: instead of training new policies from scratch, such generalist robot policies may be finetuned with only a little in-domain data, yet generalize broadly. However, to be widely applicable across a range of robotic learning scenarios, environments, and tasks, such policies need to handle diverse sensors and action spaces, accommodate a variety of commonly used robotic platforms, and finetune readily and efficiently to new domains. In this work, we aim to lay the groundwork for developing open-source, widely applicable, generalist policies for robotic manipulation（机器人操控）. As a first step, we introduce Octo, a large transformer-based policy trained on 800k trajectories from the Open X-Embodiment（具身） dataset, the largest robot manipulation（机器人操控） dataset to date. It can be instructed via language commands or goal images and can be effectively finetuned to robot setups with new sensory inputs and action spaces within a few hours on standard consumer GPUs. In experiments across 9 robotic platforms, we demonstrate that Octo serves as a versatile policy initialization that can be effectively finetuned to new observation and action spaces. We also perform detailed ablations of design decisions for the Octo model, from architecture to training data, to guide future research on building generalist robot models.

## 中文简述

提出基于预训练的线缆操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、可变形物体操控

## 关键贡献

1. **开源通用策略**：首个开源的跨机器人通用策略，支持多种观测（单/双臂、RGB/RGBD）和动作空间
2. **模块化设计**：block-structured Transformer，可灵活替换 readout tokens（任务定义）和 action head（扩散/离散）
3. **扩散策略头**：使用 diffusion action head 而非离散化 token，更适合连续动作空间
4. **大规模预训练**：在 Open X-Embodiment 的 800K+ 轨迹（9 个数据集）上预训练
## 结构化提取

- Problem: 构建跨多种机器人平台的通用策略；现有方法闭源不可复现
- Method: Block-structured Transformer + Diffusion Action Head；在 Open X-Embodiment 上预训练
- Tasks: WidowX Bridge, ALOHA bimanual, Franka Kitchen, Google Robot 等多种任务
- Sensors: RGB/RGBD 图像（多视角），proprioception
- Robot Setup: 多种（WidowX, ALOHA, Franka, Google Robot 等）
- Metrics: 任务成功率
- Limitations: 控制频率 ~6Hz（不如 ALOHA 的 50Hz）；双臂任务零样本性能有限；仅用 RGB 不用深度；预训练计算量大
- Evidence Notes: Octo 是首个开源通用机器人策略；证明了跨机器人预训练的数据效率增益；扩散策略头的设计影响了后续工作
## 本地引用关系

- [[brohan2023rt2]]
- [[chi2024diffusion]]
- [[collaboration2025open]]
## 证据元数据

- Fulltext Quality: full (from Zotero PDF)
- Evidence Coverage: complete (full text including architecture, training, experiments)
- Confidence: high (full text read, architecture and training details verified)
- Summary: UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持多机器人微调，93M 参数即可跨机器人迁移
## Problem

如何构建一个跨多种机器人平台的通用策略？现有方法（RT-1/RT-2）依赖 Google 内部大规模数据，且不可复现。需要开源的、可微调的通用策略。
## Method

- **架构**：block-structured Transformer
  - Input tokens：window of 2 frames x 4 cameras，ViT-Large image encoder（307M），patch size 14
  - Readout tokens：可学习 tokens，用于指定任务/动作空间
  - Action head：扩散头（DDPM，20 步去噪），预测未来 4 步动作块
  - 参数量：93M（Octo-Small）
- **训练**：
  - 预训练：Open X-Embodiment 9 个数据集，800K+ episodes
  - 目标函数：条件去噪（diffusion loss），image augmentation（random crop + color jitter）
- **微调**：支持冻结/部分微调策略 encoder，仅训练新机器人的 action head
- **推理**：~6Hz 控制频率（Octo-Small on T4 GPU）
## Experiments

### 零样本评估（无微调）
- 在 WidowX Bridge V2 上：Octo-Small 32% vs RT-1-X 23%
- 在 ALOHA 双臂任务上：Octo 首次展示跨机器人零样本能力
- 总体：在 9 个评估设置中的 4 个超越或匹配 RT-1-X

### 微调评估
- 在 Franka Kitchen 任务上微调：Octo + 20 demos 达到接近从头训练 + 200 demos 的性能
- 在 ALOHA 双臂任务上微调：Octo 预训练初始化显著优于随机初始化
- 单臂任务微调：预训练带来的 data efficiency 约 2-5x
## Limitations

- 控制频率 ~6Hz，对精细操控仍不够
- 双臂任务零样本成功率有限，需要微调
- 仅使用 RGB 图像，未利用深度信息
- 预训练需要大量计算资源
- 在某些数据集上不如专门训练的策略
## Key Takeaways

1. 跨机器人预训练可行且有效，数据效率提升 2-5x
2. 扩散策略头比离散化更适合连续动作
3. 开源使社区可以在不同机器人上微调通用策略
4. 模块化设计（readout tokens + 可替换 action head）是跨机器人迁移的关键
5. Octo 为后续通用策略（如 pi0）铺平道路

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[diffusion-model]]
- [[bimanual-manipulation]]

## 相关研究者

- [[team|Team, Octo Model]]
- [[pertsch|Pertsch, Karl]]
