---
title: "RankQ: Offline-to-online reinforcement learning via self-supervised action ranking"
tags: [VLM, RL, sim-to-real, robot-learning]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "RankQ 通过自监督多排序损失在离线-在线 RL 中对动作施加结构化排序（成功 > 噪声 > 随机），取代 CQL/Cal-QL 的均匀 OOD 惩罚，在 D4RL 稀疏奖励基准和 VLA 仿真-真实迁移（堆叠方块 43.1%→84.7%）上全面超越七种基线。"
authors: "Choi, Andrew; Xu, Wei"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "HN5VQGU4"
---
## 摘要

Offline-to-online reinforcement learning（强化学习） (RL) improves sample efficiency by leveraging pre-collected datasets prior to online interaction. A key challenge, however, is learning an accurate critic in large state--action spaces with limited dataset coverage. To mitigate harmful updates from value overestimation, prior methods impose pessimism by down-weighting out-of-distribution (OOD) actions relative to dataset actions. While effective, this essentially acts as a behavior cloning anchor and can hinder downstream online policy improvement when dataset actions are suboptimal. We propose RankQ, an offline-to-online Q-learning objective that augments temporal-difference learning with a self-supervised（自监督） multi-term ranking loss to enforce structured action ordering. By learning relative action preferences rather than uniformly penalizing unseen actions, RankQ shapes the Q-function such that action gradients are directed toward higher-quality behaviors. Across sparse reward（奖励） D4RL benchmarks, RankQ achieves performance competitive with or superior to seven prior methods. In vision-based robot learning, RankQ enables effective offline-to-online fine-tuning of a pretrained vision-language-action (VLA) model in a low-data regime, achieving on average a 42.7% higher simulation success rate than the next best method. In a high-data setting, RankQ improves simulation performance by 13.7% over the next best method and achieves strong sim-to-real（仿真到真实迁移） transfer, increasing real-world cube stacking success from 43.1% to 84.7% relative to the VLA's initial performance.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 视觉-语言模型、强化学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **D4RL 稀疏奖励基准全面竞争力**：在 4 个 antmaze + 3 个 adroit 环境上，RankQ 在所有环境中达到与七种基线方法持平或更优的性能，尤其在最困难的 antmaze-large 和 adroit-relocate 上显著领先。
2. **VLA 低数据量 regime 下的唯一有效方法**：仅 200 条 self-rollout + 每次 8 条在线 rollout，RankQ 是唯一能显著超越模仿学习基线的方法，平均成功率比次优方法高 42.7%（三项任务分别 +9.5%、+64.3%、+54.2%）。
3. **VLA 高数据量 regime + Sim-to-Real 验证**：800 条 rollout + 大规模 domain randomization 下，成功率比次优高 13.7%，执行速度快 25.7%；真实机器人堆叠成功率从 43.1% 提升到 84.7%（144 次试验），部分成功率从 77.8% 到 98.6%。
4. **系统性 Q-landscape 分析**：通过消融实验、∂Q/∂a 统计和 critic 准确率比较，证明 RankQ 的 Q 值景观梯度更稳定、在线迁移时分布漂移更小、动作排序准确率更高。
## 结构化提取

- **Problem**: 离线-在线 RL 中，现有悲观主义方法（CQL、Cal-QL）将所有 OOD 动作统一惩罚为次优，当离线数据集包含大量失败轨迹时阻碍在线策略改进
- **Method**: RankQ — 自监督多排序 Q-learning 目标，将数据集划分为成功/失败轨迹，构造 4 类次优动作（噪声、高噪声、随机、置换），通过 pairwise ranking loss 施加结构化动作排序
- **Tasks**: 迷宫导航（antmaze）、灵巧手操控（adroit pen/door/relocate）、桌面操控（carrot-onto-plate、cube-stacking、spoon-into-bowl）
- **Sensors**: RGB 相机（外挂静态相机）+ 语言指令（VLA 场景）；状态向量（D4RL 场景）
- **Robot Setup**: WidowX 250S 7-DOF 操控器（VLA），8-DOF ant 仿真体（antmaze），24-DOF 灵巧手（adroit）
- **Metrics**: 成功率（SR）、部分成功率（PSR）、平均完成时间（TTF）、轨迹长度
- **Limitations**: 仅稀疏奖励；VLA backbone 冻结；单一机器人平台；依赖欧氏距离定义动作相似性；需 trajectory-level 成功/失败标注
- **Evidence Notes**: 全文及附录 A-I 可用，包含完整 D4RL 数据表（3 seeds）、消融实验、Q-landscape 统计图、critic 准确率比较、sim-to-real 案例图。核心结果均有量化数据支撑。
## 本地引用关系

