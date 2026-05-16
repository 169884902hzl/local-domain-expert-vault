---
title: "Masked Autoencoder"
tags: [concept]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "掩码自编码器（MAE），通过随机遮蔽输入token并重建的自监督学习范式"
---

## Definition

Masked Autoencoder is maintained here as an evidence-linked concept. 掩码自编码器（MAE），通过随机遮蔽输入token并重建的自监督学习范式

## Key Ideas

- Direct local evidence currently comes from [[wang2026ocra]].
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

- [[wang2026ocra]] (direct evidence): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[shah2025acoustic]] (broader context): 将机器人操控扩展到声波场：通过控制稀疏圆柱形散射体的位置（2D 平面内），实现对 1D 声波场的聚焦和抑制。方法：(1) Physics-informed autoencod...
- [[jiang2024manipulation]] (broader context): 提出 CLIPU2Net 轻量级参考图像分割模型（6.6MB 解码器），集成到手眼视觉伺服系统，通过几何约束（点-点、点-线、线-线、平行线）将语言指令转化为机器人动作。GP...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: [[wang2026ocra]].
- Broader local evidence context: [[wang2026ocra]], [[wu2025imperfect]], [[wang2026beyond]], [[shah2025acoustic]], [[jiang2024manipulation]].
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
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]
- [[sim-to-real]]

## Related Papers

- [[wang2026ocra]]
- [[wu2025imperfect]]
- [[wang2026beyond]]
- [[shah2025acoustic]]
- [[jiang2024manipulation]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
