---
title: "R2RGEN: Real-to-real 3D data generation for spatially generalized manipulation"
tags: [manipulation, imitation, sim-to-real, robot-learning, physics-simulation]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出无需仿真器的 real-to-real 3D 数据生成框架 R2RGen，通过 group-wise 回溯增强和 camera-aware 后处理，用 1 次人类示范即可达到 25 次示范的空间泛化水平，支持移动操控和双臂任务。"
authors: "Xu, Xiuwei; Ma, Angyuan; Li, Hankun; Yu, Bingyao; Zhu, Zheng et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "JGG3V2TF"
---
## 摘要

Towards the aim of generalized robotic manipulation（机器人操控）, spatial generalization is the most fundamental capability that requires the policy to work robustly under different spatial distribution of objects, environment and agent itself. To achieve this, substantial human demonstrations need to be collected to cover different spatial configurations for training a generalized visuomotor policy via imitation learning（模仿学习）. Prior works explore a promising direction that leverages data generation to acquire abundant spatially diverse data from minimal source demonstrations. However, most approaches face significant sim-to-real（仿真到真实迁移） gap and are often limited to constrained settings, such as fixed-base scenarios and predefined camera viewpoints. In this paper, we propose a real-to-real 3D data generation framework (R2RGen) that directly augments the pointcloud observation-action pairs to generate real-world data. R2RGen is simulator- and rendering-free, thus being efficient and plug-and-play. Specifically, we propose a unified three-stage framework, which (1) pre-processes source demonstrations under different camera setups in a shared 3D space with scene / trajectory parsing; (2) augments objects and robot's position with a group-wise backtracking strategy; (3) aligns the distribution of generated data with real-world 3D sensor using camera-aware post-processing. Empirically, R2RGen substantially enhances data efficiency on extensive experiments and demonstrates strong potential for scaling and application on mobile manipulation（移动操控）.

## 中文简述

提出基于模仿学习的移动操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、机器人学习、物理仿真

## 关键贡献

1. **Real-to-Real 3D 数据生成框架**：首个无需仿真器和渲染器的 3D 数据生成方案，直接在真实世界的点云观测-动作对上做增强
2. **Group-wise 回溯策略**：将每个 skill 关联一组物体（而非单个目标），通过从后往前的回溯机制维护多物体间的空间约束，避免因果冲突
3. **Camera-aware 后处理**：通过 Crop、Z-buffer、Fill 三步操作使生成数据的点云分布与真实 RGB-D 传感器一致
4. **广泛适用性**：支持移动操控器、腕部相机、原始点云输入、任意物体数量和交互模式、双臂操控
## 结构化提取

- Problem: 如何从极少量人类示范（1 次）生成空间泛化数据，训练在任意物体配置和机器人视角下都能工作的视觉运动策略
- Method: 三阶段 real-to-real 3D 数据生成框架：(1) 源示范预处理（FoundationPose 追踪 + 模板补全 + 轻量标注）；(2) Group-wise 回溯增强（多物体组变换 + 运动规划 + 基座增强）；(3) Camera-aware 后处理（Crop + Z-buffer + Fill）
- Tasks: 8 个真实任务——Open-Jar, Place-Bottle, Pot-Food, Hang-Cup, Stack-Brick, Build-Bridge（单臂）, Grasp-Box, Store-Item（双臂）；另有关节物体和可变形物体辅助任务
- Sensors: ORBBEC femto bolt RGB-D 相机（外部安装或腕部安装）
- Robot Setup: 单臂 UR5e + Weiss WSG-50 + 移动基座；双臂 MobileAloha（AgileX PiPER × 2 + HexFellow 全向移动底座）
- Metrics: 成功率（success rate），在多样化物体位置/旋转和机器人视角下评估
- Limitations: 基座执行时固定、需模板扫描和标注、FoundationPose 仅支持刚性物体、策略容量瓶颈、未验证 DLO 任务
- Evidence Notes:

  - Table I: R2RGen(1 demo) 平均 40.3% vs 25 human demos 平均 41.0%
  - Table II: 跨相机设置（exterior-wrist, wrist-wrist）有效
  - Table III: 点云补全和环境处理消融，均关键
  - Table IV: Camera-aware 三步操作消融，缺一不可
  - Table V: SAM 3D 替代 FoundationPose 可处理非刚性物体
  - Figure 3: 生成数据量饱和受策略容量限制
  - Figure 4: 外观泛化：4 demo + R2RGen → 43.8% vs 40 human demos → 25%
  - Figure 5: 移动操控（MoTo 导航 + R2RGen 操控策略）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML v2, 含完整正文、附录、表格)
