---
title: "Video Generation"
tags: [concept, generative-model, video]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "基于扩散模型等生成模型合成视频帧序列的技术，在机器人领域用作视觉规划器或动力学模型。"
---

## Definition

Video Generation is maintained here as an evidence-linked concept. 基于扩散模型等生成模型合成视频帧序列的技术，在机器人领域用作视觉规划器或动力学模型。

## Key Ideas

- Direct local evidence currently comes from [[luo2026selfimproving]].
- The concept is tracked with local tags: concept, generative-model, video.
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

- [[luo2026selfimproving]] (direct evidence): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[wang2026visionlanguageaction]] (broader context): 首篇从数据基础设施视角系统分析 VLA 的综述，围绕数据集、基准和数据引擎三大支柱，揭示保真度-成本权衡、推理评估缺失和生成-接地失衡等核心瓶颈
- [[ma2026human]] (broader context): 系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[dai2024racer]] (broader context): 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GP...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[luo2026selfimproving]].
- Broader local evidence context: [[luo2026selfimproving]], [[xie2026humanintention]], [[wang2026visionlanguageaction]], [[ma2026human]], [[lee2026implicit]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[visual-planning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[luo2026selfimproving]]
- [[xie2026humanintention]]
- [[wang2026visionlanguageaction]]
- [[ma2026human]]
- [[lee2026implicit]]
- [[dai2024racer]]
- [[consortium2026openhembodiment]]
- [[zhu2026nsvla]]
