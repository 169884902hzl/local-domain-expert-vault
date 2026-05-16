---
title: "RC-NF: Robot-conditioned normalizing flow for real-time anomaly detection in robotic manipulation"
tags: [manipulation, imitation, VLM, planning]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anomaly-10 基准上取得 SOTA。"
authors: "Zhou, Shijie; Zhu, Bin; Yang, Jiarui; Zhao, Xiangyu; Chen, Jingjing et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "5D35NUPN"
---
## 摘要

Recent advances in Vision-Language-Action (VLA) models have enabled robots to execute increasingly complex tasks. However, VLA models trained through imitation learning（模仿学习） struggle to operate reliably in dynamic environments and often fail under Out-of-Distribution (OOD) conditions. To address this issue, we propose Robot-Conditioned Normalizing Flow (RC-NF), a real-time monitoring model for robotic anomaly detection and intervention that ensures the robot's state and the object's motion trajectory align with the task. RC-NF decouples the processing of task-aware robot and object states within the normalizing flow. It requires only positive samples for unsupervised training and calculates accurate robotic anomaly scores during inference through the probability density function. We further present LIBERO-Anomaly-10, a benchmark comprising three categories of robotic anomalies for simulation evaluation. RC-NF achieves state-of-the-art（现有最优方法） performance across all anomaly types compared to previous methods in monitoring robotic tasks. Real-world experiments demonstrate that RC-NF operates as a plug-and-play module for VLA models (e.g., pi0), providing a real-time OOD signal that enables state-level rollback or task-level replanning when necessary, with a response latency under 100 ms. These results demonstrate that RC-NF noticeably enhances the robustness and adaptability of VLA-based robotic systems in dynamic environments.

## 中文简述

提出基于模仿学习的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、运动规划

## 关键贡献

1. **RC-NF 模型**：提出基于条件归一化流的无监督机器人异常检测模型，核心是 RCPQNet（Robot-Conditioned Point Query Network）——一种新的仿射耦合层，将任务感知的机器人状态作为条件注入归一化流，同时解耦机器人与物体特征。
2. **LIBERO-Anomaly-10 基准**：在 LIBERO-10 基础上构建的机器人异常检测基准，包含三种操控特定异常类型（Gripper Open、Gripper Slippage、Spatial Misalignment）。
3. **真实世界验证**：RC-NF 作为 π0 的即插即用模块，在 RTX 3090 上实现 <100ms 响应延迟，支持 task-level 重规划和 state-level 轨迹回滚。
## 结构化提取

- **Problem**: VLA 模型在动态环境中 OOD 条件下不可靠，现有监控方法要么需要枚举异常（分类方法），要么延迟过高（VLM 方法），要么特征纠缠（FailDetect）
- **Method**: 基于 Glow 的条件归一化流（RC-NF），核心组件 RCPQNet 将机器人状态通过 FiLM 调制为 task-aware query，物体点集通过双分支（Dynamic Shape + Positional Residual）编码为 memory，cross-attention 交互生成仿射参数，负对数似然作为异常分数
- **Tasks**: 10 个 LIBERO 桌面操控任务（pick-and-place、开抽屉等），异常检测基准涵盖 Gripper Open、Gripper Slippage、Spatial Misalignment
- **Sensors**: 第三人称 RGB 相机（Intel RealSense D435，仿真和真实），腕部相机（仅 VLA 训练用），机器人本体感知（关节、夹爪、笛卡尔位姿）
- **Robot Setup**: Franka Research 3 机械臂，7-DOF，仿真用 LIBERO 环境
- **Metrics**: AUC（ROC 曲线下面积）、AP（Average Precision），延迟（ms）
- **Limitations**: 依赖 SAM2 分割质量；阈值校准需专家数据；任务嵌入需预定义任务集；仅用 2D 点集；评估范围有限
- **Evidence Notes**:

  - Table 1: RC-NF Average AUC 0.9309, AP 0.9494，超越最佳基线 GPT-5 约 8%/10%
  - Table 2: 消融研究验证各组件贡献，Dynamic Shape 分支最关键（去掉后 AUC 降至 0.6841）
  - Fig 4: 异常分数可视化显示 RC-NF 在 t_anomaly 前稳定在 -2 左右，异常后快速响应
  - 延迟分解：SAM2 50ms + grid sampling 1.7ms + RC-NF 30ms + 其他 5ms = 86.7ms（RTX 3090）
  - 真实世界：成功展示 task-level（抽屉关闭 → 重规划）和 state-level（球滑落/滚动 → homing 回滚）两种 OOD 处理
## 本地引用关系

