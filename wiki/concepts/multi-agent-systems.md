---
title: "Multi-Agent Systems"
tags: [multi-agent, collaboration, robotics]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "多个机器人智能体协同完成操控任务的系统，涉及空间协调、时序推理和共享工作空间感知。"
---

## Definition

Multi-Agent Systems is maintained here as an evidence-linked concept. 多个机器人智能体协同完成操控任务的系统，涉及空间协调、时序推理和共享工作空间感知。

## Key Ideas

- Direct local evidence currently comes from [[kang2026coenv]].
- The concept is tracked with local tags: multi-agent, collaboration, robotics.
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

- [[kang2026coenv]] (direct evidence): 提出 Compositional Environment 范式，将真实场景与仿真环境融合为统一决策空间，通过 Real-to-Sim 重建、VLM 驱动的双层规划（Inter...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[sakamoto2026e3vsbench]] (broader context): 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题...
- [[nazarczuk2025closed]] (broader context): 提出 CLIER 闭环交互式具身推理框架：神经符号方法处理需要视觉+物理属性测量的长时序操控任务。Seq2Seq 语言→符号程序→场景图→Transformer 动作规划器→...
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...

## Evidence Map

- Direct evidence papers: [[kang2026coenv]].
- Broader local evidence context: [[kang2026coenv]], [[zeng2026recapa]], [[zhi102unifying]], [[yu2026atrs]], [[ye2026generation]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[compositional-environment]]
- [[bimanual-manipulation]]
- [[robotic-manipulation]]
- [[planning]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[kang2026coenv]]
- [[zeng2026recapa]]
- [[zhi102unifying]]
- [[yu2026atrs]]
- [[ye2026generation]]
- [[sakamoto2026e3vsbench]]
- [[nazarczuk2025closed]]
- [[luijkx2026llmguided]]
