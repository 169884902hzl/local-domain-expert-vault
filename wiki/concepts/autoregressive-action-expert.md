---
title: "自回归动作专家 (Autoregressive Action Expert)"
tags: [autoregressive, action-generation, VLA]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "将机器人动作生成建模为因果序列预测问题，通过维护连续的运动历史实现时序感知的控制。"
---

## Definition

自回归动作专家 (Autoregressive Action Expert) is maintained here as an evidence-linked concept. 将机器人动作生成建模为因果序列预测问题，通过维护连续的运动历史实现时序感知的控制。

## Key Ideas

- Direct local evidence currently comes from [[hu2026arvla]].
- The concept is tracked with local tags: autoregressive, action-generation, VLA.
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

- [[hu2026arvla]] (direct evidence): 提出独立的自回归 Action Expert，通过 Hybrid KV Cache 维护滚动运动历史和可刷新视觉-语言前缀，配合 Dynamic Temporal Re-an...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head

## Evidence Map

- Direct evidence papers: [[hu2026arvla]].
- Broader local evidence context: [[hu2026arvla]], [[zhong2026vlaopd]], [[zheng2026pokevla]], [[zhao2026visualtactile]], [[zhang2026touchguide]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[action-chunking]]
- [[hybrid-kv-cache]]
- [[knowledge-insulation]]
- [[pi-zero]]
- [[robotic-manipulation]]

## Related Papers

- [[hu2026arvla]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[zhang2026touchguide]]
- [[zhang2026joyaira]]
- [[zhang2026handx]]
- [[zhang2026generative]]
