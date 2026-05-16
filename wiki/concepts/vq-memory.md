---
title: "VQ-Memory"
tags: [temporal-modeling, memory, VQ-VAE, manipulation]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "利用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪的时序记忆模块，用于增强 VLA 模型的长时序推理能力。"
---

## Definition

VQ-Memory is maintained here as an evidence-linked concept. 利用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪的时序记忆模块，用于增强 VLA 模型的长时序推理能力。

## Key Ideas

- Direct local evidence currently comes from [[wang2026beyond]].
- The concept is tracked with local tags: temporal-modeling, memory, VQ-VAE, manipulation.
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

- [[wang2026beyond]] (direct evidence): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[mosbach2025promptresponsive]] (broader context): 提出 SAM 2 + 记忆增强学生-教师学习框架用于 prompt 响应式物体抓取。教师策略用 PPO 从特权信息（OBB+heightmap）学习控制，学生策略通过 DAg...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[wang2026beyond]].
- Broader local evidence context: [[wang2026beyond]], [[wang2026evolvable]], [[mosbach2025promptresponsive]], [[liu2026longhorizon]], [[jia2026gsplayground]].
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
- [[long-horizon-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026beyond]]
- [[wang2026evolvable]]
- [[mosbach2025promptresponsive]]
- [[liu2026longhorizon]]
- [[jia2026gsplayground]]
- [[iek2026coral]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
