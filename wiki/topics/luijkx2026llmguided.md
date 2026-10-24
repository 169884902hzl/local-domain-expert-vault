---
title: "LLM-guided task- and affordance-level exploration in reinforcement learning"
tags: [manipulation, VLM, RL, sim-to-real, planning]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正 LLM 的物理不可行方案，在 pick-and-place 任务上实现高效采样和零样本 sim-to-real 迁移。"
authors: "Luijkx, Jelle; Ma, Runyu; Ajanović, Zlatan; Kober, Jens"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XTKEV663"
---
## 摘要

Reinforcement learning（强化学习） (RL) is a promising approach for robotic manipulation（机器人操控）, but it can suffer from low sample efficiency and requires extensive exploration of large state-action spaces. Recent methods leverage the commonsense knowledge and reasoning abilities of large language models (LLMs) to guide exploration toward more meaningful states. However, LLMs can produce plans that are semantically plausible yet physically infeasible, yielding unreliable behavior. We introduce LLM-TALE, a framework that uses LLMs' planning to directly steer RL exploration. LLM-TALE integrates planning at both the task level and the affordance（可供性） level, improving learning efficiency by directing agents toward semantically meaningful actions. Unlike prior approaches that assume optimal LLM-generated plans or rewards, LLM-TALE corrects suboptimality online and explores multimodal（多模态） affordance（可供性）-level plans without human supervision. We evaluate LLM-TALE on pick-and-place tasks in standard RL benchmarks, observing improvements in both sample efficiency and success rates over strong baselines. Real-robot experiments indicate promising zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer. Code and supplementary material are available at llm-tale.github.io.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、仿真到真实迁移、运动规划

## 关键贡献

1. **层次化 LLM 规划方案**：生成任务层计划（pick/transport 原语序列）和可供性层动作候选（多种抓取/放置方式），使用三级 prompt 结构（T: 任务规划、M: 可供性识别、P: 可供性规划）
2. **目标条件残差 RL 框架**：以 LLM 生成的可供性目标为条件，PD 控制器为基策略，RL 学习残差修正动作，内在奖励基于目标位姿误差和关节速度，无需任务特定调参
3. **Critic-不确定性引导的可供性探索**：利用价值函数估计和不确定性分数在多模态可供性间权衡探索与利用（p_sel(i) ∝ exp(β·V(s,g) - c)），在线纠正物理不可行的 LLM 方案
## 结构化提取

- **Problem**: RL 样本效率低；LLM 规划语义正确但物理不可行；现有 LLM+RL 方法依赖高质量 LLM 输出或人类示教
- **Method**: LLM-TALE = 层次化 LLM 规划（任务层 T + 可供性识别 M + 可供性规划 P） + 目标条件残差 RL（PD 基策略 + RL 残差修正） + Critic-不确定性引导的多模态可供性探索
- **Tasks**: Pick-and-place（PickCube, StackCube, PegInsert, TakeLid, OpenDrawer, PutBox）
- **Sensors**: 物体状态（位姿）；视觉变体使用 RGB-D（DrQ-v2 编码器）；真实世界使用 RealSense D435 进行物体跟踪
- **Robot Setup**: Franka Emika Panda + Franka 夹爪；笛卡尔阻抗控制器 1kHz 控制频率；末端执行器相对位姿控制 (δx, δy, δz, δrx, δry, δrz, grip)
- **Metrics**: 成功率、采样效率（达到收敛的训练步数）
- **Limitations**: 仅简单几何物体；依赖物体状态；未验证复杂操控任务（DLO/铰接体）；使用闭源 GPT-4o；未采用显式 sim-to-real 技术
- **Evidence Notes**:

  - 仿真：6 任务 × 3 seeds，对比 Text2Reward、RLPD、LLM-BC，LLM-TALE TD3 在多数任务中采样效率和成功率最优
  - 可供性探索：PegInsert 学到头部抓取更优，PutBox 学到侧面抓取 + 垂直放置避免倾倒
  - 真实世界：PutBox 零样本迁移 93.3%（15 集），LLM-only 0%（碰撞失败），证明残差学习的必要性
  - 视觉变体：CNN 编码 + random-shift augmentation，与状态输入采样效率相当
## 本地引用关系

