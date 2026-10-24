---
title: "VQ-VAE"
tags: [representation-learning, discrete-representation, autoencoder]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "向量量化变分自编码器，将连续输入映射到离散码本空间学习紧凑离散表示。"
---

## Definition

VQ-VAE is maintained here as an evidence-linked concept. 向量量化变分自编码器，将连续输入映射到离散码本空间学习紧凑离散表示。

## Key Ideas

- Direct local evidence currently comes from [[wang2026beyond]].
- The concept is tracked with local tags: representation-learning, discrete-representation, autoencoder.
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

- [[wang2026beyond]] (direct evidence): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[zhao2023finegrained]] (broader context): 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即...
- [[wu2026affordgrasp]] (broader context): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[wu2025discrete]] (broader context): 提出 Discrete Policy，将连续动作空间解耦为离散潜空间用于多任务机器人操控。三步流程：(1) VQ-VAE 编码器将连续动作序列量化为离散码序列（codeboo...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[fan2026xr1]] (broader context): 提出 XR-1 双分支 VQ-VAE（视觉+运动），学习统一视觉-运动编码 UVMC，跨模态 KL 对齐损失
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: [[wang2026beyond]].
- Broader local evidence context: [[wang2026beyond]], [[zhao2023finegrained]], [[wu2026affordgrasp]], [[wu2025discrete]], [[gu2026vistabot]], [[fan2026xr1]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vq-memory]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026beyond]]
- [[zhao2023finegrained]]
- [[wu2026affordgrasp]]
- [[wu2025discrete]]
- [[gu2026vistabot]]
- [[fan2026xr1]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
