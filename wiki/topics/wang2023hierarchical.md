---
title: "Hierarchical visual policy learning for long-horizon robot manipulation in densely cluttered scenes"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 HCLM（Hierarchical policy for Cluttered-scene Long-horizon Manipulation），视觉层次化策略协调 push/pick/place 三种参数化原语解决密集杂乱场景的长时序操控。高层策略选择原语，三个 option 输出原语参数。训练：先 BC 训练 pick/place（two-stream Transporter），后 HRL 训练高层策略+push option（Dual-Level Action Network）。创新：SEQ（Spatially Extended Q-update）用各向异性高斯扩展 push Q 值更新；TSUS（Two-Stage Update Scheme）缓解 HRL 非平稳转移问题。ClutteredRavens 基准：6 任务成功率 77-97%，4 任务最短 episode length。泛化到 16 额外方块仍 70%"
authors: "Wang, Hecheng; Qi, Lizhe; Fang, Bin; Sun, Yunquan"
year: "2023"
venue: "arXiv Preprint"
zotero_key: "RVVGSE5K"
---
## 摘要

In this work, we focus on addressing the longhorizon manipulation（操控） tasks in densely cluttered scenes. Such tasks require policies to effectively manage severe occlusions among objects and continually produce actions based on visual observations. We propose a vision-based Hierarchical policy for Cluttered-scene Long-horizon（长时序） Manipulation（操控） (HCLM). It employs a high-level policy and three options to select and instantiate three parameterized action primitives: push, pick, and place. We first train the pick and place options by behavior cloning (BC). Subsequently, we use hierarchical reinforcement learning（强化学习） (HRL) to train the high-level policy and push option. During HRL, we propose a Spatially Extended Q-update (SEQ) to augment the updates for the push option and a TwoStage Update Scheme (TSUS) to alleviate the non-stationary transition problem in updating the high-level policy. We demonstrate that HCLM significantly outperforms baseline methods in terms of success rate and efficiency in diverse tasks. We also highlight our method’s ability to generalize to more cluttered environments with more additional blocks.


## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、强化学习

## 关键贡献

1. HCLM 层次化策略：高层策略 + push/pick/place 三种参数化原语 option
2. SEQ：各向异性高斯扩展 push Q 值更新，利用推动的方向性
3. TSUS：两阶段更新方案缓解 HRL 中非平稳转移问题
4. ClutteredRavens 基准：6 个杂乱场景操控任务，多样属性和复杂度
## 结构化提取

- **Problem**: 密集杂乱场景的长时序视觉操控
- **Method**: HCLM — 层次化策略（DLAN + Two-Stream Transporter）+ SEQ + TSUS + STP Reward
- **Tasks**: 6 个 ClutteredRavens 任务（insertion/placing/alignment/stacking/packing）
- **Sensors**: 正射 RGB-D 相机（仿真）
- **Robot Setup**: UR5e + suction gripper（PyBullet 仿真）
- **Metrics**: 成功率 + 平均 episode length
- **Limitations**: 仅仿真、固定 push 长度、suction gripper
- **Evidence Notes**: 全文读取，Tables II-IV 提供完整对比和消融
## 本地引用关系

