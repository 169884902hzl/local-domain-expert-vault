---
title: "cuRoboV2: Dynamics-aware motion generation with depth-fused distance fields for high-DoF robots"
tags: [manipulation, imitation, VLM, planning, reactive-control]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "统一 GPU-native 运动生成框架，通过 B-spline 轨迹优化、密集 ESDF 感知管线和可扩展 whole-body 计算，实现从单臂到 48-DoF 人形机器人的动力学感知规划，3kg 负载下成功率 99.7%（baseline 仅 72-77%），并首次展示 LLM 辅助 CUDA 内核开发可达 73% 模块贡献率。"
authors: "Sundaralingam, Balakumar; Murali, Adithyavairavan; Birchfield, Stan"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XMD2VFMC"
---
## 摘要

Effective robot autonomy requires motion generation that is safe, feasible, and reactive. Current methods are fragmented: fast planners output physically unexecutable trajectories, reactive controllers struggle with high-fidelity perception, and existing solvers fail on high-DoF systems. We present cuRoboV2, a unified framework with three key innovations: (1) B-spline trajectory optimization that enforces smoothness and torque limits; (2) a GPU-native TSDF/ESDF perception pipeline that generates dense signed distance fields covering the full workspace, unlike existing methods that only provide distances within sparsely allocated blocks, up to 10x faster and in 8x less memory than the state-of-the-art（现有最优方法） at manipulation（操控） scale, with up to 99% collision recall; and (3) scalable GPU-native whole-body computation, namely topology-aware kinematics, differentiable inverse dynamics（逆动力学）, and map-reduce self-collision, that achieves up to 61x speedup while also extending to high-DoF humanoids (where previous GPU implementations fail). On benchmarks, cuRoboV2 achieves 99.7% success under 3kg payload (where baselines achieve only 72--77%), 99.6% collision-free IK on a 48-DoF humanoid (where prior methods fail entirely), and 89.5% retargeting constraint satisfaction (vs. 61% for PyRoki); these collision-free motions yield locomotion policies with 21% lower tracking error than PyRoki and 12x lower cross-seed variance than GMR. A ground-up codebase redesign for discoverability enabled LLM coding assistants to author up to 73% of new modules, including hand-optimized CUDA kernels, demonstrating that well-structured robotics code can unlock productive human-LLM collaboration. Together, these advances provide a unified, dynamics-aware motion generation stack that scales from single-arm manipulators to full humanoids. Code is available at https://github.com/NVlabs/curobo.

## 中文简述

提出基于力控制的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、运动规划、反应式控制

## 关键贡献

1. **B-spline 轨迹优化**：将轨迹参数化为均匀三次 B-spline 控制点，自动保证 C² 连续性，比 per-timestep 参数化用更少的决策变量实现固有光滑性，使力矩约束成为良态优化问题；支持非静态边界条件（通过 ghost control points），统一了全局规划和反应式控制。
2. **GPU-native TSDF/ESDF 感知管线**：分块稀疏 TSDF 融合深度和几何体原语，通过 PBA+ 算法按需生成密集 ESDF；支持异构分辨率（TSDF 5mm + ESDF 20mm），比 nvblox 快 10x、内存少 8x，碰撞召回率最高 99%。
3. **可扩展 whole-body GPU 计算**：拓扑感知正运动学、稀疏 Jacobian（支持 mimic joints）、map-reduce 自碰撞检测（162k 碰撞对处理速度提升 61x）、可微逆动力学（RNEA，compact spatial representation + VJP backward pass），首次在 48-DoF 人形机器人上实现碰撞自由 IK。
4. **LLM 辅助开发**：通过代码库可发现性重构（typed config、自解释命名、单文件 <254 行、测试作为可执行文档），使 Claude 模型能够编写高达 73% 的新模块代码，包括手优 CUDA 内核。
## 结构化提取

