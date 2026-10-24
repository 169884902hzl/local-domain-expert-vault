---
title: "Rapid Motor Adaptation (RMA)"
tags: [sim-to-real, reinforcement-learning, online-adaptation]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "一种基于交互历史的在线策略自适应框架，通过两阶段训练使策略能从观测-动作历史推断环境物理参数并自适应调整。"
---

## Definition

Rapid Motor Adaptation (RMA) is maintained here as an evidence-linked concept. 一种基于交互历史的在线策略自适应框架，通过两阶段训练使策略能从观测-动作历史推断环境物理参数并自适应调整。

## Key Ideas

- Direct local evidence currently comes from [[wang2026phys2real]].
- The concept is tracked with local tags: sim-to-real, reinforcement-learning, online-adaptation.
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

- [[wang2026phys2real]] (direct evidence): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...
- [[dalal2025local]] (broader context): 提出 ManipGen 系统，通过训练 3500+ 单物体 RL 专家策略并蒸馏为通用 visuomotor 策略，结合 GPT-4o 任务分解 + Grounded SAM...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[singh2025handobject]] (broader context): 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目...

## Evidence Map

- Direct evidence papers: [[wang2026phys2real]].
- Broader local evidence context: [[wang2026phys2real]], [[you2026dotsim]], [[ye2026generation]], [[yang2026asyncshield]], [[do2025watch]].
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
- [[reinforcement-learning]]
- [[domain-randomization]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wang2026phys2real]]
- [[you2026dotsim]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
- [[do2025watch]]
- [[dalal2025local]]
- [[xue2026tube]]
- [[singh2025handobject]]
