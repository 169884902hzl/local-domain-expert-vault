---
title: "PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World"
tags: [3D-generation, VLM, diffusion-model, physics-simulation, embodied-AI]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。"
authors: "Yang, Yunhan; Wang, Chunshi; Ye, Junliang; Li, Yang; Chen, Zanxin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "UUE7SHDT"
---
## 摘要

Synthesizing physics-grounded 3D assets is a critical bottleneck for interactive virtual worlds and embodied AI. Existing methods predominantly focus on static geometry, overlooking the functional properties essential for interaction. We propose that interactive asset generation must be rooted in functional logic and hierarchical physics. To bridge this gap, we introduce PhysForge, a decoupled two-stage framework supported by PhysDB, a large-scale dataset of 150,000 assets with four-tier physical annotations. First, a VLM acts as a "physical architect" to plan a "Hierarchical Physical Blueprint" defining material, functional, and kinematic constraints. Second, a physics-grounded diffusion model（扩散模型） realizes this blueprint by synthesizing high-fidelity geometry alongside precise kinematic parameters via a novel KineVoxel Injection (KVI) mechanism. Experiments demonstrate that PhysForge produces functionally plausible, simulation-ready assets, providing a robust data engine for interactive 3D content and embodied agents.

## 中文简述

提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。

**研究方向**: 3D 生成、视觉-语言模型、扩散模型、物理仿真、具身智能

## 关键贡献

1. **框架设计**: 提出解耦的"VLM 规划 + 扩散生成"两阶段框架 PhysForge，实现从单张图片生成物理完备的 3D 资产
2. **大规模数据集**: 构建 PhysDB，包含 15 万个具有四层级物理标注的 3D 资产（整体属性、静态属性、功能属性、交互属性）
3. **KineVoxel Injection (KVI)**: 提出将运动学参数编码为特殊体素（KineVoxel），在扩散去噪过程中与几何体素联合生成
4. **实验验证**: 在规划和生成任务上达到 SOTA，并展示在机器人仿真器和虚拟世界中的直接应用
## 结构化提取

- Problem: 现有 3D 生成方法只关注静态几何，忽视交互所需的功能和物理属性，导致生成的资产无法在仿真环境中使用
- Method: 两阶段解耦框架：(1) VLM (Qwen2.5-VL 微调) 规划层级物理蓝图；(2) 扩散模型 + KineVoxel Injection 联合生成几何、纹理和运动学参数
- Tasks: 物理感知的部分级 3D 资产生成（单图输入 → 带材料、功能、运动学属性的交互式 3D 资产）
- Sensors: 单张 RGB 图像（可选 2D 掩码）
- Robot Setup: 下游验证使用 RoboTwin 双臂机器人仿真器；无真实机器人实验
- Metrics: Chamfer Distance (CD)、F1-Score、BBox IoU、Voxel Recall/IoU、Joint Axis Error、Joint Pivot Error、CLIP Similarity、物理属性 MAE
- Limitations: 大规模数据集缺少精确关节参数；依赖外部数据集训练运动学；两阶段误差传播；无推理效率分析
- Evidence Notes:

  - 物理属性生成全面超越 PhysXGen 和 TRELLIS（Table 1, 2）
  - 部件规划在 PartObjaverse-Tiny 上达到 77.16% Voxel Recall，超过 OmniPart（Table 3）
  - 铰接物体关节精度大幅超越 Articulate Anything 等方法（JAE-5: 0.101 vs 0.608）（Table 4）
  - 消融实验确认关节类型嵌入和独立运动学编码器均不可或缺
  - 下游应用仅在仿真器中定性展示，无定量评估
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete
- Confidence: high
- Summary: 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。

## Problem

现有 3D 生成方法只关注静态几何和纹理，忽视交互所需的功能属性。生成的"空壳"资产无法被抓取、推动或操控，难以直接部署到具身 AI 仿真器或游戏环境中。

## Method

