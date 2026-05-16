---
title: "Reactive Motion Generation via Phase-varying Neural Potential Functions"
tags: [LfD, dynamical-systems, neural-potential-function, reactive-control, phase-variable]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "提出PNPF框架，用闭环相位变量条件化神经势函数以解决DS-LfD中轨迹交叉与状态重访问题，在2D/6D任务和真实UR10机器人上超越CONDOR与NODE"
authors: "[Tekden Ahmet, Kanoulas Dimitrios, Billard Aude, Bekiroglu Yasemin]"
year: "2026"
venue: "IEEE Robotics and Automation Letters (RAL)"
zotero_key: "65WU7TZE"
arxiv_id: "2604.26450"
doi: "10.48550/arXiv.2604.26450"
---
## 摘要

Dynamical systems (DS) methods for Learning-from-Demonstration（示范数据） (LfD) provide stable, continuous policies from few demonstrations. First-order DS are effective for many point-to-point and periodic tasks, as long as a unique velocity is defined for each state. For tasks with intersections (e.g., drawing an "8"), extensions such as second-order dynamics or phase variables are often used. However, by incorporating velocity, second-order models become sensitive to disturbances near intersections. We introduce Phase-varying Neural Potential Functions (PNPF), an LfD framework that conditions a potential function on a phase variable which is estimated directly from state progression, rather than on open-loop（开环） temporal inputs.

## 中文简述

本文提出 PNPF（Phase-varying Neural Potential Functions）框架，通过闭环相位变量条件化神经势函数来解决运动生成中的状态重访问题。框架包含名义能量函数和安全能量函数，分别引导任务行为和维持安全区域。在 2D 和 6D 任务上超越 CONDOR、NODE 等基线，并在 UR10 真实机器人上验证了实时反应性控制。

## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high
- Confidence: high
- Summary: 提出PNPF框架，用闭环相位变量条件化神经势函数以解决DS-LfD中轨迹交叉与状态重访问题，在2D/6D任务和真实UR10机器人上超越CONDOR与NODE
## 关键贡献

