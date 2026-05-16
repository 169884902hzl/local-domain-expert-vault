---
title: "Contrastive Decoding"
tags: [decoding-strategy, inference, hallucination]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "通过对比原始输入与扰动/遮蔽输入的输出分布，抑制模型对无关特征的依赖，用于减少幻觉或伪相关。"
---

## Definition

Contrastive Decoding is maintained here as an evidence-linked concept. 通过对比原始输入与扰动/遮蔽输入的输出分布，抑制模型对无关特征的依赖，用于减少幻觉或伪相关。

## Key Ideas

- Direct local evidence currently comes from [[wu2026contrastive]].
- The concept is tracked with local tags: decoding-strategy, inference, hallucination.
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

- [[wu2026contrastive]] (direct evidence): 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[chen2025effective]] (broader context): 提出 S2I 框架，将混合质量演示在片段级别进行分割、对比学习选择高质量片段、贪心轨迹优化低质量片段，仅用 3 条专家演示即可为多种下游策略（BC-RNN/DP/ACT/RI...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[wu2026contrastive]].
- Broader local evidence context: [[wu2026contrastive]], [[zheng2026pokevla]], [[zhang2026touchguide]], [[zhang2026prts]], [[wang2026stepnft]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[contrastive-learning]]
- [[spurious-correlation]]
- [[openvla]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wu2026contrastive]]
- [[zheng2026pokevla]]
- [[zhang2026touchguide]]
- [[zhang2026prts]]
- [[wang2026stepnft]]
- [[chen2025effective]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
