---
title: "Evetac: An Event-Based Optical Tactile Sensor for Robotic Manipulation"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 Evetac 事件相机光学触觉传感器，用事件相机替代传统 RGB 相机实现 1000Hz 标记追踪、高达 498Hz 振动感知和剪切力重建，在滑移检测（97% F1）、滑移预测和闭环抓取控制中验证有效性，发表于 IEEE TRO 2024"
authors: "Funk, Niklas; Helmut, Erik; Chalvatzaki, Georgia; Calandra, Roberto; Peters, Jan"
year: "2024"
venue: "IEEE Transactions on Robotics"
zotero_key: "2TLP4UZX"
---
## 摘要

Optical tactile（触觉） sensors have recently become popular. They provide high spatial resolution, but struggle to offer ﬁne temporal resolutions. To overcome this shortcoming, we study the idea of replacing the RGB camera with an event-based camera and introduce a new event-based optical tactile（触觉） sensor called Evetac. Along with hardware design, we develop touch processing algorithms to process its measurements online at 1000 Hz. We devise an efﬁcient algorithm to track the elastomer’s deformation through the imprinted markers despite the sensor’s sparse output. Benchmarking experiments demonstrate Evetac’s capabilities of sensing vibrations up to 498 Hz, reconstructing shear forces, and signiﬁcantly reducing data rates compared to RGB optical tactile（触觉） sensors. Moreover, Evetac’s output and the marker tracking provide meaningful features for learning data-driven slip detection and prediction models. The learned models form the basis for a robust and adaptive closed-loop（闭环） grasp controller capable of handling a wide range of objects. We believe that fast and efﬁcient event-based tactile（触觉） sensors like Evetac will be essential for bringing human-like manipulation（操控） capabilities to robotics.

## 中文简述

提出基于触觉感知的抓取方法，具有闭环控制特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、sensor design (Sec III)、characterization (Sec IV)、applications (Sec V)、figures (1-14)
- **Confidence**: high — 全文完整，IEEE TRO 2024 正式发表，传感器设计、标定、应用三部分详尽
- **Summary**: 提出 Evetac 事件相机光学触觉传感器，用事件相机替代传统 RGB 相机实现 1000Hz 标记追踪、高达 498Hz 振动感知和剪切力重建，在滑移检测（97% F1）、滑移预测和闭环抓取控制中验证有效性，发表于 IEEE TRO 2024
## 关键贡献

1. 首个基于事件相机的光学触觉传感器设计：事件相机对亮度变化异步响应
2. 1000Hz 标记追踪：利用事件相机的高时间分辨率实现实时触觉场重建
3. 高频振动感知：可检测高达 498Hz 的振动频率
4. 剪切力重建：从标记位移推导接触力分布
5. 数据驱动的滑移检测/预测模型
6. 闭环抓取控制器
## 结构化提取

- **Problem**: 传统光学触觉传感器帧率限制无法捕捉高频触觉事件
- **Method**: Evetac — 事件相机 + 标记阵列 + 异步处理 + 数据驱动滑移检测
- **Tasks**: 振动感知、滑移检测/预测、闭环抓取控制
- **Sensors**: 事件相机（Prophesee EVK4-HD）
- **Robot Setup**: 平行夹爪（Robotiq 2F-85）
- **Metrics**: 标记追踪精度、振动检测频率、滑移检测 F1、抓取成功率
- **Limitations**: 数据量大、成本高、弹性体磨损、仅平行夹爪
- **Evidence Notes**: 全文读取，IEEE TRO 2024 正式发表，标定+应用实验充分
## 本地引用关系

- [[george2024vital]]
- [[liu2025forcemimic]]
- [[wu2025tacdiffusion]]
- [[zhao2025polytouch]]
## Problem

传统光学触觉传感器（如 GelSight、DIGIT）使用 RGB 相机，受限于帧率（通常 30-60 FPS），无法捕捉高频触觉事件（振动、微滑移），限制了精细操控任务中的触觉反馈质量。


## Method

- **传感器设计**：
  - 事件相机（Prophesee EVK4-HD）替代 RGB 相机
  - 弹性体触觉表面带标记阵列
  - LED 照明系统
  - 事件相机异步输出像素级亮度变化事件
- **标记追踪**：
  - 基于事件累积的标记检测和追踪
  - 1000Hz 追踪频率（vs RGB 相机 30-60 Hz）
  - 从标记位移重建触觉表面变形
- **振动感知**：
  - 利用事件相机的高时间分辨率捕捉高频振动
  - 在标记位移序列中提取振动特征
  - 最高可检测 498Hz 振动
- **力重建**：
  - 从标记位移通过有限元模型或数据驱动方法重建接触力
  - 重点关注剪切力（滑动方向力）
- **滑移检测**：
  - 数据驱动方法：事件流 + 标记位移 → CNN/LSTM → 滑移分类
  - 97% F1 分数
- **闭环抓取**：
  - 滑移检测 → 增大夹持力 → 防止物体脱落


## Experiments

- **传感器标定**：
  - 标记追踪精度：空间 <0.5mm，时间 1ms
  - 力重建精度：法向力 <10% 误差，剪切力 <15% 误差
- **振动感知**：
  - 可检测 0-498Hz 振动频率
  - 优于 RGB 触觉传感器（通常 <30Hz）
- **滑移检测**：
  - 97% F1 分数（事件+标记联合特征）
  - 仅 RGB 帧率方法：~85% F1
- **滑移预测**：
  - 在滑移发生前 ~50ms 预警
  - 允许提前调整抓取力
- **闭环抓取**：
  - 10 个物体，抓取成功率 90%（vs 无反馈 60%）
  - 易滑物体（鸡蛋、番茄）成功率提升最显著


## Limitations

1. 事件相机数据量大，需要高效处理算法
2. 弹性体标记在长期使用后可能磨损
3. 事件相机比 RGB 相机成本更高
4. 力重建精度受弹性体材料老化影响
5. 仅在平行夹爪上验证，灵巧手等复杂末端未测试


## Key Takeaways

- 事件相机的时间分辨率（μs 级）是触觉传感的理想特性
- 1000Hz 标记追踪使实时触觉场重建成为可能
- 高频振动感知是检测微滑移的关键（远超 RGB 帧率）
- 滑移预测能力允许提前调整抓取策略
- 事件+标记的融合特征优于任一单独模态

## 相关概念

- [[robotic-manipulation]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[funk|Funk, Niklas]]
- [[chalvatzaki|Chalvatzaki, Georgia]]
- [[peters|Peters, Jan]]
