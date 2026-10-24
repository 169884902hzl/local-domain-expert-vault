---
title: "Octo"
tags: [VLA, robot-policy, diffusion-policy]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "开源通用机器人策略，基于扩散的 VLA 模型，支持多机器人平台和任务泛化。"
---

## Definition

Octo is maintained here as an evidence-linked concept. 开源通用机器人策略，基于扩散的 VLA 模型，支持多机器人平台和任务泛化。

## Key Ideas

- Direct local evidence currently comes from [[moroncelli2026jumpstart]].
- The concept is tracked with local tags: VLA, robot-policy, diffusion-policy.
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

- [[moroncelli2026jumpstart]] (direct evidence): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[wu2026contrastive]] (broader context): 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提...
- [[team2024octo]] (broader context): UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持...
- [[gao2025must]] (broader context): 提出 MuST（Multi-Head Skill Transformer），在 Octo 骨干上增加 N+1 个 head（N 个技能 head + 1 个进度 head），...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[moroncelli2026jumpstart]].
- Broader local evidence context: [[moroncelli2026jumpstart]], [[wu2026contrastive]], [[team2024octo]], [[gao2025must]], [[zhu2026nsvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[vision-language-action]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[moroncelli2026jumpstart]]
- [[wu2026contrastive]]
- [[team2024octo]]
- [[gao2025must]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
