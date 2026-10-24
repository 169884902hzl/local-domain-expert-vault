---
title: "Slot Attention"
tags: [representation-learning, object-centric, attention]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "一种将场景分解为可组合对象表征的注意力机制，通过竞争性交叉注意力让每个slot绑定到不同物体。"
---

## Definition

Slot Attention is maintained here as an evidence-linked concept. 一种将场景分解为可组合对象表征的注意力机制，通过竞争性交叉注意力让每个slot绑定到不同物体。

## Key Ideas

- Direct local evidence currently comes from [[spieler2026slotmpc]].
- The concept is tracked with local tags: representation-learning, object-centric, attention.
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

- [[spieler2026slotmpc]] (direct evidence): 提出Slot-MPC，将基于Slot Attention的对象中心表征（SAVi）与可微分世界模型（cOCVP）结合，通过梯度优化MPC在紧凑的对象级隐空间中进行目标条件规划...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...

## Evidence Map

- Direct evidence papers: [[spieler2026slotmpc]].
- Broader local evidence context: [[spieler2026slotmpc]], [[zhu2024scaling]], [[zheng2026pokevla]], [[zhao2025polytouch]], [[zhao2023finegrained]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[world-model]]
- [[model-predictive-control]]
- [[savi]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[spieler2026slotmpc]]
- [[zhu2024scaling]]
- [[zheng2026pokevla]]
- [[zhao2025polytouch]]
- [[zhao2023finegrained]]
- [[zhang2021dair]]
- [[yang2026ultradexgrasp]]
- [[yang2026hivla]]
