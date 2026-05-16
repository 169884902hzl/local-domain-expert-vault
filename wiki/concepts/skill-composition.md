---
title: "Skill Composition"
tags: [manipulation, planning, generalization]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "将已学习的原子操控技能（如 pick、place、push）组合为长时序任务的策略，核心挑战是底层策略在场景组合时的分布偏移。"
---

## Definition

Skill Composition is maintained here as an evidence-linked concept. 将已学习的原子操控技能（如 pick、place、push）组合为长时序任务的策略，核心挑战是底层策略在场景组合时的分布偏移。

## Key Ideas

- Direct local evidence currently comes from [[qi2026compose]].
- The concept is tracked with local tags: manipulation, planning, generalization.
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

- [[qi2026compose]] (direct evidence): 提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Polic...
- [[huang2026mimic]] (broader context): 提出频域多尺度 action tokenizer (SDAT)，通过 DCT 频谱分解将行为意图与执行细节解耦，实现意图驱动的模仿学习、one-shot 技能迁移和泛化增强
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...

## Evidence Map

- Direct evidence papers: [[qi2026compose]].
- Broader local evidence context: [[qi2026compose]], [[huang2026mimic]], [[missal2026ropedreamer]], [[zhou2025oneshot]], [[zhang2026prts]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[scene-graph]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[qi2026compose]]
- [[huang2026mimic]]
- [[missal2026ropedreamer]]
- [[zhou2025oneshot]]
- [[zhang2026prts]]
- [[yang2026ultradexgrasp]]
- [[vo2026codegraphvlp]]
- [[mitrano2024grasp]]
