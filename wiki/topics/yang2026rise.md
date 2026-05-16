---
title: "RISE: Self-Improving Robot Policy with Compositional World Model"
tags: [manipulation, VLM, RL, collision-avoidance]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实现 on-policy 自我改进，在动态分拣、背包打包、箱子闭合三项真实双臂任务上分别达到 85%/85%/95% 成功率。"
authors: "Yang, Jiazhi; Lin, Kunyang; Li, Jinwei; Zhang, Wencong; Lin, Tianwei et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PKFSG85H"
---
## 摘要

Despite the sustained scaling on model capacity and data acquisition, Vision-Language-Action (VLA) models remain brittle in contact-rich（接触丰富） and dynamic manipulation（操控） tasks, where minor execution deviations can compound into failures. While reinforcement learning（强化学习） (RL) offers a principled path to robustness, on-policy RL in the physical world is constrained by safety risk, hardware cost, and environment reset. To bridge this gap, we present RISE, a scalable framework of robotic reinforcement learning（强化学习） via imagination. At its core is a Compositional World Model that (i) predicts multi-view future via a controllable dynamics model, and (ii) evaluates imagined outcomes with a progress value model, producing informative advantages for the policy improvement. Such compositional design allows state and value to be tailored by best-suited yet distinct architectures and objectives. These components are integrated into a closed-loop（闭环） self-improving pipeline that continuously generates imaginary rollouts, estimates advantages, and updates the policy in imaginary space without costly physical interaction. Across three challenging real-world tasks, RISE yields significant improvement over prior art, with more than +35% absolute performance increase in dynamic brick sorting, +45% for backpack packing, and +35% for box closing, respectively.

## 中文简述

提出基于强化学习的操控方法，具有闭环控制特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、碰撞避免

## 关键贡献

1. **RISE 框架**：首个将世界模型作为学习环境用于挑战性真实世界操控的 on-policy RL 系统。将机器人交互从物理环境转移到想象空间，实现可扩展的自主自我改进。
2. **组合式世界模型（Compositional World Model）**：将世界建模分解为 dynamics prediction 和 value estimation 两个独立优化的子问题，各自采用最适合的架构和训练目标。dynamics model 基于 Genie Envisioner + Task-Centric Batching 策略实现可控多视角视频预测；value model 基于 π₀.5 VLA backbone + progress estimate + TD learning 实现稠密且对失败敏感的价值评估。
3. **全面实验验证**：在三项真实世界灵巧操控任务上显著超越所有 RL/IL 基线方法，成功率提升 35-45 个百分点。
## 结构化提取

- Problem: VLA 模型在接触丰富操控任务中因 exposure bias 和复合错误表现脆弱；物理世界 on-policy RL 受安全、成本和重置限制
- Method: 组合式世界模型（controllable dynamics model + progress value model）+ advantage-conditioned on-policy RL in imagination
- Tasks: Dynamic Brick Sorting（传送带分拣）、Backpack Packing（背包打包）、Box Closing（箱子闭合）
- Sensors: 3 视角 RGB 相机（top-down + 双手腕相机），192×256 分辨率
- Robot Setup: 双臂 7-DoF AgileX 机器人，absolute joint control，30 Hz 控制频率，14 维动作空间
- Metrics: Success Rate（20 次试验）+ Stage-wise Score（10 分制里程碑评分）
- Limitations: 想象-现实差距；离线-在线数据平衡需调参；世界模型训练计算成本高；DLO 形变建模精度受限
- Evidence Notes: 全文已精读（含附录）。主实验 3 项真实任务，消融实验覆盖 offline ratio、online action/state、各模块贡献、dynamics model 质量比较。基线涵盖 IL（DAgger）、online RL（PPO）、offline RL（DSRL、RECAP）。动力学模型定量比较使用 PSNR/LPIPS/SSIM/FVD/EPE 五项指标。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（正文 + 附录 + 实验细节均已覆盖）
- Confidence: high
- Summary: 提出基于组合式世界模型（dynamics model + progress value model）的想象空间强化学习框架 RISE，使 VLA 策略在无需物理交互的情况下实现 on-policy 自我改进，在动态分拣、背包打包、箱子闭合三项真实双臂任务上分别达到 85%/85%/95% 成功率。


