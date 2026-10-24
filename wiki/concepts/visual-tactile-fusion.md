---
title: "Visual-Tactile Fusion"
tags: [tactile, manipulation, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Visual-tactile fusion 将全局视觉和局部接触反馈结合，用于接触丰富操控、装配和双臂协作。"
---

## Definition

Visual-tactile fusion 是把视觉观测提供的全局几何、语义和位姿信息，与触觉观测提供的局部接触、滑移、力和形变信息融合成策略输入或训练信号。它特别适合视觉受遮挡、接触状态关键且误差容忍度低的操控任务。

## Key Ideas

- 视觉负责远距离定位和场景上下文，触觉负责接触后的局部校正。
- [[zhao2026visualtactile]] 表明 PiH 中视觉用于 approach，触觉用于补偿 peg-hole misalignment。
- [[zhao2025polytouch]] 表明多模态触觉传感器和 tactile-diffusion policy 可提升双臂接触任务成功率。
- 融合策略不仅可以作为输入融合，也可以作为奖励、示教过滤或不确定性估计信号。
- 对 DLO 操控，触觉可能提供视觉无法稳定恢复的局部张力、滑移和接触拓扑线索。

## Method Families

- Early fusion: 将视觉、触觉和机器人状态编码后拼接，输入同一策略。
- Cross-attention fusion: 用注意力机制让视觉 token 与触觉 token 动态交互。
- Tactile-as-reward: 部署时不使用触觉输入，而把触觉重建误差或触觉事件作为训练奖励。
- Tactile diffusion policy: 将触觉观测作为条件，生成接触丰富任务的动作序列。

## Key Papers

- [[zhao2026visualtactile]]: 在 PiH 中构建统一视觉-触觉观测空间，并验证 sim-to-real。
- [[zhao2025polytouch]]: 用 PolyTouch 多模态触觉手指和 tactile-diffusion policy 提升双臂接触任务。
- [[han2025upvital]]: 用非配对视觉-触觉自监督表征辅助 RL。
- [[xue2026tube]]: 当日候选，提出 reactive visual-tactile policy learning for contact-rich manipulation。
- [[liu2025forcemimic]]: 通过力-运动捕捉和 hybrid imitation learning 提供 force/tactile 融合的相邻证据。

## Evidence Map

- [[zhao2026visualtactile]] 提供视觉-触觉融合在装配任务中的直接证据，含 ablation 和真实机器人实验。
- [[zhao2025polytouch]] 提供触觉扩散策略在双臂接触任务中的本地已精读证据。
- [[han2025upvital]] 说明触觉信息也可通过自监督奖励间接改善视觉策略。
- [[xue2026tube]] 是今日候选，提示 visual-tactile diffusion 正在成为 contact-rich manipulation 的新热点。

## Open Problems

- 如何处理视觉和触觉的时间频率差异、延迟和空间配准。
- 如何让触觉融合策略泛化到不同传感器形态和安装位置。
- 如何在 DLO 操控中利用触觉估计局部张力、滑移和接触拓扑。
- 如何区分触觉真正提供的接触信息与策略对特定物体/夹具的过拟合。

## Related Concepts

- [[tactile-sensing]]
- [[diffusion-policy]]
- [[sim-to-real]]
- [[peg-in-hole]]

## Related Papers

- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[han2025upvital]]
- [[xue2026tube]]
