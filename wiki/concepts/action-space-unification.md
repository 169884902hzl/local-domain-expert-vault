---
title: "Action Space Unification"
tags: [manipulation, cross-embodiment, VLA]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "将不同机器人平台的动作表示统一到固定维度的共享空间，通过 camera-frame end-effector 表示和 action masking 实现跨具身训练。"
---

## Definition

Action Space Unification is maintained here as an evidence-linked concept. 将不同机器人平台的动作表示统一到固定维度的共享空间，通过 camera-frame end-effector 表示和 action masking 实现跨具身训练。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026joyaira]].
- The concept is tracked with local tags: manipulation, cross-embodiment, VLA.
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

- [[zhang2026joyaira]] (direct evidence): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[wu2025discrete]] (broader context): 提出 Discrete Policy，将连续动作空间解耦为离散潜空间用于多任务机器人操控。三步流程：(1) VQ-VAE 编码器将连续动作序列量化为离散码序列（codeboo...
- [[team2024octo]] (broader context): UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持...
- [[singh2025handobject]] (broader context): 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。

## Evidence Map

- Direct evidence papers: [[zhang2026joyaira]].
- Broader local evidence context: [[zhang2026joyaira]], [[zheng2026pokevla]], [[zhao2026visualtactile]], [[zhang2021dair]], [[wu2025discrete]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[cross-embodiment-transfer]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[zhang2026joyaira]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhang2021dair]]
- [[wu2025discrete]]
- [[team2024octo]]
- [[singh2025handobject]]
- [[niu2026versatile]]
