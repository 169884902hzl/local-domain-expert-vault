---
title: "MeanFlow / Mean Field Theory"
tags: [generative-model, flow-matching, imitation-learning]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "通过直接建模平均速度场实现单步生成的流匹配方法，由 Geng et al. (2025) 提出，被 ElasticFlow 引入机器人策略学习。"
---

## Definition

MeanFlow / Mean Field Theory is maintained here as an evidence-linked concept. 通过直接建模平均速度场实现单步生成的流匹配方法，由 Geng et al. (2025) 提出，被 ElasticFlow 引入机器人策略学习。

## Key Ideas

- Direct local evidence currently comes from [[chen2026elasticflow]].
- The concept is tracked with local tags: generative-model, flow-matching, imitation-learning.
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
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhang2026forceflow]] (broader context): 基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（V...
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[patil2026youve]] (broader context): 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需...
- [[lu2026unified]] (broader context): UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分...
- [[khan2026discrete]] (broader context): 提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow...

## Evidence Map

- Direct evidence papers: [[chen2026elasticflow]].
- Broader local evidence context: [[chen2026elasticflow]], [[ziakas2026aligning]], [[zhang2026forceflow]], [[yang2026hivla]], [[wang2026stepnft]].
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
- [[ziakas2026aligning]]
- [[zhang2026forceflow]]
- [[yang2026hivla]]
- [[wang2026stepnft]]
- [[patil2026youve]]
- [[lu2026unified]]
- [[khan2026discrete]]
