---
title: "Generalized Advantage Estimation"
tags: [concept, RL, advantage]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "通过指数加权的 TD residual 之和估计 advantage，平衡 bias 和 variance 的 on-policy 估计方法"
---

## Definition

Generalized Advantage Estimation is maintained here as an evidence-linked concept. 通过指数加权的 TD residual 之和估计 advantage，平衡 bias 和 variance 的 on-policy 估计方法

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: concept, RL, advantage.
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

- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[wang2026while]] (broader context): 提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机...
- [[wang2026phys2real]] (broader context): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...
- [[sagar2026robomd]] (broader context): 提出 RoboMD 框架，在视觉-语言语义嵌入空间中用深度 RL 策略主动搜索操控策略的失败诱发变体，比 VLM baseline 多发现 23% 的独特漏洞，并用发现的漏洞...
- [[liu2025autonomous]] (broader context): 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL...
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[yang2026rise]], [[zhang2026recurrent]], [[wang2026while]], [[wang2026phys2real]], [[sagar2026robomd]].
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
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[yang2026rise]]
- [[zhang2026recurrent]]
- [[wang2026while]]
- [[wang2026phys2real]]
- [[sagar2026robomd]]
- [[liu2025autonomous]]
- [[li2026affordsim]]
- [[lee2026implicit]]
