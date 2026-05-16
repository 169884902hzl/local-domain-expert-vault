---
title: "Feedback Loop"
tags: [concept, planning, control]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "LLM 与 RL 之间的双向信息反馈机制，允许高层规划器根据环境状态变化动态更新任务计划。"
---

## Definition

Feedback Loop is maintained here as an evidence-linked concept. LLM 与 RL 之间的双向信息反馈机制，允许高层规划器根据环境状态变化动态更新任务计划。

## Key Ideas

- Direct local evidence currently comes from [[saad2026hybrid]].
- The concept is tracked with local tags: concept, planning, control.
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

- [[saad2026hybrid]] (direct evidence): 提出 LLM 高层任务规划 + RL 低层控制的混合框架，在 PyBullet 仿真中用 Franka Panda 实现了比纯 RL 方法快 33.5% 的任务完成时间和更高...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[luo2026selfimproving]] (broader context): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...

## Evidence Map

- Direct evidence papers: [[saad2026hybrid]].
- Broader local evidence context: [[saad2026hybrid]], [[iek2026coral]], [[yu2026atrs]], [[vo2026codegraphvlp]], [[mitrano2024grasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[task-decomposition]]
- [[reinforcement-learning]]
- [[large-language-model]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[saad2026hybrid]]
- [[iek2026coral]]
- [[yu2026atrs]]
- [[vo2026codegraphvlp]]
- [[mitrano2024grasp]]
- [[missal2026ropedreamer]]
- [[luo2026selfimproving]]
- [[liu2026longhorizon]]
