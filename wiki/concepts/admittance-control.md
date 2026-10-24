---
title: "Admittance Control"
tags: [control, manipulation, contact-rich]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "导纳控制通过虚拟弹簧-质量-阻尼模型实现任务空间柔顺控制，使末端执行器在接触时顺应外力同时跟踪目标命令。"
---

## Definition

Admittance Control is maintained here as an evidence-linked concept. 导纳控制通过虚拟弹簧-质量-阻尼模型实现任务空间柔顺控制，使末端执行器在接触时顺应外力同时跟踪目标命令。

## Key Ideas

- Direct local evidence currently comes from [[sha2026efficient]].
- The concept is tracked with local tags: control, manipulation, contact-rich.
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

- [[sha2026efficient]] (direct evidence): 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...

## Evidence Map

- Direct evidence papers: [[sha2026efficient]].
- Broader local evidence context: [[sha2026efficient]], [[zhu2024scaling]], [[zhou2026vlbiman]], [[zheng120dottip]], [[zhao2025polytouch]].
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
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[sha2026efficient]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zheng120dottip]]
- [[zhao2025polytouch]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[zhang2026joyaira]]
