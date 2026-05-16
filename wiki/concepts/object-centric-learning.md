---
title: "Object-Centric Learning"
tags: [concept]
created: "2026-05-08"
updated: "2026-05-08"
type: "concept"
status: "done"
summary: "以物体为中心的表征学习方法，将场景分解为语义连贯的区域，使机器人以物体为单位进行感知和交互"
---

## Definition

Object-Centric Learning is maintained here as an evidence-linked concept. 以物体为中心的表征学习方法，将场景分解为语义连贯的区域，使机器人以物体为单位进行感知和交互

## Key Ideas

- Direct local evidence currently comes from [[wang2026ocra]].
- The concept is tracked with local tags: concept.
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

- [[wang2026ocra]] (direct evidence): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[yang2026rise]] (broader context): 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实...
- [[shi2025zeromimic]] (broader context): 提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...
- [[kohlbrenner2026egocentric]] (broader context): 研究 H1-2 人形机器人上分布式触觉和近觉传感器的信号属性（覆盖几何、信号类型、感知距离）如何通过 RL 策略学习全身碰撞规避行为，发现稀疏非方向性近觉信号在采样效率上优于...
- [[hartz2024art]] (broader context): 提出 TPGMM 的三重改进用于长时序操控的少样本模仿学习：(1) Riemannian 速度因式分解，将末端执行器速度分解为方向（流形上的 von Mises-Fisher...
- [[chen2026rotridiff]] (broader context): 提出RoTri三体交互表示，通过编码双臂末端执行器与物体间的相对6D位姿建立三角几何约束，并结合层次化扩散模型生成协调的双臂操控轨迹，在RLBench2上较SOTA提升10.2%。

## Evidence Map

- Direct evidence papers: [[wang2026ocra]].
- Broader local evidence context: [[wang2026ocra]], [[zhou2025oneshot]], [[yang2026rise]], [[shi2025zeromimic]], [[liu2025forcemimic]].
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
- [[point-cloud]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[wang2026ocra]]
- [[zhou2025oneshot]]
- [[yang2026rise]]
- [[shi2025zeromimic]]
- [[liu2025forcemimic]]
- [[kohlbrenner2026egocentric]]
- [[hartz2024art]]
- [[chen2026rotridiff]]
