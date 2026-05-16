---
title: "Two-hot Encoding"
tags: [action-representation, diffusion, world-model]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "一种连续动作编码方案，将每个动作维度映射到最近两个 bin 的线性插值权重，实现无损连续-离散转换，适用于扩散世界模型中的动作条件输入。"
---

## Definition

Two-hot Encoding is maintained here as an evidence-linked concept. 一种连续动作编码方案，将每个动作维度映射到最近两个 bin 的线性插值权重，实现无损连续-离散转换，适用于扩散世界模型中的动作条件输入。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: action-representation, diffusion, world-model.
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

- [[jiang2026world4rl]] (broader context): 提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-Worl...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[moletta2026preference]] (broader context): 提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trouser...
- [[keunknowndiffuser]] (broader context): 提出 3D Diffuser Actor，统一 3D 场景表示与扩散目标用于模仿学习。核心是 3D 相对去噪 Transformer：将 RGB-D 图像提升为 3D 场景...
- [[gao2026driftbased]] (broader context): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[jiang2026world4rl]], [[zhu2024scaling]], [[zhang2026touchguide]], [[xue2026tube]], [[wu2025tacdiffusion]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-space-design]]
- [[action-tokenization]]
- [[world-model]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[jiang2026world4rl]]
- [[zhu2024scaling]]
- [[zhang2026touchguide]]
- [[xue2026tube]]
- [[wu2025tacdiffusion]]
- [[moletta2026preference]]
- [[keunknowndiffuser]]
- [[gao2026driftbased]]
