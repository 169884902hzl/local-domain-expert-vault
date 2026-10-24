---
title: "One-Shot Imitation Learning"
tags: [concept, imitation-learning]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "从单次（或极少次）人类示范学习操控策略，目标是最大化数据效率并泛化到新场景"
---

## Definition

One-Shot Imitation Learning is maintained here as an evidence-linked concept. 从单次（或极少次）人类示范学习操控策略，目标是最大化数据效率并泛化到新场景

## Key Ideas

- Direct local evidence currently comes from [[zhou2026vlbiman]].
- The concept is tracked with local tags: concept, imitation-learning.
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

- [[zhou2026vlbiman]] (direct evidence): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[wang2025oneshot]] (broader context): 提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定...
- [[huang2026mimic]] (broader context): 提出频域多尺度 action tokenizer (SDAT)，通过 DCT 频谱分解将行为意图与执行细节解耦，实现意图驱动的模仿学习、one-shot 技能迁移和泛化增强
- [[dai2024racer]] (broader context): 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GP...
- [[chen2026lastr1]] (broader context): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...

## Evidence Map

- Direct evidence papers: [[zhou2026vlbiman]].
- Broader local evidence context: [[zhou2026vlbiman]], [[zhou2025oneshot]], [[wang2025oneshot]], [[huang2026mimic]], [[dai2024racer]].
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
- [[bimanual-manipulation]]
- [[cross-embodiment-transfer]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhou2026vlbiman]]
- [[zhou2025oneshot]]
- [[wang2025oneshot]]
- [[huang2026mimic]]
- [[dai2024racer]]
- [[chen2026lastr1]]
- [[zhu2026nsvla]]
- [[zhang2026prts]]
