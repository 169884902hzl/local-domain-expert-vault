---
title: "Policy Evaluation"
tags: [concept, RL]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "在给定策略下估计值函数的过程，用于量化策略从各状态出发的预期表现"
---

## Definition

Policy Evaluation is maintained here as an evidence-linked concept. 在给定策略下估计值函数的过程，用于量化策略从各状态出发的预期表现

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
- [[yin2026genie]] (broader context): Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 100...
- [[yang2026automated]] (broader context): 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[wei2026navol]] (broader context): 基于 DAgger 框架在 IsaacLab 中实现导航扩散策略的在线模仿学习，通过全局规划器提供在线专家轨迹监督，以 rollout-update 循环消除奖励工程、缓解分...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[wang2026adagamma]] (broader context): 提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error...
- [[patil2026youve]] (broader context): 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需...

## Evidence Map

- Direct evidence papers: [[wang2026offline]].
- Broader local evidence context: [[wang2026offline]], [[yin2026genie]], [[yang2026automated]], [[xu2026expertgen]], [[wei2026navol]].
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
- [[liveness]]
- [[truncation-bias]]
- [[bellman-operator]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026offline]]
- [[yin2026genie]]
- [[yang2026automated]]
- [[xu2026expertgen]]
- [[wei2026navol]]
- [[wang2026evolvable]]
- [[wang2026adagamma]]
- [[patil2026youve]]
