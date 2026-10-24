---
title: "Mixture of Experts"
tags: [moe, routing, expert-selection, scalable-models]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "通过路由机制在多个专家子网络中选择性激活，实现参数共享与任务特化的平衡架构。"
---

## Definition

Mixture of Experts is maintained here as an evidence-linked concept. 通过路由机制在多个专家子网络中选择性激活，实现参数共享与任务特化的平衡架构。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: moe, routing, expert-selection, scalable-models.
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

- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[li2026forcevla2]] (broader context): ForceVLA2 在 VLA 框架中引入 force prompt 驱动的长时推理和 Cross-Scale MoE 实现混合力-位姿控制，在5个接触丰富任务上平均成功率6...
- [[jie2026omnivlarl]] (broader context): 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE...
- [[hartz2024art]] (broader context): 提出 TPGMM 的三重改进用于长时序操控的少样本模仿学习：(1) Riemannian 速度因式分解，将末端执行器速度分解为方向（流形上的 von Mises-Fisher...
- [[antonova2021bayesian]] (broader context): 提出 BayesSim-RKHS，将可变形物体关键点视为状态分布的样本，用 RKHS 核均值嵌入实现置换不变表示，结合 BayesSim 进行仿真参数后验推断。在擦桌布、绳绕...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[xie2026humanintention]], [[li2026forcevla2]], [[jie2026omnivlarl]], [[hartz2024art]], [[antonova2021bayesian]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[continual-learning]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[xie2026humanintention]]
- [[li2026forcevla2]]
- [[jie2026omnivlarl]]
- [[hartz2024art]]
- [[antonova2021bayesian]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
