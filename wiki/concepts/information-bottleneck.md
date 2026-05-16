---
title: "Information Bottleneck"
tags: [theory, compression, generalization]
created: "2026-05-13"
updated: "2026-05-13"
type: "concept"
status: "done"
summary: "信息瓶颈原则认为，限制模型对输入信息的保留量可强制其学习任务相关的最小充分统计量，从而提升泛化能力。"
---

## Definition

Information Bottleneck is maintained here as an evidence-linked concept. 信息瓶颈原则认为，限制模型对输入信息的保留量可强制其学习任务相关的最小充分统计量，从而提升泛化能力。

## Key Ideas

- Direct local evidence currently comes from [[feng2026see]].
- The concept is tracked with local tags: theory, compression, generalization.
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

- [[feng2026see]] (direct evidence): GridS 提出可微双线性网格采样模块，将 VLA 视觉 token 从 256 压缩至 16（甚至 1），通过端到端优化的连续坐标预测保留亚 patch 级空间精度，在 7...
- [[zhi2025closedloop]] (broader context): 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比...
- [[zhao2026vitactracing]] (broader context): 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（...
- [[zhao2026visualtactile]] (broader context): 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。
- [[zhao2025polytouch]] (broader context): 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CL...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移

## Evidence Map

- Direct evidence papers: [[feng2026see]].
- Broader local evidence context: [[feng2026see]], [[zhi2025closedloop]], [[zhao2026vitactracing]], [[zhao2026visualtactile]], [[zhao2025polytouch]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[grid-sampler]]
- [[token-pruning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[feng2026see]]
- [[zhi2025closedloop]]
- [[zhao2026vitactracing]]
- [[zhao2026visualtactile]]
- [[zhao2025polytouch]]
- [[yin2026multiple]]
- [[ye2026generation]]
- [[yang2026ultradexgrasp]]
