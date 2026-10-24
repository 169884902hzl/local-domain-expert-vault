---
title: "Teleoperation"
tags: [concept, manipulation]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "遥操作：远程控制机器人执行任务的技术，是 imitation learning 数据采集的主要手段"
---

## Definition

Teleoperation is maintained here as an evidence-linked concept. 遥操作：远程控制机器人执行任务的技术，是 imitation learning 数据采集的主要手段

## Key Ideas

- Direct local evidence currently comes from [[cui2026aharobot]].
- The concept is tracked with local tags: concept, manipulation.
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

- [[cui2026aharobot]] (direct evidence): 提出 $1000 开源双臂移动操作平台 AhaRobot，SCARA 式水平臂+升降导轨+双电机消间隙控制实现 0.7mm 重复定位精度，配套 26 面标记手柄 RoboPi...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[steen2024quadratic]] (broader context): 提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impac...
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[luo2024humanagent]] (broader context): 提出人机联合学习（HAJL）框架：人类操作员与学习型辅助 agent 共享控制机器人末端执行器，进行数据收集。控制比可调（human:agent），随数据积累 agent 逐...
- [[liu820enhancing]] (broader context): 提出 LLM+HRC 框架：GPT-4 分解高层指令为子任务序列→选择运动函数→结合 YOLOv5 感知的环境信息生成可执行代码。对于 LLM 无法处理的复杂轨迹（如水平铰链...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...

## Evidence Map

- Direct evidence papers: [[cui2026aharobot]].
- Broader local evidence context: [[cui2026aharobot]], [[zhou2025oneshot]], [[xu2026expertgen]], [[steen2024quadratic]], [[qiu2025wildlma]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robopilot]]
- [[bimanual-manipulation]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[cui2026aharobot]]
- [[zhou2025oneshot]]
- [[xu2026expertgen]]
- [[steen2024quadratic]]
- [[qiu2025wildlma]]
- [[luo2024humanagent]]
- [[liu820enhancing]]
- [[liu2025forcemimic]]