- Evidence Coverage: 完整覆盖方法、实验、消融、扩展实验和附录细节
- Confidence: high
- Summary: 提出无需仿真器的 real-to-real 3D 数据生成框架 R2RGen，通过 group-wise 回溯增强和 camera-aware 后处理，用 1 次人类示范即可达到 25 次示范的空间泛化水平，支持移动操控和双臂任务。


## Problem

机器人操控中，**空间泛化**（spatial generalization）是视觉运动策略最基本也最耗数据的需求。传统方法需要大量人类示范覆盖不同物体空间配置和机器人基座位置。现有数据生成方法（如 MimicGen、DemoGen）存在三个核心局限：
1. **Sim-to-Real Gap**：基于仿真的方法在真实世界部署时性能下降严重
2. **固定基座约束**：假设固定基座和外部相机，无法处理视角变化或腕部相机
3. **单目标物体假设**：每个 skill 只能关联一个目标物体，无法处理多物体空间约束的任务（如搭桥需要两个桥墩保持特定距离）


## Method

### 三阶段管线概览

```
RoCS_DC →(SP)→ WCS →(Aug)→ WCS →(CAP)→ RoCS_DP
```

### Stage 1: Source Pre-processing（源示范预处理）

**Scene Parsing（场景解析）**：
- 使用 FoundationPose 追踪物体 6-DoF 位姿
- 基于 iPad 扫描的 3D 模板补全物体点云（解决 RGB-D 观测不完整问题）
- 将环境点云在 WCS 中单独扫描存储
- 坐标转换：外部相机用固定变换 Te，腕部相机用 (A_t^ee)^{-1}

**Trajectory Parsing（轨迹解析）**：
- 轻量级标注 UI：标注者仅需标记 skill 段的起止帧和关联物体 ID
- 每个 skill 标注 target objects 和 in-hand object
- Motion 段为 skill 段之间的自由空间运动
- 标注时间 < 60 秒/示范

### Stage 2: Group-wise Data Augmentation（分组数据增强）

**核心创新 — Group-wise Backtracking**：
- 每个 skill 关联一组物体 O_i = O_i^tar ∪ O_i^hand
- 从最后一个 skill 开始**回溯**处理
- 维护"固定物体集合" Ō_n：已被后续 skill 固定的物体不可再被增强
- 更新规则：Ō_{n-1} = (Ō_n ∪ O_n^tar) \ O_n^hand（目标物体被固定，手中物体被释放）
- 若当前组与固定集无交集 → 随机采样 XY 平面平移 + Z 轴旋转的变换矩阵

**Skill Augmentation**：对 skill 段的末端执行器位姿施加组变换 T_i
**Motion Augmentation**：用运动规划连接相邻 skill
**Base Augmentation**：随机增强机器人基座位置和朝向 → IK 求解关节角 → 生成完整机械臂点云

### Stage 3: Camera-aware 3D Post-processing（相机感知后处理）

1. **Crop**：移除投影后超出图像边界的像素
2. **Z-buffer**：仅保留最小深度值的像素（patch-wise，r 邻域），移除被遮挡的点
3. **Fill**：处理边界空像素——采用 shrink（缩小图像尺寸）或 expand（扩展环境点云）策略

最终将处理后的像素反投影回相机坐标系，得到与真实 RGB-D 传感器分布一致的点云。

### 关键技术细节

- **策略架构**：iDP3（3D Diffusion Policy），输入 ego-centric 点云 + 本体感知
- **训练参数**：To=2, Tp=16, Ta=8, 5Hz 运行，6000 epochs，RTX 4090，Adam lr=1e-4
- **数据生成量**：3 次回放 × N 种空间配置 × 3 次随机扰动（1.5cm 半径平移 + ±20° 旋转）


## Experiments

### 主实验（Table I）：8 个真实任务，one-shot 模式

