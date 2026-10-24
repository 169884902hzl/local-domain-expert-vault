---
title: "LoRA"
tags: [parameter-efficient-finetuning, llm]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "Low-Rank Adaptation，一种参数高效微调方法，通过低秩分解在冻结预训练权重旁添加可训练矩阵。"
---

## Definition

LoRA is maintained here as an evidence-linked concept. Low-Rank Adaptation，一种参数高效微调方法，通过低秩分解在冻结预训练权重旁添加可训练矩阵。

## Key Ideas

- Direct local evidence currently comes from [[jin2026grounding]].
- The concept is tracked with local tags: parameter-efficient-finetuning, llm.
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

- [[jin2026grounding]] (direct evidence): 系统性实证研究VLA模型零样本Sim-to-Real迁移的四维因子（域随机化、渲染保真度、物理真实度、RL微调），基于10k+真实世界试验得出五个关键结论：空间随机化主导迁移...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...
- [[xia2024cage]] (broader context): 提出 CAGE（Causal Attention Enables Generalizable manipulation），通过因果注意力机制实现数据高效泛化的机器人操控。核心...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...
- [[tang2025kalie]] (broader context): 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的...
- [[shi2025zeromimic]] (broader context): 提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓...

## Evidence Map

- Direct evidence papers: [[jin2026grounding]].
- Broader local evidence context: [[jin2026grounding]], [[zhi2025closedloop]], [[zhao2026visualtactile]], [[xu2026twinrlvla]], [[xia2024cage]].
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
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[jin2026grounding]]
- [[zhi2025closedloop]]
- [[zhao2026visualtactile]]
- [[xu2026twinrlvla]]
- [[xia2024cage]]
- [[wu2025imperfect]]
- [[tang2025kalie]]
- [[shi2025zeromimic]]
