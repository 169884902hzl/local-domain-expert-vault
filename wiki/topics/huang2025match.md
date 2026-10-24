---
title: "MATCH POLICY: A simple pipeline from point cloud registration to manipulation policies"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 MATCH POLICY，将操控 pick-place 策略转化为点云配准任务。核心流程：存储演示中的组合点云 Pab（pick/place 配置），推理时通过 RANSAC + colored ICP 将当前观测点云配准到存储点云，从配准姿态计算 pick-place 动作。无需训练，具有 bi-equivariant place 和 equivariant pick 性质，1 条演示即可在 Phone-on-Base 达 93.3%，10 条演示达 100%。真实 UR5 机器人 6 个任务验证"
authors: "Huang, Haojie; Liu, Haotian; Wang, Dian; Walters, Robin; Platt, Robert"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "JJDYYTSI"
---
## 摘要

Many manipulation（操控） tasks require the robot to rearrange objects relative to one another. Such tasks can be described as a sequence of relative poses between parts of a set of rigid bodies. In this work, we propose MATCH POLICY, a simple but novel pipeline for solving high-precision pick and place tasks. Instead of predicting actions directly, our method registers the pick and place targets to the stored demonstrations. This transfers action inference into a point cloud（点云） registration task and enables us to realize nontrivial manipulation（操控） policies without any training. MATCH POLICY is designed to solve high-precision tasks with a key-frame setting. By leveraging the geometric interaction and the symmetries of the task, it achieves extremely high sample efficiency and generalizability to unseen configurations. We demonstrate its state-of-the-art（现有最优方法） performance across various tasks on RLbench benchmark compared with several strong baselines and test it on a real robot with six tasks. Videos and code are available on https://haojhuang.github.io/match page/.

## 中文简述

提出基于点云的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III-IV)、experiments (Sec V-VII)、tables (I-V)、figures (1-5)
- **Confidence**: high — 全文完整，arXiv 2025 预印本，6 个 RLBench 任务 + 6 个真实机器人任务系统评估，理论分析完备
- **Summary**: 提出 MATCH POLICY，将操控 pick-place 策略转化为点云配准任务。核心流程：存储演示中的组合点云 Pab（pick/place 配置），推理时通过 RANSAC + colored ICP 将当前观测点云配准到存储点云，从配准姿态计算 pick-place 动作。无需训练，具有 bi-equivariant place 和 equivariant pick 性质，1 条演示即可在 Phone-on-Base 达 93.3%，10 条演示达 100%。真实 UR5 机器人 6 个任务验证
## 关键贡献

1. 无训练管线：将操控策略转化为点云配准（RANSAC + colored ICP），演示收集后立即可用
2. 理论分析：证明 bi-equivariant place 和 equivariant pick 性质，解释极高样本效率
3. 1 demo 即可工作：Phone-on-Base 93.3%（1 demo）vs Imagination Policy 4%（1 demo）
4. 真实机器人验证：6 个真实任务，仅需 10 条演示
## 结构化提取

- **Problem**: 高精度 pick-place 任务需要大量训练或逐物体预训练
- **Method**: MATCH POLICY — RANSAC + colored ICP 点云配准 → pick-place 动作，无需训练
- **Tasks**: RLBench 6 任务 + Open-Microwave + Put-Item-in-Drawer + 真实 6 任务
- **Sensors**: 4×RGB-D 相机（仿真）/ 3×RealSense 455（真实）
- **Robot Setup**: RLBench 仿真（Franka）+ UR5 真实机器人
- **Metrics**: 成功率（25 test configs × 3 seeds）
- **Limitations**: 开环策略、需分割、已知物体、对称物体歧义
- **Evidence Notes**: 全文读取，Tables I-V 提供完整仿真/真实/消融结果
## 本地引用关系

- [[gao2025must]]
- [[garcia2025generalizable]]
- [[xie102multiview]]
## Problem

现有 pick-place 操控方法要么需要大量训练（PerAct、RVT、3D Diffuser Actor），要么需要逐物体预训练（NDFs），要么只能单步单任务（Tax-Pose、RPDiff）。高精度任务（如 Plug-Charger、Insert-Knife）仍具挑战性。


## Method

- **存储阶段**：
  - 对每个演示，构建组合点云 Pab = Ta·Pa ∪ Tb·Pb（pick/place 目标的配置）
  - 以语言描述为 key 存储 (l, Pab) 字典
  - 点云通过 mask 分割，下采样至 4mm 体素
- **推理阶段**：
  - 根据语言指令检索对应 Pab
  - RANSAC 初始对齐 → colored ICP 精细配准 → 获得 (T̂a, T̂b)
  - 多次随机种子运行，选择 fitness score 最高的配准结果
  - 计算动作：apick = (T̂b)⁻¹T̂a，aplace = (T̂a)⁻¹T̂b
- **等变性质**：
  - 不变性：Pab 变换 g 不改变预测动作（Prop 1）
  - Bi-equivariant place：物体独立变换 ga, gb，place 动作相应变换（Prop 2）
  - Equivariant pick：pick 目标变换 gb，pick 动作相应变换（Prop 3）


## Experiments

- **RLBench 6 任务（1 demo）**：
  - Phone-on-Base 93.3%，Stack-Wine 74.67%，Plug-Charger 34.67%，Insert-Knife 44%
  - vs Imagination Policy (1 demo): 4%, 2.67%, 0%, 0%
- **RLBench 6 任务（10 demos）**：
  - Phone-on-Base 100%，Stack-Wine 98.67%，Put-Plate 13.33%，Slide-Roll 7.24%，Plug-Charger 40%，Insert-Knife 61.33%
  - vs Imagination Policy: 90.67%, 97.33%, 34.67%, 23.61%, 26.67%, 42.67%
  - vs RPDiff: 62.67%, 32%, 5.33%, 0%, 0%, 2.67%
  - vs RVT: 56%, 18.67%, 53.33%, 0%, 0%, 8%
  - vs PerAct: 66.67%, 5.33%, 12%, 0%, 0%, 0%
- **关节物体**：Open-Microwave 32%（10 demos，expert 92%）
- **长时序**：Put-Item-in-Drawer 96%（10 demos，与 expert 持平）
- **真实机器人（6 任务）**：Putting-Banana 93.3%，Packing-Shoes 100%，Arranging-Letters 66.7%
- **相机设置**：低分辨率轻微下降，单视角显著下降但仍可用


## Limitations

1. 仅输出开环策略（key-frame），无法高频闭环控制
2. 需要物体分割（虽然 SOTA 分割方法可解决）
3. 假设物体已见过，不能泛化到全新物体
4. 对称物体（plate、roll）的 pick-place 姿态多样性导致部分失败
5. 传感器噪声影响配准精度（如 Hanging-Mug 46.2% place 成功率）


## Key Takeaways

- 点云配准是 pick-place 操控的天然框架，几何对应关系直接提供动作信号
- 无需训练意味着零调参成本，演示收集后立即部署
- Bi-equivariant 性质是实现 1-demo 学习的理论保证
- 组合点云表示（仅存储相关物体）比全局点云更鲁棒
- 对于高精度任务（Plug-Charger、Insert-Knife），配准方法优于学习方法
- 开环限制是该框架的主要瓶颈，长时序任务通过串行 pick-place 动作缓解

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]

## 相关研究者

- [[huang-haojie|Huang, Haojie]]
