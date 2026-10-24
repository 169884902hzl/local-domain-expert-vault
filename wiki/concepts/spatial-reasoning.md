---
title: "Spatial Reasoning"
tags: [spatial-reasoning, VLM, embodied-AI]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "空间推理：理解和推理物体间的几何关系、空间布局和相对位置的能力。"
---

## Definition

Spatial Reasoning is maintained here as an evidence-linked concept. 空间推理：理解和推理物体间的几何关系、空间布局和相对位置的能力。

## Key Ideas

- Direct local evidence currently comes from [[zhou2026ego]].
- The concept is tracked with local tags: spatial-reasoning, VLM, embodied-AI.
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

- [[zhou2026ego]] (direct evidence): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[wang2026vlathinker]] (broader context): 首个\"thinking-with-image\"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRP...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[kang2026coenv]] (broader context): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...

## Evidence Map

- Direct evidence papers: [[zhou2026ego]].
- Broader local evidence context: [[zhou2026ego]], [[zheng2026pokevla]], [[yuan2026embodiedr1]], [[yin2026multiple]], [[wang2026vlathinker]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[cross-view-reasoning]]
- [[vision-language-model]]
- [[grasping]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[zhou2026ego]]
- [[zheng2026pokevla]]
- [[yuan2026embodiedr1]]
- [[yin2026multiple]]
- [[wang2026vlathinker]]
- [[sun2026maniparena]]
- [[kang2026coenv]]
- [[jie2026omnivlarl]]