### Stage 1: VLM-based Planning（物理蓝图规划）
- 基于 Qwen2.5-VL 微调，作为"物理架构师"
- 输入: 单张图片 + TRELLIS 生成的 3D 体素 + 可选 2D 掩码
- 体素特征提取: PartField 编码器 → 位置感知 3D 卷积网络 → 512 维嵌入
- 引入 66 个新特殊 token 用于 3D 边界框坐标量化编码
- 输出: **层级物理蓝图**（Hierarchical Physical Blueprint），包括:
  - 每个部件的边界框布局
  - 材料属性（如金属、木材）
  - 功能属性（如"容纳"、"控制"）和状态机
  - 运动学定义：父部件、关节类型（revolute/continuous/prismatic/fixed）
- 关键发现: 物理属性引导规划显著解决部件粒度歧义，即使无 2D 掩码也能产生语义合理的部件分解

### Stage 2: Diffusion-based Generation with KVI（扩散生成）
- 扩展 OmniPart 第二阶段框架
- 运动学参数表示: P_i = (O_i, A_i, L_i)，其中 O_i ∈ R³（关节原点），A_i ∈ R³（关节轴），L_i ∈ R²（运动范围）
- **KineVoxel 机制**:
  - 独立的 Kinematic Encoder (E_kine) 和 Decoder (D_kine)，均为 2 层 MLP
  - 将运动学参数映射到与几何体素共享的潜在空间
  - 在下采样后将 KineVoxel 与几何体素序列拼接，注入中间 Transformer
  - 添加关节类型嵌入 E_type 来自 VLM 规划的关节类型（如 revolute、prismatic）
- 训练损失: Conditional Flow Matching (CFM)
  - L = E[L_geo + λ_kine · L_kine]，其中 λ_kine = 10
  - 几何和运动学分别计算 L2 损失

### PhysDB 数据集
- 来源: Objaverse，覆盖 7 大类（家居、工业、武器、个人、车辆、科技电子、文化物品）
- 15 万个 3D 对象
- 四层级标注体系:
  1. **整体层**: 真实世界尺度、物体类别、使用场景
  2. **静态属性层**: 语义标签、物理材料、质量
  3. **功能层**: 内在功能（如"容纳"）、状态机（如 [open, closed]）
  4. **交互层**: 原子 affordance（如 pushable、graspable）、完整运动学定义
- 标注管线: 多模态 LLM 初始标注 + 人工筛查修正
- 运动学训练补充: PartNet-Mobility 和 Infinite-Mobility 提供精确关节参数

## Experiments

### 评估数据集
- PartObjaverse-Tiny (200 物体)
- PhysXNet 测试集 (1000 物体)
- PhysDB 测试集 (1000 物体)
- PartNet-Mobility + Infinite-Mobility 铰接物体 (340 物体)

### Table 1: 物理属性生成 (PhysXNet 测试集)
| 方法 | CD↓ | F1-0.1↑ | F1-0.05↑ | Scale(cm)↓ | Material↓ | Afford.↓ | Desc↑ |
|------|-----|---------|----------|------------|-----------|---------|-------|
| TRELLIS | 10.10 | 86.53 | 72.47 | - | - | - | - |
| PhysXGen | 9.81 | 87.91 | 73.60 | 25.83 | 1.59 | 3.69 | 0.38 |
| **PhysForge** | **9.21** | **89.24** | **75.43** | **11.04** | **0.81** | **1.22** | **0.87** |

### Table 2: 物理属性生成 (PhysDB 测试集)
| 方法 | CD↓ | F1-0.1↑ | F1-0.05↑ | Scale(m)↓ | Material↓ | Function↑ | Interaction↑ |
|------|-----|---------|----------|-----------|-----------|----------|-------------|
| TRELLIS | 24.32 | 68.19 | 53.28 | - | - | - | - |
| PhysXGen | 25.30 | 65.79 | 50.57 | 1.08 | 1.44 | 0.36 | 0.34 |
| **PhysForge** | **22.89** | **70.51** | **55.38** | **0.37** | **0.43** | **0.83** | **0.96** |

