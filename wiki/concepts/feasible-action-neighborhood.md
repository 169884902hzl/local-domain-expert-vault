---
title: "Feasible Action Neighborhood (FAN)"
tags: [concept, manipulation, VLA, regularization]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "物理操控中，每个状态周围存在一组近似等价的动作邻域，而非单一正确动作。利用FAN先验可以正则化VLA策略分布，提升泛化和样本效率。"
---

## Definition

Feasible Action Neighborhood (FAN) is maintained here as an evidence-linked concept. 物理操控中，每个状态周围存在一组近似等价的动作邻域，而非单一正确动作。利用FAN先验可以正则化VLA策略分布，提升泛化和样本效率。

## Key Ideas

- Direct local evidence currently comes from [[niu2026boosting]].
- The concept is tracked with local tags: concept, manipulation, VLA, regularization.
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

- [[niu2026boosting]] (direct evidence): 提出Feasible Action Neighborhood (FAN)引导的正则化方法，用高斯先验约束VLA策略分布形状，在SFT和RFT（PPO）两种微调范式中均显著提升...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[liu2025autonomous]] (broader context): 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...

## Evidence Map

- Direct evidence papers: [[niu2026boosting]].
- Broader local evidence context: [[niu2026boosting]], [[zhou2025oneshot]], [[luijkx2026llmguided]], [[liu2025autonomous]], [[zhu2026nsvla]].
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
- [[openvla]]
- [[action-tokenization]]
- [[online-fine-tuning]]
- [[grpo]]
- [[robotic-manipulation]]

## Related Papers

- [[niu2026boosting]]
- [[zhou2025oneshot]]
- [[luijkx2026llmguided]]
- [[liu2025autonomous]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026rcnf]]
- [[zhong2026vlaopd]]
