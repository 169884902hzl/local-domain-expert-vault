---
title: "ReVLA: Reverting Visual Domain Limitation of Robotic Foundation Models"
tags: [VLM, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "发现 OpenVLA 在 OpenX 微调时 DINO-v2 和 SigLIP 视觉编码器发生灾难性遗忘，提出渐进式 backbone 回退策略（θ = (1-α)θ_OpenVLA + α·θ_pretrained），最佳配置 ReVLA(DS gradual) 在 OOD 整体任务上达到 27.8% vs OpenVLA-fractal 13.5%（提升 77%），In-domain Visual Matching 60% vs 36.1%"
authors: "Dey, Sombit; Zaech, Jan-Nico; Nikolov, Nikolay; Van Gool, Luc; Paudel, Danda Pani"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "3R59KXPM"
---
## 摘要

Recent progress in large language models and access to large-scale robotic datasets has sparked a paradigm shift in robotics models transforming them into generalists able to adapt to various tasks, scenes, and robot modalities. A large step for the community are open Vision Language Action models which showcase strong performance in a wide variety of tasks. In this work, we study the visual generalization capabilities of three existing robotic foundation models, and propose a corresponding evaluation framework.

## 中文简述

提出基于模仿学习的操控方法，具有泛化能力特点。

**研究方向**: 视觉-语言模型、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-4)
- **Confidence**: high — 全文完整，在 OpenX 数据集上训练并在 LIBERO 基准上系统评估（4 种场景）
- **Summary**: 发现 OpenVLA 在 OpenX 微调时 DINO-v2 和 SigLIP 视觉编码器发生灾难性遗忘，提出渐进式 backbone 回退策略（θ = (1-α)θ_OpenVLA + α·θ_pretrained），最佳配置 ReVLA(DS gradual) 在 OOD 整体任务上达到 27.8% vs OpenVLA-fractal 13.5%（提升 77%），In-domain Visual Matching 60% vs 36.1%
## 关键贡献

1. 系统分析 VLA 模型中视觉编码器的灾难性遗忘现象
2. 提出渐进式 backbone 回退（gradual backbone reversal）：训练后逐步将编码器参数恢复到预训练权重
3. 证明联合回退 DINO-v2 + SigLIP 优于单独回退任一编码器
4. 设计系统消融实验：分别回退 D/S/DS，线性/余弦/渐进调度
## 结构化提取

- **Problem**: VLA 模型视觉编码器在微调中的灾难性遗忘问题
- **Method**: ReVLA — 渐进式 backbone 回退（θ = (1-α)θ_finetuned + α·θ_pretrained）
- **Tasks**: LIBERO 基准（Spatial/Object/Visual Matching/Goal）
- **Sensors**: RGB 相机
- **Robot Setup**: LIBERO 仿真环境（Franka Panda）
- **Metrics**: 成功率（10 次试验平均）
- **Limitations**: 仅 OpenVLA+LIBERO、超参数敏感、OOD 绝对性能仍低
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整定量结果和消融
## 本地引用关系

- [[garcia2025generalizable]]
- [[tang2025kalie]]
## Problem

Vision-Language-Action (VLA) 模型（如 OpenVLA）在大规模机器人数据集（OpenX）上微调时，预训练视觉编码器（DINO-v2、SigLIP）发生灾难性遗忘，导致视觉泛化能力大幅下降，尤其在分布外（OOD）任务上表现严重退化。


## Method

- **基线模型**：OpenVLA（7B 参数），基于 Prismatic VLM 架构
- **问题诊断**：对比 OpenVLA 预训练权重 vs OpenX 微调后的 DINO-v2/SigLIP 权重，发现编码器表征质量显著退化
- **渐进式回退**：
  - 线性调度：θ = (1-α)θ_finetuned + α·θ_pretrained，α 从 0 线性增至 1
  - 余弦调度：α 按余弦曲线增长
  - 渐进调度：先正常微调若干步，再开始回退
- **配置空间**：
  - D：仅回退 DINO-v2
  - S：仅回退 SigLIP
  - DS：联合回退两者
- **训练数据**：OpenX 数据集（混合多任务机器人数据）


## Experiments

- **基准**：LIBERO（4 个场景：Spatial、Object、Visual Matching、Goal）
- **关键结果**：
  - In-domain Visual Matching：ReVLA(DS gradual) 60% vs OpenVLA-fractal 36.1%
  - OOD Spatial：15.6% vs 10.8%
  - OOD Object：16.7% vs 8.3%
  - OOD Goal：14.4% vs 11.1%
  - OOD 总体：27.8% vs 13.5%（77% 提升）
  - 最佳配置：DS gradual > DS cosine > DS linear > D/S alone
- **消融**：
  - 回退策略：gradual > cosine > linear（渐进式保留更多微调知识）
  - 编码器组合：DS > D > S（联合回退效果最好）
  - 完全不微调编码器：性能介于 baseline 和 ReVLA 之间


## Limitations

1. 仅在 OpenVLA + LIBERO 上验证，未测试其他 VLA 模型或任务域
2. 回退策略需要额外超参数（α 调度、开始步数）
3. 未能从根本上解决微调-遗忘的权衡
4. OOD 绝对成功率仍偏低（~28%）
5. 未分析语言编码器的遗忘问题


## Key Takeaways

- VLA 模型的视觉编码器在机器人数据微调时会发生严重灾难性遗忘
- 渐进式参数回退是简单有效的缓解策略，无需修改训练流程
- DINO-v2 和 SigLIP 的联合回退产生互补效果
- 视觉泛化能力是 VLA 在 OOD 任务上的关键瓶颈
- 预训练视觉表征的知识保留对机器人策略学习至关重要

## 相关概念

- [[vision-language-model]]
- [[imitation-learning]]

## 相关研究者

- [[dey|Dey, Sombit]]
- [[zaech|Zaech, Jan-Nico]]
- [[nikolov|Nikolov, Nikolay]]
