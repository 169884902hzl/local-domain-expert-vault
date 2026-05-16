---
title: "Dynamical Systems (DS)"
tags: [concept, LfD, motion-generation, stability]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "基于常微分方程的运动表示方法，通过定义状态空间中的向量场实现稳定的策略学习"
---

## Definition

Dynamical Systems (DS) is maintained here as an evidence-linked concept. 基于常微分方程的运动表示方法，通过定义状态空间中的向量场实现稳定的策略学习

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: concept, LfD, motion-generation, stability.
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

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]] (broader context): 提出PNPF框架，用闭环相位变量条件化神经势函数以解决DS-LfD中轨迹交叉与状态重访问题，在2D/6D任务和真实UR10机器人上超越CONDOR与NODE
- [[styrud2025automatic]] (broader context): 提出 BETR-XP-LLM 方法，结合 LLM 和任务规划器自动生成和扩展行为树（BT）作为机器人操控策略。两阶段：(1) LLM 将自然语言目标解释为形式化目标条件 →...
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[Reactive Motion Generation via Phase-varying Neural Potential Functions]], [[styrud2025automatic]], [[shah2025acoustic]], [[zhi102unifying]], [[zhang2026visionlanguageaction]].
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
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[ji2026recovering]]