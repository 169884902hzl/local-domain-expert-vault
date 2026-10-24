---
title: "Proximity Sensing"
tags: [proximity-sensing, tactile-sensing, sensor-design]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "检测物体在非接触距离范围内的存在和距离的感知技术，包括 ToF、电容式、声学等模态"
---

## Definition

Proximity Sensing is maintained here as an evidence-linked concept. 检测物体在非接触距离范围内的存在和距离的感知技术，包括 ToF、电容式、声学等模态

## Key Ideas

- Direct local evidence currently comes from [[kohlbrenner2026egocentric]].
- The concept is tracked with local tags: proximity-sensing, tactile-sensing, sensor-design.
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

- [[kohlbrenner2026egocentric]] (direct evidence): 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[yang2025simtoreal]] (broader context): 针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[röfer2025pseudotouch]] (broader context): 提出 PseudoTouch，从深度图像预测低维触觉信号（ReSkin 15D），构建视觉-触觉跨模态映射。用 8 个基本几何体（球、圆柱、盒等）采集配对深度-触觉数据训练...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。

## Evidence Map

- Direct evidence papers: [[kohlbrenner2026egocentric]].
- Broader local evidence context: [[kohlbrenner2026egocentric]], [[zheng120dottip]], [[zhao2026visualtactile]], [[zhao2025polytouch]], [[yang2025simtoreal]].
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
- [[collision-avoidance]]
- [[tactile-sensing]]
- [[vision-language-model]]
- [[deformable-linear-object]]
## Related Papers

- [[kohlbrenner2026egocentric]]