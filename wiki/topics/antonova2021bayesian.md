---
title: "A bayesian treatment of real-to-sim for deformable object manipulation"
tags: [manipulation, sim-to-real, DLO]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 BayesSim-RKHS，将可变形物体关键点视为状态分布的样本，用 RKHS 核均值嵌入实现置换不变表示，结合 BayesSim 进行仿真参数后验推断。在擦桌布、绳绕线轴、布料 fling 三个真实场景上显著优于 BayesSim-MDNN 等基线，可推断弹性、摩擦、尺度等物理参数后验。"
authors: "Antonova, Rika; Yang, Jingyun; Sundaresan, Priya; Fox, Dieter; Ramos, Fabio et al."
year: "2021"
venue: "arXiv Preprint"
zotero_key: "UNKXJLVK"
---
## 摘要

Deformable object（可变形物体） manipulation（操控） remains a challenging task in robotics research. Conventional techniques for parameter inference and state estimation typically rely on a precise definition of the state space and its dynamics. While this is appropriate for rigid objects and robot states, it is challenging to define the state space of a deformable object（可变形物体） and how it evolves in time. In this work, we pose the problem of inferring physical parameters of deformable objects as a probabilistic inference task defined with a simulator. We propose a novel methodology for extracting state information from image sequences via a technique to represent the state of a deformable object（可变形物体） as a distribution embedding. This allows to incorporate noisy state observations directly into modern Bayesian simulation-based inference tools in a principled manner. Our experiments confirm that we can estimate posterior distributions of physical properties, such as elasticity, friction and scale of highly deformable objects, such as cloth and ropes. Overall, our method addresses the real-to-sim problem probabilistically and helps to better represent the evolution of the state of deformable objects.

## 中文简述

提出基于学习方法的绳索操控方法。

**研究方向**: 机器人操控、仿真到真实迁移、可变形物体操控

## 关键贡献

1. **分布嵌入表示**：将可变形物体关键点视为状态分布的样本，用 RKHS 核均值嵌入（kernel mean embedding）实现置换不变、噪声鲁棒的状态表示。
2. **BayesSim-RKHS 框架**：将分布嵌入集成到 BayesSim 的条件密度网络中，通过随机傅里叶特征（RFF）近似实现可微分的 RKHS-net 层。
3. **三场景真实世界验证**：擦桌布（小变形）、绳绕线轴（高变形+遮挡）、布料 fling（动态+自遮挡），两种关键点提取方法（监督+无监督）。
## 结构化提取

- **Problem**: 可变形物体仿真参数推断（real-to-sim）受限于不一致的状态表示。关键点提取噪声大、排列不固定，传统 BayesSim 方法直接使用关键点坐标推断效果差。
- **Method**: BayesSim-RKHS：将关键点视为状态分布的样本，用 RKHS 核均值嵌入（随机傅里叶特征近似）构建置换不变表示。集成到 BayesSim 的 Mixture Density Network 中，迭代推断仿真参数后验。支持监督/无监督关键点提取。
- **Tasks**: 擦桌布（Kinova Gen3 拖拽布料）；绳绕线轴（将绳绕到轴上）；布料 fling（抛起+拖拽）。
- **Sensors**: Intel RealSense D435 RGB-D（320×320），HSV 颜色分割用于评估（非推断）。
- **Robot Setup**: Kinova Gen3 7-DoF + Robotiq 2F-85 夹爪，笛卡尔速度控制。PyBullet FEM 仿真器。
- **Metrics**: Chamfer Distance（双向，仿真-真实 masks 对齐），30 条评估轨迹均值±标准差。
- **Limitations**: 仅推断参数不评估控制迁移；关键点表示有限（4-8个）；仅 PyBullet；无定量表格；1500 次仿真成本；未处理视觉 domain gap。
- **Evidence Notes**: 6 种方法对比在 3 个场景 × 2 种关键点方法上充分消融（Fig. 5/6/8）。RKHS 在绳绕线轴场景优势最显著（关键点无固定位置）。后验可视化揭示参数可辨识性差异（Fig. 7）。评估用 Chamfer Distance 基于 mask 而非关键点，避免自证循环。整体证据强度：中-强（定性折线图 + 后验分析，缺少定量误差表）。
## 本地引用关系

- [[blancomulero2024benchmarking]]
## 证据元数据

