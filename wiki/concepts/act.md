---
title: "Action Chunking with Transformers (ACT)"
tags: [imitation-learning, transformer, robot-learning]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "基于 Transformer 的模仿学习方法，通过动作分块（action chunking）处理非马尔可夫动力学，广泛用于双臂和灵巧手操控。"
---

## Definition

Action Chunking with Transformers (ACT) is maintained here as an evidence-linked concept. 基于 Transformer 的模仿学习方法，通过动作分块（action chunking）处理非马尔可夫动力学，广泛用于双臂和灵巧手操控。

## Key Ideas

- Direct local evidence currently comes from [[li2026h2r]].
- The concept is tracked with local tags: imitation-learning, transformer, robot-learning.
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

- [[li2026h2r]] (direct evidence): H2R 通过 HaMeR+SAM+LaMa 管线将第一人称人类手部视频替换为机器人手臂渲染帧，缩小人机视觉域差异，在仿真和真实双臂/灵巧手操控任务上实现 1.3%-23.3%...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。

## Evidence Map

- Direct evidence papers: [[li2026h2r]].
- Broader local evidence context: [[li2026h2r]], [[zhu2024scaling]], [[zhou2026vlbiman]], [[zhou2026sim1]], [[zhou2026ego]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[diffusion-policy]]
- [[bimanual-manipulation]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[li2026h2r]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