- [[chen2025deformpam]]
- [[gao2025must]]
- [[hartz2024art]]
- [[karim2024davil]]
- [[wu2025discrete]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、methodology (Sec III-IV)、experiments (Sec V)、tables (I-IV)、figures (1-5)
- **Confidence**: high — 全文完整，arXiv 2023，Fudan University + Tsinghua University，UR5e + suction gripper，ClutteredRavens 基准 6 任务，PyBullet 仿真，97% 成功率（block-insertion），泛化到 16 额外方块保持 70%
- **Summary**: 提出 HCLM（Hierarchical policy for Cluttered-scene Long-horizon Manipulation），视觉层次化策略协调 push/pick/place 三种参数化原语解决密集杂乱场景的长时序操控。高层策略选择原语，三个 option 输出原语参数。训练：先 BC 训练 pick/place（two-stream Transporter），后 HRL 训练高层策略+push option（Dual-Level Action Network）。创新：SEQ（Spatially Extended Q-update）用各向异性高斯扩展 push Q 值更新；TSUS（Two-Stage Update Scheme）缓解 HRL 非平稳转移问题。ClutteredRavens 基准：6 任务成功率 77-97%，4 任务最短 episode length。泛化到 16 额外方块仍 70%


## Problem

密集杂乱场景中的长时序操控任务要求策略处理严重遮挡、持续产生视觉动作。现有方法要么假设无遮挡、要么需要物体位姿输入、要么使用隐式贪心策略选择原语，无法利用原语间协同效应。


## Method

- **观察/动作空间**：
  - 观察：正射 RGB-D 图像 (H×W×4)
  - 高层动作：{push, pick&place}
  - 低层动作：(x, y, θ) 像素位置+角度
- **Dual-Level Action Network (DLAN)**：
  - 双流处理 RGB + depth
  - Push 分支：旋转 k_push=12 角度 → 密集 Q 图
  - 高层分支：非旋转 → 2 个 Q 值（push/pick&place）
  - 共享编码器 + skip connection + late fusion
  - CLIP ResNet50 编码 RGB
- **Two-Stream Transporter**（pick/place）：
  - BC 训练，模仿 Transporter 但扩展为双流
  - k_pick=1, k_place=36 角度
  - 训练后冻结参数
- **SEQ（Spatially Extended Q-update）**：
  - 各向异性高斯滤波器：沿推动方向扩展 Q 值
  - 相邻角度降级因子 κ
  - 奖励判别因子 η：仅在当前子任务完成时考虑后续 Q 值
- **TSUS（Two-Stage Update Scheme）**：
  - 训练前期（epoch < τ）：仅用成功 push 经验更新高层
  - 训练后期（epoch ≥ τ）：所有非随机 push + 成功随机 push
- **STP Reward**：步进任务进展奖励，成功 push=0.75，成功 pick&place=1.0


## Experiments

- **ClutteredRavens 基准**（6 任务，基于 Ravens/PyBullet，UR5e + suction）：
  - Block-insertion: HCLM 97% vs P&P-only 54% vs RoManNet-demo 56%
  - Place-red-in-green: HCLM 97% vs P&P-only 42% vs RoManNet-demo 90%
  - Align-box-corner: HCLM 95% vs P&P-only 64% vs RoManNet-demo 89%
  - Stack-block-pyramid: HCLM 87% vs P&P-only 19% vs RoManNet-demo 24%
  - Block-stacking: HCLM 91% vs P&P-only 31% vs RoManNet-demo 31%
  - Packing-boxes: HCLM 77% vs P&P-only 43% vs RoManNet-demo 63%
- **泛化性**（stack-block-pyramid，增加额外方块）：
  - 6 blocks: 87%, 8: 83%, 10: 81%, 12: 76%, 14: 76%, 16: 70%
  - 基线在 6+ blocks 时急剧下降（RoManNet 0%）
- **消融**：
  - 无层次结构 → 0%（BC+RL 不一致的值输出导致隐式贪心失败）
  - 无 TSUS → 52%
  - 无 SEQ → 79%
  - 原始 Transporter → 71%


## Limitations

1. 仅在仿真（PyBullet）验证，未部署真实机器人
2. Push 原语假设 15cm 固定长度推动
3. 使用 suction gripper，未验证其他末端执行器
4. HRL 训练需要先 BC 训练 pick/place，流程较长
5. TSUS 阈值 τ 需手动设定


## Key Takeaways

- 层次化策略优于隐式贪心：显式高层规划能利用原语间协同
- BC+HRL 混合训练有效：先 BC 解决探索难题，后 HRL 联合优化
- Push 方向性信息可提升 Q 值更新：SEQ 的各向异性高斯
- 非平稳问题是 HRL 的关键瓶颈：TSUS 通过两阶段控制缓解
- Push+Pick+Place 三原语组合覆盖杂乱场景长时序任务

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wang|Wang, Hecheng]]
