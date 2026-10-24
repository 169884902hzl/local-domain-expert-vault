---
title: "Kelly Criterion"
tags: [sim-to-real, robot-learning, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Kelly Criterion 是最大化长期对数增长的下注准则，在机器人性能评估中可解释为按不确定性自适应分配仿真专家权重。"
---

## Definition

Kelly Criterion 原本来自信息论和金融下注问题，目标是在有正期望但不确定的重复决策中最大化长期对数财富增长。在 [[mahboob2026betting]] 中，它被借用为机器人性能评估的权重分配类比：把不同仿真器或估计源看作 experts，根据不确定性和收益分配权重。

## Key Ideas

- Kelly 的直觉是高置信、高收益来源应获得更大权重。
- 在性能评估中，它与 inverse-variance weighting 有联系，但不是实际金钱下注。
- Full Kelly 更激进，fractional Kelly 更保守，适合有限样本下控制风险。
- [[mahboob2026betting]] 将 sim-to-real performance estimation 建模为 sequential betting。
- 对机器人实验，Kelly-style 方法的价值在于把“哪个仿真器更可信”变成可更新的权重问题。

## Method Families

- Full Kelly weighting: 按估计优势和方差分配最大增长权重。
- Fractional Kelly: 缩小权重，降低估计误差带来的风险。
- Universal portfolio: 在不知道最优 Kelly 权重时，在线组合多个 experts。
- Conservative evaluation: 用保守权重避免单一仿真器过度支配结论。

## Key Papers

- [[mahboob2026betting]]: 直接把 Kelly/universal portfolio 用于机器人 Sim-to-Real 性能评估。
- [[jia2026gsplayground]]: 高吞吐仿真可作为 performance estimation 的候选 expert source。
- [[wu2025rlgsbridge]]: Real2Sim2Real 说明更高保真仿真可改善 expert quality。
- [[li2025routing]]: DLO 物理随机化提示 expert weighting 需要关注摩擦和材料。
- [[zhao2026visualtactile]]: 触觉仿真校准说明不同仿真源可信度应区别对待。

## Evidence Map

- [[mahboob2026betting]] 是 Kelly-style evaluation 的直接证据。
- [[jia2026gsplayground]] 与 [[wu2025rlgsbridge]] 提供可作为 expert bank 的高保真仿真路线。
- [[li2025routing]] 和 [[zhao2026visualtactile]] 提供接触/触觉任务中仿真可信度不均的证据。

## Open Problems

- 如何在少量真实机器人 rollouts 下稳定估计 Kelly 权重。
- 如何避免错误仿真器在早期偶然高分后被过度加权。
- 如何把 Kelly-style weighting 用到 DLO 任务的实验选择和性能估计。
- 如何把不确定性、硬件风险和实验成本同时纳入权重。

## Related Concepts

- [[performance-evaluation]]
- [[importance-sampling]]
- [[sim-to-real]]
- [[domain-randomization]]

## Related Papers

- [[mahboob2026betting]]
- [[jia2026gsplayground]]
- [[wu2025rlgsbridge]]
- [[li2025routing]]
- [[zhao2026visualtactile]]
