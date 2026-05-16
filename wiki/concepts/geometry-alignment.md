---
title: "Geometry Alignment"
tags: [3D-vision, VLA, spatial-reasoning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "在训练阶段对齐 VLM 视觉表征与 3D 几何基础模型特征，增强空间感知但推理零额外开销。"
---

## Definition

Geometry Alignment is maintained here as an evidence-linked concept. 在训练阶段对齐 VLM 视觉表征与 3D 几何基础模型特征，增强空间感知但推理零额外开销。

## Key Ideas

- Direct local evidence currently comes from [[zheng2026pokevla]].
- The concept is tracked with local tags: 3D-vision, VLA, spatial-reasoning.
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

- [[zheng2026pokevla]] (direct evidence): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[wang2025oneshot]] (broader context): 提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定...

## Evidence Map

- Direct evidence papers: [[zheng2026pokevla]].
- Broader local evidence context: [[zheng2026pokevla]], [[zhou2025oneshot]], [[zhao2026visualtactile]], [[zhang2026generative]], [[zeng2026recapa]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[sim-to-real]]
- [[spatial-grounding]]
- [[goal-aware-segmentation]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[zheng2026pokevla]]
- [[zhou2025oneshot]]
- [[zhao2026visualtactile]]
- [[zhang2026generative]]
- [[zeng2026recapa]]
- [[yang2026asyncshield]]
- [[wu2025tacdiffusion]]
- [[wang2025oneshot]]
