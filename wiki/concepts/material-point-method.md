---
title: "Material Point Method"
tags: [concept, simulation, physics]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "混合 Eulerian-Lagrangian 粒子方法，适合大变形和柔性材料仿真，已用于可微触觉传感器建模"
---

## Definition

Material Point Method is maintained here as an evidence-linked concept. 混合 Eulerian-Lagrangian 粒子方法，适合大变形和柔性材料仿真，已用于可微触觉传感器建模

## Key Ideas

- Direct local evidence currently comes from [[you2026dotsim]].
- The concept is tracked with local tags: concept, simulation, physics.
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

- [[you2026dotsim]] (direct evidence): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[xie102multiview]] (broader context): 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...
- [[wang2025oneshot]] (broader context): 提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定...
- [[wang2023multistage]] (broader context): 提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1)...
- [[tang2025kalie]] (broader context): 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的...
- [[shi2025zeromimic]] (broader context): 提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓...

## Evidence Map

- Direct evidence papers: [[you2026dotsim]].
- Broader local evidence context: [[you2026dotsim]], [[yin2026multiple]], [[xie102multiview]], [[xia2024cage]], [[wang2025oneshot]].
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
- [[tactile-sensing]]
- [[differentiable-simulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[you2026dotsim]]
- [[yin2026multiple]]
- [[xie102multiview]]
- [[xia2024cage]]
- [[wang2025oneshot]]
- [[wang2023multistage]]
- [[tang2025kalie]]
- [[shi2025zeromimic]]
