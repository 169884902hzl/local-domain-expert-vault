---
title: "Adaptive Compute"
tags: [concept, efficiency, planning]
created: "2026-05-12"
updated: "2026-05-12"
type: "concept"
status: "done"
summary: "根据场景难度自适应调整推理计算量，在简单场景减少计算、困难场景增加计算，实现效率与安全的平衡"
---

## Definition

Adaptive Compute is maintained here as an evidence-linked concept. 根据场景难度自适应调整推理计算量，在简单场景减少计算、困难场景增加计算，实现效率与安全的平衡

## Key Ideas

- Direct local evidence currently comes from [[puthumanaillam2026muninn]].
- The concept is tracked with local tags: concept, efficiency, planning.
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

- [[puthumanaillam2026muninn]] (direct evidence): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yu2026atrs]] (broader context): 将共享 DRL 策略嵌入并行 ADMM 轨迹优化循环，自适应再分割停滞段以加速四旋翼运动规划收敛，迭代减少最高 26%、机载实时重规划 35ms/周期。
- [[tu2026embody4d]] (broader context): 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VB...
- [[lee2026implicit]] (broader context): 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...
- [[zhou2026rcnf]] (broader context): 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anoma...
- [[zhou2025oneshot]] (broader context): BiDemoSyn 从单次真实示教分解出不变协调块和可变适应块，通过视觉引导对齐和轨迹优化合成数千条双臂操控演示，在6个接触丰富任务上显著优于 DemoGen/YOTO 等基线

## Evidence Map

- Direct evidence papers: [[puthumanaillam2026muninn]].
- Broader local evidence context: [[puthumanaillam2026muninn]], [[yuan2026prefmoe]], [[yu2026atrs]], [[tu2026embody4d]], [[lee2026implicit]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[trajectory-diffusion]]
- [[denoiser-caching]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[vision-language-action]]

## Related Papers

- [[puthumanaillam2026muninn]]
- [[yuan2026prefmoe]]
- [[yu2026atrs]]
- [[tu2026embody4d]]
- [[lee2026implicit]]
- [[iek2026coral]]
- [[zhou2026rcnf]]
- [[zhou2025oneshot]]
