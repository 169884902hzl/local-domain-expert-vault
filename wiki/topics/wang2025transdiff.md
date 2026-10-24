---
title: "TransDiff: Diffusion-Based Method for Manipulating Transparent Objects Using a Single RGB-D Image"
tags: [diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 TransDiff，基于扩散模型（DDPM）的透明物体深度补全方法，用于机器人抓取透明物体。核心设计：多条件引导扩散——以 RGB 图像为输入，利用语义分割、边缘检测和法线估计作为条件信息指导深度扩散去噪。创新：(1) 多条件编码器融合语义/边缘/法线信息；(2) RVCDB（Relative Depth Consistency Distance-based Boundary）损失保持深度边界一致性；(3) 训练数据集 TranCG。ClearGrasp 数据集 RMSE 0.032，TranCG RMSE 0.028。仿真抓取成功率 87.5%，Franka Panda 真实机器人验证"
authors: "Wang, Haoxiao; Zhou, Kaichen; Gu, Binrui; Feng, Zhiyuan; Wang, Weijie et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "Y6D2TSRT"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 扩散模型

## 关键贡献

1. 首次将扩散模型（DDPM）应用于透明物体深度补全
2. 多条件引导：语义分割+边缘检测+法线估计作为条件信息
3. RVCDB 损失：基于相对深度一致性的边界感知损失
4. TranCG 数据集：大规模透明物体深度数据集
## 结构化提取

- **Problem**: 透明物体深度感知缺失导致机器人抓取困难
- **Method**: TransDiff — DDPM + 多条件引导（语义/边缘/法线）+ RVCDB 损失
- **Tasks**: 透明物体深度补全 + 基于补全深度的抓取
- **Sensors**: RGB-D 相机（RealSense）
- **Robot Setup**: Franka Emika Panda + Parallel Gripper
- **Metrics**: RMSE/MAbs（深度）+ 抓取成功率（仿真 87.5%）
- **Limitations**: 推理慢、合成数据依赖、仅抓取验证
- **Evidence Notes**: 全文读取，Tables 提供完整深度补全对比，仿真+真实抓取验证
## 本地引用关系

- [[li2025routing]]
- [[scheikl620movement]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、figures (1-8)
- **Confidence**: high — 全文完整，ICRA 2025，Peking University，DDPM 扩散模型用于透明物体深度补全，语义/边缘/法线多条件引导，RVCDB 损失（Relative Depth Consistency），ClearGrasp RMSE 0.032，TranCG RMSE 0.028，仿真抓取成功率 87.5%，Franka Panda 真实验证
- **Summary**: 提出 TransDiff，基于扩散模型（DDPM）的透明物体深度补全方法，用于机器人抓取透明物体。核心设计：多条件引导扩散——以 RGB 图像为输入，利用语义分割、边缘检测和法线估计作为条件信息指导深度扩散去噪。创新：(1) 多条件编码器融合语义/边缘/法线信息；(2) RVCDB（Relative Depth Consistency Distance-based Boundary）损失保持深度边界一致性；(3) 训练数据集 TranCG。ClearGrasp 数据集 RMSE 0.032，TranCG RMSE 0.028。仿真抓取成功率 87.5%，Franka Panda 真实机器人验证


## Problem

透明物体（玻璃杯、塑料容器）的深度感知是机器人操控的关键挑战。RGB-D 相机因透明材质的光学特性（反射、折射）无法获取准确深度。现有方法（如 ClearGrasp）依赖优化或网络回归，深度补全质量有限。


## Method

- **输入/输出**：
  - 输入：单张 RGB 图像（来自 RGB-D 相机）
  - 输出：完整深度图（补全透明区域的缺失/错误深度）
- **多条件编码**：
  - 语义分割：识别透明物体区域
  - 边缘检测：定位深度不连续边界
  - 法线估计：提供表面朝向信息
  - 三者融合作为 DDPM 的条件输入
- **DDPM 扩散框架**：
  - 前向过程：对深度图添加高斯噪声
  - 反向过程：UNet 去噪，条件引导为多条件编码
  - T 步迭代去噪生成完整深度图
- **RVCDB 损失**：
  - 相对深度一致性：保持相邻区域的深度比例关系
  - 基于距离的边界感知：在深度边界处增强损失权重
  - 与标准 L1/L2 损失互补
- **TranCG 数据集**：
  - 大规模合成透明物体深度数据
  - 多种透明物体类别和材质
  - 用于训练和评估


## Experiments

- **深度补全对比**：
  - ClearGrasp 数据集：TransDiff RMSE 0.032 vs ClearGrasp 0.045 vs NLSPN 0.041
  - TranCG 数据集：TransDiff RMSE 0.028 vs 其他方法 >0.035
  - 多条件引导优于单条件，三条件组合最优
- **消融**：
  - 去除语义条件：RMSE +0.008
  - 去除边缘条件：RMSE +0.005
  - 去除 RVCDB 损失：RMSE +0.006
- **抓取实验**：
  - 仿真（PyBullet）：透明物体抓取成功率 87.5%
  - 基于补全深度的抓取规划显著优于原始深度
  - Franka Panda 真实机器人验证


## Limitations

1. DDPM 推理速度较慢（多步去噪），实时性受限
2. 训练依赖合成数据，真实透明物体多样性不足
3. 仅验证了抓取任务，未扩展到更复杂操控（如倒水、放置）
4. 多条件模块（语义/边缘/法线）需额外预训练
5. 高度折射或镜面反射物体仍具挑战


## Key Takeaways

- 扩散模型适合透明物体深度补全：生成式模型处理不确定深度区域优于回归模型
- 多条件引导是关键：语义+边缘+法线三者互补
- RVCDB 损失提升边界质量：相对深度一致性对操控任务特别重要
- TranCG 数据集填补了透明物体深度数据的空白
- 深度补全质量直接影响抓取成功率：87.5% vs 基线显著提升

## 相关概念

- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[wang-haoxiao|Wang, Haoxiao]]
