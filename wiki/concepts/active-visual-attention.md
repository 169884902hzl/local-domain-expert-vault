---
title: "Active Visual Attention"
tags: [visual-attention, VLA, robotics]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "基于历史上下文动态重加权视觉 token 的注意力机制，使 VLA 模型能主动聚焦于任务相关视觉区域。"
---

## Definition

Active Visual Attention is maintained here as an evidence-linked concept. 基于历史上下文动态重加权视觉 token 的注意力机制，使 VLA 模型能主动聚焦于任务相关视觉区域。

## Key Ideas

- Direct local evidence currently comes from [[xiao2026avavla]].
- The concept is tracked with local tags: visual-attention, VLA, robotics.
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

- [[xiao2026avavla]] (direct evidence): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[nazarczuk2025closed]] (broader context): 提出 CLIER 闭环交互式具身推理框架：神经符号方法处理需要视觉+物理属性测量的长时序操控任务。Seq2Seq 语言→符号程序→场景图→Transformer 动作规划器→...
- [[keunknowndiffuser]] (broader context): 提出 3D Diffuser Actor，统一 3D 场景表示与扩散目标用于模仿学习。核心是 3D 相对去噪 Transformer：将 RGB-D 图像提升为 3D 场景...

## Evidence Map

- Direct evidence papers: [[xiao2026avavla]].
- Broader local evidence context: [[xiao2026avavla]], [[zhao2025polytouch]], [[ye2026generation]], [[xue2026tube]], [[xia2024cage]].
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
- [[pomdp]]
- [[film]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[xiao2026avavla]]
- [[zhao2025polytouch]]
- [[ye2026generation]]
- [[xue2026tube]]
- [[xia2024cage]]
- [[sakamoto2026e3vsbench]]
- [[nazarczuk2025closed]]
- [[keunknowndiffuser]]
