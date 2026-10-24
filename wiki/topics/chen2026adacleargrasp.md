---
title: "AdaClearGrasp: Learning adaptive clearing for zero-shot robust dexterous grasping in densely cluttered environments"
tags: [manipulation, VLM, RL, sim-to-real, grasping]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter-Bench分级评测基准"
authors: "Chen, Zixuan; Zhang, Wenquan; Fang, Jing; Zeng, Ruiming; Xu, Zhixuan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "KA457TR9"
---
## 摘要

In densely cluttered environments, physical interference, visual occlusions, and unstable contacts often cause direct dexterous（灵巧） grasping（抓取） to fail, while aggressive singulation strategies may compromise safety. Enabling robots to adaptively decide whether to clear surrounding objects or directly grasp the target is therefore crucial for robust manipulation（操控）. We propose AdaClearGrasp, a closed-loop（闭环） decision-execution framework for adaptive clearing and zero-shot（零样本） dexterous（灵巧） grasping（抓取） in densely cluttered environments. The framework formulates manipulation（操控） as a controllable high-level decision process that determines whether to directly grasp the target or first clear surrounding objects. A pretrained vision-language model（视觉-语言模型） (VLM) interprets visual observations and language task descriptions to reason about grasp interference and generate a high-level planning skeleton, which invokes structured atomic skills through a unified action interface. For dexterous（灵巧） grasping（抓取）, we train a reinforcement learning（强化学习） policy with a relative hand-object distance representation, enabling zero-shot（零样本） generalization across diverse object geometries and physical properties. During execution, visual feedback monitors outcomes and triggers replanning upon failures, forming a closed-loop（闭环） correction mechanism. To evaluate language-conditioned dexterous（灵巧） grasping（抓取） in clutter, we introduce Clutter-Bench, the first simulation benchmark with graded clutter complexity. It includes seven target objects across three clutter levels, yielding 210 task scenarios. We further perform sim-to-real（仿真到真实迁移） experiments on three objects under three clutter levels (18 scenarios). Results demonstrate that AdaClearGrasp significantly improves grasp success rates in densely cluttered environments. For more videos and code, please visit our project website: https://chenzixuan99.github.io/adaclear-grasp.github.io/.

## 中文简述

提出 AdaClearGrasp 分层闭环框架，通过 VLM 语义推理自适应决策清障或直接抓取，结合几何感知 RL 灵巧抓取策略 GeoGrasp 实现零样本跨物体泛化。

**研究方向**: 灵巧抓取、杂乱环境操控、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **AdaClearGrasp 框架**：将杂乱清障建模为自适应高层规划的闭环分层框架，集成 VLM 语义推理、结构化技能调用和失败反馈，将高层决策转化为可执行原子动作
2. **GeoGrasp 策略**：基于手-物体相对距离表示的物体无关 RL 灵巧抓取策略，几何感知设计减少场景过拟合，实现零样本跨物体泛化
3. **Clutter-Bench 基准**：首个带分级难度的标准化仿真评测基准（ManiSkill3），用于评估语言条件下的杂乱场景目标抓取
## 结构化提取

- **Problem**: 密集杂乱场景中的灵巧抓取——如何自适应决定清障策略（何时清、怎么清）vs 直接抓取
- **Method**: 分层 POMDP + VLM (Qwen3-VL-32B) 高层语义规划 + MCP 工具接口 + GeoGrasp (几何感知 RL 策略) 底层执行 + 闭环视觉反馈重规划
- **Tasks**: 语言条件下的杂乱场景目标物体灵巧抓取
- **Sensors**: RGB-D 相机（仿真 128×128，真机 Gemini 336L）；真机使用 FoundationPose 估计 6D 位姿
- **Robot Setup**: xArm7 (7-DOF) + XHand 灵巧手 (12-DOF)；仿真基于 ManiSkill3 (SAPIEN 引擎)
- **Metrics**: Success Rate (SR) — 目标抓取并提升至 ≥15cm 且保持 2 秒不脱落；40 步规划上限视为失败
- **Limitations**: Level-6 真实世界成功率仅 50%；滚动物体/非凸几何困难；依赖位姿估计精度；单平台验证；清障原语为启发式非学习策略
- **Evidence Notes**: 210 仿真场景 + 90 真实世界试验的完整定量结果；3 组消融实验验证清障、闭环、RL 泛化各自贡献；GeoGrasp 在 7 类物体（4 类未见）上的独立泛化评测；附录含 PPO 超参数、关键点定义、域随机化参数、场景生成协议等完整复现细节
## 本地引用关系

