---
title: "Visual-Language Grounding (VLG)"
tags: [concept, VLM, grounding]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "建立自然语言与视觉实体之间的语义对应关系，使模型能根据文本指令准确定位目标物体。"
---

## Definition

Visual-Language Grounding (VLG) is maintained here as an evidence-linked concept. 建立自然语言与视觉实体之间的语义对应关系，使模型能根据文本指令准确定位目标物体。

## Key Ideas

- Direct local evidence currently comes from [[li2026realvlgr1]].
- The concept is tracked with local tags: concept, VLM, grounding.
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

- [[li2026realvlgr1]] (direct evidence): 构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[kim2024openvla]] (broader context): Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...

## Evidence Map

- Direct evidence papers: [[li2026realvlgr1]].
- Broader local evidence context: [[li2026realvlgr1]], [[yin2026multiple]], [[vo2026codegraphvlp]], [[kim2024openvla]], [[aida2026cortex]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[spatial-grounding]]
- [[vision-language-model]]
- [[grasping]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026realvlgr1]]
- [[yin2026multiple]]
- [[vo2026codegraphvlp]]
- [[kim2024openvla]]
- [[aida2026cortex]]
- [[zhu2026nsvla]]
- [[zheng2026pokevla]]
- [[zhang2026visionlanguageaction]]
