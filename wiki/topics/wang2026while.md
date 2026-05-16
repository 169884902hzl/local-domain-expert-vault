---
title: "Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies"
tags: [manipulation, imitation, VLM, RL, bimanual]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机器人 8 个真实任务上达到 95% 平均成功率。"
authors: "Wang, Yi; Li, Xinchen; Xie, Pengwei; Yang, Pu; Nie, Buqing et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "F6CXWZV4"
---
## 摘要

Generalist robot policies increasingly benefit from large-scale pretraining（预训练）, but offline data alone is insufficient for robust real-world deployment. Deployed robots encounter distribution shifts, long-tail failures, task variations, and human correction opportunities that fixed demonstration（示范数据） datasets cannot fully capture. We present Learning While Deploying (LWD), a fleet-scale offline-to-online reinforcement learning（强化学习） framework for continual post-training of generalist Vision-Language-Action (VLA) policies. Starting from a pretrained VLA policy, LWD closes the loop between deployment, shared physical experience, policy improvement, and redeployment by using autonomous rollouts and human interventions collected across a robot fleet. To stabilize learning from heterogeneous, sparse-reward（奖励） fleet data, LWD combines Distributional Implicit Value Learning (DIVL) for robust value estimation with Q-learning via Adjoint Matching (QAM) for policy extraction in flow-based VLA action generators. We validate LWD on a fleet of 16 dual-arm（双臂） robots across eight real-world manipulation（操控） tasks, including semantic grocery restocking and 3--5 minute long-horizon（长时序） tasks. A single generalist policy improves as fleet experience accumulates, reaching an average success rate of 95%, with the largest gains on long-horizon（长时序） tasks.

## 中文简述

提出基于强化学习的双臂方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、双臂操控

## 关键贡献

1. **LWD 框架**：首个 fleet-scale offline-to-online RL 系统，用于通用 VLA 策略的后训练。将部署从"训练终点"重新定义为"策略改进来源"，形成数据飞轮（部署 → 共享经验 → 策略改进 → 重新部署）。
2. **DIVL（Distributional Implicit Value Learning）**：用分布式价值模型替代 IQL 的标量 expectile 回归，保留多模态回报分布中的高回报模式，通过自适应 τ 分位数选择 bootstrap 目标，适应异构 fleet 数据。
3. **QAM-based 策略提取**：将 DIVL critic 的动作梯度通过 Adjoint Matching 转化为 flow-based VLA 策略的分步监督，避免直接通过多步去噪反向传播的不稳定性。
4. **统一离线-在线训练目标**：离线和在线阶段使用相同的 RL 目标，减少 offline-to-online 不匹配问题。
5. **大规模真实世界验证**：16 台双臂机器人、8 个真实任务（含 3-5 分钟长时序任务），平均成功率 95%。
## 结构化提取

- **Problem**: 通用 VLA 策略在真实部署中遭遇分布偏移和长尾失败，离线数据不足以覆盖；现有 post-training 方法要么不能利用在线部署数据，要么只训练 task-specific 策略。
- **Method**: LWD = DIVL（分布价值学习）+ QAM（adjoint matching 策略提取），统一离线/在线 RL 目标，fleet-scale 部署数据飞轮。
- **Tasks**: 8 个真实操控任务——4 个 grocery restocking（短时序语义泛化）+ 4 个长时序（泡茶、榨汁、调酒、装鞋，3-5 分钟）。
- **Sensors**: 3 RGB 相机（1 head-view + 2 wrist-view）+ 本体感知（关节位置）。
- **Robot Setup**: 16 台 Agibot G1 双臂机器人（2×7-DoF 臂 + 平行夹爪），30Hz 关节位置控制。
- **Metrics**: Grocery 任务二值成功率；长时序任务 step-wise 分数（每 substep 0/0.5/1 取平均）；cycle time。
- **Limitations**: 简单在线调度策略、单一简短语言指令限制、无安全建模、单一平台验证。
- **Evidence Notes**: 完整 Table I/II/III 定量结果，value 可视化定性验证，两个消融实验。所有结果均来自真实机器人实验，无仿真。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖（Introduction, Method, Experiments, Ablation, Appendix 均已读取）
- Confidence: high
- Summary: 提出 LWD 框架，通过 fleet-scale offline-to-online RL（DIVL + QAM）对预训练 VLA 通用策略进行持续后训练，在 16 台双臂机器人 8 个真实任务上达到 95% 平均成功率。


