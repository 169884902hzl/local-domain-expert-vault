---
title: "Pinch Grasp"
tags: [grasping, manipulation, contact]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "两指夹持式抓取，通过指尖施加法向力固定物体，可支撑机器人全身重量。"
---

## Definition

Pinch Grasp is maintained here as an evidence-linked concept. 两指夹持式抓取，通过指尖施加法向力固定物体，可支撑机器人全身重量。

## Key Ideas

- Direct local evidence currently comes from [[schperberg2026mobius]].
- The concept is tracked with local tags: grasping, manipulation, contact.
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

- [[schperberg2026mobius]] (direct evidence): 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模...
- [[yokomizo2026physquantagent]] (broader context): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[ma2025running]] (broader context): 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FP...
- [[chen2026rotridiff]] (broader context): 提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。
- [[chen2026adacleargrasp]] (broader context): 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter...
- [[blancomulero2024benchmarking]] (broader context): 首个量化布料操控 sim-to-real gap 的基准数据集。在双臂 Franka 系统上收集动态（fling）和准静态（拖拽）布料操控数据，用 Chamfer/Hausd...
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。

## Evidence Map

- Direct evidence papers: [[schperberg2026mobius]].
- Broader local evidence context: [[schperberg2026mobius]], [[yokomizo2026physquantagent]], [[ma2025running]], [[chen2026rotridiff]], [[chen2026adacleargrasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grasping]]
- [[free-climbing]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[schperberg2026mobius]]
- [[yokomizo2026physquantagent]]
- [[ma2025running]]
- [[chen2026rotridiff]]
- [[chen2026adacleargrasp]]
- [[blancomulero2024benchmarking]]
- [[yang2026twintrack]]
- [[niu2026versatile]]
