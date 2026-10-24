---
title: "IMPACT: An implicit active-set augmented lagrangian for fast contact-implicit trajectory optimization"
tags: [contact-implicit, trajectory-optimization, MPC, manipulation]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出 IMPACT 方法，基于保护增广拉格朗日 (safeguarded AuLa) 框架求解 MPCC 形式的接触隐式轨迹优化，通过隐式接触分支选择在迭代中自动发现接触模式，在 CITO 基准上实现 2.9x-70x 加速，在 Allegro Hand CI-MPC 基准上控制质量指标全面优于 baseline。"
authors: "Li, Jiayun; Gong, Dejian; Chalvatzaki, Georgia"
year: "2026"
venue: "RSS 2026"
zotero_key: "7E5G3M27"
---
## 摘要

Contact-implicit trajectory optimization (CITO) has attracted growing attention as a unified framework for planning and control in contact-rich（接触丰富） robotic tasks. Recent approaches have demonstrated promising results in manipulation（操控） and locomotion without requiring a prescribed contact-mode schedule. It is well known that the underlying mathematical programs with complementarity constraints (MPCCs) remain numerically ill-conditioned, and systematic, scalable solution strategies for CITO remain an active area of research. More efficient and principled solvers that can handle contact constraints are therefore essential to broaden the applicability of CITO. In this work, we develop an augmented-Lagrangian approach to CITO for solving MPCC-based CITO with stationarity guarantees. The method can be interpreted as identifying the implicit contact-mode branches on the fly during the trajectory optimization (TO) iterations; we call this approach IMPACT (IMPlicit contact ACtive-set Trajectory optimization). We provide an efficient C++ implementation tailored to trajectory-optimization workloads and evaluate it on the open-source CITO and contact-implicit model predictive control (CI-MPC) benchmarks. On CITO, IMPACT achieves 2.9x-70x speedups over strong baselines (geometric mean 13.8x). On CI-MPC, we show improved control quality for contact-rich（接触丰富） trajectories on dexterous manipulation（灵巧操控） tasks in simulation. Finally, we demonstrate the proposed method on real robotic hardware on a T-shaped object pushing task.

## 中文简述

提出 IMPACT 方法，基于保护增广拉格朗日求解 MPCC 形式的接触隐式轨迹优化，CITO 基准 2.9x-70x 加速，Allegro Hand CI-MPC 控制质量全面优于 baseline。

**研究方向**: 机器人操控、模仿学习、运动规划

## 关键贡献

1. **算法**: 提出 IMPACT，基于保护增广拉格朗日 (safeguarded AuLa) 的 CITO 方法，具有 M-stationarity 收敛保证；将互补约束作为硬约束保留在子问题中，而非松弛或惩罚化
2. **内求解器**: 设计块坐标下降 (BCD) 内求解器——X 块用 Gauss-Newton + Armijo 回溯，(Y,Z) 块有闭式解（在两个凸锥候选中选择目标值更小的），理论证明可在有限步内达到任意精度的 ε-stationarity
3. **实现**: 提供 C++ 实现，针对 CITO/CI-MPC 工作负载设计接口，使用 CasADi 符号微分 + Eigen 稀疏 LDLT 分解
4. **验证**: 在两个开源基准上全面评估——CRISP CITO 基准（长期规划）和 Allegro Hand CI-MPC 基准（灵巧操控），并在真实硬件上展示 Push-T 任务
## 结构化提取

