---
title: "Slot-MPC: Goal-conditioned model predictive control with object-centric representations"
tags: [manipulation, imitation, RL, planning]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出Slot-MPC，将基于Slot Attention的对象中心表征（SAVi）与可微分世界模型（cOCVP）结合，通过梯度优化MPC在紧凑的对象级隐空间中进行目标条件规划，在仿真操控任务上以99%更低的隐空间维度实现比DINO-WM快300倍的规划速度。"
authors: "Spieler, Jonathan; Villar-Corrales, Angel; Behnke, Sven"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QR57VIR9"
---
## 摘要

Predictive world models enable agents to model scene dynamics and reason about the consequences of their actions. Inspired by human perception, object-centric world models capture scene dynamics using object-level representations, which can be used for downstream applications such as action planning. However, most object-centric world models and reinforcement learning（强化学习） (RL) approaches learn reactive policies that are fixed at inference time, limiting generalization to novel situations. We propose Slot-MPC, an object-centric world modeling framework that enables planning through Model Predictive Control (MPC). Slot-MPC leverages vision encoders to learn slot-based representations, which encode individual objects in the scene, and uses these structured representations to learn an action-conditioned object-centric dynamics model. At inference time, the learned dynamics model enables action planning via MPC, allowing agents to adapt to previously unseen situations. Since the learned world model is differentiable, we can use gradient-based MPC to directly optimize actions, which is computationally more efficient than relying on gradient-free, sampling-based MPC methods. Experiments on simulated robotic manipulation（机器人操控） tasks show that Slot-MPC improves both task performance and planning efficiency compared to non-object-centric world model baselines. In the considered offline setting with limited state-action coverage, we find that gradient-based MPC performs better than gradient-free, sampling-based MPC. Our results demonstrate that explicitly structured, object-centric representations provide a strong inductive bias for controllable and generalizable decision-making. Code and additional results are available at https://slot-mpc.github.io.

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、强化学习、运动规划

## 关键贡献

1. **Slot-MPC框架**：首个将基于Slot Attention的对象中心隐动力学模型与梯度优化MPC结合的方法，从纯视觉输入进行目标条件规划，无需奖励信号。
2. **高效隐空间规划**：Slot-based表征将隐空间维度降低约99%（4×128 vs DINO-WM的196×384），使单步规划时间从~145s降至~0.4s。
3. **梯度MPC优于采样MPC**：在离线有限数据条件下，梯度优化MPC显著优于MPPI（如Button Press 0.64 vs 0.04），因为梯度优化更贴近训练分布。
## 结构化提取

- Problem: 离线、无奖励、有限数据条件下，如何实现高效且可泛化的目标条件视觉机器人操控规划。现有反应式策略泛化性差，采样MPC计算代价高。
- Method: Slot-MPC = SAVi（Slot Attention场景分解）+ cOCVP（Transformer动作条件对象中心动力学预测）+ 梯度优化MPC（Hungarian匹配 + L2 slot距离目标）。策略网络通过行为克隆从少量专家demo学习，为MPC提供初始动作序列。
- Tasks: 按钮按压、杠杆拉动、方块堆叠、螺母套杆——均为仿真机器人操控
- Sensors: 仅单目RGB相机（64×64像素）
- Robot Setup: Meta-World Sawyer机械臂（4DoF控制）/ robosuite Panda机械臂（7DoF OSC_POSE末端控制）
- Metrics: 任务成功率（50 episode，Wilson 95% CI）；辅助指标：PSNR/SSIM/LPIPS图像预测质量、单步规划时间
- Limitations: 依赖目标图像（不支持语言目标）、依赖ground truth actions、未在真实机器人验证、对象分解质量制约性能、缺乏subgoal机制
- Evidence Notes: 完整episode评估中Slot-MPC在4个任务上成功率22%-64%，Dreamer-v3需在线交互1M-5M步才能达到类似/更差结果。DINO-WM全面失败（0%）。消融证明策略先验和梯度MPC最关键——无策略先验时复杂任务0%成功率，MPPI替代梯度MPC也导致接近0%。规划速度比DINO-WM快约300倍（0.42-0.48s vs 144-145s）。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（正文、附录、所有表格和消融实验均已覆盖）
- Confidence: high
- Summary: 提出Slot-MPC，将基于Slot Attention的对象中心表征（SAVi）与可微分世界模型（cOCVP）结合，通过梯度优化MPC在紧凑的对象级隐空间中进行目标条件规划，在仿真操控任务上以99%更低的隐空间维度实现比DINO-WM快300倍的规划速度。


