---
title: "Human Video Learning (LfHV)"
tags: [imitation-learning, robot-learning, video-learning]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "从人类活动视频中被动学习机器人操控技能的研究范式，通过 task/observation/action 三层迁移路径解决人-机器人跨体态问题。"
---

## Definition

Human Video Learning (LfHV) is maintained here as an evidence-linked concept. 从人类活动视频中被动学习机器人操控技能的研究范式，通过 task/observation/action 三层迁移路径解决人-机器人跨体态问题。

## Key Ideas

- Direct local evidence currently comes from [[ma2026human]].
- The concept is tracked with local tags: imitation-learning, robot-learning, video-learning.
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

- [[ma2026human]] (direct evidence): 系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...

## Evidence Map

- Direct evidence papers: [[ma2026human]].
- Broader local evidence context: [[ma2026human]], [[zhang2026joyaira]], [[xie2026humanintention]], [[consortium2026openhembodiment]], [[zhao2025polytouch]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[affordance-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[ma2026human]]
- [[zhang2026joyaira]]
- [[xie2026humanintention]]
- [[consortium2026openhembodiment]]
- [[zhao2025polytouch]]
- [[xue2026tube]]
- [[wang2026visionlanguageaction]]
- [[smith2024steer]]
