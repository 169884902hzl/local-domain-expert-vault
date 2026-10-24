---
title: "Contrastive Learning"
tags: [representation-learning, self-supervised, training-method]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "通过对比正负样本学习表征的自监督/监督学习方法，使相似样本嵌入相近、不相似样本嵌入远离。"
---

## Definition

Contrastive Learning is maintained here as an evidence-linked concept. 通过对比正负样本学习表征的自监督/监督学习方法，使相似样本嵌入相近、不相似样本嵌入远离。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026touchguide]].
- The concept is tracked with local tags: representation-learning, self-supervised, training-method.
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

- [[zhang2026touchguide]] (direct evidence): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[chen2025effective]] (broader context): 提出 S2I 框架，将混合质量演示在片段级别进行分割、对比学习选择高质量片段、贪心轨迹优化低质量片段，仅用 3 条专家演示即可为多种下游策略（BC-RNN/DP/ACT/RI...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。

## Evidence Map

- Direct evidence papers: [[zhang2026touchguide]].
- Broader local evidence context: [[zhang2026touchguide]], [[zhang2026prts]], [[chen2025effective]], [[zhu2024scaling]], [[zhou2025oneshot]].
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
- [[tactile-sensing]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhang2026touchguide]]
- [[zhang2026prts]]
- [[chen2025effective]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zheng2026pokevla]]
- [[zheng120dottip]]
- [[zhao2026visualtactile]]
