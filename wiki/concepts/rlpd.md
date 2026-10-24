---
title: "RLPD"
tags: [reinforcement-learning, off-policy, sample-efficient]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "RLPD 是一种面向真实世界 RL 的 off-policy 方法，通过激进复用离线和在线数据提高样本效率。"
---

## Definition

RLPD is maintained here as an evidence-linked concept. RLPD 是一种面向真实世界 RL 的 off-policy 方法，通过激进复用离线和在线数据提高样本效率。

## Key Ideas

- Direct local evidence currently comes from [[levy2026simulation]].
- The concept is tracked with local tags: reinforcement-learning, off-policy, sample-efficient.
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

- [[levy2026simulation]] (direct evidence): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线

## Evidence Map

- Direct evidence papers: [[levy2026simulation]].
- Broader local evidence context: [[levy2026simulation]], [[zhu2026nsvla]], [[zhu2024scaling]], [[zhou2026vlbiman]], [[zhou2026sim1]].
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
- [[online-fine-tuning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[levy2026simulation]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
- [[zhou2026ego]]
- [[zhou2025oneshot]]
