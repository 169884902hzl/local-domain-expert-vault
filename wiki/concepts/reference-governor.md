---
title: "Reference Governor"
tags: [control-theory, safety, constraint-management]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "基于最大输出容许集 (MOAS) 的约束管理附加模块，实时修改参考输入以避免违反状态/控制约束。"
---

## Definition

Reference Governor is maintained here as an evidence-linked concept. 基于最大输出容许集 (MOAS) 的约束管理附加模块，实时修改参考输入以避免违反状态/控制约束。

## Key Ideas

- Direct local evidence currently comes from [[schperberg2026mobius]].
- The concept is tracked with local tags: control-theory, safety, constraint-management.
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

- [[schperberg2026mobius]] (direct evidence): 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[wang2026any2any]] (broader context): 提出DiffKT3D框架，将预训练视频扩散模型(Wan 2.1)迁移至放疗3D剂量预测，通过Any2Any条件范式支持7种模态的灵活输入输出组合，并引入基于临床Scoreca...
- [[steen2024quadratic]] (broader context): 提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impac...
- [[so2025evaluating]] (broader context): 提出基于联网电子任务板的机器人操控基准，用于评估电气电路检查（万用表使用）的人机技能差距。6 个子任务：定位任务板+按键→读取屏幕+调整滑块→插入探针插头→开门+探针电路→缠...
- [[moletta2026preference]] (broader context): 提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trouser...
- [[liu2025oneshot]] (broader context): 提出 MAGIC（Manipulation Analogies for Generalizable Intelligent Contacts），通过接触类比实现单样本操控策略...

## Evidence Map

- Direct evidence papers: [[schperberg2026mobius]].
- Broader local evidence context: [[schperberg2026mobius]], [[yuan2026prefmoe]], [[xu2026token]], [[wang2026any2any]], [[steen2024quadratic]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[admittance-control]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[schperberg2026mobius]]
- [[yuan2026prefmoe]]
- [[xu2026token]]
- [[wang2026any2any]]
- [[steen2024quadratic]]
- [[so2025evaluating]]
- [[moletta2026preference]]
- [[liu2025oneshot]]
