---
title: "NavOL: Navigation policy with online imitation learning"
tags: [imitation, RL, diffusion, diffusion-model, sim-to-real]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "基于 DAgger 框架在 IsaacLab 中实现导航扩散策略的在线模仿学习，通过全局规划器提供在线专家轨迹监督，以 rollout-update 循环消除奖励工程、缓解分布偏移，在仿真和真实环境均显著优于离线方法 NavDP。"
authors: "Wei, Xiaofei; Gu, Chun; Zhang, Li"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "9Z8I6NIV"
---
## 摘要

Learning robust navigation policies remains a core challenge in robotics. Offline imitation learning（模仿学习） suffers from distribution shift and compounding errors at rollout, while reinforcement learning（强化学习） requires reward（奖励） engineering and learns inefficiently. In this paper, we propose NavOL, an online imitation learning（模仿学习） paradigm that interacts with a simulator and updates itself using expert demonstrations gathered online. Built upon a pretrained navigation diffusion policy（扩散策略） that maps local observations to future waypoints, NavOL trains in a rollout update loop: during rollout, the policy acts in the simulator and queries a global planner which has privileged access to the global environment for the optimal path segment as ground truth trajectory labels; during update, the policy is trained on the online collected observation trajectory pairs. This online imitation loop removes the need for reward（奖励） design, improves learning efficiency, and mitigates distribution shift by training on the policy own explored rollouts. Built on IsaacLab with fast, high-fidelity parallel rendering and domain randomization of camera pose and start-goal pairs, our system scales across 50 scenes on 8 RTX 4090 GPUs, collecting over 2,000 new trajectories per hour, each averaging more than 400 steps. We also introduce an indoor visual navigation benchmark with predefined start and goal positions for zero-shot（零样本） generalization. Extensive evaluations on simulation benchmarks, including the NavDP benchmark and our proposed benchmark, as well as carefully designed real-world experiments, demonstrate the effectiveness of NavOL, showing consistent performance gains in online imitation learning（模仿学习）.

## 中文简述

提出基于扩散策略的导航方法，具有零样本泛化特点。

**研究方向**: 模仿学习、强化学习、扩散模型、扩散模型、仿真到真实迁移

## 关键贡献

1. 提出 NavOL，首个将 DAgger 式在线模仿学习扩展到高维视觉扩散导航策略的框架
2. 基于 IsaacLab 实现大规模并行 rollout-update 管线：8 × RTX 4090 上每小时采集 2000+ 轨迹（50 场景），远超真实数据采集效率
3. 构建基于 3D-Front 的室内视觉导航基准，8 个未见场景 × 100 对起终点，用于零样本泛化评估
4. 在 NavDP benchmark、自建 benchmark 和 Unitree Go2 真实部署上全面超越 DD-PPO、iPlanner、ViPlanner、NavDP
## 结构化提取

- Problem: 离线模仿学习的导航扩散策略存在分布偏移和复合误差，强化学习需要奖励工程且样本效率低
- Method: DAgger 式在线模仿学习 + 扩散导航策略，rollout（策略交互 + 全局规划器标签）→ update（DDPM 去噪训练）循环
- Tasks: Point-goal 室内视觉导航（给定目标点，从起点导航至目标 1m 以内）
- Sensors: RGB-D 相机（第一人称视角），DepthAnythingV2 ViT backbone
- Robot Setup: 仿真训练用 Dingo，真实部署用 Unitree Go2 四足 + RealSense D435i
- Metrics: Success Rate (SR), Success-weighted Path Length (SPL)
- Limitations: 场景管线复杂、训练算力需求、场景边界漏洞、低矮障碍物误判、critic 贡献有限
- Evidence Notes: (1) 自建 benchmark 上 mSR 69.0 vs NavDP 42.2（+26.8），充分证明在线交互训练的优势；(2) 从零训练 16 GPU-days > NavDP 1024 GPU-days，说明数据效率提升两个数量级；(3) 真实世界三场景平均 SR 83.3% vs NavDP 26.7%，Sim-to-Real 迁移有效；(4) 消融去除专家动作后 SR 降至 43.9，证明混合执行策略的关键性
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖（全文 + 附录 + 实验表格）
- Confidence: high
- Summary: 基于 DAgger 框架在 IsaacLab 中实现导航扩散策略的在线模仿学习，通过全局规划器提供在线专家轨迹监督，以 rollout-update 循环消除奖励工程、缓解分布偏移，在仿真和真实环境均显著优于离线方法 NavDP。


## Problem

机器人视觉导航策略学习中，离线模仿学习（如 NavDP）受限于分布偏移和复合误差——策略在部署时逐步偏离训练分布导致失败；强化学习虽可交互优化，但依赖人工奖励设计且样本效率极低。如何在不引入奖励工程的前提下，通过在线交互弥合分布偏移，实现鲁棒且可 Sim-to-Real 迁移的导航策略？


## Method

### 核心架构
- **基础**: 继承 NavDP（Cai et al., 2025）的多模态扩散策略架构，包含两个协作组件：
  - **轨迹生成器 f**: DepthAnythingV2 ViT 编码 RGB-D → 16 个融合 token → Goal embedding 条件化 → DiT + DDPM 调度器去噪生成 K=24 步 waypoint 序列
  - **Critic V**: 共享视觉 token 和 DiT backbone（不含 goal token），对候选轨迹打分输出安全性标量