- Problem: 接触隐式轨迹优化 (CITO) 中 MPCC 的数值病态问题——标准 NLP 约束条件失败、乘子无界、求解不可靠
- Method: Safeguarded Augmented Lagrangian + Block Coordinate Descent；互补约束作为硬约束保留；隐式接触分支选择；Gauss-Newton + 闭式 (Y,Z) 更新
- Tasks: Push Box, Push T, Cart Transport（CITO 基准）；Allegro Hand 物体重定向（CI-MPC 基准，17 物体）；真实 Push-T（Panda 机器人）
- Sensors: 无传感器（纯模型方法，MuJoCo 仿真 + 真实机器人仅用运动学跟踪）
- Robot Setup: 仿真中 2D pusher + 物体；Allegro Hand（16 DOF）；真实 Franka Panda（7 DOF）+ T 形物体
- Metrics: 成功率、总跟踪误差、迭代数、运行时间、控制方差、控制平滑度、控制耗能、控制频率
- Limitations: 接触模式在紧实时约束下不稳定；局部规划对接触鼓励代价敏感；~10 Hz 控制频率低于 baseline；Stick 物体异常；无全局收敛保证
- Evidence Notes: 全文可获取，所有实验数据来自 Table I 和 Fig. 4；Push-T 真实实验仅报告成功率 100%（10 trials），无定量误差指标
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文通过 arXiv HTML 获取，所有章节均覆盖）
- Confidence: high
- Summary: 提出 IMPACT 方法，基于保护增广拉格朗日 (safeguarded AuLa) 框架求解 MPCC 形式的接触隐式轨迹优化，通过隐式接触分支选择在迭代中自动发现接触模式，在 CITO 基准上实现 2.9x-70x 加速，在 Allegro Hand CI-MPC 基准上控制质量指标全面优于 baseline。


## Problem

接触隐式轨迹优化 (CITO) 是接触丰富机器人任务的统一规划与控制框架，不需要预先指定接触模式序列。然而其底层的互补约束数学规划 (MPCC) 数值病态：标准 NLP 约束条件 (LICQ, MFCQ) 在可行点处失败，Lagrange 乘子可能无界，导致 KKT 条件失效。现有方法（Scholtes 松弛、惩罚法）通过修改互补结构改善数值行为，但会损害控制质量或引入启发式参数。需要一种既保留原始非光滑互补结构、又具有收敛保证且高效的求解方法。


## Method

### 核心思想
将 MPCC 的互补约束 0 ≤ G(x) ⊥ H(x) ≥ 0 通过垂直形式 (vertical form) 引入辅助变量 Y, Z，使 G(x)=y, H(x)=z，互补约束变为简单的 0 ≤ y ⊥ z ≥ 0。

### Safeguarded AuLa 外循环
- 对等式/不等式约束使用增广拉格朗日处理（惩罚项 + 乘子更新）
- 互补约束作为硬约束保留在子问题中，不吸收到增广拉格朗日函数中
- 乘子通过保护边界 (safeguard bounds) 截断防止发散
- 罚参数根据约束违反度充分下降条件自适应增大
- 收敛保证：在标准 MPCC 正则性条件下，每个可行聚点都是 M-stationary

### BCD 内求解器
- **X-块更新**: 固定 (Y,Z)，用阻尼 Gauss-Newton + Armijo 回溯线搜索求解非线性最小二乘
- **(Y,Z)-块更新**: 固定 X，每个互补对 (y_i, z_i) 有闭式解——计算两个候选（Case 1: z=0, y=max(0, G+κ/ρ)；Case 2: y=0, z=max(0, H+κ/ρ)），选目标值更小者
- 停止条件：内层增广目标停滞 |Φ(w^j) - Φ(w^{j+1})| ≤ τ_k

### 隐式接触模式发现
(Y,Z) 更新本质上是在做隐式接触分支选择——每次 BCD 迭代根据当前梯度/乘子方向自动决定每个互补对处于"接触"还是"无接触"分支，无需预设接触序列或 homotopy 调度。


## Experiments

### 基准 1: CRISP CITO（长期规划）
三个任务：Push Box, Push T, Cart Transport
- Push Box: 453 变量, 500 互补对, 150 动力学约束
- Push T: 1353 变量, 2150 互补对, 350 等式 + 200 不等式约束
- Cart Transport: 2404 变量, 900 互补对, 1200 动力学 + 300 等式 + 1200 不等式约束

