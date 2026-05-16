---
title: "Collision Avoidance"
tags: [collision-avoidance, safety, whole-body-control]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "机器人在动态环境中避免与物体或人发生碰撞的全身运动控制策略，可通过分布式触觉/近觉传感器或外部感知实现"
---

## Definition

Collision Avoidance is maintained here as an evidence-linked concept. 机器人在动态环境中避免与物体或人发生碰撞的全身运动控制策略，可通过分布式触觉/近觉传感器或外部感知实现

## Key Ideas

- Direct local evidence currently comes from [[kohlbrenner2026egocentric]].
- The concept is tracked with local tags: collision-avoidance, safety, whole-body-control.
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

- [[kohlbrenner2026egocentric]] (direct evidence): 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[pallar2025optimal]] (broader context): 提出 CBF 轨迹规划算法用于多四旋翼协作操控线缆悬挂刚体载荷。将载荷、线缆、四旋翼建模为凸多面体，利用对偶定理降低 CBF 约束的计算复杂度，确保全系统（载荷+线缆+四旋翼...
- [[du2024embedded]] (broader context): 提出子空间 IPC 仿真方法，用低分辨率嵌入四面体网格 + 高分辨率碰撞表面的双层表示，通过重心插值映射，实现 O(h) 收敛、2x 加速和 1.8x 实时率的可变形物体仿真...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...

## Evidence Map

- Direct evidence papers: [[kohlbrenner2026egocentric]].
- Broader local evidence context: [[kohlbrenner2026egocentric]], [[yang2026asyncshield]], [[zhang2021dair]], [[pallar2025optimal]], [[du2024embedded]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[bimanual-manipulation]]
- [[tactile-sensing]]
- [[proximity-sensing]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[grasping]]
## Related Papers

- [[kohlbrenner2026egocentric]]
- [[yang2026automated]]
- [[yang2026rise]]
- [[zhang2026safevla]]