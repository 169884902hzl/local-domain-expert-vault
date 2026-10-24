---
title: "沙盒仿真"
tags: [sim-to-real, embodied-navigation, data-synthesis]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "使用物理约束的语义抽象环境（非真实感仿真）进行数据合成和策略训练的方法，强调场景语义结构而非视觉真实感。"
---

## Definition

沙盒仿真 is maintained here as an evidence-linked concept. 使用物理约束的语义抽象环境（非真实感仿真）进行数据合成和策略训练的方法，强调场景语义结构而非视觉真实感。

## Key Ideas

- Direct local evidence currently comes from [[shen2026plan]].
- The concept is tracked with local tags: sim-to-real, embodied-navigation, data-synthesis.
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
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yin2026genie]] (broader context): Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 100...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...

## Evidence Map

- Direct evidence papers: [[shen2026plan]].
- Broader local evidence context: [[shen2026plan]], [[zhou2026sim1]], [[zhou2025oneshot]], [[yu2026atrs]], [[you2026dotsim]].
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
- [[experience-driven-learning]]
- [[semantic-scene-graph]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[shen2026plan]]
- [[zhou2026sim1]]
- [[zhou2025oneshot]]
- [[yu2026atrs]]
- [[you2026dotsim]]
- [[yin2026genie]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
