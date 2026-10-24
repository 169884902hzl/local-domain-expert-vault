---
title: "Large reward models: Generalizable online robot reward generation with vision-language models"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器（时序对比/绝对进度/任务完成），在 ManiSkill3 零样本长时序操控和真实世界 pick-and-place 上分别用 30 次 RL 迭代和 60 次 rollout 显著提升 IL 基线成功率。"
authors: "Wu, Yanru; Yuan, Weiduo; Qi, Ang; Guizilini, Vitor; Mao, Jiageng et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "BASQDHRW"
---
## 摘要

Reinforcement Learning（强化学习） (RL) has shown great potential in refining robotic manipulation（机器人操控） policies, yet its efficacy remains strongly bottlenecked by the difficulty of designing generalizable reward（奖励） functions. In this paper, we propose a framework for online policy refinement by adapting foundation VLMs into online reward（奖励） generators. We develop a robust, scalable reward（奖励） model based on a state-of-the-art（现有最优方法） VLM, trained on a large-scale, multi-source dataset encompassing real-world robot trajectories, human-object interactions, and diverse simulated environments. Unlike prior approaches that evaluate entire trajectories post-hoc, our method leverages the VLM to formulate a multifaceted reward（奖励） signal comprising process, completion, and temporal contrastive rewards based on current visual observations. Initializing with a base policy trained via Imitation Learning（模仿学习） (IL), we employ these VLM rewards to guide the model to correct sub-optimal behaviors in a closed-loop（闭环） manner. We evaluate our framework on challenging long-horizon（长时序） manipulation（操控） benchmarks requiring sequential execution and precise control. Crucially, our reward（奖励） model operates in a purely zero-shot（零样本） manner within these test environments. Experimental results demonstrate that our method significantly improves the success rate of the initial IL policy within just 30 RL iterations, demonstrating remarkable sample efficiency. This empirical evidence highlights that VLM-generated signals can provide reliable feedback to resolve execution errors, effectively eliminating the need for manual reward（奖励） engineering and facilitating efficient online refinement for robot learning.

## 中文简述

提出基于强化学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. 提出 Large Reward Models (LRMs) 框架，将基础 VLM 特化为帧级密集奖励生成器，实现闭环策略精炼
2. 设计三模态奖励公式：时序对比奖励（r_cont）、绝对进度奖励（r_prog）和任务完成奖励（r_comp），覆盖相对方向、绝对量化和终止判断三个认知维度
3. 在 24 个多源数据集（机器人、人类操作、仿真）上训练，在 ManiSkill3 零样本长时序操控和真实世界部署中验证有效性，仅 30 次 RL 迭代即显著提升成功率
## 结构化提取

- Problem: RL 奖励工程是机器人操控策略精炼的核心瓶颈，现有 VLM 奖励方法要么稀疏要么计算量随轨迹增长
- Method: Large Reward Models (LRMs) — 将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器，结合 PPO 在线精炼 IL 基线策略
- Tasks: 长时序操控（ManiSkill3 多阶段任务）、真实世界 pick-and-place（玩具放入碗中）
- Sensors: RGB 相机（视觉观察 I_t）
- Robot Setup: ManiSkill3 仿真（320 并行环境）、真实世界单臂机器人（π0.5 policy，20 teleop demos）
- Metrics: 闭环成功率（%）、ROC-AUC、Pearson 相关、Kendall's τ、Spearman's ρ、MAE、RMSE、Acc@±Δ
- Limitations: 真实世界实验仅一任务；r_comp 提升边际；K=10 查询间隔可能不公平；未涉及可变形物体；未报告推理延迟
- Evidence Notes:

  - 三模态奖励均可独立驱动策略改进，r_comp 成功率最高（60.93%）
  - LRM 奖励质量随 RL 训练进行同步提升（RL 与奖励模型对齐的正反馈）
  - 真实世界 60 rollouts 即可将成功率从 38.3% 提升至 51.7%（r_comp 作为轨迹过滤器）
  - 进度估计 r_prog 的 ROC-AUC 在 RL 后达到 0.950，接近 oracle 水平
## 本地引用关系

- [[wu2026large]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML版本，含全文正文、公式、表格、图片描述)
- Evidence Coverage: high (方法、实验、消融、真实世界部署均有详细描述)
- Confidence: high
- Summary: 将 Qwen3-VL-8B 通过 LoRA 特化为三模态帧级奖励生成器（时序对比/绝对进度/任务完成），在 ManiSkill3 零样本长时序操控和真实世界 pick-and-place 上分别用 30 次 RL 迭代和 60 次 rollout 显著提升 IL 基线成功率。


## Problem

RL 在机器人操控中有潜力突破模仿学习的性能天花板，但核心瓶颈在于设计可泛化的奖励函数。现有方法要么提供稀疏的 episode 级奖励（如 RoboReward），要么随轨迹长度增长计算开销（如 RoboMeter 的累积帧上下文）。需要一种能在零样本设定下提供帧级密集奖励的方法。


