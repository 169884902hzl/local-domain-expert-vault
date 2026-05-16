---
title: "Asynchronous Execution"
tags: [manipulation, control, action-chunking]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "机器人在策略推理期间持续执行动作的执行模式，是动态操控任务的结构性要求。"
---

## Definition

Asynchronous Execution is maintained here as an evidence-linked concept. 机器人在策略推理期间持续执行动作的执行模式，是动态操控任务的结构性要求。

## Key Ideas

- Direct local evidence currently comes from [[wang2026discretertc]].
- The concept is tracked with local tags: manipulation, control, action-chunking.
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
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[styrud2025automatic]] (broader context): 提出 BETR-XP-LLM 方法，结合 LLM 和任务规划器自动生成和扩展行为树（BT）作为机器人操控策略。两阶段：(1) LLM 将自然语言目标解释为形式化目标条件 →...
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...

## Evidence Map

- Direct evidence papers: [[wang2026discretertc]].
- Broader local evidence context: [[wang2026discretertc]], [[zhi2025closedloop]], [[zhang2026visionlanguageaction]], [[xue2026tube]], [[styrud2025automatic]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-chunking]]
- [[real-time-chunking]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026discretertc]]
- [[zhi2025closedloop]]
- [[zhang2026visionlanguageaction]]
- [[xue2026tube]]
- [[styrud2025automatic]]
- [[qiu2025wildlma]]
- [[liu2026longhorizon]]
- [[liu2025forcemimic]]
