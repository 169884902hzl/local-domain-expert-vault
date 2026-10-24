---
title: "Neural SDF (Signed Distance Function)"
tags: [concept]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "用神经网络参数化有符号距离函数，表示任意形状物体的隐式几何"
---

## Definition

Neural SDF (Signed Distance Function) is maintained here as an evidence-linked concept. 用神经网络参数化有符号距离函数，表示任意形状物体的隐式几何

## Key Ideas

- Direct local evidence currently comes from [[yang2026twintrack]].
- The concept is tracked with local tags: concept.
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

- [[yang2026twintrack]] (direct evidence): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...
- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]] (broader context): 提出PNPF框架，用闭环相位变量条件化神经势函数以解决DS-LfD中轨迹交叉与状态重访问题，在2D/6D任务和真实UR10机器人上超越CONDOR与NODE
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...

## Evidence Map

- Direct evidence papers: [[yang2026twintrack]].
- Broader local evidence context: [[yang2026twintrack]], [[Reactive Motion Generation via Phase-varying Neural Potential Functions]], [[zhu2024scaling]], [[zhi102unifying]], [[zheng120dottip]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[gaussian-splatting]]
- [[real-to-sim]]
- [[contact-rich-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[yang2026twintrack]]
- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[zhu2024scaling]]
- [[zhi102unifying]]
- [[zheng120dottip]]
- [[yu2026atrs]]
- [[xiao2026avavla]]
- [[wu2025imperfect]]
