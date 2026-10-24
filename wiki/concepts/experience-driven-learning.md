---
title: "生成式经验驱动学习"
tags: [rl, vlm, embodied-navigation, sim-to-real]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "通过在物理沙盒中自主合成任务和经验规则，将 VLM 高层推理蒸馏为低层策略的 RL 训练范式。"
---

## Definition

生成式经验驱动学习 is maintained here as an evidence-linked concept. 通过在物理沙盒中自主合成任务和经验规则，将 VLM 高层推理蒸馏为低层策略的 RL 训练范式。

## Key Ideas

- Direct local evidence currently comes from [[shen2026plan]].
- The concept is tracked with local tags: rl, vlm, embodied-navigation, sim-to-real.
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

- [[shen2026plan]] (direct evidence): 提出 SAGE 框架，通过物理沙盒生成合成经验（Genesis）、非对称自适应裁剪 RL 训练（Evolution）、检索增强导航（Navigation）三阶段，将 VLM...
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...
- [[sha2026efficient]] (broader context): 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。

## Evidence Map

- Direct evidence papers: [[shen2026plan]].
- Broader local evidence context: [[shen2026plan]], [[xu2026twinrlvla]], [[sha2026efficient]], [[zhou2026sim1]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[sim-to-real]]
- [[reinforcement-learning]]
- [[vision-language-model]]
- [[grpo]]
- [[asymmetric-adaptive-clipping]]
- [[robotic-manipulation]]

## Related Papers

- [[shen2026plan]]
- [[xu2026twinrlvla]]
- [[sha2026efficient]]
- [[zhou2026sim1]]
- [[zhou2025oneshot]]
- [[zhao2026vitactracing]]
- [[zhao2026rosclaw]]
- [[yu2026atrs]]
