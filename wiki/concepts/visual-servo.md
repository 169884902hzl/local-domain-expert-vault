---
title: "Visual Servo"
tags: [vision, control, manipulation]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "利用视觉反馈（目标检测/分割）闭环控制机器人末端执行器位置的技术。"
---

## Definition

Visual Servo is maintained here as an evidence-linked concept. 利用视觉反馈（目标检测/分割）闭环控制机器人末端执行器位置的技术。

## Key Ideas

- Direct local evidence currently comes from [[schperberg2026mobius]].
- The concept is tracked with local tags: vision, control, manipulation.
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

- [[schperberg2026mobius]] (direct evidence): 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模...
- [[jiang2024manipulation]] (broader context): 提出 CLIPU2Net 轻量级参考图像分割模型（6.6MB 解码器），集成到手眼视觉伺服系统，通过几何约束（点-点、点-线、线-线、平行线）将语言指令转化为机器人动作。GP...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...

## Evidence Map

- Direct evidence papers: [[schperberg2026mobius]].
- Broader local evidence context: [[schperberg2026mobius]], [[jiang2024manipulation]], [[zhu2026nsvla]], [[zhou2026vlbiman]], [[zhou2026ego]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[schperberg2026mobius]]
- [[jiang2024manipulation]]
- [[zhu2026nsvla]]
- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[zhi102unifying]]
- [[zheng120dottip]]
- [[zhao2026vitactracing]]
