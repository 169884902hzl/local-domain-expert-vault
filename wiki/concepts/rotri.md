---
title: "RoTri (Robot-Object Triadic Interaction)"
tags: [bimanual-manipulation, spatial-reasoning, interaction-modeling]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "双臂系统中编码两臂末端执行器与被操控物体之间相对6D位姿的三体空间交互表示，建立连续三角几何约束。"
---

## Definition

RoTri (Robot-Object Triadic Interaction) is maintained here as an evidence-linked concept. 双臂系统中编码两臂末端执行器与被操控物体之间相对6D位姿的三体空间交互表示，建立连续三角几何约束。

## Key Ideas

- Direct local evidence currently comes from [[chen2026rotridiff]].
- The concept is tracked with local tags: bimanual-manipulation, spatial-reasoning, interaction-modeling.
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

- [[chen2026rotridiff]] (direct evidence): 提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhong2026vlaopd]] (broader context): 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...

## Evidence Map

- Direct evidence papers: [[chen2026rotridiff]].
- Broader local evidence context: [[chen2026rotridiff]], [[zhu2026nsvla]], [[zhu2024scaling]], [[zhou2026vlbiman]], [[zhou2026rcnf]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[bimanual-manipulation]]
- [[diffusion-policy]]
- [[imitation-learning]]
- [[spatial-grounding]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[chen2026rotridiff]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026rcnf]]
- [[zhou2025oneshot]]
- [[zhong2026vlaopd]]
- [[zhi2025closedloop]]
