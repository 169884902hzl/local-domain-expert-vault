---
title: "ORPO (Odds Ratio Policy Optimization)"
tags: [concept, RL, preference-optimization]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "基于偏好对比的策略优化方法，通过最大化正样本相对于负样本的对数几率比来微调策略。"
---

## Definition

ORPO (Odds Ratio Policy Optimization) is maintained here as an evidence-linked concept. 基于偏好对比的策略优化方法，通过最大化正样本相对于负样本的对数几率比来微调策略。

## Key Ideas

- Direct local evidence currently comes from [[jia2026dreamplan]].
- The concept is tracked with local tags: concept, RL, preference-optimization.
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

- [[jia2026dreamplan]] (direct evidence): 通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwe...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[liu820enhancing]] (broader context): 提出 LLM+HRC 框架：GPT-4 分解高层指令为子任务序列→选择运动函数→结合 YOLOv5 感知的环境信息生成可执行代码。对于 LLM 无法处理的复杂轨迹（如水平铰链...
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[chen2026lastr1]] (broader context): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[jia2026dreamplan]].
- Broader local evidence context: [[jia2026dreamplan]], [[zhao2026rosclaw]], [[wu2025rlgsbridge]], [[sun2026maniparena]], [[liu820enhancing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grpo]]
- [[reinforcement-learning]]
- [[visual-reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jia2026dreamplan]]
- [[zhao2026rosclaw]]
- [[wu2025rlgsbridge]]
- [[sun2026maniparena]]
- [[liu820enhancing]]
- [[li2026affordsim]]
- [[chen2026lastr1]]
- [[zhu2026nsvla]]