1. **PNPF 框架**：基于神经势函数的反应性运动生成框架，通过闭环相位变量条件化势函数，可从少量示教中建模点到点和周期运动，并集成数据驱动的安全集合约束。
2. **闭环相位变量**：从状态进展（nominal energy）直接估计相位变量 s，而非开环时间输入。s 在每次状态更新后重新计算（s ← ϕ_nominal(x'|s)），确保扰动后系统可恢复。
3. **6D 兼容性**：通过四元数切空间中的轴角表示，支持位姿空间（位置+姿态）的运动建模，覆盖配置空间和任务空间。
## 结构化提取

- **Problem**: DS-LfD 方法在轨迹交叉任务中建模能力与反应性之间的矛盾；一阶 DS 无法处理状态重访，二阶 DS 对速度扰动敏感，相位方法依赖开环时间
- **Method**: Phase-varying Neural Potential Functions (PNPF)——闭环相位变量条件化神经势函数，势函数由名义能量（弧长）和安全能量（SDF）组成，控制律为 ẋ = -α∇ₓϕ(x|s)，相位 s 从名义能量闭环估计
- **Tasks**: 点到点运动（打结、倒豆）、周期运动（8字擦拭）、6D 位姿控制、障碍物规避、扰动恢复
- **Sensors**: 关节编码器（关节角度空间任务）、AprilTag（障碍物追踪）、动觉示教采集
- **Robot Setup**: UR10 + RG2-FT 夹爪，控制频率 50 Hz，任务空间和关节空间均支持
- **Metrics**: DTW Distance (DTWD), Fréchet Distance (FD), Final Position Error, Accuracy (≤2cm), DTWD-P, DTWD-O, Final Orientation Error
- **Limitations**: 尖角过度平滑、仅限单模态任务、示教伪影传播、安全集合依赖生成质量
- **Evidence Notes**: 论文提供了完整的仿真和真实机器人实验证据。仿真在 LASA/LAIR/CHAR/RoboTasks 四个数据集上对比 CONDOR、NODE、LPVDS 三个基线，使用 DTWD、FD、FP Error、Accuracy 四项指标，所有数据集上 PNPF 均取得最佳平均成绩。CHAR 数据集上 DTWD 降低约 83%（2.96 vs 17.67 mm）。稳定性验证覆盖 10⁵ 个扰动采样点，99.999% 成功。真实机器人在三个 6D 任务上各 10 个初始位置测试，全部成功，含障碍物和空间扰动实验。控制频率达 50 Hz。CONDO R 的原始实现未分离训练/测试集，作者修改后分离，导致其性能略低于原始报告。
## 本地引用关系

-
## Problem

基于动力学系统（DS）的 Learning-from-Demonstration（LfD）方法面临建模能力与反应性之间的根本矛盾：

1. **一阶 DS 方法**（如 SEDS、LPVDS）仅依赖当前状态生成运动，具有良好的反应性（受扰动后可恢复），但无法处理同一状态在不同时刻被重复访问的任务（如画"8"字、打结），因为每个状态只能映射到唯一速度。
2. **二阶 DS 扩展**通过引入速度信息来区分交叉点的运动方向，但存在两个关键局限：(i) 交叉点附近对速度扰动极其敏感；(ii) 当不同运动段在交叉前产生几乎相同的位置-速度对时，无法正确消歧（如打结任务中 ẋ₁ 和 ẋ₂ 的歧义）。
3. **相位/时间相关方法**（如 DMP、ProMP）用开环时间/相位变量处理状态重访，但受限于开环调度，扰动恢复能力差。

核心问题：如何在保持 DS 风格反应性的同时，获得与运动基元相当的建模能力（处理交叉轨迹、周期运动、6D 任务）？


## Method

### 核心架构

势函数定义为 **ϕ(x|s) = ϕ_nominal(x|s) + k_safety · Λ_safety(s) · ϕ_safety(x|s)**，其中 x ∈ ℝᵈ 为状态，s 为相位变量。

### 轨迹合成

- 使用 **decoder-only 神经网络 + hypernetwork** 从示教中学习生成模型
- 为每条示教分配可学习嵌入，与网络权重联合优化
- 推理时从训练嵌入向量的凸包中采样潜在向量 h'，生成新轨迹
- **名义轨迹** x*(t)：选择与所有示教 DTW 距离之和最小的生成轨迹
- **安全集合** C：通过生成轨迹构建密集采样，计算有符号距离函数（SDF）

### 能量函数设计

1. **名义能量 ϕ_nominal(x|s)**：
   - 基于名义轨迹的剩余弧长，沿轨迹单调递减至 0
   - 离轨迹点的能量通过投影到最近名义轨迹点近似（Eq. 1）
   - **关键创新**：将 ϕ_nominal 本身作为相位变量 s（闭环估计）

2. **安全能量 ϕ_safety(x|s)**：
   - 基于 SDF，引导系统返回示教覆盖区域
   - 仅在安全集合外激活（使用 relu + 平滑函数）
   - Λ_safety(s) 随任务进展增加安全项权重

### 控制律

**ẋ = -α∇ₓϕ(x|s)，s ← ϕ_nominal(x'|s)**（Eq. 3）

相位变量在每步从新状态重新估计，实现闭环相位跟踪。

### 周期运动处理

- 相位输入使用正弦编码：s̊_k = [sin(2πs/s_T), cos(2πs/s_T)]
- 相位更新：s ← s - (ϕ_nominal(x|s̊) - ϕ_nominal(x'|s̊))（Eq. 5）
- 支持多周期执行

### 6D 运动建模

- 方向用单位四元数表示，转换到末端四元数的切空间轴角表示
- r_t = Log(q_t * q̄_T)，连续化后与笛卡尔轨迹统一建模
- 推理时 -∇ϕ 直接输出角速度用于机器人控制

### 神经场建模

- 使用 **hypernetwork 条件化 MLP**：hypernetwork 接收位置编码的相位 s，MLP 接收无位置编码的状态 x
- 利用 ReLU MLP 的谱偏置（倾向于学习平滑低频函数），确保 ∇ₓϕ 在状态空间中平滑
- 训练采用 AdamW 优化器
- 包含轻量级采样安全机制：梯度停滞时激活采样候选动作

### 稳定性分析

- 使用 V(x,s) = ϕ(x|s) 作为 Lyapunov 函数候选
- 假设示教局部一致性：∇ₓϕ_nominal ⊺ ∇ₓϕ_safety ≥ -ε‖∇ₓϕ_nominal‖²
- 证明 V̇ ≤ 0，由 LaSalle 不变性原理，轨迹收敛到目标集合 S
- 限制：仅适用于单模态任务


## Experiments

### 数据集

| 数据集 | 维度 | 类型 | 示教数/轨迹 |
|--------|------|------|-------------|
| LASA | 2D | 点到点 | 多种手写形状 |
| LAIR | 2D | 点到点（交叉） | 多种含环/交叉轨迹 |
| CHAR (新) | 2D | 点到点（交叉+歧义） | 5种含相似运动段但需不同后续动作的轨迹 |
| CHAR-Periodic (新) | 2D | 周期 | 周期运动 |
| RoboTasks | 6D | 点到点 | 位置+姿态 |

### 基线方法

- **NODE**（Neural ODE with safety/stability guarantees）
- **CONDOR**（Stable motion primitives via imitation and contrastive learning）
- **LPVDS**（Linear Parameter-Varying DS）
- Naive（仅重复周期段）

### 主要结果（Table I）

**LASA (cm)**:
| 方法 | DTWD | FD | FP Error | Accuracy |
|------|------|-----|----------|----------|
| **PNPF** | **1.81** | **3.38** | **0.02** | **1.00** |
| CONDOR | 2.10 | 4.14 | 0.10 | 1.00 |
| NODE | 2.12 | 4.33 | 1.82 | 0.76 |

**LAIR (mm)**:
| 方法 | DTWD | FD | FP Error | Accuracy |
|------|------|-----|----------|----------|
| **PNPF** | **4.82** | **11.75** | **5.04** | **1.00** |
| CONDOR | 7.62 | 17.43 | 7.91 | 0.96 |

**CHAR (mm)**（含交叉歧义的关键数据集）:
| 方法 | DTWD | FD | FP Error | Accuracy |
|------|------|-----|----------|----------|
| **PNPF** | **2.96** | **8.44** | **2.00** | **1.00** |
| PNPF-50 | 3.16 | 8.70 | 2.02 | 1.00 |
| PNPF-H | 3.35 | 9.40 | 2.01 | 1.00 |
| CONDOR | 17.67 | 45.56 | 3.25 | 1.00 |

PNPF 在 CHAR 上 DTWD 相比 CONDOR 降低约 83%。

**RoboTasks (6D)**:
| 方法 | DTWD-P (cm) | DTWD-O (rad) | FP Error (cm) | F0 Error (rad) |
|------|-------------|--------------|---------------|----------------|
| **PNPF** | **2.19** | **0.08** | **0.25** | 0.17 |
| NODE | 2.62 | 0.10 | 1.51 | **0.13** |

### 稳定性验证

- 100 步闭环 rollout 分析，100 个相位值 × 1000 个扰动状态
- 在超过 99.999% 的采样情况中，相位变量和总势能单调递减或系统到达终端区域
- 启用安全机制后达到 100% 成功率

### 扰动恢复实验

- **障碍物规避**：GShape 任务（LASA），使用排斥势能实现基础避障
- **空间扰动**：double loop 任务（LAIR），CONDOR 跳过或重复运动段，LPVDS 偏离示教路径，PNPF 平滑恢复
- 原因：PNPF 的相位更新是进度感知的（progress-aware），而基线依赖速度推断任务进展

### 真实机器人实验

- **平台**：UR10 + RG2-FT 夹爪
- **任务 1 - 打结**：机器人将绳子绕圆柱体一圈后插入指定孔位（6 条示教，6D）
- **任务 2 - 倒豆**：将一杯豆子倒入另一容器（6 条示教，关节角度空间）
- **任务 3 - 3D 擦拭**：周期性 8 字运动（2 条示教，6D）
- **测试**：每个任务 10 个不同起始位置，全部成功完成
- **障碍物规避**：3 个 3.5cm 方块（AprilTag 追踪），两种配置均成功
- **空间扰动**：(i) 移动任务板，(ii) 手动移位末端执行器，均成功恢复
- **控制频率**：高达 50 Hz 在线运行


## Limitations

1. **尖角过度平滑**：由于局部能量公式的歧义性，方法倾向于过度平滑轨迹中的尖锐拐角（如 capricorn 任务中可见）
2. **仅限单模态任务**：稳定性证明要求示教局部一致性假设（每个相位处的对齐速度产生局部一致的运动方向），不适用于多模态任务
3. **示教伪影传播**：人类示教中的伪影（如打结中的不规则性）会传播到名义轨迹并降低性能
4. **安全集合依赖生成质量**：安全集合通过生成轨迹构建，生成模型质量直接影响安全约束的有效性
5. **未来方向**：论文指出将改进能量设计以更好保持方向结构，并整合视觉和力反馈


## Key Takeaways

1. **闭环相位 vs 开环时间**：PNPF 的核心洞察是将势函数条件化在从状态进展估计的闭环相位变量上，而非开环时间。这对 DLO 操控有启发——打结、缠绕等任务天然存在状态重访问题，需要反应性控制来应对绳索形变带来的扰动。

2. **安全能量作为数据驱动约束**：安全能量通过 SDF 从示教数据中学习安全区域，而非人工定义。这提供了一种将示教覆盖范围编码为可微分约束的范式，可借鉴用于 DLO 操控中的工作空间约束。

3. **势函数组合性**：ϕ = ϕ_nominal + ϕ_safety + ϕ_obstacle 的模块化设计允许灵活添加额外能量项（如障碍物规避）。在 DLO 场景中，可考虑添加绳索碰撞规避、缠绕约束等能量项。

4. **与 VLM 的潜在结合点**：PNPF 的相位变量本质上编码了任务进度。如果将相位估计替换为 VLM 输出的语义进度信号，可能实现语言/视觉引导的反应性操控。

5. **神经场用于运动建模**：使用 hypernetwork 条件化的神经场来参数化势函数，保证了梯度的平滑性和连续性。这种参数化方式可能适用于更高维度的 DLO 状态空间表示。

## 相关概念

- [[imitation-learning]]
- [[dynamical-systems]]
- [[robotic-manipulation]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[tekden-ahmet|[Tekden Ahmet, Kanoulas Dimitrios, Billard Aude, Bekiroglu Yasemin]]]
