---
title: "Bellman Operator"
tags: [concept, RL]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "将值函数递归更新的算子，经典形式用加权和，liveness 变体用 min 算子"
---

## Definition

Bellman Operator is maintained here as an evidence-linked concept. 将值函数递归更新的算子，经典形式用加权和，liveness 变体用 min 算子

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
- [[wang2026adagamma]] (broader context): 提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[sha2026efficient]] (broader context): 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插...
- [[chang2026partially]] (broader context): 提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 IC...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...

## Evidence Map

- Direct evidence papers: [[wang2026offline]].
- Broader local evidence context: [[wang2026offline]], [[wang2026adagamma]], [[ziakas2026aligning]], [[sha2026efficient]], [[chang2026partially]].
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
- [[wang2026adagamma]]
- [[ziakas2026aligning]]
- [[sha2026efficient]]
- [[chang2026partially]]
- [[zhu2026nsvla]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
