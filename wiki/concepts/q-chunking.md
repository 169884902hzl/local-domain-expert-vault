---
title: "Q-chunking"
tags: [rl, offline-rl, action-chunking]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "将 RL 的 Q 函数评估扩展到 action chunk 级别，使 critic 能直接评估动作序列的整体价值，提升与 action-chunked 策略（如 Diffusion Policy）的兼容性。"
---

## Definition

Q-chunking is maintained here as an evidence-linked concept. 将 RL 的 Q 函数评估扩展到 action chunk 级别，使 critic 能直接评估动作序列的整体价值，提升与 action-chunked 策略（如 Diffusion Policy）的兼容性。

## Key Ideas

- Direct local evidence currently comes from [[jauhri2026wholebody]].
- The concept is tracked with local tags: rl, offline-rl, action-chunking.
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

- [[jauhri2026wholebody]] (direct evidence): WHOLE-MoMa 利用次优 WBC 作为结构先验生成仿真演示数据，结合 Q-chunked IQL 离线 RL 和 Diffusion Policy 在 TiAGo++...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[wang2026discretertc]] (broader context): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: [[jauhri2026wholebody]].
- Broader local evidence context: [[jauhri2026wholebody]], [[zhao2023finegrained]], [[xue2026tube]], [[wang2026discretertc]], [[gu2026vistabot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-chunking]]
- [[offline-rl]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jauhri2026wholebody]]
- [[zhao2023finegrained]]
- [[xue2026tube]]
- [[wang2026discretertc]]
- [[gu2026vistabot]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
