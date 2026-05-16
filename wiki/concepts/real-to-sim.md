---
title: "Real-to-Sim"
tags: [sim-to-real, scene-reconstruction, digital-twin]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "将真实世界场景数字化重建到仿真环境中，实现空间一致性，用于策略验证和安全探索。"
---

## Definition

Real-to-Sim is maintained here as an evidence-linked concept. 将真实世界场景数字化重建到仿真环境中，实现空间一致性，用于策略验证和安全探索。

## Key Ideas

- Direct local evidence currently comes from [[kang2026coenv]].
- The concept is tracked with local tags: sim-to-real, scene-reconstruction, digital-twin.
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

- [[kang2026coenv]] (direct evidence): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[yang2025simtoreal]] (broader context): 针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算...
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...

## Evidence Map

- Direct evidence papers: [[kang2026coenv]].
- Broader local evidence context: [[kang2026coenv]], [[zhou2025oneshot]], [[yu2026atrs]], [[you2026dotsim]], [[ye2026generation]].
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
- [[compositional-environment]]
- [[digital-twin]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[kang2026coenv]]
- [[zhou2025oneshot]]
- [[yu2026atrs]]
- [[you2026dotsim]]
- [[ye2026generation]]
- [[yang2026asyncshield]]
- [[yang2025simtoreal]]
- [[xu2026twinrlvla]]
