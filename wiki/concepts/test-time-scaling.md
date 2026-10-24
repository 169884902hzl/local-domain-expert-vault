---
title: "Test-Time Scaling"
tags: [RL, diffusion, inference]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "在推理时增加计算量以提升模型性能的策略，如 best-of-N 采样、自一致性等"
---

## Definition

Test-Time Scaling is maintained here as an evidence-linked concept. 在推理时增加计算量以提升模型性能的策略，如 best-of-N 采样、自一致性等

## Key Ideas

- Direct local evidence currently comes from [[dong2026faster]].
- The concept is tracked with local tags: RL, diffusion, inference.
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

- [[dong2026faster]] (direct evidence): 将扩散策略的 best-of-N 采样建模为去噪 MDP，学习噪声级 critic 在初始噪声阶段筛选候选动作，以单次去噪成本恢复 best-of-N 的性能收益，在操控任务...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[gao2026driftbased]] (broader context): 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线...
- [[wu2026affordgrasp]] (broader context): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[park2026acg]] (broader context): 提出无训练的测试时引导算法 ACG，通过将 self-attention 图替换为单位矩阵构造\"不一致向量场\"，再沿反方向引导 flow matching VLA 策略生...
- [[mahboob2026betting]] (broader context): 将 sim-to-real 性能评估建模为序贯赌博问题，证明 Kelly 准则等价于逆方差最优加权估计，提出基于 Cover universal portfolio 的实用算...
- [[jeong2026your]] (broader context): 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR...

## Evidence Map

- Direct evidence papers: [[dong2026faster]].
- Broader local evidence context: [[dong2026faster]], [[zhang2026generative]], [[zhang2026handx]], [[gao2026driftbased]], [[wu2026affordgrasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[reinforcement-learning]]
- [[diffusion-model]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[planning]]
## Related Papers

- [[dong2026faster]]
- [[li2026ets]]