- Problem: 现有运动生成方法在动力学可行性、感知精度和高 DoF 可扩展性三个维度上存在根本性障碍，导致物理不可执行的轨迹、碰撞保证与高保真感知的矛盾、以及高 DoF 系统上的规划失败
- Method: GPU-native 统一运动生成框架，B-spline 轨迹优化 + TSDF/ESDF 密集感知 + 拓扑感知 whole-body 计算（运动学、逆动力学、自碰撞），支持全局规划、MPC 和 IK 三种模式
- Tasks: 运动规划、碰撞自由 IK、MPC 反应式控制、人形动作重定向、真实世界操控
- Sensors: 深度相机（ZED Mini, 1080p, 15Hz, Neural Plus depth model）
- Robot Setup: Franka Panda (7-DoF)、双 UR10e (12-DoF)、Unitree G1 (48-DoF)、I2RT YAM 机器人（真实世界）
- Metrics: 运动学成功率、动力学成功率（零负载/3kg 负载）、能耗（J）、规划时间（ms）、IK 位姿误差（μm）、IK 成功率、约束满足率、MPJPE、跨种子方差、存活率、重置次数、ESDF 生成时间、GPU 内存、碰撞召回率
- Limitations: MPC 未温启动、几何机器人分割对深度误差敏感、单相机覆盖有限、LLM 无法解释编译器中间表示、未涉及柔性/DLO 物体场景
- Evidence Notes: 全文可获取。动力学规划 benchmark (2600 problems, MotionBenchMaker+MπNets) 提供了完整的成功率-负载曲线；ESDF 对比在 Redwood bedroom 场景上完成；人形重定向使用 LeFan 70k+ 帧数据集；真实世界部署使用 I2RT YAM + ZED Mini。所有定量结果均有具体数字和 baseline 对比。LLM 贡献量化基于 git history 统计。
## 本地引用关系

