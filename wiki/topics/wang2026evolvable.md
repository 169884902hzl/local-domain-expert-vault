---
title: "Evolvable embodied agent for robotic manipulation via long short-term reflection and optimization"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt memory，在 VIMA-Bench 六个任务上提升 embodied agent 表现。"
authors: "Wang, Jianzong; Zhao, Botao; He, Yayun; Peng, Junqing; Zhang, Xulong"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "8ARAR6E4"
---
## 摘要

Achieving general-purpose robotics requires empowering robots to adapt and evolve based on their environment and feedback. Traditional methods face limitations such as extensive training requirements, difficulties in cross-task generalization, and lack of interpretability. Prompt learning offers new opportunities for self-evolving robots without extensive training, but simply reflecting on past experiences. However, extracting meaningful insights from task successes and failures remains a challenge. To this end, we propose the evolvable embodied agent (EEAgent) framework, which leverages large vision-language models (VLMs) for better environmental interpretation and policy planning. To enhance reflection on past experiences, we propose a long short-term reflective optimization (LSTRO) mechanism that dynamically refines prompts based on both past experiences and newly learned lessons, facilitating continuous self-evolution, thereby enhancing overall task success rates. Evaluations on six VIMA-Bench tasks reveal that our approach sets a new state-of-the-art（现有最优方法）, notably outperforming baselines in complex scenarios.

## 中文简述

提出基于模仿学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. 提出 Evolvable Embodied Agent (EEAgent)，用 VLM 做环境解释和 policy planning。
2. 提出 Long Short-Term Reflective Optimization (LSTRO)，动态更新 prompt memory。
3. 将错误定位、反思和 memory updating 分成明确步骤。
4. 在 VIMA-Bench 六个任务和 L1-L4 泛化协议中，与 CaP、Instruct2Act、CLIN、VIMA 系列和多种 prompting 策略比较。
## 结构化提取

- Problem: Embodied agent 难以从成功/失败中提取可复用经验，跨任务泛化和可解释性不足。
- Method: VLM environment interpreter + policy planner + LSTRO long/short-term memory update。
- Tasks: VIMA-Bench 六个任务，覆盖 L1-L4 泛化协议。
- Sensors: 视觉和语言任务输入；依赖 VLM/SAM 等感知模块。
- Robot Setup: VIMA-Bench embodied manipulation setting；非真实 DLO 硬件。
- Metrics: task success / benchmark average performance；具体表格值未逐项录入。
- Limitations: 仿真为主、非 DLO、依赖大模型、低层接触控制不足。
- Evidence Notes: arXiv HTML 全文；依据 Abstract、Methodology、Experiments and Results、Ablations。
## 本地引用关系

- [[chen2025coordinated]]
- [[li2025routing]]
- [[zhou2025oneshot]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high; method, benchmark, baselines, main performance and ablation descriptions are available; exact table values were only partially extracted.
- Confidence: medium-high
- Summary: EEAgent 用 VLM 解释环境和规划策略，并通过 Long Short-Term Reflective Optimization 从成功/失败经验中更新 prompt memory，在 VIMA-Bench 六个任务上提升 embodied agent 表现。


## Problem

传统机器人策略通常需要大量训练数据，跨任务泛化弱且难解释。LLM/VLM prompt learning 让机器人无需重新训练也能适配任务，但简单的失败反思很难提取可复用经验。论文要解决的问题是：如何让 embodied agent 从过去成功和失败中形成长期/短期记忆，并持续改进任务规划。


## Method

EEAgent 包含 Environment Interpreter、Policy Planner 和 LSTRO。Environment Interpreter 使用 VLM 解析场景和任务，Policy Planner 生成可执行动作/规划。LSTRO 在执行后定位错误、总结经验，并更新 long-term memory 与 short-term memory。长记忆保存跨任务可复用规律，短记忆服务当前任务或最近失败。


## Experiments

实验使用 VIMA-Bench，覆盖 placement generalization、combinatorial generalization、novel object generalization 和 novel task generalization。Baselines 包括 CaP、Instruct2Act、CLIN、VIMA-20M、VIMA-Gato、VIMA-Flamingo、VIMA-GPT，以及 vanilla embodied agent、CoT、self-consistency、reflection 等 prompting 策略。论文报告 EEAgent 在选定任务泛化设置中获得最高或更优平均表现，ablation 显示 LSTRO 和 memory 机制对性能有贡献。


## Limitations

1. 评估主要在 VIMA-Bench 仿真/语言视觉任务上，不是实际双臂 DLO 操控。
2. 系统依赖 GPT-4o/SAM 等大模型和视觉分割组件，成本和可复现性需要注意。
3. prompt memory 更新可能引入错误经验，缺少严格物理约束检查。
4. 对低层连续控制和接触动力学的作用有限，更适合高层策略和任务反思。


## Key Takeaways

1. 对 idea 生成最有价值的是“失败后反思 + 长短期记忆更新”的闭环，可用于 DLO 策略失败分类和下一轮数据采集。
2. 该工作不能直接证明 DLO 操控可自进化，但提供了 reflection-driven adaptation 的设计模板。
3. 我们可以把物理约束违反、张力异常、接触丢失作为 reflection 输入，而不是只用语言任务成功/失败。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[wang-jianzong|Wang, Jianzong]]
