---
title: "Knowledge Transfer"
tags: [concept, transfer-learning]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "将大规模预训练模型的知识迁移到目标领域任务，包括特征提取迁移和生成能力迁移两种范式"
---

## Definition

Knowledge Transfer is maintained here as an evidence-linked concept. 将大规模预训练模型的知识迁移到目标领域任务，包括特征提取迁移和生成能力迁移两种范式

## Key Ideas

- Direct local evidence currently comes from [[wang2026any2any]].
- The concept is tracked with local tags: concept, transfer-learning.
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

- [[wang2026any2any]] (direct evidence): 提出DiffKT3D框架，将预训练视频扩散模型(Wan 2.1)迁移至放疗3D剂量预测，通过Any2Any条件范式支持7种模态的灵活输入输出组合，并引入基于临床Scoreca...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[luijkx2026llmguided]] (broader context): 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正...
- [[li2026gazevla]] (broader context): 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法
- [[dong2025vitavla]] (broader context): 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token...
- [[do2025watch]] (broader context): 提出 RL + 变阻抗控制 + 观测历史框架用于关节物体操控，通过在线策略蒸馏（特权编码器 + 自适应模块）和任务感知+运动感知 reward 实现泛化，仿真 96%、真实世...
- [[brohan2023rt2]] (broader context): Google DeepMind 提出将 VLM 直接融入端到端机器人控制的 RT-2 模型，通过将动作表示为文本 token 与语言任务 co-fine-tune，使机器人获...

## Evidence Map

- Direct evidence papers: [[wang2026any2any]].
- Broader local evidence context: [[wang2026any2any]], [[zhang2026joyaira]], [[wu2026continually]], [[luijkx2026llmguided]], [[li2026gazevla]].
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
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026any2any]]
- [[zhang2026joyaira]]
- [[wu2026continually]]
- [[luijkx2026llmguided]]
- [[li2026gazevla]]
- [[dong2025vitavla]]
- [[do2025watch]]
- [[brohan2023rt2]]
