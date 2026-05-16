---
title: "Masked Language Modeling (MLM)"
tags: [NLP, language-model, diffusion]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "通过逐步去掩码生成文本的统一框架，涵盖自回归模型和扩散语言模型"
---

## Definition

Masked Language Modeling (MLM) is maintained here as an evidence-linked concept. 通过逐步去掩码生成文本的统一框架，涵盖自回归模型和扩散语言模型

## Key Ideas

- Direct local evidence currently comes from [[li2026ets]].
- The concept is tracked with local tags: NLP, language-model, diffusion.
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

- [[li2026ets]] (direct evidence): 提出训练无关的推理时采样方法 ETS，通过在线 Monte Carlo 估计能量项直接从 RL 最优策略采样，统一覆盖自回归模型和扩散语言模型，在推理/编码/科学基准上超越...
- [[wu2026contrastive]] (broader context): 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提...
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[chen2026elasticflow]] (broader context): 基于平均速度场的单步生成策略框架，通过 MeanFlow Identity 实现无需蒸馏的 1-NFE 推理（~71Hz），Elastic Time Horizons 机制编...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...

## Evidence Map

- Direct evidence papers: [[li2026ets]].
- Broader local evidence context: [[li2026ets]], [[wu2026contrastive]], [[wang2026beyond]], [[chen2026elasticflow]], [[zhou2026sim1]].
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
- [[diffusion-model]]
- [[test-time-scaling]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026ets]]
- [[wu2026contrastive]]
- [[wang2026beyond]]
- [[chen2026elasticflow]]
- [[zhou2026sim1]]
- [[zhang2026handx]]
- [[zhang2026generative]]
- [[yang2026hivla]]
