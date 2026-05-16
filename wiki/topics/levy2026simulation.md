---
title: "Simulation distillation: Pretraining world models in simulation for rapid real-world adaptation"
tags: [manipulation, RL, sim-to-real, physics-simulation, planning]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟真实数据实现显著性能提升。"
authors: "Levy, Jacob; Westenbroek, Tyler; Huang, Kevin; Palafox, Fernando; Yin, Patrick et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "43NAHKTR"
---
## 摘要

Simulation-to-real transfer remains a central challenge in robotics, as mismatches between simulated and real-world dynamics often lead to failures. While reinforcement learning（强化学习） offers a principled mechanism for adaptation, existing sim-to-real（仿真到真实迁移） finetuning methods struggle with exploration and long-horizon（长时序） credit assignment in the low-data regimes typical of real-world robotics. We introduce Simulation Distillation (SimDist), a sim-to-real（仿真到真实迁移） framework that distills structural priors from a simulator into a latent world model and enables rapid real-world adaptation via online planning and supervised dynamics finetuning. By transferring reward（奖励） and value models directly from simulation, SimDist provides dense planning signals from raw perception without requiring value learning during deployment. As a result, real-world adaptation reduces to short-horizon system identification, avoiding long-horizon（长时序） credit assignment and enabling fast, stable improvement. Across precise manipulation（操控） and quadruped locomotion tasks, SimDist substantially outperforms prior methods in data efficiency, stability, and final performance. Project website and code: https://sim-dist.github.io/

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、仿真到真实迁移、物理仿真、运动规划

## 关键贡献

1. 提出 SimDist 框架——基于世界模型的 Sim-to-Real 范式，将真世界适应简化为隐动力学监督学习问题，避免长时序 credit assignment
2. 在 2 个精密装配操控任务（Peg Insertion、Table Leg）和 2 个四足运动任务（Slippery Slope、Foam）上验证，仅用 15-30 分钟真世界数据即可持续自主改进
3. 证明仿真中训练的奖励和价值模型可从原始感知零样本迁移到真世界，可作为规划信号直接使用
## 结构化提取

- Problem: Sim-to-Real 迁移中端到端策略微调的低数据量不稳定性——如何保留仿真全局先验同时高效适应真世界动力学
- Method: Simulation Distillation (SimDist)——仿真中用 teacher-student 蒸馏训练完整世界模型（编码器 + 动力学 + 奖励 + 价值），真世界冻结除动力学外所有模块，MPPI 在线规划
- Tasks: Peg Insertion（方柱插入）、Table Leg（桌腿螺纹旋入）、Slippery Slope（低摩擦斜面穿越）、Foam（柔性海绵穿越）
- Sensors: 3× RGB 相机 224×224（操控）、本体感知 + 地形高度图 21×15（四足）
- Robot Setup: UR5e（操控，6D 末端执行器控制，5Hz）、Unitree Go2（四足，12 关节位置控制，50Hz）
- Metrics: Success Rate（操控/四足）、Forward Progress（四足）、Accumulated Reward（仿真消融）
- Limitations: 依赖高保真仿真器；单任务设定；dense reward 需仿真器特权状态；未涉及柔性物体；数据量需求大；控制频率受限
- Evidence Notes: 全文 arXiv HTML 可用，涵盖完整方法描述（Section III-IV）、4 个真世界任务实验（Section V）、消融实验（Table I）、四足详细结果（Table IX）。缺失：代码未开源（承诺 release）、操控任务的逐时间步成功曲线仅有汇总图、四足地形参数化具体实现细节
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 完整获取)
- Evidence Coverage: 高 — 涵盖方法细节、实验结果、消融实验、附录参数
- Confidence: high
- Summary: 提出 SimDist 框架，将仿真器中的世界模型结构先验蒸馏到隐空间，真世界适应仅需监督式微调隐动力学模型，冻结编码器/奖励/价值函数，在操控和四足任务上用 15-30 分钟真实数据实现显著性能提升。


## Problem

Sim-to-Real 迁移中，端到端策略微调在低数据量场景下容易遭遇灾难性遗忘，根本原因在于策略将任务表示、奖励和动力学紧密耦合，迁移到新域时被迫重新学习全部任务结构。如何在保留仿真中学到的全局任务结构的同时，高效适应真实环境的局部动力学差异？


## Method

### 核心思路
利用世界模型的模块化结构（编码器、动力学、奖励、价值函数），将"全局任务结构"与"局部动力学"分离：
- 全局结构（物体位置、语义角色、到目标距离）在 sim 和 real 间大致不变
- 局部动力学（接触力、摩擦、形变）在域间差异显著

### 框架流程
1. **仿真预训练**：
   - 用 PPO 训练 state-based 专家策略 πᵉ 及其价值函数 Vᵉ，保存训练中间检查点
   - 通过专家策略、中间检查点策略和随机动作扰动混合生成多样化数据集 D_sim（包含失败和恢复行为）
   - 在 D_sim 上预训练完整世界模型：编码器 E_θ → 隐状态 z_t、历史编码器 C_θ、隐动力学 f_θ、奖励模型 R_θ、价值模型 V_θ、基础策略 π_θ