- [[chen2026adacleargrasp]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: 完整覆盖方法、实验、消融、附录细节
- Confidence: high
- Summary: 提出分层闭环框架AdaClearGrasp，通过VLM语义推理自适应决策清障或直接抓取，结合几何感知RL灵巧抓取策略GeoGrasp实现零样本跨物体泛化，并引入Clutter-Bench分级评测基准


## Problem

在密集杂乱环境中，直接灵巧抓取常因物理干扰、视觉遮挡和不稳定接触而失败，而激进的分离策略可能危及安全。核心挑战是：机器人如何**自适应地决定**是清除周围障碍物还是直接抓取目标，以在密集杂乱场景中实现稳健的灵巧抓取。

现有方法的不足：
- 纯 RL 方法将操控视为低层控制问题，依赖涌现策略，在密集杂乱中缺乏长时推理和自适应交互
- 现有 VLM 方法要么只处理单物体且开环执行，要么反馈有限且未针对密集杂乱设计
- 缺乏标准化评测基准


## Method

### 整体架构
分层 POMDP 框架，四层闭环：
1. VLM 语义规划器分析场景 → 高层动作计划
2. 通过 MCP (Model Context Protocol) 将计划翻译为参数化原子技能
3. 技能库执行（清障原语 + 恢复原语 + GeoGrasp RL 策略）
4. 视觉反馈监控 → 失败时触发重规划

### VLM 语义规划 (Qwen3-VL-32B-Instruct)
- **观测空间**：RGB 图像 + 检测到的物体文本列表
- **动作空间**：结构化 JSON（action name + args + reason），如 `push(side="left")`
- **反馈机制**：前一步执行反馈（如"stuck detected"）回传 VLM，支持动态策略调整
- **安全约束**：封闭观测空间、有界动作参数、可验证执行反馈

### MCP Server
- 将操控原语封装为模型无关的工具接口（tool interface）
- VLM 生成工具调用 → MCP 解析 → 分发到对应技能执行器
- 支持替换 VLM、扩展技能库、迁移硬件平台，无需修改高层推理逻辑

### 原子技能库
**清障原语**：
- Push/Pull：从指定侧（left/center/right）接近物体，末端执行器偏航角对齐运动方向（+π/6 偏移）
- Move/Lift/Lower：笛卡尔空间精确重定位

**恢复原语**：
- InitArm/InitHand：检测到奇异点或持续碰撞时重置到安全位形

**GeoGrasp RL 策略**：
- 观测空间：59 维（54 维手-物体几何关系 + 1 维目标高度 + 4 维末端执行器状态）
  - 手-物体关系：18 个手关键点到物体点云的单位归一化最近邻向量（每关键点 3 维 × 18 = 54 维）
  - 18 关键点分布：手掌 6 点 + 4 指各 3 点（近/中/远节指骨中心）
  - 物体点云：1024 点均匀采样自网格表面
- 动作空间：19 维连续动作（7 维 xArm 关节 + 12 维 XHand 关节），相对控制，缩放因子 0.05 rad/step
- 网络结构：3 层 MLP [256, 256, 256]
- 训练：PPO，400 并行环境，γ=0.96，batch=800，lr=3e-4，训练 6M 步
- 仅在 3 个物体（Cube, Cup, Apple）上训练，无杂乱环境

### 奖励函数
R_t = R_lift + R_success + R_contact + R_nn - C_action
- R_lift (w=50)：提升高度的稠密奖励
- R_success (w=200)：物体提升 >0.15m 的稀疏奖励
- R_contact (w=10)：手指接触数（力 >0.5N）奖励
- R_nn (w=10)：最近邻距离下降的 shaping 奖励
- C_action (w=0.03)：大动作惩罚

### 域随机化
- 摩擦系数：U[0.5, 2.0]
- 物体质量：±20%
- 点云观测噪声：σ=0.005m 高斯噪声
- 初始关节位置扰动：±0.05 rad

### 闭环执行
每周期 VLM 监控状态 → 目标遮挡时选清障技能 → 清障后调 GeoGrasp → 失败时反馈 VLM 重规划（最多 5 次尝试）→ 循环至目标被抓取提升或达步数上限


## Experiments

### 评测基准：Clutter-Bench
- 基于 ManiSkill3 构建
- 7 个目标物体（YCB）：Cube, Can, Pear, Apple, Mug, Lego, Ball
- 3 个难度级别：Level-1（2 障碍物）、Level-2（4 障碍物）、Level-3（6 障碍物）
- 每组合 10 个预生成场景配置，共 210 个场景
- 物体位置在 20×20 cm² 区域内采样，朝向 U[0°, 360°)
- 物体中心最小初始距离 6cm，物理稳定化后序列化为 JSON

### 主要结果（仿真）

**Table I：Clutter-Bench 成功率对比（10 次独立试验平均）**

| 难度 | AdaClearGrasp | VLM Scaffolding | GeoGrasp (No VLM) | w/o Replan |
|------|--------------|-----------------|-------------------|------------|
| Level-1 (2 obs) | 89% | 6% | 77% | 83% |
| Level-2 (4 obs) | 84% | 0% | 40% | ~60% |
| Level-3 (6 obs) | 76% | 0% | 27% | 41% |

关键发现：
- VLM Scaffolding 在密集场景几乎全部失败（碰撞自由路径不存在）
- 自适应清障在 Level-3 比 No VLM 提升 +49%
- 闭环重规划在 Level-3 比 w/o Replan 提升 +35%

### GeoGrasp 泛化（无杂乱环境）

| 物体 | 已见/未见 | 成功率 |
|------|---------|--------|
| Cube | 已见 | 86.1% |
| Cup | 已见 | 88.9% |
| Apple | 已见 | 100.0% |
| Can | 未见 | 83.3% |
| Pear | 未见 | 72.2% |
| Ball | 未见 | 61.1% |
| LEGO | 未见 | 47.2% |

### 真实世界 Sim-to-Real
- 平台：xArm7 + XHand + Gemini 336L 外部相机 + FoundationPose 6D 位姿估计
- 3 目标 × 3 难度 × 2 场景 × 5 次重复 = 90 次试验
- 总体成功率：70.0%（63/90）
- 按难度：Level-2 = 90%，Level-4 = 70%，Level-6 = 50%
- 按物体：Orange Cube = 80%，其他详见 Table II
- 零样本迁移，无需微调

### 失败分析
- Level-6 主要失败原因：狭窄容错空间 + 位姿估计抖动 + 清障时滑动导致碰撞
- 杯子在清障时被推倒（不可预测接触力）
- Rolling Ball 和非凸 LEGO 仍具挑战


## Limitations

1. 高密度场景（Level-6）成功率仍显著下降（50% real-world），接触不确定性大
2. 滚动物体和非凸几何的成功率偏低（LEGO 47.2%，Ball 61.1%）
3. 真实世界依赖 FoundationPose 位姿估计精度，噪声直接影响规划
4. 仅在单一机器人平台（xArm7 + XHand）验证，跨具身泛化未验证
5. 清障原语基于几何运动规划（启发式），非学习策略，适应性有限
6. GeoGrasp 仅在 3 个物体上训练，更复杂未见物体的泛化边界未探索


## Key Takeaways

1. **VLM + RL 分层架构有效**：将语义推理（VLM 决策何时/如何清障）与底层控制（RL 执行抓取）解耦，比纯 RL 或纯 VLM 方法在密集杂乱中更稳健
2. **几何感知表示是零样本泛化关键**：GeoGrasp 的 18 关键点最近邻向量表示不依赖物体类别/外观，仅关注局部几何关系，3 个训练物体即可泛化到 4 个未见类别
3. **MCP 作为 VLM-机器人接口有启发性**：将操控技能封装为可调用工具接口，实现 VLM 与底层控制的解耦，利于模块化扩展
4. **闭环反馈比初始规划更重要**：消融显示 Level-3 场景中重规划贡献 +35%，说明密集杂乱中单次规划几乎不可能成功
5. **与 DLO 操控的关联**：本文的"自适应决策何时清障"思路可迁移到 DLO 场景——在抓取/操作线缆前先理清缠绕/遮挡。但本文不涉及可变形物体
6. **Clutter-Bench 填补了评测空白**：首个带分级难度的灵巧抓取杂乱基准，标准化配置保证公平对比

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[grasping]]
- [[deformable-linear-object]]

## 相关研究者

- [[chen-zixuan|Chen, Zixuan]]
