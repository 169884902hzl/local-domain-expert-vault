---
title: "Deformable Object Tracing"
tags: [concept, manipulation]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "可变形物体追踪——通过沿物体边缘滑动夹爪将非结构化构型转变为展开状态的基础操控技能，涵盖 1D 线性物体和 2D 平面物体"
---

## Definition

Deformable Object Tracing is maintained here as an evidence-linked concept. 可变形物体追踪——通过沿物体边缘滑动夹爪将非结构化构型转变为展开状态的基础操控技能，涵盖 1D 线性物体和 2D 平面物体

## Key Ideas

- Direct local evidence currently comes from [[zhao2026vitactracing]].
- The concept is tracked with local tags: concept, manipulation.
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

- [[zhao2026vitactracing]] (direct evidence): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[wang2026radar]] (broader context): 提出全自主闭环数据采集引擎 RADAR，通过 VLM 语义规划 + GNN 图扩散模仿学习 + 三阶段 VQA 评估 + LIFO 自主环境重置，仅用 2-5 次人类示教即可...
- [[scheikl620movement]] (broader context): 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabi...
- [[moletta2026preference]] (broader context): 提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trouser...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[missal2026ropedreamer]] (broader context): 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%
- [[liu2025kuda]] (broader context): 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为...

## Evidence Map

- Direct evidence papers: [[zhao2026vitactracing]].
- Broader local evidence context: [[zhao2026vitactracing]], [[zhou2026sim1]], [[wang2026radar]], [[scheikl620movement]], [[moletta2026preference]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[visual-tactile-fusion]]
- [[imitation-learning]]
- [[action-chunking]]
- [[robotic-manipulation]]

## Related Papers

- [[zhao2026vitactracing]]
- [[zhou2026sim1]]
- [[wang2026radar]]
- [[scheikl620movement]]
- [[moletta2026preference]]
- [[mitrano2024grasp]]
- [[missal2026ropedreamer]]
- [[liu2025kuda]]
