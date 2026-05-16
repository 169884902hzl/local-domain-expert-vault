---
title: "Vision-language-action in robotics: A survey of datasets, benchmarks, and data engines"
tags: [imitation, VLM, sim-to-real, robot-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈"
authors: "Wang, Ziyao; Wang, Bingying; Zhang, Hanrong; Du, Tingting; Chen, Tianyang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZN75VF2E"
---
## 摘要

Despite remarkable progress in Vision--Language--Action (VLA) models, a central bottleneck remains underexamined: the data infrastructure that underlies embodied learning. In this survey, we argue that future advances in VLA will depend less on model architecture and more on the co-design of high-fidelity data engines and structured evaluation protocols. To this end, we present a systematic, data-centric analysis of VLA research organized around three pillars: datasets, benchmarks, and data engines. For datasets, we categorize real-world and synthetic corpora along embodiment（具身） diversity, modality composition, and action space formulation, revealing a persistent fidelity-cost trade-off that fundamentally constrains large-scale collection. For benchmarks, we analyze task complexity and environment structure jointly, exposing structural gaps in compositional generalization and long-horizon（长时序） reasoning evaluation that existing protocols fail to address. For data engines, we examine simulation-based, video-reconstruction, and automated task-generation paradigms, identifying their shared limitations in physical grounding and sim-to-real（仿真到真实迁移） transfer. Synthesizing these analyses, we distill four open challenges: representation alignment, multimodal（多模态） supervision, reasoning assessment, and scalable data generation. Addressing them, we argue, requires treating data infrastructure as a first-class research problem rather than a background concern.

## 中文简述

提出基于模仿学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、视觉-语言模型、仿真到真实迁移、机器人学习

## 关键贡献

1. **统一的数据中心分类法**：将 VLA 研究组织为数据集、基准和数据引擎三大类别，明确各自在训练、评估和可扩展数据生产中的角色
2. **二维基准分析框架**：提出任务复杂度 × 环境结构的二维特征化方法（Figure 3），用于系统分析基准设计
3. **跨组件结构挑战识别**：识别三个贯穿所有组件的结构性挑战——表示对齐、长时序组合任务评估、保持物理真实性的可扩展数据生成
4. **持续更新的社区资源**：发布 GitHub 仓库 https://github.com/ziyaow1010/vla-datasets-benchmarks
## 结构化提取

- **Problem**: VLA 系统的数据基础设施（数据集、基准、数据引擎）不完善，存在 fidelity-cost trade-off、推理评估空白和生成-接地失衡
- **Method**: 以数据为中心的系统分析框架，将 VLA 研究组织为三大支柱（数据集/基准/数据引擎），使用二维特征化方法（任务复杂度 × 环境结构）分析基准
- **Tasks**: 机器人操控（抓取、推动、长时序组合任务、家庭活动等），不涉及导航和驾驶
- **Sensors**: RGB 图像（所有数据集）、RGB-D（RH20T、UMI、DexCap）、视频（Ego4D）、触觉/力（RH20T）、音频（RH20T）
- **Robot Setup**: 涵盖 22+ 种机器人平台（Franka Panda、Everyday Robots、WidowX 250、人形机器人、灵巧手等）
- **Metrics**: 任务成功率（SR）为主，部分使用 progress-based scores；CALVIN 使用序列成功率；RoboGen 使用 69 任务平均成功率
- **Limitations**: (1) 仅覆盖操控领域；(2) 缺乏统一定量元分析；(3) 对 DLO/可变形物体覆盖不足；(4) 数据引擎质量评估缺乏标准化指标
- **Evidence Notes**:

  - Table 1 对比 12 个 VLA 数据集（7 真实 + 4 合成 + 1 人类视频）
  - Table 2 对比 24 个 VLA 数据引擎（6 视频到数据 + 5 硬件辅助 + 13 生成式）
  - Figure 3 提供基准的二维定位图
  - 引用的关键定量数据来自各原论文（非原创实验）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv MCP 获取完整 17 页 PDF）
- Evidence Coverage: 全面覆盖所有章节（Introduction, Preliminaries, Datasets, Benchmarks, Data Engines, Open Problems, Conclusion）
- Confidence: high
- Summary: 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈


## Problem

VLA 模型虽然在架构上取得显著进展，但制约其发展的核心瓶颈在于**数据基础设施**（数据集、基准、数据引擎），而非模型设计本身。具体问题包括：

1. **数据集层面**：真实世界数据采集成本高、难规模化，合成数据保真度不足，两者之间存在持久的 fidelity-cost 权衡
2. **基准层面**：缺乏标准化评估协议，不同工作使用不同任务定义和成功标准；长时序推理和组合泛化能力的评估存在结构性空白
3. **数据引擎层面**：生成能力快速扩展，但物理接地（physical grounding）和 embodiment 对齐滞后


## Method

### 整体框架

以数据为中心（data-centric）的视角，将 VLA 研究划分为三大支柱：

### 1. VLA 数据集（Section 3）

**真实世界数据集**（Table 1）：
- **Open X-Embodiment**：22 种机器人，跨平台聚合，适合预训练
- **RT-1/RT-2**：单平台，数据一致性好，适合微调
- **DROID**：Franka Panda，强调视觉和环境多样性
- **BridgeData V2**：WidowX 250，低成本标准化
- **RH20T**：4 种机器人，多模态（触觉/力/音频）
- **Ego4D**：人手交互数据，语义先验

**合成数据集**：
- **SynGrasp-1B**：大规模抓取合成（10 亿级）
- **RoboCasa**：厨房场景仿真套件
- **RoboGen**：LLM 生成任务代码
- **MimicGen**：示范增强

**关键分析维度**：embodiment 多样性、动作表示（EEF vs DoF, 绝对 vs delta）、模态组成

**核心发现**：所有真实数据集都面临 fidelity-cost trade-off，合成数据存在 sim-to-real gap

### 2. VLA 基准（Section 4）

**二维分析框架**：
- 横轴：任务复杂度（短时序原子操作 → 长时序组合推理）
- 纵轴：环境结构（受约束桌面 → 多场景多样环境）

**桌面基准**：
- 简单型：Meta-World（50 任务）、LIBERO、SimplerEnv
- 复杂长时序型：CALVIN（5 步指令成功率仅 0.08%）、GemBench、COLOSSEUM

**多场景基准**：
- BEHAVIOR-1K：1000 种日常活动，全屋环境
- VLABench：长时序多步推理 + 场景语义
- Open X-Embodiment：跨 embodiment 评估

**核心空白**：缺乏结构化框架来评估 VLA 系统的推理能力，特别是时序组合、多因素变异和跨 embodiment 迁移的联合评估

### 3. VLA 数据引擎（Section 5, Table 2）

**视频到数据引擎**（Video-to-Data）：
- **H2R**：手→机器人重定向 + inpainting，成功率提升 1.3–10.2%
- **RoboWheel**：物理感知 SDF + 残差 RL
- **Video2Policy**：GPT-4o 生成可执行任务代码，88% 仿真成功率
- **X-Humanoid**：视频扩散模型"机器人化"全身运动
- **GenMimic**：零样本从视频生成模型迁移
- **UniSim**：条件视频扩散世界模型，3–4× 性能提升

**硬件辅助引擎**：
- **ALOHA**：双臂遥操作，<$20k，80–90% 成功率
- **GELLO**：3D 打印外骨骼，~$300，可靠性提升 30%
- **UMI**：GoPro + SLAM，3× 采集速度，71.7% 零样本成功率
- **DexCap**：EMF 手套 + RGB-D，灵巧操作 72% 成功率
- **Lucid-XR**：VR 头显 + 物理仿真 + 扩散渲染，5× 有效数据

**生成式数据引擎**：
- 轨迹复用：MimicGen（50k 示范 from 200 种子）、DynaMimicGen、DemoGen
- LLM 驱动：GenSim、RoboGen（77.4% 平均成功率，69 任务）、RoboTwin 2.0（100k+ 轨迹）
- 视觉增强：ROSIE（115%+ 提升）、RoboEngine、EMMA
- 预测世界模型：PointWorld、IRASim、3D-VLA、Genie

**核心局限**：数据生成速度远超物理接地和验证能力


## Experiments

本综述不包含原创实验。其主要实证贡献为：

1. **Table 1**：12 个代表性 VLA 数据集的系统对比（embodiment、模态、动作空间、关键特征）
2. **Table 2**：24 个 VLA 数据引擎的系统对比（输入源、是否需要真实机器人、人工需求、Sim2Real、关键特征）
3. **Figure 3**：任务复杂度 × 环境结构的基准二维定位图
4. **定量证据引用**：
   - CALVIN 5 步指令成功率：0.08%
   - ALOHA 双臂操作成功率：80–90%
   - UMI 零样本成功率：71.7%
   - Video2Policy 仿真成功率：88%（100+ 视频）
   - RoboGen 平均成功率：77.4%（69 任务）
   - ROSIE 整体性能提升：>115%
   - UniSim 闭环训练：3–4× 性能提升

**缺失证据**（综述中未提供但用户可能期望的）：
- 各引擎的直接对比实验（同一任务、同一基准）
- Sim-to-Real 迁移的定量对比分析
- 不同数据引擎组合策略的效果评估


## Limitations

1. **综述范围限制**：仅涵盖机器人操控领域，不包括自动驾驶和移动导航
2. **缺乏定量元分析**：没有对不同方法进行统一的实验对比，主要依赖各原论文报告的数据
3. **时效性**：VLA 领域发展迅速，部分 2025-2026 年的工作可能未涵盖
4. **数据引擎评估不足**：对数据引擎的"可靠性"评估主要停留在定性描述，缺乏标准化的引擎质量指标
5. **对 DLO 操控的覆盖有限**：虽然提到可变形材料和接触丰富操作，但没有专门讨论 DLO/线材操控的数据和基准


## Key Takeaways

1. **对我们研究方向（DLO 操控）的启示**：
   - 现有 VLA 数据集中 DLO 相关数据极度匮乏，RH20T 是唯一包含触觉/力信息的多模态数据集
   - 数据引擎（特别是生成式引擎）为 DLO 数据扩充提供了路径，但物理接地是关键瓶颈
   - 桌面基准（LIBERO、Meta-World）主要针对刚性物体，DLO 操控需要新的基准设计

2. **对 VLM-based 控制的启示**：
   - VLA 的核心挑战已从模型架构转向数据基础设施
   - 视频到数据引擎（如 H2R、Video2Policy）为利用大规模人类视频提供了可行路径
   - 世界模型（如 UniSim、IRASim）支持闭环训练，对长时序任务尤其重要

3. **对 Sim-to-Real 的启示**：
   - 合成数据的保真度仍是核心瓶颈
   - 高保真场景重建（将真实场景数字化到仿真中）是有前景的方向
   - 需要数据引擎和基准的协同设计

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wang-ziyao|Wang, Ziyao]]
