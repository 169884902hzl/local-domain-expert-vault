---
title: "Simulation Readiness"
tags: [simulation-readiness, 3d-generation, embodied-ai]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "生成的3D资产能否被物理仿真器直接消费而无需大量人工后处理，是区分具身导向3D生成与传统3D生成的核心标准"
---

## Definition

Simulation Readiness is maintained here as an evidence-linked concept. 生成的3D资产能否被物理仿真器直接消费而无需大量人工后处理，是区分具身导向3D生成与传统3D生成的核心标准

## Key Ideas

- Direct local evidence currently comes from [[ye2026generation]].
- The concept is tracked with local tags: simulation-readiness, 3d-generation, embodied-ai.
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

- [[ye2026generation]] (direct evidence): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zhang2025tissue]] (broader context): 磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[wu2025rlgsbridge]] (broader context): 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft M...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈

## Evidence Map

- Direct evidence papers: [[ye2026generation]].
- Broader local evidence context: [[ye2026generation]], [[zhou2025oneshot]], [[zhang2026generative]], [[zhang2025tissue]], [[yu2026atrs]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[3d-generation]]
- [[sim-to-real]]
- [[domain-randomization]]
- [[digital-twin]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[ye2026generation]]
- [[zhou2025oneshot]]
- [[zhang2026generative]]
- [[zhang2025tissue]]
- [[yu2026atrs]]
- [[yang2026asyncshield]]
- [[wu2025rlgsbridge]]
- [[wang2026visionlanguageaction]]
