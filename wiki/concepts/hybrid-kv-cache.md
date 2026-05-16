---
title: "混合 KV 缓存 (Hybrid KV Cache)"
tags: [architecture, inference, VLA]
created: "2026-05-15"
updated: "2026-05-15"
type: "concept"
status: "done"
summary: "双流 KV Cache 架构，分别管理高频本体感觉历史（滚动 FIFO）和低频视觉-语言前缀（可刷新缓冲区）。"
---

## Definition

混合 KV 缓存 (Hybrid KV Cache) is maintained here as an evidence-linked concept. 双流 KV Cache 架构，分别管理高频本体感觉历史（滚动 FIFO）和低频视觉-语言前缀（可刷新缓冲区）。

## Key Ideas

- Direct local evidence currently comes from [[hu2026arvla]].
- The concept is tracked with local tags: architecture, inference, VLA.
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

- [[hu2026arvla]] (direct evidence): 提出独立的自回归 Action Expert，通过 Hybrid KV Cache 维护滚动运动历史和可刷新视觉-语言前缀，配合 Dynamic Temporal Re-an...
- [[zhou2026vlbiman]] (broader context): 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例...
- [[schperberg2026mobius]] (broader context): 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模...
- [[saad2026hybrid]] (broader context): 提出 LLM 高层任务规划 + RL 低层控制的混合框架，在 PyBullet 仿真中用 Franka Panda 实现了比纯 RL 方法快 33.5% 的任务完成时间和更高...
- [[puthumanaillam2026muninn]] (broader context): 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理...
- [[marougkas2025integrating]] (broader context): 提出势场+残差 RL 方法用于紧公差插入（<1mm）。先用势场控制器（吸引力+排斥力）在无噪声仿真中达到近 100% 成功率，再用 PPO 训练残差策略补偿观测噪声（仅稀疏奖...
- [[liu2025forcemimic]] (broader context): 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs...
- [[liang2026vanim]] (broader context): VAnim 提出基于 Sparse State Update 的 LLM 框架实现文本驱动的 SVG 动画生成，通过 Identification-First Motion...

## Evidence Map

- Direct evidence papers: [[hu2026arvla]].
- Broader local evidence context: [[hu2026arvla]], [[zhou2026vlbiman]], [[schperberg2026mobius]], [[saad2026hybrid]], [[puthumanaillam2026muninn]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[autoregressive-action-expert]]
- [[asynchronous-execution]]
- [[robotic-manipulation]]
- [[robot-learning]]
- [[planning]]
- [[vision-language-action]]

## Related Papers

- [[hu2026arvla]]
- [[zhou2026vlbiman]]
- [[schperberg2026mobius]]
- [[saad2026hybrid]]
- [[puthumanaillam2026muninn]]
- [[marougkas2025integrating]]
- [[liu2025forcemimic]]
- [[liang2026vanim]]
