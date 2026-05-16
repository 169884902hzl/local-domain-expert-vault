---
title: "Agentic Generation"
tags: [concept, VLM, 3d-generation]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "用 VLM agent 作为智能监督者引导生成模型，通过 rejection sampling 确保输出与证据一致"
---

## Definition

Agentic Generation is maintained here as an evidence-linked concept. 用 VLM agent 作为智能监督者引导生成模型，通过 rejection sampling 确保输出与证据一致

## Key Ideas

- Direct local evidence currently comes from [[shi2026agile]].
- The concept is tracked with local tags: concept, VLM, 3d-generation.
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

- [[shi2026agile]] (direct evidence): 提出 VLM 引导的 agentic 生成管线，从单目视频重建手-物体交互的水密网格和 6D 轨迹，用 anchor-and-track 策略替代脆弱的 SfM 初始化，实现...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[yokomizo2026physquantagent]] (broader context): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[yang2026physforge]] (broader context): 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...

## Evidence Map

- Direct evidence papers: [[shi2026agile]].
- Broader local evidence context: [[shi2026agile]], [[zhu2026nsvla]], [[zhao2026rosclaw]], [[zhang2026handx]], [[yokomizo2026physquantagent]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[3d-generation]]
- [[hand-object-interaction]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[shi2026agile]]
- [[zhu2026nsvla]]
- [[zhao2026rosclaw]]
- [[zhang2026handx]]
- [[yokomizo2026physquantagent]]
- [[yang2026physforge]]
- [[xie2026humanintention]]
- [[xiao2026avavla]]
