---
title: "ControlNet"
tags: [concept, diffusion, conditioning]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "向预训练扩散模型注入结构化条件信号（如边缘、姿态、渲染视频）的残差控制架构。"
---

## Definition

ControlNet is maintained here as an evidence-linked concept. 向预训练扩散模型注入结构化条件信号（如边缘、姿态、渲染视频）的残差控制架构。

## Key Ideas

- Direct local evidence currently comes from [[jia2026dreamplan]].
- The concept is tracked with local tags: concept, diffusion, conditioning.
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

- [[jia2026dreamplan]] (direct evidence): 通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwe...
- [[chen2026ropa]] (broader context): ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[zhang2026touchguide]] (broader context): 提出 TouchGuide 范式，在推理时用任务特定触觉物理模型（CPM）通过对比学习训练的可行性分数引导扩散/flow-matching 视觉运动策略的去噪过程，实现动作空...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head

## Evidence Map

- Direct evidence papers: [[jia2026dreamplan]].
- Broader local evidence context: [[jia2026dreamplan]], [[chen2026ropa]], [[zhu2024scaling]], [[zhou2026sim1]], [[zhao2025polytouch]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[video-diffusion-model]]
- [[video-world-model]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jia2026dreamplan]]
- [[chen2026ropa]]
- [[zhu2024scaling]]
- [[zhou2026sim1]]
- [[zhao2025polytouch]]
- [[zhang2026touchguide]]
- [[zhang2026handx]]
- [[zhang2026generative]]
