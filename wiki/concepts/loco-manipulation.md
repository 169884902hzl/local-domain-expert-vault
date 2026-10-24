---
title: "Loco-Manipulation"
tags: [concept, manipulation, humanoid, locomotion]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "人形机器人同时执行移动和操控任务的能力，需要全身稳定性与末端灵巧性的协调。"
---

## Definition

Loco-Manipulation is maintained here as an evidence-linked concept. 人形机器人同时执行移动和操控任务的能力，需要全身稳定性与末端灵巧性的协调。

## Key Ideas

- Direct local evidence currently comes from [[niu2026versatile]].
- The concept is tracked with local tags: concept, manipulation, humanoid, locomotion.
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

- [[niu2026versatile]] (direct evidence): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...

## Evidence Map

- Direct evidence papers: [[niu2026versatile]].
- Broader local evidence context: [[niu2026versatile]], [[qiu2025wildlma]], [[jia2026gsplayground]], [[zhu2024scaling]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[whole-body-control]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[niu2026versatile]]
- [[qiu2025wildlma]]
- [[jia2026gsplayground]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
- [[zheng120dottip]]
