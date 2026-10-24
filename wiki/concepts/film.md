---
title: "FiLM"
tags: [conditioning, feature-modulation, VLM]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "Feature-wise Linear Modulation，通过仿射变换用一种模态的特征调制另一种模态的特征表示。"
---

## Definition

FiLM is maintained here as an evidence-linked concept. Feature-wise Linear Modulation，通过仿射变换用一种模态的特征调制另一种模态的特征表示。

## Key Ideas

- Direct local evidence currently comes from [[xiao2026avavla]].
- The concept is tracked with local tags: conditioning, feature-modulation, VLM.
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

- [[xiao2026avavla]] (direct evidence): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[tang2025uad]] (broader context): 提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...

## Evidence Map

- Direct evidence papers: [[xiao2026avavla]].
- Broader local evidence context: [[xiao2026avavla]], [[tang2025uad]], [[zhu2026nsvla]], [[zhong2026vlaopd]], [[zhi2025closedloop]].
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
- [[active-visual-attention]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[xiao2026avavla]]
- [[tang2025uad]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
- [[zhang2026world2minecraft]]
- [[zhang2026visionlanguageaction]]
