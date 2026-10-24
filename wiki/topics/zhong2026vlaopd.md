---
title: "VLA-OPD: Bridging offline SFT and online RL for vision-language-action models via on-policy distillation"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师提供 token 级密集监督，避免 Forward-KL 的熵爆炸和 Hard-CE 的熵坍塌，在 LIBERO 上 1-traj 初始化即达 87.4% 成功率。"
authors: "Zhong, Zhide; Yan, Haodong; Li, Junfeng; He, Junjie; Zhang, Tianran et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "D8KAAHEI"
---
## 摘要

Although pre-trained Vision-Language-Action (VLA) models exhibit impressive generalization in robotic manipulation（机器人操控）, post-training remains crucial to ensure reliable performance during deployment. However, standard offline Supervised Fine-Tuning (SFT) suffers from distribution shifts and catastrophic forgetting of pre-trained capabilities, while online Reinforcement Learning（强化学习） (RL) struggles with sparse rewards and poor sample efficiency. In this paper, we propose On-Policy VLA Distillation (VLA-OPD), a framework bridging the efficiency of SFT with the robustness of RL. Instead of relying on sparse environmental rewards, VLA-OPD leverages an expert teacher to provide dense, token-level supervision on the student's self-generated trajectories. This enables active error correction on policy-induced states while preserving pre-trained general capabilities through gentle alignment. Crucially, we formulate VLA-OPD via a Reverse-KL objective. Unlike standard Forward-KL that induces mode-covering entropy explosion, or Hard-CE that causes premature entropy collapse, our bounded mode-seeking objective ensures stable policy learning by filtering out the teacher's epistemic uncertainty while maintaining action diversity. Experiments on LIBERO and RoboTwin2.0 benchmarks demonstrate that VLA-OPD significantly improves sample efficiency over RL and robustness over SFT, while effectively mitigating catastrophic forgetting during post-training.

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **VLA-OPD 统一框架**：提出 On-Policy VLA Distillation，在学生自生成轨迹上用教师提供密集 token 级监督，同时解决 SFT 的曝光偏差和稀疏奖励 RL 的样本低效
2. **Reverse-KL 蒸馏目标**：证明 Reverse-KL 的有界 mode-seeking 特性可以过滤教师的认知不确定性同时保持动作多样性，优雅地避免 Forward-KL 熵爆炸和 Hard-CE 熵坍塌
3. **灾难性遗忘缓解**：通过确保梯度更新锚定在学生当前策略流形上，实现"温和"对齐，保持预训练通用能力
4. **广泛实验验证**：在 LIBERO 和 RoboTwin2.0 上展示优于 SFT 的鲁棒性和优于 RL 的样本效率
## 结构化提取

- **Problem**: VLA 模型 post-training 中 SFT 的分布偏移/灾难性遗忘 vs RL 的稀疏奖励/样本低效困境
- **Method**: On-Policy Distillation — 学生 on-policy 采样 → 教师密集标注 → Reverse-KL 优化；Group-Based gradient estimation
- **Tasks**: 单臂桌面操控（LIBERO: Spatial/Object/Goal/Long）、双臂协作操控（RoboTwin2.0: Pick dual bottles, Place empty cup, Handover block, Stack bowls）
- **Sensors**: 视觉观测（图像）+ 语言指令
- **Robot Setup**: LIBERO（单臂，仿真桌面）、RoboTwin2.0（双臂，仿真）；均基于 OpenVLA-OFT backbone
- **Metrics**: 任务成功率（%）、训练步数/效率、动作熵、seen-unseen trade-off
- **Limitations**: 依赖预训练教师模型；未在真实机器人上验证；教师推理开销；未讨论跨形态适用性
- **Evidence Notes**:

  - Table 2: LIBERO 上 1-traj VLA-OPD Distill 87.4% vs Student Init 48.9%，Distill+GRPO 93.4% vs Teacher 93.9%
  - Table 3: RoboTwin2.0 Distill 71.1% vs Init 45.2% vs Teacher 74.0%
  - Figure 2: LIBERO-Long 3× 训练加速
  - Figure 3: On-policy 方法显著减轻灾难性遗忘
  - Figure 4: Reverse-KL 避免熵爆炸和熵坍塌的消融验证
  - Figure 5: G=2 即可达到 80%+，G=8 最优 ~89%
