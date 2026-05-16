---
title: "Closed loop interactive embodied reasoning for robot manipulation"
tags: [manipulation, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 CLIER 闭环交互式具身推理框架：神经符号方法处理需要视觉+物理属性测量的长时序操控任务。Seq2Seq 语言→符号程序→场景图→Transformer 动作规划器→原语动作序列。支持物理属性测量（称重/刚度），闭环响应环境变化和执行失败。SHOP-VRB2 仿真 43.9%，YCB 仿真 76.7%，YCB 真实 64.4%"
authors: "Nazarczuk, Michal; Behrens, Jan Kristof; Stepanova, Karla; Hoffmann, Matej; Mikolajczyk, Krystian"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "5UC3CYCS"
---
## 摘要

Embodied reasoning systems integrate robotic hardware and cognitive processes to perform complex tasks, typically in response to a natural language query about a specific physical environment. This usually involves changing the belief about the scene or physically interacting and changing the scene (e.g. sort the objects from lightest to heaviest). In order to facilitate the development of such systems we introduce a new modular Closed Loop Interactive Embodied Reasoning (CLIER) approach that takes into account the measurements of non-visual object properties, changes in the scene caused by external disturbances as well as uncertain outcomes of robotic actions. CLIER performs multi-modal（多模态） reasoning and action planning and generates a sequence of primitive actions that can be executed by a robot manipulator. Our method operates in a closed loop, responding to changes in the environment.

## 中文简述

提出基于学习方法的绳索操控方法。

**研究方向**: 机器人操控、机器人学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV-V)、tables (I-III)、figures (1-6)
- **Confidence**: high — 全文完整，arXiv 2025 预印本（v2），Huawei/CTU/Imperial，MuBlE 仿真 + Franka 真实机器人，10 类任务，SHOP-VRB2 + YCB-VRB 基准
- **Summary**: 提出 CLIER 闭环交互式具身推理框架：神经符号方法处理需要视觉+物理属性测量的长时序操控任务。Seq2Seq 语言→符号程序→场景图→Transformer 动作规划器→原语动作序列。支持物理属性测量（称重/刚度），闭环响应环境变化和执行失败。SHOP-VRB2 仿真 43.9%，YCB 仿真 76.7%，YCB 真实 64.4%
## 关键贡献

1. 闭环交互式具身推理框架：每帧重新规划，响应环境变化和执行失败
2. 物理属性测量规划：支持重量/刚度等非视觉属性的原语动作（weigh/squeeze）
3. 神经符号方法：语言→符号程序→场景图→Transformer 动作规划→原语控制
4. MuBlE 仿真环境：MuJoCo 物理 + Blender 高质量渲染
5. SHOP-VRB2 基准：10 类需要视觉+物理推理的长时序任务
## 结构化提取

- **Problem**: 需要物理属性测量的长时序操控 + 闭环恢复
- **Method**: CLIER — 符号程序生成 + 场景图 + Transformer 动作规划 + 闭环原语执行
- **Tasks**: 10 类（称重/移动/堆叠/排序，SHOP-VRB2 + YCB-VRB）
- **Sensors**: RGB-D 相机（RealSense D455）+ 力/触觉（称重/刚度）
- **Robot Setup**: MuBlE（MuJoCo+Blender）仿真 + Franka Panda 真实
- **Metrics**: 任务成功率 + 物理属性测量准确性
- **Limitations**: 复杂任务低成功率、依赖位姿精度、仅桌面场景
- **Evidence Notes**: 全文读取，Tables I-III 提供完整结果
## 本地引用关系

- [[dalal2025local]]
- [[do2025watch]]
- [[liu820enhancing]]
- [[smith2024steer]]
- [[wang2023hierarchical]]
## Problem

具身推理系统需要在自然语言指令下执行需要物理交互的长时序任务（如"按从重到轻堆叠金属物体"）。现有方法要么开环（无法处理失败/干扰），要么仅基于视觉（无法测量重量/刚度等非视觉属性），要么缺乏快速闭环响应能力。


## Method

- **场景解析**：Mask R-CNN 分割 + ResNet 属性分类 + CosyPose 位姿回归
- **场景图**：物体节点（视觉/物理属性+位姿+gripper 关系），物理属性可为空（未知）
- **符号程序生成**：Seq2Seq 网络将语言指令翻译为 CLEVR-IEP 格式符号程序
- **符号程序执行**：在场景图上评估程序，遇到空属性则生成子目标（如"测量重量"）
- **动作规划器**：2 层 Transformer 编码器，输入场景图+子目标，预测原语动作+目标物体
- **原语动作集**：move/approach/close gripper/open gripper/lift/lower/weigh/squeeze
- **闭环执行**：
  - 物理循环：每步控制信号→物理计算→观测
  - 动作循环：每帧重新评估场景图→重新规划
  - 失败恢复：抓取失败、物体掉落等均可在下一帧恢复


## Experiments

- **SHOP-VRB2 仿真**（10 类任务）：
  - 简单任务：称重单个 74.0%、移动单个 76.0%
  - 复杂任务：堆叠按重量排序 18.0%、堆叠三物体 0.0%
  - 总体：43.9%（困难基准）
  - 失败分析：执行错误 14.4%、场景不一致 12.6%、循环检测 10.8%、识别错误 9.6%
- **YCB-VRB**（30 场景）：
  - 仿真 76.7%，真实 64.4%（sim2real 差距小）
  - 真实成功率：称重单个 88.9%、移动单个 100%、堆叠 66.7%
- **消融**（YCB）：
  - GT 位姿+GT 属性+推理: 86.7%/86.7%（sim/real）
  - 全部推理: 76.7%/64.4%
  - 位姿估计误差是主要退化来源
- **延迟**：CosyPose 0.8s、属性识别 0.15s、动作规划 0.02s（2080Ti）


## Limitations

1. 多物体复杂任务成功率低（堆叠三物体 0%）
2. 依赖 CosyPose 位姿精度，遮挡时退化
3. 关节极限和奇异位形影响执行
4. 仅桌面场景验证
5. 物理属性仅支持重量和刚度


## Key Takeaways

- 神经符号方法在需要物理交互的长时序推理中有效：符号程序提供可解释的规划
- 闭环是关键：每帧重新规划使系统从执行错误中恢复
- 物理属性测量扩展了机器人推理能力：不仅"看到"还能"感知"
- Sim-to-real 迁移良好：高质量渲染（Blender）使视觉模块零迁移
- 多物体堆叠/排序仍是挑战：长动作序列的误差累积

## 相关概念

- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[nazarczuk|Nazarczuk, Michal]]
