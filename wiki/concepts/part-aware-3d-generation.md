---
title: "Part-Aware 3D Generation"
tags: [3d-generation, part-aware, embodied-ai]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "将 3D 资产生成从整体形状推进到部件级别，使每个部件具有独立的几何、物理和功能属性，支持交互式操控"
---

## Definition

Part-Aware 3D Generation is maintained here as an evidence-linked concept. 将 3D 资产生成从整体形状推进到部件级别，使每个部件具有独立的几何、物理和功能属性，支持交互式操控

## Key Ideas

- Direct local evidence currently comes from [[yang2026physforge]].
- The concept is tracked with local tags: 3d-generation, part-aware, embodied-ai.
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

- [[yang2026physforge]] (direct evidence): 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[xiao2026avavla]] (broader context): 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉...
- [[wang2026phys2real]] (broader context): 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Re...
- [[li2026affordsim]] (broader context): 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭...

## Evidence Map

- Direct evidence papers: [[yang2026physforge]].
- Broader local evidence context: [[yang2026physforge]], [[zhang2026prts]], [[ye2026generation]], [[yang2026ultradexgrasp]], [[xie2026humanintention]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[3d-generation]]
- [[simulation-readiness]]
- [[affordance-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[yang2026physforge]]
- [[zhang2026prts]]
- [[ye2026generation]]
- [[yang2026ultradexgrasp]]
- [[xie2026humanintention]]
- [[xiao2026avavla]]
- [[wang2026phys2real]]
- [[li2026affordsim]]
