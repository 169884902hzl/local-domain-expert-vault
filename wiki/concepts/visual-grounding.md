---
title: "Visual Grounding"
tags: [visual-grounding, VLM, object-localization]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "将自然语言描述映射到图像中特定空间区域的技术，是连接高层语义推理与低层视觉感知的关键桥梁。"
---

## Definition

Visual Grounding is maintained here as an evidence-linked concept. 将自然语言描述映射到图像中特定空间区域的技术，是连接高层语义推理与低层视觉感知的关键桥梁。

## Key Ideas

- Direct local evidence currently comes from no direct backlink yet.
- The concept is tracked with local tags: visual-grounding, VLM, object-localization.
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

- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026ego]] (broader context): 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角...
- [[yokomizo2026physquantagent]] (broader context): 提出基于视觉提示（visual prompting）的 VLM 物理量推理管线 PhysQuantAgent，通过目标检测、尺度估计和截面图像生成三种视觉提示增强 VLM 对...
- [[yin2026multiple]] (broader context): 提出MCM-VG框架，通过语义对齐、实例校正和视角蒸馏三个模块建立2D-3D一致性映射，在ScanRefer和Nr3D上实现零样本3D视觉定位新SOTA
- [[yang2026hivla]] (broader context): 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越...
- [[wang2026radar]] (broader context): 提出全自主闭环数据采集引擎 RADAR，通过 VLM 语义规划 + GNN 图扩散模仿学习 + 三阶段 VQA 评估 + LIFO 自主环境重置，仅用 2-5 次人类示教即可...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[ma2026semanticcontact]] (broader context): 提出 Semantic-Contact Fields（SCFields），将视觉语义与密集外在接触概率和力估计融合为统一 3D 表示，通过仿真预训练+真实世界伪标签对齐的两阶...

## Evidence Map

- Direct evidence papers: no direct backlink yet.
- Broader local evidence context: [[zhou2026vlbiman]], [[zhou2026ego]], [[yokomizo2026physquantagent]], [[yin2026multiple]], [[yang2026hivla]].
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
- [[vision-language-action]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]

## Related Papers

- [[zhou2026vlbiman]]
- [[zhou2026ego]]
- [[yokomizo2026physquantagent]]
- [[yin2026multiple]]
- [[yang2026hivla]]
- [[wang2026radar]]
- [[vo2026codegraphvlp]]
- [[ma2026semanticcontact]]
