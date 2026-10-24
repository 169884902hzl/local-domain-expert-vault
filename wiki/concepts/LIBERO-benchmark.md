---
title: "LIBERO Benchmark"
tags: [benchmark, manipulation, lifelong-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "语言引导的机器人操控基准，包含五个任务套件，用于评估 VLA 模型在多样化操控场景下的表现。"
---

## Definition

LIBERO Benchmark is maintained here as an evidence-linked concept. 语言引导的机器人操控基准，包含五个任务套件，用于评估 VLA 模型在多样化操控场景下的表现。

## Key Ideas

- Direct local evidence currently comes from [[wang2026vlathinker]].
- The concept is tracked with local tags: benchmark, manipulation, lifelong-learning.
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

- [[wang2026vlathinker]] (direct evidence): 首个\"thinking-with-image\"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRP...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...
- [[zheng120dottip]] (broader context): 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范...
- [[zhang2026safevla]] (broader context): 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，...

## Evidence Map

- Direct evidence papers: [[wang2026vlathinker]].
- Broader local evidence context: [[wang2026vlathinker]], [[zhu2026nsvla]], [[zhu2024scaling]], [[zhou2026rcnf]], [[zhong2026vlaopd]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action-model]]
- [[robotic-manipulation]]
- [[RoboTwin-2.0]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026vlathinker]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026rcnf]]
- [[zhong2026vlaopd]]
- [[zheng2026pokevla]]
- [[zheng120dottip]]
- [[zhang2026safevla]]
