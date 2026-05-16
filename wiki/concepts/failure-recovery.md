---
title: "Failure Recovery"
tags: [concept, manipulation, planning]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "机器人在执行任务时自动检测失败并恢复执行的机制，对长时序操控至关重要。"
---

## Definition

Failure Recovery is maintained here as an evidence-linked concept. 机器人在执行任务时自动检测失败并恢复执行的机制，对长时序操控至关重要。

## Key Ideas

- Direct local evidence currently comes from [[li2026hierarchical]].
- The concept is tracked with local tags: concept, manipulation, planning.
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

- [[li2026hierarchical]] (direct evidence): 提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[levy2026simulation]] (broader context): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[dai2024racer]] (broader context): 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GP...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...

## Evidence Map

- Direct evidence papers: [[li2026hierarchical]].
- Broader local evidence context: [[li2026hierarchical]], [[liu2026longhorizon]], [[levy2026simulation]], [[aida2026cortex]], [[zhi2025closedloop]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[long-horizon-manipulation]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[planning]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[li2026hierarchical]]
- [[liu2026longhorizon]]
- [[levy2026simulation]]
- [[aida2026cortex]]
- [[zhi2025closedloop]]
- [[zeng2026recapa]]
- [[dai2024racer]]
- [[zhou2026rcnf]]
