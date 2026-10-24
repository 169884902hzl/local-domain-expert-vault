---
title: "Whole-Body Control"
tags: [concept, humanoid, control, RL]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "人形机器人全身控制，协调下肢稳定性和上肢操控的统一控制框架。"
---

## Definition

Whole-Body Control is maintained here as an evidence-linked concept. 人形机器人全身控制，协调下肢稳定性和上肢操控的统一控制框架。

## Key Ideas

- Direct local evidence currently comes from [[niu2026versatile]].
- The concept is tracked with local tags: concept, humanoid, control, RL.
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

- [[niu2026versatile]] (direct evidence): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[qiu2025wildlma]] (broader context): 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildL...
- [[fu2024mobile]] (broader context): Stanford 提出低成本全身遥操作系统 Mobile ALOHA（$32k），将 ALOHA 扩展到移动双臂操控，发现与静态 ALOHA 数据集 co-training...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[mahboob2026betting]] (broader context): 将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算...
- [[liu2025autonomous]] (broader context): 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL...

## Evidence Map

- Direct evidence papers: [[niu2026versatile]].
- Broader local evidence context: [[niu2026versatile]], [[qiu2025wildlma]], [[fu2024mobile]], [[ye2026generation]], [[yang2026asyncshield]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[loco-manipulation]]
- [[sim-to-real]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[niu2026versatile]]
- [[qiu2025wildlma]]
- [[fu2024mobile]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
- [[marougkas2025integrating]]
- [[mahboob2026betting]]
- [[liu2025autonomous]]
