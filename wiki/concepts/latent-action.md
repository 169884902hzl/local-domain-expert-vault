---
title: "Latent Action"
tags: [action-representation, VLA, video-learning]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "从人类视频中学习无需动作标注的隐式动作表征，作为 Vision-Language-Action 模型的关键桥梁。"
---

## Definition

Latent Action is maintained here as an evidence-linked concept. 从人类视频中学习无需动作标注的隐式动作表征，作为 Vision-Language-Action 模型的关键桥梁。

## Key Ideas

- Direct local evidence currently comes from [[ma2026human]].
- The concept is tracked with local tags: action-representation, VLA, video-learning.
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

- [[ma2026human]] (direct evidence): 系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[chen2026lastr1]] (broader context): 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线

## Evidence Map

- Direct evidence papers: [[ma2026human]].
- Broader local evidence context: [[ma2026human]], [[xie2026humanintention]], [[niu2026versatile]], [[gu2026vistabot]], [[chen2026lastr1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[human-video-learning]]
- [[imitation-learning]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[ma2026human]]
- [[xie2026humanintention]]
- [[niu2026versatile]]
- [[gu2026vistabot]]
- [[chen2026lastr1]]
- [[aida2026cortex]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
