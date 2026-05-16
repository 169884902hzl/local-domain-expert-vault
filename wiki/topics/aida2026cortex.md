---
title: "Cortex 2.0: Grounding world models in real-world industrial deployment"
tags: [manipulation, imitation, VLM, bimanual, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model 生成并评分候选未来轨迹，在真实工业任务上提升长时序操控可靠性。"
authors: "Aida, Adriana; Amer, Walid; Bankovic, Katarina; Behl, Dhruv; Busch, Fabian et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "HT8TMS3A"
---
## 摘要

Industrial robotic manipulation（机器人操控） demands reliable long-horizon（长时序） execution across embodiments, tasks, and changing object distributions. While Vision-Language-Action models have demonstrated strong generalization, they remain fundamentally reactive. By optimizing the next action given the current observation without evaluating potential futures, they are brittle to the compounding failure modes of long-horizon（长时序） tasks. Cortex 2.0 shifts from reactive control to plan-and-act by generating candidate future trajectories in visual latent space, scoring them for expected success and efficiency, then committing only to the highest-scoring candidate. We evaluate Cortex 2.0 on a single-arm and dual-arm manipulation（双臂操控） platform across four tasks of increasing complexity: pick and place, item and trash sorting, screw sorting, and shoebox unpacking. Cortex 2.0 consistently outperforms state-of-the-art（现有最优方法） Vision-Language-Action baselines, achieving the best results across all tasks. The system remains reliable in unstructured environments characterized by heavy clutter, frequent occlusions, and contact-rich（接触丰富） manipulation（操控）, where reactive policies fail. These results demonstrate that world-model-based planning can operate reliably in complex industrial environments.

## 中文简述

提出基于视觉-语言的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、双臂操控、运动规划

## 关键贡献

1. 提出 Cortex 2.0，将 VLA 控制从 reactive control 改为 plan-and-act。
2. 引入 world model，在 visual latent space 中生成候选未来轨迹并评分 expected success 和 efficiency。
3. 提出 Process-Reward Operator (PRO)，用于评估 progress、risk 和 termination。
4. 在单臂和双臂工业平台上评估 pick-and-place、item/trash sorting、screw sorting 和 shoebox unpacking。
## 结构化提取

- Problem: Reactive VLA 在长时序工业操控中无法评估未来失败，导致错误累积。
- Method: VLM + visual latent world model + PRO trajectory scoring + flow-matching VLA action head。
- Tasks: pick-and-place、item/trash sorting、screw sorting、shoebox unpacking。
- Sensors: 视觉观测为主；论文讨论 industrial deployment 和 multimodal/force 相关背景。
- Robot Setup: 单臂和双臂工业操控平台。
- Metrics: 任务成功、候选轨迹评分、执行效率和跨任务表现；具体表格值未在 fallback 中逐项抄录。
- Limitations: 非 DLO、复现依赖系统工程和数据、world model 可能预测错误。
- Evidence Notes: arXiv HTML 全文；重点依据 Abstract、Methodology、Dataset Composition、Experiments 和 Results。
## 本地引用关系

- [[chen2025coordinated]]
- [[gu2026vistabot]]
- [[lee2025diffdagger]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high; abstract, method outline, dataset composition, tasks and result claims are available; exact table-level success values were not exhaustively transcribed in this fallback note.
- Confidence: medium-high
- Summary: Cortex 2.0 将 VLA 从 reactive next-action policy 扩展为 plan-and-act 系统，通过视觉潜空间 world model 生成并评分候选未来轨迹，在真实工业任务上提升长时序操控可靠性。


## Problem

工业机器人长时序操控需要跨 embodiment、任务和物体分布保持可靠。现有 Vision-Language-Action models 多数是 reactive policy，只根据当前观测输出下一步动作，缺少对潜在未来失败的评估，因此在 clutter、occlusion、contact-rich 和长时序任务中容易出现 compounding failures。


## Method

Cortex 2.0 包含高层 VLM、world model、PRO 评分模块和 VLA action head。高层 VLM 解析任务和场景，world model 在视觉潜空间中预测候选未来，PRO 对候选轨迹打分，系统只提交最高分候选。底层 VLA policy 使用 flow-matching action head，将规划结果映射到机器人动作。训练数据包括 real-world deployment data、open-source/synthetic data、in-house teleoperation data 和 world model pretraining data。


## Experiments

实验覆盖单臂 pick-and-place、物品与垃圾分类、螺丝分类、鞋盒拆包四类任务。论文声称 Cortex 2.0 在所有任务上优于 VLA baselines，尤其在杂乱、遮挡和接触丰富工业环境中更可靠。评估重点是任务成功、长时序稳定性和对 reactive failure 的缓解。


## Limitations

1. 论文主要面向工业刚体/半结构化任务，不是 DLO 或柔性物体操控。
2. world model 预测错误可能导致错误候选被高估，尤其在强接触或可变形状态下。
3. 需要较大训练数据和计算预算，低资源实验室复现成本较高。
4. 结果依赖私有部署数据和系统工程细节，完全复现难度较高。


## Key Takeaways

1. 对我们的价值在于“候选未来 + 风险评分 + 再执行”的范式，可迁移到 DLO 操控的失败预判。
2. idea 生成时可把 Cortex 2.0 作为 world-model-guided planning 证据，而不是作为 DLO baseline。
3. DLO 场景需要把 visual latent world model 扩展为物理/触觉/几何约束一致的 deformable-state predictor。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[planning]]
- [[deformable-linear-object]]

## 相关研究者

- [[aida|Aida, Adriana]]
