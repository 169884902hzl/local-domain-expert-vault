---
title: "Multi-Modal Locomotion"
tags: [locomotion, multi-modal, robot-design]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "机器人通过统一形态在步行、爬行、攀爬、滚动等多种运动模式间切换的能力。"
---

## Definition

Multi-Modal Locomotion is maintained here as an evidence-linked concept. 机器人通过统一形态在步行、爬行、攀爬、滚动等多种运动模式间切换的能力。

## Key Ideas

- Direct local evidence currently comes from [[schperberg2026mobius]].
- The concept is tracked with local tags: locomotion, multi-modal, robot-design.
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

- [[schperberg2026mobius]] (direct evidence): 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...

## Evidence Map

- Direct evidence papers: [[schperberg2026mobius]].
- Broader local evidence context: [[schperberg2026mobius]], [[lee2026implicit]], [[jia2026gsplayground]], [[zhu2024scaling]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[schperberg2026mobius]]
- [[lee2026implicit]]
- [[jia2026gsplayground]]
- [[zhu2024scaling]]
- [[zheng2026pokevla]]
- [[zhao2026rosclaw]]
- [[zhao2025polytouch]]
- [[zeng2026recapa]]
