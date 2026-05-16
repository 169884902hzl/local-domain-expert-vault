---
title: "Learning to Optimize"
tags: [concept, optimization, learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "用神经网络学习优化过程的内部决策（参数调节、热启动、结构自适应），而非依赖手工规则"
---

## Definition

Learning to Optimize is maintained here as an evidence-linked concept. 用神经网络学习优化过程的内部决策（参数调节、热启动、结构自适应），而非依赖手工规则

## Key Ideas

- Direct local evidence currently comes from [[yu2026atrs]].
- The concept is tracked with local tags: concept, optimization, learning.
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
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[liu2025kuda]] (broader context): 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为...
- [[liu2025autonomous]] (broader context): 提出 RLAC 框架，用 DRL（PPO）在仿真中训练 actor 网络指导 Jacobian-based adaptive control 的初始化和预调整。核心思路：RL...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[chen2025effective]] (broader context): 提出 S2I 框架，将混合质量演示在片段级别进行分割、对比学习选择高质量片段、贪心轨迹优化低质量片段，仅用 3 条专家演示即可为多种下游策略（BC-RNN/DP/ACT/RI...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线

## Evidence Map

- Direct evidence papers: [[yu2026atrs]].
- Broader local evidence context: [[yu2026atrs]], [[zhang2026generative]], [[liu2025kuda]], [[liu2025autonomous]], [[chi2024diffusion]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[admm]]
- [[parallel-trajectory-optimization]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[yu2026atrs]]
- [[zhang2026generative]]
- [[liu2025kuda]]
- [[liu2025autonomous]]
- [[chi2024diffusion]]
- [[chen2025effective]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