### 在线模仿学习管线（DAgger 思想）
- **Expert Planner**: 基于 NavMesh（Habitat-Sim）的全局规划器，训练时提供 privileged 最优路径；部署时不需要
- **Rollout 阶段**:
  - 策略以概率 ρ=0.8 执行自身动作，以概率 0.2 执行专家动作（稳定训练）
  - 全局规划器并行提供专家轨迹标签 a*_t 和安全分数 v'_t
  - waypoint → MPC → 低级控制器执行
  - 采集数据元组 {(o_t, g_t, a*_t, v'_t)}
- **Update 阶段**:
  - 仅使用当次 rollout 数据（丢弃历史），最大化更新效率
  - 复用 rollout 时计算的 RGB-D visual tokens，避免重复编码
  - Actor loss: 标准 DDPM 去噪 MSE（式 5）
  - Critic loss: MSE(v'_t, V_θ(o, a))（式 6）
  - 总损失: L = L_actor + λL_critic（式 7）

### 场景准备
- 基于 3D-Front 数据集，BlenderProc 重贴纹理、修正法线
- 高保真渲染：全局光照、反射、阴影、AO、DLAA
- Domain randomization: 相机高度/俯仰角随机化、agent 尺寸随机化
- 起-终点筛选: 路径关键点 ≥ 5 以保证难度


## Experiments

### 仿真基准 1: NavDP Benchmark（4 场景）

| Method | mSR(↑) | mSPL(↑) |
|--------|--------|---------|
| DD-PPO | ~1.5 | ~1.5 |
| iPlanner | ~59.7 | ~54.7 |
| ViPlanner | ~68.9 | ~63.7 |
| NavDP | ~78.3 | ~73.0 |
| **NavOL** | **82.5** | **77.4** |

（按 Table 1 平均值估算，原文分场景列出具体数值）

### 仿真基准 2: 自建 Benchmark（8 个未见场景）

| Method | mSR(↑) | mSPL(↑) |
|--------|--------|---------|
| DD-PPO | 2.9 | 2.4 |
| iPlanner | 18.7 | 18.4 |
| ViPlanner | 33.0 | 31.5 |
| NavDP | 42.2 | 37.7 |
| **NavOL** | **69.0** | **63.7** |

NavOL 在自建 benchmark 上的优势更为显著（mSR +26.8），表明在线交互训练对分布外场景的泛化提升更大。

### 真实世界部署（Unitree Go2 + RealSense D435i）
| Scene | NavDP | NavOL |
|-------|-------|-------|
| Office | 4/10 | **8/10** |
| Gym | 2/10 | **7/10** |
| Corridor | 2/10 | **10/10** |

注意：训练时使用 Dingo 机器人，部署在 Go2 上——跨具身泛化能力显著。

### 计算效率对比（Table 5）
| Method | GPU-days | mSR | mSPL |
|--------|----------|-----|------|
| NavDP (32 × A100, 32 days) | ~1024 | 42.2 | 37.7 |
| NavOL from scratch (8 × 4090, 2 days) | 16 | 48.3 | 45.5 |
| NavOL (NavDP init + 8 × 4090, 2 days) | ~1040 | **69.0** | **63.7** |

从零训练仅用 16 GPU-days 即超过 NavDP 1024 GPU-days 的性能。

### 消融实验（Table 4，自建 benchmark）
- **训练场景数**: 1 scene (57.8 SR) < 10 scenes (64.8) < 50 scenes (69.0)
- **Rollout 步数**: 8 steps (67.9) ≈ 32 steps (68.5)，影响不大
- **去除专家动作** (ρ=1): SR 从 69.0 降至 43.9——纯策略 rollout 访问不良状态
- **从零训练**: 48.3 vs 69.0（有 NavDP 预训练），说明好的行为先验对在线学习至关重要
- **路径后处理**: 去除后 64.2，策略倾向于贴近障碍物
- **相机随机化**: 去除后 66.0，零样本泛化下降
- **Critic**: 去除后 67.1，提升不大（在线训练已使策略学会避障），但提供轻量安全边际


## Limitations

1. **场景管线复杂度**: BlenderProc + IsaacSim 的资产准备流程降低可及性（但为一次性开销）
2. **训练算力**: 8 × RTX 4090 × 2 天仍有门槛，尽管远低于 NavDP 的 1024 GPU-days
3. **场景边界漏洞**: 真实部署中策略偶尔将测试区域边界间隙当作可行路径
4. **低矮障碍物误判**: 相机安装高度有限，无法完整感知桌腿等低矮障碍物几何，导致穿越卡住
5. **Critic 贡献有限**: 在线训练下 critic 的额外增益仅 ~2%，主要收益来自 on-policy 数据采集


## Key Takeaways

1. **DAgger 扩展到扩散策略是可行的**: 关键在于 (a) 以预训练模型作为行为先验避免早期 rollout 崩溃；(b) 混合专家动作（ρ=0.8）稳定训练；(c) 仅保留当次 rollout 数据而非积累
2. **在线交互数据 >> 离线数据规模**: 16 GPU-days 的在线训练 > 1024 GPU-days 的离线渲染，核心是 on-policy 数据自然覆盖了策略实际访问的状态分布
3. **全局规划器作为免费标签源**: NavMesh 查询开销可忽略，但提供了高质量的 stepwise 监督——无需奖励工程
4. **Sim-to-Real + 跨具身**: 从 Dingo 到 Go2 的零样本迁移成功，验证了纯仿真训练的可行性
5. **对 DLO 操控的启示**: DAgger + 扩散策略的组合思路可迁移到 DLO 操控场景——用仿真中的最优轨迹规划器作为专家，在线纠正扩散策略的分布偏移

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[wei-xiaofei|Wei, Xiaofei]]
- [[gu-chun|Gu, Chun]]
