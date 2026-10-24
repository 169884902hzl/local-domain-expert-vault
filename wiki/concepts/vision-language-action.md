---
title: "Vision-Language-Action"
tags: [VLM, robot-learning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "VLA 模型把视觉、语言和动作统一到机器人策略中，是具身智能中连接语义理解与低层控制的重要模型族。"
---

## Definition

Vision-Language-Action (VLA) 模型在视觉和语言输入基础上直接生成机器人动作或动作 token。它通常继承 VLM/LLM 的语义理解能力，再通过机器人数据微调、动作头或专家蒸馏接入控制空间。

## Key Ideas

- VLA 的关键不是只理解图像和指令，而是把理解结果变成可执行动作。
- 动作表示可为离散 action tokens、连续 action head、flow matching 或 diffusion/action chunk。
- [[zhang2026visionlanguageaction]] 将 VLA 引入机器人超声针插入与跟踪，是医疗机器人场景的专门化 VLA。
- [[cortex2026]] 类 world-model VLA 暴露出 reactive VLA 的长时序失败问题。
- 对 DLO，VLA 可承担任务理解和高层规划，但低层接触控制仍需 tactile/diffusion/MPC。

## Method Families

- Tokenized action VLA: 将动作离散化为语言模型 token。
- Adapter/action-head VLA: 在 VLM backbone 上添加轻量动作头或 adapter。
- Expert-distilled VLA: 用专门动作模型蒸馏到 VLM/VLA。
- World-model VLA: 在动作前生成和评分未来轨迹。

## Key Papers

- [[zhang2026visionlanguageaction]]: VLA 用于机器人超声针插入和针跟踪。
- [[brohan2023rt2]]: RT-2 将 web-scale VLM 迁移到机器人控制。
- [[kim2024openvla]]: OpenVLA 提供开源 VLA baseline。
- [[dong2025vitavla]]: VITA-VLA 用 action expert distillation 教 VLM 行动。
- [[wang2025vlaadapter]]: VLA-Adapter 分析小规模 VLA 的桥接范式。

## Evidence Map

- [[zhang2026visionlanguageaction]] 提供 VLA 在特殊医疗机器人任务中的直接证据。
- [[brohan2023rt2]]、[[kim2024openvla]]、[[dong2025vitavla]] 和 [[wang2025vlaadapter]] 构成本地 VLA 基线谱系。
- [[aida2026cortex]] 说明 reactive VLA 需要 world model 和 planning 才能处理长时序工业任务。

## Open Problems

- 如何让 VLA 处理接触丰富、触觉驱动和可变形物体任务。
- 如何评估 VLA 是否真正理解物理约束，而不是语义匹配。
- 如何把 VLA 的高层规划与 diffusion/MPC/tactile 低层控制连接。
- 如何降低 VLA 微调和部署成本，使其适合实验室双臂 DLO 平台。

## Related Concepts

- [[vision-language-model]]
- [[robotic-manipulation]]
- [[planning]]
- [[robotic-ultrasound]]

## Related Papers

- [[zhang2026visionlanguageaction]]
- [[brohan2023rt2]]
- [[kim2024openvla]]
- [[dong2025vitavla]]
- [[wang2025vlaadapter]]
- [[aida2026cortex]]
