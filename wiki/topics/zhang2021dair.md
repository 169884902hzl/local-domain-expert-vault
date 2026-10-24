---
title: "DAIR: Disentangled attention intrinsic regularization for safe and efficient bimanual manipulation"
tags: [manipulation, RL, bimanual]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（interaction regions），解决双臂 RL 训练中的支配（domination）和冲突（conflict）问题。在 5 个双臂操控任务上验证，Domination Rate 降低 24%，Conflict Rate 降低约 50%，Finish Steps 减少。支持课程学习推广到 8 物体重排。"
authors: "Zhang, Minghao; Jian, Pingcheng; Wu, Yi; Xu, Huazhe; Wang, Xiaolong"
year: "2021"
venue: "arXiv Preprint"
zotero_key: "2JVS2J3V"
---
## 摘要

We address the problem of safely solving complex bimanual（双臂） robot manipulation（机器人操控） tasks with sparse rewards. Such challenging tasks can be decomposed into sub-tasks that are accomplishable by different robots concurrently or sequentially for better efficiency. While previous reinforcement learning（强化学习） approaches primarily focus on modeling the compositionality of sub-tasks, two fundamental issues are largely ignored particularly when learning cooperative strategies for two robots: (i) domination, i.e., one robot may try to solve a task by itself and leaves the other idle; (ii) conflict, i.e., one robot can interrupt another's workspace when executing different sub-tasks simultaneously, which leads to unsafe collisions. To tackle these two issues, we propose a novel technique called disentangled attention, which provides an intrinsic regularization for two robots to focus on separate sub-tasks and objects. We evaluate our method on five bimanual manipulation（双臂操控） tasks. Experimental results show that our proposed intrinsic regularization successfully avoids domination and reduces conflicts for the policies, which leads to significantly more efficient and safer cooperative strategies than all the baselines. Our project page with videos is at https://mehooz.github.io/bimanual-attention.

## 中文简述

提出基于强化学习的双臂方法。

**研究方向**: 机器人操控、强化学习、双臂操控

## 关键贡献

1. **识别双臂 RL 的支配和冲突问题**：明确指出并定义了双臂操控中的支配率、冲突率和完成步数三个评估准则。
2. **DAIR 正交注意力正则化**：通过最小化两臂注意力概率分布的点积（<α₁, α₂>²），鼓励不同臂关注不同交互区域。作为表征学习正则项，不修改奖励函数。
3. **注意力架构设计**：基于 Transformer 注意力机制，状态编码器共享参数，注意力嵌入作为残差连接。支持可变数量的交互区域和智能体。
4. **课程学习泛化**：训练 3 物体重排策略可泛化到 8 物体，Stack Tower 训练 2 块可泛化到 2 个塔。
## 结构化提取

- **Problem**: 双臂 RL 训练中的支配（一臂做所有子任务）和冲突（两臂碰撞）问题，现有方法忽略效率和安全性。稀疏奖励下协作探索困难。
- **Method**: DAIR（Disentangled Attention Intrinsic Regularization）：基于注意力的策略/Q 网络架构 + 正交注意力约束（最小化两臂注意力概率分布点积）。SAC + HER 训练，课程学习（1→3 物体）。
- **Tasks**: 5 个双臂操控任务（Rearrangement 1-8 物体、Stack Tower 1-3 物体、Open Box and Place、Push with Door、Adjust Bar）。MuJoCo 仿真 + 双 Fetch 机器人。
- **Sensors**: 仿真状态（关节角+速度+末端位置+交互区域位置/速度/姿态/目标）。无真实传感器。
- **Robot Setup**: 双臂 Fetch 机器人（MuJoCo），7-DOF + 夹爪。位置控制 + 夹爪控制。
- **Metrics**: Success Rate（50 episodes × 3 seeds）、Domination Rate（一臂操作占比，理想 50%）、Conflict Rate（两夹爪距离<阈值的步数占比）、Finish Steps（完成任务所需步数）。
- **Limitations**: 仅仿真无真实实验；交互区域手动定义；仅 SAC+HER；仅两臂；课程学习依赖；未处理 DLO/布料；稀疏奖励成功率中等。
- **Evidence Notes**: Domination/Conflict/Finish 有定量表格（Tab. 1-2, 5），3 seeds 均值±标准差。课程学习泛化有 Tab. 3-4，8 物体重排是强泛化证据。成功率为训练曲线（Fig. 3, 7），无最终收敛值表格。注意力可视化（Fig. 5）定性验证正交性。λ 消融（Fig. 4）验证鲁棒性。MLP/MADDPG 基线无法处理可变物体数（公平性讨论充分）。整体证据强度：中-强（定量表格 + 训练曲线，无真实实验）。
## 本地引用关系

- [[blancomulero2024benchmarking]]
- [[mitrano2024grasp]]
## 证据元数据

