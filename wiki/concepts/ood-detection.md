---
title: "OOD Detection"
tags: [concept, ood, distribution-shift]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "检测模型输入是否偏离训练数据分布，在机器人操控中分为 task-level 和 state-level 两种 OOD。"
---

## Definition

OOD Detection is maintained here as an evidence-linked concept. 检测模型输入是否偏离训练数据分布，在机器人操控中分为 task-level 和 state-level 两种 OOD。

## Key Ideas

- Direct local evidence currently comes from [[zhou2026rcnf]].
- The concept is tracked with local tags: concept, ood, distribution-shift.
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

- [[zhou2026rcnf]] (direct evidence): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[sun2026maniparena]] (broader context): ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Si...
- [[nie820smaller]] (broader context): 提出 KufeNet，通过不等特征编码和知识蒸馏实现 KB 级参数的抓取检测模型。不等并行结构处理 RGB-D（深度分支更多参数），3D 卷积注意力补偿 DSC 相关性损失。...
- [[nasiriany2025rtaffordance]] (broader context): 提出 RT-Affordance（RT-A），用 affordance（末端执行器关键位姿）作为策略中间表示。层次化模型：VLA 先预测 affordance plan（gr...

## Evidence Map

- Direct evidence papers: [[zhou2026rcnf]].
- Broader local evidence context: [[zhou2026rcnf]], [[zhang2026safevla]], [[zhang2026generative]], [[you2026dotsim]], [[wang2026stepnft]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[anomaly-detection]]
- [[runtime-monitoring]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhou2026rcnf]]
- [[zhang2026safevla]]
- [[zhang2026generative]]
- [[you2026dotsim]]
- [[wang2026stepnft]]
- [[sun2026maniparena]]
- [[nie820smaller]]
- [[nasiriany2025rtaffordance]]
