---
title: "DPO (Direct Preference Optimization)"
tags: [alignment, training-method, RLHF-alternative]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "直接偏好优化，一种无需显式奖励模型的 RLHF 替代方法，通过对比偏好数据直接优化策略。"
---

## Definition

DPO (Direct Preference Optimization) is maintained here as an evidence-linked concept. 直接偏好优化，一种无需显式奖励模型的 RLHF 替代方法，通过对比偏好数据直接优化策略。

## Key Ideas

- Direct local evidence currently comes from [[chen2026abotphysworld]].
- The concept is tracked with local tags: alignment, training-method, RLHF-alternative.
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

- [[chen2026abotphysworld]] (direct evidence): 基于 Wan2.1 的 14B Diffusion Transformer，通过 300 万物理标注操控视频 SFT + VLM 解耦判别器 DPO 后训练，实现物理一致的可...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线

## Evidence Map

- Direct evidence papers: [[chen2026abotphysworld]].
- Broader local evidence context: [[chen2026abotphysworld]], [[zhu2026nsvla]], [[zhu2024scaling]], [[zhou2026vlbiman]], [[zhou2026sim1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[world-model]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[chen2026abotphysworld]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
- [[zhou2026ego]]
- [[zhou2025oneshot]]
