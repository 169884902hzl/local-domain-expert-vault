---
title: "Large Reward Model"
tags: [reward-modeling, VLM, reinforcement-learning]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "将基础 VLM 通过 LoRA 特化为帧级奖励生成器，输出三模态奖励信号（时序对比/绝对进度/任务完成），实现零样本在线策略精炼。"
---

## Definition

Large Reward Model is maintained here as an evidence-linked concept. 将基础 VLM 通过 LoRA 特化为帧级奖励生成器，输出三模态奖励信号（时序对比/绝对进度/任务完成），实现零样本在线策略精炼。

## Key Ideas

- Direct local evidence currently comes from [[wu2026large]].
- The concept is tracked with local tags: reward-modeling, VLM, reinforcement-learning.
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

- [[wu2026large]] (direct evidence): 将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器（时序对比/绝对进度/任务完成），在 ManiSkill3 零样本长时序操控和真实世界 pick-and...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[xiao2026worldenv]] (broader context): 提出用扩散世界模型替代物理交互环境对 VLA 策略进行 RL 后训练，通过 VGGT 几何感知特征注入保证物理一致性，用 VLM 即时反射器提供连续奖励信号和动态终止检测，仅...
- [[ryu2025curricullm]] (broader context): 提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curr...
- [[moroncelli2026jumpstart]] (broader context): VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda...

## Evidence Map

- Direct evidence papers: [[wu2026large]].
- Broader local evidence context: [[wu2026large]], [[zhu2026nsvla]], [[zhang2026recurrent]], [[yuan2026embodiedr1]], [[xu2026expertgen]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reward-shaping]]
- [[vlm-as-judge]]
- [[task-progress-estimation]]
- [[DPO]]
- [[ppo]]
- [[lora]]

## Related Papers

- [[wu2026large]]
- [[zhu2026nsvla]]
- [[zhang2026recurrent]]
- [[yuan2026embodiedr1]]
- [[xu2026expertgen]]
- [[xiao2026worldenv]]
- [[ryu2025curricullm]]
- [[moroncelli2026jumpstart]]
