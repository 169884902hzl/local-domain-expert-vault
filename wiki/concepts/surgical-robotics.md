---
title: "Surgical Robotics"
tags: [surgical-robotics, medical-robotics, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "手术机器人研究涉及自主/半自主执行手术操作的机器人系统，当前面临数据稀缺、跨具身迁移和安全性等核心挑战。"
---

## Definition

Surgical Robotics is maintained here as an evidence-linked concept. 手术机器人研究涉及自主/半自主执行手术操作的机器人系统，当前面临数据稀缺、跨具身迁移和安全性等核心挑战。

## Key Ideas

- Direct local evidence currently comes from [[consortium2026openhembodiment]].
- The concept is tracked with local tags: surgical-robotics, medical-robotics, manipulation.
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

- [[consortium2026openhembodiment]] (direct evidence): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[styrud2025automatic]] (broader context): 提出 BETR-XP-LLM 方法，结合 LLM 和任务规划器自动生成和扩展行为树（BT）作为机器人操控策略。两阶段：(1) LLM 将自然语言目标解释为形式化目标条件 →...
- [[so2025evaluating]] (broader context): 提出基于联网电子任务板的机器人操控基准，用于评估电气电路检查（万用表使用）的人机技能差距。6 个子任务：定位任务板+按键→读取屏幕+调整滑块→插入探针插头→开门+探针电路→缠...

## Evidence Map

- Direct evidence papers: [[consortium2026openhembodiment]].
- Broader local evidence context: [[consortium2026openhembodiment]], [[zhi102unifying]], [[zhao2025polytouch]], [[wu2025tacdiffusion]], [[wu2025rlgsbridge]].
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
- [[vision-language-action]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[consortium2026openhembodiment]]
- [[zhi102unifying]]
- [[zhao2025polytouch]]
- [[wu2025tacdiffusion]]
- [[wu2025rlgsbridge]]
- [[wang2026evolvable]]
- [[styrud2025automatic]]
- [[so2025evaluating]]
