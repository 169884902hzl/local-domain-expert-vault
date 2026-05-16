---
title: "EUEA"
tags: [embodied-ai, VLM, skill-learning, planning]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "Environmental Understanding Embodied Agent，通过在单一 VLM 中微调四组环境理解技能来提升具身智能体的环境理解能力。"
---

## Definition

EUEA is maintained here as an evidence-linked concept. Environmental Understanding Embodied Agent，通过在单一 VLM 中微调四组环境理解技能来提升具身智能体的环境理解能力。

## Key Ideas

- Direct local evidence currently comes from [[bang2026environmental]].
- The concept is tracked with local tags: embodied-ai, VLM, skill-learning, planning.
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

- [[bang2026environmental]] (direct evidence): 提出 EUEA 框架，通过在单一 VLM 中微调四组环境理解技能（物体感知、任务规划、动作理解、目标识别），结合采样恢复步骤和 GRPO 精炼阶段，在 ALFRED 上实现...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[wang2026adagamma]] (broader context): 提出 AdaGamma 方法，通过轻量级 Gamma Network 学习状态依赖折扣因子 γ(s)，配合 return-consistency 目标防止 TD-error...

## Evidence Map

- Direct evidence papers: [[bang2026environmental]].
- Broader local evidence context: [[bang2026environmental]], [[zhou2026rcnf]], [[zhang2026prts]], [[zeng2026recapa]], [[xu2026roboagent]].
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
- [[planning]]
- [[grpo]]
- [[pomdp]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[bang2026environmental]]
- [[zhou2026rcnf]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[xu2026roboagent]]
- [[wu2026continually]]
- [[wang2026beyond]]
- [[wang2026adagamma]]
