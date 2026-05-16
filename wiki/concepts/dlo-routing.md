---
title: "DLO Routing"
tags: [concept, manipulation]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "将可变形线性物体（DLO）按指定顺序穿过多个夹子或通道的长时序操控任务。"
---

## Definition

DLO Routing is maintained here as an evidence-linked concept. 将可变形线性物体（DLO）按指定顺序穿过多个夹子或通道的长时序操控任务。

## Key Ideas

- Direct local evidence currently comes from [[li2026hierarchical]].
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

- [[li2026hierarchical]] (direct evidence): 提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion...
- [[wang2026radar]] (broader context): 提出全自主闭环数据采集引擎 RADAR，通过 VLM 语义规划 + GNN 图扩散模仿学习 + 三阶段 VQA 评估 + LIFO 自主环境重置，仅用 2-5 次人类示教即可...
- [[li2025routing]] (broader context): 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[wang2026ocra]] (broader context): 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界...
- [[wang2026evolvable]] (broader context): EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt...
- [[wang2025implicit]] (broader context): 提出 IPA（Implicit Physics-Aware Policy），用于通过柔性工具（软体绳索）动态操控刚性物体。核心创新是隐式物理感知：通过短时动作观测推断系统物理...

## Evidence Map

- Direct evidence papers: [[li2026hierarchical]].
- Broader local evidence context: [[li2026hierarchical]], [[wang2026radar]], [[li2025routing]], [[yuan2026prefmoe]], [[wu2026continually]].
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
- [[long-horizon-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[li2026hierarchical]]
- [[wang2026radar]]
- [[li2025routing]]
- [[yuan2026prefmoe]]
- [[wu2026continually]]
- [[wang2026ocra]]
- [[wang2026evolvable]]
- [[wang2025implicit]]
