---
title: "Canny Edge Detection"
tags: [concept, computer-vision]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "经典边缘检测算法，通过多阶段处理（噪声抑制、梯度计算、非极大值抑制、双阈值检测）提取图像中显著的结构轮廓；在 CRAFT 中被用作视频扩散模型的控制信号。"
---

## Definition

Canny Edge Detection is maintained here as an evidence-linked concept. 经典边缘检测算法，通过多阶段处理（噪声抑制、梯度计算、非极大值抑制、双阈值检测）提取图像中显著的结构轮廓；在 CRAFT 中被用作视频扩散模型的控制信号。

## Key Ideas

- Direct local evidence currently comes from [[chen2026craft]].
- The concept is tracked with local tags: concept, computer-vision.
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

- [[chen2026craft]] (direct evidence): 提出 CRAFT 框架，利用 Canny 边缘引导视频扩散模型（Wan2.1）从仿真轨迹生成七维度多样化的双臂操控训练数据（物体位姿/光照/颜色/背景/跨具身/视角/腕部+第...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[yang2026asyncshield]] (broader context): 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束...
- [[xu2026token]] (broader context): 提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。
- [[wang2025oneshot]] (broader context): 提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定...
- [[tang2025uad]] (broader context): 提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模...

## Evidence Map

- Direct evidence papers: [[chen2026craft]].
- Broader local evidence context: [[chen2026craft]], [[zhi2025closedloop]], [[zheng2026pokevla]], [[zhang2026joyaira]], [[yang2026asyncshield]].
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
- [[data-augmentation]]
- [[sim-to-real]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[chen2026craft]]
- [[zhi2025closedloop]]
- [[zheng2026pokevla]]
- [[zhang2026joyaira]]
- [[yang2026asyncshield]]
- [[xu2026token]]
- [[wang2025oneshot]]
- [[tang2025uad]]