## Problem

VLA（Vision-Language-Action）模型在接触丰富、动态变化的操控任务中表现脆弱——微小的执行偏差会导致复合错误（compounding errors）。模仿学习（IL）受限于专家数据质量和覆盖范围，且存在 exposure bias。强化学习（RL）理论上是提升鲁棒性的途径，但在物理世界中 on-policy RL 面临安全风险、硬件成本和环境重置三大障碍。现有方法要么在仿真器中训练（Sim-to-Real gap），要么依赖有限的 offline 数据（分布偏移严重）。核心矛盾：如何在真实机器人场景下实现可扩展的 on-policy RL？


## Method

### 整体架构
RISE 包含三个阶段：
1. **Policy Warm-up**：用 offline 数据（专家演示 + 策略 rollout + 人类纠正）对预训练 VLA 策略 π₀.5 进行 advantage-conditioned 微调
2. **Self-Improving Loop**：迭代执行 Rollout Stage 和 Training Stage
   - **Rollout Stage**：从 offline 数据采样初始状态 → rollout policy 生成候选动作 → dynamics model 模拟未来观测 → value model 评估 advantage
   - **Training Stage**：用 advantage-conditioned flow matching 目标训练行为策略

### Compositional World Model

**Controllable Dynamics Model**：
- 基础架构：Genie Envisioner (GE-base)，继承 LTX-Video 的效率优势
- 关键改进：
  - 额外训练轻量 action encoder，在大规模 action-labeled 数据集（Agibot World + Galaxea）上预训练
  - 对 context frames 施加更强噪声，提升对 motion blur 和 visual artifacts 的鲁棒性
  - **Task-Centric Batching**：每个 batch 只采样少量任务但覆盖同一场景下不同动作的多样样本，优先保证动作多样性而非场景多样性
- 效率：合成 25 帧多视角观测仅需 <2 秒，比 Cosmos 快 300 倍
- 仅在训练时使用，推理时零开销

**Progress Value Model**：
- 初始化：从预训练 VLA π₀.5 的 backbone 初始化（带来机器人中心的理解能力和多视角兼容性）
- 训练目标组合：
  - `L_prog`：时间进度回归（coarse monotonic understanding）
  - `L_TD`：Temporal-Difference learning（对失败敏感，用成功和失败 rollout 数据训练）
  - 最终损失：`L_V = L_prog + L_TD`
- 训练策略：前 10k 步仅 progress loss，后 40k 步加入 TD loss

### RL 公式化
- 将 advantage 定义为 chunk 内预测未来观测值相对于初始观测的改进期望
- 采用 probabilistic inference 框架，将策略优化转化为 advantage-weighted 条件生成
- 通过 discretized advantage bins（10 个均匀区间）引导策略生成

### 关键实现细节
- 机器人：双臂 7-DoF AgileX，absolute joint control，30 Hz
- 传感器：3 视角 RGB（top-down + 双手腕相机），192×256 分辨率
- Action chunk：H=50 步，维度 14（双臂各 6 DoF + 1 DoF gripper）
- Dynamics model 预训练：16×H100 GPU，batch size 512，约 7 天
- Task-specific fine-tuning：8×H100 GPU，batch size 64，约 3 天
- Value model 训练：8 GPU，50k 步，约 1 天
- Self-improving loop：约 10k 步


## Experiments

### 任务设置
| 任务 | 描述 | 挑战点 |
|------|------|--------|
| Dynamic Brick Sorting | 从传送带上抓取彩色砖块放入对应颜色箱子 | 动态目标、精准追踪 |
| Backpack Packing | 打开背包 → 放入衣物 → 提起 → 拉链 | 可变形物体操控 |
| Box Closing | 装杯 → 折侧翼 → 折后盖 → 插入锁扣 | 精密双臂协调 |

