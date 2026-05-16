---
title: "Spectral Bias"
tags: [neural-network, optimization]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "神经网络在学习混合频率信号时偏向低频分量的现象，ElasticFlow 通过 Fourier Feature 编码弹性时域来克服此偏差。"
---

## Definition

Spectral Bias is maintained here as an evidence-linked concept. 神经网络在学习混合频率信号时偏向低频分量的现象，ElasticFlow 通过 Fourier Feature 编码弹性时域来克服此偏差。

## Key Ideas

- Direct local evidence currently comes from [[chen2026elasticflow]].
- The concept is tracked with local tags: neural-network, optimization.
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

- [[chen2026elasticflow]] (direct evidence): 基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[wang2026offline]] (broader context): 将离线策略评估重新定义为折扣 liveness 问题，通过两阶段 bootstrapping 机制在稀疏奖励操控任务中捕获非单调任务进展并显著降低截断偏差。
- [[spieler2026slotmpc]] (broader context): 提出Slot-MPC，将基于Slot Attention的对象中心表征（SAVi）与可微分世界模型（cOCVP）结合，通过梯度优化MPC在紧凑的对象级隐空间中进行目标条件规划...
- [[patel2024getzero]] (broader context): 提出 GET-Zero，Graph Embodiment Transformer 通过图注意力偏置实现零样本具身泛化。每个关节作为独立 token，空间编码（SPD）+ 父子...
- [[narendra2026knowledgeguided]] (broader context): 提出KG-M3PO框架，将在线3D场景图（动态更新空间/包含/可供性关系）通过GNN编码器端到端融入M3PO强化学习训练循环，在部分可观测的多任务机械臂操控中显著优于纯视觉基...
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...
- [[mahboob2026betting]] (broader context): 将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算...

## Evidence Map

- Direct evidence papers: [[chen2026elasticflow]].
- Broader local evidence context: [[chen2026elasticflow]], [[yang2026rise]], [[wang2026offline]], [[spieler2026slotmpc]], [[patel2024getzero]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[flow-matching]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[chen2026elasticflow]]
- [[yang2026rise]]
- [[wang2026offline]]
- [[spieler2026slotmpc]]
- [[patel2024getzero]]
- [[narendra2026knowledgeguided]]
- [[moroncelli2026jumpstart]]
- [[mahboob2026betting]]
