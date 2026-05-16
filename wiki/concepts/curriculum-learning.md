---
title: "Curriculum Learning（课程学习）"
tags: [training-strategy, reinforcement-learning]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "通过从简单到困难逐步增加任务难度的训练策略，提升模型泛化能力和学习效率。"
---

## Definition

Curriculum Learning（课程学习） is maintained here as an evidence-linked concept. 通过从简单到困难逐步增加任务难度的训练策略，提升模型泛化能力和学习效率。

## Key Ideas

- Direct local evidence currently comes from [[tan2026fsunav]].
- The concept is tracked with local tags: training-strategy, reinforcement-learning.
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

- [[tan2026fsunav]] (direct evidence): 提出 Cerebrum-Cerebellum 双层架构实现零样本目标导航：Cerebellum 基于 DRL 的维度可配置局部规划器实现跨平台避障，Cerebrum 以 VL...
- [[ryu2025curricullm]] (broader context): 提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curr...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[tan2026fsunav]].
- Broader local evidence context: [[tan2026fsunav]], [[ryu2025curricullm]], [[marougkas2025integrating]], [[ziakas2026aligning]], [[zhu2026nsvla]].
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
- [[domain-randomization]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[tan2026fsunav]]
- [[ryu2025curricullm]]
- [[marougkas2025integrating]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
