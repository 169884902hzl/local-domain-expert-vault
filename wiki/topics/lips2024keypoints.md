---
title: "Learning keypoints for robotic cloth manipulation using synthetic data"
tags: [manipulation, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出合成数据管线用于训练衣物关键点检测器。三阶段流程：程序化生成单层 mesh → Nvidia Flex 变形（模拟展开后状态）→ Blender Cycles 渲染。MaxViT+UNet 架构，sim-to-real mAP 64.3%，sim+real fine-tune 74.2%（vs real-only 59.8%）。发现多样性 > 保真度：单层 mesh + 随机材质优于 Cloth3D mesh。现实差距约 20pp mAP"
authors: "Lips, Thomas; Gusseme, Victor-Louis De; wyffels, Francis"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "NABEEH4S"
---
## 摘要

Assistive robots should be able to wash, fold or iron clothes. However, due to the variety, deformability and self-occlusions of clothes, creating robot systems for cloth manipulation（操控） is challenging. Synthetic data is a promising direction to improve generalization, but the sim-to-real（仿真到真实迁移） gap limits its effectiveness. To advance the use of synthetic data for cloth manipulation（操控） tasks such as robotic folding, we present a synthetic data pipeline to train keypoint detectors for almostflattened cloth items. To evaluate its performance, we have also collected a real-world dataset.

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、dataset (Sec III)、pipeline (Sec IV)、keypoint detection (Sec V)、experiments (Sec VI)、tables (I-V)、figures (1-5)
- **Confidence**: high — 全文完整，arXiv 2024 预印本（v2），aRTF 数据集（1896 张真实图像），3 种衣物类别，完整 mesh/材质消融
- **Summary**: 提出合成数据管线用于训练衣物关键点检测器。三阶段流程：程序化生成单层 mesh → Nvidia Flex 变形（模拟展开后状态）→ Blender Cycles 渲染。MaxViT+UNet 架构，sim-to-real mAP 64.3%，sim+real fine-tune 74.2%（vs real-only 59.8%）。发现多样性 > 保真度：单层 mesh + 随机材质优于 Cloth3D mesh。现实差距约 20pp mAP
## 关键贡献

1. 完整合成数据管线：mesh 生成 → 变形 → 渲染，用于 almost-flattened 衣物关键点检测
2. aRTF 数据集：1896 张真实图像 + 标注，覆盖 T-shirt/towel/shorts/boxershorts
3. 系统性比较不同 mesh 获取和材质生成方法，发现多样性 > 保真度
4. 量化 sim-to-real gap（~20pp mAP），指出提升保真度是未来方向
## 结构化提取

- **Problem**: almost-flattened 衣物关键点检测的合成数据训练
- **Method**: 三阶段管线 — 程序化 mesh + Nvidia Flex 变形 + Blender Cycles 渲染 → MaxViT+UNet
- **Tasks**: T-shirt/towel/shorts 关键点检测（用于折叠脚本）
- **Sensors**: RGB 相机（ZED2i / 智能手机）
- **Robot Setup**: 无机器人实验（纯感知），演示折叠脚本
- **Metrics**: mAP(2,4,8 pixel)、AKD（pixel）
- **Limitations**: 已知类别、sim-to-real gap、仅 almost-flattened
- **Evidence Notes**: 全文读取，Tables I-V 提供完整数据集统计和消融结果
## 本地引用关系

- [[do2025watch]]
- [[patel2025realtosimtoreal]]
- [[wu2025rlgsbridge]]
## Problem

衣物操控（折叠、熨烫）需要准确的状态估计，但衣物多样性、可变形性和自遮挡使关键点检测困难。真实数据标注成本高且覆盖不足。现有合成数据方法在衣物关键点检测的特定设置（almost-flattened 衣物）上缺乏系统性评估。


## Method

- **Mesh 生成**：
  - 2D 模板定义边界顶点，bezier 曲线连接
  - 参数随机化（骨架、曲线、圆角半径）
  - 三角化（边长 ≤ 1cm）+ UV map 自动生成
  - 语义位置顶点自动跟踪用于标注
- **变形（Nvidia Flex）**：
  - 随机朝向掉落 → 产生褶皱
  - 有时抓取点并旋转 → 产生折叠
  - 有时翻转 → 产生可见/不可见折叠
  - 物理参数随机化：弯曲刚度、拉伸刚度、摩擦、阻力
- **渲染（Blender Cycles）**：
  - PolyHaven 环境纹理（背景 + 光照）
  - 随机桌面材质 + 颜色
  - 干扰物体（Google Scanned Objects）
  - 相机位置球面帽随机化
  - Raycasting 判断关键点可见性（2-ring 邻域）
- **关键点检测**：
  - MaxViT nano 编码器 + UNet 解码器
  - 2D heatmap 回归（高斯 blob + BCE loss）
  - 3×3 局部极大值 + 阈值 0.01 提取关键点
  - 数据增强：随机裁剪、高斯模糊/噪声、颜色/对比度/亮度
- **对称性处理**：按 bounding box 角点排序关键点，处理旋转对称（towel）和前后对称（T-shirt/shorts）


## Experiments

- **主要结果（aRTF test split）**：
  - T-shirt：sim-to-real 58.2% mAP, sim+real 69.1%, real-only 54.4%
  - Towel：sim-to-real 83.2% mAP, sim+real 88.6%, real-only 74.4%
  - Shorts：sim-to-real 51.4% mAP, sim+real 64.9%, real-only 50.7%
  - All：sim-to-real 64.3% mAP, sim+real 74.2%, real-only 59.8%
- **AKD（pixel）**：sim+real 8.7（vs real-only 16.8, sim-only 18.1）
- **Sim-to-real gap**：sim-to-sim 82.1% vs sim-to-real 64.3%（~20pp gap）
- **Mesh 比较**：单层 mesh 54.3% > Cloth3D 43.4% > 单层未变形 53.8%
- **材质比较**：随机 PolyHaven 54.3% > cloth-tailored 49.0% > 纯色 35.1%
- **失败模式**：折叠区域混淆、拉链/口袋误判、语义位置不一致


## Limitations

1. 假设衣物类型已知，未处理分类问题
2. 粒子模拟器（Nvidia Flex）物理有限：mesh 分辨率与厚度/变形粒度耦合
3. Sim-to-real gap 仍然显著（~20pp mAP）
4. 仅处理 almost-flattened 状态，不处理严重褶皱
5. 生成管线需要工程调参（变形参数手动调整）


## Key Takeaways

- 多样性 > 保真度：单层 mesh + 随机材质优于更真实的 Cloth3D mesh，但这是局部最优
- Sim-to-real gap 主要来源是衣物资产保真度（缺少缝线、拉链、口袋等细节）
- Fine-tuning 是缩小 gap 的有效手段：sim+real 比 sim-only 提升 ~10pp
- 交互式感知（多次观测）可能比静态关键点检测更适合严重变形场景
- 未来方向：text-to-3D 生成模型用于自动化资产创建

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[lips|Lips, Thomas]]
