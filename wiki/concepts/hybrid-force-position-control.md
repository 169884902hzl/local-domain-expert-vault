---
title: "混合力-位姿控制 (Hybrid Force-Position Control)"
tags: [control, manipulation, force-control]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "同时控制末端执行器位姿和接触力的混合控制策略，使机器人在接触丰富任务中实现独立的力和位姿调节。"
---

## Definition

混合力-位姿控制 (Hybrid Force-Position Control) is maintained here as an evidence-linked concept. 同时控制末端执行器位姿和接触力的混合控制策略，使机器人在接触丰富任务中实现独立的力和位姿调节。

## Key Ideas

- Direct local evidence currently comes from [[li2026forcevla2]].
- The concept is tracked with local tags: control, manipulation, force-control.
- Treat this page as a map into local readings, not as external ground truth.
- Claims should be checked against the linked `status: done` topic notes before use in proposals.
- When evidence is sparse, use the broader-context papers below only for comparison, not as proof of the concept.

## Method Families

- Direct paper-specific method: inspect the direct evidence papers listed below.
- Robot learning context: compare how the concept changes policy learning, evaluation, or deployment.
- Planning/control context: check whether the concept affects temporal abstraction, constraints, or execution feedback.
- Representation context: check whether the concept changes visual, language, tactile, or geometric state representation.
- Evaluation context: prefer papers with explicit baseline, metric, ablation, and failure analysis.

## Key Papers

- [[li2026forcevla2]] (direct evidence): ForceVLA2 在 VLA 框架中引入 force prompt 驱动的长时推理和 Cross-Scale MoE 实现混合力-位姿控制，在5个接触丰富任务上平均成功率6...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[liu2025autonomous]] (broader context): 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL...
- [[das2026dart]] (broader context): DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...

## Evidence Map

- Direct evidence papers: [[li2026forcevla2]].
- Broader local evidence context: [[li2026forcevla2]], [[liu2025forcemimic]], [[zhou2026vlbiman]], [[yang2026rise]], [[liu2025autonomous]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[impedance-control]]
- [[contact-rich-manipulation]]
- [[vla]]
- [[force-prompt]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[li2026forcevla2]]
- [[liu2025forcemimic]]
- [[zhou2026vlbiman]]
- [[yang2026rise]]
- [[liu2025autonomous]]
- [[das2026dart]]
- [[zheng120dottip]]
- [[zhang2026visionlanguageaction]]
