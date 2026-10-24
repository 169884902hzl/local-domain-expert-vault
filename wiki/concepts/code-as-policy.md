---
title: "Code-as-Policy (CaP)"
tags: [concept, manipulation, robot-learning]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "使用可执行代码作为机器人策略表示，由 LLM/VLM 生成程序组合感知和控制原语来完成操控任务"
---

## Definition

Code-as-Policy (CaP) is maintained here as an evidence-linked concept. 使用可执行代码作为机器人策略表示，由 LLM/VLM 生成程序组合感知和控制原语来完成操控任务

## Key Ideas

- Direct local evidence currently comes from [[fu2026capx]].
- The concept is tracked with local tags: concept, manipulation, robot-learning.
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

- [[fu2026capx]] (direct evidence): 提出 CaP-X 框架，包含 CaP-Gym（交互式编码环境，187 个任务）、CaP-Bench（8 个层级系统评估 12 个前沿模型）、CaP-Agent0（无需训练的...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[ma2025running]] (broader context): 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FP...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...
- [[li2026realvlgr1]] (broader context): 构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现...
- [[li2026h2r]] (broader context): H2R 通过 HaMeR+SAM+LaMa 管线将第一人称人类手部视频替换为机器人手臂渲染帧，缩小人机视觉域差异，在仿真和真实双臂/灵巧手操控任务上实现 1.3%-23.3%...
- [[dai2024racer]] (broader context): 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GP...

## Evidence Map

- Direct evidence papers: [[fu2026capx]].
- Broader local evidence context: [[fu2026capx]], [[zhao2026visualtactile]], [[ye2026reinforcement]], [[ma2025running]], [[liu2025forcemimic]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[fu2026capx]]
- [[zhao2026visualtactile]]
- [[ye2026reinforcement]]
- [[ma2025running]]
- [[liu2025forcemimic]]
- [[li2026realvlgr1]]
- [[li2026h2r]]
- [[dai2024racer]]
