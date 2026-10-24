---
title: "Reinforcement Fine-Tuning (RFT)"
tags: [concept, RL, fine-tuning]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "一种两阶段微调框架：先用 SFT（监督微调）+ CoT 数据预热模型，再用 RL（强化学习）进一步提升推理能力。"
---

## Definition

Reinforcement Fine-Tuning (RFT) is maintained here as an evidence-linked concept. 一种两阶段微调框架：先用 SFT（监督微调）+ CoT 数据预热模型，再用 RL（强化学习）进一步提升推理能力。

## Key Ideas

- Direct local evidence currently comes from [[jiang2026videop2r]].
- The concept is tracked with local tags: concept, RL, fine-tuning.
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

- [[jiang2026videop2r]] (direct evidence): 提出 VideoP2R 框架，将视频推理显式分解为感知和推理两个独立过程，通过三步 CoT 管线构建 162K 过程感知数据集，并设计 PA-GRPO 算法为两个过程分别提供...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[singh2025handobject]] (broader context): 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...

## Evidence Map

- Direct evidence papers: [[jiang2026videop2r]].
- Broader local evidence context: [[jiang2026videop2r]], [[zhou2026ego]], [[zhong2026vlaopd]], [[yang2026asyncshield]], [[xu2026twinrlvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[chain-of-thought]]
- [[grpo]]
- [[visual-reinforcement-learning]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[jiang2026videop2r]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[yang2026asyncshield]]
- [[xu2026twinrlvla]]
- [[wang2026stepnft]]
- [[singh2025handobject]]
- [[marougkas2025integrating]]
