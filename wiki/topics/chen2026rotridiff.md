---
title: "RoTri-Diff: A Spatial Robot-Object Triadic Interaction-Guided Diffusion Model for Bimanual Manipulation"
tags: [manipulation, imitation, diffusion, bimanual, grasping]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。"
authors: "Chen, Zixuan; Chan, Nga Teng; Hou, Yiwen; Tie, Chenrui; Liu, Zixuan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "X78VMT9F"
---
## 摘要

Bimanual manipulation（双臂操控） is a fundamental robotic skill that requires continuous and precise coordination between two arms. While imitation learning（模仿学习） (IL) is the dominant paradigm for acquiring this capability, existing approaches, whether robot-centric or object-centric, often overlook the dynamic geometric relationship among the two arms and the manipulated object. This limitation frequently leads to inter-arm collisions, unstable grasps, and degraded performance in complex tasks. To address this, in this paper we explicitly models the Robot-Object Triadic Interaction (RoTri) representation in bimanual（双臂） systems, by encoding the relative 6D poses between the two arms and the object to capture their spatial triadic relationship and establish continuous triangular geometric constraints. Building on this, we further introduce RoTri-Diff, a diffusion（扩散）-based imitation learning（模仿学习） framework that combines RoTri constraints with robot keyposes and object motion in a hierarchical diffusion（扩散） process. This enables the generation of stable, coordinated trajectories and robust execution across different modes of bimanual manipulation（双臂操控）. Extensive experiments show that our approach outperforms state-of-the-art（现有最优方法） baselines by 10.2% on 11 representative RLBench2 tasks and achieves stable performance on 4 challenging real-world bimanual（双臂） tasks. Project website: https://rotri-diff.github.io/.

## 中文简述

提出基于扩散模型的抓取方法。

**研究方向**: 机器人操控、模仿学习、扩散模型、双臂操控、抓取

## 关键贡献

1. **RoTri 表示**：首次提出 Robot-Object Triadic Interaction (RoTri) 表示，通过编码双臂末端执行器与物体之间的相对6D位姿（位置3D + 四元数4D × 3对 = 21维），建立连续三角几何约束
2. **RoTri-Diff 框架**：层次化扩散模型，协同整合 keyposes、object pointflow 和 RoTri 约束，生成时空一致的双臂动作轨迹
3. **全面验证**：在11个 RLBench2 任务上超越 SOTA 10.2%，在4个真实世界双臂任务上稳定执行
## 结构化提取

- Problem: 双臂操控中两臂与物体之间的动态空间关系被忽视，导致碰撞、抓取不稳和性能退化
- Method: RoTri-Diff — 基于扩散的层次化模仿学习框架，显式建模 Robot-Object Triadic Interaction (RoTri) 表示，整合 keyposes、object pointflow 和 RoTri 约束
- Tasks: 11个 RLBench2 双臂任务（Push Buttons, Lift Ball, Lift Tray, Push Box, Handover Item Easy/Hard, Pick Laptop, Put Item into Drawer, Sweep to Dustpan, Pick Plate, Put Bottle in Fridge）+ 4个真实世界任务
- Sensors: 多视角 RGBD 相机（Eye-on-Hand ×2 + Eye-on-Base RealSense）
- Robot Setup: 仿真：RLBench2 (CoppeliaSim)；真实：双 xArm6 机器人
- Metrics: 成功率（%），100次 rollout 取平均（仿真），5次试验成功计数（真实）
- Limitations: 刚体假设、依赖准确6D位姿估计、未验证可变形物体和跨具身迁移、真实世界试验数少
- Evidence Notes:

  - RoTri 表示的核心是 $R = [p_{L \to R}, p_{L \to O}, p_{R \to O}] \in \mathbb{R}^{21}$，编码末端执行器间和末端执行器-物体间的相对6D位姿
  - 层次化扩散过程分三阶段：预测 pointflow + RoTri 片段 → 生成 keyposes → 生成连续动作
  - Pick Plate 任务最能体现 RoTri 的价值：PPI 0.0% vs RoTri-Diff 40.7%
  - 消融表明 keypose-only 和 continuous-only 都不够，必须层次化组合
  - 多物体场景通过置换不变的 Transformer 编码器聚合多个 RoTri 向量
## 本地引用关系

