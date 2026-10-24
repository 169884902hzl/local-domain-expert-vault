---
title: "红队测试 (Red Teaming)"
tags: [safety, adversarial, VLA, RL]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "通过自动生成对抗性输入来系统性发现模型漏洞的安全评估方法，在具身 AI 中用于测试 VLA 对语言变化的鲁棒性。"
---

## Definition

红队测试 (Red Teaming) is maintained here as an evidence-linked concept. 通过自动生成对抗性输入来系统性发现模型漏洞的安全评估方法，在具身 AI 中用于测试 VLA 对语言变化的鲁棒性。

## Key Ideas

- Direct local evidence currently comes from [[tong2026uncovering]].
- The concept is tracked with local tags: safety, adversarial, VLA, RL.
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

- [[tong2026uncovering]] (direct evidence): 提出 DAERT 框架，利用基于 ROVER 的多样性感知强化学习训练 VLM 攻击者，自动生成语义保持但导致 VLA 执行失败的对抗指令，将 π₀ 成功率从 93.33%...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...
- [[zhang2026recurrent]] (broader context): 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 S...

## Evidence Map

- Direct evidence papers: [[tong2026uncovering]].
- Broader local evidence context: [[tong2026uncovering]], [[zhu2026nsvla]], [[zhou2026ego]], [[zhao2026visualtactile]], [[zhao2026rosclaw]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vla]]
- [[reinforcement-learning]]
- [[grpo]]
- [[adversarial-robustness]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[tong2026uncovering]]
- [[zhu2026nsvla]]
- [[zhou2026ego]]
- [[zhao2026visualtactile]]
- [[zhao2026rosclaw]]
- [[zhang2026world2minecraft]]
- [[zhang2026safevla]]
- [[zhang2026recurrent]]
