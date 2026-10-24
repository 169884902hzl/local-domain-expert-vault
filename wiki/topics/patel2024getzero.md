---
title: "GET-zero: Graph embodiment transformer for zero-shot embodiment generalization"
tags: [imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 GET-Zero，Graph Embodiment Transformer 通过图注意力偏置实现零样本具身泛化。每个关节作为独立 token，空间编码（SPD）+ 父子编码（有向）作为注意力偏置。44 个 LEAP Hand 配置 RL 专家策略 → BC 蒸馏到单一 GET 模型。自建模 FK 损失提升泛化。新图结构零样本 16% 提升，新几何 10%，两者兼具 20%。仿真达到专家 99% 性能，真实 LEAP Hand 验证零样本操控"
authors: "Patel, Austin; Song, Shuran"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "B327T7AJ"
---
## 摘要

This paper introduces GET-Zero, a model architecture and training procedure for learning an embodimentaware control policy that can immediately adapt to new hardware changes without retraining. To do so, we present Graph Embodiment（具身） Transformer (GET), a transformer model that leverages the embodiment（具身） graph connectivity as a learned structural bias in the attention mechanism. We use behavior cloning to distill demonstration（示范数据） data from embodiment（具身）-specific expert policies into an embodiment（具身）-aware GET model that conditions on the hardware configuration of the robot to make control decisions. We conduct a case study on a dexterous（灵巧） inhand object rotation task using different configurations of a four-fingered robot hand with joints removed and with link length extensions. Using the GET model along with a selfmodeling loss enables GET-Zero to zero-shot（零样本） generalize to unseen variation in graph structure and link length, yielding a 20% improvement over baseline methods. All code and qualitative video results are on our project website.

## 中文简述

提出基于Transformer的灵巧手方法，具有零样本泛化特点。

**研究方向**: 模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、case study (Sec IV)、experiments (Sec V)、tables (I-III)、figures (1-5)
- **Confidence**: high — 全文完整，arXiv 2024 预印本（v2），Stanford University，LEAP Hand 44 训练配置+10 零样本配置+真实部署，全面对比 ET/MetaMorph/Amorpheus 基线
- **Summary**: 提出 GET-Zero，Graph Embodiment Transformer 通过图注意力偏置实现零样本具身泛化。每个关节作为独立 token，空间编码（SPD）+ 父子编码（有向）作为注意力偏置。44 个 LEAP Hand 配置 RL 专家策略 → BC 蒸馏到单一 GET 模型。自建模 FK 损失提升泛化。新图结构零样本 16% 提升，新几何 10%，两者兼具 20%。仿真达到专家 99% 性能，真实 LEAP Hand 验证零样本操控
## 关键贡献

1. Graph Embodiment Transformer (GET)：图连接性作为注意力偏置（空间+父子编码）
2. 具身感知蒸馏框架：独立训练 RL 专家 → BC 蒸馏到单一模型，简化数据生成
3. 自建模 FK 损失：预测关节 3D 位置，与图编码协同提升泛化
4. 零样本图+几何泛化：比最佳基线提升 20%
## 结构化提取

- **Problem**: 零样本具身泛化到图结构和几何变化
- **Method**: GET — 图注意力偏置（SPD+父子编码）+ 自建模 FK 损失 + BC 蒸馏
- **Tasks**: 灵巧手物体旋转（yaw 轴 2π）
- **Sensors**: 关节本体感觉（角度/速度/PD目标）+ URDF 几何信息
- **Robot Setup**: LEAP Hand（44 训练配置 + 10 零样本配置），仿真 IsaacGym + 真实
- **Metrics**: 平均旋转角速度（°/s）
- **Limitations**: 单任务、不跨手模型、需大量演示数据
- **Evidence Notes**: 全文读取，Tables I-III 提供完整对比和消融
## 本地引用关系

- [[chen2025vividex]]
- [[gao2025must]]
- [[han2025upvital]]
- [[luo2024humanagent]]
## Problem

机器人硬件修改（关节移除、连杆延长）通常需要重新训练策略。现有具身感知方法或忽略图连接性（纯注意力），或图表示不完整（DFS 线性化），无法泛化到图结构变化（如手指数量/关节数改变）。如何设计能零样本泛化到新图结构和几何变化的策略架构？


## Method

- **具身 Token 化**：
  - 每个 token = [全局可变观测, 全局固定观测, 局部可变观测, 局部固定观测]
  - 可变局部：关节角度/速度 + PD 目标
  - 固定局部：URDF 中关节 3D 位置和相对父关节旋转
  - 可变全局：正弦相位编码（旋转周期 2s）
- **图注意力偏置**：
  - 空间编码：SPD（最短路径距离）→ 学习标量偏置 s_φ(i,j)
  - 父子编码：有向距离 → 偏置 p 和 c（区分 parent→child 和 child→parent）
  - 注意力矩阵：A_ij = QK^T/√d + s + p + c（不变于 token 排列顺序）
- **自建模头**：预测每关节在机器人局部坐标系的 3D 位置（FK），L2 监督
- **训练流程**：
  - 1. 程序化生成 236 种 LEAP Hand 配置（移除关节/连杆+延长连杆）
  - 2. 每配置用 PPO (IsaacGym) 训练 RL 专家（灵巧手旋转任务）
  - 3. 筛选 44 个能在 30s 完成旋转的配置
  - 4. 收集每配置 7 小时演示数据 → BC 训练 GET


## Experiments

- **仿真实验**（44 训练配置 + 10 零样本配置 × 5 seeds）：
  - 训练图：GET-Zero 16.32°/s（RL 专家 16.50°/s，达 99%）
  - 新图：GET-Zero 10.07°/s（ET 8.68，ET+DFS 6.45）→ +16%
  - 新几何：GET-Zero 15.80°/s（ET 12.92，ET+DFS 14.37）→ +10%
  - 新图+新几何：GET-Zero 9.75°/s（ET 8.12，ET+DFS 6.27）→ +20%
- **消融**：
  - 自建模 + 图编码 → 最佳组合
  - 自建模无图编码 → 反而降低 4.6%（FK 需要图信息）
  - DFS 线性化 → 图变化时下降 26%（排列敏感）
  - 空间编码贡献 > 父子编码
- **FK 预测**：GET-Zero 0.82mm vs ET 7.97mm vs ET+DFS 9.03mm
- **真实实验**（LEAP Hand + AR 标记追踪）：
  - 训练配置：GET-Zero 20.5°/s（70% sim 比率）
  - 零样本新图：8.3°/s，新几何：21.8°/s
  - ET 基线在所有配置上显著差于 GET-Zero


## Limitations

1. 不太可能零样本迁移到全新机械手模型
2. 最多编码 16 个关节，未编码关节极限/电机强度/摩擦
3. 仅验证单任务（灵巧手旋转）
4. BC 蒸馏需要大量演示数据（每配置 7 小时）


## Key Takeaways

- 图注意力偏置是具身泛化的关键：排列不变的图编码优于 DFS 线性化
- 自建模损失与图编码协同：无图编码时自建模反而有害
- BC 蒸馏比联合 RL 更简单：独立训练专家 → 联合蒸馏
- 空间编码比父子编码更重要：相邻关节的通信最关键
- 少量训练配置即可合理泛化：10 个配置即可达到可接受的零样本性能

## 相关概念

- [[imitation-learning]]
- [[grasping]]

## 相关研究者

- [[patel|Patel, Austin]]
