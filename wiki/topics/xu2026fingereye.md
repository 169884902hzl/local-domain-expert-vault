---
title: "FingerEye: Continuous and unified vision-tactile sensing for dexterous manipulation"
tags: [manipulation, imitation, DLO, tactile]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。"
authors: "Xu, Zhixuan; Li, Yichen; Wu, Xuanye; Qiu, Tianyu; Shao, Lin"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "2X7VC74B"
---
## 摘要

Dexterous（灵巧） robotic manipulation（机器人操控） requires comprehensive perception across all phases of interaction: pre-contact, contact initiation, and post-contact. Such continuous feedback allows a robot to adapt its actions throughout interaction. However, many existing tactile（触觉） sensors, such as GelSight and its variants, only provide feedback after contact is established, limiting a robot's ability to precisely initiate contact. We introduce FingerEye, a compact and cost-effective sensor that provides continuous vision-tactile（触觉） feedback throughout the interaction process. FingerEye integrates binocular RGB cameras to provide close-range visual perception with implicit stereo depth. Upon contact, external forces and torques deform a compliant ring structure; these deformations are captured via marker-based pose estimation and serve as a proxy for contact wrench sensing. This design enables a perception stream that smoothly transitions from pre-contact visual cues to post-contact tactile（触觉） feedback. Building on this sensing capability, we develop a vision-tactile（触觉） imitation learning（模仿学习） policy that fuses signals from multiple FingerEye sensors to learn dexterous manipulation（灵巧操控） behaviors from limited real-world data. We further develop a digital twin of our sensor and robot platform to improve policy generalization. By combining real demonstrations with visually augmented simulated observations for representation learning（表征学习）, the learned policies become more robust to object appearance variations. Together, these design aspects enable dexterous manipulation（灵巧操控） across diverse object properties and interaction regimes, including coin standing, chip picking, letter retrieving, and syringe manipulation（操控）. The hardware design, code, appendix, and videos are available on our project website: https://nus-lins-lab.github.io/FingerEyeWeb/

## 中文简述

提出基于模仿学习的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、可变形物体操控、触觉感知

## 关键贡献

1. 提出 FingerEye 传感器：双目 RGB 提供近距离视觉，柔性 ring deformation 提供接触 wrench proxy。
2. 用 AprilTag/marker pose estimation 估计柔性结构变形，并建立 deformation 与 force/torque 的相关性。
3. 提出 FingerEye Policy，将多个 FingerEye 传感器和 wrist camera 融合，用 transformer policy 从少量真实演示学习灵巧操作。
4. 建立 sensor/robot digital twin，并使用 simulation-augmented representation learning 提升视觉外观泛化。
## 结构化提取

- Problem: 现有触觉传感器多在接触后工作，无法覆盖 pre-contact 到 post-contact 的连续感知。
- Method: 双目 RGB + compliant ring deformation + marker pose estimation；transformer-based multi-view vision-tactile policy；digital twin + sim-augmented representation learning。
- Tasks: coin standing、chip picking、letter retrieving、syringe manipulation。
- Sensors: 多个 FingerEye 指尖传感器、wrist RealSense D435、机器人本体状态。
- Robot Setup: uFactory xArm7 + LEAP Hand，leader-follower teleoperation 收集演示。
- Metrics: pose/wrench sensitivity、任务成功次数、外观泛化；具体附录数值未逐项录入。
- Limitations: 平台绑定、wrench proxy 精度有限、未验证 DLO 长线接触。
- Evidence Notes: arXiv HTML 全文；依据 Abstract、Sensor Design、Policy Experiments、Results & Analysis、Limitations。
## 本地引用关系

- [[li2025routing]]
- [[xue2026tube]]
- [[zhao2025polytouch]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high; sensor design, policy architecture, robot platform, tasks and sim-augmented representation learning are available; some appendix details were not exhaustively transcribed.
- Confidence: high
- Summary: FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。


## Problem

灵巧操控需要在 pre-contact、contact initiation 和 post-contact 全阶段连续感知。GelSight 等触觉传感器通常只在接触后提供反馈，难以帮助机器人精确发起接触。纯视觉又无法可靠感知接触力和局部变形。因此论文目标是设计一种能平滑连接近距离视觉和触觉反馈的传感器，并验证其对 dexterous manipulation policy 的价值。


## Method

硬件上，FingerEye 将 binocular RGB cameras 和 compliant ring structure 集成在指尖。接触前，双目视觉提供局部几何和物体接近信息；接触后，外力导致柔性环变形，marker pose 变化被估计为接触 wrench proxy。策略学习上，xArm7 + LEAP Hand 每个指尖装 FingerEye，wrist RealSense 提供全局视觉。policy 使用 transformer 融合多视角视觉-触觉信号和机器人状态，预测 action chunks。


## Experiments

传感器实验包括 pose estimation 鲁棒性、sensitivity analysis、wrench-deformation correlation 和 delicate grasping。策略实验包括 coin standing、chip picking、letter retrieving、syringe manipulation 等 dexterous tasks。Sim-augmented representation learning 使用真实演示和少量模拟演示，通过视觉增强让 representation 更能泛化到不同颜色/外观。论文指出直接混合仿真和真实 action supervision 效果差，而把仿真用于视觉 representation 辅助更稳。


## Limitations

1. 传感器设计与 LEAP Hand/xArm7 平台绑定较强，迁移到双臂 DLO 夹持器需要硬件适配。
2. 接触 wrench 是由形变估计得到的 proxy，不等价于高精度六轴力传感器。
3. DLO 操控中的长线接触、滑移和张力传播未验证。
4. 策略仍依赖真实演示，sim-to-real 动作监督不能直接混合。


## Key Takeaways

1. FingerEye 支持“接触前视觉 + 接触后触觉”的连续感知，非常适合 DLO 抓取点接近、接触建立和张力调整阶段。
2. 该工作与 Tube Diffusion Policy 互补：FingerEye 提供传感器，TDP 提供 reactive visual-tactile policy。
3. 对我们的 idea，可以把 FingerEye/PolyTouch 作为 tactile sensing 证据，探索 DLO 局部张力和滑移估计。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu|Xu, Zhixuan]]
- [[shao-lin|Shao, Lin]]