## 本地引用关系

- [[zhong2026vlaopd]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 完整获取)
- Evidence Coverage: 完整覆盖所有章节（Introduction, Preliminaries, Methodology, Experiments, Ablation, Related Work, Conclusion），包含所有表格数据和公式推导
- Confidence: high
- Summary: 提出 VLA-OPD 框架，通过 On-Policy 蒸馏将 SFT 的密度监督与 RL 的在线探索结合，核心创新是 Reverse-KL 目标函数，在学生自生成轨迹上用教师提供 token 级密集监督，避免 Forward-KL 的熵爆炸和 Hard-CE 的熵坍塌，在 LIBERO 上 1-traj 初始化即达 87.4% 成功率。


## Problem

VLA 模型 post-training 面临两难困境：
1. **Offline SFT** 存在分布偏移（distribution shift）和灾难性遗忘（catastrophic forgetting）问题——模型在专家状态上训练但在自身诱导状态上评估，执行误差不断累积
2. **Online RL** 虽能通过环境交互解决分布偏移，但依赖稀疏奖励（仅任务成功/失败的二元信号），导致样本效率极低、优化方差高
3. 直接将 SFT 改为 on-policy（如 DAgger）使用 Forward-KL 会引发熵爆炸，使用 Hard-CE 则导致熵坍塌


## Method

### 整体架构（三阶段循环）

**Phase 1: On-Policy Sampling（学生探索）**
- 学生策略 π_θ 在环境中生成轨迹 D_k
- 关键：状态来自学生诱导分布 d^{π_θ}，而非专家分布
- 对于仅有 1 条 demo 初始化的学生，频繁遇到 OOD 状态，显式捕获"失败状态"用于后续纠正

**Phase 2: Dense Teacher Labeling（教师标注）**
- 冻结的教师策略 π_tea 对学生访问的每个状态提供动作分布 q_t(a) = π_tea(a|s_t)
- 优势：(1) 将延迟 RL 问题转为即时监督信号；(2) 在 OOD 状态上传授恢复行为

**Phase 3: Mode-Seeking Optimization（优化更新）**
- 优化目标：max_θ J(θ) = E_{s~π_θ}[-D_KL(π_θ(·|s) || π_tea(·|s))]
- Token 级内在奖励：r_t^{OPD} = -(log π_θ(a_t|s_t) - log π_tea(a_t|s_t))
- 计算梯度时对学生的 log-probability 项使用 stop_gradient

### 关键设计选择：Reverse-KL 的理论分析

三种对齐目标的对比：
- **Forward-KL (D_KL(π_tea || π_θ))**：mode-covering，在 OOD 状态强迫学生覆盖教师全部支撑集 → 模仿教师的不确定性 → 熵爆炸
- **Hard-CE (argmax matching)**：丢弃教师的软概率分布 → 在多峰决策边界处学生被迫刚性追踪 → 熵坍塌，丧失探索多样性
- **Reverse-KL (D_KL(π_θ || π_tea))**：mode-seeking，学生只需在教师可接受的概率质量内选择动作 → 有界熵 → 过滤教师尾部不确定性，保留有效模式内的随机性

### Group-Based Gradient Estimation

- 对每条指令采样 G 条轨迹 {τ_1, ..., τ_G}，策略梯度取组内平均
- 不使用 GRPO 的结果奖励归一化，直接使用 Reverse-KL reward 作为 advantage
- G=2 即可达到 80%+ 成功率，G=8 最优（~89%）

### 初始化策略

- LIBERO：1-traj SFT（每任务 1 条 demo）
- RoboTwin2.0：1000-traj SFT（每任务 1000 条 demo）
- 教师模型：SimpleVLA-RL（已通过 RL 训练的专家）


## Experiments

### 基准测试

**LIBERO（单臂操控，4 个任务套件）**

