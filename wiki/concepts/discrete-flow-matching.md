---
title: "Discrete Flow Matching"
tags: [flow-matching, generative-model, discrete-action]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "将 flow matching 范式从连续欧几里得空间扩展到有限离散空间，用 CTMC 生成器替代连续向量场，实现离散动作的生成式建模。"
---

## Definition

Discrete Flow Matching is maintained here as an evidence-linked concept. 将 flow matching 范式从连续欧几里得空间扩展到有限离散空间，用 CTMC 生成器替代连续向量场，实现离散动作的生成式建模。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: flow-matching, generative-model, discrete-action.
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

- [[khan2026discrete]] (broader context): 提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[patil2026youve]] (broader context): 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需...
- [[lu2026unified]] (broader context): UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分...
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[deshpande2026molmob0t]] (broader context): 基于 MolmoSpaces 生成 1.7M 仿真专家轨迹，训练三种策略架构（VLM+flow-matching、π0 复现、轻量 Transformer），在 Franka...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[khan2026discrete]], [[ziakas2026aligning]], [[yang2026hivla]], [[wang2026stepnft]], [[patil2026youve]].
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
- [[ctmc]]
- [[diffusion-policy]]
- [[offline-rl]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[khan2026discrete]]
- [[ziakas2026aligning]]
- [[yang2026hivla]]
- [[wang2026stepnft]]
- [[patil2026youve]]
- [[lu2026unified]]
- [[he2026generative]]
- [[deshpande2026molmob0t]]
