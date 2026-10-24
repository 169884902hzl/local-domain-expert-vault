---
title: "Contact-Implicit Trajectory Optimization (CITO)"
tags: [trajectory-optimization, contact-rich, MPC]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "不预设接触模式序列，将接触动力学（法向/切向互补约束）直接嵌入轨迹优化的规划框架。"
---

## Definition

Contact-Implicit Trajectory Optimization (CITO) is maintained here as an evidence-linked concept. 不预设接触模式序列，将接触动力学（法向/切向互补约束）直接嵌入轨迹优化的规划框架。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: trajectory-optimization, contact-rich, MPC.
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

- [[li2026impact]] (broader context): 提出 IMPACT 方法，基于保护增广拉格朗日 (safeguarded AuLa) 框架求解 MPCC 形式的接触隐式轨迹优化，通过隐式接触分支选择在迭代中自动发现接触模式...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[kumar122constraining]] (broader context): 提出 COGIS 方法，在部分可观测环境中在线学习障碍物几何模型（GPIS）并通过约束优化精化数据集。利用名义动力学模型预测与实际状态差异推断接触点，结合视觉预处理/后处理清...
- [[chen2026posterior]] (broader context): POCO 将生成式策略改进建模为免似然的 chunk 级后验推断问题，通过 Implicit E-M 和裁剪代理目标实现离线到在线的稳定高效微调，7 仿真 + 6 真实任务上...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[li2026impact]], [[zhou2025oneshot]], [[kumar122constraining]], [[chen2026posterior]], [[zhou2026sim1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[trajectory-optimization]]
- [[planning]]
- [[robotic-manipulation]]
- [[deformable-linear-object]]
## Related Papers

- [[li2026impact]]