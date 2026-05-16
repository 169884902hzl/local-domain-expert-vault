---
title: "Open-Vocabulary Navigation（开放词汇导航）"
tags: [navigation, vlm, zero-shot]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "机器人导航到任意自然语言描述的目标，不限于预定义的物体类别集合。"
---

## Definition

Open-Vocabulary Navigation（开放词汇导航） is maintained here as an evidence-linked concept. 机器人导航到任意自然语言描述的目标，不限于预定义的物体类别集合。

## Key Ideas

- Direct local evidence currently comes from [[tan2026fsunav]].
- The concept is tracked with local tags: navigation, vlm, zero-shot.
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

- [[tan2026fsunav]] (direct evidence): 提出 Cerebrum-Cerebellum 双层架构实现零样本目标导航：Cerebellum 基于 DRL 的维度可配置局部规划器实现跨平台避障，Cerebrum 以 VL...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[tong2024ovalprompt]] (broader context): 提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词...
- [[singh2025intellirms]] (broader context): 提出 IntelliRMS，基于 LLM+VLM 的端到端工业机器人操控系统架构。核心组件：(1) General Perception（Mask R-CNN 开放词汇检测）...
- [[shen2026plan]] (broader context): 提出 SAGE 框架，通过物理沙盒生成合成经验（Genesis）、非对称自适应裁剪 RL 训练（Evolution）、检索增强导航（Navigation）三阶段，将 VLM...
- [[narendra2026knowledgeguided]] (broader context): 提出KG-M3PO框架，将在线3D场景图（动态更新空间/包含/可供性关系）通过GNN编码器端到端融入M3PO强化学习训练循环，在部分可观测的多任务机械臂操控中显著优于纯视觉基...
- [[liu2025kuda]] (broader context): 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为...

## Evidence Map

- Direct evidence papers: [[tan2026fsunav]].
- Broader local evidence context: [[tan2026fsunav]], [[zhi2025closedloop]], [[yin2026multiple]], [[tong2024ovalprompt]], [[singh2025intellirms]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-navigation]]
- [[vision-language-model]]
- [[spatial-grounding]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[tan2026fsunav]]
- [[zhi2025closedloop]]
- [[yin2026multiple]]
- [[tong2024ovalprompt]]
- [[singh2025intellirms]]
- [[shen2026plan]]
- [[narendra2026knowledgeguided]]
- [[liu2025kuda]]
