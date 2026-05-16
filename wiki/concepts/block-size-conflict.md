---
title: "Block Size Conflict"
tags: [dLLM, RL, multi-domain]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "扩散语言模型多域 RL 后训练中，不同推理域对 block size 的偏好不同，导致固定 block size 产生域间结构冲突"
---

## Definition

Block Size Conflict is maintained here as an evidence-linked concept. 扩散语言模型多域 RL 后训练中，不同推理域对 block size 的偏好不同，导致固定 block size 产生域间结构冲突

## Key Ideas

- Direct local evidence currently comes from [[jiang2026blockr1]].
- The concept is tracked with local tags: dLLM, RL, multi-domain.
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

- [[jiang2026blockr1]] (direct evidence): 揭示扩散语言模型多域 RL 后训练中 block size 域冲突问题，通过 teacher-student 管线为每个训练样本分配最优 block size，构建 41K...
- [[jiang2026break]] (broader context): 提出 b1 框架，通过 RL 学习动态大小的推理块并施加单调熵下降约束，解决扩散语言模型中固定大小分块破坏推理连贯性的问题，在数学推理基准上相比固定分块基线最高提升 19.53%。
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhang2021dair]] (broader context): 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（inter...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[yang2026automated]] (broader context): 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...

## Evidence Map

- Direct evidence papers: [[jiang2026blockr1]].
- Broader local evidence context: [[jiang2026blockr1]], [[jiang2026break]], [[ziakas2026aligning]], [[zhang2021dair]], [[yuan2026prefmoe]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grpo]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jiang2026blockr1]]
- [[jiang2026break]]
- [[ziakas2026aligning]]
- [[zhang2021dair]]
- [[yuan2026prefmoe]]
- [[yu2026atrs]]
- [[yang2026automated]]
- [[yang2026asyncshield]]
