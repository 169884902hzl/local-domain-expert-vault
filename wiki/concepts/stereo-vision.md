---
title: "Stereo Vision（双目视觉）"
tags: [concept, perception, 3d-vision]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "通过同步双目图像对推断 3D 空间结构的视觉感知方式，无需显式 3D 重建即可提供隐式深度线索。"
---

## Definition

Stereo Vision（双目视觉） is maintained here as an evidence-linked concept. 通过同步双目图像对推断 3D 空间结构的视觉感知方式，无需显式 3D 重建即可提供隐式深度线索。

## Key Ideas

- Direct local evidence currently comes from [[han2026stereopolicy]].
- The concept is tracked with local tags: concept, perception, 3d-vision.
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

- [[han2026stereopolicy]] (direct evidence): 提出 StereoPolicy 框架，通过 Stereo Transformer 融合双目图像对实现隐式 3D 几何推理，无需显式 3D 重建，在扩散策略和 VLA 模型上均...
- [[xu2026fingereye]] (broader context): FingerEye 是一种紧凑低成本视觉-触觉传感器，结合双目 RGB 与柔性环形结构变形估计，在接触前、接触瞬间和接触后连续提供局部感知，并用于灵巧手模仿学习。
- [[haldar2026point]] (broader context): 利用 VLM 引导的自动化点云提取管线和统一的 3D 点表示，实现零样本 Sim-to-Real 策略迁移，在 6 个真实世界操控任务中比图像基线提升最高 66%。
- [[chuang2025active]] (broader context): 提出 AV-ALOHA 系统，在 ALOHA 2 基础上增加 7-DoF AV 臂搭载立体相机，通过 VR 头显控制相机视角，实现沉浸式遥操作，实验证明 active vis...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...

## Evidence Map

- Direct evidence papers: [[han2026stereopolicy]].
- Broader local evidence context: [[han2026stereopolicy]], [[xu2026fingereye]], [[haldar2026point]], [[chuang2025active]], [[zhu2026nsvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[point-cloud]]
- [[diffusion-policy]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[han2026stereopolicy]]
- [[xu2026fingereye]]
- [[haldar2026point]]
- [[chuang2025active]]
- [[zhu2026nsvla]]
- [[zhou2026vlbiman]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