## Problem

现有多数对象中心世界模型和RL方法学习的是推理时固定的反应式策略，泛化到新场景的能力有限。同时，基于采样的MPC（如CEM、MPPI）需要评估数百至数千条候选轨迹，计算代价高昂。在离线、无奖励信号的有限数据条件下，如何实现高效且可泛化的目标条件视觉规划仍是一个开放问题。


## Method

### 架构总览
Slot-MPC由三个核心模块组成：

1. **对象中心场景解析（SAVi）**：
   - 基于SAVi (Kipf et al., 2022)将每帧图像分解为N_S个slot（默认4个，128维）
   - 使用Slot Attention进行slot与图像特征的交叉注意力，slot之间竞争特征位置
   - 每个slot通过共享GRU + MLP独立更新
   - Spatial Broadcast Decoder将每个slot重建为物体图像+mask，加权求和得到重建帧
   - 训练：自监督图像重建损失 L_SAVi

2. **条件对象中心预测器（cOCVP）**：
   - 基于OCVP (Villar-Corrales et al., 2023)的Transformer架构
   - 将动作向量通过线性投影映射到与slot相同的embedding空间，逐时间步与slot相加
   - 自回归预测未来slot状态：Ŝ_{t+1} = cOCVP(S_1, f_a(a_1), ..., S_t, f_a(a_t))
   - 联合训练损失：图像预测损失 + slot对齐损失（与SAVi编码的真实slot对齐）
   - 4层Transformer，256维token，8个64维注意力头，FFN隐层1024

3. **策略网络（Policy Prior）**：
   - 通过行为克隆从少量专家示教中学习
   - Transformer架构，处理当前帧的slot + 可学习[ACT]token来回归动作
   - 用于为MPC提供初始动作序列，显著提升优化效率

### 规划流程
- **目标编码**：目标图像 → SAVi → 目标slots S_Goal
- **当前状态编码**：当前观测 → SAVi → 当前slots S_t
- **前向rollout**：cOCVP自回归预测H步后的slots Ŝ_{t+H}
- **MPC目标**：J_MPC = ||Ŝ_{t+H} - S_Goal||²（Hungarian匹配对齐后计算）
- **梯度优化**：a ← a - η∇J_MPC（单条轨迹梯度下降）
- **滚动时域**：每步执行优化后序列的第一个动作，然后重新规划

### 关键设计
- **Hungarian匹配**：slot顺序在不同时间步和预测-目标间不保证一致，需匹配后比较
- **离线训练**：所有模块从无奖励离线数据训练（随机探索数据 + 少量专家demo）
- **任务无关**：世界模型不依赖任务奖励，可跨任务复用


## Experiments

### 环境
| 环境 | 来源 | 任务 | 观测 | 动作维度 |
|------|------|------|------|----------|
| Button Press | Meta-World | 按随机位置的按钮 | 64×64 RGB | 4 |
| Lever Pull | Meta-World | 拉随机位置的杠杆 | 64×64 RGB | 4 |
| Stack | robosuite | 将两个方块叠放 | 64×64 RGB | 7 (Panda) |
| Square | robosuite (MimicGen) | 将方形螺母套到杆上 | 64×64 RGB | 7 (Panda) |

### 数据
- **随机探索数据**：Meta-World 9000条训练 / robosuite 9000条训练（用于训练SAVi和cOCVP）
- **专家demo**：Meta-World 200条 / robosuite 1800条（用于训练策略网络）
- 评估：50条episode，Wilson 95%置信区间

### 主要结果（Table 1，完整episode评估）
| 方法 | Button Press | Lever Pull | Stack | Square |
|------|-------------|-----------|-------|--------|
| **Slot-MPC** | **0.64** | 0.52 | **0.42** | **0.22** |
| DINO-WM | 0.00 | 0.00 | 0.00 | 0.00 |
| Dreamer-v3 | **0.64** | **0.56** | 0.30 | 0.00 |
| GC-BC | 0.54 | 0.10 | 0.30 | 0.00 |

