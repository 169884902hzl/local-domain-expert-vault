---
title: "Grasp Synthesis"
tags: [concept, grasping]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "生成满足物理合理性和语义约束的抓取姿态的方法，涵盖几何驱动、语义驱动和 diffusion-based 范式。"
---

## Definition

Grasp Synthesis is maintained here as an evidence-linked concept. 生成满足物理合理性和语义约束的抓取姿态的方法，涵盖几何驱动、语义驱动和 diffusion-based 范式。

## Key Ideas

- Direct local evidence currently comes from [[wu2026affordgrasp]].
- The concept is tracked with local tags: concept, grasping.
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

- [[wu2026affordgrasp]] (direct evidence): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[ma2025running]] (broader context): 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FP...
- [[chen2026adacleargrasp]] (broader context): 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[huang2026flexitac]] (broader context): 提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-...
- [[das2026dart]] (broader context): DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。
- [[chen2026ropa]] (broader context): ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实...

## Evidence Map

- Direct evidence papers: [[wu2026affordgrasp]].
- Broader local evidence context: [[wu2026affordgrasp]], [[ma2025running]], [[chen2026adacleargrasp]], [[yang2026ultradexgrasp]], [[niu2026versatile]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[affordance-learning]]
- [[dexterous-grasping]]
- [[latent-diffusion]]
- [[diffusion-policy]]
- [[grasping]]
- [[robotic-manipulation]]

## Related Papers

- [[wu2026affordgrasp]]
- [[ma2025running]]
- [[chen2026adacleargrasp]]
- [[yang2026ultradexgrasp]]
- [[niu2026versatile]]
- [[huang2026flexitac]]
- [[das2026dart]]
- [[chen2026ropa]]
