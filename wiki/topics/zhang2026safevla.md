---
title: "SafeVLA: Towards safety alignment of vision-language-action model via constrained learning"
tags: [manipulation, VLM, RL, collision-avoidance]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，在 Safety-CHORES 基准上累计违规成本降低 83.58% 同时成功率提升 3.85%。"
authors: "Zhang, Borong; Zhang, Yuhao; Ji, Jiaming; Lei, Yingshan; Cai, Yishuai et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "FG6KUX89"
---
## 摘要

Vision-language-action models (VLAs) show potential as generalist robot policies. However, these models pose extreme safety challenges during real-world deployment, including the risk of harm to the environment, the robot itself, and humans. How can safety constraints be explicitly integrated into VLAs? We address this by exploring an integrated safety approach (ISA), systematically modeling safety requirements, then actively eliciting diverse unsafe behaviors, effectively constraining VLA policies via safe reinforcement learning（强化学习）, and rigorously assuring their safety through targeted evaluations. Leveraging the constrained Markov decision process (CMDP) paradigm, ISA optimizes VLAs from a min-max perspective against elicited safety risks. Thus, policies aligned through this comprehensive approach achieve the following key features: (I) effective safety-performance trade-offs, reducing the cumulative cost of safety violations by 83.58% compared to the state-of-the-art（现有最优方法） method, while also maintaining task success rate (+3.85%). (II) strong safety assurance, with the ability to mitigate long-tail risks and handle extreme failure scenarios. (III) robust generalization of learned safety behaviors to various out-of-distribution perturbations. The effectiveness is evaluated on long-horizon（长时序） mobile manipulation（移动操控） tasks. Our data, models and newly proposed benchmark environment are available at https://pku-safevla.github.io.

## 中文简述

提出基于强化学习的移动操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、碰撞避免

## 关键贡献

1. **Integrated Safety Approach (ISA) 探索**：首次系统性地研究 VLA 安全对齐的完整管线，涵盖安全建模、风险诱导、策略约束和安全保证四个相互关联的方面。
2. **Safety-CHORES 基准环境**：基于 AI2THOR 构建的新型安全评测基准，包含细粒度安全约束、大规模程序化生成场景（150K 室内场景 + 800K 3D 资产），以及五类安全关键组件（角落、盲区、易碎品集合、关键点、危险设备）。
3. **实证验证与关键发现**：ISA 对齐后的策略相比 SOTA 方法（FLaRe）累计违规成本降低 83.58%，同时任务成功率提升 3.85%；具有强安全保证（消除长尾风险）；学到的安全行为可泛化到 OOD 扰动。
## 结构化提取

- Problem: VLA 模型缺乏显式安全约束集成机制，真实部署面临环境/机器人/人类伤害风险
- Method: ISA（Integrated Safety Approach）= 安全建模（CMDP + 谓词逻辑）+ 风险诱导（Safety-CHORES 基准）+ 策略约束（Lagrangian SafeRL min-max 优化）+ 安全保证（三维度评估）
- Tasks: 长时序移动操控 — Safety-ObjNav（导航找物）、Safety-PickUp（桌面拾取）、Safety-Fetch（导航+拾取复合）
- Sensors: RGB 视觉输入 + 本体感知输入（proprioceptive），egocentric RealSense D455（sim-to-real）
- Robot Setup: 仿真中 AI2THOR 移动操控平台；Sim-to-Real 使用双 Realman RM75-6F 机械臂 + PsiBot G0-R 手爪
- Metrics: Task Success Rate (SR)、Cumulative Cost (CC = $\sum_{k=1}^{K}\sum_{t=0}^{L-1} c_k(s_t, a_t)$)
- Limitations: 仅移动操控场景、轨迹谓词 credit assignment 初步、sim-to-real 单任务验证、安全谓词需人工定义、未测动态人机场景
- Evidence Notes:

  - ISA vs FLaRe: CC 降低 83.58%，SR 提升 3.85%（Table 1）
  - 高成本轨迹消除：不安全行为严重度上界降至 FLaRe 的 1/35（Figure 3）
  - 安全-任务解耦：ISA 的 cost-success 无显著相关性，FLaRe 有显著负相关（p<0.01）
  - 风险诱导消融：去除后 CC 3x 增长，SR 从 0.865 降至 0.645（Figure 7 Left）
  - Lagrangian vs 固定惩罚：动态乘子在满足约束下获得更高 SR（Figure 6）
  - OOD 泛化：4 类视觉扰动下 SR 仅降 0.042，安全指标稳定（Table 2）
  - 极端失败：FLaRe CC=71.68 vs ISA CC=2.20（32x 差距）（Figure 7 Right）
  - Sim-to-Real：Safety-PickUp 成功部署，通过感知对齐/动力学解耦/数字孪生/数据管线一致性四策略
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML)
- Evidence Coverage: complete (all main sections + experiments + sim-to-real read)
- Confidence: high
- Summary: 首次系统探索将安全约束显式嵌入 VLA 模型，提出 ISA 框架（建模-诱导-约束-保证），基于 CMDP 的 SafeRL Lagrangian 方法对齐 VLA 安全性，在 Safety-CHORES 基准上累计违规成本降低 83.58% 同时成功率提升 3.85%。


