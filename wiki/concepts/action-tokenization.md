---
title: "Action Tokenization"
tags: [concept, imitation-learning, action-representation]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "将连续动作轨迹离散化为 token 序列的表征方法，用于结构化动作空间和支持离散化策略学习"
---

## Definition

Action Tokenization is maintained here as an evidence-linked concept. 将连续动作轨迹离散化为 token 序列的表征方法，用于结构化动作空间和支持离散化策略学习

## Key Ideas

- Direct local evidence currently comes from [[huang2026mimic]].
- The concept is tracked with local tags: concept, imitation-learning, action-representation.
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

- [[huang2026mimic]] (direct evidence): 提出频域多尺度 action tokenizer (SDAT)，通过 DCT 频谱分解将行为意图与执行细节解耦，实现意图驱动的模仿学习、one-shot 技能迁移和泛化增强
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...

## Evidence Map

- Direct evidence papers: [[huang2026mimic]].
- Broader local evidence context: [[huang2026mimic]], [[zhu2024scaling]], [[zhou2025oneshot]], [[zheng2026pokevla]], [[zhao2026visualtactile]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[huang2026mimic]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[zhao2023finegrained]]
- [[zhang2026world2minecraft]]
