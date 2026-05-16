---
title: "FLASH: Fast learning via GPU-accelerated simulation for high-fidelity deformable manipulation in minutes"
tags: [manipulation, imitation, sim-to-real, robot-learning, physics-simulation]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "GPU 原生可变形物体仿真框架，基于 NCP 接触求解器和 Projective Dynamics 实现 3M+ DoF 实时仿真，训练策略分钟级完成并零样本迁移到真实双臂机器人完成衣物折叠"
authors: "Luo, Siyuan; Zhou, Bingyang; Zhang, Chong; Liu, Xin; Huang, Zhenhao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CPZZ9BAE"
---
## 摘要

Simulation frameworks such as Isaac Sim have enabled scalable robot learning for locomotion and rigid-body manipulation（操控）; however, contact-rich（接触丰富） simulation remains a major bottleneck for deformable object（可变形物体） manipulation（操控）. The continuously changing geometry of soft materials, together with large numbers of vertices and contact constraints, makes it difficult to achieve high accuracy, speed, and stability required for large-scale interactive learning. We present FLASH, a GPU-native simulation framework for contact-rich（接触丰富） deformable manipulation（操控）, built on an accurate NCP-based solver that enforces strict contact and deformation constraints while being explicitly designed for fine-grained GPU parallelism. Rather than porting conventional single-instruction-multiple-data (SIMD) solvers to GPUs, FLASH redesigns the physics engine from the ground up to leverage modern GPU architectures, including optimized collision handling and memory layouts. As a result, FLASH scales to over 3 million degrees of freedom at 30 FPS on a single RTX 5090, while accurately simulating physical interactions. Policies trained solely on FLASH-generated synthetic data in minutes achieve robust zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer, which we validate on physical robots performing challenging deformable manipulation（操控） tasks such as towel folding and garment folding, without any real-world demonstration（示范数据）, providing a practical alternative to labor-intensive real-world data collection.

## 中文简述

提出基于力控制的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、机器人学习、物理仿真

## 关键贡献

1. **高性能可变形仿真与渲染**：从零设计的 GPU 优化架构，基于非光滑 Newton 求解器，在单块 RTX 5090 上实现 3M+ DoF 接触丰富场景 30fps 实时仿真，比传统方法快 100-300x
2. **高通量合成数据训练**：全自动管线，无需真实世界示范数据，利用大规模仿真交互、系统化 domain randomization 和状态监督来训练视觉操控策略
3. **零样本 Sim-to-Real 迁移**：高保真接触建模和遮挡感知深度渲染，使纯仿真训练的策略可直接部署到真实机器人
4. **跨物体和设置的通用性**：支持多种可变形物体（布料和体积材料）和不同学习设置，无需针对任务重新设计仿真器
## 结构化提取

- Problem: 可变形物体操控仿真中物理保真度与计算吞吐量不可兼得，接触丰富场景下 Schur 补稠密化导致大规模并行不可行
- Method: GPU-native Projective Dynamics + NCP 接触 + 惯性主导稀疏近似 + 非光滑 Newton 求解器 + Teacher-Student DAgger 蒸馏 + Domain Randomization
- Tasks: 毛巾折叠（单臂/双臂/人形）、T 恤折叠、短裤折叠
- Sensors: 深度相机（ZED Mini，俯视），本体感知（关节状态）
- Robot Setup: Airbot Play（6-DoF 双臂桌面臂 + 平行夹爪）、AdamU（上半身人形 + 灵巧手）
- Metrics: 成功率（5cm 内 + 40s 超时）、仿真吞吐量（ms/step）、训练时间（wall-clock）
- Limitations: CPU-GPU 传输开销、深度传感器薄织物噪声、缺乏触觉反馈、二值抓取模型、渲染线性扩展
- Evidence Notes: 跨仿真器视觉对比（Fig.4）；参数消融（Fig.4b）；并行吞吐量表（Table II）；AdamU 连续 1h 106 次试验 85.8%（Fig.7）；T 恤 70%（35/50）；短裤 60%（12/20）；恢复行为演示（Fig.6）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete (正文 + 补充材料全部覆盖)
- Confidence: high
- Summary: GPU 原生可变形物体仿真框架，基于 NCP 接触求解器和 Projective Dynamics 实现 3M+ DoF 实时仿真，训练策略分钟级完成并零样本迁移到真实双臂机器人完成衣物折叠


## Problem

可变形物体操控是机器人领域的长期挑战。现有仿真器无法同时满足高物理保真度和高计算吞吐量：CPU 精度引擎缺乏可扩展性，GPU 方案受限于求解器级并行不足和低效内存访问。接触丰富的软体仿真中，大量顶点和接触约束使 Schur 补矩阵变稠密，导致大规模并行仿真不可行。


## Method

### 仿真核心
- **基础框架**：基于 Projective Dynamics 的 local-global 流水线，FEM 离散化，隐式 Euler 积分
- **接触建模**：NCP（Nonlinear Complementarity Problem）基于 Lagrange 乘子的接触约束，Signorini-Coulomb 摩擦定律
- **非光滑 Newton 求解器**：saddle-point 系统求解，Cholesky 分解的稀疏表示 A⁻¹ = S⊤S，使全局求解和 Schur 补计算可表达为稀疏矩阵乘法
- **轻量化近似**：用 M⁻¹ 替代 A⁻¹ 构建 Schur 补（惯性主导近似），保持稀疏性同时保留数值鲁棒性
- **多环境并行**：block-diagonal 组装，所有核心操作使用标准稀疏原语，计算开销随环境数线性增长

