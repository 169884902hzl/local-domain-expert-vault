---
title: "Mode Collapse"
tags: [concept, rl-finetuning, diffusion-policy, multimodal-policy]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "RL微调生成式策略时，多样行为分布坍缩为单一奖励最大化模式的现象。"
---

## Definition

Mode Collapse is maintained here as an evidence-linked concept. RL微调生成式策略时，多样行为分布坍缩为单一奖励最大化模式的现象。

## Key Ideas

- Direct local evidence currently comes from [[longhini2026behavioral]].
- The concept is tracked with local tags: concept, rl-finetuning, diffusion-policy, multimodal-policy.
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

- [[longhini2026behavioral]] (direct evidence): 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[tong2026uncovering]] (broader context): 提出 DAERT 框架，利用基于 ROVER 的多样性感知强化学习训练 VLM 攻击者，自动生成语义保持但导致 VLA 执行失败的对抗指令，将 π₀ 成功率从 93.33%...
- [[shi2026agile]] (broader context): 提出 VLM 引导的 agentic 生成管线，从单目视频重建手-物体交互的水密网格和 6D 轨迹，用 anchor-and-track 策略替代脆弱的 SfM 初始化，实现...
- [[lian2026langforce]] (broader context): 揭示 VLA 模型在目标驱动数据集上的\"视觉捷径\"病理（语言条件互信息坍缩为零），提出基于贝叶斯分解的双分支框架 LangForce，通过 Latent Action Q...
- [[chen2026posterior]] (broader context): POCO 将生成式策略改进建模为免似然的 chunk 级后验推断问题，通过 Implicit E-M 和裁剪代理目标实现离线到在线的稳定高效微调，7 仿真 + 6 真实任务上...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...

## Evidence Map

- Direct evidence papers: [[longhini2026behavioral]].
- Broader local evidence context: [[longhini2026behavioral]], [[zhong2026vlaopd]], [[yuan2026prefmoe]], [[tong2026uncovering]], [[shi2026agile]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[behavioral-mode-discovery]]
- [[multimodal-policy]]
- [[diffusion-policy]]
- [[online-fine-tuning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[longhini2026behavioral]]
- [[zhong2026vlaopd]]
- [[yuan2026prefmoe]]
- [[tong2026uncovering]]
- [[shi2026agile]]
- [[lian2026langforce]]
- [[chen2026posterior]]
- [[ziakas2026aligning]]
