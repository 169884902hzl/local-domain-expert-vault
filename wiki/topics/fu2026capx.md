---
title: "CaP-X: A framework for benchmarking and improving coding agents for robot manipulation"
tags: [manipulation, VLM, RL, sim-to-real, robot-learning]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出 CaP-X 框架，包含 CaP-Gym（交互式编码环境，187 个任务）、CaP-Bench（8 个层级系统评估 12 个前沿模型）、CaP-Agent0（无需训练的 agentic 框架，集成视觉差分、自动技能库合成和并行推理）和 CaP-RL（GRPO 后训练编码 agent），在仿真和真实机器人上达到接近人类专家水平的操控成功率。"
authors: "Fu, Max; Yu, Justin; El-Refai, Karim; Kou, Ethan; Xue, Haoru et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "2WN8WV6R"
---
## 摘要

"Code-as-Policy" considers how executable code can complement data-intensive Vision-Language-Action (VLA) methods, yet their effectiveness as autonomous controllers for embodied manipulation（操控） remains underexplored. We present CaP-X, an open-access framework for systematically studying Code-as-Policy agents in robot manipulation（机器人操控）. At its core is CaP-Gym, an interactive environment in which agents control robots by synthesizing and executing programs that compose perception and control primitives. Building on this foundation, CaP-Bench evaluates frontier language and vision-language models across varying levels of abstraction, interaction, and perceptual grounding. Across 12 models, CaP-Bench reveals a consistent trend: performance improves with human-crafted abstractions but degrades as these priors are removed, exposing a dependence on designer scaffolding. At the same time, we observe that this gap can be mitigated through scaling agentic test-time computation--through multi-turn interaction, structured execution feedback, visual differencing, automatic skill synthesis, and ensembled reasoning--substantially improves robustness even when agents operate over low-level primitives. These findings allow us to derive CaP-Agent0, a training-free framework that recovers human-level reliability on several manipulation（操控） tasks in simulation and on real embodiments. We further introduce CaP-RL, showing reinforcement learning（强化学习） with verifiable rewards improves success rates and transfers from sim2real with minimal gap. Together, CaP-X provides a principled, open-access platform for advancing embodied coding agents.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **CaP-Gym**：统一的交互式机器人编码环境，集成 RoboSuite、LIBERO-PRO 和 BEHAVIOR 三大仿真器，覆盖 187 个任务，同时兼容仿真和真实机器人系统。
2. **CaP-Bench**：系统性基准，设计 8 个评估层级（S1-S4 单轮、M1-M4 多轮），沿三个轴变化：抽象层级（高级→低级原语）、时间交互（单轮→多轮）、感知接地（文本→多模态→视觉差分），评估 12 个前沿（V）LM。
3. **CaP-Agent0**：无需训练的 agentic 框架，通过三个关键组件弥补 CaP-Bench 发现的缺陷：多轮视觉差分（VDM）、自动合成任务无关技能库、并行推理（多模型集成）。
4. **CaP-RL**：将 RLVR（带可验证奖励的强化学习）直接应用于编码 agent，使用 GRPO 后训练 Qwen2.5-Coder-7B，实现 Sim-to-Real 最小迁移差距。
## 结构化提取

