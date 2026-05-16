---
title: "VLM-as-a-Judge"
tags: [evaluation, VLM, benchmark]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "使用 VLM 作为评判模型评估开放式回答的方法，通过语义对齐打分替代精确匹配"
---

## Definition

VLM-as-a-Judge is maintained here as an evidence-linked concept. 使用 VLM 作为评判模型评估开放式回答的方法，通过语义对齐打分替代精确匹配

## Key Ideas

- Direct local evidence currently comes from [[sakamoto2026e3vsbench]].
- The concept is tracked with local tags: evaluation, VLM, benchmark.
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
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[wang2025vlaadapter]] (broader context): 提出 VLA-Adapter，系统分析 VLA 模型中 VL→A 桥接范式的有效性。发现中间层 Raw 特征优于深层（语义偏差）、深层 ActionQuery 最优、多层特征...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[tong2024ovalprompt]] (broader context): 提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词...

## Evidence Map

- Direct evidence papers: [[sakamoto2026e3vsbench]].
- Broader local evidence context: [[sakamoto2026e3vsbench]], [[zheng2026pokevla]], [[zhang2026joyaira]], [[yin2026multiple]], [[wang2026evolvable]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[sakamoto2026e3vsbench]]
- [[zheng2026pokevla]]
- [[zhang2026joyaira]]
- [[yin2026multiple]]
- [[wang2026evolvable]]
- [[wang2025vlaadapter]]
- [[vo2026codegraphvlp]]
- [[tong2024ovalprompt]]
