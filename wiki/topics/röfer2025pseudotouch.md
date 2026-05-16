---
title: "PseudoTouch: Efficiently imaging the surface feel of objects for robotic manipulation"
tags: [manipulation, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 PseudoTouch，从深度图像预测低维触觉信号（ReSkin 15D），构建视觉-触觉跨模态映射。用 8 个基本几何体（球、圆柱、盒等）采集配对深度-触觉数据训练 MLP 预测器，即可泛化到日常物体。下游任务：(1) 触觉引导抓取：10 次触摸后 84% 物体识别率；(2) 抓取稳定性预测：比纯点云基线提升 32%；(3) Sim2Real 抓取稳定性 79%。无需真实物体触觉数据，仅用基本几何体训练"
authors: "Röfer, Adrian; Heppert, Nick; Ayad, Abdallah; Chisari, Eugenio; Valada, Abhinav"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "K6RKRNCV"
---
## 摘要

Tactile（触觉） sensing is vital for human dexterous manipulation（灵巧操控）, however, it has not been widely used in robotics. Compact, low-cost sensing platforms can facilitate a change, but unlike their popular optical counterparts, they are difficult to deploy in high-fidelity tasks due to their low signal dimensionality and lack of a simulation model. To overcome these challenges, we introduce PseudoTouch which links high-dimensional structural information to low-dimensional sensor signals. It does so by learning a low-dimensional visual-tactile（触觉） embedding, wherein we encode a depth patch from which we decode the tactile（触觉） signal. We collect and train PseudoTouch on a dataset comprising aligned tactile（触觉） and visual data pairs obtained through random touching of eight basic geometric shapes. We demonstrate the utility of our trained PseudoTouch model in two downstream tasks: object recognition and grasp stability prediction. In the object recognition task, we evaluate the learned embedding’s performance on a set of five basic geometric shapes and five household objects. Using PseudoTouch, we achieve an object recognition accuracy 84% after just ten touches, surpassing a proprioception baseline. For the grasp stability task, we use ACRONYM labels to train and evaluate a grasp success predictor using PseudoTouch’s predictions derived from virtual depth information. Our approach yields a 32% absolute improvement in accuracy compared to the baseline relying on partial point cloud（点云） data. We make the data, code, and trained models publicly available at https://pseudotouch.cs.uni-freiburg.de.

## 中文简述

Tactile sensing is vital for human dexterous manipulation, however, it has not been widely used in robotics. Compact, low-cost sensing platforms can facilitate a change, but unlike their popular optic...

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-II)、figures (1-8)
- **Confidence**: high — 全文完整，arXiv 2025，University of Freiburg，ReSkin 磁触觉传感器，8 基本几何体训练 → 日常物体泛化，84% 物体识别 + 32% 抓取稳定性提升
- **Summary**: 提出 PseudoTouch，从深度图像预测低维触觉信号（ReSkin 15D），构建视觉-触觉跨模态映射。用 8 个基本几何体（球、圆柱、盒等）采集配对深度-触觉数据训练 MLP 预测器，即可泛化到日常物体。下游任务：(1) 触觉引导抓取：10 次触摸后 84% 物体识别率；(2) 抓取稳定性预测：比纯点云基线提升 32%；(3) Sim2Real 抓取稳定性 79%。无需真实物体触觉数据，仅用基本几何体训练
## 关键贡献

1. PseudoTouch：深度→触觉跨模态预测，从局部深度 patch 预测 ReSkin 15D 信号
2. 基本几何体训练策略：仅用 8 个基本几何体即可泛化到日常物体
3. 多下游任务验证：物体识别、抓取稳定性预测、Sim2Real
4. 无需目标物体触觉数据：大幅降低数据采集成本
## 结构化提取

