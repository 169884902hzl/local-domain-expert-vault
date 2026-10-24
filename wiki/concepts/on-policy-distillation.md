---
title: "On-Policy Distillation"
tags: [distillation, on-policy, VLA, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "在学生策略自生成轨迹上用教师策略提供密集 token 级监督的蒸馏框架，结合了 SFT 的密集监督优势和 RL 的 on-policy 探索能力。"
---

## Definition

On-Policy Distillation is maintained here as an evidence-linked concept. 在学生策略自生成轨迹上用教师策略提供密集 token 级监督的蒸馏框架，结合了 SFT 的密集监督优势和 RL 的 on-policy 探索能力。

## Key Ideas

- Direct local evidence currently comes from [[zhong2026vlaopd]].
- The concept is tracked with local tags: distillation, on-policy, VLA, robot-learning.
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

- [[zhong2026vlaopd]] (direct evidence): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA

## Evidence Map

- Direct evidence papers: [[zhong2026vlaopd]].
- Broader local evidence context: [[zhong2026vlaopd]], [[zhu2024scaling]], [[zheng2026pokevla]], [[zhao2026visualtactile]], [[zhao2025polytouch]].
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
- [[imitation-learning]]
- [[catastrophic-forgetting]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[zhong2026vlaopd]]
- [[zhu2024scaling]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026touchguide]]
- [[yin2026multiple]]
