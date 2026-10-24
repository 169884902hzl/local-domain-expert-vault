---
title: "RT-Affordance: Affordances are Versatile Intermediate Representations for Robot Manipulation"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 RT-Affordance（RT-A），用 affordance（末端执行器关键位姿）作为策略中间表示。层次化模型：VLA 先预测 affordance plan（gripper 开合时末端位姿序列），再以 affordance 图叠加条件化策略。在抓取（68% vs RT-2 28%）、非抓取操控（70% vs RT-2 3%）上大幅超越。~750 张低成本标注图像即可学习新任务，OOD 鲁棒性优于 10% 退化"
authors: "Nasiriany, Soroush; Kirmani, Sean; Ding, Tianli; Smith, Laura; Zhu, Yuke et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "SFAWZEVA"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-5)
- **Confidence**: high — 全文完整，ICRA 2025 论文（Google DeepMind），RT-1 机器人平台，5 抓取 + 6 操控任务，全面对比 RT-2/GC-RT-2，消融和 OOD 分析
- **Summary**: 提出 RT-Affordance（RT-A），用 affordance（末端执行器关键位姿）作为策略中间表示。层次化模型：VLA 先预测 affordance plan（gripper 开合时末端位姿序列），再以 affordance 图叠加条件化策略。在抓取（68% vs RT-2 28%）、非抓取操控（70% vs RT-2 3%）上大幅超越。~750 张低成本标注图像即可学习新任务，OOD 鲁棒性优于 10% 退化
## 关键贡献

1. Affordance 作为策略中间表示：末端执行器关键位姿序列（gripper 开/合时），表达力强且紧凑
2. 桥接机器人数据和 web 数据：affordance 推理需要语义+空间推理，与 VQA/检测等 web 任务天然对齐
3. 低成本新任务学习：仅 ~750 张标注图像（1h 收集+2h 标注），无需额外遥操作演示
4. 层次化 VLA 模型：PaLM-E 2 骨干，先预测 affordance 再条件化策略
## 结构化提取

- **Problem**: 策略中间表示的平衡 + 桥接 robot/web 数据
- **Method**: RT-Affordance — 层次 VLA + affordance plan + 低成本标注
- **Tasks**: 抓取（5 类新物体）+ 非抓取操控（6 任务）
- **Sensors**: 单目头戴相机（RT-1 平台）
- **Robot Setup**: Google RT-1 机器人 + PaLM-E 2 骨干
- **Metrics**: 任务成功率
- **Limitations**: 新运动泛化弱、需相机参数、仅内部平台
- **Evidence Notes**: 全文读取，Tables I-III 提供完整对比和消融
## 本地引用关系

- [[dey2025revla]]
- [[garcia2025generalizable]]
- [[liu2025kuda]]
- [[liu820enhancing]]
- [[tang2025uad]]
## Problem

现有策略中间表示各有局限：语言不够具体（缺乏空间指导）、目标图像过度指定（难学习+难提供）、轨迹草图缺乏方向信息。如何找到既表达力强又轻量的中间表示，同时能桥接机器人数据和网络数据？


## Method

- **Affordance 定义**：q = (e_t1, e_t2, ..., e_tn)，gripper 状态变化（开→合/合→开）时和轨迹终点的末端位姿
- **Affordance 条件化策略**：
  - 将 affordance 投影为 2D 手部轮廓叠加在图像上
  - 不同关键帧用不同颜色区分时序
  - 需要相机内外参（否则可用文本 token）
  - BC 训练 + web 数据共训练（同 RT-2）
- **Affordance 预测模型**：
  - VLA（PaLM-E 2 1B）微调
  - 训练数据：(1) 机器人轨迹提取的 affordance、(2) web 数据、(3) ~750 张低成本标注图像
  - 输出：2D 像素坐标的 affordance 文本
- **推理流程**：
  - 给定初始图像+语言→预测 affordance plan→叠加图像→策略生成动作
  - 可选重规划：固定或自适应间隔更新 affordance


## Experiments

- **抓取新物体**（5 类：dustpan/kettle/pot/box/headphones）：
  - RT-2: 28%，GC-RT-2: 24%
  - RT-A（Oracle Aff）: 76%，RT-A: 68%
  - RT-2 失败模式：抓 center 而非 handle、旋转不够
- **非抓取操控**（6 任务：place into receptacle/articulated manipulation）：
  - RT-2: 3%，RT-A: 70%，RT-A（Oracle）: 70%
- **OOD 鲁棒性**（5 抓取任务，数百测试图离线评估）：
  - In-distribution: 77%
  - OOD 新物体: 69%，新视角: 77%，新背景: 74%
  - OOD 退化不超过 10%
- **消融**：
  - 无增强数据: 24%（-53%），无 web 数据: 11%（-66%）
  - web 数据和增强数据对 affordance 预测都关键


## Limitations

1. 不具备完全新颖运动/技能的泛化能力
2. Affordance 投影依赖相机内外参
3. 仅在 Google 内部机器人验证
4. 预测 affordance 有时不够精确（pot 抓取）
5. 未探索组合不同策略表示


## Key Takeaways

- Affordance 是语言和动作之间的"恰到好处"的抽象：比语言更具体，比目标图像更紧凑
- 从 gripper 状态变化自动提取 affordance 是简洁有效的策略
- ~750 张标注图像即可学习新任务：远比遥操作高效
- Web 数据共训练对 affordance 预测至关重要（去除后下降 66%）
- 层次化 VLA 架构使语言→affordance→动作的流程自然且可解释

## 相关概念

- [[robotic-manipulation]]
- [[grasping]]

## 相关研究者

- [[nasiriany|Nasiriany, Soroush]]
- [[kirmani|Kirmani, Sean]]
- [[smith|Smith, Laura]]