Baselines: Scholtes Relaxation (SR), Squared Penalty Method (PM), CRISP

| 指标 | IMPACT vs CRISP | IMPACT vs 最快 baseline (PM) |
|------|-----------------|------------------------------|
| 速度提升 | 16.8x, 25.0x, 34.0x (几何均值 24.3x) | 5.7x, 2.9x, 25.0x (几何均值 7.4x) |
| 总体速度范围 | 2.9x-70x (几何均值 13.8x) | — |

轨迹质量（跟踪误差）：IMPACT 在 Push Box 和 Cart Transport 上排名第二（仅次于 SR 和 CRISP），在 Push T 上接近 CRISP。成功率：Push Box 100%, Push T 100%, Cart Transport 100%。

### 基准 2: Allegro Hand CI-MPC（灵巧操控）
17 个物体，Allegro Hand 重定向任务，最多 20 个同时接触点，MPC horizon=4

| 指标 | IMPACT | cfree(0.1) | cfree(0.2) |
|------|--------|------------|------------|
| 成功率 | 91.8%±4.1 | 91.2%±4.2 | 92.9%±3.9 |
| 控制方差 | 1.55±0.13 | 2.16±0.21 | 4.44±0.49 |
| 控制平滑度 | 0.029±0.004 | 0.044±0.008 | 0.088±0.012 |
| 控制耗能 | 3.0±1.0 | 4.8±2.0 | 8.2±4.8 |
| 控制频率 | ~9.5 Hz | ~50 Hz | ~54 Hz |

IMPACT 在控制质量指标上全面优于 cfree，但频率较低。Stick 物体是异常点（长细几何对 LCP 建模敏感）。

### 基准 3: 真实硬件 Push-T
Panda 机器人推动 T 形物体到目标位姿，10 次试验，100% 成功率。通过调优接触半径约束的 sim-to-real 迁移。


## Limitations

1. **有限计算预算下的接触模式稳定性**: 在紧实时约束下，内求解只能做粗略求解，接触分支选择可能在不同迭代间跳变；需要 trust-region 或模式更新迟滞等稳定机制
2. **局部规划与接触鼓励代价依赖**: 在 Allegro Hand 设定下作为局部规划器运行，对局部最小值敏感，依赖启发式接触鼓励代价；在 stick 物体上表现较差（长细几何使接触维护高度敏感）
3. **控制频率**: CI-MPC 下仅 ~10 Hz（vs cfree 的 ~50 Hz），对需要高频率控制的任务可能受限
4. **未涉及**: 全局收敛性（仅保证聚点的 stationarity）、GPU 加速、多线程并行


## Key Takeaways

1. **互补约束不一定要松弛**: IMPACT 证明保留非光滑互补结构并利用 AuLa + BCD 处理是可行且高效的，这挑战了"必须光滑化才能优化"的常见假设
2. **对 DLO 操控的启示**: DLO 操控同样是接触丰富的任务，DLO 与环境的接触模式更复杂（线-面、线-线接触），IMPACT 的隐式接触模式发现框架可能适用于 DLO 轨迹规划
3. **Sim-to-Real 实践**: 论文通过调优接触半径参数实现 Push-T 的 sim-to-real 迁移，表明物理接触模型参数的精细调节是关键
4. **效率与质量的平衡**: IMPACT 通过隐式分支选择在效率上大幅领先，但牺牲了一定的轨迹质量（跟踪误差排名第二），这种权衡在实时控制场景中是可接受的

## 相关概念

- [[contact-implicit-trajectory-optimization]]
- [[trajectory-optimization]]
- [[planning]]
- [[robotic-manipulation]]
- [[deformable-linear-object]]

## 相关研究者

- [[li-jiayun|Li, Jiayun]]
- [[gong-dejian|Gong, Dejian]]
- [[chalvatzaki|Chalvatzaki, Georgia]]
