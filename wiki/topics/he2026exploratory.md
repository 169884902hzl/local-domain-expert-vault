---
title: "Towards Exploratory and Focused Manipulation with Bimanual Active Perception: A New Problem, Benchmark and Strategy"
tags: [manipulation, imitation, bimanual, tactile-sensing]
created: "2026-05-05"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 Exploratory and Focused Manipulation (EFM) 问题定义，构建 10 任务基准 EFM-10，设计双臂主动感知策略 BAP——利用非操作臂提供 eye-in-hand 主动视觉、操作臂提供力觉感知，通过模仿学习验证 BAP 的有效性。"
authors: "He, Yuxin; Zhang, Ruihao; Shen, Tianao; Liu, Cheng; Nie, Qiang"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GT24PNZ3"
---
## 摘要

Recently, active vision has reemerged as an important concept for manipulation（操控）, since visual occlusion occurs more frequently when main cameras are mounted on the robot heads. We reflect on the visual occlusion issue and identify its essence as the absence of information useful for task completion. Inspired by this, we come up with the more fundamental problem of Exploratory and Focused Manipulation（操控） (EFM). The proposed problem is about actively collecting information to complete challenging manipulation（操控） tasks that require exploration or focus. As an initial attempt to address this problem, we establish the EFM-10 benchmark that consists of 4 categories of tasks that align with our definition (10 tasks in total). We further come up with a Bimanual（双臂） Active Perception (BAP) strategy, which leverages one arm to provide active vision and another arm to provide force sensing while manipulating. Based on this idea, we collect a dataset named BAPData for the tasks in EFM-10. With the dataset, we successfully verify the effectiveness of the BAP strategy in an imitation learning（模仿学习） manner. We hope that the EFM-10 benchmark along with the BAP strategy can become a cornerstone that facilitates future research towards this direction. Project website: EFManipulation.github.io.

## 中文简述

提出基于模仿学习的双臂方法。

**研究方向**: 机器人操控、模仿学习、双臂操控、触觉感知

## 关键贡献

1. **提出 EFM 问题定义**：将视觉遮挡问题泛化为更根本的"主动信息收集"问题，形式化定义了四类任务需求
2. **构建 EFM-10 基准**：包含 4 类共 10 个真实世界操控任务，覆盖语义探索、视觉遮挡、精细操作和复合场景
3. **提出 Bimanual Active Perception (BAP) 策略**：利用非操作臂提供 6-DoF eye-in-hand 主动视觉，操作臂提供力觉感知，无需高自由度主动颈部即可实现主动感知
4. **收集 BAPData 数据集**：1810 段专家遥操作演示，是目前最大的带主动视觉的双臂操控数据集，也是唯一同时包含高自由度主动视觉和力觉信息的数据集
## 结构化提取

- **Problem**: 操控中的主动信息收集问题——机器人需要主动探索隐藏语义信息、规避视觉遮挡、或聚焦精细操作区域才能完成任务
- **Method**: BAP（Bimanual Active Perception）策略——非操作臂提供 eye-in-hand 主动视觉 + 操作臂提供 6D Force/Torque 力觉感知，基于模仿学习实现
- **Tasks**: EFM-10 基准——4 类 10 个任务：Toy-Find/Toy-Match（语义探索）、Cup-Hang/Cup-Place/Box-Push（视觉遮挡）、Light-Plug/Bread-Brush/Nail-Knock（精细聚焦）、Cable-Match/Charger-Plug（复合）
- **Sensors**: 头部 RGB-D 相机（Orbbec Gemini 2L）、2× 腕部 RGB 相机（Logitech C922Pro）、双臂内置 6D Force/Torque 传感器
- **Robot Setup**: JAKA K-1 双臂机器人（2× 7-DoF），Pico Ultra 4 VR 遥操作采集数据
- **Metrics**: 任务成功率（Success Rate, %）、平均最大垂直力（Avg. Fz Max），每设置 30 次随机试验评估
- **Limitations**: 精细操作成功率仍低；语义条件化和空间推理能力不足；双臂同时操作时 BAP 失效；仅验证模仿学习范式
- **Evidence Notes**: 全文证据覆盖完整。Table III 验证主动视野组成对成功率的影响；Table IV 展示四种策略在 EFM-10 上的全面对比；Table V 展示力觉感知对精细操作的提升；Figure 5 分析典型失败模式。部分具体数值（Table IV 详细逐任务数据、Table V 绝对数值）在 HTML 中因表格格式不完整，从文中描述和已有数据可推断趋势。
## 本地引用关系
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 版本，含所有章节、表格、图片描述)
- Evidence Coverage: 完整覆盖 Introduction、Related Work、EFM-10 Benchmark、BAP Strategy、全部实验（Table III-V）、Failure Analysis、Conclusion
- Confidence: high
- Summary: 提出 Exploratory and Focused Manipulation (EFM) 问题定义，构建 10 任务基准 EFM-10，设计双臂主动感知策略 BAP——利用非操作臂提供 eye-in-hand 主动视觉、操作臂提供力觉感知，通过模仿学习验证 BAP 的有效性。


