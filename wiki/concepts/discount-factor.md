---
title: "Discount Factor"
tags: [concept, RL, temporal-structure]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "RL 中控制有效规划视界和 bootstrap 强度的标量参数，标准方法使用固定值，AdaGamma 将其推广为状态依赖函数"
---

## Definition

Discount Factor is maintained here as an evidence-linked concept. RL 中控制有效规划视界和 bootstrap 强度的标量参数，标准方法使用固定值，AdaGamma 将其推广为状态依赖函数

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: concept, RL, temporal-structure.
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

- [[wang2026adagamma]] (broader context): 提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[wang2026offline]] (broader context): 将离线策略评估重新定义为折扣 liveness 问题，通过两阶段 bootstrapping 机制在稀疏奖励操控任务中捕获非单调任务进展并显著降低截断偏差。
- [[jiang2026blockr1]] (broader context): 揭示扩散语言模型多域 RL 后训练中 block size 域冲突问题，通过 teacher-student 管线为每个训练样本分配最优 block size，构建 41K...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[wang2026adagamma]], [[zhang2026prts]], [[wu2025rlgsbridge]], [[wang2026offline]], [[jiang2026blockr1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[wang2026adagamma]]
- [[zhang2026prts]]
- [[wu2025rlgsbridge]]
- [[wang2026offline]]
- [[jiang2026blockr1]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
- [[zhou2026ego]]
