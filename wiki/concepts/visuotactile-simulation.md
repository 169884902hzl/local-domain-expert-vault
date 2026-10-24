---
title: "Visuotactile Simulation"
tags: [simulation, tactile-sensing]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "视触觉仿真：在仿真环境中生成视觉触觉传感器信号（如 marker 位移场或 RGB 触觉图），用于 RL 策略训练。"
---

## Definition

Visuotactile Simulation is maintained here as an evidence-linked concept. 视触觉仿真：在仿真环境中生成视觉触觉传感器信号（如 marker 位移场或 RGB 触觉图），用于 RL 策略训练。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: simulation, tactile-sensing.
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

- [[huang2026flexitac]] (broader context): 提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[kohlbrenner2026egocentric]] (broader context): 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zhang2025tissue]] (broader context): 磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[huang2026flexitac]], [[yan2026tac2real]], [[kohlbrenner2026egocentric]], [[zhou2025oneshot]], [[zhang2026world2minecraft]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[tactile-sensing]]
- [[sim-to-real]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[huang2026flexitac]]
- [[yan2026tac2real]]
- [[kohlbrenner2026egocentric]]
- [[zhou2025oneshot]]
- [[zhang2026world2minecraft]]
- [[zhang2026joyaira]]
- [[zhang2026generative]]
- [[zhang2025tissue]]
