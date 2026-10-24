---
title: "Perturbation Guidance"
tags: [diffusion, guidance, generative-model]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "通过故意退化模型（扰动 attention/dropout）构造低质量生成方向，沿反方向引导采样以提升输出质量，无需额外训练。"
---

## Definition

Perturbation Guidance is maintained here as an evidence-linked concept. 通过故意退化模型（扰动 attention/dropout）构造低质量生成方向，沿反方向引导采样以提升输出质量，无需额外训练。

## Key Ideas

- Direct local evidence currently comes from [[park2026acg]].
- The concept is tracked with local tags: diffusion, guidance, generative-model.
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

- [[park2026acg]] (direct evidence): 提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造\"不一致向量场\"，再沿反方向引导 flow matching VLA 策略生...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...

## Evidence Map

- Direct evidence papers: [[park2026acg]].
- Broader local evidence context: [[park2026acg]], [[zhang2026touchguide]], [[wang2026discretertc]], [[zheng2026pokevla]], [[zhu2024scaling]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-coherence]]
- [[classifier-guidance]]
- [[flow-matching-policy]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[park2026acg]]
- [[zhang2026touchguide]]
- [[wang2026discretertc]]
- [[zheng2026pokevla]]
- [[zhu2024scaling]]
- [[zhao2025polytouch]]
- [[zhang2026generative]]
- [[xue2026tube]]
