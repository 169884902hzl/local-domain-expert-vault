---
title: "Conformal Prediction"
tags: [concept, uncertainty, calibration]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "分布无关的统计校准方法，通过 split-conformal regression 提供有限样本覆盖率保证，用于量化预测不确定性"
---

## Definition

Conformal Prediction is maintained here as an evidence-linked concept. 分布无关的统计校准方法，通过 split-conformal regression 提供有限样本覆盖率保证，用于量化预测不确定性

## Key Ideas

- Direct local evidence currently comes from [[puthumanaillam2026muninn]].
- The concept is tracked with local tags: concept, uncertainty, calibration.
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

- [[puthumanaillam2026muninn]] (direct evidence): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...

## Evidence Map

- Direct evidence papers: [[puthumanaillam2026muninn]].
- Broader local evidence context: [[puthumanaillam2026muninn]], [[zhu2024scaling]], [[zhou2026ego]], [[zhang2026world2minecraft]], [[zhang2026prts]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[denoiser-caching]]
- [[adaptive-compute]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[puthumanaillam2026muninn]]
- [[zhu2024scaling]]
- [[zhou2026ego]]
- [[zhang2026world2minecraft]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[yuan2026prefmoe]]
- [[yang2026twintrack]]