## Problem

预训练的通用机器人策略（VLA）仅依赖离线数据无法应对真实部署中的分布偏移、长尾失败、任务变化和人类纠正机会。现有方法要么仅使用离线数据（RECAP）无法快速适应，要么使用在线策略（HG-DAgger）但只利用成功轨迹且缺乏原则性的 RL 目标。需要一个能在 fleet-scale 部署中持续改进通用 VLA 策略的 RL 框架，同时保持策略的通用性（非 task-specific）。


## Method

### 整体架构
LWD 分两个阶段：
- **离线阶段**：在混合离线 buffer（demonstrations + rollouts + play data）上预训练 policy πθ、critic Qϕ 和分布价值 Vψ。
- **在线阶段**：将策略部署到 robot fleet，自主 rollout + 人类干预数据流入在线 buffer Bon，与 Boff 混合 replay 持续更新策略。

### DIVL（Distributional Implicit Value Learning）
- **核心思想**：保持 IQL 的不对称 bootstrap 原则（避免 max_a Q(s,a) 外推），但用分布模型替代标量 expectile 回归。
- **分布建模**：Vψ(s) 预测状态条件下的 Q 值分布 pψ(v|s)（用 201 个 category 的离散分布，覆盖 [-0.1, 1.1]）。
- **TD 目标**：yQ = r_t + γ^H Quant_τ(Vψ(s_{t+H}))，取 τ-分位数而非标量期望。
- **自适应 τ**：基于分布归一化熵 H(s) 调整 τ，高不确定性时降低 τ（更保守），低不确定性时保持高 τ（更乐观）。
- **理论保证**：Proposition 1 证明 DIVL 的两步过程（拟合分布 → 提取分位数）与直接不对称回归有相同最优解。

### QAM（Q-learning via Adjoint Matching）
- 避免直接将 ∇_a Qϕ 通过 flow 多步去噪反向传播（不稳定且昂贵）。
- 保持参考 flow fβ（behavior-cloned 初始化后固定），优化 fθ。
- 终端 adjoint state g̃_1 = -∇_a Qϕ(s, a[1])/λ，通过 adjoint dynamics 回传，生成局部回归目标。

### 网络架构
- **Actor**：π0.5 flow-based VLA（PaliGemma VLM backbone: Gemma-2B + SigLIP，action expert: Gemma-300M）。
- **Value/Critic**：共享 Gemma3-270M-IT + SigLIP-So400M backbone，readout token 作状态表示，独立 value head（categorical）和 critic head（clipped double-Q）。
- **在线训练**：freeze actor VLM backbone，仅更新 action expert；value/critic 继续全参数微调。

### 关键训练细节
- 离线阶段使用 n-step chunk-level TD（长时序任务 n=10）加速稀疏奖励传播。
- 在线阶段使用 1-step TD（避免跨 policy/intervention 边界）。
- 人类干预段作为普通 replay transition 存储，使用相同 terminal reward 标签。
- 每 50 training steps 广播新策略到 fleet。


## Experiments

