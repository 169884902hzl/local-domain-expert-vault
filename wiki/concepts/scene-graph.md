---
title: "Scene Graph"
tags: [representation, perception, structured-reasoning]
created: "2026-05-03"
updated: "2026-05-03"
type: "concept"
status: "done"
summary: "将视觉场景编码为图结构，节点表示物体（含 3D 几何和语义特征），边表示物体间关系（空间、语义），用于结构化感知和推理。"
---

## Definition

Scene Graph is maintained here as an evidence-linked concept. 将视觉场景编码为图结构，节点表示物体（含 3D 几何和语义特征），边表示物体间关系（空间、语义），用于结构化感知和推理。

## Key Ideas

- Direct local evidence currently comes from [[qi2026compose]].
- The concept is tracked with local tags: representation, perception, structured-reasoning.
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

- [[qi2026compose]] (direct evidence): 提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Polic...
- [[zhi102unifying]] (broader context): 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[xu2026twinrlvla]] (broader context): 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在...
- [[xie2026humanintention]] (broader context): MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 S...
- [[xie102multiview]] (broader context): 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减...

## Evidence Map

- Direct evidence papers: [[qi2026compose]].
- Broader local evidence context: [[qi2026compose]], [[zhi102unifying]], [[zhang2026world2minecraft]], [[ye2026generation]], [[yang2026ultradexgrasp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-model]]
- [[diffusion-model]]
- [[imitation-learning]]
- [[graph-neural-network]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[qi2026compose]]
- [[zhi102unifying]]
- [[zhang2026world2minecraft]]
- [[ye2026generation]]
- [[yang2026ultradexgrasp]]
- [[xu2026twinrlvla]]
- [[xie2026humanintention]]
- [[xie102multiview]]
