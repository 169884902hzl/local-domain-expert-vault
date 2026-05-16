---
title: "Motion Generation"
tags: [concept, diffusion, autoregressive]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "从文本或其他条件信号生成人体或手部运动序列的技术，主要范式包括扩散模型和自回归模型。"
---

## Definition

Motion Generation is maintained here as an evidence-linked concept. 从文本或其他条件信号生成人体或手部运动序列的技术，主要范式包括扩散模型和自回归模型。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026handx]].
- The concept is tracked with local tags: concept, diffusion, autoregressive.
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

- [[zhang2026handx]] (direct evidence): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[scheikl620movement]] (broader context): 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabi...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[park2026demodiffusion]] (broader context): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[li2025routing]] (broader context): 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle...
- [[jiang2026world4rl]] (broader context): 提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-Worl...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[chen2026ropa]] (broader context): ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实...

## Evidence Map

- Direct evidence papers: [[zhang2026handx]].
- Broader local evidence context: [[zhang2026handx]], [[scheikl620movement]], [[zhang2026generative]], [[park2026demodiffusion]], [[li2025routing]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[action-tokenization]]
- [[bimanual-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[zhang2026handx]]
- [[scheikl620movement]]
- [[zhang2026generative]]
- [[park2026demodiffusion]]
- [[li2025routing]]
- [[jiang2026world4rl]]
- [[chi2024diffusion]]
- [[chen2026ropa]]
