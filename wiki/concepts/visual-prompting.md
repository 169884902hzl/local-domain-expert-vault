---
title: "Visual Prompting"
tags: [VLM, visual-reasoning, prompting]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "通过在输入图像上叠加结构化视觉线索来引导 VLM 推理的技术范式，无需修改模型参数。"
---

## Definition

Visual Prompting is maintained here as an evidence-linked concept. 通过在输入图像上叠加结构化视觉线索来引导 VLM 推理的技术范式，无需修改模型参数。

## Key Ideas

- Direct local evidence currently comes from [[yokomizo2026physquantagent]].
- The concept is tracked with local tags: VLM, visual-reasoning, prompting.
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

- [[yokomizo2026physquantagent]] (direct evidence): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[liu2025kuda]] (broader context): 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...

## Evidence Map

- Direct evidence papers: [[yokomizo2026physquantagent]].
- Broader local evidence context: [[yokomizo2026physquantagent]], [[vo2026codegraphvlp]], [[liu2025kuda]], [[zhu2026nsvla]], [[zhou2026vlbiman]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[physical-reasoning]]
- [[grounding-dino]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[yokomizo2026physquantagent]]
- [[vo2026codegraphvlp]]
- [[liu2025kuda]]
- [[zhu2026nsvla]]
- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026prts]]