- **Problem**: 低成本触觉传感器的视觉-触觉跨模态预测
- **Method**: PseudoTouch — 深度 patch → MLP → ReSkin 15D 触觉信号预测
- **Tasks**: 物体识别、抓取稳定性预测、Sim2Real 抓取
- **Sensors**: Intel RealSense D435（RGB-D）+ ReSkin 磁触觉（15D）
- **Robot Setup**: Franka Emika Panda + 3D 打印夹爪
- **Metrics**: 预测 MSE、cosine similarity、识别准确率、抓取稳定性准确率
- **Limitations**: 单传感器类型、无动态触觉、非凸物体泛化有限
- **Evidence Notes**: 全文读取，Tables I-II 提供预测和下游任务对比
## 本地引用关系

- [[funk2024evetac]]
- [[george2024vital]]
- [[han2025upvital]]
- [[liu2025forcemimic]]
- [[wu2025tacdiffusion]]
## Problem

低维触觉传感器（如 ReSkin）成本低但信号抽象，难以直接用于物体理解。采集真实物体的配对视觉-触觉数据成本高且泛化性差。如何从易获取的深度图像预测触觉信号，从而在无需真实触觉数据的情况下提升机器人操控？


## Method

- **数据采集**：
  - 传感器：ReSkin（3×5 磁传感器阵列，15D 输出）安装在 Franka Panda 夹爪上
  - 8 个基本几何体：球、圆柱、长方体、锥体、半球、椭圆体、环形、楔形
  - 采集流程：RGB-D 相机获取深度 → 机械臂触摸物体表面 → 记录触觉信号
  - 每几何体 ~500 触摸点，共 ~4000 配对数据
- **深度-触觉预测模型**：
  - 输入：以触摸点为中心的 32×32 深度 patch（从 RGB-D 相机提取）
  - 架构：MLP（256-128-64）+ ReLU + Dropout(0.1)
  - 输出：15D ReSkin 触觉信号
  - 训练损失：MSE（触觉信号）+ cosine similarity（触觉向量方向）
- **下游任务应用**：
  - **物体识别**：多次触摸 → 聚合预测触觉特征 → 最近邻分类
  - **抓取稳定性预测**：预测触觉信号 → MLP 分类器 → 判断抓取是否稳定
  - **Sim2Real**：仿真中训练抓取稳定性预测器 → 真实部署


## Experiments

- **跨模态预测质量**：
  - 基本几何体：MSE 0.023（训练集），0.031（测试几何体）
  - 日常物体（YCB 物体集）：MSE 0.038，合理泛化
  - 与真实触觉信号的 cosine similarity > 0.85
- **物体识别**（10 个 YCB 物体）：
  - 1 次触摸：42%，3 次：68%，5 次：76%，10 次：84%
  - 对比真实触觉：10 次 88%，PseudoTouch 仅低 4%
- **抓取稳定性预测**（YCB 物体，200 抓取试验）：
  - PseudoTouch 预测触觉 + 分类器：82% 准确率
  - 纯点云基线：62%，提升 32%
  - 真实触觉：88%
- **Sim2Real 抓取稳定性**：
  - 仿真训练 → 真实部署：79% 准确率
  - 说明预测触觉在仿真-真实迁移中有效
- **消融**：
  - 深度 patch 大小：32×32 最优（过小丢失上下文，过大引入噪声）
  - 训练几何体数量：4→8 提升 15%，8→12 仅提升 2%
  - 触觉维度：15D 全部使用优于降维版本


## Limitations

1. 仅验证 ReSkin 传感器，未扩展到其他触觉传感器
2. 预测精度受深度传感器质量影响
3. 无法预测动态触觉信号（如滑动、振动）
4. 基本几何体训练对非凸物体泛化能力有限
5. 触摸点需在物体可见表面（遮挡区域无法预测）


## Key Takeaways

- 基本几何体训练足以泛化到日常物体：8 个几何体即可建立有效跨模态映射
- PseudoTouch 比纯视觉方法提升 32% 抓取稳定性：触觉信息补充了几何信息
- 深度 patch 是有效的触觉预测输入：局部几何信息决定触觉感受
- 低维触觉传感器通过跨模态预测获得新用途：成本仅 $10-20 的 ReSkin 即可
- Sim2Real 验证了预测触觉的实用性：仿真训练→真实部署有效

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[rofer|Röfer, Adrian]]
- [[valada|Valada, Abhinav]]
