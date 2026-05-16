---
title: "灵巧抓取 (Dexterous Grasping)"
tags: [manipulation, grasping, planning]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "使用多指灵巧手抓取物体的技术，相比平行夹爪具有更高的自由度和操作灵活性"
---

## Definition

灵巧抓取 (Dexterous Grasping) is maintained here as an evidence-linked concept. 使用多指灵巧手抓取物体的技术，相比平行夹爪具有更高的自由度和操作灵活性

## Key Ideas

- Direct local evidence currently comes from [[chen2026adacleargrasp]].
- The concept is tracked with local tags: manipulation, grasping, dexterous-hand.
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

- [[chen2026adacleargrasp]] (direct evidence): 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[ma2025running]] (broader context): 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FP...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[gao2025must]] (broader context): 提出 MuST（Multi-Head Skill Transformer），在 Octo 骨干上增加 N+1 个 head（N 个技能 head + 1 个进度 head），...
- [[das2026dart]] (broader context): DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: [[chen2026adacleargrasp]].
- Broader local evidence context: [[chen2026adacleargrasp]], [[niu2026versatile]], [[ma2025running]], [[zheng120dottip]], [[gao2025must]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grasping]]
- [[robotic-manipulation]]
- [[sim-to-real]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[chen2026adacleargrasp]]
- [[niu2026versatile]]
- [[ma2025running]]
- [[zheng120dottip]]
- [[gao2025must]]
- [[das2026dart]]
- [[zhou2025oneshot]]
- [[zhao2025polytouch]]
