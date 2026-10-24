---
title: "Tube diffusion policy: Reactive visual-tactile policy learning for contact-rich manipulation"
tags: [manipulation, imitation, diffusion, robot-learning, tactile]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal action chunk 的 observation-conditioned feedback flow，用于高频视觉-触觉接触丰富操控。"
authors: "Xue, Teng; Rigo, Alberto; Huang, Bingjian; Shen, Jiayi; Xu, Zhengtong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "8HVGWQGI"
---
## 摘要

Contact-rich（接触丰富） manipulation（操控） is central to many everyday human activities, requiring continuous adaptation to contact uncertainty and external disturbances through multi-modal（多模态） perception, particularly vision and tactile（触觉） feedback. While imitation learning（模仿学习） has shown strong potential for learning complex manipulation（操控） behaviors, most existing approaches rely on action chunking, which fundamentally limits their ability to react to unforeseen observations during execution. This limitation becomes especially critical in contact-rich（接触丰富） scenarios, where physical uncertainty and high-frequency tactile（触觉） feedback demand rapid, reactive control. To address this challenge, we propose Tube Diffusion Policy（扩散策略） (TDP), a novel reactive visual-tactile（触觉） policy learning framework that bridges diffusion（扩散）-based imitation learning（模仿学习） with tube-based feedback control. By leveraging the expressive power of generative models, TDP learns an observation-conditioned feedback flow around nominal action chunks, forming an action tube that enables fast and adaptive reactions during execution. We evaluate TDP on the widely used Push-T benchmark and three additional challenging visual-tactile（触觉） dexterous manipulation（灵巧操控） tasks. Across all benchmarks, TDP consistently outperforms state-of-the-art（现有最优方法） imitation learning（模仿学习） baselines. Two real-world experiments further validate its robust reactivity under contact uncertainty and external disturbances. Moreover, the step-wise correction mechanism enabled by action tube significantly reduces the required denoising steps, making TDP well suited for real-time, high-frequency feedback control in contact-rich（接触丰富） manipulation（操控）.

## 中文简述

提出基于扩散策略的灵巧手方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习、触觉感知

## 关键贡献

1. 提出 Tube Diffusion Policy (TDP)，把 diffusion-based imitation learning 和 tube-based feedback control 结合。
2. 用 diffusion phase 生成 nominal action chunk，再用 streaming phase 在每个控制步进行 flow-based correction。
3. 提出 action tube 表示，让策略围绕名义动作轨迹快速响应新观测。
4. 在 1-D point-mass、Push-T、虚拟视觉-触觉任务和真实接触任务上评估。
## 结构化提取

- Problem: Action chunking 在接触丰富任务中反应慢，扩散策略推理频率低，难以利用高频触觉反馈。
- Method: diffusion phase 生成 nominal action chunk；streaming phase 以 flow-based feedback control 做 step-wise correction，形成 action tube。
- Tasks: 1-D point-mass、Push-T、虚拟视觉-触觉灵巧操作、真实接触任务。
- Sensors: RGB/视觉输入、触觉反馈、机器人状态。
- Robot Setup: 论文含仿真和真实实验；具体硬件细节在原文附录。
- Metrics: success/score、denoising steps、reactivity、ablation；具体表格值未逐项录入。
- Limitations: 依赖示教、非 DLO、触觉硬件泛化和真实复杂接触稳定性待验证。
- Evidence Notes: arXiv HTML 全文；依据 Abstract、Methodology、Experiments、Results、Limitations。
## 本地引用关系

- [[li2025routing]]
- [[wu2025tacdiffusion]]
- [[zhao2025polytouch]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high; method, stability analysis outline, benchmarks, ablations and limitations are available; exact table values were not fully transcribed.
- Confidence: high
- Summary: Tube Diffusion Policy 将扩散式 action chunk 与 tube-based feedback control 结合，学习围绕 nominal action chunk 的 observation-conditioned feedback flow，用于高频视觉-触觉接触丰富操控。


## Problem

接触丰富操控需要根据触觉和视觉反馈连续调整动作。现有 imitation learning 常用 action chunking，一次生成一段动作，执行期间对未预见接触变化反应慢。扩散策略能表达复杂动作分布，但标准 denoising 推理频率低，难以处理高频触觉反馈。


## Method

TDP 使用 dual-time formulation。慢时间尺度上，扩散模型根据观测生成名义 action chunk；快时间尺度上，streaming flow policy 根据实时视觉/触觉反馈对当前动作做 step-wise correction。网络结构包含 U-Net backbone、FiLM-conditioned residual blocks、视觉和触觉 encoders。论文还给出 stability analysis，用 Lyapunov 风格分析 streaming phase 的误差演化。


## Experiments

实验包括 1-D point-mass、Push-T 的 state/image 输入版本、虚拟视觉-触觉 dexterous manipulation，以及真实机器人接触丰富任务。论文报告 TDP 在 Push-T 和视觉-触觉任务中优于 DDPM、DDIM、flow matching 等 baselines，并且用更少 denoising steps 达到有竞争力性能。Ablation 显示去掉 diffusion phase 会降低表现，说明仅依赖局部 linearization 不够。


## Limitations

1. TDP 仍依赖示教数据，未解决低数据量任务中的 demonstration acquisition。
2. 触觉硬件、采样频率和跨传感器泛化仍是部署风险。
3. 当前任务偏接触丰富刚体/灵巧操控，不直接覆盖 DLO。
4. 虽有稳定性分析，但真实复杂接触系统中的稳定性仍需实证。


## Key Takeaways

1. 这是今天最关键的 idea 证据之一：它直接说明 tactile + reactive correction 可以补足 action chunk 的开环问题。
2. 对 DLO routing，可以把 TDP 的 action tube 思路迁移为“nominal DLO path + tactile/contact correction”。
3. 可与 [[zhao2025polytouch]]、[[wu2025tacdiffusion]] 和 [[li2025routing]] 组合成 tactile-conditioned DLO diffusion policy 的实验路线。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[tactile-sensing]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[xue|Xue, Teng]]
