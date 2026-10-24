---
title: "Parallel Trajectory Optimization"
tags: [concept, planning, optimization]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "利用并行计算加速长时序轨迹优化的方法族，通过 ADMM 等框架将轨迹分段后并行求解"
---

## Definition

Parallel Trajectory Optimization is maintained here as an evidence-linked concept. 利用并行计算加速长时序轨迹优化的方法族，通过 ADMM 等框架将轨迹分段后并行求解

## Key Ideas

- Direct local evidence currently comes from [[yu2026atrs]].
- The concept is tracked with local tags: concept, planning, optimization.
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

- [[yu2026atrs]] (direct evidence): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[liu2026longhorizon]] (broader context): 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反...
- [[aida2026cortex]] (broader context): Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xie102multiview]] (broader context): 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减...

## Evidence Map

- Direct evidence papers: [[yu2026atrs]].
- Broader local evidence context: [[yu2026atrs]], [[zhou2025oneshot]], [[zeng2026recapa]], [[vo2026codegraphvlp]], [[liu2026longhorizon]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[admm]]
- [[planning]]
- [[reinforcement-learning]]
- [[learning-to-optimize]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[yu2026atrs]]
- [[zhou2025oneshot]]
- [[zeng2026recapa]]
- [[vo2026codegraphvlp]]
- [[liu2026longhorizon]]
- [[aida2026cortex]]
- [[zhang2026generative]]
- [[xie102multiview]]
