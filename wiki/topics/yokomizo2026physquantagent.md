---
title: "PhysQuantAgent: An inference pipeline of mass estimation for vision-language models"
tags: [manipulation, VLM, physical-reasoning, grasping]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对物体质量的估计能力，并构建了约 300 个带真实质量标注的 RGB-D 数据集 VisPhysQuant。"
authors: "Yokomizo, Hisayuki; Miyanishi, Taiki; Gang, Yan; Kurita, Shuhei; Inoue, Nakamasa et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "UUZUIH2N"
---
## 摘要

Vision-Language Models (VLMs) are increasingly applied to robotic perception and manipulation（操控）, yet their ability to infer physical properties required for manipulation（操控） remains limited. In particular, estimating the mass of real-world objects is essential for determining appropriate grasp force and ensuring safe interaction. However, current VLMs lack reliable mass reasoning capabilities, and most existing benchmarks do not explicitly evaluate physical quantity estimation under realistic sensing conditions. In this work, we propose PhysQuantAgent, a framework for real-world object mass estimation using VLMs, together with VisPhysQuant, a new benchmark dataset for evaluation. VisPhysQuant consists of RGB-D videos of real objects captured from multiple viewpoints, annotated with precise mass measurements. To improve estimation accuracy, we introduce three visual prompting methods that enhance the input image with object detection, scale estimation, and cross-sectional image generation to help the model comprehend the size and internal structure of the target object. Experiments show that visual prompting significantly improves mass estimation accuracy on real-world data, suggesting the efficacy of integrating spatial reasoning with VLM knowledge for physical inference.

## 中文简述

PhysQuantAgent 通过视觉提示（visual prompting）增强 VLM 对物体质量的估计能力，构建了 VisPhysQuant 数据集，并在 xArm7 上验证了抓取力调整。

**研究方向**: 机器人操控、视觉-语言模型、物理量推理、抓取力控制

## 关键贡献

1. **PhysQuantAgent 框架**：即插即用的推理管线，通过视觉提示（visual prompting）增强 VLM 的质量估计能力，无需 3D 重建
2. **VisPhysQuant 数据集**：约 300 个真实 RGB-D 视频样本，360 度视角覆盖，带精确质量标注（TANITA KJ-212，精度 ±0.3g），物体质量范围 0.001kg-5kg，中位数 0.08kg
3. **三种视觉提示模块**：目标检测（Grounding DINO）、尺度估计（RGB-D 深度 + 相机内参）、截面图像生成（Nano Banana Pro）
4. **自适应工具选择机制**：VLM 在 Stage 1 自动选择最适合目标物体的视觉提示工具
5. **真实机器人验证**：在 xArm7 上验证了质量估计→抓取力调整的完整闭环
## 结构化提取

- **Problem**: VLM 缺乏可靠的质量推理能力；现有基于重建的方法计算昂贵且误差大；缺少适合机器人抓取的小型物体质量数据集
- **Method**: PhysQuantAgent——即插即用的视觉提示推理管线，包含目标检测、尺度估计、截面图像生成三种提示模块，VLM 自适应选择并从原始+增强图像中估计质量
- **Tasks**: 物体质量估计（视觉输入→质量数值），机器人抓取力调整
- **Sensors**: RGB-D 相机（iPhone 16 Pro LiDAR，Record3D 应用）
- **Robot Setup**: xArm7 机械臂，夹爪力控制通过调节电流实现
- **Metrics**: Minimum Ratio Error (MnRE) = min(m/m̂, m̂/m)
- **Limitations**: 透明物体深度失效；截面图像幻觉；数据集规模小（~300 物体）；机器人验证仅为展示性
- **Evidence Notes**: 全文可获取。主实验 Figure 9 展示 MnRE 对比（图表为图像格式，具体数值需查原文）。消融 Table II 同为图像格式。帧数消融 Figure 10 显示 5-10 帧最优。机器人实验为定性展示。缺少定量误差统计表和显著性检验。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 获取，含方法、实验、消融、定性分析）
- Confidence: high
- Summary: 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对物体质量的估计能力，并构建了约 300 个带真实质量标注的 RGB-D 数据集 VisPhysQuant。


## Problem

VLM 在机器人操控中被广泛使用，但缺乏可靠的质量推理能力。操控中初始抓取力的设定依赖物体质量——力太小物体会滑落，太大会损坏物体。现有方法（如 NeRF2Physics、PUGS）依赖计算密集的 3D 重建管线来估计体积和密度，成本高且误差大（相对误差约 80-100%）。同时，现有数据集（如 ABO）主要包含家具尺度物体，缺少适合机器人抓取的小型物体的质量标注。


## Method

### 整体架构
PhysQuantAgent 是一个两阶段推理管线：

**Stage 1（工具选择）**：VLM 分析输入场景，从三种视觉提示工具中选择最适合当前目标物体的模块。

**Stage 2（质量估计）**：将原始图像和经选定的视觉提示增强后的图像一同输入 VLM，输出质量估计值。

### 三种视觉提示工具

