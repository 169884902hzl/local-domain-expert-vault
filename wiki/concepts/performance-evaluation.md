---
title: "Performance Evaluation"
tags: [sim-to-real, robot-learning, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Performance Evaluation 关注固定策略在目标环境中的真实表现估计，是机器人实验规划和 Sim-to-Real 验证的核心环节。"
---

## Definition

Performance Evaluation 指给定一个固定策略、控制器或机器人系统，估计其在目标真实环境中的期望表现。它不同于 policy learning：策略通常已经固定，目标是用有限实验成本获得可信性能估计。

## Key Ideas

- 机器人真实实验昂贵、慢且有硬件风险，不能只依赖大量真机 trials。
- 仿真评估便宜但有 sim-real gap，需要估计或校正偏差。
- [[mahboob2026betting]] 将性能评估建模为 sequential betting / expert weighting 问题。
- 对 DLO，性能评估必须覆盖材料、摩擦、长度、初始形状和干扰。
- 高质量 idea 需要先定义 metrics、baselines、pilot 和 failure modes，否则无法变成实验。

## Method Families

- Direct real-world evaluation: 直接在目标硬件上估计成功率或代价。
- Simulation-assisted evaluation: 用仿真扩展测试覆盖，再用少量真实数据校正。
- Importance-sampling evaluation: 用 proposal samples 加权估计目标表现。
- Expert/betting evaluation: 多个仿真器或估计源按可信度自适应加权。

## Key Papers

- [[mahboob2026betting]]: 性能评估的直接方法论文。
- [[chen2025benchmarking]]: RoboTwin benchmark 展示双臂真实评估难度。
- [[huang2026kinder]]: 物理推理 benchmark 提供系统化评估维度。
- [[li2025routing]]: DLO routing 给出真实/仿真性能对比。
- [[zhao2026visualtactile]]: PiH 中同时评估 seen/unseen、sim-to-real、ablation。

## Evidence Map

- [[mahboob2026betting]] 说明评估本身是研究问题，而不是训练后的附属步骤。
- [[chen2025benchmarking]] 和 [[huang2026kinder]] 提供 benchmark 化评估证据。
- [[li2025routing]] 与 [[zhao2026visualtactile]] 展示具体操控任务中指标、泛化和真机迁移的重要性。

## Open Problems

- 如何用很少真机 trials 评估 DLO 策略的可靠性和风险。
- 如何把失败类型、接触力、DLO 张力和任务成功率综合成评价。
- 如何避免只在单一 benchmark 上过拟合。
- 如何把每日 idea 自动转成带 pilot 和审计指标的实验计划。

## Related Concepts

- [[sim-to-real]]
- [[domain-randomization]]
- [[importance-sampling]]
- [[kelly-criterion]]

## Related Papers

- [[mahboob2026betting]]
- [[chen2025benchmarking]]
- [[huang2026kinder]]
- [[li2025routing]]
- [[zhao2026visualtactile]]