- [[sundaralingam2026curobov2]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文通过 ar5iv 获取，涵盖所有章节包括附录）
- Confidence: high
- Summary: 统一 GPU-native 运动生成框架，通过 B-spline 轨迹优化、密集 ESDF 感知管线和可扩展 whole-body 计算，实现从单臂到 48-DoF 人形机器人的动力学感知规划，3kg 负载下成功率 99.7%（baseline 仅 72-77%），并首次展示 LLM 辅助 CUDA 内核开发可达 73% 模块贡献率。


## Problem

当前机器人运动生成面临三个根本性障碍：
1. **可行性鸿沟（Feasibility Gap）**：快速规划器忽略动力学，输出的轨迹在物理上不可执行。3kg 负载下，现有方法（cuRobo、VAMP）的成功率从 ~99% 骤降至 72-77%，因为轨迹违反力矩限制。
2. **感知-反应性权衡（Perception-Reactivity Trade-off）**：基于模型的控制器（RMP、MPC）提供安全保证但无法处理高保真深度数据；学习方法处理视觉观测快但缺乏碰撞保证和泛化能力。
3. **可扩展性壁垒（Scalability Wall）**：单臂平台上的方法在高 DoF 系统（如 48-DoF 人形机器人）上收敛缓慢或完全失败，尤其是碰撞避障 IK。


## Method

### 核心架构
运动生成被形式化为轨迹优化问题（Eq. 1-9），优化变量为 B-spline 控制点 U。每轮迭代包含六个步骤：
1. B-spline 插值从控制点生成轨迹 waypoints
2. 正运动学 + RNEA 计算连杆位姿、Jacobians 和关节力矩
3. 并行代价评估（世界碰撞、自碰撞、状态代价）
4. 代价聚合
5. 反向传播计算梯度
6. 优化器更新控制点

### B-spline 轨迹空间（Sec. 4）
- 每个关节轨迹 U ∈ ℝ^(d×K) 用 K 个控制点参数化
- C² 连续性由 B-spline 基函数自动保证
- 梯度计算：反向传播即为前向的转置（Eq. 13），支持高效 GPU 并行 reduction
- 非静态边界：引入 3 个 ghost control points（u₋₃, u₋₂, u₋₁），从初始状态 Θ₀ 计算得出（Eq. 15-17），消除边界约束冲突
- 静态终止：重复最终 knot 四次即可满足零速度/加速度终止条件

### ESDF 感知管线（Sec. 5）
**分块稀疏 TSDF**：
- 8³ 体素块 + 哈希表映射，仅分配表面附近的块
- 双通道：depth_sum/depth_wt（深度观测）和 geom_sdf（几何原语），查询时取 min
- 100K 活跃块仅占 ~350MB GPU 内存（等效密集网格的 1/11）

**深度融合**：Voxel-Project 策略，每个体素投射到深度图像，单线程无原子写入

**ESDF 生成三阶段**：
1. Site Seeding：scatter（遍历 TSDF 块）或 gather（ESDF 格点探测 TSDF）；gather 支持固定工作维度，兼容 CUDA graph
2. Distance Propagation：PBA+（Parallel Banding Algorithm），3 轴分离的精确欧几里得 Voronoi 图，5 次固定 kernel launch
3. Sign Recovery：对解析原语，沿 site-to-query 方向偏移采样相邻体素获取符号

### 高 DoF 扩展（Sec. 6）
**正运动学**：自适应 kernel dispatch——简单机器人（≤100 spheres）用融合单 kernel；复杂机器人用双 kernel split（帧变换 + 并行 sphere/CoM/Jacobian 计算）

**并行梯度反传**：预计算拓扑缓存，每个线程仅遍历相关运动链，O(1) 查找祖先连杆

**稀疏 Jacobian**：两级过滤（coarse affects[j,e] 剪枝 + fine-grained mimic joint 检查），每个线程计算一列 Jacobian

**Map-reduce 自碰撞**：将碰撞对分块到 thread blocks，每块在 shared memory 中找最大穿透对，最后全局 reduce

**可微 RNEA**：
- Compact spatial representation：12 floats/link（R+p 代替 6×6 矩阵）
- VJP backward pass：O(n) 梯度计算，避免 GRiD 的 O(n²) Jacobian
- Tree-level parallelism：warp-level 同步，float4 向量化全局内存访问

### 求解器策略
- **IK**：LM（Levenberg-Marquardt）求解位姿目标 → L-BFGS 精化碰撞约束
- **全局规划**：多 seed 轨迹优化 + 碰撞自由图搜索 seed
- **MPC**：短执行时域重优化


## Experiments

### 数据集和平台
- 硬件：NVIDIA RTX 4090 GPU
- 规划 benchmark：MotionBenchMaker + MπNets 数据集，2600 个问题，Franka Panda
- IK benchmark：7-DoF Franka, 12-DoF 双 UR10e, 48-DoF Unitree G1
- 人形动作重定向：LeFan 数据集，70k+ 帧
- ESDF benchmark：Redwood bedroom 场景

### 主要结果

**动力学感知规划（Tab. 3, Fig. 11-12）**：
| 方法 | 运动学成功率 | 零负载动力学 | 3kg 负载 | 能耗(P75) | 规划时间 |
|------|-------------|-------------|---------|-----------|---------|
| cuRoboV2 | >99% | 99.7% | **99.7%** | **106 J** | 48 ms |
| cuRobo | 99.8% | 97.9% | 77.1% | 116 J | 36 ms |
| VAMP (AORRTC) | 98.9% | 95.8% | 75% | 131-160 J | — |

- 动力学约束仅增加 +7ms 端到端时间（35ms → 42ms），RNEA 占 kernel 时间的 29%
- B-spline 固有光滑性比 per-timestep 优化多解决 66 个问题（2591 vs 2525/2600）

**逆动力学对比（Fig. 13）**：
- 7-DoF (batch 256)：cuRoboV2 29.3μs vs GRiD 18.8μs (1.5×) vs Newton 400μs (14×)
- 12-DoF：cuRoboV2 45μs vs GRiD 21.5μs (2×) vs Newton 661μs (15×)
- 48-DoF：**GRiD 失败**（shared memory 溢出），cuRoboV2 96.2μs vs Newton 1713μs (18×)

**碰撞自由 IK（Fig. 15）**：
- 48-DoF G1：cuRoboV2 **99.6%**（2.4μm 误差, 533ms），cuRobo **0%**，PyRoki **0%**

**人形动作重定向（Fig. 16-17）**：
- 约束满足率：cuRoboV2-MPC 96.6%，cuRoboV2-IK 89.5%，PyRoki 61.2%，mink 40.6%

**行走策略训练（Fig. 18-20）**：
- 爬行运动：cuRoboV2 MPJPE 151.4±4.5mm，mink 174.1±50.7mm（**12× 方差差异**）
- PyRoki 重置次数 2× cuRoboV2（4.6 vs 2.2）
- 总体：cuRoboV2 最低 MPJPE (145.5mm)、最高存活率 (99.6%)、最少重置 (1.1)

**ESDF 性能（Fig. 21-23）**：
- 10mm TSDF + 全覆盖：cuRoboV2 1.69ms vs nvblox 12.68ms (**7×**)，内存 1.63GB vs 11.87GB (**7×**)
- 20mm：cuRoboV2 1.52ms, recall 97.0% vs nvblox 2.97ms, recall 85.4%
- TSDF+原语 stamping 使规划时间减少 19%（47ms → 38ms）

**真实世界操控**：I2RT YAM 机器人 + ZED Mini，2.5mm TSDF + 2cm ESDF，MPC 实时碰撞避障，单控制循环内完成全部感知-规划流水线

**LLM 辅助开发（Fig. 26-27）**：
- 代码库从 121 → 390 文件，测试从 264 → 3978 (15×)
- LLM 贡献：R1-R3 阶段 6-18%，N1 阶段 50%，**N2 阶段 73%**
- RNEA CUDA kernel、scene collision migration、PBA ESDF 均有 LLM 大量参与

### 消融实验
- B-spline vs per-timestep（Fig. 12）：B-spline 产生连续加速度/加加速度曲线，per-timestep 产生锯齿状
- scatter vs gather seeding：r≥4 时 scatter 更优（+2.5% recall），r≈1 时 gather 更优（+2-4%）
- 有/无动力学约束的 kernel 时间分解（Tab. 3-4）


## Limitations

1. **MPC 温启动**：当前 MPC 未从全局规划的 B-spline 结果温启动，这是自然的下一步
2. **感知鲁棒性**：基于几何的机器人分割对深度估计误差敏感，学习型 RGB 分割可能更鲁棒
3. **单相机覆盖**：仅部分场景覆盖，多相机融合可改善重建完整性
4. **LLM 辅助限制**：LLM 能生成和 profile GPU 代码，但解释中间编译器表示（如区分虚拟/物理寄存器压力）仍需人工判断
5. cuRoboV2-MPC 的位姿跟踪精度不如 cuRoboV2-IK（因为 MPC 解更难的优化问题）
6. 论文未讨论 DLO/柔性物体场景的直接适用性


## Key Takeaways

1. **B-spline 作为轨迹空间是动力学约束优化的关键**：C² 连续性使力矩约束成为良态问题，比加速度正则化更根本。对于 DLO 操控，B-spline 参数化可能对长时域平滑轨迹生成（如连续弯折操作）有启发价值。
2. **密集 ESDF 的 O(1) 碰撞查询 + TSDF/ESDF 分离是实用化关键**：传统方法要么内存爆炸（密集）要么查询稀疏（块级 ESDF）。PBA+ 的固定 kernel launch 数量使其完全兼容 CUDA graph，实现确定性延迟——这对安全关键的反应式控制至关重要。
3. **Whole-body 碰撞自由 IK 证明了 GPU-native 运动优化的可扩展性**：48-DoF 上 99.6% 成功率 vs 竞品 0%，这意味着双臂 12-DoF 系统上的规划问题可以轻松解决，对双臂 DLO 操控的直接规划器选型有参考价值。
4. **力矩感知规划消除了"先规划后检查"的范式**：3kg 负载下 99.7% vs 77% 的差距表明，忽略动力学在负载场景下是致命的。
5. **人形动作重定向中参考动作质量直接传播到下游 RL 策略**：碰撞自由参考动作降低 MPJPE 和 12× 方差，这个方法论可借鉴到 DLO 操控的 demonstration 质量评估。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[planning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[sundaralingam|Sundaralingam, Balakumar]]
- [[murali|Murali, Adithyavairavan]]
- [[birchfield|Birchfield, Stan]]
