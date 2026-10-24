---
title: "Contact Curriculum"
tags: [reinforcement-learning, dexterous-manipulation, reward-shaping]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "训练课程学习策略，初期禁用工具与外部表面的接触，让策略先在自由空间学会轨迹跟踪，再逐步引入接触动力学"
---

## Definition

Contact Curriculum is maintained here as an evidence-linked concept. 训练课程学习策略，初期禁用工具与外部表面的接触，让策略先在自由空间学会轨迹跟踪，再逐步引入接触动力学

## Key Ideas

- Direct local evidence currently comes from [[fang2026dexdrummer]].
- The concept is tracked with local tags: reinforcement-learning, dexterous-manipulation, reward-shaping.
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

- [[fang2026dexdrummer]] (direct evidence): 提出分层式灵巧鼓手机器人框架 DexDrummer，高层用参数化运动基元+残差 RL 实现鼓棒轨迹跟踪，低层用接触靶向奖励（指尖接触、支点奖励、手臂能量惩罚、接触课程）训练手...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: [[fang2026dexdrummer]].
- Broader local evidence context: [[fang2026dexdrummer]], [[marougkas2025integrating]], [[zhou2026sim1]], [[zhou2025oneshot]], [[zheng120dottip]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reward-shaping]]
- [[reinforcement-learning]]
- [[contact-rich-manipulation]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[fang2026dexdrummer]]
- [[marougkas2025integrating]]
- [[zhou2026sim1]]
- [[zhou2025oneshot]]
- [[zheng120dottip]]
- [[zhao2026vitactracing]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
