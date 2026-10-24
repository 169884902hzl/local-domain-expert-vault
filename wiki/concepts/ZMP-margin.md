---
title: "ZMP Margin (Zero Moment Point Margin)"
tags: [stability, locomotion, dynamics]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "零矩点到支撑多边形中心的归一化距离误差，用于评估运动控制策略的动态稳定性。"
---

## Definition

ZMP Margin (Zero Moment Point Margin) is maintained here as an evidence-linked concept. 零矩点到支撑多边形中心的归一化距离误差，用于评估运动控制策略的动态稳定性。

## Key Ideas

- Direct local evidence currently comes from [[wu2026reliable]].
- The concept is tracked with local tags: stability, locomotion, dynamics.
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

- [[wu2026reliable]] (direct evidence): 提出 MoE-CTS 统一框架，将 Mixture-of-Experts 集成到学生编码器以增强多地形表征，并设计 RoboGauge 预测评估套件，通过 sim-to-si...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[wu2026reliable]].
- Broader local evidence context: [[wu2026reliable]], [[yin2026multiple]], [[he2026generative]], [[ziakas2026aligning]], [[zhu2026nsvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[domain-randomization]]
- [[pomdp]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wu2026reliable]]
- [[yin2026multiple]]
- [[he2026generative]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