| 方法 | Spatial | Object | Goal | Long | Avg |
|------|---------|--------|------|------|-----|
| Teacher (SimpleVLA-RL) | 94.2 | 96.1 | 94.6 | 90.7 | 93.9 |
| OpenVLA-OFT (50-traj) | 84.7 | 88.4 | 79.2 | 53.7 | 76.5 |
| Nora (50-traj) | 92.2 | 95.4 | 89.4 | 74.6 | 87.9 |
| Student Init (1-traj) | 63.6 | 54.9 | 59.6 | 17.3 | 48.9 |
| VLA-OPD Distill (1-traj) | 84.3 | 93.8 | 92.5 | 78.9 | 87.4 |
| VLA-OPD Distill+GRPO (1-traj) | 93.4 | 95.3 | 94.5 | 90.2 | 93.4 |

- VLA-OPD (Distill) 用 1-traj 即超越多数 50-traj 方法
- VLA-OPD (Distill+GRPO) 几乎恢复教师性能（93.4% vs 93.9%）

**RoboTwin2.0（双臂协作，4 个任务）**

| 方法 | Pick Dual Bottles | Place Empty Cup | Handover Block | Stack Bowls | Avg |
|------|-------------------|-----------------|----------------|-------------|-----|
| Teacher | 68.3 | 94.2 | 57.8 | 75.8 | 74.0 |
| π_0 | 50.0 | 60.0 | 39.0 | 53.0 | 50.5 |
| RDT | 18.0 | 42.0 | 26.0 | 42.0 | 32.0 |
| Student Init | 29.7 | 77.3 | 33.1 | 40.6 | 45.2 |
| VLA-OPD Distill | 66.4 | 90.6 | 52.3 | 75.0 | 71.1 |

- 双臂场景下 Distill 即从 45.2% 提升至 71.1%，接近教师 74.0%

### 训练效率

- LIBERO-Object：~10 步达到 90%+，对比 GRPO 的渐进上升
- LIBERO-Long：50 步达到 ~80%，GRPO 需 150+ 步，**3× 加速**
- 训练曲线平滑，无 GRPO 的剧烈波动

### 灾难性遗忘分析

- Seen-Unseen trade-off 实验：在目标任务上微调，评估 4 个 held-out 任务
- Offline SFT：seen 性能提升时 unseen 性能急剧下降（接近零）
- VLA-OPD/RL：on-policy 方法几乎无遗忘，unseen 性能保持稳定
- VLA-OPD 在多数轴上优于或持平 RL

### 消融实验

**对齐目标消融**（RoboTwin2.0 Beat Block Hammer）：
- Reverse-KL：稳定上升，最高成功率
- Forward-KL：早期性能下降超 50%（性能低谷），熵爆炸
- Hard-CE：最终停滞在最低成功率，熵坍塌

**Group Size 消融**（LIBERO-Object, batch=32）：
- G=8：最平滑，最终 ~89%
- G=4：竞争力强
- G=2：仍达 80%+，证明小 group size 仍有足够信噪比


## Limitations

1. **依赖教师模型**：框架需要一个已训练好的专家教师（本工作中使用 SimpleVLA-RL），教师质量直接影响蒸馏上限
2. **未在真实机器人上验证**：仅在仿真基准 LIBERO 和 RoboTwin2.0 上评估，缺少 Sim-to-Real 验证
3. **教师推理开销**：每个学生状态都需要教师推理获取 action logits，计算开销显著
4. **教师-学生形态匹配假设**：论文未讨论教师和学生使用不同机器人形态时的适用性
5. **论文声明未来工作**将减少对特定教师模型的依赖，说明当前这是一个已知局限


## Key Takeaways

1. **Reverse-KL 作为蒸馏目标的洞见**：在 VLA on-policy 场景中，Reverse-KL 的 mode-seeking 特性是关键创新，可直接应用于其他需要 policy distillation 的机器人学习任务
2. **On-policy + Dense supervision 的组合**：将 SFT 的密集监督与 RL 的 on-policy 探索结合是一个通用范式，不限于 VLA 模型
3. **灾难性遗忘的缓解机制**：on-policy 数据使模型保持在安全的分布邻域内，这一思路对持续学习（continual learning）场景有参考价值
4. **与 DLO 操控的潜在关联**：VLA-OPD 的 on-policy 纠错机制对处理 DLO 操控中的复合误差有启发意义，尤其是教师在 OOD 状态上提供恢复行为的思路
5. **数据效率**：1-traj 初始化即可超越 50-traj SFT 方法，对数据稀缺场景极具价值

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhong|Zhong, Zhide]]
