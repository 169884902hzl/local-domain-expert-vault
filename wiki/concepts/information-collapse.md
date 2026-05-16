---
title: "Information Collapse"
tags: [VLA, information-theory, dataset-bias]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "在目标驱动数据集上，语言指令的条件互信息坍缩为零，导致 VLA 模型退化为纯视觉策略。"
---

## Definition

Information Collapse is maintained here as an evidence-linked concept. 在目标驱动数据集上，语言指令的条件互信息坍缩为零，导致 VLA 模型退化为纯视觉策略。

## Key Ideas

- Direct local evidence currently comes from [[lian2026langforce]].
- The concept is tracked with local tags: VLA, information-theory, dataset-bias.
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

- [[lian2026langforce]] (direct evidence): 揭示 VLA 模型在目标驱动数据集上的\"视觉捷径\"病理（语言条件互信息坍缩为零），提出基于贝叶斯分解的双分支框架 LangForce，通过 Latent Action Q...
- [[longhini2026behavioral]] (broader context): 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026forceflow]] (broader context): 基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（V...

## Evidence Map

- Direct evidence papers: [[lian2026langforce]].
- Broader local evidence context: [[lian2026langforce]], [[longhini2026behavioral]], [[zhong2026vlaopd]], [[zhi2025closedloop]], [[zhao2026vitactracing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-shortcut]]
- [[vision-language-action]]
- [[vla]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[lian2026langforce]]
- [[longhini2026behavioral]]
- [[zhong2026vlaopd]]
- [[zhi2025closedloop]]
- [[zhao2026vitactracing]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[zhang2026forceflow]]
