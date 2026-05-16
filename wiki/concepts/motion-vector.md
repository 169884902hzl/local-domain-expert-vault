---
title: "Motion Vector（运动向量）"
tags: [concept, representation]
created: "2026-05-09"
updated: "2026-05-09"
type: "concept"
status: "done"
summary: "视频编解码中用于压缩帧间冗余的宏块位移向量，作为 VLA 时序建模的紧凑动态表示"
---

## Definition

Motion Vector（运动向量） is maintained here as an evidence-linked concept. 视频编解码中用于压缩帧间冗余的宏块位移向量，作为 VLA 时序建模的紧凑动态表示

## Key Ideas

- Direct local evidence currently comes from [[lin2026hifvla]].
- The concept is tracked with local tags: concept, representation.
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

- [[lin2026hifvla]] (direct evidence): HiF-VLA 利用 MPEG-4 运动向量作为紧凑时序表示，通过后视先验编码、前视推理和后视调制联合专家实现双向时序推理，在 LIBERO-Long（96.4%）和 CAL...
- [[gu2026refinedp]] (broader context): 提出REFINE-DP框架，通过DPPO联合优化扩散策略高层规划器和RL底层控制器，使人形机器人loco-manipulation任务成功率从50-70%提升至90%+，仅需...
- [[zhou2026sim1]] (broader context): 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhang2026handx]] (broader context): 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scal...
- [[zhang2026generative]] (broader context): 将 flow matching 的动作生成从固定时间积分重构为驻定速度场上的迭代优化，实现自适应计算和零样本 OOD 检测，可即插即用替换 VLA 模型中的 flow head
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[yang2026twintrack]] (broader context): 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪...

## Evidence Map

- Direct evidence papers: [[lin2026hifvla]].
- Broader local evidence context: [[lin2026hifvla]], [[gu2026refinedp]], [[zhou2026sim1]], [[zhou2026rcnf]], [[zhang2026handx]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[vision-language-action]]
- [[world-model]]
- [[action-chunking]]
- [[long-horizon-manipulation]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[lin2026hifvla]]
- [[gu2026refinedp]]
- [[zhou2026sim1]]
- [[zhou2026rcnf]]
- [[zhang2026handx]]
- [[zhang2026generative]]
- [[yu2026atrs]]
- [[yang2026twintrack]]