### 渲染与 Real-to-Sim
- 几何建模：程序化生成简单物体，3D 扫描重建复杂衣物
- 物理标定：Poisson 比、Young 模量对齐（grid search 最小化点云到网格距离）
- 深度渲染：ray-casting 管线（GPU OptiX / CPU Embree），支持 domain randomization（随机遮挡、边界噪声、自遮挡）

### 策略学习
- **Teacher-Student 蒸馏**：
  - Teacher：基于布料状态的层次有限状态机，使用启发式规则驱动末端执行器抓取/运输关键点
  - Student：CNN 编码深度图 + MLP 处理本体感知，5 步历史堆叠，输出 EE 位置增量 + gripper 开/闭
  - DAgger 训练，MAE loss（位置）+ log-probability loss（gripper）+ 辅助 MSE loss（状态重建）
- **Domain Randomization**：布料动力学参数（0.5x~1.5x）、初始状态、本体感知噪声、感知扰动

### Sim-to-Real 部署
- 感知：YOLOv8 + SAM2 分割目标物体深度图
- 控制：策略输出 EE 位置增量 → 数值 IK → 高频低级控制器
- 双臂输出 8 维动作（每臂 Δp ∈ ℝ³ + w ∈ ℝ）


## Experiments

### 跨仿真器比较（T 恤双袖折叠）
| 仿真器 | 表现 |
|--------|------|
| FLASH | 最接近真实：平滑对称折叠、稳定落位、准确摩擦粘附 |
| Genesis (PBD) | 大弹性回弹、摩擦不稳定、持续滑动 |
| Isaac Sim (FEM) | 剪切畸变、过度褶皱、拉伸-弯曲耦合困难 |
| Newton (VBD) | 弯曲过刚、折袖未贴桌面、弹性展开 |

### 大规模并行吞吐量（ms/step）
| 环境数 | FLASH | Genesis | Isaac Sim | Newton |
|--------|-------|---------|-----------|--------|
| 1 | 5.68 | 5.97 | 18.02 | 9.57 |
| 64 | 50.43 | N/A | 22.62 | 52.79 |
| 256 | 185.10 | N/A | 47.81 | 480.64 |

Genesis 在多环境下数值不稳定发散。

### 仿真训练时间（单块 RTX 5090）
| 任务 | 训练时间 |
|------|----------|
| 单臂毛巾折叠 | 50 min |
| 人形机器人毛巾折叠 | 50 min |
| 双臂毛巾折叠 | 150 min |
| T 恤折叠 | 600 min |
| 短裤折叠 | 600 min |

### 真实机器人实验
- **平台**：Airbot Play（6-DoF 桌面臂）+ AdamU（上半身人形）
- **感知**：ZED Mini 俯视深度相机
- **毛巾折叠（AdamU 1 小时连续评估）**：85.8% 成功率（91/106），成功标准 = 5cm 内 + 40s 超时
- **T 恤折叠**：70% 成功率（35/50）
- **短裤折叠**：60% 成功率（12/20）
- **鲁棒性**：容忍 ±8cm 初始位置偏移 + 任意旋转；展示恢复行为（抓取失败重试、人类干扰恢复）

### 参数消融
- 控制速度增加 10x → 肩部区域更紧（动态拉动效应）
- 弯曲刚度增加 → 肩部抬升和弹性回弹增大
- 极低求解器迭代（2 次）→ 远程弹性耦合减弱但仍数值稳定


## Limitations

1. **CPU-GPU 传输开销**：部分管线仍有 CPU-GPU 数据搬运，优化空间
2. **感知瓶颈**：深度传感器噪声在薄织物上表现差、自遮挡导致抓取偏移（占真实失败的大部分）
3. **硬件抽象间隙**：统一二值抓取模型忽略电机级动力学（驱动延迟、backlash），缺乏触觉反馈
4. **复杂长时域操控**：需要改进学习公式和监督信号（更有效的奖励/反馈设计）
5. **渲染线性扩展**：当前 ray-casting 因动态顶点更新导致线性增长，未来可用 batched geometry updates 优化


## Key Takeaways

1. **求解器级 GPU 并行设计**是可变形仿真可扩展性的关键——不能简单移植 SIMD 求解器到 GPU，需要从底层重新设计
2. **惯性主导近似**（M⁻¹ 替代 A⁻¹）是接触丰富场景中保持稀疏性的有效策略，在软材料操控中精度-效率权衡良好
3. **Teacher-Student + Domain Randomization** 的仿真训练管线已可支撑零样本迁移，无需真实数据
4. **深度图（非 RGB）** 作为策略输入在 Sim-to-Real 中差距更小，但薄织物上的噪声仍是主要失败源
5. 对 DLO 操控的启示：FLASH 的 NCP 接触模型和轻量化求解思路可适用于 DLO 与环境的丰富接触场景

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[luo-siyuan|Luo, Siyuan]]
