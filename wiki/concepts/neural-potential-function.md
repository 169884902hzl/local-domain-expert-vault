---
title: "Neural Potential Function"
tags: [concept, energy-based-model, dynamical-systems]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "用神经网络参数化标量势函数，其负梯度定义向量场（保守场约束），用于机器人策略学习"
---

## Definition

Neural Potential Function is maintained here as an evidence-linked concept. 用神经网络参数化标量势函数，其负梯度定义向量场（保守场约束），用于机器人策略学习

## Key Ideas

- Direct local evidence currently comes from [[ji2026recovering]].
- The concept is tracked with local tags: concept, energy-based-model, dynamical-systems.
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

- [[ji2026recovering]] (direct evidence): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]] (broader context): 提出PNPF框架，用闭环相位变量条件化神经势函数以解决DS-LfD中轨迹交叉与状态重访问题，在2D/6D任务和真实UR10机器人上超越CONDOR与NODE
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[liu2025kuda]] (broader context): 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为...
- [[giacomuzzo2024blackbox]] (broader context): 提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagr...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[ji2026recovering]].
- Broader local evidence context: [[ji2026recovering]], [[Reactive Motion Generation via Phase-varying Neural Potential Functions]], [[shah2025acoustic]], [[marougkas2025integrating]], [[liu2025kuda]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[energy-based-model]]
- [[diffusion-policy]]
- [[dynamical-systems]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[ji2026recovering]]
- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[shah2025acoustic]]
- [[marougkas2025integrating]]
- [[liu2025kuda]]
- [[giacomuzzo2024blackbox]]
- [[chi2024diffusion]]
- [[zhu2024scaling]]
