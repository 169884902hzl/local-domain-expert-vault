---
title: "Behavioral Mode Discovery"
tags: [concept, diffusion-policy, multimodal-policy, rl-finetuning]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "通过无监督方式从预训练生成策略的潜在噪声空间中发现和组织轨迹级行为模式，以互信息为代理指标进行RL微调正则化。"
---

## Definition

Behavioral Mode Discovery is maintained here as an evidence-linked concept. 通过无监督方式从预训练生成策略的潜在噪声空间中发现和组织轨迹级行为模式，以互信息为代理指标进行RL微调正则化。

## Key Ideas

- Direct local evidence currently comes from [[longhini2026behavioral]].
- The concept is tracked with local tags: concept, diffusion-policy, multimodal-policy, rl-finetuning.
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

- [[longhini2026behavioral]] (direct evidence): 提出BMD框架，通过无监督发现扩散策略潜在噪声空间中的行为模式，以互信息作为内在奖励正则化RL微调，在保持多模态行为多样性的同时提升任务成功率。
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[sha2026efficient]] (broader context): 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插...
- [[niu2026versatile]] (broader context): 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[longhini2026behavioral]].
- Broader local evidence context: [[longhini2026behavioral]], [[wu2026continually]], [[sha2026efficient]], [[niu2026versatile]], [[ziakas2026aligning]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-policy]]
- [[mode-collapse]]
- [[steering-policy]]
- [[multimodal-policy]]
- [[skill-discovery]]
- [[robotic-manipulation]]

## Related Papers

- [[longhini2026behavioral]]
- [[wu2026continually]]
- [[sha2026efficient]]
- [[niu2026versatile]]
- [[ziakas2026aligning]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026sim1]]
