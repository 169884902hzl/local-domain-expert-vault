---
title: "Code as Policies"
tags: [planning, LLM, programmatic-control]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "利用 LLM 生成可执行代码作为机器人策略，通过程序化推理替代端到端神经网络规划。"
---

## Definition

Code as Policies is maintained here as an evidence-linked concept. 利用 LLM 生成可执行代码作为机器人策略，通过程序化推理替代端到端神经网络规划。

## Key Ideas

- Direct local evidence currently comes from [[vo2026codegraphvlp]].
- The concept is tracked with local tags: planning, LLM, programmatic-control.
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

- [[vo2026codegraphvlp]] (direct evidence): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...

## Evidence Map

- Direct evidence papers: [[vo2026codegraphvlp]].
- Broader local evidence context: [[vo2026codegraphvlp]], [[gu2026vistabot]], [[zhou2025oneshot]], [[liu2026longhorizon]], [[aida2026cortex]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[semantic-scene-graph]]
- [[task-and-motion-planning]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[vo2026codegraphvlp]]
- [[gu2026vistabot]]
- [[zhou2025oneshot]]
- [[liu2026longhorizon]]
- [[aida2026cortex]]
- [[zhao2026visualtactile]]
- [[xu2026fingereye]]
- [[wang2026discretertc]]
