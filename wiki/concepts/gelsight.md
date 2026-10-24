---
title: "GelSight"
tags: [concept]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "基于光学的高分辨率触觉传感器，通过相机检测弹性体变形来感知几何和力"
---

## Definition

GelSight is maintained here as an evidence-linked concept. 基于光学的高分辨率触觉传感器，通过相机检测弹性体变形来感知几何和力

## Key Ideas

- Direct local evidence currently comes from [[wang2026ocra]].
- The concept is tracked with local tags: concept.
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

- [[wang2026ocra]] (direct evidence): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[george2024vital]] (broader context): 提出 VITaL 预训练方法，通过时间感知的多模态对比损失将视觉和触觉编码器投影到共享潜在空间。关键发现：用触觉数据预训练的纯视觉策略性能大幅提升（USB 插入 20%→85...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: [[wang2026ocra]].
- Broader local evidence context: [[wang2026ocra]], [[zhao2025polytouch]], [[yan2026tac2real]], [[xu2026fingereye]], [[george2024vital]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[visual-tactile-fusion]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[wang2026ocra]]
- [[zhao2025polytouch]]
- [[yan2026tac2real]]
- [[xu2026fingereye]]
- [[george2024vital]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
