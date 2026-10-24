---
title: "4D Generation"
tags: [concept, video-generation, 3d-generation]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "从单目视频或图像生成时空一致的动态 3D 场景（4D 表示），支持任意新视角合成"
---

## Definition

4D Generation is maintained here as an evidence-linked concept. 从单目视频或图像生成时空一致的动态 3D 场景（4D 表示），支持任意新视角合成

## Key Ideas

- Direct local evidence currently comes from [[tu2026embody4d]].
- The concept is tracked with local tags: concept, video-generation, 3d-generation.
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

- [[tu2026embody4d]] (direct evidence): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[yang2026physforge]] (broader context): 提出两阶段框架 PhysForge，通过 VLM 规划层级物理蓝图 + 扩散模型生成带运动学参数的部分感知 3D 资产，并构建 15 万物理标注数据集 PhysDB。

## Evidence Map

- Direct evidence papers: [[tu2026embody4d]].
- Broader local evidence context: [[tu2026embody4d]], [[zhu2026nsvla]], [[zhou2026sim1]], [[zhou2025oneshot]], [[zhang2026handx]].
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
- [[video-diffusion-model]]
- [[world-model]]
- [[warp-then-inpaint]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[tu2026embody4d]]
- [[zhu2026nsvla]]
- [[zhou2026sim1]]
- [[zhou2025oneshot]]
- [[zhang2026handx]]
- [[ye2026generation]]
- [[yang2026ultradexgrasp]]
- [[yang2026physforge]]
