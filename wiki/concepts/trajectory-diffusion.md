---
title: "Trajectory Diffusion"
tags: [concept, diffusion, planning]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "将机器人轨迹（状态-动作序列或构型空间路径）建模为扩散去噪过程，通过反向扩散生成多模态运动规划"
---

## Definition

Trajectory Diffusion is maintained here as an evidence-linked concept. 将机器人轨迹（状态-动作序列或构型空间路径）建模为扩散去噪过程，通过反向扩散生成多模态运动规划

## Key Ideas

- Direct local evidence currently comes from [[puthumanaillam2026muninn]], [[chi2024diffusion]].
- The concept is tracked with local tags: concept, diffusion, planning.
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

- [[puthumanaillam2026muninn]] (direct evidence): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[chi2024diffusion]] (direct evidence): Columbia/Toyota/MIT 提出将机器人视觉运动策略表示为条件去噪扩散过程的 Diffusion Policy，在 4 个基准的 15 个任务上平均提升 46.9...
- [[stambaugh2026mixeddensity]] (broader context): 提出非均匀时间密度扩散规划器 MDD，用单一扁平扩散模型在轨迹不同区段分配不同时间分辨率，在 D4RL 基准上超越 Diffusion Veteran 达到新 SOTA。
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[chen2026abotphysworld]] (broader context): 基于 Wan2.1 的 14B Diffusion Transformer，通过 300 万物理标注操控视频 SFT + VLM 解耦判别器 DPO 后训练，实现物理一致的可...
- [[wang2026beyond]] (broader context): 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP...
- [[wang2026any2any]] (broader context): 提出DiffKT3D框架，将预训练视频扩散模型(Wan 2.1)迁移至放疗3D剂量预测，通过Any2Any条件范式支持7种模态的灵活输入输出组合，并引入基于临床Scoreca...
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...

## Evidence Map

- Direct evidence papers: [[puthumanaillam2026muninn]], [[chi2024diffusion]].
- Broader local evidence context: [[puthumanaillam2026muninn]], [[chi2024diffusion]], [[stambaugh2026mixeddensity]], [[lee2026implicit]], [[chen2026abotphysworld]].
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
- [[denoiser-caching]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[puthumanaillam2026muninn]]
- [[chi2024diffusion]]
- [[stambaugh2026mixeddensity]]
- [[lee2026implicit]]
- [[chen2026abotphysworld]]
- [[wang2026beyond]]
- [[wang2026any2any]]
- [[tu2026embody4d]]
