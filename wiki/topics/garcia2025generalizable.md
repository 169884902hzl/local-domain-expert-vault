---
title: "Towards Generalizable Vision-Language Robotic Manipulation: A Benchmark and LLM-Guided 3D Policy"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任务规划 + VLM 物体定位 + 3D-LOTUS 运动控制，在 GemBench Level 2-4 上大幅超越现有方法，Level 4 从 ~0% 提升至 17.4%"
authors: "Garcia, Ricardo; Chen, Shizhe; Schmid, Cordelia"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "W3Y9ZAPY"
---
## 摘要

Generalizing language-conditioned robotic policies to new tasks remains a significant challenge, hampered by the lack of suitable simulation benchmarks. In this paper, we address this gap by introducing GemBench, a novel benchmark to assess generalization capabilities of vision-language robotic manipulation（机器人操控） policies. GemBench incorporates seven general action primitives and four levels of generalization, spanning novel placements, rigid and articulated objects, and complex long-horizon（长时序） tasks. We evaluate state-of-the-art（现有最优方法） approaches on GemBench and also introduce a new method. Our approach 3D-LOTUS leverages rich 3D information for action prediction conditioned on language. While 3D-LOTUS excels in both efficiency and performance on seen tasks, it struggles with novel tasks. To address this, we present 3D-LOTUS++, a framework that integrates 3D-LOTUS’s motion planning capabilities with the task planning capabilities of LLMs and the object grounding accuracy of VLMs. 3D-LOTUS++ achieves state-of-the-art（现有最优方法） performance on novel tasks of GemBench, setting a new standard for generalization in robotic manipulation（机器人操控）. Code, dataset, real robot videos and trained models are available at https: //www.di.ens.fr/willow/research/gembench/.

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、GemBench (Sec III)、method (Sec IV)、experiments (Sec V)、tables (I-V)、figures (1-3)
- **Confidence**: high — 全文完整，ICRA 2025 正式发表，GemBench 4 级泛化基准 + 3D-LOTUS/3D-LOTUS++ 方法 + 真实机器人验证
- **Summary**: 提出 GemBench 基准（7 种动作技能 × 4 级泛化）和 3D-LOTUS 策略（PTV3 骨干 + 分类式动作预测），增强版 3D-LOTUS++ 集成 LLM 任务规划 + VLM 物体定位 + 3D-LOTUS 运动控制，在 GemBench Level 2-4 上大幅超越现有方法，Level 4 从 ~0% 提升至 17.4%
## 关键贡献

1. GemBench 基准：16 训练任务（31 变体）+ 44 测试任务（92 变体），4 级泛化（新位置/新刚性物体/新关节物体/长时序任务）
2. 3D-LOTUS：PTV3 点云骨干 + cross-attention 语言条件 + 分类式动作预测（优于回归）
3. 3D-LOTUS++：LLM（LLaMa3-8B）任务规划 + VLM（OWLv2+SAM）物体定位 + 3D-LOTUS 运动控制
4. 系统消融揭示：物体定位是 Level 1-2 瓶颈，运动控制是 Level 3-4 瓶颈
## 结构化提取

- **Problem**: 视觉-语言操控策略泛化能力评估和方法不足
- **Method**: GemBench 基准 + 3D-LOTUS（PTV3+分类动作）+ 3D-LOTUS++（LLM+VLM+3D策略）
- **Tasks**: 7 种动作技能（press/pick/push/screw/close/open/stack），4 级泛化
- **Sensors**: 4×RGB-D 相机 + 机器人本体感觉
- **Robot Setup**: RLBench 仿真（Franka）+ UR5 真实机器人
- **Metrics**: 成功率（20 episodes × 5 seeds）
- **Limitations**: LLM 无视觉、物体混淆、长时序成功率低
- **Evidence Notes**: 全文读取，Tables II-V 提供完整定量和消融结果
## 本地引用关系

- [[dey2025revla]]
- [[tang2025kalie]]
## Problem

视觉-语言机器人操控策略在未见任务上的泛化能力差，且缺乏系统性基准来评估泛化能力。现有基准（RLBench、VIMA-Bench、Colosseum）主要评估已见任务性能或环境扰动，不评估向全新任务的泛化。


## Method

- **3D-LOTUS**：
  - 点云预处理：多视角 RGB-D→统一点云→1cm³ 体素下采样→排除机械臂点
  - 骨干：PTV3（U-Net 架构 + transformer 层），cross-attention 融合语言
  - 动作预测：分类式（每轴 30 bins × 1cm，旋转 72 bins × 5°），优于回归
  - 训练：150k iterations，11h/A100
- **3D-LOTUS++**：
  - LLM 任务规划：LLaMa3-8B 分解指令为 6 种原子动作序列
  - VLM 物体定位：OWLv2 检测 + SAM 分割 → 3D 点云 + 语义嵌入
  - 运动控制：3D-LOTUS 修改版（点特征改为物体标签编码 + 时间索引 + 停止预测）


## Experiments

- **RLBench-18Task**：3D-LOTUS 83.1%（SOTA，2.22 V100 GPU days vs RVT-2 6.6）
- **GemBench**：
  - Level 1（新位置）：3D-LOTUS 94.3%（最优）
  - Level 2（新物体）：3D-LOTUS++ 64.5%（vs 3D-LOTUS 49.9%）
  - Level 3（新关节物体）：3D-LOTUS++ 41.5%（vs 3D-LOTUS 38.1%）
  - Level 4（长时序）：3D-LOTUS++ 17.4%（vs 所有其他 ~0%）
- **真实机器人**：seen 8.1/10，unseen 3D-LOTUS++ 7.9/10
- **消融**：分类>回归，cross-attention>adaptive norm；物体定位是主要瓶颈


## Limitations

1. LLM 无视觉输入，可能在长时序任务中产生错误规划
2. 零样本物体定位（OWLv2+SAM）在相似物体间混淆（如 tuna/soup can）
3. Level 4 长时序任务成功率仍低（17.4%）
4. 3D-LOTUS++ 在 Level 1 上不如端到端 3D-LOTUS
5. 运动控制在偏离训练数据配置时泛化差


## Key Takeaways

- 分类式动作预测比回归式更适合离散化的操控动作空间
- 模块化架构（LLM 规划 + VLM 定位 + 3D 策略控制）是泛化操控的有效范式
- 物体定位（而非策略）是新物体泛化的主要瓶颈
- GemBench 揭示现有方法在长时序泛化上近乎完全失效（~0%）
- 3D 点云表示 + PTV3 骨干是当前最高效的 3D 策略架构

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]

## 相关研究者

- [[garcia|Garcia, Ricardo]]
- [[chen|Chen, Shizhe]]
- [[schmid|Schmid, Cordelia]]
