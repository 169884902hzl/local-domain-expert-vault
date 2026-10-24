---
title: "Aligning Flow Map Policies with Optimal Q-Guidance"
tags: [manipulation, VLM, RL, diffusion, flow-matching]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12 个操控与运动任务上 IQM 成功率 0.91，较 MVP 提升 21.3%"
authors: "Ziakas, Christos; Russo, Alessandra; Bose, Avishek Joey"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "T8RZ3C7S"
---
## 摘要

Generative policies based on expressive model classes, such as diffusion（扩散） and flow matching, are well-suited to complex control problems with highly multimodal（多模态） action distributions. Their expressivity, however, comes at a significant inference cost: generating each action typically requires simulating many steps of the generative process, compounding latency across sequential decision-making rollouts. We introduce flow map policies, a novel class of generative policies designed for fast action generation by learning to take arbitrary-size jumps including one-step jumps-across the generative dynamics of existing flow-based policies. We instantiate flow map policies for offline-to-online reinforcement learning（强化学习） (RL) and formulate online adaptation as a trust-region optimization problem that improves the critic's Q-value while remaining close to the offline policy. We theoretically derive FLOW MAP Q-GUIDANCE (FMQ), a principled closed-form learning target that is optimal for adapting offline flow map policies under a critic-guided trust-region constraint. We further introduce Q-GUIDED BEAM SEARCH (QGBS), a stochastic flow-map sampler that combines renoising with beam search to enable iterative inference-time refinement. Across 12 challenging robotic manipulation（机器人操控） and locomotion tasks from OGBench and RoboMimic, FMQ achieves state-of-the-art（现有最优方法） performance in offline-to-online RL, outperforming the previous one-step policy MVP by a relative improvement of 21.3% on the average success rate.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、扩散模型、Flow Matching

## 关键贡献

1. **Flow Map Policies 框架**：将单步策略统一为 flow-based 生成策略的两时间跳算子（two-time jump operator），包含 Lagrangian、Eulerian、Progressive 三种自蒸馏目标，Mean Flow Policy 是 Eulerian 变体的特例
2. **FMQ（Flow Map Q-Guidance）**：形式化在线适配为 trust-region 优化问题，推导出解析最优闭式学习目标（Theorem 3.2），无需蒸馏网络或 best-of-N 启发式，引入不确定性感知自适应信任区域
3. **QGBS（Q-Guided Beam Search）**：推理时随机采样 + beam search 结合 Q-梯度投影的迭代精化算法，纯推理过程不影响训练速度
4. **实验验证**：12 个任务（OGBench + RoboMimic）上 IQM 0.91，较 MVP 提升 21.3%，在线适配速度提升 2.77×
## 结构化提取

- Problem: 生成策略推理延迟高 + 在线适配缺乏原理性方法（依赖启发式 best-of-N）
- Method: Flow Map Policy（单步跳跃生成策略）+ FMQ（trust-region 最优 Q-梯度引导）+ QGBS（推理时随机 beam search）
- Tasks: 12 个连续控制任务（机器人操控 + 运动导航），来自 OGBench 和 RoboMimic
- Sensors: 低维状态向量（关节角度、位置、速度等），无视觉传感器
- Robot Setup: 仿真环境（RoboMimic 的 Franka 机械臂、OGBench 的人形/蚂蚁运动体），无真实机器人
- Metrics: Success Rate（50 episodes 平均），IQM（5 seeds，95% stratified bootstrap CI），收敛速度比
- Limitations: 线性化 Q 近似、依赖 critic 质量、部分任务 QGBS 退化、未验证真实机器人和高维视觉输入
- Evidence Notes: 完整实验包含 12 个任务 × 5 seeds，主结果 Table 1、消融 Table 2-3、收敛分析 Fig.3-4，附录含完整算法伪代码（Algorithm 1-2）和成功轨迹可视化
## 本地引用关系

