---
title: "Benchmarking the Sim-to-Real Gap in Cloth Manipulation"
tags: [manipulation, sim-to-real, DLO]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "首个量化布料操控 sim-to-real gap 的基准数据集。在双臂 Franka 系统上收集动态（fling）和准静态（拖拽）布料操控数据，用 Chamfer/Hausdorff Distance 评估 MuJoCo、Bullet、Flex、SOFA 四个仿真器。MuJoCo 在动态任务上误差最低（CDd 0.067-0.079），准静态任务所有仿真器差距不大。推荐 MuJoCo 用于布料操控仿真。"
authors: "Blanco-Mulero, David; Barbany, Oriol; Alcan, Gokhan; Colomé, Adrià; Torras, Carme et al."
year: "2024"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "H4GWJCUT"
---
## 摘要

Realistic physics engines play a crucial role for learning to manipulate deformable objects such as garments in simulation. By doing so, researchers can circumvent challenges such as sensing the deformation of the object in the realworld. In spite of the extensive use of simulations for this task, few works have evaluated the reality gap between deformable object（可变形物体） simulators and real-world data. We present a benchmark dataset to evaluate the sim-to-real（仿真到真实迁移） gap in cloth manipulation（操控）. The dataset is collected by performing a dynamic as well as a quasi-static cloth manipulation（操控） task involving contact with a rigid table. We use the dataset to evaluate the reality gap, computational time, and simulation stability of four popular deformable object（可变形物体） simulators: MuJoCo, Bullet, Flex, and SOFA. Additionally, we discuss the benefits and drawbacks of each simulator. The benchmark dataset is open-source. Supplementary material, videos, and code, can be found at https://sites.google.com/view/cloth-sim2real-benchmark.

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、仿真到真实迁移、可变形物体操控

## 关键贡献

1. **首个布料操控 sim-to-real gap 基准数据集**：3 种布料（毛巾/格子布/亚麻布）× 2 种任务（动态/准静态），包含点云和 RGB-D 数据。
2. **四仿真器系统评估**：MuJoCo（mass-spring）、Bullet（PBD/FEM）、Flex（PBD/GPU）、SOFA（FEM/mass-spring），评估 reality gap + 稳定性 + 计算时间。
3. **仿真器无关的评估框架**：开源代码，可扩展到新仿真器，使用 Chamfer Distance 和 Hausdorff Distance 作为度量。
4. **实践建议**：推荐 MuJoCo 用于布料操控（最低动态误差 + 有机器人模型 + CPU/GPU 支持）。
## 结构化提取

- **Problem**: 布料操控仿真训练广泛使用，但从未量化 sim-to-real gap。动态操控涉及高加速度惯性力，仿真器难以准确模拟，需要基准评估。
- **Method**: 3 种布料 × 2 种任务（动态 fling + 准静态拖拽）的真实数据集。4 仿真器（MuJoCo/Bullet/Flex/SOFA）参数调优后评估。度量：单向 Chamfer Distance + Hausdorff Distance + 稳定性 + 计算时间。20 random seeds 统计分析。
- **Tasks**: 动态 fling（双臂 quintic 轨迹，Y/Z/roll，高加速度）；准静态下降+拖拽（Y/Z，低速+刚性表面接触）。
- **Sensors**: Microsoft Azure Kinect RGB-D（1280×720, 30fps），点云经 MiVOS 分割预处理。
- **Robot Setup**: 双臂 Franka Emika Panda，X 轴固定 51cm，pinch grasp。
- **Metrics**: CDd/CDq（动态/准静态 Chamfer Distance），HDd/HDq（Hausdorff Distance），Ls（稳定性），Step Time（ms/仿真步）。
- **Limitations**: 仅 3 种软布料；无控制器学习 sim-to-real 评估；参数调优成本高（500 sweeps）；仅 fling + 拖拽；单一传感器；未覆盖最新仿真器。
- **Evidence Notes**: 量化结果可靠（20 seeds × 4 仿真器 × 3 布料 × 2 任务 = 480 组实验，Tab. III）。BO/CMA-ES 调参公平（每仿真器独立优化）。真实数据集点云质量高（RGB-D + MiVOS 分割）。仿真器特征对比系统（Tab. I）。频率 × 稳定性 × 误差分析（Fig. 5）揭示仿真器行为模式。整体证据强度：强（系统性基准 + 统计分析）。
## 本地引用关系

-
## 证据元数据

- **Zotero Key**: H4GWJCUT
- **Citekey**: blancomulero2024benchmarking
- **Authors**: Blanco-Mulero David, Barbany Oriol, Alcan Gokhan, Colomé Adrià, Torras Carme, Kyrki Ville
- **Affiliation**: Aalto University + IRI (CSIC-UPC)
- **Venue**: IEEE Robotics and Automation Letters (RA-L), Vol. 9, No. 3, 2024
- **Paper Type**: Benchmark/Evaluation paper (sim-to-real gap measurement)
- **Fulltext Quality**: Complete, 8 pages with tables, figures, and detailed simulator comparison
- **Evidence Coverage**: High for sim-to-real gap quantification (Tab. III, 20 seeds × 4 simulators × 3 fabrics × 2 tasks); High for simulator comparison (Tab. I, Fig. 4-5)
- **Confidence**: High on quantitative results (rigorous experimental setup with BO/CMA-ES parameter tuning)
- **Summary**: 首个量化布料操控 sim-to-real gap 的基准数据集。在双臂 Franka 系统上收集动态（fling）和准静态（拖拽）布料操控数据，用 Chamfer/Hausdorff Distance 评估 MuJoCo、Bullet、Flex、SOFA 四个仿真器。MuJoCo 在动态任务上误差最低（CDd 0.067-0.079），准静态任务所有仿真器差距不大。推荐 MuJoCo 用于布料操控仿真。


