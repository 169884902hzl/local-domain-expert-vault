---
title: "VLM Planning"
tags: [concept, VLM, planning]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "利用视觉-语言模型作为零样本规划器，从图像观测和语言指令直接生成操控动作或高层计划。"
---

## Definition

VLM Planning is maintained here as an evidence-linked concept. 利用视觉-语言模型作为零样本规划器，从图像观测和语言指令直接生成操控动作或高层计划。

## Key Ideas

- Direct local evidence currently comes from [[jia2026dreamplan]].
- The concept is tracked with local tags: concept, VLM, planning.
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

- [[jia2026dreamplan]] (direct evidence): 通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwe...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[li2026hierarchical]] (broader context): 提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion...

## Evidence Map

- Direct evidence papers: [[jia2026dreamplan]].
- Broader local evidence context: [[jia2026dreamplan]], [[zhou2026rcnf]], [[zhang2026prts]], [[xu2026roboagent]], [[vo2026codegraphvlp]].
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
- [[code-as-policies]]
- [[vla]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[jia2026dreamplan]]
- [[zhou2026rcnf]]
- [[zhang2026prts]]
- [[xu2026roboagent]]
- [[vo2026codegraphvlp]]
- [[sakamoto2026e3vsbench]]
- [[liu2026longhorizon]]
- [[li2026hierarchical]]
