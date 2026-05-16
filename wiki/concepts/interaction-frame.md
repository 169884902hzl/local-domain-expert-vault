---
title: "Interaction Frame"
tags: [concept, manipulation, force-control]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "基于物理的瞬时局部坐标基，通过环境刚度谱分解将力调节与运动执行解耦，用于接触丰富操控的混合力-位控制"
---

## Definition

Interaction Frame is maintained here as an evidence-linked concept. 基于物理的瞬时局部坐标基，通过环境刚度谱分解将力调节与运动执行解耦，用于接触丰富操控的混合力-位控制

## Key Ideas

- Direct local evidence currently comes from [[fang2026force]].
- The concept is tracked with local tags: concept, manipulation, force-control.
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

- [[fang2026force]] (direct evidence): 提出 Interaction Frame 将接触操控的力-位分解为物理可观测量，构建全局视觉策略+高频局部力控策略的分层架构，在抛光和插入类任务上显著优于所有基线，泛化到未见...
- [[yokomizo2026physquantagent]] (broader context): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...
- [[xiao2026worldenv]] (broader context): 提出用扩散世界模型替代物理交互环境对 VLA 策略进行 RL 后训练，通过 VGGT 几何感知特征注入保证物理一致性，用 VLM 即时反射器提供连续奖励信号和动态终止检测，仅...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wu2026large]] (broader context): 将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器（时序对比/绝对进度/任务完成），在 ManiSkill3 零样本长时序操控和真实世界 pick-and...

## Evidence Map

- Direct evidence papers: [[fang2026force]].
- Broader local evidence context: [[fang2026force]], [[yokomizo2026physquantagent]], [[ye2026reinforcement]], [[yang2026rise]], [[xu2026twinrlvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[hybrid-force-position-control]]
- [[contact-rich-manipulation]]
- [[robotic-manipulation]]
- [[impedance-control]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[fang2026force]]
- [[yokomizo2026physquantagent]]
- [[ye2026reinforcement]]
- [[yang2026rise]]
- [[xu2026twinrlvla]]
- [[xiao2026worldenv]]
- [[xiao2026avavla]]
- [[wu2026large]]
