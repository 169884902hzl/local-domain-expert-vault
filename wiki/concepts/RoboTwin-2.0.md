---
title: "RoboTwin 2.0 Benchmark"
tags: [benchmark, bimanual-manipulation, simulation]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "双臂操控仿真基准，包含 50 个双臂协作任务，具有强域随机化机制，用于评估 VLA 模型的双臂协调能力。"
---

## Definition

RoboTwin 2.0 Benchmark is maintained here as an evidence-linked concept. 双臂操控仿真基准，包含 50 个双臂协作任务，具有强域随机化机制，用于评估 VLA 模型的双臂协调能力。

## Key Ideas

- Direct local evidence currently comes from [[wang2026vlathinker]].
- The concept is tracked with local tags: benchmark, bimanual-manipulation, simulation.
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

- [[wang2026vlathinker]] (direct evidence): 首个\"thinking-with-image\"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRP...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[feng2026demystifying]] (broader context): 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真...
- [[dong2025vitavla]] (broader context): 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token...
- [[chen2025benchmarking]] (broader context): RoboTwin 双臂协作挑战赛（CVPR 2025 MEIS Workshop）技术报告。基于 RoboTwin 仿真平台（1.0/2.0）和 AgileX COBOT-M...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...

## Evidence Map

- Direct evidence papers: [[wang2026vlathinker]].
- Broader local evidence context: [[wang2026vlathinker]], [[zhong2026vlaopd]], [[zhang2026joyaira]], [[yin2026multiple]], [[feng2026demystifying]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action-model]]
- [[bimanual-manipulation]]
- [[LIBERO-benchmark]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026vlathinker]]
- [[zhong2026vlaopd]]
- [[zhang2026joyaira]]
- [[yin2026multiple]]
- [[feng2026demystifying]]
- [[dong2025vitavla]]
- [[chen2025benchmarking]]
- [[aida2026cortex]]
