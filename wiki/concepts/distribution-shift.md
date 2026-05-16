---
title: "Distribution Shift"
tags: [imitation-learning, generalization, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "训练数据分布与实际部署时遇到的分布不一致的问题，在模仿学习/VLA post-training 中导致复合误差累积。"
---

## Definition

Distribution Shift is maintained here as an evidence-linked concept. 训练数据分布与实际部署时遇到的分布不一致的问题，在模仿学习/VLA post-training 中导致复合误差累积。

## Key Ideas

- Direct local evidence currently comes from [[zhong2026vlaopd]].
- The concept is tracked with local tags: imitation-learning, generalization, robot-learning.
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

- [[zhong2026vlaopd]] (direct evidence): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[qi2026compose]] (broader context): 提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Polic...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[lee2025diffdagger]] (broader context): 提出 Diff-DAgger，利用扩散策略训练目标（diffusion loss）作为不确定性估计器实现 robot-gated DAgger。核心洞察：扩散 loss 在...

## Evidence Map

- Direct evidence papers: [[zhong2026vlaopd]].
- Broader local evidence context: [[zhong2026vlaopd]], [[xie2026humanintention]], [[qi2026compose]], [[zhu2024scaling]], [[ye2026generation]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[on-policy-distillation]]
- [[imitation-learning]]
- [[catastrophic-forgetting]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[zhong2026vlaopd]]
- [[xie2026humanintention]]
- [[qi2026compose]]
- [[zhu2024scaling]]
- [[ye2026generation]]
- [[sakamoto2026e3vsbench]]
- [[liu2026longhorizon]]
- [[lee2025diffdagger]]