## Problem

当主摄像头安装在机器人头部时，视觉遮挡更加频繁。本文认为视觉遮挡的本质是"完成任务所需信息的缺失"（absence of information useful for task completion），并由此提出更根本的 **Exploratory and Focused Manipulation (EFM)** 问题：机器人需要主动收集信息（探索或聚焦）才能完成具有挑战性的操控任务。核心是区分四类能力需求：语义探索、视觉遮挡下的探索、精细操作所需的聚焦、以及同时需要探索和聚焦的复合任务。


## Method

### BAP 策略核心思想
- **非操作臂** → 提供 eye-in-hand 主动视觉：腕部相机提供 6-DoF 可变视角，主动捕获操作区域和末端执行器
- **操作臂** → 提供力觉感知：内置 6D Force/Torque 传感器，用于精细接触操作
- 策略与颈部主动视觉完全兼容，可在双臂均忙时结合使用

### 硬件系统
- **机器人**：JAKA K-1 双臂机器人，每臂 7-DoF，内置 F/T 传感器
- **相机**：Orbbec Gemini 2L（头部固定）+ 2× Logitech C922Pro（腕部）
- **遥操作**：Pico Ultra 4 VR 头显
- **数据频率**：10 Hz

### 数据集 BAPData
- 1810 段专家演示，覆盖 EFM-10 全部 10 个任务
- 每段数据包含：头部相机图像、左右腕部相机图像、机器人状态（末端位姿 + 夹爪状态，dim=14+2）、6D Force/Torque 数据

### 策略实现方式
采用模仿学习（Imitation Learning），测试了四种代表性策略：
- **ACT**：单任务 Transformer 策略，使用 action chunking
- **Diffusion Policy (DP)**：单任务扩散模型策略（CNN 版本）
- **GR-MG**：多任务 Transformer 策略，使用未来图像预测和 action chunking
- **Pi-0**：多任务 VLM + flow matching 策略

状态/动作空间：笛卡尔空间（Cartesian space），action chunk 大小为 8

### 力觉融合方式（GR-MG variant）
- 将当前 6D Force/Torque 通过线性层编码为 embedding
- 将编码结果和查询 token 附加到输入序列
- 训练模型额外预测未来的 Force/Torque chunk


## Experiments

### 实验 1：验证 Eye-in-Hand 主动视觉的有效性（Table III）

选取 4 个任务（Toy-Match, Cup-Hang, Nail-Knock, Charger-Plug），对比三种主动视野设置下的成功率（每设置 30 次试验）：

| 主动视野可见内容 | Toy-Match | Cup-Hang | Nail-Knock | Charger-Plug |
|---|---|---|---|---|
| 均不可见 | 20.0% | 23.3% | 6.67% | 0.00% |
| 仅操作区域可见 | - | 76.7% | 26.7% | 13.3% |
| 操作区域 + 末端执行器 | **76.7%** | **90.0%** | **43.3%** | **20.0%** |

