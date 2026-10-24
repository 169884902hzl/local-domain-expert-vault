---
title: "A Black-Box Physics-Informed Estimator Based on Gaussian Process Regression for Robot Inverse Dynamics Identification"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagrangian 线性算子推导力矩 GP；(2) 证明能量的多项式结构并设计多项式核。在 7-DOF Franka 仿真中 nMSE < 10%（唯一方法），真实 MELFA 机器人上与精细调节的模型方法相当"
authors: "Giacomuzzo, Giulio; Carli, Ruggero; Romeres, Diego; Dalla Libera, Alberto"
year: "2024"
venue: "IEEE Transactions on Robotics"
zotero_key: "BVDZ7S2H"
---
## 摘要

Learning the inverse dynamics（逆动力学） of robots directly from data, adopting a black-box approach, is interesting for several real-world scenarios where limited knowledge about the system is available. In this article, we propose a black-box model based on Gaussian process（高斯过程） (GP) regression for the identiﬁcation of the inverse dynamics（逆动力学） of robotic manipulators. The proposed model relies on a novel multidimensional kernel, called Lagrangian Inspired Polynomial (LIP) kernel. The LIP kernel is based on two main ideas. First, instead of directly modeling the inverse dynamics（逆动力学） components, we model as GPs the kinetic and potential energy of the system. The GP prior on the inverse dynamics（逆动力学） components is derived from those on the energies by applying the properties of GPs under linear operators. Second, as regards the energy prior deﬁnition, we prove a polynomial structure of the kinetic and potential energy, and we derive a polynomial kernel that encodes this property. As a consequence, the proposed model allows also to estimate the kinetic and potential energy without requiring any label on these quantities. Results on simulation and on two real robotic manipulators, namely a 7 DOF Franka Emika Panda, and a 6 DOF MELFA RV4FL, show that the proposed model outperforms state-of-the-art（现有最优方法） black-box estimators based both on Gaussian processes and neural networks in terms of accuracy, generality, and data efﬁciency. The experiments on the MELFA robot also demonstrate that our approach achieves performance comparable to ﬁne-tuned model-based estimators, despite requiring less prior information. The code of the proposed model is publicly available.

## 中文简述

提出基于高斯过程的绳索操控方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、background (Sec II)、method (Sec III)、experiments (Sec V)、tables (I-III)、figures (1-9)
- **Confidence**: high — 全文完整，IEEE TRO 2024 正式发表，仿真 Franka Panda（3-7 DOF）+ 真实 Franka Panda + MELFA RV-4FL 系统评估
- **Summary**: 提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagrangian 线性算子推导力矩 GP；(2) 证明能量的多项式结构并设计多项式核。在 7-DOF Franka 仿真中 nMSE < 10%（唯一方法），真实 MELFA 机器人上与精细调节的模型方法相当
## 关键贡献

1. LIP 核：首个编码 Lagrangian 方程的多输出 GP 核，建模力矩间的物理关联
2. 能量先验：证明动能/势能的多项式结构，推导定制的多项式核
3. 能量估计：从力矩观测估计动能和势能（无标签），可集成能量控制策略
4. 广泛验证：仿真 + 两个真实机器人（Franka Panda + MELFA RV-4FL）
## 结构化提取

- **Problem**: 机器人逆动力学黑盒辨识的数据效率和泛化问题
- **Method**: LIP 核 — Lagrangian 感知的多项式 GP 核
- **Tasks**: 逆动力学辨识、轨迹跟踪控制
- **Sensors**: 关节编码器 + 力矩传感器
- **Robot Setup**: Franka Panda（7-DOF）+ MELFA RV-4FL（6-DOF）
- **Metrics**: nMSE（归一化均方误差）
- **Limitations**: 计算复杂度、无正定性保证、DOF 扩展性
- **Evidence Notes**: 全文读取，IEEE TRO 2024，仿真+双真实机器人验证
## 本地引用关系

- [[chen2025coordinated]]
## Problem

机器人逆动力学的纯黑盒学习方法（NN/GP）数据效率低、泛化能力差。现有方法忽略力矩分量间的 Lagrangian 物理关联，限制了性能上限。


## Method

- **核心思想**：
  - T(q,q̇) 和 V(q) 建模为独立 GP（零均值，多项式核 kT, kV）
  - Lagrangian L = T - V 也是 GP，核为 kL = kT + kV
  - 力矩 τ = GL（线性算子），τ 的核通过线性算子性质推导
- **势能核 kV**：乘积形式，每个关节一个一阶多项式核（revolute 用 [cos(q), sin(q)]，prismatic 用 q）
- **动能核 kT**：求和形式（每连杆一个），每连杆包含齐次多项式核（速度）× 二阶多项式核（关节角）
- **训练**：GP 超参数通过边际似然最大化优化
- **能量估计**：利用 τ 和 T/V 的联合高斯分布，条件后验直接计算


## Experiments

- **仿真 Franka（泛化）**：
  - 6-DOF：LIP 中位 nMSE ~3%（vs GIP ~8%、SE ~15%、DeLan ~10%）
  - 7-DOF：LIP 是唯一保持 nMSE <10% 的方法
  - 能量估计：动能 nMSE ~1%，势能 nMSE <0.01%
- **数据效率**：50 样本即可接近最优（vs SE/GIP 需 300+）
- **真实 Franka**：LIP 在所有关节上 nMSE 最低
- **真实 MELFA**：LIP 与精细模型方法（ID/SP）相当，无需物理模型先验
- **轨迹跟踪**：CT 控制器 + LIP 前馈，跟踪误差显著低于名义模型


## Limitations

1. GP 训练计算复杂度 O(N³)，大数据集受限
2. 不保证惯性矩阵正定性
3. 机器人 DOF 增加时超参数优化变难
4. 仅验证逆动力学辨识，未在闭环控制中大规模验证
5. DeLan 在 7-DOF 上性能差但用了 10× 数据


## Key Takeaways

- 编码 Lagrangian 物理结构是提升黑盒逆动力学辨识的关键
- 多项式核比通用核（SE）更适合逆动力学的有限维函数空间
- 多输出 GP（建模力矩间关联）比独立单输出 GP 泛化更好
- 黑盒方法可在真实工业机器人上达到模型方法的精度
- 从力矩测量估计能量是 GP 框架的有价值副产品

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]

## 相关研究者

- [[giacomuzzo|Giacomuzzo, Giulio]]