- Slot-MPC在Meta-World匹配Dreamer-v3（尽管Dreamer-v3需要在线交互+奖励信号，1M-5M步），在robosuite全面超越
- DINO-WM在完整episode评估中完全失败（0%），因patch-based表征在大搜索空间下长时域规划崩溃
- Slot-MPC在DINO-WM原始短子轨迹评估协议下也大幅领先（Table 7: 0.80/0.86/0.38/0.18 vs 0.56/0.10/0.00/0.04）

### 消融实验（Table 3a）
| 变体 | Button Press | Lever Pull | Stack | Square |
|------|-------------|-----------|-------|--------|
| 完整Slot-MPC | **0.64** | **0.52** | **0.42** | **0.22** |
| w/o 对象中心表征 | 0.62 | 0.48 | 0.20 | 0.04 |
| w/o MPC | **0.64** | **0.52** | 0.36 | 0.18 |
| w/o 策略先验 | 0.32 | 0.18 | 0.00 | 0.00 |
| w/ MPPI（非梯度） | 0.04 | 0.04 | 0.00 | 0.00 |

关键发现：
- **策略先验最关键**：无策略先验时复杂任务（Stack/Square）完全失败
- **梯度MPC >> 采样MPC**：MPPI在离线设定下严重退化为接近0%
- **对象中心表征对复杂任务重要**：Stack从0.42→0.20，Square从0.22→0.04

### 计算效率（Table 4）
| 方法 | Meta-World | robosuite |
|------|-----------|-----------|
| **Slot-MPC** | **0.42±0.01s** | **0.48±0.02s** |
| Slot-MPC w/ MPPI | 4.22±0.06s | 5.19±0.03s |
| DINO-WM | 144.37±0.83s | 145.30±0.72s |

隐空间维度对比：4×128=512 vs DINO-WM 196×384=75,264（99%降低）

### MPC目标消融（Table 3b）
- Slot间SSE距离和余弦相似度效果最佳
- 使用slot mask的IoU较差（偏向背景和大物体）


## Limitations

1. **依赖目标图像**：不支持自然语言目标描述（作者提到TextOCVP作为未来方向）
2. **依赖真实动作标签**：训练动力学模型和策略需要ground truth actions
3. **分解质量依赖**：性能受限于对象中心分解模型的质量
4. **仅仿真验证**：未在真实机器人上验证Sim-to-Real迁移
5. **精细操作不足**：Meta-World上常接近目标但未完成最后一步（如未完全按下按钮）
6. **subgoal缺失**：缺乏子目标分解机制，可能限制超长时域任务


## Key Takeaways

1. **对象中心表征是高效规划的强归纳偏置**：通过将场景分解为少量slot，隐空间维度降低99%，使梯度优化MPC成为可能。这对DLO操控有启发——如果将DLO也作为独立slot建模，可能实现高效柔性物体规划。

2. **离线设定下梯度MPC显著优于采样MPC**：MPPI在分布外查询时性能崩溃（0.04→0.00），梯度优化因更贴近训练分布而更稳健。这挑战了社区中"采样MPC更鲁棒"的普遍认知。

3. **策略先验是长时域任务的瓶颈**：无策略先验时Stack和Square完全失败（0%），表明纯从目标图像进行长时域规划仍极其困难。对于DLO操控这类复杂任务，需要类似的引导机制。

4. **世界模型的预测精度≠任务完成**：DINO-WM的图像预测质量（PSNR/SSIM）不逊于Slot-MPC（Table 2），但任务成功率0%。说明patch-based表征的预测精度不能转化为有效的规划能力。

5. **任务无关世界模型的可行性**：从随机探索数据训练的世界模型可跨任务复用，只需少量专家demo学习策略先验。这降低了数据采集门槛。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[planning]]
- [[deformable-linear-object]]

## 相关研究者

- [[spieler|Spieler, Jonathan]]
- [[villar-corrales|Villar-Corrales, Angel]]
- [[behnke|Behnke, Sven]]
