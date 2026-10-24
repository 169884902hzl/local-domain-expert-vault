---
title: "Constraining Gaussian Process Implicit Surfaces for Robot Manipulation via Dataset Refinement"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 COGIS 方法，在部分可观测环境中在线学习障碍物几何模型（GPIS）并通过约束优化精化数据集。利用名义动力学模型预测与实际状态差异推断接触点，结合视觉预处理/后处理清洗标签，CMAwM 优化数据子集使 GPIS 满足任务约束（碰撞自由路径/无穿透）。仿真线缆 83.3% 成功率 vs TAMPC 50%/baseline 3.3%，真实线缆 10/10 vs TAMPC 2/10 vs ablation 10/10（但 episode 更短）"
authors: "Kumar, Abhinav; Mitrano, Peter; Berenson, Dmitry"
year: "2022"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "MFNMMWQ4"
---
## 摘要

Model-based control faces fundamental challenges in partially-observable environments due to unmodeled obstacles. We propose an online learning and optimization method to identify and avoid unobserved obstacles online. Our method, Constraint Obeying Gaussian Implicit Surfaces (COGIS), infers contact data using a combination of visual input and state tracking, informed by predictions from a nominal dynamics model. We then ﬁt a Gaussian process（高斯过程） implicit surface (GPIS) to these data and reﬁne the dataset through a novel method of enforcing constraints on the estimated surface. This allows us to design a Model Predictive Control (MPC) method that leverages the obstacle estimate to complete multiple manipulation（操控） tasks. By modeling the environment instead of attempting to directly adapt the dynamics, our method succeeds at both low-dimensional peg-in-hole tasks and high-dimensional deformable object（可变形物体） manipulation（操控） tasks. Our method succeeds in 10/10 trials vs 1/10 for a baseline on a real-world cable manipulation（操控） task under partial observability of the environment.

## 中文简述

提出基于高斯过程的线缆操控方法，具有接触丰富特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III-IV)、experiments (Sec V)、tables (I-II)、figures (1-6)、所有算法伪代码
- **Confidence**: high — 全文完整，IEEE RA-L 2024 论文，peg-in-hole + 仿真线缆 + 真实线缆操控系统评估，30 次试验统计
- **Summary**: 提出 COGIS 方法，在部分可观测环境中在线学习障碍物几何模型（GPIS）并通过约束优化精化数据集。利用名义动力学模型预测与实际状态差异推断接触点，结合视觉预处理/后处理清洗标签，CMAwM 优化数据子集使 GPIS 满足任务约束（碰撞自由路径/无穿透）。仿真线缆 83.3% 成功率 vs TAMPC 50%/baseline 3.3%，真实线缆 10/10 vs TAMPC 2/10 vs ablation 10/10（但 episode 更短）
## 关键贡献

1. 在线障碍物几何建模：融合视觉输入 + 动力学推断的接触数据 + GPIS
2. 数据集精化：CMAwM 优化数据子集使 GPIS 满足任意约束（不需可微/凸）
3. 动力学信息接触推断：比较名义模型预测与实际状态差异识别接触点
4. 视觉预处理/后处理：减少假阳性接触，防止已知自由空间被错误占据
## 结构化提取

- **Problem**: 部分可观测环境中未建模障碍物导致的操控失败
- **Method**: COGIS — 动力学推断接触 + GPIS 障碍物建模 + CMAwM 约束精化 + MPPI 控制
- **Tasks**: Peg-in-hole（3 环境）+ 仿真线缆 + 真实线缆
- **Sensors**: RGB-D 相机 + 关节编码器 + 力/力矩（间接）
- **Robot Setup**: PyBullet/MuJoCo 仿真 + 真实双臂机器人
- **Metrics**: 成功率（30 trials）+ 控制步数
- **Limitations**: 动力学误差=接触假设、核参数敏感、静态环境
- **Evidence Notes**: 全文读取，Tables I-II 提供完整成功率+参数设置
## 本地引用关系

- [[chen2025deformpam]]
- [[collins2025shapespace]]
- [[li2025routing]]
## Problem

模型基控制在部分可观测环境中面临未建模障碍物挑战。特别是高维可变形物体操控中，动力学模型无法预测与遮挡障碍物的接触。现有方法（在线动力学适应、TAMPC）在高维状态空间中数据需求大或信号稀疏。


## Method

- **接触推断**：
  - 观察 (Xt, ut, Xt+1)，名义模型预测 X̂t+1
  - 标签 Y = min(dx(Xt,Xt+1)/dx(Xt,X̂t+1), 1)，Ŷ = 2Y-1
  - Y ≤ 0.5 → 接触，X̂ 对应内部点
- **视觉预处理**：
  - 投影到深度图判断可见性
  - 可见点标签设为 1（外部），接触可见障碍物的点标签设为 0
  - 仅添加不可见内部点和可见接触点
- **GPIS 建模**：
  - GPIS(x) < 0 内部、= 0 表面、> 0 外部
  - Matern 核（ν=1.5），梯度下降更新参数
- **约束精化（CMAwM）**：
  - 二值优化：max c·ω s.t. h_all(D̄,ω,...)
  - c = σ(Σ K(D̄,Di))：偏好保留与全数据集相似的点
  - Peg-in-hole 约束：连通分量保证碰撞自由路径
  - 线缆约束：μ+Φ⁻¹(ζ)σ ≤ 0 防止线缆状态穿透表面
- **MPC 控制器**：
  - MPPI 框架，目标函数 = 目标代价 + 动作正则 + 碰撞代价 + 探索代价
  - 碰撞代价基于 GPIS 预测语义
  - 探索代价利用 GPIS 不确定性引导


## Experiments

- **Peg-in-Hole（PyBullet，3 任务）**：
  - Peg-U: 73.3% vs TAMPC 60%, ablation 43.3%
  - Peg-T: 80% vs TAMPC 76.7%, ablation 80%
  - Peg-I: 86.7% vs TAMPC 63.3%
- **仿真线缆操控（MuJoCo，双臂 16-DOF）**：
  - COGIS: 83.3% vs TAMPC 50%, baseline 3.3%
  - 消融（无接触精化）: 56.7%，无视觉预处理: 66.7%，无后处理: 70%，无局部最小检测: 76.7%
- **真实线缆操控**：
  - COGIS: 10/10（avg 73.1 steps）vs TAMPC 2/10, ablation 10/10（avg 102.5 steps）
  - 接触精化减少表面伪影，缩短轨迹长度


## Limitations

1. 假设动力学误差由接触引起：非接触误差会产生虚假障碍物
2. GPIS 对核参数敏感，Matern 核可能不适合复杂几何
3. CMAwM 优化在大数据集上计算成本较高
4. 约束是任务特异的：一个任务的表面模型可能不适合另一个任务
5. 静态环境假设，不支持移动障碍物


## Key Takeaways

- 在部分可观测环境中，建模障碍物几何比直接适应动力学更高效（尤其在可变形物体高维空间）
- 动力学预测与实际状态差异是免费获取接触信息的有效途径
- 约束精化（CMAwM）是处理 GPIS 噪声数据的关键：不要求约束可微或凸
- 视觉预处理/后处理的双保险策略有效减少假阳性接触
- 不确定性驱动的探索帮助逃离局部最小

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[planning]]

## 相关研究者

- [[kumar|Kumar, Abhinav]]
- [[mitrano|Mitrano, Peter]]
- [[berenson|Berenson, Dmitry]]
