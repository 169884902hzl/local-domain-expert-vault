---
title: "Reinforcement Learning with Foundation Priors: Let the Embodied Agent Efficiently Learn on Its Own"
tags: [manipulation, RL, robot-learning]
created: "2026-05-05"
updated: "2026-05-05"
type: "literature"
status: "done"
summary: "提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控"
authors: "Ye, Weirui; Zhang, Yunsheng; Weng, Haoyang; Gu, Xianfan; Wang, Shengjie et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PM4EWHMF"
---
## 摘要

Reinforcement learning（强化学习） (RL) is a promising approach for solving robotic manipulation（机器人操控） tasks. However, it is challenging to apply the RL algorithms directly in the real world. For one thing, RL is data-intensive and typically requires millions of interactions with environments, which are impractical in real scenarios. For another, it is necessary to make heavy engineering efforts to design reward（奖励） functions manually. To address these issues, we leverage foundation models in this paper. We propose Reinforcement Learning（强化学习） with Foundation Priors (RLFP) to utilize guidance and feedback from policy, value, and success-reward（奖励） foundation models. Within this framework, we introduce the Foundation-guided Actor-Critic (FAC) algorithm, which enables embodied agents to explore more efficiently with automatic reward（奖励） functions. The benefits of our framework are threefold: (1) \textit{sample efficient}; (2) \textit{minimal and effective reward（奖励） engineering}; (3) \textit{agnostic to foundation model forms and robust to noisy priors}. Our method achieves remarkable performances in various manipulation（操控） tasks on both real robots and in simulation. Across 5 dexterous（灵巧） tasks with real robots, FAC achieves an average success rate of 86\% after one hour of real-time learning. Across 8 tasks in the simulated Meta-world, FAC achieves 100\% success rates in 7/8 tasks under less than 100k frames (about 1-hour training), outperforming baseline methods with manual-designed rewards in 1M frames. We believe the RLFP framework can enable future robots to explore and learn autonomously in the physical world for more tasks. Visualizations and code are available at https://yewr.github.io/rlfp.

## 中文简述

提出基于强化学习的灵巧手方法。

**研究方向**: 机器人操控、强化学习、机器人学习

## 关键贡献

1. **RLFP 框架**：系统性地提出将三种 foundation model 先验（策略 Mπ、价值 M𝒱、成功奖励 Mℛ）注入 RL 的统一框架，形式化为扩展的 GCMDP 𝒢' = (𝒢, ℳ)
2. **FAC 算法**：基于 Actor-Critic 架构（DrQ-v2 变体），通过 policy regularization（策略先验）、reward shaping（价值先验）、success buffer imitation（成功奖励先验）三种机制利用先验知识
3. **实证验证**：真实机器人 5 个灵巧任务平均 86% 成功率（1 小时训练）；Meta-World 8 个任务中 7/8 达 100% 成功率（<100k frames）；系统消融证明每个先验的贡献和对噪声的鲁棒性
## 结构化提取

- Problem: RL 在真实机器人上样本效率低、奖励工程重
- Method: RLFP 框架 + FAC 算法（DrQ-v2 + policy regularization + value-based reward shaping + success buffer imitation）
- Tasks: 桌面灵巧操控（Pick Place, Open Door, Watering Plants, Unscrew Bottle Cap, Play Golf）+ Meta-World 8 任务
- Sensors: 固定外部 RGB 相机 + 腕部 RGB 相机
- Robot Setup: Franka Emika Panda（7-DoF 臂 + 1-DoF 平行爪夹爪），桌面环境，物体位置随机化
- Metrics: 成功率（10 次评估平均，3 seeds），样本效率（达到目标成功率所需 frames）
- Limitations: 依赖人工设计底层技能和 prompt；仿真需 in-domain 微调扩散模型；GPT-4V 在仿真中失效；未验证复杂场景（DLO、多臂）；强噪声先验下不够鲁棒
- Evidence Notes:

  - 真实机器人：5 任务平均 86% 成功率（1h 训练），vs Code Prior 22%，vs Vanilla RL 0%（Table 1）
  - 仿真 Meta-World：8 任务全部 100% 成功率，7/8 在 <100k frames 达到（Figure 6）
  - 消融：成功奖励先验最关键；策略先验对困难任务不可或缺；价值先验和 success buffer 提升效率（Figure 8a）
  - 鲁棒性：离散化策略先验性能接近原始；20% 随机噪声可接受；蒸馏奖励模型（50k 图像）替代 oracle 奖励性能下降有限（Figure 8b, c）
## 本地引用关系

- [[ye2026reinforcement]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML v5, 84523 chars)
- Evidence Coverage: complete (all sections read: Abstract, Intro, Related Work, Method, Experiments, Ablation, Discussion, References)
- Confidence: high
- Summary: 提出 RLFP 框架，将 foundation model 的策略先验、价值先验和成功奖励先验三种知识系统注入 RL，实现在真实机器人上 1 小时训练达 86% 成功率的灵巧操控


## Problem

RL 应用于真实机器人操控面临两大核心挑战：
1. **样本效率低**：标准 RL 算法（如 DrQ-v2）需要数百万次环境交互，在真实场景不可行
2. **奖励工程重**：需要人工设计密集奖励函数，工程负担大

受人类学习范式启发（观察行为 → 调整策略 → 强化成功），论文探索如何利用 foundation model 的先验知识来同时解决这两个问题。


## Method

