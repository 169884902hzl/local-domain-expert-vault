---
title: "Spatial Generalization"
tags: [generalization, manipulation, policy-learning]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "空间泛化指视觉运动策略在物体、环境和机器人自身不同空间分布下稳健工作的能力，是机器人操控中最基本也最耗数据的泛化维度。"
---

## Definition

Spatial Generalization is maintained here as an evidence-linked concept. 空间泛化指视觉运动策略在物体、环境和机器人自身不同空间分布下稳健工作的能力，是机器人操控中最基本也最耗数据的泛化维度。

## Key Ideas

- Direct local evidence currently comes from [[xu2026r2rgen]].
- The concept is tracked with local tags: generalization, manipulation, policy-learning.
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

- [[xu2026r2rgen]] (direct evidence): 提出无需仿真器的 real-to-real 3D 数据生成框架 R2RGen，通过 group-wise 回溯增强和 camera-aware 后处理，用 1 次人类示范即可...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[wang2023multistage]] (broader context): 提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1)...
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[niu2026boosting]] (broader context): 提出Feasible Action Neighborhood (FAN)引导的正则化方法，用高斯先验约束VLA策略分布形状，在SFT和RFT（PPO）两种微调范式中均显著提升...
- [[narendra2026knowledgeguided]] (broader context): 提出KG-M3PO框架，将在线3D场景图（动态更新空间/包含/可供性关系）通过GNN编码器端到端融入M3PO强化学习训练循环，在部分可观测的多任务机械臂操控中显著优于纯视觉基...
- [[jin2026grounding]] (broader context): 系统性实证研究VLA模型零样本Sim-to-Real迁移的四维因子（域随机化、渲染保真度、物理真实度、RL微调），基于10k+真实世界试验得出五个关键结论：空间随机化主导迁移...

## Evidence Map

- Direct evidence papers: [[xu2026r2rgen]].
- Broader local evidence context: [[xu2026r2rgen]], [[yuan2026embodiedr1]], [[wang2023multistage]], [[tu2026embody4d]], [[sun2026maniparena]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[data-augmentation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[xu2026r2rgen]]
- [[yuan2026embodiedr1]]
- [[wang2023multistage]]
- [[tu2026embody4d]]
- [[sun2026maniparena]]
- [[niu2026boosting]]
- [[narendra2026knowledgeguided]]
- [[jin2026grounding]]