- [[zhou2026rcnf]]
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取全文，含正文、补充材料、表格和公式）
- Evidence Coverage: 高（方法细节完整、实验表格齐全、消融研究充分、真实世界实验有视频和延迟数据）
- Confidence: high
- Summary: 提出 RC-NF（基于条件归一化流的机器人异常检测模型），通过 RCPQNet 解耦机器人状态与物体点集特征，实现 <100ms 实时异常检测，并在 LIBERO-Anomaly-10 基准上取得 SOTA。


## Problem

Vision-Language-Action (VLA) 模型通过模仿学习训练，在动态环境中难以可靠运行，尤其在 Out-of-Distribution (OOD) 条件下容易失败。现有运行时监控方法存在两类问题：

1. **基于分类的方法**（如行为树、预条件检测）：需要穷举异常条件，难以覆盖现实操控的组合爆炸式异常。
2. **基于 VLM 的方法**（如 Sentinel、双系统架构）：需要多步推理，延迟在秒级（多秒），无法实现实时干预。

此外，现有的无监督方法（如 FailDetect）直接拼接图像特征与机器人状态，导致特征纠缠和特征不平衡。


## Method

### 整体架构

RC-NF 基于 Glow 架构的条件归一化流，将物体点集映射到以任务嵌入为均值的高斯潜变量空间。推理时通过负对数似然计算异常分数。

**输入**：
- **物体点集** x ∈ ℝ^{B×T×N×2}：由 SAM2 从视频流中分割物体 mask 后经 grid sampling 得到，其中 B=batch, T=滑动窗口步数, N=每帧采样点数, 2D 坐标
- **条件 c=(s, τ)**：机器人状态 s（关节、夹爪、笛卡尔位姿）和任务嵌入 τ

**条件归一化流**：
- 由 K=12 个条件变换步骤组成
- 每步包含 ActNorm → Permute → Affine Coupling Layer（RCPQNet）
- 潜变量分布：Z ~ N(μ_task, I)，其中 μ_task 由任务嵌入 τ 广播得到
- 训练：最大化对数似然（Eq. 5-6），仅需正样本

### RCPQNet（核心创新）

将点集沿时间维度分为两半 x_b 和 x_t，用 x_b 和条件 c 生成仿射参数 γ, β：
- y = [γ⊙x_t + β; x_b]

包含两个关键组件：

**1. Task-aware Robot-Conditioned Query**
- 机器人状态通过线性层投影到潜空间
- 通过 FiLM 机制用任务嵌入 τ 调制，生成 query token
- 同时编码机器人状态上下文和高层任务目标

**2. Dual-Branch Point Feature Encoding**
- **Dynamic Shape 分支**：对每帧进行居中和归一化以消除平移和尺度影响，提取形状特征
- **Positional Residual 分支**：补偿形状归一化丢失的绝对位置信息
- 两个分支分别经 MLP → average pooling → GRU → Transformer encoder 生成 memory token
- Query 和 memory token 通过 cross-attention 交互

### 任务嵌入

- **Spherical Uniform Encoding**：将任务提示映射到 T 维超球面（半径 R=5）上的均匀分布向量
- 保证任务嵌入在潜空间中最大分离，为密度估计提供最优几何结构
- 实现时通过优化算法获得均匀分布的球面向量

### 异常检测与处理

**阈值设定**：
- Upper_𝒯 = μ_𝒯 + Q_{1-α}(D_𝒯)，基于校准数据集 S1 和 S2 的统计量
- 训练时进行去偏以保证异常分数的时间平滑性

**异常处理策略**：
- **Task-level OOD**（环境/上下文与指令不匹配）→ 通知高层控制器进行任务重规划
- **State-level OOD**（任务有效但物理配置偏移）→ 激活 homing 过程回滚轨迹，调整后交还 VLA

### 训练策略

- **BalancedHardSampler**：两阶段训练，前期标准采样，后期根据推理结果加权，平衡初始阶段与抓取阶段的轨迹分布差异
- K=12 个 flow steps，训练 100 epochs
- 仿真环境中用计算机图形技术生成 SAM2 首帧 bounding box（确保可复现）
- 真实世界中用 Gemini 2.5 Pro 零样本生成 bounding box


## Experiments

### 仿真实验

**数据集**：LIBERO-10（50 demonstrations/task）训练，LIBERO-Anomaly-10 评估

**LIBERO-Anomaly-10 三种异常类型**：
1. **Gripper Open**：夹爪在应抓取时保持打开，物体位置正常但机器人状态异常
2. **Gripper Slippage**：夹爪摩擦力设为零，物体滑落产生异常轨迹波动
3. **Spatial Misalignment**：机器人朝错误方向移动（前/左/右而非目标后方），测试语义-空间错位

**主要结果（Table 1）**：

