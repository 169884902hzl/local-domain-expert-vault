---
title: "Runtime Monitoring"
tags: [concept, runtime-monitoring, robot-safety]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "在机器人任务执行过程中实时监控行为一致性，检测异常并触发干预策略。"
---

## Definition

Runtime Monitoring is maintained here as an evidence-linked concept. 在机器人任务执行过程中实时监控行为一致性，检测异常并触发干预策略。

## Key Ideas

- Direct local evidence currently comes from [[zhou2026rcnf]].
- The concept is tracked with local tags: concept, runtime-monitoring, robot-safety.
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
- [[liu2025oneshot]] (broader context): 提出 MAGIC（Manipulation Analogies for Generalizable Intelligent Contacts），通过接触类比实现单样本操控策略...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...

## Evidence Map

- Direct evidence papers: [[zhou2026rcnf]].
- Broader local evidence context: [[zhou2026rcnf]], [[liu2025oneshot]], [[jeong2026your]], [[zhu2026nsvla]], [[zhu2024scaling]].
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
- [[ood-detection]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhou2026rcnf]]
- [[liu2025oneshot]]
- [[jeong2026your]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2025oneshot]]
- [[zhong2026vlaopd]]
