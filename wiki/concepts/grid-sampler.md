---
title: "GridS (Differentiable Grid Sampler)"
tags: [VLA, token-pruning, differentiable-sampling]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "GridS 是一种即插即用的可微视觉 token 采样模块，通过连续坐标预测和双线性插值实现 VLA 的高效压缩，在 76% FLOPs 削减下保持操控性能。"
---

## Definition

GridS (Differentiable Grid Sampler) is maintained here as an evidence-linked concept. GridS 是一种即插即用的可微视觉 token 采样模块，通过连续坐标预测和双线性插值实现 VLA 的高效压缩，在 76% FLOPs 削减下保持操控性能。

## Key Ideas

- Direct local evidence currently comes from [[feng2026see]].
- The concept is tracked with local tags: VLA, token-pruning, differentiable-sampling.
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

- [[feng2026see]] (direct evidence): GridS 提出可微双线性网格采样模块，将 VLA 视觉 token 从 256 压缩至 16（甚至 1），通过端到端优化的连续坐标预测保留亚 patch 级空间精度，在 7...
- [[ziakas2026aligning]] (broader context): 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12...
- [[puthumanaillam2026muninn]] (broader context): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[kuroki2025gendom]] (broader context): 提出 GenDOM，通过将策略条件化于可变形物体参数（Young's modulus + Poisson's ratio）实现 one-shot 泛化。在可微分物理仿真器中用...
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[chang2026partially]] (broader context): 提出部分群等变 MDP（PI-MDP）框架，通过门控函数在对称区域使用等变 Bellman 备份、在对称破缺区域回退标准备份，显著提升 RL 的样本效率和鲁棒性；发表于 IC...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...

## Evidence Map

- Direct evidence papers: [[feng2026see]].
- Broader local evidence context: [[feng2026see]], [[ziakas2026aligning]], [[puthumanaillam2026muninn]], [[kuroki2025gendom]], [[he2026generative]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[deformable-attention]]
- [[information-bottleneck]]
- [[dinov2]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[feng2026see]]
- [[ziakas2026aligning]]
- [[puthumanaillam2026muninn]]
- [[kuroki2025gendom]]
- [[he2026generative]]
- [[chang2026partially]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
