---
title: "STEER: Flexible robotic manipulation via dense language grounding"
tags: [manipulation, VLM, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机器人演示数据集重新标注，提取抓取角度（top-down/side/diagonal）、重定向（upright↔horizontal）、提升/放置等基本技能原语；(2) RT-1 策略在这些密集标注上训练；(3) VLM（Gemini 1.5 Pro）或人类在推理时通过 API 编排技能。结果：STEER 倒水任务 90%（vs RT-H 70%、RT-1 不可行、OpenVLA 不可行），零样本 VLM 编排倒水 6/10，self-improvement 提升到 8/10"
authors: "Smith, Laura; Irpan, Alex; Arenas, Montserrat Gonzalez; Kirmani, Sean; Kalashnikov, Dmitry et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "5VXTQXML"
---
## 摘要

The complexity of the real world demands robotic systems that can intelligently adapt to unseen situations. We present STEER, a robot learning framework that bridges high-level, commonsense reasoning with precise, flexible low-level control. Our approach translates complex situational awareness into actionable low-level behavior through training language-grounded policies with dense annotation. By structuring policy training around fundamental, modular manipulation（操控） skills expressed in natural language, STEER exposes an expressive interface for humans or Vision-Language Models (VLMs) to intelligently orchestrate the robot's behavior by reasoning about the task and context. Our experiments demonstrate the skills learned via STEER can be combined to synthesize novel behaviors to adapt to new situations or perform completely new tasks without additional data collection or training.


## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 机器人操控、视觉-语言模型、机器人学习

## 关键贡献

1. 密集语言标注框架：从异构演示中提取可组合的操控原语
2. 抓取角度/重定向/提升放置等技能原语的语言索引
3. VLM 编排零样本新任务：无需额外训练
4. 100× 更小模型超越 OpenVLA：密集标注 > 大模型
## 结构化提取

- **Problem**: 训练可被高级推理灵活引导的低级操控策略
- **Method**: STEER — 密集语言标注 + RT-1 训练 + VLM/人类编排
- **Tasks**: Kettle/Plant/Fruit 抓取 + 倒水 + 杯子翻转
- **Sensors**: 机器人头部相机（RGB）
- **Robot Setup**: 移动操控机器人（7-DoF arm + 2F gripper + 移动基座）
- **Metrics**: 任务成功率 + 可引导性
- **Limitations**: 部分人工标注、物体名称敏感、技能原语有限
- **Evidence Notes**: 全文读取，Figures 5-7 提供完整结果可视化
## 本地引用关系

- [[chen2025effective]]
- [[dey2025revla]]
- [[garcia2025generalizable]]
- [[nasiriany2025rtaffordance]]
- [[shi2025zeromimic]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、system design (Sec III)、experiments (Sec IV)、figures (1-7)
- **Confidence**: high — 全文完整，arXiv 2024，Google DeepMind + UC Berkeley，移动操控机器人（RT-1 平台），70K 演示+15K 抓取数据集，密集语言标注训练可引导策略，倒水 90%，零样本新任务
- **Summary**: 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机器人演示数据集重新标注，提取抓取角度（top-down/side/diagonal）、重定向（upright↔horizontal）、提升/放置等基本技能原语；(2) RT-1 策略在这些密集标注上训练；(3) VLM（Gemini 1.5 Pro）或人类在推理时通过 API 编排技能。结果：STEER 倒水任务 90%（vs RT-H 70%、RT-1 不可行、OpenVLA 不可行），零样本 VLM 编排倒水 6/10，self-improvement 提升到 8/10


## Problem

机器人操控策略通常只能执行训练时见过的任务序列，无法适应新的场景组合。如何设计低级策略使其可被高级推理系统（VLM/人类）灵活引导，从而无需新数据即可合成新行为？


## Method

- **密集标注**（从 70K+15K 演示中提取）：
  - **抓取角度**：3D 单位向量表示腕部朝向 → 20 个聚类 → 语义标签（top-down/side/diagonal）
  - **重定向**：检测 gripper 闭合期间的腕部朝向变化 → "reorient object upright/horizontal"
  - **提升/放置**：检测 gripper 闭合+垂直运动 → "hold and lift object" / "place object"
- **策略训练**：
  - RT-1 架构，条件化于密集语言指令
  - 原始指令被替换为密集标注的子轨迹指令
  - 混合 RT-1 数据集(70K) + MOO 抓取数据(15K)
- **高级编排**：
  - VLM（Gemini 1.5 Pro）作为代码编写 agent
  - API：grasp(object, approach), reorient(object, direction), lift(object), place(object)
  - 零样本：无示例，VLM 根据场景和任务描述生成代码
  - Self-improvement：成功轨迹作为 in-context examples → 6/10 → 8/10


## Experiments

- **未见物体抓取**（3 场景×10-20 trials）：
  - Kettle: STEER 80% (top) / 85% (side), RT-1 55%, OpenVLA 60%
  - Potted Plant: STEER 80%, RT-1 30%, OpenVLA 50%
  - Fruit in Clutter: STEER 67%, RT-1 33%, OpenVLA 47%
- **新任务（倒水）**：
  - STEER (human): 90%, RT-H (language motions): 70%, RT-1: 不可行, OpenVLA: 不可行, Goal Image: 0%
  - STEER 仅需 5 条开环指令（vs RT-H 需 15 条闭环指令）
- **VLM 编排**：
  - 零样本倒水：6/10
  - Self-improvement（加 2 个 in-context examples）：8/10
  - 失败原因：低级策略对物体名称敏感
- **可引导性测试**：
  - STEER 根据语言指令显著改变抓取策略
  - RT-1/OpenVLA 无明显变化


## Limitations

1. 密集标注目前需部分人工锚定（约 20 个聚类标注）
2. 低级策略对物体名称敏感（VLM 生成名称与训练不匹配）
3. 仅验证桌面操控，未扩展到移动操控
4. 技能原语类型有限（抓取/旋转/提升/放置）
5. VLM 编排成功率低于人工编排


## Key Takeaways

- 密集语言标注是低成本提升策略灵活性的关键：无需新数据
- 技能可组合性使零样本新任务成为可能：倒水 90%
- 100× 更小模型+密集标注可超越大模型：RT-1(35M) > OpenVLA(7B)
- 抓取角度是重要的技能维度：影响下游任务可行性
- VLM self-improvement 有效：6/10 → 8/10 仅需成功示例

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[grasping]]

## 相关研究者

- [[smith|Smith, Laura]]
- [[kirmani|Kirmani, Sean]]
