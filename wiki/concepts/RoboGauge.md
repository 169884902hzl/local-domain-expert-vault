---
title: "RoboGauge"
tags: [sim-to-real, evaluation, locomotion]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "基于 MuJoCo 的 sim-to-sim 预测评估框架，通过 6 个本体感觉指标量化四足运动策略的 Sim-to-Real 可迁移性。"
---

## Definition

RoboGauge is maintained here as an evidence-linked concept. 基于 MuJoCo 的 sim-to-sim 预测评估框架，通过 6 个本体感觉指标量化四足运动策略的 Sim-to-Real 可迁移性。

## Key Ideas

- Direct local evidence currently comes from [[wu2026reliable]].
- The concept is tracked with local tags: sim-to-real, evaluation, locomotion.
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
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yin2026genie]] (broader context): Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 100...

## Evidence Map

- Direct evidence papers: [[wu2026reliable]].
- Broader local evidence context: [[wu2026reliable]], [[zhou2026sim1]], [[zhou2025oneshot]], [[zhao2026vitactracing]], [[zhao2026rosclaw]].
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
- [[domain-randomization]]
- [[mixture-of-experts]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wu2026reliable]]
- [[zhou2026sim1]]
- [[zhou2025oneshot]]
- [[zhao2026vitactracing]]
- [[zhao2026rosclaw]]
- [[yu2026atrs]]
- [[you2026dotsim]]
- [[yin2026genie]]
