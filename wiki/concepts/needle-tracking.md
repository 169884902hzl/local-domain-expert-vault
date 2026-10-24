---
title: "Needle Tracking"
tags: [VLM, manipulation, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Needle tracking 在超声图像中实时定位针尖和针体，是机器人超声引导针插入闭环控制的关键感知任务。"
---

## Definition

Needle Tracking 指在 ultrasound 或其他医学图像序列中持续估计针尖、针体或针轨迹的位置。对机器人针插入而言，它提供闭环控制反馈，决定是否继续推进、调整角度或暂停。

## Key Ideas

- 超声图像中针体可能低对比、遮挡或间歇不可见，跟踪比普通视觉检测更难。
- [[zhang2026visionlanguageaction]] 用 CDF tracking head 融合浅层和深层视觉特征，提高针跟踪稳定性。
- Needle tracking 与 action generation 解耦时，可用异步 pipeline 提升控制频率。
- 不确定性感知控制可在跟踪置信度低时避免危险动作。
- 该概念与 DLO 不直接重合，但在“细长物体视觉跟踪 + 闭环控制”上有方法相似性。

## Method Families

- Template/traditional tracking: 用几何、边缘或模板匹配跟踪针。
- Deep visual tracking: 用 CNN/Siamese/Transformer 特征跟踪。
- VLA-assisted tracking: 将跟踪头接入 VLA/VLM backbone。
- Uncertainty-aware control: 根据跟踪置信度调整机器人动作。

## Key Papers

- [[zhang2026visionlanguageaction]]: VLA + CDF tracking head 用于超声针跟踪。
- [[brohan2023rt2]]: 作为 VLA 语义到动作的通用背景。
- [[dong2025vitavla]]: VLA 动作专家蒸馏，可作为小模型控制参考。
- [[wang2025vlaadapter]]: 小型 VLA adapter 对实时部署有启发。
- [[jeong2026your]]: VLA attention heads 可检测路径偏差，和跟踪/恢复机制相邻。

## Evidence Map

- [[zhang2026visionlanguageaction]] 是 needle tracking 的直接本地证据。
- [[wang2025vlaadapter]] 和 [[dong2025vitavla]] 提供高频/轻量 VLA 部署参考。
- [[jeong2026your]] 提供用 VLA 内部 attention 做路径偏差检测的相邻证据。

## Open Problems

- 如何在超声图像强噪声和遮挡下保持针尖稳定跟踪。
- 如何把跟踪不确定性转化为安全控制策略。
- 如何将细长物体 tracking 经验迁移到 DLO、线缆和绳索视觉跟踪。
- 如何在低延迟要求下运行 VLA/VLM tracking head。

## Related Concepts

- [[robotic-ultrasound]]
- [[vision-language-action]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[zhang2026visionlanguageaction]]
- [[brohan2023rt2]]
- [[dong2025vitavla]]
- [[wang2025vlaadapter]]
- [[jeong2026your]]
