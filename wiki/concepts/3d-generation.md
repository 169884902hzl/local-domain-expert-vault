---
title: "3D Generation"
tags: [3d-generation, embodied-ai, simulation]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "利用生成模型（扩散、自回归、VAE等）合成3D几何、纹理、结构和物理属性的技术，在具身AI中强调仿真就绪性而非视觉逼真度"
---

## Definition

3D Generation is maintained here as an evidence-linked concept. 利用生成模型（扩散、自回归、VAE等）合成3D几何、纹理、结构和物理属性的技术，在具身AI中强调仿真就绪性而非视觉逼真度

## Key Ideas

- Direct local evidence currently comes from [[ye2026generation]].
- The concept is tracked with local tags: 3d-generation, embodied-ai, simulation.
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

- [[ye2026generation]] (direct evidence): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[scheikl620movement]] (broader context): 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabi...
- [[pallar2025optimal]] (broader context): 提出 CBF 轨迹规划算法用于多四旋翼协作操控线缆悬挂刚体载荷。将载荷、线缆、四旋翼建模为凸多面体，利用对偶定理降低 CBF 约束的计算复杂度，确保全系统（载荷+线缆+四旋翼...
- [[jia2026gsplayground]] (broader context): 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研...
- [[dong2025vitavla]] (broader context): 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token...

## Evidence Map

- Direct evidence papers: [[ye2026generation]].
- Broader local evidence context: [[ye2026generation]], [[zhou2025oneshot]], [[xie2026humanintention]], [[wang2026visionlanguageaction]], [[scheikl620movement]].
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
- [[gaussian-splatting]]
- [[digital-twin]]
- [[world-model]]
- [[deformable-linear-object]]
- [[robotic-manipulation]]

## Related Papers

- [[ye2026generation]]
- [[zhou2025oneshot]]
- [[xie2026humanintention]]
- [[wang2026visionlanguageaction]]
- [[scheikl620movement]]
- [[pallar2025optimal]]
- [[jia2026gsplayground]]
- [[dong2025vitavla]]
