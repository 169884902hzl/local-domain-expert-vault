---
title: "Diffusion Language Model (dLLM)"
tags: [concept]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "使用离散扩散过程生成文本的语言模型，通过去噪恢复被 mask 的 token，支持并行生成（block-based semi-autoregressive），代表模型包括 LLaDA、Dream 7B。"
---

## Definition

Diffusion Language Model (dLLM) is maintained here as an evidence-linked concept. 使用离散扩散过程生成文本的语言模型，通过去噪恢复被 mask 的 token，支持并行生成（block-based semi-autoregressive），代表模型包括 LLaDA、Dream 7B。

## Key Ideas

- Direct local evidence currently comes from [[jiang2026break]].
- The concept is tracked with local tags: concept.
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

- [[jiang2026break]] (direct evidence): 提出 b1 框架，通过 RL 学习动态大小的推理块并施加单调熵下降约束，解决扩散语言模型中固定大小分块破坏推理连贯性的问题，在数学推理基准上相比固定分块基线最高提升 19.53%。
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[wu2026affordgrasp]] (broader context): 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[team2024octo]] (broader context): UC Berkeley 提出开源通用机器人策略 Octo，基于 Transformer 扩散策略头，在 Open X-Embodiment 的 800K+ 轨迹上预训练，支持...
- [[qi2026compose]] (broader context): 提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Polic...

## Evidence Map

- Direct evidence papers: [[jiang2026break]].
- Broader local evidence context: [[jiang2026break]], [[zhang2026handx]], [[zhang2026generative]], [[xu2026expertgen]], [[wu2026affordgrasp]].
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
- [[reinforcement-learning]]
- [[reasoning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[jiang2026break]]
- [[zhang2026handx]]
- [[zhang2026generative]]
- [[xu2026expertgen]]
- [[wu2026affordgrasp]]
- [[wang2026beyond]]
- [[team2024octo]]
- [[qi2026compose]]