## Problem

布料操控研究广泛依赖仿真引擎训练控制器，但从未系统性量化仿真与现实之间的 reality gap。特别是动态操控任务（如 fling）涉及高加速度和布料惯性力，仿真器难以准确模拟。没有基准数据集和评估标准来衡量不同仿真器的保真度。


## Method

### 数据集
- 双臂 Franka Panda 执行 quintic 多项式轨迹
- 动态任务：fling motion（Y/Z/roll，4/3/3 via-points），评估 cloth dynamics 阶段
- 准静态任务：缓慢下降+拖拽（Y/Z，2/2 via-points），评估 contact 阶段
- 3 种布料（50×70cm，不同重量/弹性），来自公开 household 数据集
- Microsoft Azure Kinect RGB-D，30fps，1280×720
- MiVOS 语义分割提取布料点云

### 评估流程
1. 记录真实数据 → 2. 预处理点云 → 3. 在仿真器中重现轨迹 → 4. 计算 CD/HD
- 仿真器参数通过 Bayesian Optimization + CMA-ES 优化（500 sweeps）
- 20 random seeds × 仿真器 × 布料 × 任务
- 评估 3 种频率（10/100/1000 Hz）

### 度量
- CD（单向 Chamfer Distance）：平均点云误差，l1 范数
- HD（单向 Hausdorff Distance）：最大点云误差
- Ls（稳定性）：滤波前后网格差异
- Step Time（计算时间/仿真步）


## Experiments

### 动态任务结果（Tab. III, CDd/HDd）
| 仿真器 | Towel CDd | Cheq. CDd | Linen CDd |
|--------|----------|----------|----------|
| MuJoCo | 0.079±0.031 | 0.067±0.026 | 0.071±0.031 |
| SOFA | 0.078±0.029 | 0.068±0.024 | 0.061±0.024 |
| Bullet | 0.155±0.093 | 0.119±0.060 | 0.116±0.054 |
| Flex | 0.168±0.129 | 0.164±0.134 | 0.160±0.131 |

### 准静态任务结果（Tab. III, CDq/HDq）
- 所有仿真器 CDq 在 0.07-0.10 范围，差距较小
- Flex 准静态表现最好（CDq ~0.07-0.08）

### 仿真器对比（Tab. I）
- MuJoCo：mass-spring，CPU/GPU，有机器人模型，RGB-D，推荐
- Bullet：PBD/FEM，CPU，有机器人模型，参数敏感
- Flex：PBD，仅 GPU，默认无机器人模型（IsaacSim 有）
- SOFA：FEM/mass-spring，CPU/GPU，无机器人模型

### 频率影响（Fig. 5）
- MuJoCo/Bullet：低频（10Hz）不稳定，高频显著改善
- Flex/SOFA：不同频率表现一致
- 100Hz 所有仿真器步长约毫秒级，但动态操控 hardware-in-the-loop 仍不可行


## Limitations

1. **仅评估 3 种软布料**：无硬挺织物（如牛仔裤），作者发现仅 Bullet/MuJoCo 能近似硬布料行为。
2. **无控制器学习评估**：仅评估仿真器本身的 reality gap，未评估学习到的控制器在 sim-to-real 迁移后的性能退化。
3. **参数调优依赖优化**：每仿真器 × 布料 × 任务需 500 sweeps BO/CMA-ES 调参，实践中成本高。
4. **仅双臂 fling + 拖拽**：未覆盖折叠、放置、穿脱等常见布料操控任务。
5. **传感器单一**：仅 Azure Kinect RGB-D，未评估触觉或其他传感器对 reality gap 的影响。
6. **发表于 2024 年初**：未覆盖更新的仿真器如 IsaacSim（2024+版本）和 MuJoCo MJX。


## Key Takeaways

1. **动态操控的 sim-to-real gap 远大于准静态**：动态任务 CDd 比准静态 CDq 大 2-3 倍。这对 DLO/布料操控中动态动作（如 fling、swing）的 sim-to-real 迁移有重要启示——需要更精细的仿真或 domain randomization。
2. **MuJoCo 最适合可变形物体操控仿真**：动态误差最低 + 有完整机器人模型 + CPU/GPU 支持。这支持了本地 vault 中多篇论文选择 MuJoCo 作为仿真平台的决策。
3. **准静态任务仿真器差距不大**：对低加速度操控（如缓慢调整 DLO 形状），仿真器选择影响较小。
4. **对本研究方向的启示**：双臂 DLO 操控若涉及动态动作（如 fling 穿缆），应优先使用 MuJoCo，且需要 domain randomization 或 real-to-sim 参数调优来缩小 reality gap。本基准数据集的方法论（点云 CD/HD 度量 + BO 参数调优）可直接应用于 DLO 操控的 sim-to-real 评估。

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[blanco-mulero|Blanco-Mulero, David]]
