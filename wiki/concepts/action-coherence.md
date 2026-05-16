---
title: "Action Coherence"
tags: [manipulation, imitation-learning, policy]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "动作序列的时序连贯性和平滑程度，衡量连续动作间的一致性，对精细操控至关重要。"
---

## Definition

Action Coherence is maintained here as an evidence-linked concept. 动作序列的时序连贯性和平滑程度，衡量连续动作间的一致性，对精细操控至关重要。

## Key Ideas

- Direct local evidence currently comes from [[park2026acg]].
- The concept is tracked with local tags: manipulation, imitation-learning, policy.
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

- [[park2026acg]] (direct evidence): 提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造\"不一致向量场\"，再沿反方向引导 flow matching VLA 策略生...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: [[park2026acg]].
- Broader local evidence context: [[park2026acg]], [[zhu2026nsvla]], [[zhu2024scaling]], [[zhou2025oneshot]], [[zhong2026vlaopd]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-chunking]]
- [[perturbation-guidance]]
- [[imitation-learning]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[park2026acg]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
