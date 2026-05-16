---
title: "Real-Time Chunking (RTC)"
tags: [manipulation, imitation-learning, action-chunking]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "将异步 action chunking 执行重新表述为 inpainting 问题，冻结已执行 action 并生成一致的未来 action。"
---

## Definition

Real-Time Chunking (RTC) is maintained here as an evidence-linked concept. 将异步 action chunking 执行重新表述为 inpainting 问题，冻结已执行 action 并生成一致的未来 action。

## Key Ideas

- Direct local evidence currently comes from [[wang2026discretertc]].
- The concept is tracked with local tags: manipulation, imitation-learning, action-chunking.
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

- [[wang2026discretertc]] (direct evidence): 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超...
- [[xue2026tube]] (broader context): Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal a...
- [[gu2026vistabot]] (broader context): VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，V...
- [[zhang2026visionlanguageaction]] (broader context): 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确...
- [[wu2025tacdiffusion]] (broader context): 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键...
- [[wu2025imperfect]] (broader context): 提出 SSDF（Self-Supervised Data Filtering）框架，从失败轨迹中筛选高质量片段扩展训练数据。三步：(1) 多模态 Transformer 自监...
- [[so2025evaluating]] (broader context): 提出基于联网电子任务板的机器人操控基准，用于评估电气电路检查（万用表使用）的人机技能差距。6 个子任务：定位任务板+按键→读取屏幕+调整滑块→插入探针插头→开门+探针电路→缠...
- [[shi2025zeromimic]] (broader context): 提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓...

## Evidence Map

- Direct evidence papers: [[wang2026discretertc]].
- Broader local evidence context: [[wang2026discretertc]], [[xue2026tube]], [[gu2026vistabot]], [[zhang2026visionlanguageaction]], [[wu2025tacdiffusion]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[action-chunking]]
- [[asynchronous-execution]]
- [[discrete-diffusion-policy]]
- [[diffusion-model]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[wang2026discretertc]]
- [[xue2026tube]]
- [[gu2026vistabot]]
- [[zhang2026visionlanguageaction]]
- [[wu2025tacdiffusion]]
- [[wu2025imperfect]]
- [[so2025evaluating]]
- [[shi2025zeromimic]]