- **Zotero Key**: 2JVS2J3V
- **Citekey**: zhang2021dair
- **Authors**: Zhang Minghao, Jian Pingcheng, Wu Yi, Xu Huazhe, Wang Xiaolong
- **Affiliation**: Tsinghua University + UC San Diego + UC Berkeley + Shanghai Qi Zhi Institute
- **Venue**: arXiv preprint, 2021-10 (Under review)
- **Paper Type**: Methods paper (RL intrinsic regularization for bimanual manipulation)
- **Fulltext Quality**: Complete, 10 pages with figures, tables, and appendix
- **Evidence Coverage**: High for domination/conflict reduction (Tab. 1-2, Fig. 3); High for generalization (Tab. 3-4); Medium for synergistic behavior (Tab. 5, single task)
- **Confidence**: High on domination/conflict metrics (3 seeds, clear definitions); Medium on generalization to 8 objects (single task)
- **Summary**: 提出 DAIR（Disentangled Attention Intrinsic Regularization），通过正交注意力约束让双臂机器人关注不同的交互区域（interaction regions），解决双臂 RL 训练中的支配（domination）和冲突（conflict）问题。在 5 个双臂操控任务上验证，Domination Rate 降低 24%，Conflict Rate 降低约 50%，Finish Steps 减少。支持课程学习推广到 8 物体重排。


## Problem

双臂机器人 RL 训练中的两个关键问题：（1）支配（domination）：一个臂试图独自完成所有子任务，另一臂闲置；（2）冲突（conflict）：两臂同时操作同一区域导致不安全碰撞。现有 RL 方法关注子任务组合性，但忽略这两个效率和安全问题。稀疏奖励下鼓励协作探索也缺乏有效机制。


## Method

### 状态表示
- 状态 s = [s₁,...,s_N, s_{N+1},...,s_{N+M}]，前 N 个为机器人状态（关节角+速度+末端位置），后 M 个为交互区域状态（位置+速度+姿态+目标位置）
- 交互区域定义灵活：小物体 1 个区域，大物体（bar）2 个区域

### 网络架构（Fig. 2）
- 每个智能体 i 有独立的状态编码器 f_{i,j}(·)
- 注意力嵌入 v_i = Σ α_{i,j} f_{i,j}(s_j)
- α_{i,j} = softmax(β_{i,j})，β 基于缩放点积注意力
- 策略 π_{φ_i}(a_i|s) = h_i(f_{i,i}(s_i) + LayerNorm(g_i(v_i)))

### DAIR 正则化（Eq. 7）
- L_attn(φ_i) = Σ_{j≠i} <α_i, α_j>²
- 目标：最小化两臂注意力分布的点积 → 正交 → 关注不同区域
- 联合训练：min J_π(φ_i) + λL_attn(φ_i)，λ=0.05
- 同时应用于 Policy 和 Q-function 网络

### 训练
- SAC + HER（future-replace, k=4）
- Adam lr=0.0001, γ=0.98, buffer 1M, batch 512
- 3 seeds，课程学习：1 → 2 → 3 物体


## Experiments

### 子任务分配（Tab. 1, Fig. 3）
- Open Box and Place：DAIR Domination 53.4% vs Attention 77.2%，Conflict 4.0% vs 7.4%
- Push with Door（sparse）：DAIR Conflict 18.7% vs Attention 44.1%
- 稀疏奖励下 DAIR 效果优于 informative reward（更灵活的协作空间）

### 课程学习泛化（Tab. 3-4）
- Stack Tower：3 物体 DAIR 68.3% vs Attention 42.0%；2→4(two towers) DAIR 17.5% vs 0%
- Rearrangement：3 物体 DAIR 89.0% vs Attention 66.7%；3→8 DAIR 33.3% vs 0%

### 冲突惩罚消融（Tab. 2）
- 即使加 collision penalty（-1.0），DAIR 仍持续降低冲突率

### 协同行为（Tab. 5, Fig. 7）
- Adjust Bar：DAIR 仍保持学习效率，Domination 52.6% vs 56.1%，Finish Steps 18.2 vs 23.5

### λ 敏感性（Fig. 4）
- λ 从 0.02 到 0.2 均有效，方法鲁棒


## Limitations

1. **仅仿真验证**：MuJoCo 仿真 + Fetch 机器人，无真实世界实验。
2. **交互区域需手动定义**：每个任务需手动指定交互区域（物体位置/大物体端点），无法从感知自动提取。
3. **仅 SAC + HER**：未验证与其他 RL 算法（PPO、TD3）的兼容性。
4. **仅两臂场景**：虽声称可推广到多智能体，但实验仅 N=2。
5. **课程学习依赖**：多物体任务需要渐进式训练（1→2→3），直接训练 3 物体难以成功。
6. **稀疏奖励成功率中等**：Open Box 稀疏奖励下成功率未报告精确数值（仅曲线），Push with Door 稀疏奖励曲线收敛较慢。
7. **未处理 DLO 或布料**：仅刚体物体（方块、门、cover、bar），未涉及可变形物体。


## Key Takeaways

1. **正交注意力是双臂协作的有效归纳偏置**：鼓励两臂关注不同区域自然解决了支配和冲突问题，无需设计复杂的奖励函数。这一思路可迁移到其他多臂/多智能体协作场景。
2. **与 [[mitrano2024grasp]]（GL-signature）互补**：GL-signature 提供拓扑约束指导重抓取规划（运动规划层），DAIR 提供注意力正则化避免双臂冲突（RL 训练层）。两者结合：拓扑约束过滤不可行抓取 + 注意力正则化鼓励分工。
3. **对本研究方向的启示**：双臂 DLO 操控的 RL 训练中，可将 DLO 的不同段/关键点定义为交互区域，用 DAIR 鼓励一臂操作 DLO 的一端、另一臂操作另一端或辅助物体，避免两臂争抢同一抓取点。
4. **课程学习 + 注意力架构支持可变输入**：可处理不同数量的交互区域，这对 DLO 操控（关键点数量可变）有直接参考价值。

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zhang-minghao|Zhang, Minghao]]