### 设置
- **平台**：Agibot G1 双臂机器人（2x 7-DoF 臂 + 平行夹爪 + 3 RGB 相机），30Hz 关节位置控制。
- **Fleet**：16 台机器人（4 台 grocery + 3 台 × 4 长时序任务）。
- **时间预算**：4 小时 wall-clock ≈ 60 小时 fleet 总数据。
- **任务**：
  - Grocery restocking（4 个）：flat-shelf, misplaced-item correction, freezer (door), open-cooler (carton)
  - Long-horizon（4 个）：Gongfu Tea, Fruit Juice, Cocktail, Shoebox（3-5 分钟，5-8 subtasks）

### 主结果（Table I）
| Method | Restock | Correct | Freezer | Cooler | Tea | Juice | Cocktail | Shoebox | **Avg** |
|--------|---------|---------|---------|--------|-----|-------|----------|---------|---------|
| SFT | 0.70 | 0.88 | 0.83 | 0.95 | 0.64 | 0.66 | 0.70 | 0.70 | 0.76 |
| RECAP | 0.95 | 0.96 | 0.94 | 0.95 | 0.84 | 0.82 | 0.71 | 0.70 | 0.85 |
| HG-DAgger | 1.00 | 0.92 | 0.92 | 1.00 | 0.60 | 0.66 | 0.76 | 0.90 | 0.85 |
| LWD (Offline) | 1.00 | 1.00 | 0.92 | 0.95 | 0.72 | 0.74 | 0.83 | 0.86 | 0.88 |
| **LWD (Online)** | **1.00** | **1.00** | **0.97** | 0.98 | **0.89** | **0.90** | **0.93** | **0.92** | **0.95** |

关键观察：
- LWD (Online) 在所有 8 个任务上达到最佳或接近最佳。
- 长时序任务提升最显著：从 SFT 0.68 → LWD 0.91（avg long-horizon）。
- Grocery 任务已接近饱和（RECAP/HG-DAgger 也高），LWD 仍保持竞争力。
- LWD 比参考策略减少 23.75s 平均 cycle time。

### 消融实验
1. **DIVL vs Expectile Regression**（Table II）：DIVL 在长时序任务上优势更大（offline +9.7%, online +16.7%）。
2. **Adaptive τ vs Constant τ**（Table III）：adaptive τ 平均 0.88 vs constant 0.84，在 Restocking/Cocktail 上提升明显。

### Value Function 可视化
- 成功 episode 中 value 随 subtask 完成逐步上升，失败 episode 中 value 在停滞点不再增长。
- 表明稀疏奖励下 DIVL 学到的 value 能反映任务进度。


## Limitations

1. 在线更新使用简单的实时调度策略，可能不适合更大规模部署或长期持续改进。
2. 长时序任务依赖单一简短语言指令（如"Make Tea"），复杂任务需要更强的 VLM 推理进行任务分解和细粒度提示。
3. 未显式建模执行安全，缺乏安全感知学习和控制机制。
4. 人类干预的判断依赖操作员主观决定，干预一致性可能影响学习信号质量。
5. 仅在 Agibot G1 平台验证，跨平台泛化性未验证。


## Key Takeaways

1. **Fleet-scale data flywheel**：部署本身成为训练数据来源，这对 DLO 操控场景的 long-tail failure 很有价值——DLO 的构型空间大、失败模式多样，fleet 经验的聚合能加速覆盖。
2. **Offline-to-online RL 对长时序任务的特别优势**：DLO 操控经常涉及多步骤（抓取→搬运→放置→系结），LWD 的 TD 传播 + value stitching 机制比 imitation learning 更能处理 compounding errors。
3. **DIVL 的分布式价值建模**适合异构数据：DLO 操控中同一状态可能有多种成功/失败路径，分布模型能保留稀有但可复现的成功模式。
4. **QAM 作为 flow policy 提取方法**：如果 DLO 操控使用 flow-based VLA（如 π0），QAM 提供了稳定利用 critic gradient 的途径，避免了直接反向传播的不稳定性。
5. **VLM backbone 冻结 + action expert 微调**的在线策略：计算高效，适合 DLO 场景中快速适应新材料/构型。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wang-yi|Wang, Yi]]