2. **真世界适应**：
   - **冻结**：E_θ、C_θ、R_θ、V_θ、π_θ
   - **仅微调**：隐动力学 f_θ
   - 损失函数退化为纯 latent dynamics L2 loss
   - 迭代收集 on-policy 轨迹 → 更新动力学 → 改善规划

3. **在线规划**：MPPI (Model Predictive Path Integral) 采样候选动作序列，用世界模型评估回报并重要性加权

### 关键架构决策
- **Chunked Prediction**：动力学模型用 transformer 一次前向传播预测 T 步未来状态，而非自回归展开，充分利用 GPU 并行
- **Sequence-to-Sequence 奖励/价值建模**：transformer 聚合整个轨迹的隐状态信息，比逐帧 MLP 更准确估计回报
- **Minimal History**：历史编码器只处理本体感知（低维）+ 最近一帧外部感知（图像），降低推理延迟
- **Teacher-Student 蒸馏**：利用仿真器的特权信息（精确状态、最优价值函数）生成大规模密集监督


## Experiments

### 操控实验（UR5e）
- **设置**：6D 末端执行器位姿目标，3 个 224×224 RGB 相机（腕部、俯视、侧视），ResNet-18 编码，隐状态维度 64
- **训练数据**：100K 仿真轨迹，约 36% 为专家数据
- **任务**：
  - Peg Insertion：16mm 方柱插入（Narrow 2×2 / Wide 35×35 初始位置）
  - Table Leg：桌腿螺纹对准旋入（Narrow / Wide）
- **对比方法**：RLPD、IQL、SGFT-SAC、Diffusion Policy、π₀.₅
- **关键结果**：SimDist 成功率约为最佳基线的 2 倍；标准 RL 微调频繁出现灾难性遗忘；SGFT 避免了灾难性崩溃但样本效率远低于 SimDist

### 四足实验（Unitree Go2）
- **设置**：12 关节位置目标，本体感知 + 地形高度图（CNN 编码），控制频率 50Hz，RTX 4090M 笔记本
- **训练数据**：100M 仿真数据点，55.7% 专家数据
- **任务**：
  - Slippery Slope：PTFE 覆盖斜面，极低摩擦，1.82m 穿越
  - Foam：5cm 记忆海绵垫，未建模柔性动力学，3.00m 穿越
- **关键结果**：
  - Slippery Slope 0.3 m/s：SimDist 5/5 成功，IQL 0/5，RLPD 0/5
  - Foam 1.2 m/s：SimDist 5/5，IQL 3/5，RLPD 不稳定未报告
  - 真世界数据：32.1 min (Foam) / 35.7 min (Slippery Slope)

### 消融实验（仿真评估）
| 变体 | Peg Insertion | Table Leg | Quadruped |
|------|:---:|:---:|:---:|
| SimDist (完整) | 0.90 | 0.85 | 22.78 |
| 50% 数据量 | 0.72 | 0.61 | 22.73 |
| 10% 数据量 | 0.06 | 0.02 | 19.38 |
| 仅专家数据 | 0.10 | 0.05 | 16.68 |
| MLP 奖励/价值 | 0.82 | 0.60 | 19.47 |
| 加重建损失 | 0.32 | 0.21 | 23.34 |

- 数据多样性和规模对操控任务至关重要（10% 数据 → 接近失败）
- 仅专家数据严重退化（缺失败行为覆盖）
- MLP 替换 transformer 奖励/价值模型一致性能下降
- 重建损失对操控严重负面影响（-0.58/-0.64），对四足微弱正面

### 真世界动力学分析
- 预训练模型平均 latent loss：0.076 → 微调后：0.019
- 微调前：错误预测 PTFE 表面稳定接触，无法预测滑移
- 微调后：准确预测未来滑移，规划轨迹反映真实接触动力学


## Limitations

1. **依赖高保真仿真器**：需要与真实环境结构相近的仿真器（物理几何正确），且需要能训练 state-based 专家策略
2. **单任务设定**：每个任务单独训练世界模型，未验证多任务通用性
3. **奖励函数需要仿真器精确状态**：dense reward 从仿真器特权状态计算，真世界无法直接获取
4. **仅验证刚性物体操控**：未涉及 DLO、柔性物体等复杂接触场景
5. **仿真数据量大**：操控 100K 轨迹 / 四足 100M 数据点，数据生成和预训练成本不低
6. **控制频率限制**：操控 5Hz，四足 50Hz，高频动态可能不适用


## Key Takeaways

### 对 DLO 操控的启示
- **世界模型模块化思路可用于 DLO**：DLO 的全局结构（形状表示、目标构型）和局部动力学（形变、摩擦）同样可分离
- **冻结奖励/价值 + 仅微调动力学**的策略在 DLO 场景下可能有效——DLO 形变动力学的 sim-to-real gap 比刚性物体更严重，更需要高效适应
- **数据多样性（包含失败和恢复行为）是关键**：DLO 操控中失败模式丰富，这一发现尤其相关
- **重建损失对视觉操控有害**：DLO 高维视觉观测中更应注意避免重建损失的干扰

### 对 VLM-based 控制的启示
- SimDist 的编码器从原始感知学习隐表示，与 VLM 的视觉编码有互补性
- 未来方向：用 VLM 替换 ResNet 编码器，利用语言引导的语义表示增强世界模型

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[planning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[levy|Levy, Jacob]]
- [[westenbroek|Westenbroek, Tyler]]
