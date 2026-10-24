---
title: "Potential Field Shaping"
tags: [concept]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "在语义嵌入空间中构建 success/failure 的势场，为 RL 提供密集导航信号"
---

## Definition

Potential Field Shaping is maintained here as an evidence-linked concept. 在语义嵌入空间中构建 success/failure 的势场，为 RL 提供密集导航信号

## Key Ideas

- Direct local evidence currently comes from [[sagar2026robomd]].
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

- [[sagar2026robomd]] (direct evidence): 提出 RoboMD 框架，在视觉-语言语义嵌入空间中用深度 RL 策略主动搜索操控策略的失败诱发变体，比 VLM baseline 多发现 23% 的独特漏洞，并用发现的漏洞...
- [[yan2026tac2real]] (broader context): 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[ma2026human]] (broader context): 系统综述人类视频驱动的机器人操控学习，提出 task/observation/action 三层 skill transfer 分类法，覆盖 200+ 篇论文、50+ 开源数...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[chuang2025active]] (broader context): 提出 AV-ALOHA 系统，在 ALOHA 2 基础上增加 7-DoF AV 臂搭载立体相机，通过 VR 头显控制相机视角，实现沉浸式遥操作，实验证明 active vis...
- [[chi2024diffusion]] (broader context): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[chen2025vegetable]] (broader context): 提出约束灵巧操控框架，用 Allegro 手在 Franka 臂上通过 RL 学习可控停止的蔬菜重定向策略，实现重定向→牢固握持→削皮的多步骤循环，4 种蔬菜上 90% 牢固...

## Evidence Map

- Direct evidence papers: [[sagar2026robomd]].
- Broader local evidence context: [[sagar2026robomd]], [[yan2026tac2real]], [[marougkas2025integrating]], [[ma2026human]], [[ji2026recovering]].
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
- [[contrastive-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[sagar2026robomd]]
- [[yan2026tac2real]]
- [[marougkas2025integrating]]
- [[ma2026human]]
- [[ji2026recovering]]
- [[chuang2025active]]
- [[chi2024diffusion]]
- [[chen2025vegetable]]
