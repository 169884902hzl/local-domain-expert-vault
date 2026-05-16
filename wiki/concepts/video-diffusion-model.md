---
title: "Video Diffusion Model"
tags: [diffusion, robot-learning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Video diffusion model 学习时空一致的视频潜表示，可用于视角合成、状态预测和机器人策略特征提取。"
---

## Definition

Video Diffusion Model (VDM) 是把扩散生成扩展到视频序列的模型族，通常通过时空 VAE、Diffusion Transformer 或 cross-attention 建模帧间一致性。在机器人操控中，VDM 的价值不一定是生成最终视频，而是提供包含几何、语义和时序信息的潜表示。

## Key Ideas

- VDM 可以把历史帧、目标视角和文本/图像条件整合到一个时空潜空间。
- [[gu2026vistabot]] 使用 CogVideoX 的潜空间特征作为动作策略输入，避免生成图像再编码。
- 视频扩散的时序 memory 有助于闭环控制中的状态一致性，但推理频率可能成为实时控制瓶颈。
- VDM 生成结果若缺乏物理约束，可能在接触任务中产生视觉上合理但控制上错误的状态。
- 在机器人中使用 VDM 时，latent 是否可控、是否保留动作相关几何，比生成视频主观质量更关键。

## Method Families

- Text/image-conditioned video generation: 根据文本、图像或历史帧生成视频。
- View synthesis VDM: 以目标视角或几何投影为条件，生成新视角视频或潜表示。
- Latent feature extraction: 不解码视频，直接把 VDM latent 作为策略观测。
- World-model-style prediction: 用视频生成预测未来观测或状态，用于规划和评估。

## Key Papers

- [[gu2026vistabot]]: 用 CogVideoX 进行视角合成潜特征提取，并接入 ACT/π₀ 控制框架。
- [[chi2024diffusion]]: 虽不是 VDM，但建立了机器人动作扩散的基础范式，便于区分 action diffusion 与 video diffusion。
- [[keunknowndiffuser]]: 使用 3D 场景表示和扩散策略，提供 VDM 与三维潜表示结合的相邻证据。
- [[lee2025diffdagger]]: 提供 diffusion loss 作为不确定性信号的证据，可启发 VDM latent 的可靠性评估。
- [[chen2025coordinated]]: 使用 state diffusion 预测未来状态，是视频/状态生成模型服务控制的相邻路线。

## Evidence Map

- [[gu2026vistabot]] 证明 VDM latent 可直接服务机器人跨视角操控，而不只作为视觉生成模块。
- [[gu2026vistabot]] 的限制指出推理约 3 Hz，对高速任务不够。
- [[chi2024diffusion]] 和 [[keunknowndiffuser]] 提供对照：机器人扩散可作用于动作、轨迹或三维场景表示，不必局限于视频像素生成。

## Open Problems

- 如何把 VDM 的生成先验与接触物理、力觉和机器人状态一致性约束结合。
- 如何降低 VDM 推理延迟，使其能进入高频闭环控制。
- 如何判断 VDM latent 是否真的编码了任务相关几何，而不是外观纹理。
- 如何扩展到 DLO 操控中长时间、多接触、可变形状态的视频预测。

## Related Concepts

- [[diffusion-model]]
- [[diffusion-policy]]
- [[novel-view-synthesis]]
- [[robotic-manipulation]]

## Related Papers

- [[gu2026vistabot]]
- [[chi2024diffusion]]
- [[keunknowndiffuser]]
