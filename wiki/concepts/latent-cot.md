---
title: "Latent Chain-of-Thought Reasoning"
tags: [reasoning, VLA, latent-space, chain-of-thought]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "在连续隐空间中进行链式推理，避免显式语言 CoT 的延迟和离散化瓶颈，适用于 VLA 模型的物理动态建模。"
---

## Definition

Latent Chain-of-Thought Reasoning is maintained here as an evidence-linked concept. 在连续隐空间中进行链式推理，避免显式语言 CoT 的延迟和离散化瓶颈，适用于 VLA 模型的物理动态建模。

## Key Ideas

- Direct local evidence currently comes from [[chen2026lastr1]].
- The concept is tracked with local tags: reasoning, VLA, latent-space, chain-of-thought.
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

- [[chen2026lastr1]] (direct evidence): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[li2026gazevla]] (broader context): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...

## Evidence Map

- Direct evidence papers: [[chen2026lastr1]].
- Broader local evidence context: [[chen2026lastr1]], [[xie2026humanintention]], [[shah2025acoustic]], [[niu2026versatile]], [[missal2026ropedreamer]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[chain-of-thought]]
- [[vision-language-action]]
- [[vla]]
- [[reinforcement-learning]]
- [[physical-reasoning]]
- [[robotic-manipulation]]

## Related Papers

- [[chen2026lastr1]]
- [[xie2026humanintention]]
- [[shah2025acoustic]]
- [[niu2026versatile]]
- [[missal2026ropedreamer]]
- [[li2026gazevla]]
- [[gu2026vistabot]]
- [[aida2026cortex]]
