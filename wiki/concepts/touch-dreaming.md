---
title: "Touch Dreaming"
tags: [concept, tactile, imitation, representation-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "将未来触觉预测作为辅助训练目标的表征学习方法，在 latent 空间用 EMA teacher 监督触觉 latent 预测，正则化策略网络学习接触感知表征。"
---

## Definition

Touch Dreaming is maintained here as an evidence-linked concept. 将未来触觉预测作为辅助训练目标的表征学习方法，在 latent 空间用 EMA teacher 监督触觉 latent 预测，正则化策略网络学习接触感知表征。

## Key Ideas

- Direct local evidence currently comes from [[niu2026versatile]].
- The concept is tracked with local tags: concept, tactile, imitation, representation-learning.
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

- [[niu2026versatile]] (direct evidence): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[george2024vital]] (broader context): 提出 VITaL 预训练方法，通过时间感知的多模态对比损失将视觉和触觉编码器投影到共享潜在空间。关键发现：用触觉数据预训练的纯视觉策略性能大幅提升（USB 插入 20%→85...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[niu2026versatile]].
- Broader local evidence context: [[niu2026versatile]], [[zhao2026visualtactile]], [[xue2026tube]], [[xu2026fingereye]], [[zhao2025polytouch]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[tactile-sensing]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[niu2026versatile]]
- [[zhao2026visualtactile]]
- [[xue2026tube]]
- [[xu2026fingereye]]
- [[zhao2025polytouch]]
- [[wu2025tacdiffusion]]
- [[george2024vital]]
- [[zhu2024scaling]]
