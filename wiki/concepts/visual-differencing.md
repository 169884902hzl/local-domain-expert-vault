---
title: "Visual Differencing Module (VDM)"
tags: [concept, VLM, manipulation]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "将视觉观察转换为结构化自然语言描述的模块，通过文本化场景差异辅助编码 agent 进行闭环推理"
---

## Definition

Visual Differencing Module (VDM) is maintained here as an evidence-linked concept. 将视觉观察转换为结构化自然语言描述的模块，通过文本化场景差异辅助编码 agent 进行闭环推理

## Key Ideas

- Direct local evidence currently comes from [[fu2026capx]].
- The concept is tracked with local tags: concept, VLM, manipulation.
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

- [[fu2026capx]] (direct evidence): 提出 CaP-X 框架，包含 CaP-Gym（交互式编码环境，187 个任务）、CaP-Bench（8 个层级系统评估 12 个前沿模型）、CaP-Agent0（无需训练的...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[yuan2026embodiedr1]] (broader context): 提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...

## Evidence Map

- Direct evidence papers: [[fu2026capx]].
- Broader local evidence context: [[fu2026capx]], [[zhu2026nsvla]], [[zhou2026vlbiman]], [[zhou2026ego]], [[zhang2026visionlanguageaction]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[code-as-policy]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[fu2026capx]]
- [[zhu2026nsvla]]
- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
- [[yuan2026embodiedr1]]
- [[xiao2026avavla]]
