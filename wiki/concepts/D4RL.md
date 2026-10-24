---
title: "D4RL"
tags: [concept, benchmark, RL]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "D4RL：面向深度数据驱动强化学习的标准化数据集与基准，包含 Maze2D、Antmaze、Franka Kitchen 等任务域"
---

## Definition

D4RL is maintained here as an evidence-linked concept. D4RL：面向深度数据驱动强化学习的标准化数据集与基准，包含 Maze2D、Antmaze、Franka Kitchen 等任务域

## Key Ideas

- Direct local evidence currently comes from [[stambaugh2026mixeddensity]].
- The concept is tracked with local tags: concept, benchmark, RL.
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

- [[stambaugh2026mixeddensity]] (direct evidence): 提出非均匀时间密度扩散规划器 MDD，用单一扁平扩散模型在轨迹不同区段分配不同时间分辨率，在 D4RL 基准上超越 Diffusion Veteran 达到新 SOTA。
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...

## Evidence Map

- Direct evidence papers: [[stambaugh2026mixeddensity]].
- Broader local evidence context: [[stambaugh2026mixeddensity]], [[zhu2026nsvla]], [[zhou2026ego]], [[zhong2026vlaopd]], [[zhao2026visualtactile]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[offline-rl]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[stambaugh2026mixeddensity]]
- [[zhu2026nsvla]]
- [[zhou2026ego]]
- [[zhong2026vlaopd]]
- [[zhao2026visualtactile]]
- [[zhang2026world2minecraft]]
- [[zhang2026safevla]]
- [[zhang2026recurrent]]
