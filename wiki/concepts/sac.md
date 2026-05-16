---
title: "Soft Actor-Critic (SAC)"
tags: [concept, reinforcement-learning, policy-optimization]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "基于最大熵的 off-policy actor-critic 算法，通过鼓励策略随机性提升探索和鲁棒性，广泛用于连续控制任务。"
---

## Definition

Soft Actor-Critic (SAC) is maintained here as an evidence-linked concept. 基于最大熵的 off-policy actor-critic 算法，通过鼓励策略随机性提升探索和鲁棒性，广泛用于连续控制任务。

## Key Ideas

- Direct local evidence currently comes from [[saad2026hybrid]].
- The concept is tracked with local tags: concept, reinforcement-learning, policy-optimization.
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

- [[saad2026hybrid]] (direct evidence): 提出 LLM 高层任务规划 + RL 低层控制的混合框架，在 PyBullet 仿真中用 Franka Panda 实现了比纯 RL 方法快 33.5% 的任务完成时间和更高...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[ryu2025curricullm]] (broader context): 提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curr...
- [[li2025routing]] (broader context): 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle...
- [[huang2025match]] (broader context): 提出 MATCH POLICY，将操控 pick-place 策略转化为点云配准任务。核心流程：存储演示中的组合点云 Pab（pick/place 配置），推理时通过 RAN...
- [[gao2026driftbased]] (broader context): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...

## Evidence Map

- Direct evidence papers: [[saad2026hybrid]].
- Broader local evidence context: [[saad2026hybrid]], [[zhao2026visualtactile]], [[zhang2021dair]], [[wu2025rlgsbridge]], [[ryu2025curricullm]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[ppo]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[saad2026hybrid]]
- [[zhao2026visualtactile]]
- [[zhang2021dair]]
- [[wu2025rlgsbridge]]
- [[ryu2025curricullm]]
- [[li2025routing]]
- [[huang2025match]]
- [[gao2026driftbased]]
