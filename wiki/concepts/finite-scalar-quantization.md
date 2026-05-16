---
title: "Finite Scalar Quantization"
tags: [concept, tokenization, autoregressive]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "将连续运动特征量化为有限均匀级别整数 token 的方法，用于自回归运动生成模型的离散化表示。"
---

## Definition

Finite Scalar Quantization is maintained here as an evidence-linked concept. 将连续运动特征量化为有限均匀级别整数 token 的方法，用于自回归运动生成模型的离散化表示。

## Key Ideas

- Direct local evidence currently comes from [[zhang2026handx]].
- The concept is tracked with local tags: concept, tokenization, autoregressive.
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

- [[zhang2026handx]] (direct evidence): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[mitrano2024grasp]] (broader context): 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿...
- [[kim2024openvla]] (broader context): Stanford/UC Berkeley 提出开源 VLA 模型 OpenVLA，7B 参数基于 Prismatic VLM，在 Open X-Embodiment 970K...
- [[ji2026recovering]] (broader context): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[zhu2026nsvla]] (broader context): 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA
- [[zhu2024scaling]] (broader context): 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...

## Evidence Map

- Direct evidence papers: [[zhang2026handx]].
- Broader local evidence context: [[zhang2026handx]], [[mitrano2024grasp]], [[kim2024openvla]], [[ji2026recovering]], [[zhu2026nsvla]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-tokenization]]
- [[motion-generation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[zhang2026handx]]
- [[mitrano2024grasp]]
- [[kim2024openvla]]
- [[ji2026recovering]]
- [[zhu2026nsvla]]
- [[zhu2024scaling]]
- [[zhou2026vlbiman]]
- [[zhou2026rcnf]]
