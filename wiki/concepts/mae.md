---
title: "Masked Autoencoder (MAE)"
tags: [visual-representation, pre-training, self-supervised]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "基于掩码重建的自监督视觉预训练方法，通过随机遮蔽图像 patch 并重建来学习视觉表征，已被广泛用于机器人视觉编码器预训练。"
---

## Definition

Masked Autoencoder (MAE) is maintained here as an evidence-linked concept. 基于掩码重建的自监督视觉预训练方法，通过随机遮蔽图像 patch 并重建来学习视觉表征，已被广泛用于机器人视觉编码器预训练。

## Key Ideas

- Direct local evidence currently comes from [[li2026h2r]].
- The concept is tracked with local tags: visual-representation, pre-training, self-supervised.
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

- [[li2026h2r]] (direct evidence): H2R 通过 HaMeR+SAM+LaMa 管线将第一人称人类手部视频替换为机器人手臂渲染帧，缩小人机视觉域差异，在仿真和真实双臂/灵巧手操控任务上实现 1.3%-23.3%...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...
- [[yang2026physforge]] (broader context): 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。
- [[wang2026ocra]] (broader context): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[han2025upvital]] (broader context): 提出 UpViTaL 框架，利用非配对视觉-触觉数据通过自监督表示学习辅助 RL 灵巧操控。核心设计：(1) LSTM 触觉自编码器从时序触觉序列学习触觉表示；(2) MAE...
- [[dong2025vitavla]] (broader context): 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[li2026h2r]].
- Broader local evidence context: [[li2026h2r]], [[zhang2026recurrent]], [[yang2026physforge]], [[wang2026ocra]], [[han2025upvital]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[r3m]]
- [[imitation-learning]]
- [[visual-reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[li2026h2r]]
- [[zhang2026recurrent]]
- [[yang2026physforge]]
- [[wang2026ocra]]
- [[han2025upvital]]
- [[dong2025vitavla]]
- [[consortium2026openhembodiment]]
- [[zhu2026nsvla]]
