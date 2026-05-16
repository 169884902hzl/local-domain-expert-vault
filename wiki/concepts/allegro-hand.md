---
title: "Allegro Hand"
tags: [dexterous-manipulation, hardware, benchmark]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "Wonik Robotics 生产的 4 指 16 DOF 灵巧手，广泛用作灵巧操控和接触丰富控制研究的基准平台。"
---

## Definition

Allegro Hand is maintained here as an evidence-linked concept. Wonik Robotics 生产的 4 指 16 DOF 灵巧手，广泛用作灵巧操控和接触丰富控制研究的基准平台。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: dexterous-manipulation, hardware, benchmark.
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

- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[singh2025handobject]] (broader context): 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目...
- [[park2026demodiffusion]] (broader context): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[li2026impact]] (broader context): 提出 IMPACT 方法，基于保护增广拉格朗日 (safeguarded AuLa) 框架求解 MPCC 形式的接触隐式轨迹优化，通过隐式接触分支选择在迭代中自动发现接触模式...
- [[guzey2025bridging]] (broader context): 提出 HUDOR 框架，通过物体导向的点追踪奖励实现从单个人类视频到多指灵巧手策略的在线微调。核心流程：(1) VR 头显采集人类手指尖轨迹并转换到机器人坐标系；(2) 利用...
- [[chen2025vegetable]] (broader context): 提出约束灵巧操控框架，用 Allegro 手在 Franka 臂上通过 RL 学习可控停止的蔬菜重定向策略，实现重定向→牢固握持→削皮的多步骤循环，4 种蔬菜上 90% 牢固...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zheng120dottip]], [[singh2025handobject]], [[park2026demodiffusion]], [[li2026impact]], [[guzey2025bridging]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[dexterous-grasping]]
- [[contact-implicit-trajectory-optimization]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zheng120dottip]]
- [[singh2025handobject]]
- [[park2026demodiffusion]]
- [[li2026impact]]
- [[guzey2025bridging]]
- [[chen2025vegetable]]
- [[zhu2024scaling]]
- [[zhang2026visionlanguageaction]]
