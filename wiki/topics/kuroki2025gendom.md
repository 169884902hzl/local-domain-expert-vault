---
title: "GenDOM: Generalizable one-shot deformable object manipulation with parameter-aware policy"
tags: [manipulation, imitation, DLO]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用网格密度损失从单次真实演示估计参数。仿真中 ID 提升 62%、OOD 提升 15%，真实世界绳索提升 26%、布料提升 50%。仅需 1 次真实演示。"
authors: "Kuroki, So; Guo, Jiaxian; Matsushima, Tatsuya; Okubo, Takuya; Kobayashi, Masato et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "T9YUGAYP"
---
## 摘要

Due to the inherent uncertainty in their deformability during motion, previous methods in deformable object（可变形物体） manipulation（操控）, such as rope and cloth, often required hundreds of real-world demonstrations to train a manipulation（操控） policy for each object, which hinders their applications in our ever-changing world. To address this issue, we introduce GenDOM, a framework that allows the manipulation（操控） policy to handle different deformable objects with only a single real-world demonstration（示范数据）. To achieve this, we augment the policy by conditioning it on deformable object（可变形物体） parameters and training it with a diverse range of simulated deformable objects so that the policy can adjust actions based on different object parameters. At the time of inference, given a new object, GenDOM can estimate the deformable object（可变形物体） parameters with only a single real-world demonstration（示范数据） by minimizing the disparity between the grid density of point clouds of real-world demonstrations and simulations in a differentiable physics simulator. Empirical validations on both simulated and real-world object manipulation（操控） setups clearly show that our method can manipulate different objects with a single demonstration（示范数据） and significantly outperforms the baseline in both environments (a 62% improvement for in-domain ropes and a 15% improvement for out-of-distribution ropes in simulation, as well as a 26% improvement for ropes and a 50% improvement for cloths in the real world), demonstrating the effectiveness of our approach in one-shot（单样本） deformable object（可变形物体） manipulation（操控）.

## 中文简述

提出基于点云的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、可变形物体操控

## 关键贡献

1. **参数感知策略（Parameter-Aware Policy）**：首次将 Young's modulus 和 Poisson's ratio 作为策略输入条件，使策略能根据物体动力学参数调整动作。在仿真中随机采样参数训练，一个网络覆盖多种物体。
2. **梯度 Real2Sim 参数估计**：基于可微分物理仿真器（PlasticineLab），通过最小化点云网格密度（64³）L1 损失，从单次真实演示估计物体参数。仅需 1 次演示，无需大量标注数据。
3. **One-shot 泛化验证**：仿真 ID 提升 62%、OOD 提升 15%（vs R2S2R）；真实世界绳索（3 种）提升 26%、布料（2 种）提升 50%。
## 结构化提取

- **Problem**: 可变形物体操控需要针对每个物体收集大量真实演示（数百次），不同物体动力学差异大。Real2Sim2Real 仍需 20+ 演示。如何用单次演示实现泛化？
- **Method**: GenDOM：参数感知策略（条件化于 Young's modulus + Poisson's ratio）+ 梯度 Real2Sim 参数优化（可微分物理仿真器 + 64³ 网格密度 L1 损失）。仿真中随机采样参数训练 MLP，推理时从单次真实演示估计参数。
- **Tasks**: Rope reaching（绳端到目标位置）、Rope casting（空中瞬时动作）、Cloth spreading（布料展开）。仿真 + 真实世界。
- **Sensors**: 两个 Intel RealSense D435i RGB-D 相机（点云采集），xArm 7 机器人。
- **Robot Setup**: xArm 7（7-DOF），预定义垂直提升动作用于参数估计，策略预测释放坐标/加速度。
- **Metrics**: 目标坐标误差（cm，3 trials 均值±标准差），展开比例，加速比，Chamfer Distance（Real2Sim）。
- **Limitations**: 仅 3 绳 + 2 布；简单开环任务；线性各向同性假设；仿真器限制；预定义动作；无闭环反馈；评估度量有限。
- **Evidence Notes**: 参数估计有 Sim2Sim 和 Real2Sim 对比（Tab. II-III），梯度法显著优于 PointNet++。泛化有 ID/OOD 对比（Tab. V，40 goal coordinates）。真实世界有 3 种绳 × 7 目标 × 3 trials（Tab. VI）和 2 种布 × 5 trials（Tab. VII）。消融验证参数贡献（Tab. IV）。整体证据强度：中-强（定量表格 + 真实实验，但任务简单且物体种类有限）。
## 本地引用关系

- [[antonova2021bayesian]]
- [[blancomulero2024benchmarking]]
## 证据元数据

- **Zotero Key**: T9YUGAYP
- **Citekey**: kuroki2025gendom
- **Authors**: Kuroki So, Guo Jiaxian, Matsushima Tatsuya, Okubo Takuya, Kobayashi Masato, Ikeda Yuya, Takanami Ryosuke, Yoo Paul, Matsuo Yutaka, Iwasawa Yusuke
- **Affiliation**: The University of Tokyo + Osaka University
- **Venue**: arXiv preprint, 2025-01 (v4)
- **Paper Type**: Methods paper (one-shot deformable object manipulation via parameter-aware policy)
- **Fulltext Quality**: Complete, 6 pages with tables, figures, and comprehensive experiments
- **Evidence Coverage**: High for parameter estimation and generalization (Tab. II-VII); High for real-world deployment (Tab. VI-VII); Medium for cloth extension (single task)
- **Confidence**: High on simulation comparison (40 goal coordinates, 3 trials/real); Medium on cloth generalization (2 cloths only)
- **Summary**: 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用网格密度损失从单次真实演示估计参数。仿真中 ID 提升 62%、OOD 提升 15%，真实世界绳索提升 26%、布料提升 50%。仅需 1 次真实演示。


