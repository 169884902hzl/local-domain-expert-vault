---
title: "Vision-Language Embedding (VLE)"
tags: [concept, VLM]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "将视觉和语言映射到共享嵌入空间的模型，可用于零样本奖励估计和偏好生成"
---

## Definition

Vision-Language Embedding (VLE) is maintained here as an evidence-linked concept. 将视觉和语言映射到共享嵌入空间的模型，可用于零样本奖励估计和偏好生成

## Key Ideas

- Direct local evidence currently comes from [[ghosh2026reducing]].
- The concept is tracked with local tags: concept, VLM.
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

- [[ghosh2026reducing]] (direct evidence): ROVED 框架通过 VLE 生成偏好标签、不确定性过滤选择性地查询 oracle，并在训练中参数高效微调 VLE，在 Meta-World 操控任务上减少 50-80% o...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...

## Evidence Map

- Direct evidence papers: [[ghosh2026reducing]].
- Broader local evidence context: [[ghosh2026reducing]], [[zhu2026nsvla]], [[zhang2026prts]], [[zhou2026vlbiman]], [[zhou2026rcnf]].
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
- [[preference-based-rl]]
- [[contrastive-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[ghosh2026reducing]]
- [[zhu2026nsvla]]
- [[zhang2026prts]]
- [[zhou2026vlbiman]]
- [[zhou2026rcnf]]
- [[zhong2026vlaopd]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
