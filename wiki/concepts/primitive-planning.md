---
title: "Primitive-Based Task Planning"
tags: [task-planning, primitives, hierarchical-control]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "将操控任务分解为可复用的原子操作原语序列，通过符号化计划实现结构化执行"
---

## Definition

Primitive-Based Task Planning is maintained here as an evidence-linked concept. 将操控任务分解为可复用的原子操作原语序列，通过符号化计划实现结构化执行

## Key Ideas

- Direct local evidence currently comes from [[zhu2026nsvla]].
- The concept is tracked with local tags: task-planning, primitives, hierarchical-control.
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

- [[zhu2026nsvla]] (direct evidence): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[nazarczuk2025closed]] (broader context): 提出 CLIER 闭环交互式具身推理框架：神经符号方法处理需要视觉+物理属性测量的长时序操控任务。Seq2Seq 语言→符号程序→场景图→Transformer 动作规划器→...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[liu820enhancing]] (broader context): 提出 LLM+HRC 框架：GPT-4 分解高层指令为子任务序列→选择运动函数→结合 YOLOv5 感知的环境信息生成可执行代码。对于 LLM 无法处理的复杂轨迹（如水平铰链...
- [[garcia2025generalizable]] (broader context): 提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...

## Evidence Map

- Direct evidence papers: [[zhu2026nsvla]].
- Broader local evidence context: [[zhu2026nsvla]], [[zhang2026prts]], [[nazarczuk2025closed]], [[missal2026ropedreamer]], [[liu820enhancing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[neuro-symbolic-learning]]
- [[robotic-manipulation]]
- [[hierarchical-rl]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhu2026nsvla]]
- [[zhang2026prts]]
- [[nazarczuk2025closed]]
- [[missal2026ropedreamer]]
- [[liu820enhancing]]
- [[garcia2025generalizable]]
- [[zhi2025closedloop]]
- [[zeng2026recapa]]
