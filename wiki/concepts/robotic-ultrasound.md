---
title: "Robotic Ultrasound"
tags: [VLM, manipulation, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Robotic Ultrasound 将机器人控制与超声成像结合，用于自动扫描、针插入、针跟踪和医学介入任务。"
---

## Definition

Robotic Ultrasound (RUS) 指用机器人执行超声探头操作、图像采集、针插入或其他超声引导介入任务。它结合医学图像、力/接触控制和机器人运动规划，目标是降低对人工经验的依赖并提升一致性。

## Key Ideas

- RUS 的核心挑战是超声图像噪声、组织变形、探头接触力和针可见性。
- [[zhang2026visionlanguageaction]] 将 VLA 引入超声引导自动针插入和 needle tracking。
- 异步 tracking/control pipeline 可分别满足视觉跟踪和动作生成的频率需求。
- 不确定性感知控制对医疗机器人安全性很关键。
- 对通用具身智能而言，RUS 是高风险、强闭环、强感知约束任务的案例。

## Method Families

- Autonomous ultrasound scanning: 控制探头完成扫描和目标定位。
- Ultrasound-guided needle insertion: 根据图像反馈控制针插入。
- VLA/VLM-assisted RUS: 用多模态模型理解图像和生成动作。
- Uncertainty-aware medical control: 将感知置信度纳入安全控制。

## Key Papers

- [[zhang2026visionlanguageaction]]: VLA 用于 adaptive ultrasound-guided needle insertion and tracking。
- [[brohan2023rt2]]: VLA 通用控制背景。
- [[kim2024openvla]]: 开源 VLA baseline。
- [[dong2025vitavla]]: 高效 VLA 蒸馏路线。
- [[wang2025vlaadapter]]: tiny-scale VLA adapter，对实时医疗机器人有参考。

## Evidence Map

- [[zhang2026visionlanguageaction]] 是 RUS 的直接本地证据，包含跟踪头、控制策略和实验结果。
- [[dong2025vitavla]] 与 [[wang2025vlaadapter]] 说明 VLA 可通过 adapter/distillation 降低部署成本。
- [[brohan2023rt2]] 和 [[kim2024openvla]] 提供 VLA 基础模型背景。

## Open Problems

- 如何保证超声图像低质量时的闭环安全。
- 如何把组织变形、接触力和针轨迹纳入统一 world model。
- 如何降低 VLA 在医疗机器人中的延迟和验证成本。
- 如何将细长物体跟踪经验迁移到线缆/DLO 操控。

## Related Concepts

- [[needle-tracking]]
- [[vision-language-action]]
- [[robotic-manipulation]]
- [[sim-to-real]]

## Related Papers

- [[zhang2026visionlanguageaction]]
- [[brohan2023rt2]]
- [[kim2024openvla]]
- [[dong2025vitavla]]
- [[wang2025vlaadapter]]
