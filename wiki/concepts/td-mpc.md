---
title: "TD-MPC"
tags: [world-model, model-based-RL, planning, MPC]
created: "2026-05-10"
updated: "2026-05-10"
type: "concept"
status: "done"
summary: "TD-MPC 是一种基于隐世界模型的规划方法，结合 TD learning 和 MPC 实现高效策略学习。"
---

## Definition

TD-MPC is maintained here as an evidence-linked concept. TD-MPC 是一种基于隐世界模型的规划方法，结合 TD learning 和 MPC 实现高效策略学习。

## Key Ideas

- Direct local evidence currently comes from [[levy2026simulation]].
- The concept is tracked with local tags: world-model, model-based-RL, planning, MPC.
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

- [[levy2026simulation]] (direct evidence): 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。

## Evidence Map

- Direct evidence papers: [[levy2026simulation]].
- Broader local evidence context: [[levy2026simulation]], [[lee2026implicit]], [[zhou2026rcnf]], [[zhou2025oneshot]], [[zhang2026prts]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[world-model]]
- [[model-predictive-control]]
- [[MPPI]]
- [[latent-dynamics-model]]
- [[planning]]
- [[robotic-manipulation]]

## Related Papers

- [[levy2026simulation]]
- [[lee2026implicit]]
- [[zhou2026rcnf]]
- [[zhou2025oneshot]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[yuan2026prefmoe]]
- [[yu2026atrs]]
