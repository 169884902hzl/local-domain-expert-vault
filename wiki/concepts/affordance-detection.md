---
title: "Affordance Detection"
tags: [affordance, perception, 3D-vision]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "从感知数据（点云、图像）中预测物体功能区域（可供性）的技术，用于引导机器人与物体进行语义正确的交互。"
---

## Definition

Affordance Detection is maintained here as an evidence-linked concept. 从感知数据（点云、图像）中预测物体功能区域（可供性）的技术，用于引导机器人与物体进行语义正确的交互。

## Key Ideas

- Direct local evidence currently comes from [[li2026affordsim]].
- The concept is tracked with local tags: affordance, perception, 3D-vision.
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

- [[li2026affordsim]] (direct evidence): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[you2026dotsim]] (broader context): 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Rea...
- [[wu2026affordgrasp]] (broader context): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[tong2024ovalprompt]] (broader context): 提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词...
- [[tang2025uad]] (broader context): 提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模...
- [[tang2025kalie]] (broader context): 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的...

## Evidence Map

- Direct evidence papers: [[li2026affordsim]].
- Broader local evidence context: [[li2026affordsim]], [[zhou2026rcnf]], [[zheng2026pokevla]], [[you2026dotsim]], [[wu2026affordgrasp]].
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
- [[point-cloud]]
- [[robotic-manipulation]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026affordsim]]
- [[zhou2026rcnf]]
- [[zheng2026pokevla]]
- [[you2026dotsim]]
- [[wu2026affordgrasp]]
- [[tong2024ovalprompt]]
- [[tang2025uad]]
- [[tang2025kalie]]
