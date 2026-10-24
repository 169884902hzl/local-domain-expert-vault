---
title: "Discrete Diffusion Policy"
tags: [diffusion, imitation-learning, action-generation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "通过将连续 action 量化为离散 token 并用 iterative unmasking 生成 action chunk 的策略方法。"
---

## Definition

Discrete Diffusion Policy is maintained here as an evidence-linked concept. 通过将连续 action 量化为离散 token 并用 iterative unmasking 生成 action chunk 的策略方法。

## Key Ideas

- Direct local evidence currently comes from [[wang2026discretertc]].
- The concept is tracked with local tags: diffusion, imitation-learning, action-generation.
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

- [[wang2026discretertc]] (direct evidence): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...
- [[scheikl620movement]] (broader context): 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabi...

## Evidence Map

- Direct evidence papers: [[wang2026discretertc]].
- Broader local evidence context: [[wang2026discretertc]], [[wu2025tacdiffusion]], [[zhu2024scaling]], [[zhao2025polytouch]], [[zhang2026generative]].
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
- [[real-time-chunking]]
- [[action-chunking]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026discretertc]]
- [[wu2025tacdiffusion]]
- [[zhu2024scaling]]
- [[zhao2025polytouch]]
- [[zhang2026generative]]
- [[xue2026tube]]
- [[xia2024cage]]
- [[scheikl620movement]]