| Method | Average AUC | Average AP |
|--------|------------|------------|
| GPT-5 | 0.8500 | 0.8507 |
| Gemini 2.5 Pro | 0.8186 | 0.8313 |
| Claude 4.5 | 0.8214 | 0.8249 |
| FailDetect | 0.7181 | 0.7700 |
| **RC-NF (Ours)** | **0.9309** | **0.9494** |

- RC-NF 超越最佳基线约 8% AUC 和 10% AP
- VLM 在 Spatial Misalignment 上退化为近随机水平（AUC ≈ 0.5）
- RC-NF 在 Spatial Misalignment 上尤其突出（AUC 0.9676）

**消融研究（Table 2）**：

| 变体 | Average AUC | Average AP |
|------|------------|------------|
| RC-NF (完整) | 0.9309 | 0.9494 |
| w/o Task Embedding | 0.8643 | 0.9008 |
| w/o Robot State | 0.7152 | 0.8401 |
| w/o Pos. Residual branch | 0.8947 | 0.9225 |
| w/o Dyn. Shape branch | 0.6841 | 0.7899 |

关键发现：
- 去掉任务嵌入 → Spatial Misalignment 性能大幅下降（因无法区分任务特定异常）
- 去掉机器人状态 → Gripper Open AUC 最低（0.6327，因为夹爪打开不直接移动物体）
- Dynamic Shape 分支最关键（去掉后平均 AUC 降至 0.6841，Spatial Misalignment 降至 0.1022）

### 真实世界实验

**硬件**：Franka Research 3 机械臂，腕部+第三人称 Intel RealSense D435 相机
**VLA 模型**：π0
**延迟**（RTX 3090）：SAM2 推理 50ms + Grid Sampling 1.7ms + RC-NF 推理 30ms + 其他 5ms = **总计 86.7ms**

**Task-level OOD 处理**：任务"将蓝色球放入打开的抽屉"中，抽屉中途关闭 → RC-NF 检测到异常 → 触发高层控制器重规划（先重置球、打开抽屉，再执行任务）

**State-level OOD 处理**：
- 球被重新放回桌面 → RC-NF 立即检测异常 → 激活 homing 过程重新对齐轨迹
- 球滚到夹爪后方 → RC-NF 检测异常 → 调整轨迹朝向球的新位置
- 异常分数恢复正常后，控制无缝交还 VLA

### 任务嵌入补充实验

- 将 Spatial Misalignment 的 3 个任务加入训练集后，RC-NF 性能几乎不下降
- 但去掉任务嵌入后，RC-NF 监控性能降至约 0.6
- FailDetect 性能降至 0.5，无法区分同一训练集内的不同任务


## Limitations

1. **依赖 SAM2 分割质量**：首帧需要 bounding box prompt，仿真环境用图形技术保证，真实环境依赖 Gemini 2.5 Pro 零样本生成，分割失败会传播影响
2. **阈值校准依赖专家数据**：需要成功的专家演示数据来估计异常阈值（Eq. 7），对每个任务都需要独立校准
3. **任务嵌入需预定义任务集**：Spherical Uniform Encoding 需要事先知道任务数量，新增任务需要重新计算嵌入
4. **仅处理 2D 点集**：使用 2D 坐标的点集表示，未利用深度信息
5. **异常处理策略较简单**：state-level 仅用 homing 过程回滚，未考虑更精细的恢复策略
6. **评估范围有限**：仿真仅在 LIBERO-10 上评估，真实世界仅展示了一个任务场景


## Key Takeaways

1. **归一化流用于异常检测的优势**：相比 VLM 需要多步推理（秒级延迟），归一化流可直接计算概率密度作为异常分数，延迟低至 86.7ms。这对于 DLO 操控中需要快速响应（如绳索滑落）的场景尤其有价值。

2. **解耦机器人-物体特征的必要性**：RCPQNet 将机器人状态作为 query、物体点集作为 memory，通过 cross-attention 交互而非简单拼接。这种设计思路可用于 DLO 操控中将机器人手部状态与 DLO 形状特征解耦。

3. **点集表示 vs 原始图像特征**：基于 SAM2 分割 + grid sampling 的点集表示比原始图像特征更鲁棒。对于 DLO，可以用类似的点集/曲线采样方法表示 DLO 的形状变化。

4. **任务感知条件化**：任务嵌入通过 FiLM 机制调制机器人状态特征，使模型能区分不同任务下的正常/异常行为。这对多任务 DLO 操控场景有借鉴意义。

5. **无监督训练范式**：仅需正样本（成功演示），不需要穷举异常类型。在 DLO 操控中，失败模式多样且难以枚举，这种无监督范式尤其适合。

6. **Real-time 意味着可闭环**：<100ms 延迟使异常检测可以嵌入闭环控制，在 DLO 操控中可用于实时检测绳索滑落、缠绕异常等。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zhou-shijie|Zhou, Shijie]]
- [[zhu-bin|Zhu, Bin]]
