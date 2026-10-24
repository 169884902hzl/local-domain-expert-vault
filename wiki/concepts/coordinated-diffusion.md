---
title: "Coordinated Diffusion"
tags: [diffusion, multi-agent, imitation-learning]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控框架。"
---

## Definition

Coordinated Diffusion is maintained here as an evidence-linked concept. 通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控框架。

## Key Ideas

- Direct local evidence currently comes from [[peters2026coordinated]].
- The concept is tracked with local tags: diffusion, multi-agent, imitation-learning.
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

- [[peters2026coordinated]] (direct evidence): 提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-an...
- [[gu2026refinedp]] (broader context): 提出REFINE-DP框架，通过DPPO联合优化扩散策略高层规划器和RL底层控制器，使人形机器人loco-manipulation任务成功率从50-70%提升至90%+，仅需...
- [[chen2026rotridiff]] (broader context): 提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。
- [[chen2025coordinated]] (broader context): 将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...

## Evidence Map

- Direct evidence papers: [[peters2026coordinated]].
- Broader local evidence context: [[peters2026coordinated]], [[gu2026refinedp]], [[chen2026rotridiff]], [[chen2025coordinated]], [[ziakas2026aligning]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[imitation-learning]]
- [[classifier-guidance]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[peters2026coordinated]]
- [[gu2026refinedp]]
- [[chen2026rotridiff]]
- [[chen2025coordinated]]
- [[ziakas2026aligning]]
- [[zhu2024scaling]]
- [[zhou2026sim1]]
- [[zhao2025polytouch]]
