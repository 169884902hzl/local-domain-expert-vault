---
title: "Active vision might be all you need: Exploring active vision in bimanual robotic manipulation"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 AV-ALOHA 系统，在 ALOHA 2 基础上增加 7-DoF AV 臂搭载立体相机，通过 VR 头显控制相机视角，实现沉浸式遥操作，实验证明 active vision 在遮挡/精度任务（Group 2）上显著优于固定相机，但在简单任务（Group 1）上可能因动作空间增大而降低性能"
authors: "Chuang, Ian; Lee, Andrew; Gao, Dechen; Naddaf-Sh, M.-Mahdi; Soltani, Iman"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "4DUED9V3"
---
## 摘要

Imitation learning（模仿学习） has demonstrated significant potential in performing high-precision manipulation（操控） tasks using visual feedback. However, it is common practice in imitation learning（模仿学习） for cameras to be fixed in place, resulting in issues like occlusion and limited field of view. Furthermore, cameras are often placed in broad, general locations, without an effective viewpoint specific to the robot's task. In this work, we investigate the utility of active vision (AV) for imitation learning（模仿学习） and manipulation（操控）, in which, in addition to the manipulation（操控） policy, the robot learns an AV policy from human demonstrations to dynamically change the robot's camera viewpoint to obtain better information about its environment and the given task. We introduce AV-ALOHA, a new bimanual（双臂） teleoperation robot system with AV, an extension of the ALOHA 2 robot system, incorporating an additional 7-DoF robot arm that only carries a stereo camera and is solely tasked with finding the best viewpoint. This camera streams stereo video to an operator wearing a virtual reality (VR) headset, allowing the operator to control the camera pose using head and body movements. The system provides an immersive teleoperation experience, with bimanual（双臂） first-person control, enabling the operator to dynamically explore and search the scene and simultaneously interact with the environment. We conduct imitation learning（模仿学习） experiments of our system both in real-world and in simulation, across a variety of tasks that emphasize viewpoint planning. Our results demonstrate the effectiveness of human-guided AV for imitation learning（模仿学习）, showing significant improvements over fixed cameras in tasks with limited visibility. Project website: https://soltanilara.github.io/av-aloha/

## 中文简述

提出基于模仿学习的双臂方法。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、system description (Sec III)、experiments (Sec IV-V)、table (I)、figures (1-3)
- **Confidence**: high — 全文完整，7 个任务（5 仿真 + 2 真实）× 7 种相机配置的系统评估充分
- **Summary**: 提出 AV-ALOHA 系统，在 ALOHA 2 基础上增加 7-DoF AV 臂搭载立体相机，通过 VR 头显控制相机视角，实现沉浸式遥操作，实验证明 active vision 在遮挡/精度任务（Group 2）上显著优于固定相机，但在简单任务（Group 1）上可能因动作空间增大而降低性能
## 关键贡献

1. AV-ALOHA 系统：在 ALOHA 2 基础上增加 7-DoF AV 臂（ViperX-300 改装），仅承载立体相机
2. VR 沉浸式遥操作：Meta Quest 头显控制 AV 臂，提供立体视觉和第一人称操控体验
3. 开源仿真环境：MuJoCo 中实现完整的 AV-ALOHA，仅需 VR 头显即可收集数据
4. 系统性评估：7 个任务 × 7 种相机配置的完整消融
## 结构化提取

- **Problem**: 固定相机在遮挡/精度任务中的视觉信息不足问题
- **Method**: AV-ALOHA — 7-DoF AV 臂 + VR 头显控制 + ACT 策略学习
- **Tasks**: Peg/Slot Insertion、Hook Package、Pour Test Tube、Thread Needle、Occluded Insertion、Hidden Pick
- **Sensors**: ZED Mini 立体相机（AV）、RealSense D405（固定+手腕）
- **Robot Setup**: 3×ViperX-300（2 操控 + 1 AV），开源低成本（额外 ~$6600）
- **Metrics**: 成功率（两阶段：部分/完全成功）
- **Limitations**: 动作空间大、数据量少、distribution shift
- **Evidence Notes**: 全文读取，Table I 提供 7 任务×7 配置的完整成功率
## 本地引用关系

- [[chen2025coordinated]]
- [[chen2025effective]]
- [[lee2025diffdagger]]
- [[wu2025imperfect]]
## Problem

模仿学习中相机通常固定放置，导致遮挡和视野受限问题。现有系统缺乏独立于操控臂的动态视角调整能力，无法在需要精确视角的任务（如穿针、遮挡插入）中获取关键视觉信息。


## Method

- **硬件**：2×ViperX-300（操控臂）+ 1×ViperX-300 改为 7-DoF（AV 臂）+ ZED Mini 立体相机 + Meta Quest 2/3 VR 头显 + 4×RealSense D405（2 固定 + 2 手腕）
- **遥操作**：VR 头显追踪操作者头部姿态 → 差分逆运动学（Damped Least Squares）→ AV 臂关节角度；操控臂可用 VR 控制器或 ALOHA leader arms
- **策略训练**：ACT（LeRobot 实现），动作空间扩展至 21 维（2×7 操控 + 7 AV），chunk size=50，ResNet18 视觉骨干
- **数据**：每个任务 50 条演示，统一收集所有相机视角的数据


## Experiments

- **任务分组**：
  - Group 1（不需要 AV）：Peg Insertion、Slot Insertion、Hook Package
  - Group 2（受益于 AV）：Pour Test Tube、Thread Needle、Occluded Insertion、Hidden Pick
- **关键结果**：
  - Group 2 任务中 AV + Wrist 配置整体最优：Occluded Insertion 95%/30%（grasp/insert）、Hidden Pick 95%/60%
  - Thread Needle 任务 AV 单独达到 98%/52%，远超 Static 88%/30%
  - Group 1 任务中 Static 相机表现更好：Slot Insertion Static 98%/78% vs AV 88%/50%
  - 使用所有 6 个相机（AV+Static+Wrist）从未进入前三，信息冗余反而有害
  - AV 单独在 pour test tube 和 thread needle 上达到最高成功率


## Limitations

1. 扩大的动作空间（21 维）增加了策略学习复杂度
2. 50 条演示数据量偏少，可能不足以充分学习 AV 策略
3. AV 策略受 distribution shift 影响更大（移动相机视角变化大）
4. 真实机器人任务仅 2 个，20 次试验统计量有限
5. VR 头显长时间佩戴影响操作体验


## Key Takeaways

- Active vision 在遮挡和精度敏感任务上显著提升模仿学习性能
- 简单任务中固定相机更优（稳定坐标系、可预测的视觉输入）
- AV 与操控解耦（独立手臂）优于手腕相机（视角依赖任务执行）
- 更多相机不等于更好，信息冗余和复杂度增加会降低性能
- 人类自然视角调整行为是学习 AV 策略的有效信号源

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[chuang|Chuang, Ian]]
