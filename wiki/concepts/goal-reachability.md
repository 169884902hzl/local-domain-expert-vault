---
title: "Goal Reachability"
tags: [reinforcement-learning, planning, VLA]
created: "2026-05-01"
updated: "2026-05-01"
type: "concept"
status: "done"
summary: "从当前状态-动作对出发，最终实现语言指定目标的概率估计，超越静态语义匹配的时序可达性度量。"
---

## Definition

Goal Reachability is maintained here as an evidence-linked concept. 从当前状态-动作对出发，最终实现语言指定目标的概率估计，超越静态语义匹配的时序可达性度量。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026prts]].
- The concept is tracked with local tags: reinforcement-learning, planning, VLA.
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

- [[zhang2026prts]] (direct evidence): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%

## Evidence Map

- Direct evidence papers: [[zhang2026prts]].
- Broader local evidence context: [[zhang2026prts]], [[zeng2026recapa]], [[mitrano2024grasp]], [[zhou2025oneshot]], [[yu2026atrs]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[contrastive-reinforcement-learning]]
- [[long-horizon-manipulation]]
- [[vision-language-action]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[mitrano2024grasp]]
- [[zhou2025oneshot]]
- [[yu2026atrs]]
- [[vo2026codegraphvlp]]
- [[sakamoto2026e3vsbench]]
- [[missal2026ropedreamer]]