## Method

- **骨干模型**: Qwen3-VL-8B-Instruct，通过 LoRA 微调
- **训练数据**: 24 个来源的结构化数据集 D = {(I_t, d, p_t)}
  - 真实机器人: Open X-Embodiment
  - 人类操作: HOI4D, EgoDex
  - 仿真环境: LIBERO, RoboCasa
  - 时序采样: 每条轨迹提取 11 个 keyframe（p ∈ {0.0, 0.1, ..., 1.0}）
- **三模态奖励**:
  - Temporal Contrastive Reward (r_cont): 比较帧对 (I_{t-Δt}, I_t) 判断哪帧更接近目标，输出 {+1, -1, 0}，用 DPO + CoT 训练
  - Absolute Progress Reward (r_prog): 单帧估计任务完成百分比（0.0-1.0 离散 11 级），用 SFT + CoT 训练
  - Task Completion Reward (r_comp): 二值判断是否满足语义目标，用 SFT 训练
- **在线策略精炼**: 基于 PPO + GAE，使用 Interval-Hold 策略（每 K 步查询 LRM 并缓存奖励），从 π_SFT 初始化
- **真实世界应用**: 用 r_comp 作为自动分类器过滤成功轨迹，迭代微调策略


## Experiments

### LRM 奖励质量评估
- **时序对比**: Kendall's τ 和 Spearman's ρ 提升 15.3%（对比零样本 Qwen3-VL-8B baseline）
- **进度估计**: MAE 降低 20.0%，RMSE 降低 19.3%，Acc@±0.2 提升 8.6 个百分点
- **任务完成**: 69.38% vs baseline 69.23%（边际提升，说明基础 VLM 已具备较强的语义目标识别能力）

### ManiSkill3 零样本闭环评估（320 并行环境，30 RL 迭代）
| 方法 | 成功率 |
|------|--------|
| π_SFT baseline | 未明确报告基线值（论文仅报告精炼后数值） |
| LRM (r_comp) | 60.93% |
| LRM (r_cont) | 60.31% |
| LRM (r_prog) | 60.00% |
| RoboReward-8B | 低于 LRM r_prog（Table IV） |
| RoboMeter-4B | 低于 LRM r_prog（Table IV） |
| Env Reward（上界） | 最高，使用特权状态 |
注：Table IV 中统一 K=10 查询间隔，作者承认此设置可能不利于 RoboReward 等稀疏方法

### 开环奖励质量分析（80 条轨迹对比 oracle）
- r_comp ROC-AUC: 0.660 → 0.795（RL 后提升）
- r_prog ROC-AUC: 0.874 → 0.950（RL 后提升）
- r_prog per-trajectory Pearson 相关: 0.671
- r_cont 步级方向准确率: 85.5%

### 真实世界 pick-and-place（玩具长颈鹿放入碗中）
| 方法 | 成功率 |
|------|--------|
| SFT baseline（20 demos 微调 π0.5） | 38.3% |
| LRM refined（60 rollouts, r_comp 过滤） | 51.7% |


## Limitations

1. 任务完成模型（r_comp）相对零样本 baseline 仅边际提升，说明 VLM 原生能力在二值判断上已较强
2. 统一 K=10 查询间隔的公平性存疑，RoboReward 等设计用于更稀疏查询的方法可能被低估
3. 真实世界实验仅限单一 pick-and-place 任务，泛化性验证不足
4. LRM 奖励与特权环境奖励仍有明显差距
5. 未涉及可变形物体（DLO）操控，所有实验均为刚体操作
6. 论文未报告单次 LRM 推理延迟，仅提到 Interval-Hold 缓解计算问题
7. 进度估计使用离散 11 级而非连续值，粒度受限


## Key Takeaways

1. **三模态奖励分解是强设计模式**: 时序对比提供方向梯度、进度估计提供量化反馈、完成判断提供终止信号——三者互补且可独立使用
2. **帧级 vs 轨迹级奖励是关键区分**: LRM 的帧级输入避免了 RoboMeter 式的累积上下文膨胀，更适合在线高频反馈
3. **多域训练实现零样本泛化**: 机器人 + 人类 + 仿真三类数据混合训练，使 LRM 在完全未见过的 ManiSkill3 环境中有效
4. **Interval-Hold 策略实用**: 通过缓存奖励桥接 VLM 推理频率与控制频率的差距
5. **与 DLO 操控的潜在关联**: 奖励建模框架可直接应用于 DLO 任务，但需要额外处理形变状态的可视化评估

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[wu-yanru|Wu, Yanru]]
- [[yuan-weiduo|Yuan, Weiduo]]
- [[qi-ang|Qi, Ang]]
- [[guizilini-vitor|Guizilini, Vitor]]
