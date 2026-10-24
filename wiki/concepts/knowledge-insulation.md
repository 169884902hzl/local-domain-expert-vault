---
title: "知识隔离 (Knowledge Insulation)"
tags: [VLA, robot-learning, representation-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "通过 read-only KV transfer 防止下游任务梯度覆盖上游预训练表示的技术，用于多阶段 VLA 训练。"
---

## Definition

知识隔离 (Knowledge Insulation) is maintained here as an evidence-linked concept. 通过 read-only KV transfer 防止下游任务梯度覆盖上游预训练表示的技术，用于多阶段 VLA 训练。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: VLA, robot-learning, representation-learning.
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

- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[li2026gazevla]] (broader context): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...
- [[brohan2023rt2]] (broader context): Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zheng2026pokevla]], [[xu2026token]], [[li2026gazevla]], [[do2025watch]], [[brohan2023rt2]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[flow-matching]]
- [[mixture-of-transformers]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[zheng2026pokevla]]
- [[xu2026token]]
- [[li2026gazevla]]
- [[do2025watch]]
- [[brohan2023rt2]]
- [[zhu2024scaling]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