### Table 3: 部件结构规划 (PartObjaverse-Tiny, %)
| 方法 | Voxel Recall↑ | Voxel IoU↑ | Bbox IoU↑ |
|------|--------------|-----------|----------|
| PartField | 69.65 | 46.04 | 37.33 |
| OmniPart (SAM mask) | 68.33 | 43.34 | 34.33 |
| PhysForge-bbox (w/o mask) | 67.89 | 35.53 | 32.30 |
| PhysForge (w/o mask) | 73.63 | 47.66 | 36.32 |
| OmniPart | 73.79 | 52.92 | 41.66 |
| **PhysForge (Ours)** | **77.16** | **53.74** | **42.95** |

### Table 4: 铰接物体生成 (340 铰接物体)
| 方法 | CD↓ | Clip-Sim↑ | JAE-5↓ | JPE-5↓ | JAE-all↓ | JPE-all↓ |
|------|-----|----------|--------|--------|---------|---------|
| Articulate Anything | 23.31 | 0.87 | 0.608 | 0.257 | 0.694 | 0.197 |
| Singapo | 21.10 | 0.85 | 0.241 | 0.153 | - | - |
| URDFormer | 25.42 | 0.84 | 0.781 | 0.652 | - | - |
| PhysForge (w/o jt emb) | 10.73 | 0.90 | 0.157 | 0.132 | 0.292 | 0.141 |
| PhysForge (w/o kin enc) | 11.31 | 0.89 | 0.158 | 0.117 | 0.204 | 0.120 |
| **PhysForge** | **10.21** | **0.93** | **0.101** | **0.071** | **0.164** | **0.096** |

### 消融实验关键发现
1. 关节类型嵌入是两阶段的关键接口：移除后 Stage 2 无法解决运动学歧义
2. 独立运动学编码器/解码器对精确关节参数至关重要
3. 物理属性引导规划（w/o mask vs PhysForge-bbox w/o mask）显著提升部件分解质量

### 下游应用展示
- 机器人仿真: 导入 RoboTwin 仿真器，机械臂可操控资产生成的功能部件
- 虚拟世界: 导入 Unity/UE，支持复杂物理交互，无需手动 rigging
- Agent 交互: 具身智能体可通过自然语言查询物理蓝图，规划操控任务

## Limitations

1. PhysDB 在 15 万规模上仅标注关节类型，不提供精确数值关节参数；运动学训练依赖外部数据集（PartNet-Mobility、Infinite-Mobility）
2. 两阶段管线存在误差传播风险：VLM 规划错误会直接影响扩散生成质量
3. 依赖 TRELLIS 第一阶段的体素重建质量
4. 论文未提供运行时间/推理效率分析
5. 物理标注管线涉及多模态 LLM + 人工修正，可扩展性受限

## Key Takeaways

1. **VLM 作为物理架构师**的设计范式值得借鉴：利用 VLM 的世界知识先验进行高层物理规划，再由专用模型执行精确生成——这种"规划-生成"解耦思路可推广到其他需要物理理解的生成任务
2. **KineVoxel Injection** 将异构模态（几何 vs 运动学）映射到统一潜在空间并联合扩散，是一种优雅的多模态融合策略
3. **PhysDB 数据集**的四层级标注体系为物理感知 3D 资产生成建立了标准化标注规范
4. 对具身 AI 的意义：生成的仿真就绪资产可直接导入机器人仿真器，为操控任务提供大规模仿真环境数据引擎
5. 与我们研究的关联：虽然不直接涉及 DLO 操控，但其生成的带物理属性的铰接物体可作为 DLO 操控仿真环境中的交互对象；VLM 规划范式可启发 DLO 操控中的任务规划

## 相关概念

- [[novel-view-synthesis]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[yang-yunhan|Yang, Yunhan]]
- [[li-yang|Li, Yang]]
