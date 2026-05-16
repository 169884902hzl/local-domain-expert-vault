---
title: "Vision Shortcut"
tags: [VLA, dataset-bias, generalization]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "VLA 模型在目标驱动数据上学习视觉-动作捷径，忽略语言指令，在 OOD 和模糊场景中失败。"
---

## Definition

Vision Shortcut is maintained here as an evidence-linked concept. VLA 模型在目标驱动数据上学习视觉-动作捷径，忽略语言指令，在 OOD 和模糊场景中失败。

## Key Ideas

- Direct local evidence currently comes from [[lian2026langforce]].
- The concept is tracked with local tags: VLA, dataset-bias, generalization.
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

- [[lian2026langforce]] (direct evidence): 揭示 VLA 模型在目标驱动数据集上的\"视觉捷径\"病理（语言条件互信息坍缩为零），提出基于贝叶斯分解的双分支框架 LangForce，通过 Latent Action Q...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...

## Evidence Map

- Direct evidence papers: [[lian2026langforce]].
- Broader local evidence context: [[lian2026langforce]], [[zhu2026nsvla]], [[zhou2026vlbiman]], [[zhou2026sim1]], [[zhou2026rcnf]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[information-collapse]]
- [[vision-language-action]]
- [[vla]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[lian2026langforce]]
- [[zhu2026nsvla]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
- [[zhou2026ego]]
- [[zhou2025oneshot]]
- [[zhong2026vlaopd]]
