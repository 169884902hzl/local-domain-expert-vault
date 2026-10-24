---
title: "Flow Map Policy"
tags: [RL, flow-matching, generative-model, policy-learning]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "基于 flow map 两时间跳算子的单步生成策略，通过学习平均速度场实现任意跨度跳跃，统一 Mean Flow Policy 和 Consistency Model 等单步方法"
---

## Definition

Flow Map Policy is maintained here as an evidence-linked concept. 基于 flow map 两时间跳算子的单步生成策略，通过学习平均速度场实现任意跨度跳跃，统一 Mean Flow Policy 和 Consistency Model 等单步方法

## Key Ideas

- Direct local evidence currently comes from [[ziakas2026aligning]].
- The concept is tracked with local tags: RL, flow-matching, generative-model, policy-learning.
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

- [[ziakas2026aligning]] (direct evidence): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[patil2026youve]] (broader context): 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需...
- [[lu2026unified]] (broader context): UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分...
- [[khan2026discrete]] (broader context): 提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow...
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[wei2026navol]] (broader context): 基于 DAgger 框架在 IsaacLab 中实现导航扩散策略的在线模仿学习，通过全局规划器提供在线专家轨迹监督，以 rollout-update 循环消除奖励工程、缓解分...

## Evidence Map

- Direct evidence papers: [[ziakas2026aligning]].
- Broader local evidence context: [[ziakas2026aligning]], [[patil2026youve]], [[lu2026unified]], [[khan2026discrete]], [[he2026generative]].
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
- [[diffusion-model]]
- [[reinforcement-learning]]
- [[offline-to-online-rl]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[ziakas2026aligning]]
- [[patil2026youve]]
- [[lu2026unified]]
- [[khan2026discrete]]
- [[he2026generative]]
- [[zhao2026rosclaw]]
- [[wang2026stepnft]]
- [[wei2026navol]]
