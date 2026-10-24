---
title: "Compositional Environment"
tags: [sim-to-real, multi-agent, planning]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "融合真实世界与仿真组件的统一决策空间，使多智能体在共享虚拟空间中规划、验证和优化协作策略。"
---

## Definition

Compositional Environment is maintained here as an evidence-linked concept. 融合真实世界与仿真组件的统一决策空间，使多智能体在共享虚拟空间中规划、验证和优化协作策略。

## Key Ideas

- Direct local evidence currently comes from [[kang2026coenv]].
- The concept is tracked with local tags: sim-to-real, multi-agent, planning.
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
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2025simtoreal]] (broader context): 针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算...

## Evidence Map

- Direct evidence papers: [[kang2026coenv]].
- Broader local evidence context: [[kang2026coenv]], [[yu2026atrs]], [[wang2026visionlanguageaction]], [[zhou2025oneshot]], [[luijkx2026llmguided]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[sim-to-real]]
- [[multi-agent-systems]]
- [[real-to-sim]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[kang2026coenv]]
- [[yu2026atrs]]
- [[wang2026visionlanguageaction]]
- [[zhou2025oneshot]]
- [[luijkx2026llmguided]]
- [[zeng2026recapa]]
- [[ye2026generation]]
- [[yang2025simtoreal]]
