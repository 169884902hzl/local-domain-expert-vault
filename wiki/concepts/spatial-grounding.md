---
title: "Spatial Grounding"
tags: [vision, VLM, spatial-reasoning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "将自然语言描述与视觉场景中的空间位置/区域建立对应关系的能力，是 embodied VLM 的核心技能之一。"
---

## Definition

Spatial Grounding is maintained here as an evidence-linked concept. 将自然语言描述与视觉场景中的空间位置/区域建立对应关系的能力，是 embodied VLM 的核心技能之一。

## Key Ideas

- Direct local evidence currently comes from [[zheng2026pokevla]].
- The concept is tracked with local tags: vision, VLM, spatial-reasoning.
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

- [[zheng2026pokevla]] (direct evidence): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[tong2024ovalprompt]] (broader context): 提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词...
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[kim2024openvla]] (broader context): Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[garcia2025generalizable]] (broader context): 提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任...

## Evidence Map

- Direct evidence papers: [[zheng2026pokevla]].
- Broader local evidence context: [[zheng2026pokevla]], [[yang2026asyncshield]], [[vo2026codegraphvlp]], [[tong2024ovalprompt]], [[smith2024steer]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[vision-language-action]]
- [[robotic-manipulation]]
- [[affordance-learning]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zheng2026pokevla]]
- [[yang2026asyncshield]]
- [[vo2026codegraphvlp]]
- [[tong2024ovalprompt]]
- [[smith2024steer]]
- [[kim2024openvla]]
- [[jie2026omnivlarl]]
- [[garcia2025generalizable]]
