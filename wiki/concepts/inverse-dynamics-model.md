---
title: "Inverse Dynamics Model"
tags: [concept, robotics, action-prediction]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "将连续视觉帧对映射为机器人可执行动作的模型，是视觉规划范式中连接视觉规划与物理执行的关键组件。"
---

## Definition

Inverse Dynamics Model is maintained here as an evidence-linked concept. 将连续视觉帧对映射为机器人可执行动作的模型，是视觉规划范式中连接视觉规划与物理执行的关键组件。

## Key Ideas

- Direct local evidence currently comes from [[luo2026selfimproving]].
- The concept is tracked with local tags: concept, robotics, action-prediction.
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

- [[luo2026selfimproving]] (direct evidence): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...
- [[giacomuzzo2024blackbox]] (broader context): 提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagr...
- [[chen2025coordinated]] (broader context): 将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[wang2026phys2real]] (broader context): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...

## Evidence Map

- Direct evidence papers: [[luo2026selfimproving]].
- Broader local evidence context: [[luo2026selfimproving]], [[giacomuzzo2024blackbox]], [[chen2025coordinated]], [[zhou2026sim1]], [[zhang2026handx]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[visual-planning]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[luo2026selfimproving]]
- [[giacomuzzo2024blackbox]]
- [[chen2025coordinated]]
- [[zhou2026sim1]]
- [[zhang2026handx]]
- [[you2026dotsim]]
- [[yang2026rise]]
- [[wang2026phys2real]]
