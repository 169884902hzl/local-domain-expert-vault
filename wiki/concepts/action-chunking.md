---
title: "Action Chunking"
tags: [manipulation, imitation-learning, policy]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "策略每次推理输出一段未来动作序列而非单步动作的方法，广泛应用于机器人模仿学习。"
---

## Definition

Action Chunking is maintained here as an evidence-linked concept. 策略每次推理输出一段未来动作序列而非单步动作的方法，广泛应用于机器人模仿学习。

## Key Ideas

- Direct local evidence currently comes from [[wang2026discretertc]].
- The concept is tracked with local tags: manipulation, imitation-learning, policy.
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

- [[wang2026discretertc]] (direct evidence): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。

## Evidence Map

- Direct evidence papers: [[wang2026discretertc]].
- Broader local evidence context: [[wang2026discretertc]], [[zhao2023finegrained]], [[xue2026tube]], [[gu2026vistabot]], [[zhu2024scaling]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[asynchronous-execution]]
- [[real-time-chunking]]
- [[diffusion-model]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026discretertc]]
- [[zhao2023finegrained]]
- [[xue2026tube]]
- [[gu2026vistabot]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zheng2026pokevla]]
- [[zhao2026visualtactile]]
