---
title: "CoEnv: Driving embodied multi-agent collaboration via compositional environment"
tags: [manipulation, imitation, VLM, RL, sim-to-real]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Interactive + Iterative 模式）和碰撞感知 Sim-to-Real 迁移，实现多臂机器人协同操控，在 5 个真实任务上达到 49% 总体成功率"
authors: "Kang, Li; Fan, Yutao; Li, Rui; Zhou, Heng; Qin, Yiran et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TRJEQVEN"
---
## 摘要

Multi-agent embodied systems hold promise for complex collaborative manipulation（操控）, yet face critical challenges in spatial coordination, temporal reasoning, and shared workspace awareness. Inspired by human collaboration where cognitive planning occurs separately from physical execution, we introduce the concept of compositional environment -- a synergistic integration of real-world and simulation components that enables multiple robotic agents to perceive intentions and operate within a unified decision-making space. Building on this concept, we present CoEnv, a framework that leverages simulation for safe strategy exploration while ensuring reliable real-world deployment. CoEnv operates through three stages: real-to-sim scene reconstruction that digitizes physical workspaces, VLM-driven action synthesis supporting both real-time planning with high-level interfaces and iterative planning with code-based trajectory generation, and validated sim-to-real（仿真到真实迁移） transfer with collision detection for safe deployment. Extensive experiments on challenging multi-arm manipulation（操控） benchmarks demonstrate CoEnv's effectiveness in achieving high task success rates and execution efficiency, establishing a new paradigm for multi-agent embodied AI.

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. 提出 **Compositional Environment** 概念——融合仿真和真实世界组件的统一决策空间，用于多智能体具身协作
2. 提出 **CoEnv 框架**——结合仿真驱动的规划与 VLM-based agent（Interactive 模式用 GPT-5，Iterative 模式用 Claude Code），实现协同操控策略的合成、验证和部署
3. 在 5 个多臂操控任务（最多 3 台异构机器人）上验证，并展示可扩展的多智能体数据生成管线
## 结构化提取

- Problem: 多智能体具身系统的空间协调、时序推理和共享工作空间感知
- Method: Compositional Environment (Real-to-Sim + VLM 双层规划 + 碰撞感知 Sim-to-Real)
- Tasks: 多臂协同操控（Cube Stacking, Ball Pickup, Transfer Cylinder, Place Cucumber, Brush Box）
- Sensors: 2-3× Intel RealSense D435i RGBD cameras (multi-view)
- Robot Setup: 2× Franka Research 3 (2-agent), 1× Franka + AgileX Piper 双臂 (3-agent), 固定基座
- Metrics: 子任务成功率 S_i, 任务成功率 SR, Overall success rate (%), 数据生成效率 (episodes/session)
- Limitations: sim-to-real 位姿偏差、规划循环停滞、模式特异性局限、未验证可变形/铰接物体、未蒸馏端到端策略
- Evidence Notes:

  - 5 个真实任务 × 10 次试验 × 2 种模式 = 100 次试验
  - 完整消融实验：去掉 adaptive camera (-20%), 去掉 checkpoint (-30%)
  - 数据生成效率：Iterative 模式比 Interactive 高 4-12×
  - 所有结果均基于真实机器人实验，非仿真-only
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML, ~86K chars)
- Evidence Coverage: high (all sections read: abstract, intro, related work, methodology, experiments, ablation, data collection, conclusion)
- Confidence: high
- Summary: 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Interactive + Iterative 模式）和碰撞感知 Sim-to-Real 迁移，实现多臂机器人协同操控，在 5 个真实任务上达到 49% 总体成功率


## Problem

多智能体具身系统在协同操控中面临三个核心挑战：
1. **空间协调**：多机器臂共享工作空间，需避免碰撞和冲突
2. **时序推理**：长时域任务中子任务间的依赖关系复杂
3. **共享工作空间感知**：单视角遮挡导致 VLM 无法准确理解场景

现有方法的不足：
- RoCo/MALMM 等依赖文本表征，缺乏细粒度空间推理和碰撞避免能力
- 现有 VLM 框架主要针对单智能体场景，缺乏多智能体技能整合机制
- 仿真到真实迁移技术未有效扩展到多智能体系统


## Method

CoEnv 框架包含三个阶段：

### Stage 1: Real-to-Sim Scene Reconstruction (Sec 3.1)
- **3D Asset Generation**：使用 Meshy 从真实参考生成 3D mesh 资产，标准化尺寸并预定义物理属性
- **Multi-View Object Localization**：
  - Grounded SAM2 检测和分割目标物体
  - GPT-5 作为视觉推理模块消除歧义（处理视觉相似物体）
  - FoundationPose 估计 6-DoF 位姿
  - 多视角融合：平移取算术平均，旋转取四元数平均（尊重 SO(3) 流形结构）
- **Simulation Environment**：基于 ManiSkill（SAPIEN 物理引擎），支持可重置的迭代相机标定修正

