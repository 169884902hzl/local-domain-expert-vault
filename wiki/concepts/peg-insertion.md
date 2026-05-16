---
title: "Peg Insertion"
tags: [manipulation, benchmark]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "销钉插入：经典的接触丰富机器人操控基准任务，要求机器人将圆柱销钉精确插入孔中。"
---

## Definition

Peg Insertion is maintained here as an evidence-linked concept. 销钉插入：经典的接触丰富机器人操控基准任务，要求机器人将圆柱销钉精确插入孔中。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: manipulation, benchmark.
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

- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[wang2023hierarchical]] (broader context): 提出 HCLM（Hierarchical policy for Cluttered-scene Long-horizon Manipulation），视觉层次化策略协调 pu...
- [[tang2025uad]] (broader context): 提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[yan2026tac2real]], [[zhao2026visualtactile]], [[zhao2023finegrained]], [[zhang2026visionlanguageaction]], [[xu2026token]].
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
- [[tactile-sensing]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[yan2026tac2real]]
- [[zhao2026visualtactile]]
- [[zhao2023finegrained]]
- [[zhang2026visionlanguageaction]]
- [[xu2026token]]
- [[wu2025tacdiffusion]]
- [[wang2023hierarchical]]
- [[tang2025uad]]
