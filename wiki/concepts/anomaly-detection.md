---
title: "Anomaly Detection"
tags: [concept, anomaly-detection, unsupervised-learning]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "识别偏离正常行为模式的异常事件，在机器人操控中用于运行时故障检测和干预。"
---

## Definition

Anomaly Detection is maintained here as an evidence-linked concept. 识别偏离正常行为模式的异常事件，在机器人操控中用于运行时故障检测和干预。

## Key Ideas

- Direct local evidence currently comes from [[zhou2026rcnf]].
- The concept is tracked with local tags: concept, anomaly-detection, unsupervised-learning.
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

- [[zhou2026rcnf]] (direct evidence): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[nie820smaller]] (broader context): 提出 KufeNet，通过不等特征编码和知识蒸馏实现 KB 级参数的抓取检测模型。不等并行结构处理 RGB-D（深度分支更多参数），3D 卷积注意力补偿 DSC 相关性损失。...
- [[lips2024keypoints]] (broader context): 提出合成数据管线用于训练衣物关键点检测器。三阶段流程：程序化生成单层 mesh → Nvidia Flex 变形（模拟展开后状态）→ Blender Cycles 渲染。Ma...
- [[li2026realvlgr1]] (broader context): 构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现...
- [[kang2026coenv]] (broader context): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[funk2024evetac]] (broader context): 提出 Evetac 事件相机光学触觉传感器，用事件相机替代传统 RGB 相机实现 1000Hz 标记追踪、高达 498Hz 振动感知和剪切力重建，在滑移检测（97% F1）、...

## Evidence Map

- Direct evidence papers: [[zhou2026rcnf]].
- Broader local evidence context: [[zhou2026rcnf]], [[jeong2026your]], [[you2026dotsim]], [[nie820smaller]], [[lips2024keypoints]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[normalizing-flow]]
- [[runtime-monitoring]]
- [[ood-detection]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhou2026rcnf]]
- [[jeong2026your]]
- [[you2026dotsim]]
- [[nie820smaller]]
- [[lips2024keypoints]]
- [[li2026realvlgr1]]
- [[kang2026coenv]]
- [[funk2024evetac]]
