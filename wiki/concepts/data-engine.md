---
title: "Data Engine"
tags: [data-engine, VLA, data-generation]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "可扩展的数据生成系统或管线，持续生成、转换或增强 VLA 模型训练数据，而非提供静态数据集。"
---

## Definition

Data Engine is maintained here as an evidence-linked concept. 可扩展的数据生成系统或管线，持续生成、转换或增强 VLA 模型训练数据，而非提供静态数据集。

## Key Ideas

- Direct local evidence currently comes from [[wang2026visionlanguageaction]].
- The concept is tracked with local tags: data-engine, VLA, data-generation.
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

- [[wang2026visionlanguageaction]] (direct evidence): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[blancomulero2024benchmarking]] (broader context): 首个量化布料操控 sim-to-real gap 的基准数据集。在双臂 Franka 系统上收集动态（fling）和准静态（拖拽）布料操控数据，用 Chamfer/Hausd...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...

## Evidence Map

- Direct evidence papers: [[wang2026visionlanguageaction]].
- Broader local evidence context: [[wang2026visionlanguageaction]], [[blancomulero2024benchmarking]], [[zhou2025oneshot]], [[zheng2026pokevla]], [[zhao2026visualtactile]].
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
- [[sim-to-real]]
- [[imitation-learning]]
- [[domain-randomization]]
- [[world-model]]
- [[robotic-manipulation]]

## Related Papers

- [[wang2026visionlanguageaction]]
- [[blancomulero2024benchmarking]]
- [[zhou2025oneshot]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
- [[ye2026generation]]
- [[xu2026fingereye]]
- [[xie2026humanintention]]
