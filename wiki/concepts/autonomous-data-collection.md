---
title: "自主数据采集"
tags: [data-collection, autonomous, robot-learning]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "无需人类干预的机器人操控数据自动生成范式，通过闭环管线实现持续数据采集。"
---

## Definition

自主数据采集 is maintained here as an evidence-linked concept. 无需人类干预的机器人操控数据自动生成范式，通过闭环管线实现持续数据采集。

## Key Ideas

- Direct local evidence currently comes from [[wang2026radar]].
- The concept is tracked with local tags: data-collection, autonomous, robot-learning.
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

- [[wang2026radar]] (direct evidence): 提出全自主闭环数据采集引擎 RADAR，通过 VLM 语义规划 + GNN 图扩散模仿学习 + 三阶段 VQA 评估 + LIFO 自主环境重置，仅用 2-5 次人类示教即可...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[ye2026reinforcement]] (broader context): 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...

## Evidence Map

- Direct evidence papers: [[wang2026radar]].
- Broader local evidence context: [[wang2026radar]], [[consortium2026openhembodiment]], [[zhao2026visualtactile]], [[zhang2026touchguide]], [[zhang2026recurrent]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[vision-language-model]]
- [[environment-reset]]
- [[robot-learning]]
- [[robotic-manipulation]]
- [[planning]]

## Related Papers

- [[wang2026radar]]
- [[consortium2026openhembodiment]]
- [[zhao2026visualtactile]]
- [[zhang2026touchguide]]
- [[zhang2026recurrent]]
- [[ye2026reinforcement]]
- [[wang2026visionlanguageaction]]
- [[smith2024steer]]
