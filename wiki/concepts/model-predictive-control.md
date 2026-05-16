---
title: "Model Predictive Control (MPC)"
tags: [control, planning, robotics]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "基于动力学模型在每步重新优化控制序列的滚动时域控制方法，适用于高维非线性系统。"
---

## Definition

Model Predictive Control (MPC) is maintained here as an evidence-linked concept. 基于动力学模型在每步重新优化控制序列的滚动时域控制方法，适用于高维非线性系统。

## Key Ideas

- Direct local evidence currently comes from [[missal2026ropedreamer]].
- The concept is tracked with local tags: control, planning, robotics.
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

- [[missal2026ropedreamer]] (direct evidence): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[kumar122constraining]] (broader context): 提出 COGIS 方法，在部分可观测环境中在线学习障碍物几何模型（GPIS）并通过约束优化精化数据集。利用名义动力学模型预测与实际状态差异推断接触点，结合视觉预处理/后处理清...
- [[das2026dart]] (broader context): DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。
- [[chen2025coordinated]] (broader context): 将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、...

## Evidence Map

- Direct evidence papers: [[missal2026ropedreamer]].
- Broader local evidence context: [[missal2026ropedreamer]], [[zhang2026prts]], [[zeng2026recapa]], [[sakamoto2026e3vsbench]], [[aida2026cortex]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[world-model]]
- [[recurrent-state-space-model]]
- [[deformable-linear-object]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[missal2026ropedreamer]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[sakamoto2026e3vsbench]]
- [[aida2026cortex]]
- [[kumar122constraining]]
- [[das2026dart]]
- [[chen2025coordinated]]
