---
title: "CurricuLLM: Automatic Task Curricula Design for Learning Complex Robot Skills Using Large Language Models"
tags: [VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curriculum（子任务序列+reward+goal distribution）；(2) 代码采样：生成 Python 环境代码；(3) 策略评估+自动修正。在 Fetch-Slide/Push、AntMaze、Berkeley Humanoid 四任务上验证，匹配或超越手动 curriculum，且大幅减少人工设计成本。真实 Berkeley Humanoid 上成功验证行走和转向"
authors: "Ryu, Kanghyun; Liao, Qiayuan; Li, Zhongyu; Delgosha, Payam; Sreenath, Koushil et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "KA3ZI5WH"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于大语言模型的操控方法。

**研究方向**: 视觉-语言模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025，UC Berkeley，4 仿真环境+真实 Berkeley Humanoid 验证，全面对比手动 curriculum 和基线方法
- **Summary**: 提出 CurricuLLM，利用 LLM（GPT-4-turbo）自动生成 RL 任务级 curriculum。三步流程：(1) LLM 基于任务描述和物理参数设计 curriculum（子任务序列+reward+goal distribution）；(2) 代码采样：生成 Python 环境代码；(3) 策略评估+自动修正。在 Fetch-Slide/Push、AntMaze、Berkeley Humanoid 四任务上验证，匹配或超越手动 curriculum，且大幅减少人工设计成本。真实 Berkeley Humanoid 上成功验证行走和转向
## 关键贡献

1. LLM 驱动的 curriculum 自动设计：从任务描述直接生成 curriculum
2. 三步流程：curriculum 设计 → 代码采样 → 策略评估（闭环）
3. 跨平台验证：从平面操控到四足导航到人形机器人
4. 匹配手动设计性能：在多个任务上达到与专家设计相当的 success rate
## 结构化提取

- **Problem**: RL curriculum 设计自动化
- **Method**: CurricuLLM — LLM 设计 curriculum + 代码采样 + 策略评估闭环
- **Tasks**: Fetch-Slide, Fetch-Push, AntMaze, Berkeley Humanoid Walking
- **Sensors**: 关节本体感觉 + 位置/速度观测
- **Robot Setup**: Fetch robot + Ant + Berkeley Humanoid（仿真+真实）
- **Metrics**: 成功率（到达目标/完成任务）
- **Limitations**: 依赖 LLM 质量、未验证接触丰富任务、需 domain randomization
- **Evidence Notes**: 全文读取，Tables I-II 提供仿真和消融对比
## 本地引用关系

- [[garcia2025generalizable]]
- [[karim2024davil]]
- [[liu2025autonomous]]
- [[liu820enhancing]]
- [[patel2025realtosimtoreal]]
## Problem

RL 学习复杂机器人技能需要精心设计的任务 curriculum（从简到难），但手动设计 curriculum 耗时且依赖专家经验。如何自动化 curriculum 设计，使其适应不同任务和机器人平台？


## Method

- **Step 1: Curriculum Design**：
  - 输入：任务描述、环境物理参数（关节范围、速度限制等）、评估标准
  - LLM（GPT-4-turbo）生成子任务序列，每步包含：reward function、goal sampling distribution、success criterion
  - 支持渐进式复杂度：从简单子目标逐步增加难度
- **Step 2: Code Sampling**：
  - LLM 生成 Python 代码定义每个子任务的环境
  - 代码包含：reward shaping、goal sampling、termination condition
  - 自动语法检查和运行验证
- **Step 3: Policy Evaluation**：
  - 在每个子任务上用 RL（PPO/SAC）训练策略
  - 评估当前子任务成功率，决定是否进入下一阶段
  - 失败时 LLM 根据失败日志修改 curriculum
- **Curriculum 类型**：
  - Goal curriculum：逐步扩大目标分布范围
  - Action curriculum：从受限动作空间到完整动作空间
  - Reward curriculum：从 dense reward 到 sparse reward
- **RL 训练细节**：
  - PPO 用于连续控制任务
  - SAC 用于离散动作任务
  - 标准 MLP actor-critic 架构


## Experiments

- **仿真实验**（4 任务）：
  - Fetch-Slide：CurricuLLM 92% vs 手动 90% vs 无 curriculum 45%
  - Fetch-Push：CurricuLLM 88% vs 手动 85% vs 无 curriculum 52%
  - AntMaze (UMaze)：CurricuLLM 80% vs 手动 82% vs 无 curriculum 35%
  - Berkeley Humanoid Walking：CurricuLLM 75% vs 手动 78% vs 无 curriculum 20%
- **真实机器人验证**：
  - Berkeley Humanoid 真实部署：行走和转向成功率 ~70%
  - Sim2Real 使用 domain randomization 桥接
- **消融**：
  - LLM 生成的 reward vs 手动 reward：性能相当
  - 1-shot vs multi-shot curriculum：多步 curriculum 显著优于单步
  - 自动修正 vs 固定 curriculum：自动修正提升 ~10%
- **效率**：Curriculum 设计时间从数小时（手动）降至 ~5 分钟（LLM）


## Limitations

1. 依赖 LLM 质量：生成错误代码或不适 curriculum 可能导致训练失败
2. 未验证超长时序任务（>5 步 curriculum）
3. 仅验证标准 RL 基准任务，未涵盖接触丰富操控
4. 自动修正循环可能增加总训练时间
5. Sim2Real 迁移仍需 domain randomization


## Key Takeaways

- LLM 可有效自动化 curriculum 设计：匹配手动设计性能
- 三步闭环流程（设计→采样→评估）是关键：支持自动修正
- Curriculum 类型需匹配任务特性：不同任务需要不同的渐进策略
- 大幅减少人工设计成本：从数小时降至数分钟
- 跨平台泛化：同一框架适用于操控、导航和运动控制

## 相关概念

- [[vision-language-model]]

## 相关研究者

- [[ryu|Ryu, Kanghyun]]
