---
title: "多材料切割"
tags: [robotic-cutting, multi-material, deformation]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "机器人对由多种不同物理属性材料组成的物体进行切割，需要处理材料耦合、断裂和接触力差异。"
---

## Definition

多材料切割 is maintained here as an evidence-linked concept. 机器人对由多种不同物理属性材料组成的物体进行切割，需要处理材料耦合、断裂和接触力差异。

## Key Ideas

- Direct local evidence currently comes from [[yang2026automated]].
- The concept is tracked with local tags: robotic-cutting, multi-material, deformation.
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

- [[yang2026automated]] (direct evidence): 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...

## Evidence Map

- Direct evidence papers: [[yang2026automated]].
- Broader local evidence context: [[yang2026automated]], [[shah2025acoustic]], [[niu2026versatile]], [[luijkx2026llmguided]], [[zhu2024scaling]].
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
- [[reinforcement-learning]]
- [[collision-avoidance]]
- [[residual-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[yang2026automated]]
- [[shah2025acoustic]]
- [[niu2026versatile]]
- [[luijkx2026llmguided]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[zhi2025closedloop]]
