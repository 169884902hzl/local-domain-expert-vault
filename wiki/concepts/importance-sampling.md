---
title: "Importance Sampling"
tags: [sim-to-real, robot-learning, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Importance Sampling 通过对辅助分布样本加权估计目标分布期望，在机器人中主要用于低成本性能估计和仿真辅助评估。"
---

## Definition

Importance Sampling (IS) 是一种估计目标分布期望的方差缩减方法：从更容易采样的 proposal distribution 取样，再用 likelihood ratio 或归一化权重修正，使估计接近目标分布结果。

## Key Ideas

- 在机器人真实评估稀缺时，IS 可用仿真样本辅助估计真实性能。
- IS 的效果高度依赖 proposal distribution 与真实分布的重叠。
- 如果仿真与真实差距过大，权重会高方差甚至失效。
- [[mahboob2026betting]] 将 IS 与 Kelly-style weighting 对比，指出机器人评估要考虑有限样本和 sim-real mismatch。
- 对 DLO，IS 的难点是很难显式写出真实绳索物理和仿真物理的密度比。

## Method Families

- Classical IS: 用显式 likelihood ratio 加权。
- Self-normalized IS: 用归一化权重降低有限样本不稳定性，但可能有偏。
- Multiple proposal IS: 多个仿真器或随机化环境共同提供样本。
- Adaptive weighting: 根据观测到的真实反馈调整不同仿真源权重。

## Key Papers

- [[mahboob2026betting]]: 将机器人性能评估与 IS/Kelly/universal portfolio 联系起来。
- [[li2025routing]]: DLO 中摩擦随机化提示 proposal distribution 选择的重要性。
- [[zhao2026visualtactile]]: 触觉 Sim-to-Real 中真实/仿真差距说明 IS 需要谨慎。
- [[jia2026gsplayground]]: 高吞吐仿真可提供大量 proposal samples。
- [[wu2025rlgsbridge]]: Real2Sim2Real 说明高保真仿真可改善 proposal 质量。

## Evidence Map

- [[mahboob2026betting]] 是本 vault 中 IS 与机器人性能评估的直接来源。
- [[jia2026gsplayground]] 和 [[wu2025rlgsbridge]] 提供构造更好 proposal simulators 的基础。
- [[li2025routing]] 和 [[zhao2026visualtactile]] 说明真实接触参数差距会影响权重可靠性。

## Open Problems

- 如何在没有显式真实分布密度时估计权重。
- 如何检测仿真 proposal 与真实 rollout 的 support mismatch。
- 如何在 DLO 这类高维形变任务中避免权重退化。
- 如何把 IS 与主动真实实验选择结合，减少硬件试验次数。

## Related Concepts

- [[performance-evaluation]]
- [[sim-to-real]]
- [[domain-randomization]]
- [[kelly-criterion]]

## Related Papers

- [[mahboob2026betting]]
- [[li2025routing]]
- [[zhao2026visualtactile]]
- [[jia2026gsplayground]]
- [[wu2025rlgsbridge]]
