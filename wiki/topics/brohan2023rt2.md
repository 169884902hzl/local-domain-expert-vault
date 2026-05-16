---
title: "RT-2: Vision-language-action models transfer web knowledge to robotic control"
tags: [VLM, robot-learning]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获得语义推理和泛化能力，在未见过的物体、指令和环境中实现 3x 泛化提升"
authors: "Brohan, Anthony; Brown, Noah; Carbajal, Justice; Chebotar, Yevgen; Chen, Xi et al."
year: "2023"
venue: "arXiv Preprint"
zotero_key: "J9HQZVC6"
---
## 摘要

We study how vision-language models trained on Internet-scale data can be incorporated directly into end-to-end（端到端） robotic control to boost generalization and enable emergent semantic reasoning. Our goal is to enable a single end-to-end（端到端） trained model to both learn to map robot observations to actions and enjoy the benefits of large-scale pretraining（预训练） on language and vision-language data from the web. To this end, we propose to co-fine-tune state-of-the-art（现有最优方法） vision-language models on both robotic trajectory data and Internet-scale vision-language tasks, such as visual question answering. In contrast to other approaches, we propose a simple, general recipe to achieve this goal: in order to fit both natural language responses and robotic actions into the same format, we express the actions as text tokens and incorporate them directly into the training set of the model in the same way as natural language tokens. We refer to such category of models as vision-language-action models (VLA) and instantiate an example of such a model, which we call RT-2. Our extensive evaluation (6k evaluation trials) shows that our approach leads to performant robotic policies and enables RT-2 to obtain a range of emergent capabilities from Internet-scale training. This includes significantly improved generalization to novel objects, the ability to interpret commands not present in the robot training data (such as placing an object onto a particular number or icon), and the ability to perform rudimentary reasoning in response to user commands (such as picking up the smallest or largest object, or the one closest to another object). We further show that incorporating chain of thought reasoning allows RT-2 to perform multi-stage semantic reasoning, for example figuring out which object to pick up for use as an improvised hammer (a rock), or which type of drink is best suited for someone who is tired (an energy drink).

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 视觉-语言模型、机器人学习

## 关键贡献

1. **VLA 模型概念**：提出 Vision-Language-Action (VLA) 模型，将动作表示为文本 token（如"1 128 191 255"代表 7-DOF 关节增量），直接融入 VLM 的输出空间
2. **Co-fine-tuning**：在机器人轨迹数据和互联网视觉-语言任务（如 VQA）上联合微调，保留语义理解能力
3. **两种变体**：RT-2-PaLI-X（基于 PaLI-X）和 RT-2-PaLM-E（基于 PaLM-E），参数量从 55B 到 305B
4. **涌现推理**：模型展现出链式思维推理能力，如"Pick up the object that is not the apple"等需要语义理解的任务
## 结构化提取

- Problem: 机器人策略缺乏语义理解和开放世界泛化
- Method: Vision-Language-Action (VLA) 模型；动作表示为文本 token；co-fine-tune
- Tasks: Google Robot 13+操控任务 + 泛化评估（未见物体/指令/环境）
- Sensors: RGB 图像（机器人摄像头）
- Robot Setup: Google Mobile Manipulator（7-DOF arm + 移动基座）
- Metrics: 任务成功率
- Limitations: 控制频率低（1-3Hz）；无法执行精细操控；仅限单臂数据；模型巨大（55-305B 参数）
- Evidence Notes: RT-2 是 VLA 模型的开山之作；动作即文本的范式被后续工作广泛采用；证明了大规模 VLM 预训练对机器人控制的迁移价值
## 本地引用关系

- [[kim2024openvla]]
- [[team2024octo]]
## 证据元数据

- Fulltext Quality: full (full paper from Zotero)
- Evidence Coverage: complete (full text, experiments, emergent reasoning evaluation)
- Confidence: high (full text read, all experiments covered)
- Summary: Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获得语义推理和泛化能力，在未见过的物体、指令和环境中实现 3x 泛化提升
## Problem

机器人策略通常只在窄域数据上训练，缺乏对开放世界语义的理解。如何利用互联网规模的视觉-语言预训练知识来提升机器人操控的泛化和推理能力？
## Method

- **动作表示**：将 7-DOF 关节增量（每个维度离散化为 256 bins）转为文本 token 序列（如 "1 128 191 255 ..."），每个数字作为一个 token
- **模型架构**：
  - RT-2-PaLI-X：55B 参数，基于 PaLI-X VLM
  - RT-2-PaLM-E：305B 参数，基于 PaLM-E，可接受多模态历史输入
- **训练数据**：RT-1 的 13 个机器人任务 + 互联网 VQA 数据
- **推理**：1-3Hz 控制频率（55B）/ 3-5Hz（经过量化加速），动作空间为 7-DOF 末端执行器增量 + gripper
- **Chain-of-Thought**：RT-2-PaLM-E 支持 CoT 推理，先生成思维文本再生成动作
## Experiments

### 泛化评估（Google 机器人真实环境）
- **未见物体**：RT-2 在 14/20 任务成功 vs RT-1 的 8/20
- **未见指令**（如语义理解）：RT-2 在 10/16 成功 vs RT-1 的 3/16
- **未见环境**：RT-2 在 12/20 成功 vs RT-1 的 4/20
- **总体泛化**：RT-2 在未见场景中成功率约为 RT-1 的 3 倍

### 涌现推理能力
- 能理解抽象概念："pick up object about to fall off the table"
- 能处理否定指令："pick up the object that is not the apple"
- 数量理解："pick up the Nth object from the left"
- 视觉推理：识别品牌、数字、颜色组合

### 已见任务性能
- RT-2 在 RT-1 原始 13 个任务上与 RT-1 相当（~67% vs ~69%），co-fine-tune 并不损害已知任务性能
## Limitations

- 控制频率仅 1-3Hz，无法执行需要高频反馈的精细操控
- 模型规模巨大（55-305B），难以部署到本地硬件
- 仅在 Google 内部机器人上验证，可复现性有限
- 动作空间为末端执行器增量，未涉及关节空间控制
- 训练需要大规模机器人数据和计算资源
## Key Takeaways

1. VLM 知识可通过简单 co-fine-tune 迁移到机器人控制，无需专门架构
2. 动作即文本的设计简洁通用，使 LLM 的推理能力自然涌现到机器人领域
3. 大规模预训练是关键：305B 的 PaLM-E 变体泛化能力更强
4. 控制频率（1-3Hz）仍然是瓶颈，远低于 ALOHA 的 50Hz
5. 奠定了后续 VLA 模型（OpenVLA、Octo）的基础

## 相关概念

- [[vision-language-model]]
- [[robot-learning]]
- [[grasping]]

## 相关研究者

- [[brohan|Brohan, Anthony]]
