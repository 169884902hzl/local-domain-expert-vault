---
title: "Motion Primitives"
tags: [planning, manipulation, control]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "参数化的运动基元，用少量参数生成任务空间轨迹，降低 RL 探索难度"
---

## Definition

Motion Primitives is maintained here as an evidence-linked concept. 参数化的运动基元，用少量参数生成任务空间轨迹，降低 RL 探索难度

## Key Ideas

- Direct local evidence currently comes from [[fang2026dexdrummer]].
- The concept is tracked with local tags: planning, manipulation, control.
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

- [[fang2026dexdrummer]] (direct evidence): 提出分层式灵巧鼓手机器人框架 DexDrummer，高层用参数化运动基元+残差 RL 实现鼓棒轨迹跟踪，低层用接触靶向奖励（指尖接触、支点奖励、手臂能量惩罚、接触课程）训练手...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[sundaralingam2026curobov2]] (broader context): 统一 GPU-native 运动生成框架，通过 B-spline 轨迹优化、密集 ESDF 感知管线和可扩展 whole-body 计算，实现从单臂到 48-DoF 人形机器...
- [[levy2026simulation]] (broader context): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[chen2026abotphysworld]] (broader context): 基于 Wan2.1 的 14B Diffusion Transformer，通过 300 万物理标注操控视频 SFT + VLM 解耦判别器 DPO 后训练，实现物理一致的可...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...

## Evidence Map

- Direct evidence papers: [[fang2026dexdrummer]].
- Broader local evidence context: [[fang2026dexdrummer]], [[zhou2026rcnf]], [[yuan2026prefmoe]], [[sundaralingam2026curobov2]], [[levy2026simulation]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[residual-rl]]
- [[planning]]
- [[reinforcement-learning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[fang2026dexdrummer]]
- [[zhou2026rcnf]]
- [[yuan2026prefmoe]]
- [[sundaralingam2026curobov2]]
- [[levy2026simulation]]
- [[iek2026coral]]
- [[chen2026abotphysworld]]
- [[zhou2026sim1]]