## Problem

VLA 模型作为通用机器人策略展现巨大潜力，但真实部署时面临严重安全挑战：可能对环境、机器人自身和人类造成伤害。现有 VLA 训练方法（imitation learning 或标准 RL fine-tuning）缺乏显式安全约束集成机制。核心问题是：**如何在不牺牲任务性能的前提下，将安全约束显式地集成到 VLA 中？**


## Method

### ISA 框架（四部分）

#### 4.1 安全建模（Modeling Safety）
- 基于移动操控场景，定义静态任务组件 $(e_i, x_i, q_i, G, \Phi, \Psi)$，包括场景、初始位姿、物体类别集合，以及状态-动作安全谓词 $\Phi$ 和轨迹级安全谓词 $\Psi$。
- **状态-动作谓词** $\phi(s,a)$：通过组合逻辑 $P_s(s) \wedge P_a(a) \wedge R(s,a)$ 定义。
- **轨迹级谓词** $\psi(\tau)$：捕获时序相关的安全违规。
- 三类任务：
  - Safety-ObjNav：多房间导航寻找目标物体
  - Safety-PickUp：在桌面拾取指定物体
  - Safety-Fetch：导航 + 拾取的复合任务

#### 4.2 风险诱导（Eliciting Risks）
- 利用 ProcTHOR 150K 多样化室内场景 + Objaverse 800K 3D 资产。
- 五类安全关键组件：
  1. **Corners** ($\phi_{\text{corner}}$)：狭窄角落导致卡住或反复碰撞
  2. **Blind Spots** ($\psi_{\text{blind spot}}$)：对已见但当前未观察障碍物的碰撞
  3. **Fragile Collections** ($\psi_{\text{fragile collection}}$)：操作时对附近易碎品的附带损害
  4. **Critical Points** ($\psi_{\text{critical point}}$)：间接动作导致不稳定物体跌落
  5. **Dangerous Equipment** ($\phi_{\text{dangerous equipment}}$)：禁止与危险物品（如灶台）交互

#### 4.3 策略约束（Constraining Policies）
- 将安全谓词转化为成本信号：
  - 状态-动作谓词违规：当前步骤 cost=1
  - 轨迹级谓词违规：违规段最后一步 cost=1
- 采用 Lagrangian 松弛将 CMDP 转化为无约束 min-max 优化：
  $$\min_{\theta} \max_{\lambda \geq 0} [-\mathcal{J}_r(\theta) + \sum_{i=0}^{n} \lambda_i \mathcal{J}_{c_i}(\theta)]$$
- 迭代更新模型参数 $\theta$ 和 Lagrange 乘子 $\lambda$，优先保证安全再最大化任务性能。

#### 4.4 安全保证（Safety Assurance）
三个评估维度：
- **Test-time Safety**：标准测试集和 OOD 扰动下的安全约束遵守
- **Long-tail Safety**：统计上低频事件的安全性
- **Extreme Failure Safety**：任务不可能完成时的固有安全行为


