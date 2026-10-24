---
title: "Embodied Question Answering"
tags: [embodied-ai, VLM, question-answering]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "智能体在 3D 环境中导航以收集视觉证据并回答自然语言问题的任务范式"
---

## Definition

Embodied Question Answering is maintained here as an evidence-linked concept. 智能体在 3D 环境中导航以收集视觉证据并回答自然语言问题的任务范式

## Key Ideas

- Direct local evidence currently comes from [[sakamoto2026e3vsbench]].
- The concept is tracked with local tags: embodied-ai, VLM, question-answering.
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

- [[sakamoto2026e3vsbench]] (direct evidence): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[brohan2023rt2]] (broader context): Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...

## Evidence Map

- Direct evidence papers: [[sakamoto2026e3vsbench]].
- Broader local evidence context: [[sakamoto2026e3vsbench]], [[brohan2023rt2]], [[zheng2026pokevla]], [[zhang2026joyaira]], [[zeng2026recapa]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[active-perception]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[sakamoto2026e3vsbench]]
- [[brohan2023rt2]]
- [[zheng2026pokevla]]
- [[zhang2026joyaira]]
- [[zeng2026recapa]]
- [[yin2026multiple]]
- [[wang2026visionlanguageaction]]
- [[wang2026evolvable]]
