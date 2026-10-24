---
title: "Energy-Based Model"
tags: [concept, generative-model]
created: "2026-05-06"
updated: "2026-05-06"
type: "concept"
status: "done"
summary: "通过标量能量函数建模数据分布的生成模型，低能量对应高概率"
---

## Definition

Energy-Based Model is maintained here as an evidence-linked concept. 通过标量能量函数建模数据分布的生成模型，低能量对应高概率

## Key Ideas

- Direct local evidence currently comes from [[ji2026recovering]].
- The concept is tracked with local tags: concept, generative-model.
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

- [[ji2026recovering]] (direct evidence): 提出EnergyFlow框架，通过参数化标量能量函数使去噪场为其梯度，证明保守场约束可从扩散策略中恢复专家的soft Q函数梯度作为奖励信号，无需对抗训练即可实现模仿学习与逆...
- [[giacomuzzo2024blackbox]] (broader context): 提出 LIP（Lagrangian Inspired Polynomial）核用于 GP 回归的机器人逆动力学辨识。核心思想：(1) 将动能和势能建模为 GP，通过 Lagr...
- [[zhang2026world2minecraft]] (broader context): 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[zhang2026joyaira]] (broader context): 京东提出的 VLA 基础模型 JoyAI-RA，通过多源多级预训练（网页数据 + 自建 EgoLive 自我中心视频 + 仿真 + 真机数据）和统一动作空间实现跨具身泛化操控...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[ye2026generation]] (broader context): 首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移

## Evidence Map

- Direct evidence papers: [[ji2026recovering]].
- Broader local evidence context: [[ji2026recovering]], [[giacomuzzo2024blackbox]], [[zhang2026world2minecraft]], [[zhang2026visionlanguageaction]], [[zhang2026joyaira]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[diffusion-model]]
- [[inverse-reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[ji2026recovering]]
- [[giacomuzzo2024blackbox]]
- [[zhang2026world2minecraft]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026joyaira]]
- [[zhang2026generative]]
- [[zeng2026recapa]]
- [[ye2026generation]]