## Experiments

### 实验设置
- **环境**：Safety-CHORES（AI2THOR 仿真器）
- **初始模型**：SPOC-DINOv2
- **训练步数**：ObjNav/PickUp 15M 步，Fetch 25M 步
- **Cost threshold** $b_i$：设为 FLaRe 收敛成本的 20%

### Baseline 方法
| 方法 | 类型 |
|------|------|
| SPOC | IL-only |
| SPOC-GT | IL + ground truth 信息 |
| FLaRe | IL + 标准 RL fine-tuning |
| FLaRe-RS | IL + RL + reward shaping |
| Poliformer | RL-only (导航) |

### 主要结果
- ISA 相比 FLaRe：CC 降低 **83.58%**，SR 提升 **+3.85%**
- ISA 消除了高累积成本轨迹（CC>10），不安全行为严重度上界降至 FLaRe 的 1/35
- 安全成本与任务成功解耦（ISA 的 T-test 拒绝 cost-success 相关性，而 FLaRe 有显著负相关 p<0.01）

### 消融实验
1. **风险诱导的重要性**：去除安全关键组件后 CC 近乎三倍（5.01 vs 1.854），SR 显著下降（0.645 vs 0.865）
2. **Lagrangian 乘子的优势**：动态乘子优于固定惩罚系数，在满足成本约束的同时获得更高 SR
3. **Cost threshold 影响**：严格阈值（10%）降低成本但也略微影响 SR；20% 提供平衡

### OOD 泛化
- 四种扰动：颜色、光照、材质、全部组合
- SR 平均仅下降 0.042，安全指标保持稳定
- PickUp+All 甚至显示 CC 下降

### 极端失败场景
- 使用陌生目标诱导 100% 任务失败
- FLaRe CC=71.68（ISA 的 32 倍），SPOC CC=14.63（ISA 的 7 倍）
- ISA CC=2.20，证明安全行为已内化而非表面现象

### Sim-to-Real 验证
- 平台：双 Realman RM75-6F 机械臂 + PsiBot G0-R 手爪 + egocentric RealSense D455
- 成功部署 Safety-PickUp 任务
- 关键策略：感知对齐（FoundationPose 6D pose）、动力学解耦（语义/Cartesian 动作空间）、数字孪生对齐（PID 参数微调）、数据管线一致性


## Limitations

1. 仅在移动操控任务上验证，未涉及灵巧操作或双臂协同等更复杂场景
2. 轨迹级安全谓词的 credit assignment 仍为初步探索（仅归因于违规段最后一步），未来需改进
3. Sim-to-Real 仅在 Safety-PickUp 单一任务上验证，泛化性有待进一步证明
4. 安全谓词需要人工定义和工程化，难以覆盖所有潜在安全风险
5. 未在真实世界的复杂动态场景（如人机共存）中测试


## Key Takeaways

1. **CMDP + Lagrangian SafeRL 可有效约束 VLA 安全**：通过 min-max 优化显式平衡安全与性能，比 reward shaping 更优。这对我们研究双臂 DLO 操控的安全约束集成有直接参考价值。
2. **风险诱导是关键**：仅用安全约束方法不够，还需要丰富多样的场景来诱导和暴露潜在不安全行为。Safety-CHORES 的五类安全关键组件设计思路可借鉴到 DLO 场景（如线缆缠绕、碰撞易碎品等）。
3. **安全行为可泛化到 OOD**：学到的安全行为不是表面模式匹配，在视觉扰动和极端失败下依然保持。
4. **Sim-to-Real 可行但需工程适配**：感知对齐、动力学解耦、数字孪生是三大关键策略。
5. **VLA 安全对齐是新兴方向**：这是首个系统性工作，后续在灵巧操作、DLO 操控等细分领域的安全对齐尚属空白。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[collision-avoidance]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhang-borong|Zhang, Borong]]
- [[zhang-yuhao|Zhang, Yuhao]]
- [[ji-jiaming|Ji, Jiaming]]
