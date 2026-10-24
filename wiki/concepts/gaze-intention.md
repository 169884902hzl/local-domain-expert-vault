---
title: "注视意图 (Gaze Intention)"
tags: [gaze, intention, manipulation]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "利用人类注视信号作为意图的可观测代理，用于桥接人类与机器人之间的具身差距。"
---

## Definition

注视意图 (Gaze Intention) is maintained here as an evidence-linked concept. 利用人类注视信号作为意图的可观测代理，用于桥接人类与机器人之间的具身差距。

## Key Ideas

- Direct local evidence currently comes from [[li2026gazevla]].
- The concept is tracked with local tags: gaze, intention, manipulation.
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

- [[li2026gazevla]] (direct evidence): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[zhang2025tissue]] (broader context): 磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[steen2024quadratic]] (broader context): 提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impac...
- [[ozdamar820pushing]] (broader context): 提出仅依赖触觉反馈的响应式推动策略（RPS），使移动机器人在无视觉和物体模型的情况下推动未知物体到目标位置。电容触觉传感器覆盖机器人底盘，通过接触位置自适应调整底盘运动。Lo...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...

## Evidence Map

- Direct evidence papers: [[li2026gazevla]].
- Broader local evidence context: [[li2026gazevla]], [[zhang2025tissue]], [[xie2026humanintention]], [[steen2024quadratic]], [[ozdamar820pushing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[li2026gazevla]]
- [[zhang2025tissue]]
- [[xie2026humanintention]]
- [[steen2024quadratic]]
- [[ozdamar820pushing]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zhi2025closedloop]]
