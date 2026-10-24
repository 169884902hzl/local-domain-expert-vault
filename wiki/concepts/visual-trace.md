---
title: "Visual Trace"
tags: [VLA, visual-prompting, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "2D 关键点轨迹作为 VLA 的视觉 prompt，将高层空间意图传递给低层执行器。"
---

## Definition

Visual Trace is maintained here as an evidence-linked concept. 2D 关键点轨迹作为 VLA 的视觉 prompt，将高层空间意图传递给低层执行器。

## Key Ideas

- Direct local evidence currently comes from [[liu2026longhorizon]].
- The concept is tracked with local tags: VLA, visual-prompting, manipulation.
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

- [[liu2026longhorizon]] (direct evidence): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2025tissue]] (broader context): 磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...

## Evidence Map

- Direct evidence papers: [[liu2026longhorizon]].
- Broader local evidence context: [[liu2026longhorizon]], [[zhi2025closedloop]], [[zhi102unifying]], [[zhao2026visualtactile]], [[zhao2025polytouch]].
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
- [[robotic-manipulation]]
- [[long-horizon-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]

## Related Papers

- [[liu2026longhorizon]]
- [[zhi2025closedloop]]
- [[zhi102unifying]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[zhang2026visionlanguageaction]]
- [[zhang2025tissue]]
- [[xue2026tube]]
