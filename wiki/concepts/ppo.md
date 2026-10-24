---
title: "Proximal Policy Optimization (PPO)"
tags: [concept, reinforcement-learning, policy-optimization]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "基于trust-region的策略梯度方法，通过clip函数限制策略更新幅度，广泛用于VLA模型的强化微调。"
---

## Definition

Proximal Policy Optimization (PPO) is maintained here as an evidence-linked concept. 基于trust-region的策略梯度方法，通过clip函数限制策略更新幅度，广泛用于VLA模型的强化微调。

## Key Ideas

- Direct local evidence currently comes from [[niu2026boosting]].
- The concept is tracked with local tags: concept, reinforcement-learning, policy-optimization.
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

- [[niu2026boosting]] (direct evidence): 提出Feasible Action Neighborhood (FAN)引导的正则化方法，用高斯先验约束VLA策略分布形状，在SFT和RFT（PPO）两种微调范式中均显著提升...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移

## Evidence Map

- Direct evidence papers: [[niu2026boosting]].
- Broader local evidence context: [[niu2026boosting]], [[zhang2026world2minecraft]], [[zhang2026recurrent]], [[zhang2026handx]], [[yuan2026embodiedr1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grpo]]
- [[vla]]
- [[online-fine-tuning]]
- [[feasible-action-neighborhood]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[niu2026boosting]]
- [[zhang2026world2minecraft]]
- [[zhang2026recurrent]]
- [[zhang2026handx]]
- [[yuan2026embodiedr1]]
- [[yu2026atrs]]
- [[you2026dotsim]]
- [[ye2026generation]]
