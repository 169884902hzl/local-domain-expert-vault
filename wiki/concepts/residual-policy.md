---
title: "残差策略"
tags: [RL, policy-learning, trajectory-adaptation]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "RL策略学习对名义轨迹的残差修正，而非从零学习完整动作策略，降低学习难度并提高数据效率。"
---

## Definition

残差策略 is maintained here as an evidence-linked concept. RL策略学习对名义轨迹的残差修正，而非从零学习完整动作策略，降低学习难度并提高数据效率。

## Key Ideas

- Direct local evidence currently comes from [[yang2026automated]].
- The concept is tracked with local tags: RL, policy-learning, trajectory-adaptation.
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
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[sha2026efficient]] (broader context): 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...

## Evidence Map

- Direct evidence papers: [[yang2026automated]].
- Broader local evidence context: [[yang2026automated]], [[you2026dotsim]], [[sha2026efficient]], [[marougkas2025integrating]], [[zhou2026ego]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[multi-material-cutting]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[yang2026automated]]
- [[you2026dotsim]]
- [[sha2026efficient]]
- [[marougkas2025integrating]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhang2026recurrent]]
