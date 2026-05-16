---
title: "Multi-Agent Imitation Learning"
tags: [multi-agent, imitation-learning, coordination]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "多个智能体通过模仿专家示范学习协调行为的模仿学习方法，面临联合状态-动作空间指数增长的数据瓶颈。"
---

## Definition

Multi-Agent Imitation Learning is maintained here as an evidence-linked concept. 多个智能体通过模仿专家示范学习协调行为的模仿学习方法，面临联合状态-动作空间指数增长的数据瓶颈。

## Key Ideas

- Direct local evidence currently comes from [[peters2026coordinated]].
- The concept is tracked with local tags: multi-agent, imitation-learning, coordination.
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

- [[peters2026coordinated]] (direct evidence): 提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-an...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[chen2025coordinated]] (broader context): 将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...

## Evidence Map

- Direct evidence papers: [[peters2026coordinated]].
- Broader local evidence context: [[peters2026coordinated]], [[zhao2026rosclaw]], [[moroncelli2026jumpstart]], [[chen2025coordinated]], [[zhou2026vlbiman]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[coordinated-diffusion]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[peters2026coordinated]]
- [[zhao2026rosclaw]]
- [[moroncelli2026jumpstart]]
- [[chen2025coordinated]]
- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[zhao2025polytouch]]
- [[zhang2026recurrent]]