- **Problem**: 系统性评估和改进 Code-as-Policy agent 在机器人操控中的表现，量化人类脚手架对 agent 性能的贡献，探索无需训练的 agentic 基础设施能否恢复接近人类水平的可靠性
- **Method**: 分层编码环境 CaP-Gym（Gymnasium 接口 + REPL）→ 8 层级基准 CaP-Bench（抽象×时间×感知）→ 无训练 agentic 框架 CaP-Agent0（VDM + 技能库 + 并行推理）→ GRPO 后训练 CaP-RL
- **Tasks**: Cube Lift, Cube Stack, Spill Wipe, Peg Insertion, Cube Re-stack, Two-Arm Lift, Two-Arm Handover（仿真 7 核心）；LIBERO-PRO 30 任务（桌面）；BEHAVIOR 2 任务（移动操控：Pick up Radio, Pick up Soda Can）；真实世界 6+ 任务
- **Sensors**: RGB-D 相机；SAM3 语言条件分割；Molmo 2 开放词汇指向；仿真特权状态（mask + object poses）
- **Robot Setup**: 仿真：RoboSuite（单臂桌面）、LIBERO-PRO（单臂桌面）、BEHAVIOR（R1Pro 轮式人形移动操控）；真实：Franka Emika Panda（单臂桌面）、AgiBot G1（双臂人形）
- **Metrics**: Task Success Rate（Zero-Shot Pass@1，100 trials/task）、Navigation Success Rate（<1m 距离）、Code Execution Success Rate
- **Limitations**: 接触密集任务（插入/倒液）仍脆弱；RL 仅在 3 个 S1 任务上训练；技能库单轮合成；依赖 IK 插值而非优化控制；Zero-Shot Pass@1 不允许重置重试
- **Evidence Notes**: 全文 185K 字符已完整阅读；关键实验数据来自 Table 2-4 和 Figure 3-8；CaP-Agent0 消融实验（Figure 8）验证了三个组件各自的贡献；CaP-RL Sim-to-Real 结果来自 Table 4，真实世界仅评估 Cube Lift 和 Cube Stack 两个任务
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high
- Confidence: high
- Summary: 提出 CaP-X 框架，包含 CaP-Gym（交互式编码环境，187 个任务）、CaP-Bench（8 个层级系统评估 12 个前沿模型）、CaP-Agent0（无需训练的 agentic 框架，集成视觉差分、自动技能库合成和并行推理）和 CaP-RL（GRPO 后训练编码 agent），在仿真和真实机器人上达到接近人类专家水平的操控成功率。


## Problem

当前 Code-as-Policy（CaP）方法在机器人操控中的应用存在三个关键问题：

1. **人类先验依赖不明**：已有 CaP 方法主要依赖人类设计的高级原语（如 `stack_objs_in_order()`），无法区分性能提升来自 agent 自身推理能力还是人类脚手架提供的简化。
2. **缺乏系统性基准**：没有跨不同抽象层级、交互模式和感知接地方式的统一评估框架来量化编码 agent 在机器人控制中的表现。
3. **VLA 与程序化控制的鸿沟**：VLA 模型需要大量数据、缺乏可解释性、难以跨具身迁移；经典控制可解释但依赖人工设计，难以扩展到开放环境。


## Method

### CaP-Gym 架构
- 基于 Gymnasium 接口的分层控制框架
- 低层环境循环（物理仿真器或真实世界）+ 有状态 Code Executor 循环（REPL）
- 单个代码环境"回合"对应一次生成程序的完整执行，可触发多个底层仿真步
- **感知原语**：SAM3（语言条件分割）、Molmo 2（开放词汇指向）、OpenCV、Open3D
- **控制原语**：运动规划器、逆运动学求解器（PyRoki），支持碰撞检测、可达性约束

### CaP-Bench 层级设计
- **S1**：高级原语 + 特权状态（无噪声）
- **S2**：高级原语 + 真实感知（RGB-D）
- **S3**：低级原语 + 使用示例
- **S4**：低级原语，无示例
- **M1**：多轮 + 文本反馈（stdout/stderr）
- **M2**：多轮 + 直接 RGB 图像反馈
- **M3**：多轮 + 视觉差分模块（VDM，视觉→结构化文本）
- **M4**：低级原语 + VDM + 使用示例

### CaP-Agent0 三大组件
1. **视觉差分模块（VDM）**：将视觉观察转换为结构化自然语言描述，避免跨模态对齐问题
2. **自动技能库**：从成功执行轨迹中提取可复用函数，经 LLM 分析识别高频任务无关逻辑，合成为 9 个持久化技能函数
3. **并行推理**：每回合并发采样候选方案（单模型 9 次查询 或 3×3 多模型），中心 agent 综合为最终代码

### CaP-RL
- 在 CaP-Gym 上对编码 agent 进行 GRPO 后训练
- 基模型：Qwen2.5-Coder-7B-Instruct
- 训练任务：Cube Lift、Cube Stack、Spill Wipe
- 使用特权状态 API（S1 层级）确保奖励信号稳定


## Experiments

### CaP-Bench 核心发现

**Takeaway 1**：单轮零样本设置下，所有前沿模型均未达到人类专家水平。闭源模型一致优于开源模型，更新架构表现更强。

**Takeaway 2**：高级抽象提升性能但限制表达力。S4→S1 单调递增的成功率表明人类先验显著简化了搜索空间，但也掩盖了低层推理的缺陷。

