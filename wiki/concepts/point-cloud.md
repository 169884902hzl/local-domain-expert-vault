---
title: "Point Cloud"
tags: [3d-perception, vision]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "三维点云感知，用于机器人操控中的空间理解和动作生成"
---

## Definition

Point Cloud is maintained here as an evidence-linked concept. 三维点云感知，用于机器人操控中的空间理解和动作生成

## Key Ideas

- Direct local evidence currently comes from [[gao2026driftbased]].
- The concept is tracked with local tags: 3d-perception, vision.
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

- [[gao2026driftbased]] (direct evidence): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...
- [[xie102multiview]] (broader context): 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减...
- [[wang2023multistage]] (broader context): 提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1)...
- [[röfer2025pseudotouch]] (broader context): 提出 PseudoTouch，从深度图像预测低维触觉信号（ReSkin 15D），构建视觉-触觉跨模态映射。用 8 个基本几何体（球、圆柱、盒等）采集配对深度-触觉数据训练...
- [[patankar2025synthesizing]] (broader context): 提出基于常螺旋运动分解和点云的抓取/重抓取合成算法。将复杂操控任务表示为常螺旋运动序列（如 pivot-slide-pivot），使用任务导向抓取度量 η 计算每段螺旋的抓取...
- [[kuroki2025gendom]] (broader context): 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用...
- [[huang2025match]] (broader context): 提出 MATCH POLICY，将操控 pick-place 策略转化为点云配准任务。核心流程：存储演示中的组合点云 Pab（pick/place 配置），推理时通过 RAN...
- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...

## Evidence Map

- Direct evidence papers: [[gao2026driftbased]].
- Broader local evidence context: [[gao2026driftbased]], [[xie102multiview]], [[wang2023multistage]], [[röfer2025pseudotouch]], [[patankar2025synthesizing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[gao2026driftbased]]
- [[xie102multiview]]
- [[wang2023multistage]]
- [[röfer2025pseudotouch]]
- [[patankar2025synthesizing]]
- [[kuroki2025gendom]]
- [[huang2025match]]
- [[do2025watch]]