- [[ziakas2026aligning]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖 Introduction, Method (§3.1-3.4), Experiments (§4.1-4.3), Related Work, Conclusion, Appendix A-C
- Confidence: high
- Summary: 提出基于 flow map 的单步生成策略框架 FMQ，通过 trust-region 最优 Q-梯度对齐实现高效的 offline-to-online RL 适配，在 12 个操控与运动任务上 IQM 成功率 0.91，较 MVP 提升 21.3%


## Problem

基于扩散模型和 flow matching 的生成策略在多模态动作分布的复杂控制问题中表现优异，但存在两个核心问题：

1. **推理延迟高**：每次动作生成需要模拟 ODE 多步动力学，在序列决策中延迟累积
2. **在线适配困难**：现有单步策略（如 MVP）依赖启发式 best-of-N 采样来选择高 Q 值动作，计算开销大且无法保证局部最优


## Method

### 核心架构

**Flow Map Policy（§3.1）**：
- 参数化平均速度 $u_{r,t}(a_r|s)$ 替代瞬时速度 $v_t$，通过 $X_{r,t}(a_r|s) = a_r + (t-r)u_{r,t}(a_r|s)$ 实现任意时间跨度的跳跃
- 单步生成：$a_1 = a_0 + u_{0,1}^{off}(a_0|s)$，$a_0 \sim \mathcal{N}(0, I)$
- 三种自蒸馏目标：
  - Lagrangian（LPD，Eq.4）：回归时间导数与切线条件
  - Eulerian（EPD，Eq.5）：回归空间导数 + 速度场一致性
  - Progressive（PPD，Eq.6）：半群性质一致性

### 在线适配（§3.3）

**FMQ 的核心创新（Theorem 3.2）**：
- 将在线适配建模为 trust-region 约束优化：在 $\|u_{r,1} - u_{r,1}^{ref}\|^2 \leq \eta$ 下最大化 $Q_\phi$
- 闭式最优解：$u_{r,1}^* = u_{r,1}^{off} + \eta \frac{\nabla_a Q_\phi(s, a_1)}{\|\nabla_a Q_\phi(s, a_1)\|_2}$
- 学习目标（Eq.12）是自引导的：不需要额外蒸馏网络，offline velocity 冻结作为 anchor

**不确定性感知自适应信任区域（Eq.13）**：
- 基于 twin-critic 差异 $\delta_{critic} = \frac{1}{\sqrt{2}}|Q_{\phi_1} - Q_{\phi_2}|$
- $\eta_{eff} = \frac{\eta}{1 + \beta \tilde{\delta}_{critic}}$：critic 一致时步长大，不一致时收缩

### 推理时搜索（§3.4）

**QGBS 算法**：
- 基于 SNR 的 renoising：$a_{t'} = t' \cdot a_1 + (1-t') \cdot \epsilon$，将已生成动作扰动到中间态
- 重新应用 flow map 得到多样化候选动作
- Trust-region Q-投影选择最优 M 个候选
- 迭代 K 步，计算量 NFE = M(1 + KB)


## Experiments

### 数据集

- **RoboMimic**（2 操控任务）：can（抓取罐子放入容器）、square（方形螺母装配到销钉）
- **OGBench**（10 任务）：
  - 操控（6）：cube-dbl-t3/4（双方块重排/交换）、cube-trl-t3/4（三方块拆堆/循环排列）、scene-t4/5（场景组合操控）
  - 运动（4）：hmaze-med-t3/4（人形迷宫）、amaze-gnt-t4/5（蚂蚁迷宫）

### 主要结果（Table 1）

| 方法 | IQM Success Rate [95% CI] |
|------|--------------------------|
| QC（10 步 flow matching） | 0.86 [0.84, 0.87] |
| MVP（单步 mean flow） | 0.75 [0.73, 0.77] |
| MVP + QGBS | 0.81 [0.78, 0.83] |
| FMQ | **0.91** [0.89, 0.93] |
| FMQ + QGBS | **0.93** [0.91, 0.94] |

- FMQ 在 cube-trl-t4 上 0.88 vs QC 0.37 vs MVP 0.32（最显著差异）
- FMQ 在 amaze-gnt-t4 上 0.80 vs QC 0.64 vs MVP 0.42
- 评估协议：1M 离线 + 1M 在线，每 100K 步评估 50 episodes，5 seeds IQM + 95% CI

### 消融实验

**QGBS 配置（Table 2）**：K=1, B=4, M=4 最优（20 NFE, IQM 0.93），比 best-of-32（32 NFE）少 37.5% 计算量但性能更高

**Flow Map 变体（Table 3）**：ESD（Eulerian）IQM 0.79 [0.77, 0.81] 最稳定；PSD（Progressive）0.77；LSD（Lagrangian）0.79

**收敛速度（Fig.3, Table 4）**：FMQ 达到 MVP 最高成功率 2.77× 更快，hmaze-med-t3 上 6.14×

### Trust-region 收敛分析（Fig.4）

在线训练中，$\|u^{on} - u^{off}\|^2$ 从 0 逐渐增大并稳定在 $\eta_{eff}$ 附近，验证 trust-region 约束有效工作。


## Limitations

1. **线性化近似局限**：FMQ 依赖 Q 函数的一阶 Taylor 展开，在 Q-landscape 非线性程度高的区域可能不够准确
2. **Critic 质量依赖**：方法效果直接受 critic 估计精度影响，uncertainty-aware 信任区域虽缓解但不消除此依赖
3. **QGBS 部分任务退化**：在 hmaze-med-t3 和 amaze-gnt-t4 上 QGBS 使性能分别下降 15.9% 和 3.8%
4. **未验证真实机器人**：所有实验均在仿真环境中完成，尚未部署到物理平台
5. **评估范围**：仅涉及低维状态/动作空间，未验证高维视觉输入场景


## Key Takeaways

1. **Trust-region 形式化的优势**：将在线适配建模为 trust-region 问题并推导闭式解，避免了 best-of-N 的大量采样开销，同时保证局部最优性。这个思路可推广到其他生成策略的在线适配
2. **Flow Map 统一框架**：将 Mean Flow Policy、Consistency Model 等单步方法统一到 flow map 框架下，不同自蒸馏目标的选择提供了精度-效率权衡的理论指导
3. **推理时 scaling**：QGBS 展示了在不修改训练的情况下通过推理时搜索提升性能的可能性，类似于 LLM 中的推理 scaling
4. **对 DLO 操控的启示**：FMQ 的单步生成 + Q-梯度引导策略在需要快速决策的实时操控中有应用潜力，但当前仅验证了低维状态空间
5. **自适应信任区域**：基于 critic 集成差异的不确定性感知步长调节是 RL 中简单有效的安全机制

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[flow-matching]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[ziakas|Ziakas, Christos]]
