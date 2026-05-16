---
title: "Transparent Object Manipulation"
tags: [manipulation, vision, transparent-objects]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "透明物体操控是机器人操控中的视觉感知挑战，透明/反光材质导致深度估计和边界检测不稳定。"
---

## Definition

Transparent Object Manipulation is maintained here as an evidence-linked concept. 透明物体操控是机器人操控中的视觉感知挑战，透明/反光材质导致深度估计和边界检测不稳定。

## Key Ideas

- Direct local evidence currently comes from [[du2026bioprovlaagent]].
- The concept is tracked with local tags: manipulation, vision, transparent-objects.
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

- [[du2026bioprovlaagent]] (direct evidence): 提出基于 VLA 的低成本（$800-850）生物实验室多 Agent 闭环系统，通过 LLM 协议解析、VLM-RAG 状态验证和在线数据增强（AugSmolVLA）实现...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...

## Evidence Map

- Direct evidence papers: [[du2026bioprovlaagent]].
- Broader local evidence context: [[du2026bioprovlaagent]], [[zhou2026vlbiman]], [[zhou2026sim1]], [[zhou2026rcnf]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[vision-language-action-model]]
- [[domain-randomization]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[du2026bioprovlaagent]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
- [[zhou2025oneshot]]
- [[zhong2026vlaopd]]
- [[zhi2025closedloop]]
- [[zhao2026vitactracing]]