### Stage 2: Simulation-Conditioned Action Synthesis (Sec 3.2)
两阶段规划：
- **Stage I: Hierarchical Task Planning**
  - VLM (GPT-5) 将目标 G 分解为高层语义子目标 H = {h_1, ..., h_L}
  - 分配执行计划 E = {e_1, ..., e_L}，每个 e_l 指定 agent、action primitive、目标参数
  - Action primitives: Move, Grasp, Place, Rotate
  - **Adaptive Camera Control**：动态调整仿真视角，聚合多视角观察以处理遮挡

- **Stage II: Grounded Execution**（两种互补模式）
  - **Interactive Mode**：闭环 VLM 反馈（执行→观察→验证→适应），引入 checkpoint 机制在关键节点检查前置条件
  - **Iterative Mode**：Code Agent (Claude Code) 生成完整程序编码全部执行逻辑，迭代优化直到成功或达到最大迭代次数

- **Validation and Data Collection**：验证成功的轨迹存入知识库 D，可作为未来规划的 in-context 演示或训练数据

### Stage 3: Sim-to-Real Transfer (Sec 3.3)
- **Trajectory Interpolation**：记录每个 primitive action 完成时的关节配置，线性插值生成平滑轨迹
- **Collision Volume Verification**：正向运动学计算扫掠碰撞体积，要求所有 agent 对的碰撞体积不相交，违反则触发重规划


## Experiments

### Setup
- **硬件配置**：
  - 2-agent：2× Franka Research 3
  - 3-agent：1× Franka Research 3 + AgileX Piper 双臂平台
- **感知**：2-3 个 Intel RealSense D435i 相机（多视角 RGBD）
- **仿真**：ManiSkill (SAPIEN)
- **评估**：每模式每任务 10 次试验
- **Metrics**：子任务成功率 S_i，任务成功率 SR，Overall (%)

### 5 个任务
1. **Cube Stacking** (2-agent)：各臂拾取立方体并堆叠 → 75%
2. **Ball Pickup** (2-agent)：双手协调抬起足球 → 50%
3. **Transfer Cylinder** (2-agent)：传递圆柱体 → 25%
4. **Place Cucumber** (3-agent)：放黄瓜入锅 → 35%
5. **Brush Box** (3-agent)：刷子扫物 → 60%

### 主要结果 (Table 1)
| Task | Interactive SR | Iterative SR | Overall |
|------|---------------|-------------|---------|
| Cube Stacking | 6/10 | 9/10 | 75% |
| Ball Pickup | 4/10 | 6/10 | 50% |
| Transfer Cylinder | 4/10 | 1/10 | 25% |
| Place Cucumber | 4/10 | 3/10 | 35% |
| Brush Box | 7/10 | 5/10 | 60% |
| **Average** | **50%** | **48%** | **49%** |

### 模式互补性
- **Iterative 模式优势**：精确轨迹控制（Cube Stacking 9/10 vs 6/10，Ball Pickup 6/10 vs 4/10）
- **Interactive 模式优势**：复杂多阶段协调（Transfer Cylinder 4/10 vs 1/10，Brush Box 7/10 vs 5/10）

### 消融实验 (Table 2)
- **去掉自适应相机**：50% → 30%，对遮挡严重的任务影响最大（Transfer Cylinder 和 Brush Box 降至 0/10）
- **去掉 Checkpoint 验证**：50% → 20%，普遍性下降（级联错误传播）
- 两者组合贡献 2.5× 提升

### 数据生成效率 (Table 3)
- Iterative 模式：Cube Stacking 17.5 episodes/session，Brush Box 9.5 episodes/session
- Interactive 模式：分别 1.5 和 2.5 episodes/session
- 环境重置仅占 token 消耗的 10-32%


## Limitations

1. **Sim-to-Real 位姿偏差**：接触密集型原语（抓取、插入）容易因微小偏差而失败
2. **规划循环停滞**：VLM/Code Agent 有时进入重复重规划循环，生成相似但同样失败的方案
3. **模式特异性局限**：Interactive 模式在长序列中累积漂移；Iterative 模式难以处理需要闭环适应的反应性任务
4. **未扩展到可变形/铰接物体**：当前仅验证刚体物体
5. **未从收集数据蒸馏端到端策略**：数据管线已建立但尚未用于训练通用多智能体策略


## Key Takeaways

1. **Compositional Environment 范式对 DLO 操控的启示**：将仿真作为"认知介质"的思路可扩展到可变形物体——在仿真中安全探索 DLO 策略，验证后迁移到真实，但需解决柔体仿真精度问题
2. **VLM 双层规划架构**：Hierarchical Planning + Grounded Execution 的分离设计值得借鉴，对双臂 DLO 任务，可将 DLO 形状约束和碰撞避免融入高层规划
3. **Adaptive Camera + Checkpoint 机制**：对多臂 DLO 场景特别重要——DLO 的遮挡更严重，需要在关键操作节点（如接触前）检查 DLO 形态
4. **碰撞体积验证方法的局限**：当前基于刚体扫掠体积的方法不适用于 DLO，需要柔体碰撞检测
5. **数据生成管线**：CoEnv 的仿真验证→真实收集流程可作为多臂 DLO 数据集构建的参考

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[kang|Kang, Li]]
- [[zhou-heng|Zhou, Heng]]
