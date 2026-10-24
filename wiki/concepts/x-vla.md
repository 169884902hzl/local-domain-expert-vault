---
title: "X-VLA"
tags: [VLA, cross-embodiment, soft-prompt]
created: "2026-05-16"
updated: "2026-05-16"
type: "concept"
status: "done"
summary: "X-VLA 使用软提示解决跨具身体征的异构数据问题，实现可扩展的跨具身体征 VLA 模型。"
---

## Definition

X-VLA is maintained here as an evidence-linked concept. X-VLA 使用软提示解决跨具身体征的异构数据问题，实现可扩展的跨具身体征 VLA 模型。

## Key Ideas

- Direct local evidence currently comes from [[du2026bioprovlaagent]].
- The concept is tracked with local tags: VLA, cross-embodiment, soft-prompt.
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

- [[du2026bioprovlaagent]] (direct evidence): 提出基于 VLA 的低成本（$800-850）生物实验室多 Agent 闭环系统，通过 LLM 协议解析、VLM-RAG 状态验证和在线数据增强（AugSmolVLA）实现...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zhao2026rosclaw]] (broader context): 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...

## Evidence Map

- Direct evidence papers: [[du2026bioprovlaagent]].
- Broader local evidence context: [[du2026bioprovlaagent]], [[zhu2026nsvla]], [[zhou2026rcnf]], [[zhong2026vlaopd]], [[zheng2026pokevla]].
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
- [[SmolVLA]]
- [[cross-embodiment-transfer]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[du2026bioprovlaagent]]
- [[zhu2026nsvla]]
- [[zhou2026rcnf]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zhao2026rosclaw]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026safevla]]
