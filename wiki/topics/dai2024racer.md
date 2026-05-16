---
title: "RACER: Rich language-guided failure recovery policies for imitation learning"
tags: [manipulation, imitation, VLM, robot-learning]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GPT-4-turbo 标注丰富语言。在 18 个 RLBench 任务上 70.2% 成功率（vs RVT 62.9%），真实世界 Franka 72.5%（vs RVT 25%）。"
authors: "Dai, Yinpei; Lee, Jayjun; Fazeli, Nima; Chai, Joyce"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "YHME4NNK"
---
## 摘要

Developing robust and correctable visuomotor policies for robotic manipulation（机器人操控） is challenging due to the lack of self-recovery mechanisms from failures and the limitations of simple language instructions in guiding robot actions. To address these issues, we propose a scalable data generation pipeline that automatically augments expert demonstrations with failure recovery trajectories and fine-grained language annotations for training. We then introduce Rich languAge-guided failure reCovERy (RACER), a supervisor-actor framework, which combines failure recovery data with rich language descriptions to enhance robot control. RACER features a vision-language model（视觉-语言模型） (VLM) that acts as an online supervisor, providing detailed language guidance for error correction and task execution, and a language-conditioned visuomotor policy as an actor to predict the next actions. Our experimental results show that RACER outperforms the state-of-the-art（现有最优方法） Robotic View Transformer (RVT) on RLbench across various evaluation settings, including standard long-horizon（长时序） tasks, dynamic goal-change tasks and zero-shot（零样本） unseen tasks, achieving superior performance in both simulated and real world environments. Videos and code are available at: https://rich-language-failure-recovery.github.io.

## 中文简述

提出基于模仿学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习

## 关键贡献

1. **首个探索 rich language 在机器人操控失败恢复中的作用的工作**：证明丰富语言（包含失败分析、空间运动描述、预期结果）比简单指令更有效。
2. **可扩展的数据增强管线**：自动从专家演示中生成失败恢复轨迹（10,159 条），GPT-4-turbo 标注丰富语言指令，无需人工干预。
3. **RACER supervisor-actor 框架**：VLM（LLaVA-Next-8B）作为在线监督员分析场景并生成丰富指令，RVT（替换 T5-11B 编码器）作为 actor 执行动作。
4. **多维度验证**：标准多任务、动态目标切换、零样本未见任务、真实世界 few-shot sim-to-real。
## 结构化提取

- **Problem**: IL 训练的 visuomotor policy 缺乏自恢复能力，仅从成功轨迹学习。现有语言引导方法使用简单指令不足以指导纠正失败。需要自动化的失败恢复和丰富语言指导。
- **Method**: 数据增强管线（关键帧扰动 + GPT-4-turbo 丰富语言标注）+ RACER supervisor-actor 框架（LLaVA-Next-8B VLM 监督员 + T5-11B 增强的 RVT actor）。VLM 每步分析场景生成丰富指令，actor 基于视觉+语言预测 9-DoF waypoint 动作。
- **Tasks**: 18 RLBench 多任务（标准评估 + 目标切换 + 零样本未见任务）；真实世界 4 任务（Open Drawer / Place Fruits / Push Buttons / Put Item on Shelf）。
- **Sensors**: 4 个 RGB-D 相机（前/左肩/右肩/手腕），VLM 仅用前视角 RGB，RVT 用所有视角点云。真实世界：RealSense D455 前视角。
- **Robot Setup**: 仿真 RLBench（Franka）；真实 Franka Emika Panda 7-DoF + 固定 RealSense D455。
- **Metrics**: 成功率（%）、平均排名、目标切换成功率、零样本未见任务成功率、语言丰富度（句子长度/语义角色/标签数）、人工干预率。
- **Limitations**: 依赖专家演示+启发式关键帧提取；仅支持稀疏 waypoint 预测；VLM 指令质量未独立评估；未在 DLO/长时序/多机器人场景验证；真实数据量小（60 demo/4 任务）；未报告推理延迟。
- **Evidence Notes**: 仿真 18 任务 5 seeds 有均值±标准差（Tab I），消融充分（语言类型×失败恢复，Fig 4），目标切换和零样本实验设计新颖（Tab III）。真实世界 4 任务 40 episodes（Tab IV），RACER vs 5 种消融对比充分。语言丰富度量化分析可信（Tab II）。VLM 生成指令质量无独立评估是主要缺失。整体证据强度：仿真强，真实世界中等。
## 本地引用关系

