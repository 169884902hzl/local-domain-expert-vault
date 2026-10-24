---
title: "关节物体操控"
tags: [articulated-object, manipulation, simulation]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "对具有可动关节的物体（门、抽屉、保险箱等）进行操控的任务，涉及关节约束推理和多步交互。"
---

## Definition

关节物体操控 is maintained here as an evidence-linked concept. 对具有可动关节的物体（门、抽屉、保险箱等）进行操控的任务，涉及关节约束推理和多步交互。

## Key Ideas

- Direct local evidence currently comes from [[wang2026beyond]].
- The concept is tracked with local tags: articulated-object, manipulation, simulation.
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

- [[wang2026beyond]] (direct evidence): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[garcia2025generalizable]] (broader context): 提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任...
- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...
- [[deshpande2026molmob0t]] (broader context): 基于 MolmoSpaces 生成 1.7M 仿真专家轨迹，训练三种策略架构（VLM+flow-matching、π0 复现、轻量 Transformer），在 Franka...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...

## Evidence Map

- Direct evidence papers: [[wang2026beyond]].
- Broader local evidence context: [[wang2026beyond]], [[qiu2025wildlma]], [[garcia2025generalizable]], [[do2025watch]], [[deshpande2026molmob0t]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[long-horizon-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[wang2026beyond]]
- [[qiu2025wildlma]]
- [[garcia2025generalizable]]
- [[do2025watch]]
- [[deshpande2026molmob0t]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
