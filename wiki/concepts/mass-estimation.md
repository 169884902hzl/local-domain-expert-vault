---
title: "Mass Estimation"
tags: [physical-reasoning, manipulation, VLM]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "从视觉观测估计物体质量的技术，对机器人抓取力控制至关重要。"
---

## Definition

Mass Estimation is maintained here as an evidence-linked concept. 从视觉观测估计物体质量的技术，对机器人抓取力控制至关重要。

## Key Ideas

- Direct local evidence currently comes from [[yokomizo2026physquantagent]].
- The concept is tracked with local tags: physical-reasoning, manipulation, VLM.
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

- [[yokomizo2026physquantagent]] (direct evidence): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[wang2026phys2real]] (broader context): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...
- [[yin2026genie]] (broader context): Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 100...
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[wang2026while]] (broader context): 提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机...
- [[tang2025kalie]] (broader context): 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的...
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...

## Evidence Map

- Direct evidence papers: [[yokomizo2026physquantagent]].
- Broader local evidence context: [[yokomizo2026physquantagent]], [[wang2026phys2real]], [[yin2026genie]], [[yang2026rise]], [[wang2026while]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[visual-prompting]]
- [[physical-reasoning]]
- [[grasping]]
- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]

## Related Papers

- [[yokomizo2026physquantagent]]
- [[wang2026phys2real]]
- [[yin2026genie]]
- [[yang2026rise]]
- [[wang2026while]]
- [[tang2025kalie]]
- [[li2026affordsim]]
- [[iek2026coral]]