## Problem

可变形物体操控需要针对每个物体收集大量真实世界演示（通常数百次），因为不同物体的变形特性（弹性、塑性）差异巨大。现有 Sim-to-Real 方法要么需要大量真实数据调参，要么泛化能力有限。Real2Sim2Real 方法仍需 20+ 演示进行参数估计。核心挑战：如何用单次真实演示即可操控不同可变形物体？


## Method

### 参数感知策略训练（Fig. 2a）
- 随机采样 Young's modulus p_y ~ U(500, 10500) 和 Poisson's ratio p_l ~ U(0.2, 0.4)
- 在仿真中执行动作，收集（目标坐标 g, 释放坐标 r, p_y, p_l）
- 训练 MLP 策略 π(r | g, p_y, p_l)，L1 损失

### 梯度 Real2Sim 参数优化（Fig. 2b）
- 机器人执行预定义提升动作（垂直提起物体）
- 两个 RGB-D 相机记录点云轨迹
- 可微分物理仿真器中执行相同动作
- 将仿真和真实点云转换为 64³ 网格密度
- 最小化 L1 网格密度损失，反向传播优化 p_y 和 p_l
- 用估计的参数条件化预训练策略执行操控

### 三个任务
1. **Rope reaching**：控制绳端到释放坐标，使绳摆动到目标位置
2. **Rope casting**：空中瞬时动作，使绳端到达目标坐标
3. **Cloth spreading**：控制布料中心，加速展开到桌面


## Experiments

### 参数估计（Tab. II-III）
- Sim2Sim：梯度法 Young's modulus 差 11.69 vs PointNet++ 173.51（显著优势）
- Real2Sim：3 种绳索的 Chamfer Distance 均优于 PointNet++（如 cotton 0.034 vs 0.092）
- 估计参数：cotton [1779, 0.35]，polyester [3276, 0.35]，polyethylene [8000, 0.36]

### 消融（Tab. IV）
- 两个参数联合使用效果最好：Rope reaching 0.024 vs 无参数 0.062

### 泛化（Tab. V）
| 方法 | ID | OOD |
|------|-----|-----|
| GenDOM | 0.031±0.050 | 0.039±0.042 |
| R2S2R (three ropes) | 0.082±0.081 | 0.096±0.104 |
| R2S2R (cotton rope) | 0.047±0.033 | 0.046±0.044 |

### 真实世界绳索（Tab. VI）
- GenDOM (sim+real) 全面最优：cotton 0.112, polyester 0.076, polyethylene 0.193
- 比 π_RD（300 真实演示训练）提升 10-32%
- 比 R2S2R 提升 44%

### 真实世界布料（Tab. VII）
- 有参数：cotton 展开 0.78（加速比 1.70），rubber 展开 0.98（加速比 0.26）
- 无参数：cotton 展开 0.52，rubber 展开 0.97
- 参数感知策略对 cotton 提升 50%


## Limitations

1. **仅 3 种绳索 + 2 种布料**：物体多样性有限，未验证更复杂物体（如弹簧绳、弹性带、厚布料）。
2. **简单任务**：Rope reaching/casting 是开环动作（单步），Cloth spreading 也是预设轨迹+加速度调节。未涉及闭环操控（如折叠、打结、穿缆）。
3. **线性各向同性假设**：使用 Young's modulus + Poisson's ratio 假设线性弹性，无法表征非线性和各向异性材料。
4. **仿真器限制**：PlasticineLab 基于粒子动力学，与真实物理有差距。参数范围 [500, 10500] 是人为设定的。
5. **预定义动作**：Real2Sim 参数估计需要机器人执行固定的提升动作，不能从任意操控演示估计参数。
6. **无闭环反馈**：策略是开环的（预测释放坐标/加速度后直接执行），无法在线修正。
7. **评估度量有限**：仅用目标坐标误差（cm）和展开比例，未用成功率等更全面的度量。


## Key Takeaways

1. **参数感知策略是 DLO 泛化的有效路径**：将物理参数作为策略输入条件，可在单次演示后快速适配新物体。这一思路可扩展到双臂 DLO 操控——将绳索刚度、阻尼等参数作为策略条件。
2. **与 [[antonova2021bayesian]]（BayesSim-RKHS）对比**：两者都从真实数据推断可变形物体参数。Antonova et al. 用贝叶斯推断+RKHS 嵌入（1500 仿真），GenDOM 用可微分物理+网格密度（单次演示）。GenDOM 更高效，但假设线性弹性。
3. **与 [[blancomulero2024benchmarking]]（Cloth Benchmark）互补**：Blanco-Mulero et al. 量化仿真器 reality gap，GenDOM 通过 Real2Sim 参数估计缩小 gap。两者结合：先用基准选择仿真器，再用 GenDOM 自动调参。
4. **对本研究方向的启示**：双臂 DLO 操控的 one-shot 泛化可将 DLO 物理参数（刚度、阻尼、摩擦系数）作为策略条件。结合可微分仿真器，从真实穿缆演示中估计参数，实现快速适配新绳索。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[sim-to-real]]
- [[bimanual-manipulation]]

## 相关研究者

- [[kuroki|Kuroki, So]]
