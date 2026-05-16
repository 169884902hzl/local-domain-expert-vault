---
title: "Trajectory Optimization"
tags: [planning, optimization, control]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "通过求解约束优化问题生成机器人运动轨迹的方法，目标函数通常包含光滑性和能量项，约束包括碰撞避障和动力学限制。"
---

## Definition

Trajectory Optimization is maintained here as an evidence-linked concept. 通过求解约束优化问题生成机器人运动轨迹的方法，目标函数通常包含光滑性和能量项，约束包括碰撞避障和动力学限制。

## Key Ideas

- Direct local evidence currently comes from [[sundaralingam2026curobov2]].
- The concept is tracked with local tags: planning, optimization, control.
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

- [[sundaralingam2026curobov2]] (direct evidence): 统一 GPU-native 运动生成框架，通过 B-spline 轨迹优化、密集 ESDF 感知管线和可扩展 whole-body 计算，实现从单臂到 48-DoF 人形机器...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...

## Evidence Map

- Direct evidence papers: [[sundaralingam2026curobov2]].
- Broader local evidence context: [[sundaralingam2026curobov2]], [[zhou2025oneshot]], [[yu2026atrs]], [[zhou2026rcnf]], [[zeng2026recapa]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[contact-implicit-trajectory-optimization]]
- [[planning]]
- [[robotic-manipulation]]
- [[deformable-linear-object]]
## Related Papers

- [[li2026impact]]