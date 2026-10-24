---
title: "Differentiable Simulation"
tags: [concept, simulation, optimization]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "仿真过程可对参数求导，支持基于梯度的系统辨识和策略优化"
---

## Definition

Differentiable Simulation is maintained here as an evidence-linked concept. 仿真过程可对参数求导，支持基于梯度的系统辨识和策略优化

## Key Ideas

- Direct local evidence currently comes from [[you2026dotsim]].
- The concept is tracked with local tags: concept, simulation, optimization.
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

- [[you2026dotsim]] (direct evidence): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[kuroki2025gendom]] (broader context): 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zhang2025tissue]] (broader context): 磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移

## Evidence Map

- Direct evidence papers: [[you2026dotsim]].
- Broader local evidence context: [[you2026dotsim]], [[kuroki2025gendom]], [[zhou2025oneshot]], [[zhang2026joyaira]], [[zhang2026generative]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[sim-to-real]]
- [[material-point-method]]
- [[tactile-sensing]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[you2026dotsim]]
- [[kuroki2025gendom]]
- [[zhou2025oneshot]]
- [[zhang2026joyaira]]
- [[zhang2026generative]]
- [[zhang2025tissue]]
- [[yu2026atrs]]
- [[ye2026generation]]
