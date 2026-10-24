---
title: "Score-Based Diffusion"
tags: [diffusion, generative-model, score-matching]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "基于分数匹配的扩散模型框架，通过学习数据分布的 score function（梯度）实现从噪声到数据的反向采样。"
---

## Definition

Score-Based Diffusion is maintained here as an evidence-linked concept. 基于分数匹配的扩散模型框架，通过学习数据分布的 score function（梯度）实现从噪声到数据的反向采样。

## Key Ideas

- Direct local evidence currently comes from [[peters2026coordinated]].
- The concept is tracked with local tags: diffusion, generative-model, score-matching.
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

- [[peters2026coordinated]] (direct evidence): 提出 CoDi 框架，通过用户定义的多 Agent 代价函数引导独立训练的单 Agent 扩散策略，实现无需多 Agent 示范数据的协调多机器人操控，在双臂 pick-an...
- [[scheikl620movement]] (broader context): 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabi...
- [[puthumanaillam2026muninn]] (broader context): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[li2026hpedit]] (broader context): 提出 HP-Edit 框架，利用 VLM 训练的 HP-Scorer 作为任务感知奖励函数，结合 Flow-GRPO 对扩散模型图像编辑器进行人类偏好对齐的后训练，在 8 个...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[khan2026discrete]] (broader context): 提出 DRIFT，首个面向离散动作空间的 CTMC 策略 offline-to-online 微调方法，通过 advantage-weighted discrete flow...
- [[jiang2026blockr1]] (broader context): 揭示扩散语言模型多域 RL 后训练中 block size 域冲突问题，通过 teacher-student 管线为每个训练样本分配最优 block size，构建 41K...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...

## Evidence Map

- Direct evidence papers: [[peters2026coordinated]].
- Broader local evidence context: [[peters2026coordinated]], [[scheikl620movement]], [[puthumanaillam2026muninn]], [[li2026hpedit]], [[lee2026implicit]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[classifier-guidance]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[peters2026coordinated]]
- [[scheikl620movement]]
- [[puthumanaillam2026muninn]]
- [[li2026hpedit]]
- [[lee2026implicit]]
- [[khan2026discrete]]
- [[jiang2026blockr1]]
- [[ji2026recovering]]
