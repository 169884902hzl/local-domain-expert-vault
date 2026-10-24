---
title: "思维链推理 (Chain-of-Thought)"
tags: [reasoning, VLA, CoT]
created: "2026-04-30"
updated: "2026-04-30"
type: "concept"
status: "done"
summary: "在 VLA 模型中引入中间推理步骤（如意图预测、任务分解），提升动作生成的逻辑一致性和精度。"
---

## Definition

思维链推理 (Chain-of-Thought) is maintained here as an evidence-linked concept. 在 VLA 模型中引入中间推理步骤（如意图预测、任务分解），提升动作生成的逻辑一致性和精度。

## Key Ideas

- Direct local evidence currently comes from [[li2026gazevla]].
- The concept is tracked with local tags: reasoning, VLA, CoT.
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

- [[li2026gazevla]] (direct evidence): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[brohan2023rt2]] (broader context): Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获...
- [[gao2025must]] (broader context): 提出 MuST（Multi-Head Skill Transformer），在 Octo 骨干上增加 N+1 个 head（N 个技能 head + 1 个进度 head），...
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zheng2026pokevla]] (broader context): PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入...

## Evidence Map

- Direct evidence papers: [[li2026gazevla]].
- Broader local evidence context: [[li2026gazevla]], [[brohan2023rt2]], [[gao2025must]], [[zhu2024scaling]], [[zhou2025oneshot]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[gaze-intention]]
- [[imitation-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[li2026gazevla]]
- [[brohan2023rt2]]
- [[gao2025must]]
- [[zhu2024scaling]]
- [[zhou2025oneshot]]
- [[zhi2025closedloop]]
- [[zhi102unifying]]
- [[zheng2026pokevla]]