**关键发现**：主动视野必须同时捕获操作区域和操作末端执行器，仅捕获手持物体不够——因为手持物体相对于末端执行器的位姿是随机且多样的，无法仅凭物体位姿直接推断末端执行器的调整方向。

### 实验 2：EFM-10 基准策略评估（Table IV）

使用 BAPData 训练（不含力觉数据），在 EFM-10 上评估四种策略：

**主要观察**：
- ACT 和 DP 作为单任务策略，无法处理语言驱动的语义探索任务（Toy-Find）
- DP 在多模态动作分布任务（Box-Push）上优于 ACT，但在精细任务（Nail-Knock, Charger-Plug）上劣于 ACT（因缺少 temporal ensemble）
- Pi-0 指令跟随能力最强，在不涉及精细操作的任务上表现最好
- 所有策略在极精细任务（Light-Plug, Charger-Plug）上表现均不佳

### 实验 3：力觉感知的效果（Table V）

在 GR-MG 策略上添加力觉融合，测试两个精细任务：

| 任务 | 指标 | 无力觉 | 有力觉 | 变化 |
|---|---|---|---|---|
| Light-Plug | 成功率 | - | - | +16.7% |
| Light-Plug | 平均最大 Fz | - | - | -29%（相对） |
| Bread-Brush | 成功率 | - | - | +13.3% |
| Bread-Brush | 平均最大 Fz | - | - | -22%（相对） |

**关键发现**：力觉感知使成功率显著提升，同时使操作臂最大垂直力降低，实现了神经网络隐式学到的力柔顺控制（neural force compliance control）。可视化分析表明模型能预测力变化趋势并据此调整动作。

### 失败案例分析
1. **语义探索任务**（Toy-Find, Toy-Match, Cable-Match）：主要失败原因是未能准确根据语义上下文条件化动作，如选错颜色
2. **视觉遮挡任务**（Cup-Hang, Cup-Place, Box-Push）：失败模式多样——Cup-Hang 杯子被抓过低、Cup-Place 未找到最优视角、Box-Push 未能适应边界情况
3. **精细操作任务**（Light-Plug, Bread-Brush, Nail-Knock, Charger-Plug）：主要原因是策略的空间感知/推理能力不足，导致微小定位偏差


## Limitations

1. **策略泛化性不足**：所有测试策略在极精细任务上成功率仍很低（Light-Plug, Charger-Plug < 30%）
2. **语义条件化能力有限**：语言驱动任务的准确率受限于策略的指令跟随能力
3. **空间推理不够**：精细操作的微小定位误差频繁出现
4. **主动视角搜索未优化**：策略未能自主寻找最优视角避免遮挡
5. **仅用模仿学习**：未探索 RL 或其他学习范式
6. **BAP 策略局限性**：当双臂同时操作时无法使用非操作臂提供主动视觉，需要结合颈部主动视觉
7. **数据集规模有限**：1810 段演示对于 10 个任务仍显不足，尤其是精细操作任务


## Key Takeaways

1. **对 DLO 操控的直接启示**：BAP 策略可直接应用于线缆操控场景——非操作臂提供近距离视觉观察线缆状态，操作臂提供力觉反馈处理精细接触。Cable-Match 任务已初步验证了这一方向的可行性。
2. **末端执行器可视性的重要性**：精细操作时主动视野必须包含末端执行器（而非仅包含手持物体），这对 DLO 操控中的插入、缠绕等操作有直接指导意义。
3. **力觉感知的隐性柔顺控制**：神经网络通过模仿学习可以隐式学到力柔顺控制行为，无需显式的力控制规则，这对接触丰富的 DLO 操控（如打结、插入）很有价值。
4. **EFM 问题定义的框架价值**：四类任务分类法（语义探索、视觉遮挡、精细聚焦、复合）为系统评估 DLO 操控方法提供了结构化视角。
5. **主动感知与 Sim-to-Real 的结合点**：BAP 策略在仿真中同样适用，可以作为 Sim-to-Real 迁移中主动感知的统一框架。


## 本地引用关系

-
## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[tactile-sensing]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[he|He, Yuxin]]
