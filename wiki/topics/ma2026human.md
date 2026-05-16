---
title: "Robot learning from human videos: A survey"
tags: [manipulation, imitation, robot-learning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数据集和视频生成方案"
authors: "Ma, Junyi; Zhang, Erhang; Yang, Haoran; Li, Ditao; Xu, Chenyang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "V692E6A7"
---
## 摘要

A critical bottleneck hindering further advancement in embodied AI and robotics is the challenge of scaling robot data. To address this, the field of learning robot manipulation（机器人操控） skills from human video data has attracted rapidly growing attention in recent years, driven by the abundance of human activity videos and advances in computer vision. This line of research promises to enable robots to acquire skills passively from the vast and readily available resource of human demonstrations, substantially favoring scalable learning for generalist robotic systems. Therefore, we present this survey to provide a comprehensive and up-to-date review of human-video-based learning techniques in robotics, focusing on both human-robot skill transfer and data foundations. We first review the policy learning foundations in robotics, and then describe the fundamental interfaces to incorporate human videos. Subsequently, we introduce a hierarchical taxonomy of transferring human videos to robot skills, covering task-, observation-, and action-oriented pathways, along with a cross-family analysis of their couplings with different data configurations and learning paradigms. In addition, we investigate the data foundations including widely-used human video datasets and video generation schemes, and provide large-scale statistical trends in dataset development and utilization. Ultimately, we emphasize the challenges and limitations intrinsic to this field, and delineate potential avenues for future research. The paper list of our survey is available at https://github.com/IRMVLab/awesome-robot-learning-from-human-videos.

## 中文简述

提出基于模仿学习的操控方法，具有人类视频学习特点。

**研究方向**: 机器人操控、模仿学习、机器人学习

## 关键贡献

1. **提出三层 skill transfer 分类法**：将人类视频到机器人技能的迁移方法系统性地分为 Task-Oriented、Observation-Oriented、Action-Oriented 三个层次
2. **跨族分析**：分析不同 transfer 路径与数据配置、学习范式的耦合关系
3. **数据基础综述**：汇总 50+ 开源人类视频数据集，提供大规模统计数据集发展趋势
4. **视频生成方案梳理**：综述利用视频生成技术合成人类视频用于机器人学习的方法
5. **维护活跃论文列表**：GitHub 仓库持续更新，按分类法组织 200+ 篇相关论文
## 结构化提取

- Problem: 机器人数据规模化瓶颈 → 利用海量人类视频被动学习机器人操控技能
- Method: 系统综述 + 三层分类法（Task-Oriented / Observation-Oriented / Action-Oriented），辅以数据基础和 HOI 分析工具梳理
- Tasks: 机器人操控（抓取、放置、工具使用、双臂协作、灵巧操控）；不限于特定任务类型
- Sensors: RGB 视频（主要输入）；部分方法使用深度、触觉（如 Visual-Tactile Pretraining）
- Robot Setup: 涵盖多种机器人平台——机械臂、灵巧手、人形机器人、移动操控平台；单臂和双臂
- Metrics: 综述无统一指标；各被引方法使用任务成功率、泛化能力、zero-shot 成功率等
- Limitations: 人-机器人形态差异、动作空间鸿沟、数据噪声、评估标准化不足、Sim-to-Real 差距
- Evidence Notes: 基于摘要和 GitHub 完整论文列表分析；缺少全文中的定量对比表格和统计图；分类体系和方法概述基于摘要描述和 GitHub 分类结构推断，与正文一致性高
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: partial（PDF 下载不完整，基于摘要 + GitHub 完整论文列表分类法完成分析）
- Evidence Coverage: medium-high（摘要覆盖研究动机、分类体系、数据基础；GitHub 提供完整论文列表和分类结构；缺少正文详细方法论讨论和实验对比表格）
- Confidence: medium-high
- Summary: 系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数据集和视频生成方案


## Problem

机器人数据规模化的瓶颈限制了 embodied AI 和机器人的进一步发展。人类活动视频作为海量、易获取的数据源，能否被动地让机器人从中习得操控技能？核心挑战包括：

1. **数据规模化瓶颈**：机器人示范数据采集成本高、多样性有限
2. **人-机器人跨体态鸿沟**：人类和机器人在形态、自由度、感知方式上存在本质差异
3. **缺乏统一分类体系**：现有工作散落在不同层面（任务、观测、动作），缺乏系统性的梳理和对比


## Method

综述性论文，核心贡献是提出了一个层次化的分类体系（hierarchical taxonomy）：

### 1. Policy Learning Foundations
回顾机器人策略学习基础，描述如何将人类视频纳入机器人学习的基本接口。

### 2. Human-Robot Skill Transfer 三层分类法

**Task-Oriented Transfer（任务导向迁移）**
- 从人类视频中提取任务结构和意图，指导机器人在任务层面做决策
- **Task structures**：提取任务分解、子任务序列、操作程序（如 Chain-of-Modality, GPT-4V for Robotics, VLMimic）
- **Task intents**：推断人类演示的目标和意图（如 BC-Z, XSkill, One-Shot Imitation）
- 代表方法：利用 VLM/LLM 从视频中提取任务计划，生成可执行的动作序列

**Observation-Oriented Transfer（观测导向迁移）**
- 弥合人-机器人之间的视觉域差距，使机器人能利用人类视频的视觉信息
- **Transformed videos**：将人类视频编辑/转换为机器人视角视频（如 Masquerade, Phantom, MimicDreamer, AR2-D2, RoboTube）
- **Visual embeddings**：学习共享的视觉表征（如 R3M, VIP, LIV, EgoBridge, GR-2）
- 关键工具：域适应、视觉预训练、视频条件策略学习

**Action-Oriented Transfer（动作导向迁移）**
- 从人类视频中提取可执行的动作知识
- **Affordances**：提取交互位姿、抓取点、操作轨迹（如 OKAMI, R+X, ZeroMimic, DemoDiffusion, EgoZero）
- **Latent actions**：从视频中学习隐式动作表征（如 LAPA, UniVLA, Moto, CLAP, VLA-JEPA, LDA-1B）
- 近年热点：VLA（Vision-Language-Action）模型的大规模预训练

### 3. 数据基础

**开源人类视频数据集（50+）**：
- 第一视角（Ego）：Ego4D, EPIC-KITCHENS, EgoDex, HO-Cap, HoloAssist, UniHand 系列
- 第三视角（Exo）：Kinetics-700, Something-Something, Breakfast, ActivityNet
- 混合视角（Ego+Exo）：Ego-Exo4D, RH20T-Human, TACO, ARCTIC, OakInk2
- 趋势：数据集规模从早期的小规模（<10h）发展到现在的百万级视频（Panda-70M, EgoVid-5M, Action100M）

**视频生成方案**：
- 利用扩散模型生成合成人类视频用于策略学习
- 代表工作：Gen2Act, Dreamitate, NovaFlow, Universal Policy via Text-Guided Video Generation

### 4. HOI 分析技术
- 手部检测与重建：MediaPipe Hands, FrankMocap, HaWoR, WiLoR
- 6D 位姿估计：FoundationPose, MegaPose, Any6D
- 点追踪：CoTracker, SpatialTracker, TAPIR
- 3D 重建：BundleSDF, InstantMesh, SAM 3D Body


## Experiments

综述论文无独立实验，但基于 GitHub 论文列表可以观察到以下统计趋势：

**时间分布**：
- 2015-2021：早期探索，年均 <5 篇
- 2022-2023：快速增长，约 20 篇/年
- 2024：爆发期，40+ 篇
- 2025-2026：持续高速增长，2025 年已超 60 篇，2026 年前 4 个月已超 25 篇

**方法分布**（基于论文列表统计）：
- Action-Oriented（Affordances + Latent actions）：占比最大，约 60%+
- Observation-Oriented：约 20%
- Task-Oriented：约 15%
- 数据/HOI 工具：约 5%

**发表趋势**：
- 顶会集中：CoRL、ICRA、CVPR、RSS、NeurIPS、ICLR 是主要发表场所
- 双臂/灵巧操控方向增长明显
- VLA 模型结合人类视频是 2025-2026 最热门方向

**缺失证据**：
- 正文中的定量对比表格和 benchmark 汇总（因缺少全文无法提取）
- 具体的数据集规模对比统计图
- 跨方法的系统性性能对比


## Limitations

1. **人-机器人形态差异**：手部 vs 夹爪、人形 vs 非人形机器人的迁移仍是开放问题
2. **动作空间鸿沟**：人类视频不包含机器人动作标签，需要通过 affordance/latent action 间接获取
3. **数据质量**：互联网视频噪声大、视角不一致、缺少精确标注
4. **评估标准化**：不同方法使用不同的评估指标和实验设置，难以公平比较
5. **Sim-to-Real 差距**：部分方法依赖仿真环境验证，真实世界泛化能力不确定
6. **综述本身的局限性**：领域发展极快，部分最新工作可能未收录


## Key Takeaways

1. **对 DLO 操控的启示**：Action-Oriented Transfer 中的 affordance 方法（如点轨迹追踪）和 latent action 方法可直接应用于柔性物体操控，但目前专门处理 DLO 的人类视频学习方法极少
2. **VLM/VLA 是核心趋势**：2025-2026 年大量工作将 VLM/VLA 与人类视频学习结合，如 Being-H0、EgoVLA、CLAP、UniVLA 等，这为基于 VLM 的机器人控制提供了丰富的数据增强路径
3. **第一视角数据集的爆发**：Ego4D、Ego-Exo4D 等大规模 ego-centric 数据集为从人类视角学习操控技能提供了前所未有的数据基础
4. **Latent Action 是关键突破口**：从人类视频学习无需动作标注的隐式动作表征（LAPA, Moto, VLA-JEPA）正在解决"视频无动作标签"的核心问题
5. **视频生成作为数据增强**：利用扩散模型生成合成人类视频是新兴方向，可缓解数据稀缺问题
6. **与我们研究的交叉点**：Obs-Oriented 的 transformed videos 方法（如 Phantom, Masquerade）与 Sim-to-Real 有天然联系；Action-Oriented 的 affordance 方法可直接服务于 DLO 操控中的交互点识别

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[ma-junyi|Ma, Junyi]]
