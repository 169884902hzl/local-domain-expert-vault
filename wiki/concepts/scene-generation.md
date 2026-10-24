---
title: "Scene Generation"
tags: [concept, simulation, scene-generation]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "利用 LLM/VLM 等生成模型从自然语言或高层语义指令自动构建仿真场景的技术"
---

## Definition

Scene Generation is maintained here as an evidence-linked concept. 利用 LLM/VLM 等生成模型从自然语言或高层语义指令自动构建仿真场景的技术

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: concept, simulation, scene-generation.
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

- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[kang2026coenv]] (broader context): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[chen2026ropa]] (broader context): ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实...
- [[boerdijk2025autonomous]] (broader context): 提出 3D 打印夹具（fixture）方法，通过在刚性物体上安装可拆卸的带 fiducial marker 的夹具，实现纯 RGB 图像的自主 6D 位姿标注（平均精度约 6...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zhou2026sim1]], [[ye2026generation]], [[yang2026ultradexgrasp]], [[xie2026humanintention]], [[kang2026coenv]].
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
- [[domain-randomization]]
- [[vla]]
- [[real-to-sim]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[zhou2026sim1]]
- [[ye2026generation]]
- [[yang2026ultradexgrasp]]
- [[xie2026humanintention]]
- [[kang2026coenv]]
- [[jia2026gsplayground]]
- [[chen2026ropa]]
- [[boerdijk2025autonomous]]