### RLFP 框架形式化
- 将任务建模为 Goal-Conditioned MDP (GCMDP)：𝒢 = (𝒮, 𝒜, 𝒫, ℛ, 𝒯, γ)
- 扩展为 𝒢' = (𝒢, ℳ)，其中 ℳ 是 foundation model 集合
- 三种先验：
  - **策略先验** Mπ(s, 𝒯): 𝒮 × 𝒯 → 𝒜，提供合理初始行为
  - **价值先验** M𝒱(s, 𝒯): 𝒮 × 𝒯 → ℝ，评估状态好坏
  - **成功奖励先验** Mℛ(s, 𝒯): 𝒮 × 𝒯 → {0,1}，判断任务是否成功

### FAC (Foundation-guided Actor-Critic) 算法
基于 DrQ-v2，增加三个关键组件：

1. **Success-reward 指导**：用 Mℛ 识别成功轨迹存入 success buffer 𝒟succ，训练时对 actor 施加行为克隆损失 ℒsucc = KL(πϕ(st), 𝒩(at, σ̂²))
2. **Policy regularization**：对 actor 施加 KL 散度约束使其接近策略先验 ℒreg = KL(πϕ, 𝒩(Mπ(st, 𝒯), σ̂²))，证明先验偏差有上界（Theorem 2）
3. **Value-based reward shaping**：利用价值先验构造势函数 F(s, s', 𝒯) = γM𝒱(s', 𝒯) - M𝒱(s, 𝒯)，与成功奖励组合为最终奖励 ℛ = λMℛ + F（λ=100）

**安全探索**：训练初期用策略先验动作预热（10 轨迹）；执行时由 critic 在 actor 和 prior 动作中选择更优者（a* = arg max Q(s, ai)），随着训练进行逐步偏向 actor

### Foundation Model 获取方式
- **成功奖励先验**：真实任务用 GPT-4V 判断最终观测是否成功；仿真用 ground-truth 0-1 奖励
- **策略先验**：真实任务用 GPT-4V 生成代码策略（基于 Code as Policies [35]）；仿真用 Seer [21]（视频扩散模型）蒸馏策略
- **价值先验**：使用 VIP [36]（基于大规模数据预训练的通用价值模型）


## Experiments

### 真实机器人实验（Table 1）
- **硬件**：Franka Emika Panda（7-DoF 臂 + 1-DoF 夹爪）
- **传感器**：固定外部 RGB 相机 + 腕部相机
- **5 个灵巧任务**：Pick Place（30 min, 40 轨迹）、Open Door（60 min, 75 轨迹）、Watering Plants（60 min, 60 轨迹）、Unscrew Bottle Cap（60 min, 50 轨迹）、Play Golf（60 min, 115 轨迹）
- **结果**（10 次评估平均）：
  - Pick Place: 70%, Open Door: 90%, Watering Plants: 80%, Unscrew Bottle Cap: 90%, Play Golf: 100%
  - **FAC 平均 86%**，Code Policy Prior 平均 22%，Vanilla DrQ-v2 全部失败（0%）

### Meta-World 仿真实验（Figure 6）
- **8 个任务**：FAC 在 7/8 任务中 <100k frames（约 1 小时）达到 100% 成功率
- 较难的 bin-picking 任务需要 <400k frames
- 对比基线：DrQ-v2（人工奖励，1M frames）、R3M+DrQ-v2、VIP+DrQ-v2、UniPi、蒸馏策略
- FAC 全面超越所有基线，包括使用人工设计奖励在 1M frames 下训练的 DrQ-v2

### 消融实验（Figure 8）
1. **各先验重要性**：成功奖励先验最关键（去掉后性能大幅下降或失败）；策略先验对困难任务（bin-picking, door-opening）不可或缺；价值先验和 success buffer 提升样本效率
2. **对策略先验噪声的鲁棒性**：离散化策略（仅 {-1, 0, +1}）与原始策略性能相近；加 20% 均匀噪声仍可收敛；50% 噪声下多数环境仍达 100%
3. **对成功奖励先验噪声的鲁棒性**：用 50k 图像蒸馏的代理模型（1.7% 假阳性，9.9% 假阴性）替代 oracle 奖励，性能下降有限


## Limitations

1. 仍需人工设计底层技能原语（move_to, grasp, release, rotate_anticlockwise）和 prompt
2. 仿真中需用 in-domain 数据微调视频扩散模型才能获得有效策略先验
3. GPT-4V 作为成功奖励在仿真图像上表现差，仿真实验仍依赖 ground-truth 奖励
4. 仅在桌面级操控任务上验证，未涉及更复杂的场景（如 DLO 操控、多臂协作）
5. 策略先验 50% 反向噪声时性能严重下降，对系统性强误导不够鲁棒


## Key Takeaways

1. **对 DLO 操控的启发**：RLFP 的三层先验框架可直接应用于 DLO 任务——VLM 生成抓取-弯曲策略作为策略先验，VIP 类模型评估形变状态作为价值先验，视觉判断操控完成度作为成功奖励先验
2. **Reward shaping 理论保证**：基于势函数的 reward shaping 证明不改变最优策略，这为 DLO 稀疏奖励场景提供了理论支撑
3. **VLM 作为 reward source**：GPT-4V 判断任务成功的思路可用于 DLO 的形变评估，但需要更细粒度的视觉理解
4. **Sim-to-Real 潜力**：1 小时真实训练时间具有实际部署价值，框架对 foundation model 噪声的鲁棒性降低了 Sim-to-Real 中模型迁移的精度要求
5. **与当前研究方向的关系**：本论文为"foundation model 辅助 RL"提供了系统框架，可与我们双臂 DLO 操控的研究结合——特别是在设计自动奖励和加速真实世界学习方面

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[ye-weirui|Ye, Weirui]]
