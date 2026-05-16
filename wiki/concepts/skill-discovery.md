---
title: "Skill Discovery"
tags: [concept, unsupervised-learning, rl]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "无监督地发现和习得多种可区分行为的方法，通常通过最大化潜变量与状态/轨迹的互信息。"
---

## Definition

Skill Discovery is maintained here as an evidence-linked concept. 无监督地发现和习得多种可区分行为的方法，通常通过最大化潜变量与状态/轨迹的互信息。

## Key Ideas

- Direct local evidence currently comes from [[longhini2026behavioral]].
- The concept is tracked with local tags: concept, unsupervised-learning, rl.
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

- [[longhini2026behavioral]] (direct evidence): 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[xu2026r2rgen]] (broader context): 提出无需仿真器的 real-to-real 3D 数据生成框架 R2RGen，通过 group-wise 回溯增强和 camera-aware 后处理，用 1 次人类示范即可...

## Evidence Map

- Direct evidence papers: [[longhini2026behavioral]].
- Broader local evidence context: [[longhini2026behavioral]], [[wu2026continually]], [[zhou2026vlbiman]], [[zhao2026visualtactile]], [[zhao2026rosclaw]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[behavioral-mode-discovery]]
- [[multimodal-policy]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[longhini2026behavioral]]
- [[wu2026continually]]
- [[zhou2026vlbiman]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[yang2026hivla]]
- [[xu2026token]]
- [[xu2026r2rgen]]