- [[choi2026rankq]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete (正文 + 附录 A-I，含 D4RL 详细数据表、消融、Q-landscape 分析、sim-to-real 案例图)
- Confidence: high
- Summary: RankQ 通过自监督多排序损失在离线-在线 RL 中对动作施加结构化排序（成功 > 噪声 > 随机），取代 CQL/Cal-QL 的均匀 OOD 惩罚，在 D4RL 稀疏奖励基准和 VLA 仿真-真实迁移（堆叠方块 43.1%→84.7%）上全面超越七种基线。


## Problem

离线-在线 RL（offline-to-online RL）面临的核心问题：在大状态-动作空间中，离线数据集覆盖有限导致 critic 估计不准确。现有方法（CQL、Cal-QL）通过对 OOD 动作施加悲观（pessimism）来抑制过高估计，但本质上是将策略锚定到数据集动作——当数据集动作本身是次优的（尤其是失败轨迹占多数时），这种均匀惩罚会阻碍在线策略改进。关键问题是：如何在数据集之外塑造价值函数，使其梯度指向更高质量的动作区域，而非简单地"惩罚所有未知动作"？


## Method

### 核心思想

RankQ 用**自监督多排序损失**（self-supervised multi-term ranking loss）替代 CQL/Cal-QL 的均匀 OOD 惩罚。核心区别：不把所有未见动作统一标记为"坏"，而是构造**结构化的动作质量层级**，让 Q 函数的梯度指向更高质量的动作区域。

### 技术细节

**数据集划分**：将离线数据集 D 划分为 D_success（成功轨迹）和 D_failure（失败轨迹）。

**构造次优动作**（仅对 D_success 中的 transition (s, a)）：
- **噪声动作** a_ε = a + ε，ε ~ N(0, σ)，小幅扰动
- **高噪声动作** a_{2ε} = a + 2ε，较大扰动
- **随机动作** a_r ~ U(-1, 1)^{|a|}，任意动作
- **置换动作** a_p ~ D，从无关状态采样的动作

**排序约束**（三组）：
1. Eq. 4 — 成功动作优于所有次优变体：Q(s,a) > Q(s,a')，a' ∈ {a_ε, a_{2ε}, a_r, a_p}
2. Eq. 5 — 次优动作之间的链式排序：Q(s,a_ε) > Q(s,a_{2ε}) > Q(s,a_r)
3. Eq. 6 — 失败动作仍优于随机动作：Q(s,a) > Q(s,a_r)，(s,a) ~ D_failure

**损失函数**：使用 softplus 的 pairwise ranking function R(s, a⁺, a⁻) = sp(Q_θ(s, a⁻) - Q_θ(s, a⁺))，最终目标为 α_0·L^succ_Q + L^neg_Q + α_1·L^fail_Q + L^TD_Q。默认 α_0 = α_1 = 1, σ = 0.15。

### VLA 集成

- VLA 模型：π₀（flow-matching action head + VLM backbone），预训练于 BridgeV2
- RL 算法：SACFlow（SAC + flow matching），仅微调 action head v_θ，冻结 VLM backbone E_θ
- 动作表示：action chunk A ∈ R^{C×7}，C=4，5 Hz 控制
- RankQ 仅需 4 次 critic 评估（4 类次优动作），而 CQL/Cal-QL 需 20 次（10 策略采样 + 10 随机采样），训练速度快约 2.8×
- 仅使用单步积分（K=1），推理延迟降低 2×

### 与 CQL/Cal-QL 的本质区别

| 方面 | CQL | Cal-QL | RankQ |
|------|-----|--------|-------|
| OOD 处理 | 均匀惩罚策略动作 | 有下界的惩罚 | 结构化动作排序 |
| 梯度方向 | ∂Q/∂a 指向数据集动作（含失败） | 同 CQL，但幅度受控 | ∂Q/∂a 指向高质量动作区域 |
| 悲观主义 | 无界 → 梯度爆炸 | 有下界 → 梯度可控 | 无悲观主义 → 梯度稳定 |
| 数据假设 | 数据集动作优于策略动作 | 同 CQL | 成功动作 > 噪声动作 > 随机动作 |


## Experiments

### 数据集与环境

**D4RL 基准**：
- antmaze-medium-play/diverse, antmaze-large-play/diverse（8 DOF ant 迷宫导航）
- adroit-pen/door/relocate（24 DOF 灵巧手操控）
- 稀疏奖励，基于 SAC + MLP

**VLA 低数据量**：
- 200 条 self-rollout（约 40 条成功），每次更新 8 条在线 rollout
- WidowX 7-DOF 操控器，3 项任务：carrot-onto-plate、cube-stacking、spoon-into-bowl
- 初始成功率：carrot 73.5%, cube 24%, spoon 20.5%
- 单一 EmbodiedGen 场景 + 物体位置/yaw 随机化

**VLA 高数据量 Sim-to-Real**：
- 800 条 self-rollout（仅约 64 条成功，~8% 初始成功率），每次更新 192 条在线 rollout
- 100 个 EmbodiedGen 场景 + 全面 domain randomization（物体位置、机器人姿态、相机位置、光照）
- ManiSkill 3 仿真框架

**Sim-to-Real**：
- WidowX 250S 7-DOF 操控器
- 外挂 Logitech C922 摄像头
- NVIDIA RTX 4090 推理
- 3×3 网格 → 72 种方块配置，每策略 72 次试验，共 144 次真实世界试验

### 主要结果

**D4RL（在线微调后成功率）**：
| 环境 | 最佳基线 | RankQ |
|------|---------|-------|
| antmaze-medium-play | 0.989 (Cal-QL+SAC) | 0.977 |
| antmaze-medium-diverse | 0.983 (CQL+SAC) | 0.962 |
| antmaze-large-play | 0.828 (CQL) | **0.912** |
| antmaze-large-diverse | 0.740 (Cal-QL) | **0.847** |
| adroit-pen | 0.987 (Cal-QL) | 0.969 |
| adroit-door | 0.991 (CQL+SAC) | **0.991** |
| adroit-relocate | 0.937 (Cal-QL) | **0.932** |

**VLA 低数据量（最终成功率）**：
| 任务 | 初始 | 次优基线 | RankQ |
|------|------|---------|-------|
| carrot-onto-plate | 0.735 | 0.835 (CQL+SAC) | **0.930** |
| cube-stacking | 0.240 | 0.260 (CQL) | **0.940** |
| spoon-into-bowl | 0.205 | 0.258 (CQL) | **0.800** |

**VLA 高数据量 Sim-to-Real（训练最终）**：
| 方法 | 成功率 | 完成时间 |
|------|--------|---------|
| CQL | 0.690 | 11.42s |
| Cal-QL | 0.743 | 10.51s |
| SAC+OFF | 0.128 | — |
| RankQ | **0.880** | **8.36s** |

**真实机器人结果（144 次试验）**：
| | PSR↑ | SR↑ | TTF(s)↓ |
|--|------|-----|---------|
| Baseline VLA | 0.778 | 0.431 | 14.81±6.00 |
| RankQ | **0.986** | **0.847** | **12.34±4.94** |

### 消融实验（附录 D）

在 D4RL 上测试三种消融：
1. σ=0.15→0.30：对简单任务无影响，对 antmaze-large-play 有轻微退化
2. 移除 permuted-action ranking (a_p)：对 adroit-door 有明显负面影响，对 antmaze-large-diverse 略有正面
3. 移除链式损失 L^neg_Q：对 antmaze-large-play 和 adroit-relocate 有负面影响

结论：默认配置在所有环境提供强基线性能，但最优配置可能因环境而异。

### Q-landscape 分析（附录 E）

- CQL 的 ∂Q/∂a 在离线训练阶段出现大幅尖峰（无界悲观主义导致），Cal-QL 尖峰较小（有校准下界）
- RankQ 的 ∂Q/∂a 统计量在整个训练过程中最稳定，离线→在线过渡时几乎无分布漂移
- CQL/Cal-QL 需要在线阶段"遗忘"离线期间学到的悲观偏置

### Critic 准确率（附录 F）

- RankQ 在排序"成功动作 > 四类次优动作"上准确率最高
- CQL/Cal-QL 对随机和高噪声动作准确率接近 RankQ，但对噪声和置换动作准确率较低
- 随训练推进，CQL/Cal-QL 逐渐接近 RankQ 的准确率，说明 RankQ 的排序目标与现有方法隐含学习目标一致，但样本效率更高


## Limitations

论文未明确声明局限性，但可从实验和设计推断：

1. **仅验证稀疏奖励**：所有实验均基于 sparse reward + rule-based success detection，未测试 dense reward 或 shaped reward 场景。
2. **VLA backbone 冻结**：仅微调 flow-matching action head，未探索 backbone 联合微调的效果。
3. **单一机器人平台**：Sim-to-Real 仅在 WidowX 250S 上验证，未测试双臂、移动操控等更复杂设置。
4. **动作空间假设**：排序构造依赖动作空间的欧氏距离（噪声 perturbation），对离散或混合动作空间的适用性未知。
5. **成功/失败划分依赖**：需要明确的 trajectory-level 成功/失败标注，对连续质量梯度（部分成功）的场景可能不够灵活。
6. **超参数敏感性**：虽然默认参数表现良好，但 antmaze 环境需要 α_0=20（因成功样本极度稀少），表明在极端不平衡场景下可能需要调参。
7. **比较范围有限**：D4RL 直接复用 Cal-QL 代码库，未包含 franka-kitchen 等环境；VLA 基线数量较少。


## Key Takeaways

1. **排序优于惩罚**：通过构造结构化的动作质量层级（而非均匀悲观），可以更有效地塑造 Q 值景观，使梯度自然指向高质量动作区域。这比 CQL/Cal-QL 的"所有 OOD 都不好"策略更符合学习信号的本质。
2. **低数据量 regime 的突破**：当数据集中 80% 是失败轨迹时，CQL/Cal-QL 的"数据集动作优于策略动作"假设完全失效，而 RankQ 能从稀疏成功和大量失败中提取有效学习信号。这对真实机器人 RL 极为重要——self-rollout 场景下初始成功率往往很低。
3. **VLA RL 微调的工程启示**：冻结 backbone + 仅微调 action head + 单步积分推理的方案，在保持 VLM 感知能力的同时实现了高效的 RL 微调。RankQ 的 4 次 critic 评估 vs CQL/Cal-QL 的 20 次，使得实际训练效率提升 2.8×。
4. **Sim-to-Real 的完整链路**：EmbodiedGen 生成随机化场景 → ManiSkill 3 仿真 → 大规模 domain randomization → RankQ 训练 → 零样本迁移真实机器人，成功率翻倍。这条链路对我们的 Sim-to-Real 工作有直接参考价值。
5. **Q-landscape 可视化分析**：论文展示的 ∂Q/∂a 统计图和梯度流可视化方法（Fig. 1, Fig. E.3）是理解和诊断 RL 训练的有力工具。

## 相关概念

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[choi|Choi, Andrew]]
- [[xu-wei|Xu, Wei]]
