---
title: "上下文模仿学习"
tags: [imitation-learning, in-context-learning, few-shot]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "通过少量示教作为上下文先验，无需微调即可泛化到新任务的模仿学习范式。"
---

## Definition

上下文模仿学习 is maintained here as an evidence-linked concept. 通过少量示教作为上下文先验，无需微调即可泛化到新任务的模仿学习范式。

## Key Ideas

- Direct local evidence currently comes from [[wang2026radar]].
- The concept is tracked with local tags: imitation-learning, in-context-learning, few-shot.
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

- [[wang2026radar]] (direct evidence): 提出全自主闭环数据采集引擎 RADAR，通过 VLM 语义规划 + GNN 图扩散模仿学习 + 三阶段 VQA 评估 + LIFO 自主环境重置，仅用 2-5 次人类示教即可...
- [[tang2025kalie]] (broader context): 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的...
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[park2026demodiffusion]] (broader context): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[collaboration2025open]] (broader context): Google DeepMind 联合 21 个机构发布 Open X-Embodiment 数据集，包含 22 个机器人平台的 1M+ episodes、500+ 技能，并提...
- [[chen2026ropa]] (broader context): ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实...
- [[ao2025llmasbtplanner]] (broader context): 提出利用 LLM 通过四种 in-context learning 方法和监督微调直接生成机器人装配任务的行为树（BT），在 Siemens 齿轮组装配任务和 Furnitu...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA

## Evidence Map

- Direct evidence papers: [[wang2026radar]].
- Broader local evidence context: [[wang2026radar]], [[tang2025kalie]], [[smith2024steer]], [[park2026demodiffusion]], [[collaboration2025open]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[diffusion-policy]]
- [[behavior-prior]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[wang2026radar]]
- [[tang2025kalie]]
- [[smith2024steer]]
- [[park2026demodiffusion]]
- [[collaboration2025open]]
- [[chen2026ropa]]
- [[ao2025llmasbtplanner]]
- [[zhu2026nsvla]]
