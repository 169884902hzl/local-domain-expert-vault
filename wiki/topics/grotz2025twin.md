---
title: "TWIN: Two-handed Intelligent Benchmark for Bimanual Manipulation"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 TWIN 双臂操控基准，扩展 RLBench 至双臂场景，包含 13 个新任务（23 变体），覆盖 prehensile、non-prehensile 和混合操作类型。核心功能是自动生成训练数据而无需人类演示。评估了 ACT、RVT-LF、PerAct-LF 和 PerAct2 四种方法，PerAct-LF 在 128px/100 demos 设置下平均成功率最高（23.3%），但所有方法整体成功率偏低，反映了双臂操控的高复杂度"
authors: "Grotz, Markus; Shridhar, Mohit; Chao, Yu-Wei; Asfour, Tamim; Fox, Dieter"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "J2AXX59R"
---
## 摘要

Bimanual manipulation（双臂操控） is challenging due to precise spatial and temporal coordination required between two arms. While there exist several real-world bimanual（双臂） systems, there is a lack of simulated benchmarks with a large task diversity for systematically studying bimanual（双臂） capabilities across a wide range of tabletop tasks. This paper addresses the gap by presenting a benchmark for bimanual manipulation（双臂操控）. A key functionality is the ability to autonomously generate training data without the necessity of human demonstrations to the robot. We open-source our code and benchmark, which comprises 13 new tasks with 23 unique task variations, each requiring a high degree of coordination and adaptability. To initiate the benchmark, we extended multiple state-of-theart techniques to the domain of bimanual manipulation（双臂操控）. The project website with code is available at: http://bimanual. github.io.

## 中文简述

提出基于学习方法的双臂方法。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、task descriptions (Sec IV)、method (Sec III)、evaluation (Sec V)、tables (I-IV)、figures (1-3)
- **Confidence**: high — 全文完整，ICRA 2025 正式发表，13 个双臂任务 + 23 变体，4 种基线方法系统评估
- **Summary**: 提出 TWIN 双臂操控基准，扩展 RLBench 至双臂场景，包含 13 个新任务（23 变体），覆盖 prehensile、non-prehensile 和混合操作类型。核心功能是自动生成训练数据而无需人类演示。评估了 ACT、RVT-LF、PerAct-LF 和 PerAct2 四种方法，PerAct-LF 在 128px/100 demos 设置下平均成功率最高（23.3%），但所有方法整体成功率偏低，反映了双臂操控的高复杂度
## 关键贡献

1. TWIN 基准：13 个双臂任务（23 变体），基于 RLBench 扩展，保留自动数据生成功能
2. 自动数据生成：无需人类演示，通过 waypoint-based motion planning 自动生成训练数据
3. 任务分类体系：基于双臂分类法（temporal/spatial/physical coupling + symmetric/synchronous coordination）对任务进行系统分类
4. 多基线评估：扩展 PerAct、RVT 和 ACT 至双臂场景
## 结构化提取

- **Problem**: 缺乏系统性双臂操控仿真基准和自动数据生成能力
- **Method**: TWIN — RLBench 扩展 + 13 双臂任务 + 自动数据生成 + 4 种基线
- **Tasks**: 13 个双臂任务（push/lift/pick/handover/rope/sweep/tray 等），23 变体
- **Sensors**: 4×RGB-D 相机 + 机器人本体感觉
- **Robot Setup**: 2×Franka Panda 仿真（Coppeliasim/RLBench）
- **Metrics**: 成功率（0/100 二值，100 episodes/test set）
- **Limitations**: 整体成功率低、无真实实验、对称性问题
- **Evidence Notes**: 全文读取，Table IV 提供完整 13 任务 × 4 方法 × 3 设置的定量结果
## 本地引用关系

- [[chen2025coordinated]]
- [[karim2024davil]]
- [[liu2025autonomous]]
## Problem

双臂操控需要两臂之间精确的时空协调，但缺乏具有大规模任务多样性的仿真基准来系统性研究双臂操控能力。现有基准（robosuite 3 个、ManiSkill2 2 个双臂任务）不足以有意义地评估双臂操控方法。


## Method

- **基准框架**：基于 RLBench 扩展，使用两个 Franka Panda 机器人
- **任务分类**：13 个任务按耦合类型（时间/空间/物理）和协调类型（对称/同步）分类
  - Prehensile：plate pickup、drawer item、fridge bottle、handover、notebook、tray oven
  - Non-prehensile：push box、push buttons、rope straightening、dust sweep
  - Mixed：ball lift、tray lift
- **数据生成**：利用 RLBench 的 waypoint 系统自动生成演示
- **评估方法**：
  - ACT：transformer + action chunking，输出关节角度，不支持语言
  - RVT-LF：两个 RVT 网络 leader-follower 架构
  - PerAct-LF：两个 PerAct 网络 leader-follower 架构（改进版，FP16 加速）
  - PerAct2：单一双臂 PerAct 网络
- **传感器**：4×RGB-D（front、left shoulder、right shoulder、wrist）


## Experiments

- **PerAct-LF (128px, 100 demos)**：平均 23.3%（最高）
  - push box 27%、ball lift 31%、buttons 37%、plate 2%、drawer 94%、fridge 19%
  - notebook 13%、rope 22%、dust 45%、tray 1%、handover easy 4%、oven 8%
- **PerAct2 (128px, 100 demos)**：平均 12.4%
- **ACT (128px, 100 demos)**：平均 10.5%
- **RVT-LF (128px, 100 demos)**：平均 5.2%
- **关键发现**：
  - ACT 因输出关节角度而非 6-DoF pose，对同一机器人模型难以区分左右臂
  - drawer 任务（PerAct-LF 94%）成功率最高，rope/dust 任务相对较好
  - fridge/handover 任务几乎全部失败
  - 增加分辨率（128→256）对 ACT 有帮助但对 PerAct 效果不一


## Limitations

1. 所有方法在大多数任务上成功率偏低，双臂操控复杂性凸显
2. 基于离散动作的方法依赖采样式运动规划器执行
3. ACT 不支持语言指令，无法处理语言条件化任务
4. 仅在仿真中评估，未进行真实机器人实验
5. 任务使用相同型号的两个机器人，对称性区分是挑战


## Key Takeaways

- 双臂操控基准需要覆盖不同类型的协调（时空、物理耦合、对称/同步）
- 自动数据生成是基准可扩展性的关键，避免人类演示瓶颈
- 关节角度预测（ACT）在双臂场景中因对称性问题不如 6-DoF pose 输出
- Leader-follower 架构（PerAct-LF）优于单一双臂网络（PerAct2）在多数任务上
- 当前 SOTA 方法在双臂任务上仍有巨大提升空间

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[grotz|Grotz, Markus]]
- [[fox|Fox, Dieter]]