**Takeaway 3**：闭环多轮交互 + 视觉接地显著改善性能。
- M1（文本反馈）> S2（单轮）
- M2（直接图像）反而降低性能（跨模态对齐鸿沟）
- M3（VDM 文本化视觉差分）一致优于 M1 和 M2
- M4（低级原语 + VDM + 多轮）可达到甚至超过 M3（高级 + 多轮）水平

### CaP-Agent0 结果

**CaP-Bench 7 任务**：在 100 次试验/任务上，4/7 任务达到或超越人类专家水平。

**LIBERO-PRO（30 个任务）**：

| 方法 | libero-object Pos | Task | libero-goal Pos | Task | libero-spatial Pos | Task |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| OpenVLA | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| π₀ | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| π₀.₅ | 0.17 | 0.01 | 0.38 | 0.00 | 0.20 | 0.01 |
| CaP-Agent0 | **0.22** | **0.18** | **0.26** | **0.17** | **0.12** | **0.14** |

CaP-Agent0 在指令扰动（Task）下显著优于 VLA 方法，因为 VLA 依赖训练数据中的指令分布。

**BEHAVIOR（2 个长时距移动操控任务）**：

| 任务 | 导航成功率 | | 任务成功率 | |
|------|:---:|:---:|:---:|:---:|
| | Human | CaP-Agent0 | Human | CaP-Agent0 |
| Pick up Radio | 88% | 80% | 36% | 56% |
| Pick up Soda Can | 80% | 84% | 72% | 72% |

### CaP-RL 结果

| 方法 | Cube Lift (Sim) | Cube Stack (Sim) | Spill Wipe (Sim) | Cube Lift (Real) | Cube Stack (Real) |
|------|:---:|:---:|:---:|:---:|:---:|
| Human Expert | 93% | 73% | 100% | 92% | 84% |
| Qwen 2.5 Coder 7B (base) | 25% | 4% | 30% | 24% | 12% |
| Qwen w/ CaP-RL | **80%** | **44%** | **93%** | **84%** | **76%** |

- Sim-to-Real 迁移几乎无性能损失（Cube Lift: 80%→84%，Cube Stack: 44%→76%）
- 关键原因：agent 推理的是抽象感知 API 而非原始视觉特征

### 真实世界演示
- 在 Franka Emika Panda 和 AgiBot G1 上零样本执行复杂任务
- 展示机械搜索、数学推理、物理常识堆叠、人在回路纠正等能力
- 无需任务特定训练数据或跨具身大幅修改


## Limitations

1. **接触密集任务仍脆弱**：对需要紧密视觉伺服和连续反馈的行为（如精密插入、倒液），程序化控制表现不佳。
2. **RL 训练范围有限**：仅在 3 个任务上用特权状态 API（S1）进行 GRPO 后训练，未在噪声感知（S2）下训练。
3. **技能库合成非迭代**：当前仅单轮合成，未来可迭代精炼和修剪。
4. **低层原语仍依赖 IK 插值**：作者指出直接关节空间插值可能次优，应引入优化控制原语处理碰撞和约束。
5. **评估协议局限**：Zero-Shot Pass@1 协议下每任务实例仅允许一次连续交互，不允许环境重置重试。


## Key Takeaways

1. **视觉差分（文本接地）远优于直接图像输入**：对 VLM-based 控制设计有重要启示——将视觉信息结构化为文本描述比直接输入原始图像更有效，这值得在 DLO 操控的视觉反馈设计中借鉴。
2. **多轮交互是鲁棒性的关键**：agent 通过迭代调试、状态自检和错误恢复，在低级原语上也能达到高级原语的表现。DLO 操控中状态估计不确定性强，多轮闭环尤为重要。
3. **自动技能库弥合抽象鸿沟**：从成功执行中自动合成可复用函数，提供了一种介于人工抽象和原子原语之间的可扩展中间方案。
4. **Sim-to-Real 迁移差距极小**：CaP-RL 通过在抽象感知 API 层面推理（而非原始像素），实现了近乎零损失的 Sim-to-Real 迁移，这对 DLO 操控的 Sim-to-Real 方法有参考价值。
5. **CaP 与 VLA 互补**：论文指出混合 CaP-VLA 策略（coding agent 管理高层逻辑，VLA 执行低层动作）是有前景的方向。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[fu-max|Fu, Max]]