- [[luijkx2026llmguided]]
- [[ma2025running]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含方法、实验、真实机器人结果）
- Confidence: high
- Summary: 提出 LLM-TALE 框架，利用 LLM 在任务层和可供性层进行层次化规划，引导 RL 探索语义有意义的动作空间，通过 critic-uncertainty 机制在线纠正 LLM 的物理不可行方案，在 pick-and-place 任务上实现高效采样和零样本 sim-to-real 迁移。


## Problem

RL 应用于机器人操控时样本效率低，尤其在长时序稀疏奖励任务中需要大量探索。现有方法：
- 内在动机方法（如 curiosity）可能被无关新颖状态吸引（"noisy-TV" 问题）
- 人类示教方法成本高
- LLM 生成奖励函数可能导致 reward hacking
- LLM 直接生成动作依赖高质量 LLM 输出，且仅限 off-policy RL

核心矛盾：LLM 的语义推理能力强，但缺乏物理理解；RL 能通过与环境交互学习物理行为，但探索效率低。


## Method

### 规划阶段（训练前一次性执行）
1. **任务层规划**：prompt T 将自然语言任务指令分解为 pick/transport 原语序列（Python 函数）
2. **可供性识别**：prompt M 为每个原语枚举语义上不同的可供性模式（如顶部抓取 vs 侧面抓取）
3. **可供性规划**：prompt P 将每个可供性描述映射为末端执行器姿态规范（位置 + EE z轴 + EE y轴），transport 任务使用物体中心表示提高鲁棒性

### 训练阶段
- **基策略**：PD 控制器沿线性轨迹驱动末端执行器向目标移动
- **残差策略**：π(·|s, gj) 学习修正动作，执行动作 a = a_PD + a_residual
- **目标选择**：基于价值函数 V_ϕ(s, g_j^i) 和不确定性 c_j^i 的 softmax 采样
- **不确定性衰减**：c ← max((1-α)c, c_min)，已探索的模式不确定性降低
- **内在奖励**：基于目标位姿误差的 dense shaping（如 r_in = -tanh(5·e_pos) - 0.25·tanh(‖q̇‖)）
- **外部奖励**：稀疏二值 {0, 1} 任务成功信号

### 技术细节
- LLM：GPT-4o，训练前查询一次并缓存结果
- 兼容 on-policy（PPO）和 off-policy（TD3）
- 视觉变体使用 DrQ-v2 式编码器（CNN + random-shift augmentation）


## Experiments

### 仿真实验（6 个任务）
- **ManiSkill**：PickCube、StackCube、PegInsertionSide
- **RLBench**：TakeLid、OpenDrawer、PutBox（自定义，含倾倒约束）
- **动作空间**：(δx, δy, δz, δrx, δry, δrz, grip)
- **基线**：Text2Reward（zero-shot/few-shot）、RLPD（25 次示教）、LLM-BC（消融）
- **结果**：
  - LLM-TALE TD3 在所有任务上收敛最快且最稳定
  - LLM-TALE PPO 略慢但仍有正趋势（PegInsert 除外）
  - 大多数设置下比 RLPD（需示教）和 Text2Reward 更高效
  - LLM-BC 消融（BC 替换 PD 基策略）表现差——BC 在 OOD 状态下失效
  - 视觉变体（PickCube/StackCube）与状态输入相当的采样效率

### 可供性探索分析
- **PegInsert**（2 模态）：快速学到头部抓取优于端部抓取
- **PutBox**（4 模态）：最终放弃顶部抓取，选择侧面抓取 + 垂直放置（避免倾倒）

### 真实世界实验
- **平台**：Franka Panda + Franka 夹爪，笛卡尔阻抗控制器 1kHz，RealSense D435 RGB-D 相机
- **任务**：PutBox
- **结果**：
  - LLM-TALE TD3：15 集中 93.3% 成功率（1 次失败）
  - LLM-only 基策略：0%（全部因碰撞失败）
- **轨迹分析**：残差策略学会避开碰撞、增加垂直间距，轨迹更高效

### 关键结果表
| 方法 | PickCube | StackCube | PegInsert | PutBox (real) |
|------|----------|-----------|-----------|---------------|
| LLM-TALE TD3 | 高且快 | 高且快 | 高且快 | 93.3% |
| LLM-TALE PPO | 高（稍慢） | 高（稍慢） | 正趋势 | - |
| Text2Reward | 较低 | 较低 | 较低 | - |
| RLPD (25 demos) | 可比 | 可比 | 可比 | - |
| LLM-BC TD3 | 仅 PickCube 有效 | 失败 | 失败 | - |
| LLM-only | - | - | - | 0% |


## Limitations

1. **几何复杂度受限**：仅适用于简单物体（方块、盒子、抽屉把手），不处理复杂几何
2. **依赖物体状态**：需要精确的物体位姿估计（真实部署需要状态估计器）
3. **任务类型有限**：仅验证了 pick-and-place 类型，未涉及铰接体、DLO 等复杂物体
4. **LLM 依赖**：使用 GPT-4o（闭源、需 API），未测试开源 LLM 的表现
5. **无 Sim-to-Real 技术**：仅依赖残差策略的自然鲁棒性，未采用域随机化等方法
6. **单步 affordance**：affordance 目标是固定姿态点，非动态轨迹


## Key Takeaways

### 对 DLO 操控的启发
- **层次化规划范式值得借鉴**：任务层分解 + affordance 层候选的思想可迁移到 DLO 任务（如 pick-and-hang 需要选择抓取点、拉拽方向等）
- **多模态 affordance 探索**：DLO 有多种抓取和操控方式，critic-uncertainty 机制可用于在线选择最优操控策略
- **残差 RL 提升鲁棒性**：LLM/DVA 提供粗略方向，RL 学习精细修正——适合 DLO 形变补偿
- **局限性明显**：DLO 的形变自由度远超刚体，固定目标点范式不直接适用；需要动态轨迹级 affordance

### 对 VLM-based 控制的启发
- **LLM 作为"高层引导器"而非"直接执行器"**：避免 LLM 的物理不可行问题，用 RL 弥合语义-物理差距
- **无需示教数据**：仅靠 LLM 规划 + 稀疏奖励即可高效学习，降低数据采集成本
- **在线纠正 LLM 错误**：价值函数和不确定性机制自然淘汰物理不可行的 LLM 方案

### 方法亮点
- 训练前一次性查询 LLM 并缓存，训练过程中无需反复调用 API
- 兼容 on-policy 和 off-policy 算法
- 内在奖励不依赖任务特定调参

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[luijkx|Luijkx, Jelle]]
- [[ma-runyu|Ma, Runyu]]
- [[ajanovic-zlatan|Ajanović, Zlatan]]
- [[kober|Kober, Jens]]
