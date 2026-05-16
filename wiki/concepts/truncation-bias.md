---
title: "Truncation Bias"
tags: [concept, RL]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "因评估回合被人工截断（超时）导致的值函数系统性低估，将潜在的接近成功误判为失败"
---

## Definition

Truncation Bias is maintained here as an evidence-linked concept. 因评估回合被人工截断（超时）导致的值函数系统性低估，将潜在的接近成功误判为失败

## Key Ideas

- Direct local evidence currently comes from [[wang2026offline]].
- The concept is tracked with local tags: concept, RL.
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

- [[wang2026offline]] (direct evidence): 将离线策略评估重新定义为折扣 liveness 问题，通过两阶段 bootstrapping 机制在稀疏奖励操控任务中捕获非单调任务进展并显著降低截断偏差。
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[mahboob2026betting]] (broader context): 将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[chang2026partially]] (broader context): 提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 IC...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[wang2026offline]].
- Broader local evidence context: [[wang2026offline]], [[yang2026rise]], [[moroncelli2026jumpstart]], [[mahboob2026betting]], [[ji2026recovering]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[policy-evaluation]]
- [[liveness]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wang2026offline]]
- [[yang2026rise]]
- [[moroncelli2026jumpstart]]
- [[mahboob2026betting]]
- [[ji2026recovering]]
- [[chang2026partially]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
