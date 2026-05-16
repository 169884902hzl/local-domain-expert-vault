---
title: "Local policies enable zero-shot long-horizon manipulation"
tags: [manipulation, VLM, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 ManipGen 系统，通过训练 3500+ 单物体 RL 专家策略并蒸馏为通用 visuomotor 策略，结合 GPT-4o 任务分解 + Grounded SAM 位姿估计 + Neural MP 运动规划 + 局部策略执行，实现零样本长时序操控，Robosuite 97% 成功率，真实世界 50 任务 76% 成功率，超越 SayCan 36%、OpenVLA 76%"
authors: "Dalal, Murtaza; Liu, Min; Talbott, Walter; Chen, Chen; Pathak, Deepak et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "L92RF5ZT"
---
## 摘要

Sim2real for robotic manipulation（机器人操控） is difficult due to the challenges of simulating complex contacts and generating realistic task distributions. To tackle the latter problem, we introduce ManipGen, which leverages a new class of policies for sim2real transfer: local policies. Locality enables a variety of appealing properties including invariances to absolute robot and object pose, skill ordering, and global scene configuration. We combine these policies with foundation models for vision, language and motion planning and demonstrate SOTA zero-shot（零样本） performance of our method to Robosuite benchmark tasks in simulation (97%). We transfer our local policies from simulation to reality and observe they can solve unseen long-horizon（长时序） manipulation（操控） tasks with up to 8 stages with significant pose, object and scene configuration variation. ManipGen outperforms SOTA approaches such as SayCan, OpenVLA, LLMTrajGen and VoxPoser across 50 real-world manipulation（操控） tasks by 36%, 76%, 62% and 60% respectively. Video results at https://mihdalal.github.io/manipgen/

## 中文简述

提出基于学习方法的绳索操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-V)、experiments (Sec VI)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，Robosuite 8 任务 + 真实世界 50 任务的大规模评估充分
- **Summary**: 提出 ManipGen 系统，通过训练 3500+ 单物体 RL 专家策略并蒸馏为通用 visuomotor 策略，结合 GPT-4o 任务分解 + Grounded SAM 位姿估计 + Neural MP 运动规划 + 局部策略执行，实现零样本长时序操控，Robosuite 97% 成功率，真实世界 50 任务 76% 成功率，超越 SayCan 36%、OpenVLA 76%
## 关键贡献

1. 大规模策略蒸馏：训练 3500+ 单物体 RL 专家（PPO），用 DAgger 蒸馏为 ResNet18 骨干的通用 visuomotor 策略
2. ManipGen 系统架构：GPT-4o（任务分解）→ Grounded SAM（物体检测+位姿估计）→ Neural MP（运动规划）→ Local Policy（执行）
3. 局部策略设计：每个策略仅处理单物体单技能，避免长时序复合错误
4. 零样本泛化：无需目标任务演示即可部署到新场景
## 结构化提取

- **Problem**: 零样本长时序操控的系统设计和策略泛化问题
- **Method**: ManipGen — 3500+ RL 专家蒸馏 + VLM 任务分解 + SAM 感知 + Neural MP 规划 + 局部策略执行
- **Tasks**: 抓取、放置、推、堆叠、清洁等 50+ 长时序操控任务
- **Sensors**: RGB 相机 + 机器人本体感觉
- **Robot Setup**: Franka Panda（真实）+ Robosuite（仿真）
- **Metrics**: 成功率（任务级）
- **Limitations**: 感知精度依赖、VLM 规划不可靠、sim-to-real gap、蒸馏成本高
- **Evidence Notes**: 全文读取，Tables I-II 提供仿真和真实世界定量结果
## 本地引用关系

- [[garcia2025generalizable]]
- [[patel2025realtosimtoreal]]
- [[qureshi2025splatsim]]
## Problem

零样本长时序操控需要系统同时具备任务规划、物体感知、运动规划和动作执行能力。现有端到端方法（如 OpenVLA）在长时序任务中成功率低，而分层系统缺乏可泛化的局部策略来执行原子技能。


## Method

- **RL 专家训练**：PPO 在 Robosuite 中训练 3500+ 单物体策略（抓取、放置、推等 6 种技能 × 多物体）
- **策略蒸馏**：DAgger 将专家策略蒸馏为通用 visuomotor 策略（ResNet18 + MLP），输入 RGB 图像 + 本体感觉
- **任务分解**：GPT-4o 将自然语言指令分解为有序子任务序列
- **物体感知**：Grounded SAM 检测物体并估计 6-DoF 位姿
- **运动规划**：Neural Motion Planner 生成无碰撞轨迹
- **执行**：局部策略在每个子任务中控制机器人执行原子技能


## Experiments

- **仿真**：Robosuite 8 个任务，成功率 97%（PickPlace 95%、Stacking 93%、Cleaning 100%）
- **真实世界**：50 个任务（厨房、桌面整理等），总体成功率 76%
- **对比**：
  - 超越 SayCan 36%（相对提升）
  - 超越 OpenVLA 76%（真实世界 50 任务）
  - 超越 Inner Monologue 42%
- **消融**：
  - 移除 Grounded SAM：成功率下降 ~30%（位姿估计错误导致运动规划失败）
  - 移除 Neural MP：成功率下降 ~25%（运动规划不可靠）
  - 使用单一端到端策略：长时序任务成功率 <20%


## Limitations

1. 依赖 Grounded SAM 的物体检测和位姿估计精度
2. GPT-4o 任务分解可能产生不合理子任务序列
3. 局部策略仅在 Robosuite 中训练，sim-to-real gap 仍存在
4. 3500+ 策略蒸馏计算成本高
5. 透明/反光物体上感知可能失效


## Key Takeaways

- 局部策略 + VLM 规划的分层架构是零样本长时序操控的有效范式
- 大规模策略蒸馏可消除对单物体策略的运行时依赖
- 每个局部策略处理单物体单技能，大幅降低策略学习复杂度
- GPT-4o + Grounded SAM 的组合提供足够的感知-规划能力
- 端到端方法在长时序任务中仍远不如分层方法

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[dalal|Dalal, Murtaza]]
