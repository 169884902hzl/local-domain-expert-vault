---
title: "One-shot real-world demonstration synthesis for scalable bimanual manipulation"
tags: [manipulation, imitation, sim-to-real, bimanual, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线"
authors: "Zhou, Huayi; Jia, Kui"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "8WBUSK7P"
---
## 摘要

Learning dexterous（灵巧） bimanual manipulation（双臂操控） policies critically depends on large-scale, high-quality demonstrations, yet current paradigms face inherent trade-offs: teleoperation provides physically grounded data but is prohibitively labor-intensive, while simulation-based synthesis scales efficiently but suffers from sim-to-real（仿真到真实迁移） gaps. We present BiDemoSyn, a framework that synthesizes contact-rich（接触丰富）, physically feasible bimanual（双臂） demonstrations from a single real-world example. The key idea is to decompose tasks into invariant coordination blocks and variable, object-dependent adjustments, then adapt them through vision-guided alignment and lightweight trajectory optimization. This enables the generation of thousands of diverse and feasible demonstrations within several hours, without repeated teleoperation or reliance on imperfect simulation. Across six dual-arm（双臂） tasks, we show that policies trained on BiDemoSyn data generalize robustly to novel object poses and shapes, significantly outperforming recent strong baselines. Beyond the one-shot（单样本） setting, BiDemoSyn naturally extends to few-shot（少样本）-based synthesis, improving object-level diversity and out-of-distribution generalization while maintaining strong data efficiency. Moreover, policies trained on BiDemoSyn data exhibit zero-shot（零样本） cross-embodiment（具身） transfer to new robotic platforms, enabled by object-centric observations and a simplified 6-DoF end-effector action representation that decouples policies from embodiment（具身）-specific dynamics. By bridging the gap between efficiency and real-world fidelity, BiDemoSyn provides a scalable path toward practical imitation learning（模仿学习） for complex bimanual manipulation（双臂操控） without compromising physical grounding.

## 中文简述

提出基于模仿学习的双臂方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、双臂操控、运动规划

## 关键贡献

1. **One-Shot Synthesis Framework**: 提出三阶段流水线——任务分解（不变/可变块分离）、视觉引导对齐、物理感知轨迹优化——从单次示教合成数千条演示
2. **Reality-Grounded Data Generation**: 完全不依赖仿真器，所有合成轨迹在真实世界生成，确保物理保真度
3. **Empirical Validation**: 在6个接触丰富双臂任务上全面验证，支持 zero-shot 跨平台迁移和 few-shot 扩展
## 结构化提取

- Problem: 双臂模仿学习的大规模演示数据获取——如何在保证物理真实性的前提下从单次示教扩展数据
- Method: BiDemoSyn 三阶段流水线（分解 → 视觉对齐 → 轨迹优化）+ Diffusion Policy 双臂适配
- Tasks: plugpen（插笔帽）、inserting（孔轴插入）、unscrew（拧瓶盖）、pouring（倒水）、pressing（按压喷嘴）、reorient（翻转物体）
- Sensors: 立体相机（RGB + 深度图）
- Robot Setup: 双固定臂 + 平行夹爪（主平台）；辅助人形双臂平台（跨平台验证）
- Metrics: 合成效率（秒/条）、数据质量（视觉真实度）、成功率（30 trials/task）、OOD 泛化率
- Limitations: 仅静态/准静态场景；不处理高度可变形物体；准静态假设；多阶段依赖接触任务受限
- Evidence Notes: 全文包含完整定量实验——6任务×3策略×3数据源，含 ID/OOD 评估、效率对比、few-shot 扩展、空间泛化分析、跨平台迁移验证。补充材料（任务/硬件/数据收集细节）未读取。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖 Abstract、Introduction、Method (IV.A-C)、Experiments (V.A-B)、Conclusion、References；补充材料未读取
- Confidence: high
- Summary: BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线


## Problem

双臂模仿学习需要大规模高质量演示数据，但现有两条路径各有致命缺陷：(1) 遥操作数据质量高但人力成本极高（约91秒/条）；(2) 仿真合成可扩展但存在 Sim-to-Real gap。如何在**不使用仿真、不重复遥操作**的前提下，从单次真实示教生成大规模物理可行的双臂演示？


## Method

### 核心思路
将演示轨迹分解为"不变协调块"和"可变适应块"，对可变块做视觉感知适配，再通过物理约束优化重新组合。

### Stage 1: Deconstruction (IV.A)
- 输入单次示教 τ = {o_t, a_t}
- 分解为 Bimanual Execution Blocks {B_i}，每块包含左右臂状态序列
- **单臂运动块**: 一臂显著运动、另一臂静止（阈值 δ/ζ 判定，式4）
- **双臂协调块**: 两臂同步/异步调整（式5）
- 每块进一步细化为 Atomic Execution Primitives (AEPs)——最小运动单元（式6）
- 最终分类为 **invariant**（语义原语如拧、按、提升）和 **variable**（依赖物体几何的抓取等）两类

### Stage 2: Vision-based Initial Frame Alignment (IV.B)
- **Object Perception**: 用 YOLO-World / Florence2+SAM2 检测分割目标物体
- **State Estimation**: 用 image moments + PCA 从深度图估计实例级 6D pose (R, c)，无需 CAD 模型
- **Pose Alignment**: 计算刚体变换 T 将示教中的物体 pose 映射到新场景（式9），调整抓取位姿

### Stage 3: Trajectory Modulation and Optimization (IV.C)
- **Collision-Aware Validation**: IK 验证可达性 + 运动规划器检查碰撞
- **Instance-Level Motion Adaptation**: 根据 3D bounding box 差异偏移运动端点（式10，λ=0.8~1.0）
- 最终重组为合成轨迹 τ' = {τ_inv, {B_i'}}