- [[chen2026rotridiff]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（涵盖方法、实验、消融、真实验证）
- Confidence: high
- Summary: 提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。


## Problem

现有双臂模仿学习方法（robot-centric 或 object-centric）忽略了双臂与被操控物体之间的动态几何关系，导致：
1. 双臂碰撞
2. 抓取不稳定
3. 复杂任务性能退化

核心问题：如何在双臂系统中显式建模两臂与物体之间的**空间三体关系（triadic interaction）**，并将其作为约束融入策略学习。


## Method

### 整体架构
RoTri-Diff 包含三个核心组件：

**1. 视觉感知与 RoTri 建模（Section III-B）**
- 3D 语义特征：DINOv2 提取像素语义特征 → 多视角融合 → PointNet++ 下采样得到紧凑表示 $S_t \in \mathbb{R}^{N_s \times (3+D)}$
- 初始物体点云：Grounding DINO + SAM 生成物体 mask → 采样 $N_q=200$ 个点得到 $F_0$
- RoTri 向量：$R_0 = [p_{left \to right}, p_{left \to obj}, p_{right \to obj}] \in \mathbb{R}^{21}$，每对包含 3D 位置 + 4D 四元数

**2. IL 引导信号（Section III-C）**
- **Keypose**：启发式算法提取轨迹转折点（关节速度趋零或夹爪开合事件）
- **Object Pointflow**：利用物体6D位姿将初始点云变换到未来 keypose 位置，消除推理时实时位姿估计需求
- **RoTri Relationship**：不直接预测完整 RoTri 轨迹，而是学习增量变化 $\Delta R_t$，通过累积 $R_t = R_{t-1} + \Delta R_t$ 更新

**3. 层次化扩散模型（Section III-D）**
- **Observation Encoder**：CLIP 文本编码器 + MLP（机器人状态、初始物体点、初始 RoTri）
- **三阶段生成**：
  - Stage 1：同时预测 object pointflow + 自回归预测 RoTri 片段
  - Stage 2：基于 pointflow 和 RoTri 生成 keypose 动作
  - Stage 3：整合所有信号生成连续动作序列
- 使用 Relative Self-Attention + RoPE 利用3D空间信息
- FiLM 调制融入本体感知和去噪步

**训练**：DDPM，1000步噪声调度，L1 损失，8× A5000 GPU，batch size 64，AdamW lr=1e-4
**推理**：仿真用 DDPM 1000步，真实用 DDIM 20步，生成50步连续动作

### 与现有方法的关键区别（Table I）
RoTri-Diff 是唯一同时整合 keyposes + object movement + robot-object interaction 的方法。


## Experiments

### 仿真实验（RLBench2，11个任务）

| 协调类型 | 任务 | RoTri-Diff | PPI (SOTA) | 提升 |
|---------|------|-----------|-----------|------|
| Symmetric | Push Buttons | 97.0 | 70.7 | +26.3 |
| Synchronous | Lift Ball | 95.7 | 92.0 | +3.7 |
| Synchronous | Lift Tray | 94.3 | 89.3 | +5.0 |
| Synchronous | Push Box | 95.0 | 92.0 | +3.0 |
| Asynchronous | Handover Item (Easy) | 73.3 | 62.7 | +10.6 |
| Asynchronous | Handover Item (Hard) | 52.3 | 37.3 | +15.0 |
| Asynchronous | Pick Laptop | 66.0 | 46.3 | +19.7 |
| Asynchronous | Put Item into Drawer | 87.0 | 79.7 | +7.3 |
| Asynchronous | Sweep to Dustpan | 96.7 | 98.7 | -2.0 |
| Asynchronous | Pick Plate | 40.7 | 0.0 | +40.7 |
| Asynchronous | Put Bottle in Fridge | 92.0 | 82.6（原文数据） | — |

**平均成功率：80.9%，较 SOTA 提升 10.2%**

关键发现：
- Pick Plate 任务：RoTri-Diff 40.7% vs PPI 0.0%，证明 RoTri 约束对精细协调至关重要
- Handover Item (Hard)：RoTri-Diff 52.3% vs AnyBimanual 15.0%，异步协调显著优势
- 仅 Sweep to Dustpan 略低于 PPI（-2.0%）

### 消融实验（Table III, Fig. 4）

**RoTri 应用方式消融**（4个代表任务）：
| 变体 | Push Buttons | Lift Tray | Pick Plate | Put Bottle in Fridge |
|------|-------------|-----------|-----------|---------------------|
| RoTri (Keypose Only) | 93.7 | 92.6 | 29.3 | 90.3 |
| RoTri (Continuous Only) | 95.3 | 88.7 | 21.3 | 86.0 |
| **RoTri-Diff (Full)** | **97.0** | **94.3** | **40.7** | **92.0** |

- Keypose Only 在 Pick Plate 降至 29.3%：缺少连续约束导致精细动作不稳
- Continuous Only 在 Pick Plate 仅 21.3%：缺少 keypose 锚点导致复杂任务失败
- 密集 RoTri 引导优于稀疏引导（5步/10步间隔），证明逐时间步引导防止漂移

### 真实世界实验（双 xArm6 机器人）

| 任务 | 协调类型 | 成功次数 |
|------|---------|---------|
| Pick Tomato & Banana | Symmetric | 5/5 |
| Pick Plate | Asynchronous | 3/5 |
| Wash Plate | Asynchronous | 4/5 |
| Lift Basket | Synchronous | 4/5 |

- 示范数据：Meta Quest 2 遥操作采集，50次（Lift Basket, Pick Place）或 20次（其余）
- 感知配置：2个 Eye-on-Hand 相机 + 1个 Eye-on-Base RealSense 相机


## Limitations

1. **刚体假设**：RoTri 建模基于刚体物体，无法处理可变形物体（DLO）
2. **6D 位姿估计依赖**：需要准确的物体6D位姿，限制了在非结构化环境中的泛化
3. **单一具身**：仅在 xArm6 双臂平台上验证，未展示跨具身迁移能力
4. **未见与 DLO 操控的关联**：方法设计未考虑可变形物体场景
5. **真实验证规模有限**：每个任务仅5次试验，统计置信度有限


## Key Takeaways

### 与我们研究方向的关联
1. **RoTri 三体交互表示**：将双臂-物体关系显式编码为几何约束的思路值得借鉴。对于 DLO 操控，可探索将 DLO 形状表示纳入三体关系建模
2. **层次化扩散策略**：keypose → 连续动作的层次生成架构，结合中间表示（pointflow, RoTri）作为条件，可用于 DLO 操控中的抓取-放置序列规划
3. **增量预测范式**：RoTri 通过预测 $\Delta R_t$ 而非绝对值，减少学习难度——对 DLO 连续形变建模有启发
4. **局限性的研究机会**：论文明确指出无法处理可变形物体，这为我们的 DLO 操控研究提供了差异化定位

### 方法论启发
- 三角几何约束作为正则化信号，可迁移到其他需要精细协调的操控任务
- 自回归 RoTri 片段预测 + 层次化扩散的组合模式，可适用于长序列操控

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]
- [[deformable-linear-object]]

## 相关研究者

- [[chen-zixuan|Chen, Zixuan]]
- [[chan-nga-teng|Chan, Nga Teng]]
