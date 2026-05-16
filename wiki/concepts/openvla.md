---
title: "OpenVLA"
tags: [vla, open-source, manipulation]
created: "2026-05-02"
updated: "2026-05-02"
type: "concept"
status: "done"
summary: "OpenVLA是开源视觉-语言-动作模型，基于Prismatic VLM架构，支持多任务机器人操控。"
---

## Definition

OpenVLA is maintained here as an evidence-linked concept. OpenVLA是开源视觉-语言-动作模型，基于Prismatic VLM架构，支持多任务机器人操控。

## Key Ideas

- Direct local evidence currently comes from [[jin2026grounding]].
- The concept is tracked with local tags: vla, open-source, manipulation.
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
- [[smith2024steer]] (broader context): 提出 STEER（Structured Training for Embodied Reasoning），通过密集语言标注训练灵活可引导的低级操控策略。方法：(1) 对现有机...
- [[kim2024openvla]] (broader context): Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K...
- [[dalal2025local]] (broader context): 提出 ManipGen 系统，通过训练 3500+ 单物体 RL 专家策略并蒸馏为通用 visuomotor 策略，结合 GPT-4o 任务分解 + Grounded SAM...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...

## Evidence Map

- Direct evidence papers: [[jin2026grounding]].
- Broader local evidence context: [[jin2026grounding]], [[smith2024steer]], [[kim2024openvla]], [[dalal2025local]], [[zhu2024scaling]].
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
- [[action-chunking]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jin2026grounding]]
- [[smith2024steer]]
- [[kim2024openvla]]
- [[dalal2025local]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zhi2025closedloop]]
- [[zhi102unifying]]
