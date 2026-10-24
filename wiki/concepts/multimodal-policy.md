---
title: "Multimodal Policy"
tags: [concept, imitation-learning, diffusion-policy]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "能表示多种不同但均有效的行为策略的策略表示，常见于机器人操控中的多抓取策略、多路径规划等场景。"
---

## Definition

Multimodal Policy is maintained here as an evidence-linked concept. 能表示多种不同但均有效的行为策略的策略表示，常见于机器人操控中的多抓取策略、多路径规划等场景。

## Key Ideas

- Direct local evidence currently comes from [[longhini2026behavioral]].
- The concept is tracked with local tags: concept, imitation-learning, diffusion-policy.
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
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026forceflow]] (broader context): 基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（V...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[wang2026ocra]] (broader context): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。

## Evidence Map

- Direct evidence papers: [[longhini2026behavioral]].
- Broader local evidence context: [[longhini2026behavioral]], [[ziakas2026aligning]], [[zhu2024scaling]], [[zhao2026rosclaw]], [[zhang2026forceflow]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-policy]]
- [[mode-collapse]]
- [[behavioral-mode-discovery]]
- [[skill-discovery]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[longhini2026behavioral]]
- [[ziakas2026aligning]]
- [[zhu2024scaling]]
- [[zhao2026rosclaw]]
- [[zhang2026forceflow]]
- [[xu2026roboagent]]
- [[wang2026ocra]]
- [[niu2026versatile]]