- [[brohan2023rt2]]
## 证据元数据

- **Zotero Key**: YHME4NNK
- **Citekey**: dai2024racer
- **Authors**: Dai Yinpei, Lee Jayjun, Fazeli Nima, Chai Joyce
- **Affiliation**: University of Michigan, CSE + Robotics Departments
- **Venue**: arXiv preprint, 2024-09 (CoRL投稿)
- **Paper Type**: Methods paper (failure recovery + language-guided policy)
- **Fulltext Quality**: Complete, 7 pages with tables, figures, and detailed experiments
- **Evidence Coverage**: High for simulation experiments (18 tasks, 5 seeds, ablations); High for real-world (4 tasks, ablations); Medium for VLM supervisor quality (no human evaluation of instruction quality)
- **Confidence**: High on main results (quantitative tables with variance); Medium on VLM instruction quality (no separate evaluation metric)
- **Summary**: 提出 RACER 框架，VLM 在线监督员提供丰富语言指令指导 visuomotor policy 从失败中恢复。通过自动数据增强管线生成 10,159 条失败恢复轨迹，GPT-4-turbo 标注丰富语言。在 18 个 RLBench 任务上 70.2% 成功率（vs RVT 62.9%），真实世界 Franka 72.5%（vs RVT 25%）。


## Problem

Imitation learning 训练的 visuomotor policy 仅从成功轨迹学习，缺乏自恢复能力。在线失败时无法自动纠正，而人工干预代价高。现有语言引导方法（如 OLAF、RT-H、YAY Robot）只使用简单语言指令（动词+名词），不足以描述失败原因和空间纠正细节。需要一种能自动生成丰富语言指导的失败恢复机制。


## Method

### 数据增强管线（Sec III-B）
1. **失败定义**：关键帧处注入截断高斯噪声，分为 recoverable failure（可用专家动作纠正）和 catastrophic failure（需场景重置）
2. **关键帧识别**：基于夹爪状态、位置变化、时间步启发式规则识别 alignment/grasping/releasing 关键帧
3. **恢复策略**：alignment 失败用 one-step recovery（直接重用专家动作）；grasping/releasing 失败用 two-step recovery（先中间过渡动作再恢复）
4. **语言标注**：GPT-4-turbo 输入任务描述 + GT 物体位置 + 失败类型 + 启发式运动描述 → 输出连贯自然语言指令
5. **数据量**：2250 专家演示 × 5 次扰动 → 过滤后 10,159 条丰富语言标注轨迹

### RACER 框架（Sec III-C）
1. **Supervisor（VLM）**：LLaVA-Next-8B + LoRA（rank 128, α=256），输入前视角 RGB + 任务目标 + 上一条指令 + 机器人状态描述（模板化运动变化）→ 输出下一步丰富指令
2. **Actor（Visuomotor Policy）**：修改版 RVT，CLIP 替换为 T5-11B 增强语言理解，移除时间步本体感受输入以增强语言可控性
3. **语言输入格式**："Task goal: {goal}. Current instruction: {rich instruction}"
4. **在线推理**：每步 VLM 分析场景 → 生成指令 → RVT 执行动作

### 训练细节
- Supervisor：LoRA 微调 2 epochs，deepspeed zero2，batch 64，lr 2e-5
- Actor：LAMB optimizer，18 epochs，batch 48，lr 1.5e-3
- 硬件：8× A40 40GB，总计 ~30 小时


## Experiments

