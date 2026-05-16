---
title: "Kinematic Retargeting"
tags: [concept, manipulation, imitation]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "将人体手部运动轨迹通过几何映射转换为机器人末端执行器位姿的技术，是人体-机器人模仿的基础步骤。"
---

## Definition

Kinematic Retargeting is maintained here as an evidence-linked concept. 将人体手部运动轨迹通过几何映射转换为机器人末端执行器位姿的技术，是人体-机器人模仿的基础步骤。

## Key Ideas

- Direct local evidence currently comes from [[park2026demodiffusion]].
- The concept is tracked with local tags: concept, manipulation, imitation.
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

- [[park2026demodiffusion]] (direct evidence): 利用预训练扩散策略对运动学重定向的人体示范轨迹进行 SDEdit 式中间步去噪，实现无需配对数据或在线训练的单次人体-机器人模仿操控。
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[huang2026kinder]] (broader context): 提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP...
- [[consortium2026openhembodiment]] (broader context): 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgica...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...

## Evidence Map

- Direct evidence papers: [[park2026demodiffusion]].
- Broader local evidence context: [[park2026demodiffusion]], [[zhao2026visualtactile]], [[missal2026ropedreamer]], [[huang2026kinder]], [[consortium2026openhembodiment]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[imitation-learning]]
- [[diffusion-policy]]
- [[sdedit]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]

## Related Papers

- [[park2026demodiffusion]]
- [[zhao2026visualtactile]]
- [[missal2026ropedreamer]]
- [[huang2026kinder]]
- [[consortium2026openhembodiment]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
