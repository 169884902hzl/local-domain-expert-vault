---
title: "Impedance Control"
tags: [control, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "阻抗控制：通过调节末端执行器的刚度与阻尼实现柔顺交互的力控制方法，广泛用于接触丰富的机器人操控任务。"
---

## Definition

Impedance Control is maintained here as an evidence-linked concept. 阻抗控制：通过调节末端执行器的刚度与阻尼实现柔顺交互的力控制方法，广泛用于接触丰富的机器人操控任务。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: control, robot-learning.
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

- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[do2025watch]], [[zhu2024scaling]], [[zhao2025polytouch]], [[zhang2026visionlanguageaction]], [[zhang2026prts]].
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
- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[do2025watch]]
- [[zhu2024scaling]]
- [[zhao2025polytouch]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
