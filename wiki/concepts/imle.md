---
title: "IMLE (Implicit Maximum Likelihood Estimation)"
tags: [concept, generative-model, planning]
created: "2026-05-07"
updated: "2026-05-07"
type: "concept"
status: "done"
summary: "隐式极大似然估计，一种隐式生成模型训练方法，通过最近邻匹配确保模式覆盖，推理速度比扩散模型快两个数量级"
---

## Definition

IMLE (Implicit Maximum Likelihood Estimation) is maintained here as an evidence-linked concept. 隐式极大似然估计，一种隐式生成模型训练方法，通过最近邻匹配确保模式覆盖，推理速度比扩散模型快两个数量级

## Key Ideas

- Direct local evidence currently comes from [[lee2026implicit]].
- The concept is tracked with local tags: concept, generative-model, planning.
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

- [[lee2026implicit]] (direct evidence): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线
- [[zhang2026prts]] (broader context): 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂...
- [[zeng2026recapa]] (broader context): 提出三层层级预测校正框架 ReCAPA，通过 action/subgoal/trajectory 三级预测与 Sinkhorn + Score-field 对齐机制，在训练阶...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[xu2026roboagent]] (broader context): 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD...

## Evidence Map

- Direct evidence papers: [[lee2026implicit]].
- Broader local evidence context: [[lee2026implicit]], [[zhou2026rcnf]], [[zhou2025oneshot]], [[zhang2026prts]], [[zeng2026recapa]].
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
- [[model-predictive-control]]
- [[mppi]]
- [[planning]]
- [[flow-matching]]
- [[robotic-manipulation]]

## Related Papers

- [[lee2026implicit]]
- [[zhou2026rcnf]]
- [[zhou2025oneshot]]
- [[zhang2026prts]]
- [[zeng2026recapa]]
- [[yu2026atrs]]
- [[yang2026ultradexgrasp]]
- [[xu2026roboagent]]
