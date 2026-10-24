---
title: "Advantage-Conditioned Reinforcement Learning"
tags: [RL, policy-optimization, advantage]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "将 advantage 信号作为条件输入引导策略生成，而非直接用作 reward 的 RL 训练范式，适用于 flow-matching/diffusion 策略。"
---

## Definition

Advantage-Conditioned Reinforcement Learning is maintained here as an evidence-linked concept. 将 advantage 信号作为条件输入引导策略生成，而非直接用作 reward 的 RL 训练范式，适用于 flow-matching/diffusion 策略。

## Key Ideas

- Direct local evidence currently comes from [[yang2026rise]].
- The concept is tracked with local tags: RL, policy-optimization, advantage.
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

- [[yang2026rise]] (direct evidence): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[karim2024davil]] (broader context): 提出 DA-VIL 框架，结合 RL（PPO 预测刚度 K）和 QP 变阻抗控制器实现双臂自适应操控。RL 策略以离散 bin 预测 6 维对角刚度矩阵，QP solver...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[chen2026adacleargrasp]] (broader context): 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...

## Evidence Map

- Direct evidence papers: [[yang2026rise]].
- Broader local evidence context: [[yang2026rise]], [[zhang2026prts]], [[yan2026tac2real]], [[karim2024davil]], [[consortium2026openhembodiment]].
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
- [[world-model]]
- [[flow-matching]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[yang2026rise]]
- [[zhang2026prts]]
- [[yan2026tac2real]]
- [[karim2024davil]]
- [[consortium2026openhembodiment]]
- [[chen2026adacleargrasp]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
