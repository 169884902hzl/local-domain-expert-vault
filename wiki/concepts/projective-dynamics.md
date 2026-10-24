---
title: "Projective Dynamics"
tags: [physics-simulation, FEM, optimization]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "结合 FEM 物理精度与 PBD 效率的 local-global 优化仿真框架，通过辅助投影状态求解弹性力。"
---

## Definition

Projective Dynamics is maintained here as an evidence-linked concept. 结合 FEM 物理精度与 PBD 效率的 local-global 优化仿真框架，通过辅助投影状态求解弹性力。

## Key Ideas

- Direct local evidence currently comes from [[luo2026flash]].
- The concept is tracked with local tags: physics-simulation, FEM, optimization.
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

- [[luo2026flash]] (direct evidence): GPU 原生可变形物体仿真框架，基于 NCP 接触求解器和 Projective Dynamics 实现 3M+ DoF 实时仿真，训练策略分钟级完成并零样本迁移到真实双臂机...
- [[levy2026simulation]] (broader context): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[yang2026physforge]] (broader context): 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。
- [[yang2026automated]] (broader context): 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。
- [[xu2026r2rgen]] (broader context): 提出无需仿真器的 real-to-real 3D 数据生成框架 R2RGen，通过 group-wise 回溯增强和 camera-aware 后处理，用 1 次人类示范即可...
- [[xiao2026worldenv]] (broader context): 提出用扩散世界模型替代物理交互环境对 VLA 策略进行 RL 后训练，通过 VGGT 几何感知特征注入保证物理一致性，用 VLM 即时反射器提供连续奖励信号和动态终止检测，仅...
- [[shen2026plan]] (broader context): 提出 SAGE 框架，通过物理沙盒生成合成经验（Genesis）、非对称自适应裁剪 RL 训练（Evolution）、检索增强导航（Navigation）三阶段，将 VLM...
- [[hou2026world]] (broader context): 以机器人学习为中心的世界模型综述，按架构范式（IDM/单骨干/MoE/统一VLA/隐空间）分类梳理世界模型与策略的耦合方式，系统总结世界模型作为仿真器（RL训练+评估）和视频...

## Evidence Map

- Direct evidence papers: [[luo2026flash]].
- Broader local evidence context: [[luo2026flash]], [[levy2026simulation]], [[yang2026physforge]], [[yang2026automated]], [[xu2026r2rgen]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[FEM-simulation]]
- [[NCP-contact]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[luo2026flash]]
- [[levy2026simulation]]
- [[yang2026physforge]]
- [[yang2026automated]]
- [[xu2026r2rgen]]
- [[xiao2026worldenv]]
- [[shen2026plan]]
- [[hou2026world]]
