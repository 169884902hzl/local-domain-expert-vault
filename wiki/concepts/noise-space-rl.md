---
title: "Noise-Space Reinforcement Learning"
tags: [concept, RL, diffusion, flow-matching, VLA]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "冻结 diffusion/flow-matching 解码器，仅在噪声空间训练轻量级 actor 进行策略适应的方法"
---

## Definition

Noise-Space Reinforcement Learning is maintained here as an evidence-linked concept. 冻结 diffusion/flow-matching 解码器，仅在噪声空间训练轻量级 actor 进行策略适应的方法

## Key Ideas

- Direct local evidence currently comes from [[lu2026unified]].
- The concept is tracked with local tags: concept, RL, diffusion, flow-matching, VLA.
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

- [[lu2026unified]] (direct evidence): UniSteer 通过近似 action-to-noise 反演将人类纠正动作映射到噪声空间，统一噪声空间 RL 与人类引导的 SFT，在 4 个真实操控任务上平均 66 分...
- [[patil2026youve]] (broader context): 发现预训练扩散/Flow Matching策略在推理时使用固定优化的初始噪声向量（golden ticket）替代高斯采样，可在43个任务中38个提升成功率最高58%，且无需...
- [[he2026generative]] (broader context): 提出 SoftGAC，将 MaxEnt RL 的端点熵正则化提升为路径空间相对熵，用 K=6 步轻量高斯桥转移实现单次前向通过的动作生成，在 DMC 和 HumanoidBe...
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[wang2026stepnft]] (broader context): 提出无需 critic 和 likelihood 的在线 RL 框架 π-StepNFT，通过 SDE 采样扩展探索空间并以逐步对比排序损失实现精细对齐，在 LIBERO f...
- [[jauhri2026wholebody]] (broader context): WHOLE-MoMa 利用次优 WBC 作为结构先验生成仿真演示数据，结合 Q-chunked IQL 离线 RL 和 Diffusion Policy 在 TiAGo++...
- [[dong2026faster]] (broader context): 将扩散策略的 best-of-N 采样建模为去噪 MDP，学习噪声级 critic 在初始噪声阶段筛选候选动作，以单次去噪成本恢复 best-of-N 的性能收益，在操控任务...
- [[chen2025vividex]] (broader context): 提出 ViViDex 框架，从人类视频中提取参考轨迹，用 RL + trajectory-guided reward 训练基于状态的灵巧操控策略，再 rollout 成功轨迹...

## Evidence Map

- Direct evidence papers: [[lu2026unified]].
- Broader local evidence context: [[lu2026unified]], [[patil2026youve]], [[he2026generative]], [[xu2026expertgen]], [[wang2026stepnft]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-policy]]
- [[flow-matching-policy]]
- [[diffusion-steering]]
- [[reinforcement-learning]]
- [[vision-language-action]]
- [[diffusion-model]]

## Related Papers

- [[lu2026unified]]
- [[patil2026youve]]
- [[he2026generative]]
- [[xu2026expertgen]]
- [[wang2026stepnft]]
- [[jauhri2026wholebody]]
- [[dong2026faster]]
- [[chen2025vividex]]