### 主要结果（Table I，20 次试验平均值）
| 方法 | Brick Sorting Succ. | Score | Backpack Succ. | Score | Box Closing Succ. | Score |
|------|---------------------|-------|----------------|-------|--------------------|-------|
| π₀.5 | 35% | 8.28 | 30% | 4.25 | 35% | 7.50 |
| π₀.5+DAgger | 15% | 6.10 | 50% | 7.00 | 40% | 7.50 |
| π₀.5+PPO | 10% | 7.68 | 35% | 5.88 | 10% | 4.75 |
| π₀.5+DSRL | 10% | 6.65 | 10% | 3.50 | 10% | 7.63 |
| RECAP | 50% | 9.00 | 40% | 6.13 | 60% | 8.13 |
| **RISE** | **85%** | **9.78** | **85%** | **9.50** | **95%** | **9.88** |

### 消融实验关键发现
1. **Offline data ratio**（Table II）：最佳比例 0.6，过低导致灾难性遗忘，过高限制探索
2. **Online action + state**（Table III）：单独 online action 从 35%→40%，加入 online state →70%，证实动态生成状态的必要性
3. **模块消融**（Table IV）：
   - 去掉 visual pre-training：sorting accuracy 下降 32.15%，completion 降至 15%
   - 去掉 Task-Centric Batching：completion 下降 30%
   - 去掉 progress loss：success 下降 20%
   - 去掉 TD learning：success 下降 35%
4. **Dynamics model 质量**（Table V）：RISE 在 PSNR、LPIPS、SSIM、FVD、EPE 上全面优于 Cosmos 和 GE

### 评估指标
- Success Rate：任务完全成功的百分比
- Stage-wise Score：10 分制里程碑评分（每个子目标 2.5 分），更细粒度地捕捉部分成功


## Limitations

1. **想象-现实差距**：世界模型在罕见或欠表示场景下仍可能生成物理不可信的过渡，需要 uncertainty-aware imagination 和物理约束的进一步研究
2. **离线-在线数据平衡**：真实世界数据仍然必不可少，最优离线/在线比例需要额外调参，理解原则仍是开放问题
3. **计算成本**：虽然将瓶颈从物理交互转移到计算，但训练高保真世界模型本身计算开销巨大（16+8 H100 GPU，总计约 11 天训练），对计算受限场景不够友好
4. **失败模式**（Fig. 18）：动态分拣中追踪失败/抓取滑脱、背包打包中可变形物体操控不稳定、箱子闭合中双臂同步误差导致翻盖错位


## Key Takeaways

1. **组合式世界模型设计理念**：将 dynamics 和 value 分离，各自使用最适合的架构，是 VLA 自我改进的关键设计。这种解耦思路可推广到其他机器人学习场景。
2. **想象空间 RL 的可行性**：首次证明世界模型可以作为有效的 on-policy RL 学习环境用于真实世界灵巧操控，避免了物理交互的成本和安全风险。这与我们的 Sim-to-Real 研究有互补性——世界模型学习可视为一种"学习型仿真器"。
3. **Task-Centric Batching 策略**：优先保证同一场景下的动作多样性而非场景多样性，这一原则对 DLO 操控中的数据采样策略有借鉴意义。
4. **Value model 的双层训练**：progress estimate 提供稳定的粗粒度信号，TD learning 提供对失败敏感的细粒度信号。这种组合对接触丰富的操控任务特别重要。
5. **与 DLO 操控的相关性**：Backpack Packing 任务涉及可变形物体（衣物、背包），与 DLO 操控直接相关。RISE 在此任务上从 30%→85%（+55%），表明想象空间 RL 对可变形物体操控有显著潜力。但该方法对世界模型精度要求高，DLO 的复杂形变可能需要更精细的 dynamics model。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[collision-avoidance]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[yang-jiazhi|Yang, Jiazhi]]
- [[lin-kunyang|Lin, Kunyang]]
