---
title: "力提示 (Force Prompt)"
tags: [prompting, manipulation, force-control, vla]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "将子任务力状态编码为文本 prompt 输入 VLM，构建力感知任务概念以驱动接触丰富操控的阶段推理。"
---

## Definition

力提示 (Force Prompt) is maintained here as an evidence-linked concept. 将子任务力状态编码为文本 prompt 输入 VLM，构建力感知任务概念以驱动接触丰富操控的阶段推理。

## Key Ideas

- Direct local evidence currently comes from [[li2026forcevla2]].
- The concept is tracked with local tags: prompting, manipulation, force-control, vla.
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

- [[li2026forcevla2]] (direct evidence): ForceVLA2 在 VLA 框架中引入 force prompt 驱动的长时推理和 Cross-Scale MoE 实现混合力-位姿控制，在5个接触丰富任务上平均成功率6...
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...

## Evidence Map

- Direct evidence papers: [[li2026forcevla2]].
- Broader local evidence context: [[li2026forcevla2]], [[luijkx2026llmguided]], [[zhu2026nsvla]], [[zhong2026vlaopd]], [[zheng120dottip]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[hybrid-force-position-control]]
- [[contact-rich-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026forcevla2]]
- [[luijkx2026llmguided]]
- [[zhu2026nsvla]]
- [[zhong2026vlaopd]]
- [[zheng120dottip]]
- [[zhao2026visualtactile]]
- [[zhang2026safevla]]
- [[zhang2026prts]]