### 仿真：18 RLBench 任务多任务性能（Tab I）
| 模型 | 平均成功率 | 平均排名 |
|------|----------|---------|
| PerAct | 49.4% | 3.7 |
| RVT | 62.9% | 2.2 |
| Act3D | 65.0% | 2.2 |
| RACER | **70.2%** | **1.6** |
| RACER+H | **80.1%** | – |

- RACER+H 允许人工干预，仅 24% 步骤需要干预

### 语言丰富度消融（Fig 4）
- 无指令 → 简单指令 → 丰富指令：性能持续提升
- 失败恢复数据在所有语言设置下提升约 2%
- 丰富指令训练的策略在测试时用简单指令仍然优于简单训练+简单测试（66.31%→69.94%）

### 目标切换（Tab III 上）
| 模型 | 平均成功率 |
|------|----------|
| RVT | 9.0% |
| RACER | **60.0%** |

### 零样本未见任务（Tab III 下）
| 模型 | 平均成功率 |
|------|----------|
| RVT | 16.0% |
| RACER | **47.0%** |

### 真实世界：Franka Panda 4 任务（Tab IV）
| 模型 | 平均成功率 |
|------|----------|
| RVT | 25.0% |
| RACER (scratch) | 32.5% |
| RACER (w/o FA) | 62.5% |
| RACER | **72.5%** |

- RACER w/o FA = 有丰富指令但无失败分析部分
- 从 25% 到 72.5% 的提升证明了丰富语言 + 失败恢复数据在 sim-to-real 中的关键作用
- 60 条人工 demo（每任务 15 条），3 次扰动增强

### 语言丰富度对比（Tab II）
| 数据集 | 平均长度 | 语义角色数 | 唯一标签数 |
|--------|---------|----------|----------|
| RT-H | 4.52 | 1.06 | 2.26 |
| YAY | 4.73 | 1.04 | 3.79 |
| Ours (simple) | 4.38 | 1.06 | 2.69 |
| Ours (rich) | 18.28 | 3.64 | 8.31 |


## Limitations

1. **依赖专家演示进行数据增强**：关键帧提取和扰动策略基于启发式规则，需要已有专家轨迹，无法从零开始生成失败数据。
2. **仅支持稀疏关键帧预测**：使用 waypoint-based policy（RVT），不支持密集连续控制（如 Diffusion Policy），限制了精细操控任务。
3. **VLM 指令质量未独立评估**：未设计指标量化 VLM 生成指令的准确性、相关性或信息量，仅通过端到端成功率间接验证。
4. **语言训练范式仅限于 RLBench 物体操控**：未在 DLO 操控、长时序任务、或多机器人协作等场景验证。
5. **真实世界数据量小**：仅 60 条 demo（每任务 15 条），4 个任务，未报告统计显著性。
6. **推理延迟**：每步需要 VLM 推理 + RVT 推理，实时性受限，未报告推理时间。


## Key Takeaways

1. **丰富语言是失败恢复的关键**：简单指令（"move left"）vs 丰富指令（"The robot overshot to the right. Correct by moving slightly left, then align above the jar lid."）导致成功率差异显著。丰富语言包含失败分析+空间运动+预期结果三要素，比简单指令提供更多可操作信息。
2. **VLM 作为在线监督员是新范式**：无需人工在线干预，VLM 自动分析失败并生成纠正指令，实现自主失败恢复。与 [[brohan2023rt2]]（RT-2）的端到端 VLA 和 [[shi2024yay]]（YAY Robot）的人工干预形成对比。
3. **丰富语言训练有正则化效果**：真实世界中，简单/无指令训练的策略出现严重过拟合（在不同任务间重复相同行为），而丰富语言训练防止过拟合，提高 sim-to-real 泛化。
4. **对本研究方向的启示**：双臂 DLO 操控中失败频繁（如夹取失败、缠绕），RACER 的 VLM 监督员模式可用于自动检测和纠正 DLO 操控中的失败。丰富语言描述对于理解 DLO 状态变化（如"绳索从夹爪中滑出"）比简单指令更有价值。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[dai|Dai, Yinpei]]