**(a) Object Detection（目标检测）**：
- 使用 Grounding DINO 检测目标物体并生成 bounding box
- 目的：将 VLM 注意力集中在目标物体上，减少背景干扰
- 解决问题：VLM 可能将周围物体纳入质量估计

**(b) Scale Estimation（尺度估计）**：
- 利用 RGB-D 相机的深度数据和相机内参（针孔模型）计算物体的实际物理尺寸
- 分割目标物体后，估计水平和垂直范围，将度量长度作为尺度标注叠加到图像上
- 与 3DAxiesPrompts 不同，该方法自动生成尺度参考，无需手动标注
- 公式：基于针孔模型，从像素坐标和深度值计算度量距离

**(c) Cross-sectional Image（截面图像）**：
- 使用图像编辑模型（Nano Banana Pro）从多个方向生成物体截面视图
- 目的：揭示物体内部结构和材料分布，辅助密度感知推理
- 解决问题：外观相似但内部密度不同的物体（如实心 vs 空心）

### 任务定义
给定 N 个视角的 RGB-D 观测数据，VLM 预测物体质量 m̂：
- 损失函数：ℒ = |m - m̂|（绝对质量误差）
- 评估指标：Minimum Ratio Error（MnRE）= min(m/m̂, m̂/m)，对称且尺度无关

### 实现细节
- 从 15 秒 30fps 视频中每隔 30 帧采样，得到约 15 张图像
- 物体检测和长度估计使用 Grounded-Segment-Anything
- 截面图像生成使用 Gemini 3 Pro Image-preview（Nano Banana Pro）


## Experiments

### 实验设置
- **数据集**：VisPhysQuant（~300 个物体）
- **指标**：Minimum Ratio Error (MnRE)
- **VLM 模型**：Qwen3-VL-8B、Gemini 2.5 Pro、Gemini 3.1 Pro
- **Baseline**：NeRF2Physics（基于重建的方法）；PUGS 因性能较低被排除

### 主要结果
1. **VLM 超越重建方法**：现代 VLM 在无视觉提示的情况下已优于 NeRF2Physics，即使没有显式的体积估计
2. **视觉提示持续提升性能**：PhysQuantAgent 在所有测试 VLM 上一致提升 MnRE
3. **帧数消融**（Figure 10）：
   - 精度不随帧数单调增加
   - 5-10 帧时达到最佳性能
   - 帧数太少信息不足，太多引入冗余反而略微降低精度
   - PhysQuantAgent 仅需少量帧即可达到竞争力性能，而 NeRF2Physics 需约 30 张图像
4. **视觉提示消融**（Table II）：所有提示策略均优于无提示 baseline，空间/结构线索对 VLM 质量估计有帮助

### 定性分析
- **成功案例**：尺度估计帮助 VLM 推断物体大小和体积，显著提升质量预测准确性
- **失败案例**：
  - 透明物体（玻璃）：LiDAR 信号穿透透明物体导致深度值高估，尺度估计产生大误差
  - 截面图像生成：可能产生伪影或不存在的物体，导致质量高估

### 机器人应用
- 在 xArm7 机器人上验证
- 流程：录视频 → 估计质量 → 根据估计质量调整抓取电流 → 逐渐闭合夹爪直到接触检测
- NeRF2Physics 质量估计不准确 → 抓取力不足 → 抓取失败
- PhysQuantAgent 提供更可靠的质量估计 → 稳定抓取成功


## Limitations

1. **透明物体**：LiDAR 深度对透明物体失效，导致尺度估计大误差（作者建议可用 Depth Anything 等深度估计模型缓解）
2. **截面图像幻觉**：图像生成模型可能在不存在的位置生成物体，导致质量高估
3. **数据集规模**：VisPhysQuant 仅约 300 个物体，多样性有限
4. **材料推理受限**：VLM 对材料属性的推理依赖先验知识，对非常见材料可能不可靠
5. **质量范围**：虽然覆盖 0.001-5kg，但极端轻量或重量物体的性能未详细分析
6. **闭环验证有限**：机器人实验仅为展示性，未进行大规模系统性评估


## Key Takeaways

1. **视觉提示 > 重训练**：通过在输入图像上叠加结构化视觉线索，可以在不修改 VLM 参数的情况下显著提升物理推理能力，这对 DLO 操控中估计绳索刚度、柔性等属性有直接启发
2. **自适应工具选择**：让 VLM 自己判断需要哪种信息（尺度 vs 内部结构），比固定管线更灵活
3. **少量帧即可推理**：5-10 帧就够用，远低于重建方法需要的 30+ 帧，这对实时机器人应用非常关键
4. **VLM 的物理先验**：现代 VLM 已具备一定的物理量推理能力，只需正确的提示方式来激活，说明模型内部已有相关表征
5. **物理属性估计的新范式**：从"重建→计算"转向"视觉提示→直接推理"，避免昂贵的中间表示

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[physical-reasoning]]
- [[grasping]]
- [[deformable-linear-object]]

## 相关研究者

- [[yokomizo|Yokomizo, Hisayuki]]
- [[miyanishi-taiki|Miyanishi, Taiki]]
- [[kurita|Kurita, Shuhei]]