### Policy Learning (III)
- 基于 Diffusion Policy 架构，适配双臂动作空间 a_t = [a^L_t, a^R_t] ∈ R^{2d}
- UNet 用非对称层处理：浅层各臂独立，深层融合双臂协调特征
- Mahalanobis 范数加权训练损失，优先建模双臂交互


## Experiments

### Setup
- **6个任务**: plugpen（插笔帽）、inserting（孔轴插入）、unscrew（拧瓶盖）、pouring（倒水）、pressing（按压喷嘴）、reorient（翻转物体）
- **硬件**: 双固定臂 + 平行夹爪，立体相机；辅助人形双臂平台验证跨平台
- **数据量**: 每任务 1008~7776 条合成演示
- **Policies**: DP (RGB)、DP3 (PCD)、EquiBot (PCD)
- **Baselines (数据收集)**: DemoGen、YOTO、Teleoperation
- **Baselines (Training-Free)**: ReKep、ReKep+、ODIL、MAGIC

### Main Results (Table I)
| Policy | Method | ID Avg | OOD Avg |
|--------|--------|--------|---------|
| DP (RGB) | DemoGen | 55.0% | 19.4% |
| DP (RGB) | YOTO | 56.7% | 21.1% |
| DP (RGB) | **BiDemoSyn** | **67.8%** | **42.2%** |
| DP3 (PCD) | DemoGen | 66.1% | 30.0% |
| DP3 (PCD) | YOTO | 67.8% | 33.9% |
| DP3 (PCD) | **BiDemoSyn** | **81.1%** | **54.4%** |
| EquiBot (PCD) | DemoGen | 68.9% | 40.6% |
| EquiBot (PCD) | YOTO | 71.1% | 47.8% |
| EquiBot (PCD) | **BiDemoSyn** | **86.7%** | **66.7%** |

### Efficiency
- BiDemoSyn: ~5 秒/条
- DemoGen: <1 秒/条（但存在视角畸变伪影）
- YOTO: ~42 秒/条
- Teleoperation: ~91 秒/条

### Few-shot Extension (Table II)
- EquiBot 策略下，1-shot→20-shot 的 ID 成功率从 86.7% → 90.0%，OOD 从 66.7% → 72.2%
- Few-shot 主要改善 OOD 泛化（物体几何多样性），对 ID 性能提升有限

### Spatial Generalization (Fig. 6)
- unscrew 任务：稀疏覆盖(6×6) 53.3% → 密集覆盖(10×10) 76.7%
- reorient 任务：低方向多样性(#Ornt.=3) 37.3% → 高方向多样性(#Ornt.=7) 73.3%

### Cross-Embodiment Transfer (Fig. 8)
- 训练策略 zero-shot 迁移到人形双臂机器人，plugpen 和 reorient 任务成功率高


## Limitations

1. 仅适用于静态/准静态场景，不支持完全动态环境
2. 不处理极端形变物体（如高度可变形物体、关节物体的大变形）
3. 准静态假设排除了高速动态任务（如接抛）
4. 多阶段相互依赖接触任务（如系绳）需进一步扩展
5. 不规则形状的 bounding box 适应可能不够精确，有时需人工辅助


## Key Takeaways

### 与我们研究的相关性
1. **DLO 操控启发**: BiDemoSyn 的不变/可变块分解思路可用于 DLO 任务——DLO 的拓扑变化可作为"可变块"，而抓取/释放的协调模式作为"不变块"。但 DLO 的高度可变形性是其明确指出的局限之一
2. **数据合成范式**: 该工作验证了"真实世界合成"而非仿真合成的可行性——对于 DLO 这种 Sim-to-Real gap 特别大的物体类型尤其有价值
3. **视觉对齐方法**: 用 image moments + PCA 做实例级 pose 估计的方法简洁有效，可借鉴用于 DLO 形状估计
4. **跨平台迁移**: object-centric 观察 + 6-DoF EE action 的设计解耦了策略与机器人本体，对我们设计通用 DLO 操控策略有参考价值

### 与现有本地笔记的关联
- 与 [[ACT]]（遥操作数据收集范式）和 [[Diffusion Policy]]（策略架构）形成互补
- 与 [[MimicGen]]（仿真合成范式）形成对比：BiDemoSyn 完全避免仿真
- 跨平台迁移思路与 [[Open X-Embodiment]] 目标一致

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[bimanual-manipulation]]
- [[planning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zhou|Zhou, Huayi]]
- [[jia|Jia, Kui]]
