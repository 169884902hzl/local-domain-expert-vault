---
title: "JoyAI-RA 0.1: A foundation model for robotic autonomy"
tags: [manipulation, VLM, robot-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控，在 RoboTwin 2.0、RoboCasa GR1 和真实 AgiBot G1 评测中全面超越 π0.5 和 Motus。"
authors: "Zhang, Tianle; Yuan, Zhihao; Chi, Dafeng; Liu, Peidong; Li, Dongwei et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "S5HGTPQ8"
---
## 摘要

Robotic autonomy in open-world environments is fundamentally limited by insufficient data diversity and poor cross-embodiment（具身） generalization. Existing robotic datasets are often limited in scale and task coverage, while relatively large differences across robot embodiments impede effective behavior knowledge transfer. To address these challenges, we propose JoyAI-RA, a vision-language-action (VLA) embodied foundation model tailored for generalizable robotic manipulation（机器人操控）. JoyAI-RA presents a multi-source multi-level pretraining（预训练） framework that integrates web data, large-scale egocentric human manipulation（操控） videos, simulation-generated trajectories, and real-robot data. Through training on heterogeneous multi-source data with explicit action-space unification, JoyAI-RA effectively bridges embodiment（具身） gaps, particularly between human manipulation（操控） and robotic control, thereby enhancing cross-embodiment（具身） behavior learning. JoyAI-RA outperforms state-of-the-art（现有最优方法） methods in both simulation and real-world benchmarks, especially on diverse tasks with generalization demands.

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、机器人学习

## 关键贡献

1. 提出 JoyAI-RA，一个面向通用机器人操控的 VLA 基础模型
2. 设计多源多级预训练框架，统一整合网页数据、大规模自我中心人类操作视频（EgoLive）、仿真轨迹和真机演示数据
3. 通过统一动作空间（camera-frame end-effector + 固定维度 action masking）桥接具身鸿沟，配合三阶段训练范式实现有效跨源知识迁移
## 结构化提取

- Problem: 开放世界机器人操控的数据多样性不足和跨具身泛化困难
- Method: VLM backbone + Perceiver-based action expert，统一动作空间（camera-frame 6-DoF + 固定维度 masking），三阶段训练（VLM Co-Pretrain → VLA Co-Pretrain → Post-Train），flow matching 连续动作生成
- Tasks: 双臂操控（RoboTwin 2.0 50 任务）、灵巧手操控（RoboCasa GR1 24 任务）、真实世界 6 任务（办公室/茶几/厨房/餐桌/药房）
- Sensors: 多视角 RGB 相机，本体感知（关节状态）
- Robot Setup: AgiBot G1 人形机器人、ALOHA、Fourier、GR1（仿真）
- Metrics: 任务成功率（%），每个任务 20-50 次 rollout 取平均
- Limitations: 长时序精确推理弱、协调密集型操控受限、in-domain 数据分布不匹配时有害、未报告参数量和推理速度、未在非 JD 平台验证
- Evidence Notes: 全文可读，实验数据完整包含逐任务分解和详细消融。附录提供完整 RoboTwin 2.0 逐任务结果（Table A/C）、RoboCasa 逐任务结果（Table B）和真实世界任务描述（Appendix B）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文可读，包含实验、消融、附录详细数据）
- Confidence: high
- Summary: 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控，在 RoboTwin 2.0、RoboCasa GR1 和真实 AgiBot G1 评测中全面超越 π0.5 和 Motus。


## Problem

开放世界机器人自主操控面临两大核心瓶颈：
1. **数据多样性不足**：现有机器人数据集规模和任务覆盖有限，无法覆盖长尾交互和场景多样性
2. **跨具身泛化困难**：不同机器人平台之间形态差异大，行为知识迁移效果差，特别是人类操作视频到机器人控制之间的具身鸿沟


## Method

### 整体架构
- **VLM Backbone**: 处理视觉-语言理解，输出多模态表征
- **Perception-Action Expert**: 基于 Perceiver 架构，通过 latent bottleneck 进行高效多模态融合，生成连续动作序列
- 语义理解与低层控制解耦设计

### 统一动作空间
- **Camera-Frame End-Effector 表示**: 将末端执行器状态和动作统一到相机坐标系，6-DoF 分解为 3D 平移 + 3D 轴角旋转
- **统一动作维度**: 固定长度动作向量覆盖左右臂、左右灵巧手、左右夹爪等所有执行器组；无对应自由度的维度在 loss 中 mask，支持从单臂夹爪到双臂灵巧手系统的跨形态训练

### 三阶段训练
1. **VLM Co-Pretraining**: 在多模态网页数据 + 具身 VQA + 跨具身动作数据（FAST token）+ 人类视频上训练视觉-语言先验
2. **VLA Co-Pretraining**: 引入 flow matching loss，在仿真轨迹 + 真机演示 + 重定向人类视频上学习连续动作生成，保留 VLM 能力
3. **Post-Training**: 仅用目标真机数据端到端微调，仅优化 flow matching loss

### 动作生成
- Flow matching 框架下的条件速度场预测
- 时间自适应 AdaLN 调制视觉-语言特征
- Perceiver attention 残差机制融合视觉-语言上下文与动作 latent


## Experiments

### 仿真评测

**RoboTwin 2.0（双臂操控，50 任务）**:
| Method | Easy (%) | Hard (%) |
|--------|----------|----------|
| π0 | 65.92 | 58.40 |
| π0.5 | 82.74 | 76.76 |
| Motus | 88.66 | 87.02 |
| LingBot-VLA | 88.56 | 86.68 |
| **JoyAI-RA** | **90.48** | **89.28** |

**RoboCasa GR1 Tabletop（24 任务，6DoF 灵巧手）**:
| Method | SR (%) |
|--------|--------|
| GR00T-N1.6 | 47.6 |
| ABot-M0 | 58.3 |
| **JoyAI-RA** | **63.2** |

### 真实世界评测
- **平台**: AgiBot G1 人形机器人
- **场景**: 办公室、茶几、厨房、餐桌、药房（6 个任务）
- **结果**: 平均成功率 0.74 vs π0.5 的 0.62
- 在 Headphones 和 Remedy 任务上优势最大（语义定位和精确放置）
- Cup 和 Croissant（长时序精确推理）仍弱于 π0.5

### 消融实验
1. **EgoLive 数据消融**: Full EgoLive + JDAgibot → 87.42% vs 无预训练 81.64%，10% 子集仅 81.40%，说明需要足够规模
2. **EgoLive vs EgoDex**: EgoLive 87.16% vs EgoDex 86.88%，联合使用 89.30%（互补）
3. **两阶段共训练**: VLM+VLA 联合 → 90.48%，单独 VLM 87.84%，单独 VLA 87.42%
4. **仿真数据**: VLA 阶段加仿真 → +1.14%
5. **In-domain EgoLive**: 对对齐任务有效（Remedy、Headphones），对不匹配任务可能有害（Mouse、Food Scraps）


## Limitations

1. 长时序精确视觉推理和分级顺序操控仍有挑战（Cup、Croissant 任务不如 π0.5）
2. 低层执行敏感性和协调密集型操控（如 Food Scraps）仍受 egocentric 数据之外的因素制约
3. In-domain 人类数据在分布不匹配时可能引入冲突信号
4. 论文未报告模型参数量、推理速度和计算开销
5. 未在非 JD 平台（如 Franka、UR5）上验证，泛化性仅限于所测平台


## Key Takeaways

1. **多源异构预训练是有效的**: 网页 → 人类视频 → 仿真 → 真机的渐进式训练策略显著优于单源训练
2. **EgoLive 人类视频的关键贡献**: 在空间推理和多步结构化任务上提供可迁移先验，且效果随规模增长未饱和
3. **统一动作空间设计实用**: camera-frame 表示 + action masking 是一种简洁有效的跨具身方案，可借鉴到 DLO 操控的跨平台适配中
4. **对 DLO 操控的启示**: 多源预训练框架可扩展纳入 DLO 仿真和人类操作视频；flow matching + Perceiver 架构可能适合 DLO 轨迹的连续生成
5. **三阶段训练范式值得参考**: VLM 预训练 → VLA 共训练 → 目标平台后训练的分层策略可复用到新任务领域

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhang-tianle|Zhang, Tianle]]
