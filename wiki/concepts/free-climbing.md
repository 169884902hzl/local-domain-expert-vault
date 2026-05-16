---
title: "Free Climbing"
tags: [climbing, locomotion, grasping]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "机器人在离散垂直结构（如梯子、横杆）上通过抓取而非吸附实现攀爬的技术。"
---

## Definition

Free Climbing is maintained here as an evidence-linked concept. 机器人在离散垂直结构（如梯子、横杆）上通过抓取而非吸附实现攀爬的技术。

## Key Ideas

- Direct local evidence currently comes from [[schperberg2026mobius]].
- The concept is tracked with local tags: climbing, locomotion, grasping.
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
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[wu2026affordgrasp]] (broader context): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[ma2025running]] (broader context): 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FP...
- [[huang2026flexitac]] (broader context): 提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-...
- [[das2026dart]] (broader context): DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。

## Evidence Map

- Direct evidence papers: [[schperberg2026mobius]].
- Broader local evidence context: [[schperberg2026mobius]], [[yokomizo2026physquantagent]], [[yang2026twintrack]], [[wu2026affordgrasp]], [[niu2026versatile]].
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
- [[multi-modal-locomotion]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[schperberg2026mobius]]
- [[yokomizo2026physquantagent]]
- [[yang2026twintrack]]
- [[wu2026affordgrasp]]
- [[niu2026versatile]]
- [[ma2025running]]
- [[huang2026flexitac]]
- [[das2026dart]]
