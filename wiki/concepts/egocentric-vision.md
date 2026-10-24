---
title: "第一人称视觉 (Egocentric Vision)"
tags: [egocentric, vision, human-data]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "第一人称视角的视觉数据，与机器人头部安装的相机视角相似，可作为机器人训练数据的替代来源。"
---

## Definition

第一人称视觉 (Egocentric Vision) is maintained here as an evidence-linked concept. 第一人称视角的视觉数据，与机器人头部安装的相机视角相似，可作为机器人训练数据的替代来源。

## Key Ideas

- Direct local evidence currently comes from [[li2026gazevla]].
- The concept is tracked with local tags: egocentric, vision, human-data.
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
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head

## Evidence Map

- Direct evidence papers: [[li2026gazevla]].
- Broader local evidence context: [[li2026gazevla]], [[zhou2025oneshot]], [[zhi2025closedloop]], [[zhi102unifying]], [[zheng2026pokevla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[gaze-intention]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[li2026gazevla]]
- [[zhou2025oneshot]]
- [[zhi2025closedloop]]
- [[zhi102unifying]]
- [[zheng2026pokevla]]
- [[zhao2025polytouch]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026generative]]