- **Zotero Key**: UNKXJLVK
- **Citekey**: antonova2021bayesian
- **Authors**: Antonova Rika, Yang Jingyun, Sundaresan Priya, Fox Dieter, Ramos Fabio, Bohg Jeannette
- **Affiliation**: Stanford + CMU + NVIDIA + U. Sydney + UW
- **Venue**: arXiv preprint, 2021-12
- **Paper Type**: Methods paper (Bayesian inference for real-to-sim)
- **Fulltext Quality**: Complete, 8 pages with figures and experimental results
- **Evidence Coverage**: High for three real-world scenarios (wiping/winding/fling); Medium for quantitative comparison (plots without numeric tables)
- **Confidence**: High on method comparison (6 baselines, 30 evaluation trajectories); Medium on generalizability (3 scenarios only)
- **Summary**: 提出 BayesSim-RKHS，将可变形物体关键点视为状态分布的样本，用 RKHS 核均值嵌入实现置换不变表示，结合 BayesSim 进行仿真参数后验推断。在擦桌布、绳绕线轴、布料 fling 三个真实场景上显著优于 BayesSim-MDNN 等基线，可推断弹性、摩擦、尺度等物理参数后验。


## Problem

可变形物体操控的仿真参数推断是 sim-to-real 的关键瓶颈。传统方法假设可靠的低维状态表示（如刚体位姿），但可变形物体缺乏规范形状，关键点提取不一致且可置换。现有 BayesSim 方法直接使用关键点坐标，在噪声和不一致的表示下推断效果差。


## Method

### 核心思路
- 关键点 k₁,...,k_K 视为分布 P(X) 的样本
- 核均值嵌入 μ_X = E[φ(X)] ≈ (1/N) Σ φ(x_n)，用 RFF 近似 φ
- RKHS-net 层：可微分，ω 和 σ 通过梯度下降学习
- 嵌入后特征替换原始关键点坐标，输入 BayesSim MDNN

### 推断流程
1. 执行真实操控轨迹，记录 RGB 图像
2. 从先验采样仿真参数，生成仿真轨迹
3. 提取关键点（监督/无监督），经 RKHS-net 嵌入
4. 训练 MDNN 学习条件密度 q(θ|x)
5. 从后验采样，迭代 15 轮（每轮 100 仿真轨迹）

### 关键点提取
- **监督方法**（Grannen et al. 2020）：ResNet-34 预测热图，250 张标注图像（125 仿真+125 真实）
- **无监督方法**（Kulkarni et al. 2019）：Transporter 架构，扩展了机器人 mask

### 仿真器
- PyBullet + FEM 选项，快速但低精度
- 推断参数：弯曲刚度、弹性刚度、摩擦、尺度（4D）


## Experiments

### 评估方法
- 30 条评估轨迹，Chamfer Distance 度量仿真-真实对齐
- 6 种方法对比：BayesSim-MDNN、BayesSim-MDRFF、BayesSim-RKHS、BayesZoom-RKHS、NN-bulk-1.5k、GP-bulk-1.5k

### 擦桌布任务（Fig. 5）
- BayesSim-RKHS 在两种关键点方法下均优于其他方法
- 无监督关键点：RKHS 方法的"distance to GT"显著低于 MDNN

### 绳绕线轴任务（Fig. 6）
- RKHS 方法优势最大（关键点在绳上移动无固定位置）
- BayesSim-MDNN 几乎无法收敛

### 布料 fling 任务（Fig. 8）
- RKHS 方法仍最优，但与基线差距较小
- 无监督关键点有时落在机器人上（限制因素）

### 后验分析（Fig. 7）
- 尺度和摩擦参数后验较集中（易推断）
- 弯曲和弹性刚度后验更分散（难推断）


## Limitations

1. **仅推断仿真参数，不涉及控制器学习**：未评估推断后的仿真参数是否改善 sim-to-real 控制策略迁移。
2. **关键点表示有限**：4-8 个关键点无法完整表征复杂可变形物体状态，特别是自遮挡严重的场景。
3. **仅 PyBullet FEM**：未在其他仿真器（如 MuJoCo、SOFA）上验证方法的仿真器无关性。
4. **无定量表格**：实验结果仅以折线图展示，缺少精确数值（成功率/误差均值）。
5. **计算成本**：15 轮 × 100 仿真轨迹 = 1500 次仿真，对复杂场景可能较慢。
6. **未处理视觉 domain gap**：假设仿真和真实的视觉外观近似匹配，未使用 domain randomization。


## Key Takeaways

1. **分布嵌入是处理可变形物体状态表示的有效范式**：关键点置换不变性 + 噪声鲁棒性，对 DLO 操控中的状态估计有直接参考价值。
2. **与 [[blancomulero2024benchmarking]] 互补**：Blanco-Mulero et al. 量化仿真器本身的 reality gap，本文提供从真实数据推断仿真参数的自动化方法，两者可结合：先用本基准识别最佳仿真器，再用 BayesSim-RKHS 调优参数。
3. **对本研究方向的启示**：双臂 DLO 操控的 sim-to-real 需要精确的绳索物理参数（刚度、阻尼、摩擦）。BayesSim-RKHS 可用于从真实 DLO 操控视频中推断这些参数的后验分布，实现自动化的 real-to-sim 校准。
4. **RKHS-net 的可微分设计**使其可端到端集成到更大的学习框架中。

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[antonova|Antonova, Rika]]
- [[fox|Fox, Dieter]]