| 设置 | Open-Jar | Place-Bottle | Pot-Food | Hang-Cup | Stack-Brick | Build-Bridge | Grasp-Box | Store-Item | 平均 |
|------|----------|-------------|----------|----------|-------------|-------------|-----------|-----------|------|
| 1 Source | 3.1% | 3.1% | 3.1% | 3.1% | 3.1% | 3.1% | 4.2% | 4.2% | 3.4% |
| +DemoGen | 18.8% | 15.6% | – | – | – | – | 16.7% | 16.7% | – |
| +R2RGen | **50.0%** | **50.0%** | **37.5%** | **34.4%** | **43.8%** | **34.4%** | **41.7%** | **33.3%** | **40.3%** |
| 10 Source | 56.3% | 34.3% | 9.4% | 15.6% | 9.4% | 9.4% | 25.0% | 20.8% | 22.5% |
| 25 Source | 78.1% | 53.1% | 21.9% | 43.8% | 40.6% | 28.1% | 29.2% | 33.3% | 41.0% |
| 40 Source | 87.5% | 68.8% | 28.1% | 43.8% | 50.0% | 43.8% | 37.5% | 41.7% | 50.2% |

**核心发现**：R2RGen(1 demo) ≈ 25 human demos 的性能！

### 跨相机设置（Table II）
- **Exterior-Wrist** 和 **Wrist-Wrist** 均有效
- 朴素跨相机部署（训练外部视角、测试腕部视角）→ 灾难性失败
- R2RGen 通过 3D 坐标变换消除域差距

### 扩展实验

**非刚性物体（Table V）**：
- 关节物体：使用 SAM 3D 替代 FoundationPose
- 可变形物体（布料覆盖）：同样有效

**外观泛化（Figure 4）**：
- 4 种外观组合（2 瓶 × 2 底座），R2RGen(4 demo) → 43.8% vs 40 human demos → 25%
- 空间泛化是其他泛化的基础前提

**移动操控（Figure 5）**：
- 导航系统 MoTo + R2RGen 训练的操控策略
- 成功泛化到不同对接点（>5cm 偏差）

### 消融实验

**点云处理（Table III）**：移除点云补全 → 大幅增强下数据不真实；移除环境处理 → 视角变化鲁棒性下降

**Camera-aware 处理（Table IV）**：Crop、Z-buffer、Fill 三者均对最终性能至关重要


## Limitations

1. **移动基座执行期间固定**：假设每次任务执行中基座不动，不支持动态移动操控
2. **需要模板扫描和轻量标注**：每个物体需要 iPad 扫描 3D 模板，每条示范需 <60 秒标注
3. **FoundationPose 仅支持刚性物体**：非刚性物体需切换到 SAM 3D 等，增加复杂度
4. **策略容量瓶颈**：iDP3 使用轻量 PointNet 编码器，生成数据量增大后性能饱和
5. **未验证高可变形 DLO 任务**：布料实验表明可行性，但线缆等细长柔性体未涉及
6. **物体分割依赖首帧标注**：需要人工在首帧标注物体掩码


## Key Takeaways

1. **Real-to-Real 范式的可行性**：完全绕开仿真器和渲染器，直接在 3D 空间操作点云-动作对，既高效又避免 sim-to-real gap。这对 DLO 操控很有启发——DLO 的仿真建模本身就非常困难，real-to-real 范式可能是更实际的方向
2. **Group-wise 是处理多物体任务的关键**：单目标增强无法处理搭桥等多物体空间约束任务。对于 DLO 操控中"先固定线缆一端再操作另一端"这类序列性空间约束，group-wise 回溯机制有直接借鉴价值
3. **Camera-aware 后处理不可忽视**：直接增强点云会导致"看到不该看的"和"漏掉该看到的"，必须通过 Crop/Z-buffer/Fill 校准到 RGB-D 传感器分布。这是 3D 数据生成方法区别于 2D 方法的独特挑战
4. **数据效率惊人**：1 次示范生成数据 ≈ 25 次人类示范，说明空间泛化的数据需求高度冗余，自动数据生成是解决数据瓶颈的有效路径
5. **空间泛化是其他泛化的基础**：论文明确指出 spatial generalization 是 appearance generalization 的前提。对于 DLO 操控研究，先解决空间泛化（不同起始位置、不同缠绕形态）再考虑外观泛化（不同线缆材质/颜色）是合理的路线

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu-xiuwei|Xu, Xiuwei]]
- [[ma-angyuan|Ma, Angyuan]]
