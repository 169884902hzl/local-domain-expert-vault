---
title: "Incremental few-shot adaptation for non-prehensile object manipulation using parallelizable physics simulators"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于 MuJoCo 物理仿真器的增量式 few-shot 适应方法，通过 CEM 优化仿真参数使动力学模型与真实推物交互对齐，用于非抓取式物体推动的模型预测控制"
authors: "Baumeister, Fabian; Mack, Lukas; Stueckler, Joerg"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "FKG35VUK"
---
## 摘要

Few-shot（少样本） adaptation is an important capability for intelligent robots that perform tasks in open-world settings such as everyday environments or flexible production. In this paper, we propose a novel approach for non-prehensile manipulation（操控） which incrementally adapts a physics-based dynamics model for model-predictive control (MPC). The model prediction is aligned with a few examples of robot-object interactions collected with the MPC. This is achieved by using a parallelizable rigid-body physics simulation as dynamic world model and sampling-based optimization of the model parameters. In turn, the optimized dynamics model can be used for MPC using efficient sampling-based optimization. We evaluate our fewshot adaptation approach in object pushing experiments in simulation and with a real robot.

## 中文简述

提出基于学习方法的非抓取式操控方法，具有少样本学习特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV, 含仿真和真实机器人)、figures (Fig 1-6)、conclusion
- **Confidence**: high — 全文完整，方法描述详实，仿真和真实实验都有
- **Summary**: 提出基于 MuJoCo 物理仿真器的增量式 few-shot 适应方法，通过 CEM 优化仿真参数使动力学模型与真实推物交互对齐，用于非抓取式物体推动的模型预测控制
## 关键贡献

1. 提出增量式 few-shot 适应方法，使用可并行化刚体物理仿真（MuJoCo）作为动力学模型，CEM 优化仿真参数以对齐真实交互轨迹
2. 提出 minimum snap 轨迹关键点规划，降低 MPC 控制频率（从 1kHz 到 10Hz），实现实时控制
3. 在仿真和真实机器人上验证非抓取式推物任务
## 结构化提取

- **Problem**: 物理仿真参数难以精确标定，影响基于仿真的 MPC 性能
- **Method**: MuJoCo 作为动力学模型 + CEM 参数优化 + minimum snap 轨迹关键点 MPC
- **Tasks**: 非抓取式 2D 物体推动（推长方体到目标位姿）
- **Sensors**: MoCap（240Hz 位姿）+ 机器人关节编码器（1kHz 速度）
- **Robot Setup**: Franka Panda 7-DoF + 球形末端执行器，笛卡尔位置控制
- **Metrics**: 成功率、执行时间、轨迹损失、轨迹长度、参数估计误差
- **Limitations**: 仅推物任务、关节限制问题、接近最优初始化无改善
- **Evidence Notes**: 全文读取，Fig 2-6 提供定量结果，含仿真和真实实验
## 本地引用关系

- [[ozdamar820pushing]]
- [[patel2025realtosimtoreal]]
- [[wu2025imperfect]]
## Problem

机器人在开放世界中执行操控任务需要快速适应新物体和环境。基于物理仿真的 MPC 是有前景的方向，但仿真参数（摩擦、质量）难以精确标定。需要一种 few-shot 方法从少量真实交互中增量式优化仿真参数。


## Method

- **动力学模型**：MuJoCo 刚体物理仿真，机器人末端建模为球体，物体建模为长方体
- **MPC**：iCEM 采样优化关键点序列，minimum snap 轨迹插值实现平滑控制
- **参数优化**：replay buffer 存储交互轨迹，CEM 优化滑动/扭转/滚动摩擦和末端质量参数
- **增量学习**：每次任务执行后将轨迹加入 replay buffer，迭代优化参数


## Experiments

- **仿真**：MuJoCo 中推物任务，评估参数恢复精度（Δ=0.2 和 Δ=1.0）
- **真实机器人**：Franka Panda 7-DoF + 球形末端执行器 + MoCap，推长方体到目标位姿
- **关键结果**：
  - 仿真中滑动摩擦误差在首 episode 后大幅下降
  - 真实机器人上偏移初始化参数，6 episode 后执行时间降至约 1/3
  - 默认 MuJoCo 参数初始化下无显著改善趋势
  - 10 Hz MPC 重规划频率（i9 CPU）


## Limitations

1. 仅验证了简单的 2D 推物任务
2. 关节加速度/速度限制导致多次任务失败
3. 当初始化接近最优时无明显改善
4. 参数优化在 2 episode 后趋于波动


## Key Takeaways

- Real2Sim2Real 路线：不学习神经网络动力学，而是优化物理仿真参数，few-shot 即可生效
- Minimum snap 关键点规划是降低 MPC 控制频率的有效策略
- CEM + 可并行仿真 = 实时 MPC 可行
- 增量式 replay buffer 允许持续优化

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[baumeister|Baumeister, Fabian]]
