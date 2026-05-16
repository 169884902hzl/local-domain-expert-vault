---
title: "MPPI (Model Predictive Path Integral)"
tags: [concept, planning, control]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "基于路径积分的采样式模型预测控制算法，通过大量随机扰动轨迹的指数加权平均求解随机最优控制问题。"
---

## Definition

MPPI (Model Predictive Path Integral) is maintained here as an evidence-linked concept. 基于路径积分的采样式模型预测控制算法，通过大量随机扰动轨迹的指数加权平均求解随机最优控制问题。

## Key Ideas

- Direct local evidence currently comes from [[iek2026coral]].
- The concept is tracked with local tags: concept, planning, control.
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

- [[iek2026coral]] (direct evidence): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[lee2026implicit]] (direct evidence): 用 IMLE 替代高斯提案分布作为 MPPI 的多模态轨迹生成器，在行人导航中实现 50 Hz 实时规划
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...

## Evidence Map

- Direct evidence papers: [[iek2026coral]], [[lee2026implicit]].
- Broader local evidence context: [[iek2026coral]], [[lee2026implicit]], [[mitrano2024grasp]], [[zhou2025oneshot]], [[zhang2026prts]], [[zeng2026recapa]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[model-predictive-control]]
- [[planning]]
- [[contact-rich-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[iek2026coral]]
- [[lee2026implicit]]
- [[mitrano2024grasp]]
- [[zhou2025oneshot]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[yu2026atrs]]
- [[yang2026ultradexgrasp]]
- [[xu2026roboagent]]
