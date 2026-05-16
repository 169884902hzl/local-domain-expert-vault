---
title: "Classifier-Free Guidance (CFG)"
tags: [diffusion, conditional-generation]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "无需外部分类器的条件引导生成方法，通过同时训练条件和无条件模型，推理时插值两者输出以增强条件一致性。"
---

## Definition

Classifier-Free Guidance (CFG) is maintained here as an evidence-linked concept. 无需外部分类器的条件引导生成方法，通过同时训练条件和无条件模型，推理时插值两者输出以增强条件一致性。

## Key Ideas

- Direct local evidence currently comes from [[chen2026elasticflow]].
- The concept is tracked with local tags: diffusion, conditional-generation.
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

- [[chen2026elasticflow]] (direct evidence): 基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[peters2026coordinated]] (broader context): 提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-an...
- [[park2026acg]] (broader context): 提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造\"不一致向量场\"，再沿反方向引导 flow matching VLA 策略生...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[wu2026contrastive]] (broader context): 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提...

## Evidence Map

- Direct evidence papers: [[chen2026elasticflow]].
- Broader local evidence context: [[chen2026elasticflow]], [[zhang2026touchguide]], [[wang2026discretertc]], [[peters2026coordinated]], [[park2026acg]].
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
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[chen2026elasticflow]]
- [[zhang2026touchguide]]
- [[wang2026discretertc]]
- [[peters2026coordinated]]
- [[park2026acg]]
- [[ziakas2026aligning]]
- [[zhang2026generative]]
- [[wu2026contrastive]]
