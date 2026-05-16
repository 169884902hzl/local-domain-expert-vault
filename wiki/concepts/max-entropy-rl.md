---
title: "MaxEnt RL"
tags: [reinforcement-learning, policy-optimization]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "最大熵强化学习在期望回报中加入策略熵奖励，鼓励策略在最大化值的同时保持随机性，用于离线策略连续控制。"
---

## Definition

MaxEnt RL is maintained here as an evidence-linked concept. 最大熵强化学习在期望回报中加入策略熵奖励，鼓励策略在最大化值的同时保持随机性，用于离线策略连续控制。

## Key Ideas

- Direct local evidence currently comes from [[he2026generative]].
- The concept is tracked with local tags: reinforcement-learning, policy-optimization.
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

- [[he2026generative]] (direct evidence): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[yang2025simtoreal]] (broader context): 针对移动机器人在ICRA 2024 Sim2Real竞赛中的长时序拾取-放置任务，提出SMMS运动模糊缓解策略和反馈线性化伺服控制（含Design Function），在无算...
- [[wang2023multistage]] (broader context): 提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1)...
- [[tong2026uncovering]] (broader context): 提出 DAERT 框架，利用基于 ROVER 的多样性感知强化学习训练 VLM 攻击者，自动生成语义保持但导致 VLA 执行失败的对抗指令，将 π₀ 成功率从 93.33%...
- [[lips2024keypoints]] (broader context): 提出合成数据管线用于训练衣物关键点检测器。三阶段流程：程序化生成单层 mesh → Nvidia Flex 变形（模拟展开后状态）→ Blender Cycles 渲染。Ma...

## Evidence Map

- Direct evidence papers: [[he2026generative]].
- Broader local evidence context: [[he2026generative]], [[ji2026recovering]], [[zhong2026vlaopd]], [[zhang2026safevla]], [[yang2025simtoreal]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[soft-bridge-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[he2026generative]]
- [[ji2026recovering]]
- [[zhong2026vlaopd]]
- [[zhang2026safevla]]
- [[yang2025simtoreal]]
- [[wang2023multistage]]
- [[tong2026uncovering]]
- [[lips2024keypoints]]
