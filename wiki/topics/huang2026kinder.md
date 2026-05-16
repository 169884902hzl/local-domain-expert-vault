---
title: "KinDER: A physical reasoning benchmark for robot learning and planning"
tags: [manipulation, imitation, RL, sim-to-real, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP/IL/RL/FM 四大范式在空间推理、非抓取操控、工具使用、组合几何约束和动态约束五类物理推理挑战上的表现，并展示 TidyBot++ 真实机器人上的 Sim-to-Real 验证"
authors: "Huang, Yixuan; Li, Bowen; Saxena, Vaibhav; Liang, Yichao; Mishra, Utkarsh Aashu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "6IXEFC6X"
---
## 摘要

Robotic systems that interact with the physical world must reason about kinematic and dynamic constraints imposed by their own embodiment（具身）, their environment, and the task at hand. We introduce KinDER, a benchmark for Kinematic and Dynamic Embodied Reasoning that targets physical reasoning challenges arising in robot learning and planning. KinDER comprises 25 procedurally generated environments, a Gymnasium-compatible Python library with parameterized skills and demonstrations, and a standardized evaluation suite with 13 implemented baselines spanning task and motion planning, imitation learning（模仿学习）, reinforcement learning（强化学习）, and foundation-model-based approaches. The environments are designed to isolate five core physical reasoning challenges: basic spatial relations, nonprehensile multi-object manipulation（操控）, tool use, combinatorial geometric constraints, and dynamic constraints, disentangled from perception, language understanding, and application-specific complexity. Empirical evaluation shows that existing methods struggle to solve many of the environments, indicating substantial gaps in current approaches to physical reasoning. We additionally include real-to-sim-to-real（仿真到真实迁移） experiments on a mobile manipulator to assess the correspondence between simulation and real-world physical interaction. KinDER is fully open-sourced and intended to enable systematic comparison across diverse paradigms for advancing physical reasoning in robotics. Website and code: https://prpl-group.com/kinder-site/

## 中文简述

提出基于强化学习的非抓取式操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、强化学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **KinDERGarden**：25 个程序化生成的仿真环境，分为 Kinematic2D（6 个）、Dynamic2D（4 个）、Kinematic3D（5 个）、Dynamic3D（10 个）四类，每个环境有无限变体
2. **KinDERGym**：pip 安装的 Python 包，包含 Gymnasium API、参数化 skills/concepts、多种遥操作接口（键盘/PS5/iPhone/Quest 3S）、预采集演示数据（≥100 demos for 10 envs）
3. **KinDERBench**：标准化 benchmark，在 8 个代表性环境上评测 13 个 baseline（TAMP×1 + RL×3 + IL×4 + FM×4 + MPC×1），多维度指标（SR, Rwd, Inf-Time）
4. **Real-to-Sim-to-Real**：在 TidyBot++ 移动操控平台上验证 Shelf3D 环境的仿真-真实对应性
## 结构化提取

- **Problem**: 机器人物理推理能力缺乏统一评测标准，现有 benchmark 无法将物理推理从感知/语言/领域复杂性中解耦评估
- **Method**: 三层架构 — KinDERGarden（25 个程序化生成环境）+ KinDERGym（Gymnasium 兼容 Python 库）+ KinDERBench（13 baselines 标准化评测）。环境使用 object-centric states，稀疏奖励。3D 环境基于 TidyBot++（Kinova Gen3 7DOF + Robotiq 2F-85），2D 环境使用圆形底盘+伸缩臂
- **Tasks**: 覆盖五大类物理推理 — 空间关系（Rearrange3D/Table3D）、非抓取多物体操控（SweepIntoDrawer3D/ScoopPour3D）、工具使用（StickButton2D/Transport3D/DynPushPullHook2D）、组合几何约束（Shelf3D/Packing3D/ConstrainedCupboard3D）、动态约束（Tossing3D/BalanceBeam3D）
- **Sensors**: Object-centric states（默认）；可选 RGB 图像观测；Real-to-Sim-to-Real 使用顶部摄像头 + 开放词汇检测 [105]
- **Robot Setup**:
- **Metrics**: Success Rate (SR), Cumulative Reward (Rwd), Inference Time (Inf-Time)；5 seeds × 50 episodes
- **Limitations**: 仿真不完整覆盖真实物理；排除随机性/部分可观测/多样形态/多机器人；baseline 数量有限；BP 的工程成本高且未能量化
- **Evidence Notes**: 全文 arXiv HTML 版本完整获取（93,839 字符），包含正文 8 节 + 5 个表格 + 12 个附录表格 + 8 张图。数据直接来自 Table II-V 原始数据。OOD 泛化和 planning scaling 实验提供额外证据。

  - 2D: 圆形底盘（SE(2)）+ 伸缩臂 + 真空吸盘(Kinematic)/双指夹爪(Dynamic)
  - 3D: TidyBot++ 移动底盘 + Kinova Gen3 7DOF 臂 + Robotiq 2F-85 夹爪
  - Real robot: TidyBot++ 全向移动操控平台
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv MCP 获取完整 HTML 全文，含正文、表格、Appendix）
- Evidence Coverage: 完整覆盖 Introduction、Core Challenges、Related Work、KinDERGarden（25 个环境）、KinDERGym（软件栈）、KinDERBench（13 baselines，8 环境评估）、Real-to-Sim-to-Real 实验、Limitations、Appendix 环境细节
- Confidence: high
- Summary: 提出 KinDER benchmark，包含 25 个程序化生成的物理推理环境、Gymnasium 兼容的 Python 库和 13 个 baseline，系统评估 TAMP/IL/RL/FM 四大范式在空间推理、非抓取操控、工具使用、组合几何约束和动态约束五类物理推理挑战上的表现，并展示 TidyBot++ 真实机器人上的 Sim-to-Real 验证


## Problem

机器人与物理世界交互时，必须对自身形态（embodiment）、环境和任务施加的运动学（kinematic）和动力学（dynamic）约束进行推理。然而：
1. **缺乏共识**：物理推理在 TAMP、RL、IL、Foundation Model 等不同子领域中被独立研究，缺乏统一评测标准
2. **现有 benchmark 的局限**：现有 benchmark 要么覆盖广泛的任务多样性但未聚焦物理推理本身，要么聚焦应用场景（家庭辅助等）导致物理推理与感知/语言/领域复杂性纠缠在一起
3. **难以定向评估**：无法将物理推理能力从感知、语言理解和应用复杂性中解耦出来独立测量


## Method

### 五大核心物理推理挑战
1. **Basic Spatial Relations**：理解物体间空间关系（左/右/上/下），被动判断 + 主动实现
2. **Nonprehensile Multi-Object Manipulation**：推、拉、扫、搅等多物体非抓取式操控，利用全臂/全身接触
3. **Tool Use**：使用工具（钩子、棍子、容器、扫帚等）操控其他物体，包括即兴使用
4. **Combinatorial Geometric Constraints**：在紧凑空间中避免碰撞，约束数量随物体数多项式增长
5. **Dynamic Constraints**：控制动态系统满足速度/加速度/倾覆等约束（如不洒水、保持平衡）

### 环境设计
- **Kinematic2D**：纯 Python 实现，无物理引擎。圆形底盘 + 伸缩臂 + 真空吸盘。碰撞即回退。
- **Dynamic2D**：Pymunk 物理引擎。圆形底盘 + 伸缩臂 + 双指夹爪。建模速度和加速度。
- **Kinematic3D**：PyBullet 碰撞检测。TidyBot++ 底盘 + Kinova Gen3 7DOF 臂 + Robotiq 2F-85 夹爪。运动学抓取。
- **Dynamic3D**：MuJoCo 物理引擎。同上机器人。动态抓取（物体不刚性附着）。复用 RoboCasa/MimicLabs 资产。

### 状态表示
- 所有环境使用 **object-centric states**：物体名称 → 特征向量映射
- 支持降级为 RGB 图像观测或固定物体数量的 flattened state
- 稀疏奖励：成功前每步 -1，成功即终止

### 参数化 Skills 和 Concepts
- Skills 实现为 options，关联 PDDL operators 和 samplers
- Concepts 实现为关系谓词 + 分类器，定义两层场景图（scene graph）
- 用于 bilevel planning、LLM/VLM planning baselines


## Experiments

### 评估设置
- 8 个环境 × 13 个 baseline
- 5 random seeds × 50 episodes/seed
- 3 指标：SR（成功率）, Rwd（累积奖励）, Inf-Time（推理时间）

### 主要结果（Table II 均值）

| Environment | Top Method | SR | Key Finding |
|---|---|---|---|
| Motion2D | BP/LLMCon/VLMCon/MPC | ~1.00 | 简单任务所有方法均可行 |
| StickButton2D | BP | 0.99 | 工具使用任务，LLM/VLM 有显著差距 |
| DynObstruction2D | VLA | 0.50 | 动态环境 VLA 意外领先 |
| DynPushPullHook2D | VLA | 0.43 | 唯一取得非平凡 SR 的方法 |
| BaseMotion3D | BP/LLMCon/VLMCon | 1.00 | 简单 3D 任务 |
| Transport3D | BP | 0.46 | 工具+组合约束，仅 planning 方法有效 |
| Shelf3D | BP | 1.00 | 紧凑空间打包，RL/IL 几乎全部失败 |
| SweepIntoDrawer3D | DP | 0.14 | 长视野多阶段任务，所有方法表现差 |

### 平均成功率排名
BP (0.57) > LLMCon = VLMCon (0.43) > LLMPlan = VLMPlan (0.34) > MPC (0.32) > VLA (0.32) > GSC (0.26) > DPES (0.25) > DP (0.24) > PPO (0.13) > MBRL (0.08) > SAC (0.02)

### 关键发现
1. **VLM ≈ LLM**：VLMPlan 和 LLMPlan 表现接近，说明 VLM 未能有效利用 RGB 图像额外信息
2. **In-context examples 重要**：LLMCon/VLMCon (0.43) 显著优于 LLMPlan/VLMPlan (0.34)
3. **VLA 泛化能力强**：VLA 在 2D 动态环境（DynPushPullHook2D）表现出跨域迁移能力
4. **RL 仅在短视野有效**：PPO/SAC 仅在 Motion2D 等简单任务中有非零 SR
5. **DP 在长视野有潜力**：Diffusion Policy 在 SweepIntoDrawer3D 取得 0.14 SR

### OOD 泛化（Table IV）
- DynObstruction2D：训练 1 个障碍物，测试 0/2/3 个
- DP: 0.35/0.30/0.26（从 0.33 逐渐下降）
- VLA: 0.52/0.43/0.40（从 0.50 逐渐下降，VLA 更鲁棒）

### Bilevel Planning 扩展（Table V）
- StickButton2D：1 按钮 SR 0.99 → 5 按钮 SR 0.02 → 10 按钮 SR 0.00
- 推理时间从 1.51s 增长到 38.39s

### Real-to-Sim-to-Real
- 使用 TidyBot++ 移动操控平台
- 通过顶部摄像头定位机器人和物体 → 初始化仿真状态 → 在仿真中生成 plan → 真实世界执行
- 验证了 Shelf3D 环境的仿真-真实对应性


## Limitations

1. **仿真局限性**：真实物理交互的某些方面未被完全捕捉
2. **设计取舍**：排除了随机性（stochasticity）、部分可观测性（partial observability）、多样化机器人形态（diverse embodiments）、多机器人协作（multi-robot coordination）
3. **Baseline 覆盖有限**：仅 13 个 baseline，许多替代方法未被评估
4. **工程成本未量化**：BP 工程成本高（需手动定义 skills/concepts），但这一维度难以定量衡量
5. **动态环境差异**：Kinematic2D/3D 无物理引擎，Dynamic2D/3D 分别用 Pymunk/MuJoCo，物理保真度不同


## Key Takeaways

1. **物理推理是当前机器人方法的共同短板**：即使在剥离感知和语言复杂性后，现有方法在多个环境上 SR 仍然很低
2. **Planning 和 Learning 的互补性**：BP 工程成本高但效果最好，IL（特别是 VLA）泛化能力令人惊讶
3. **对我们研究的启发**：
   - KinDER 的 25 个环境可作为 DLO 操控相关物理推理能力的评测基准
   - Nonprehensile multi-object manipulation 挑战与 DLO 操控中的接触丰富操控直接相关
   - Tool use（钩子、扫帚等工具使用）对 DLO 的工具辅助操控有参考价值
   - VLA 在动态环境中的出色表现提示：预训练 VLA 可能是 DLO 操控的有力候选
4. **开源生态完整**：pip-installable、Gymnasium 兼容、多平台测试、400+ 单元测试，适合作为后续研究的实验平台

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[huang-yixuan|Huang, Yixuan]]
