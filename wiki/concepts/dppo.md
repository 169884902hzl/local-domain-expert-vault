---
title: "DPPO"
tags: [concept, RL, diffusion]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "Diffusion Policy Policy Optimization——将扩散策略的去噪过程展开为augmented MDP，使用PPO策略梯度进行在线微调的方法。"
---

## Definition

DPPO is maintained here as an evidence-linked concept. Diffusion Policy Policy Optimization——将扩散策略的去噪过程展开为augmented MDP，使用PPO策略梯度进行在线微调的方法。

## Key Ideas

- Direct local evidence currently comes from [[gu2026refinedp]].
- The concept is tracked with local tags: concept, RL, diffusion.
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

- [[gu2026refinedp]] (direct evidence): 提出REFINE-DP框架，通过DPPO联合优化扩散策略高层规划器和RL底层控制器，使人形机器人loco-manipulation任务成功率从50-70%提升至90%+，仅需...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[xu2026expertgen]] (broader context): ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本...
- [[stambaugh2026mixeddensity]] (broader context): 提出非均匀时间密度扩散规划器 MDD，用单一扁平扩散模型在轨迹不同区段分配不同时间分辨率，在 D4RL 基准上超越 Diffusion Veteran 达到新 SOTA。
- [[park2026demodiffusion]] (broader context): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...
- [[li2025routing]] (broader context): 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能

## Evidence Map

- Direct evidence papers: [[gu2026refinedp]].
- Broader local evidence context: [[gu2026refinedp]], [[zhang2026handx]], [[xu2026expertgen]], [[stambaugh2026mixeddensity]], [[park2026demodiffusion]].
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
- [[online-fine-tuning]]
- [[residual-rl]]
- [[action-chunking]]
- [[reinforcement-learning]]
- [[diffusion-model]]

## Related Papers

- [[gu2026refinedp]]
- [[zhang2026handx]]
- [[xu2026expertgen]]
- [[stambaugh2026mixeddensity]]
- [[park2026demodiffusion]]
- [[li2026affordsim]]
- [[li2025routing]]
- [[lee2026implicit]]
