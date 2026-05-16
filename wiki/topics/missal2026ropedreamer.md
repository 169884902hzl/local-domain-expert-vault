---
title: "RopeDreamer: A kinematic recurrent state space model for dynamics of flexible deformable linear objects"
tags: [manipulation, imitation, DLO, planning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%"
authors: "Missal, Tim; Domingues, Lucas; Guler, Berk; Manschitz, Simon; Peters, Jan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "6KQGIVWK"
---
## 摘要

The robotic manipulation（机器人操控） of Deformable Linear Objects (DLOs) is a fundamental challenge due to the high-dimensional, non-linear dynamics of flexible structures and the complexity of maintaining topological integrity during contact-rich（接触丰富） tasks. While recent data-driven methods have utilized Recurrent and Graph Neural Networks for dynamics modeling, they often struggle with self-intersections and non-physical deformations, such as tangling and link stretching. In this paper, we propose a latent dynamics framework that combines a Recurrent State Space Model with a Quaternionic Kinematic Chain representation to enable robust, long-term forecasting of DLO（可变形物体） states. By encoding the DLO（可变形物体） as a sequence of relative rotations (quaternions) rather than independent Cartesian positions, we inherently constrain the model to a physically valid manifold that preserves link-length constancy. Furthermore, we introduce a dual-decoder architecture that decouples state reconstruction from future-state prediction, forcing the latent space to capture the underlying physics of deformation. We evaluate our approach on a large-scale simulated dataset of complex pick-and-place trajectories involving self-intersections. Our results demonstrate that the proposed model achieves a 40.52% reduction in open-loop（开环） prediction error over 50-step horizons compared to the state-of-the-art（现有最优方法） baseline, while reducing inference time by 31.17%. Our model further maintains superior topological consistency in scenarios with multiple crossings, proving its efficacy as a compositional primitive for long-horizon（长时序） manipulation（操控） planning.

## 中文简述

提出基于学习方法的可变形物体方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、可变形物体操控、运动规划

## 关键贡献

1. **RSSM 适配高段数 DLO 动力学**：将 Recurrent State Space Model 引入 DLO 领域，通过确定性（GRU）+随机性状态分解实现 50 步稳定开环预测，无需真值修正
2. **四元数运动链表示**（Quaternionic Kinematic Chain）：将 DLO 编码为单位四元数序列（相邻段间的相对旋转），从表示层面保证链长恒定，消除非物理拉伸
3. **全面的仿真验证**：在 1M 转换的大规模 MuJoCo 数据集上，RMSE 相比 SOTA（GA-Net S）降低 40.52%，推理速度提升 31.17%，拓扑准确率（Gauss Code 匹配）在 50 步后仍维持 38-65%（基线在 30 步即降至 10% 以下）
## 结构化提取

- **Problem**: DLO 动力学预测——在自交叉和接触丰富场景下实现长时序稳定、拓扑一致的开环预测
- **Method**: RSSM + 四元数运动链 + 双解码器（重构/预测分离），ELBO 损失优化
- **Tasks**: 单臂平面 DLO pick-and-place 动力学预测（非端到端任务，仅动力学模型评估）
- **Sensors**: 仿真中直接获取 DLO 段位置（真值状态）；实际部署计划结合 TrackDLO 等视觉追踪
- **Robot Setup**: MuJoCo 仿真，单臂 mocap 末端执行器，DLO 为 70 段胶囊体链（10mm×10mm），平面操作
- **Metrics**: RMSE（段位置误差）、推理时间（ms/步）、Gauss Code 拓扑准确率（%）
- **Limitations**: 仅仿真验证、初始重构损失 trade-off、仅平面操控、未闭环部署、未验证不同材质泛化、代码未发布
- **Evidence Notes**: 全文证据充分，实验包含 500 次独立 rollout、3 个模型规模 × 2 种基线 × 多个规模的全面对比、消融实验验证四元数表示与 RSSM 的各自贡献。拓扑评估使用 Gauss Code 提供了客观可复现的量化指标。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文获取）
- Evidence Coverage: full（全文含 Introduction, Related Work, Problem Formulation, Method, Experiments, Conclusion）
- Confidence: high
- Summary: 提出将 RSSM 与四元数运动链结合的 DLO 潜空间动力学框架，通过双解码器分离重构与预测，在 50 步开环预测中将 RMSE 降低 40.52%，推理速度提升 31.17%


## Problem

机器人操控 DLO（如绳索、线缆）的核心挑战在于 DLO 的高维非线性动力学和拓扑完整性维护。现有数据驱动方法（GNN 如 GA-Net、RNN 如 IN-BiLSTM）存在三个关键缺陷：
1. **过平滑与过压缩**：GNN 的局部消息传递无法处理长程依赖（一个端点的动作影响中间段）
2. **非物理变形**：基于笛卡尔坐标的段级编码缺乏物理约束，导致"拉伸"或"穿透"
3. **拓扑崩塌**：自交叉场景（如绳环、结）下拓扑结构快速丧失

目标：构建一个计算高效、物理一致、支持长时序开环预测的 DLO 动力学模型。


## Method

### 核心架构（Figure 3）

整体为 **RSSM-based World Model**，包含以下模块：

#### 1. 四元数运动链表示
- 预处理阶段将 DLO 状态 $\mathbf{s}_t$ 从笛卡尔坐标转换为混合表示：
  - 第一段：笛卡尔位置 $\mathbf{p}^0 \in \mathbb{R}^3$（基座位置）
  - 后续段：单位四元数 $\mathbf{q}^i \in \mathbb{H}$（段 $i-1$ 与段 $i$ 间的相对旋转）
- 状态向量维度：$3 + 4(L-1)$，其中 $L$ 为段数
- 通过正运动学可重建所有段位置
- **关键优势**：从表示层面保证链长恒定，模型无法预测"拉伸"；且因仅编码几何而非段间距离，可泛化至不同长度的 DLO

#### 2. RSSM 潜空间动力学
- **Action Encoder**：Link-aware 设计——可学习嵌入层编码抓取段索引 + MLP 编码位移 $\Delta p$
- **State Encoder**：将四元数运动链状态投影到嵌入空间
- **Recurrent Model**（GRU）：融合前一步确定性状态 $\mathbf{h}_{t-1}$、随机状态 $\mathbf{z}_{t-1}$、动作嵌入 $\mathbf{a}_{t-1}$，输出当前确定性状态 $\mathbf{h}_t$
- **Posterior**：$z_t \sim q_\phi(z_t | h_t, e_t)$，基于当前观测编码
- **Prior**：$\hat{z}_t \sim p_\phi(\hat{z}_t | h_t)$，仅基于确定性状态预测

#### 3. 双解码器策略（Dual-Decoder）
- **Reconstruction Decoder**：用 $(h_t, z_t)$（后验）重构当前状态 $\hat{s}_t^{recon}$，确保潜空间捕获即时几何
- **Prediction Decoder**：用 prior 链式前推一步得到 $(h_{t+1}, \hat{z}_{t+1})$，预测下一状态 $\hat{s}_{t+1}^{pred}$
- 分离设计防止重构损失主导预测动力学，使潜空间专为多步"dreaming"优化

#### 4. 损失函数（修改版 ELBO）
$$\mathcal{L}_{total} = \mathcal{L}_{recon} + \mathcal{L}_{pred} + \beta \mathcal{L}_{KL}$$
- $\mathcal{L}_{recon}$：后验重构 MSE
- $\mathcal{L}_{pred}$：先验预测 MSE（关键——驱动"dreaming"能力）
- $\mathcal{L}_{KL}$：后验与先验的 KL 散度，保持潜空间稳定性

### 模型规模
三个配置（Small / Medium / Large），参数量逐级增加（具体见表 I），均基于 RMSE 与参数量的最优权衡选择。


## Experiments

### 数据集
- **规模**：10,000 条轨迹 × 100 步 = 1M 转换，80/10/10 划分
- **仿真**：MuJoCo 3.3.7，DLO 建模为 70 个胶囊体（10mm×10mm），球铰连接
- **物理参数**：胶囊摩擦 0.8，关节弯曲刚度 0.005，地面摩擦 1.0，阻尼 0.05
- **动作**：随机 pick-and-place，抓取随机段，提升 50mm 后在 XY 平面移动 50mm（方向均匀采样 $[0, 2\pi)$）

### 基线
1. **GA-Net**（GNN + Transformer Encoder + Attention）：6 个规模（XS~XL），参数 2.45M~68.69M
2. **IN-BiLSTM**（Interaction Network + BiLSTM）：3 个规模（S/M/L），参数 18.64M~74.52M

### 主要结果

#### 开环 RMSE（Figure 4）
- 5 步 warmup 后，50 步开环预测，500 次独立 rollout 取平均
- **RopeDreamer Large** 在 t=50 时 RMSE 相比最佳基线（GA-Net S）降低 **40.52%**
- GA-Net 短期精度高（前几步），但长期 RMSE 快速发散（t=10 增长 15.68mm，t=50 增长 64.94mm）
- RopeDreamer 增长更稳定（t=10 仅增 5.44mm，t=50 增 19.05mm）
- RopeDreamer 标准差在全时序保持稳定，基线呈指数增长趋势
- 消融实验：将四元数表示用于 GA-Net（XS/Quat）仍无法阻止长期发散 → 稳定性主要来自 RSSM 而非仅坐标表示

#### 推理速度（Figure 5）
- RopeDreamer Large：0.53ms/步 vs GA-Net S：0.77ms/步 → **31.17% 加速**
- 原因：潜空间内进行时间前推，无需每步构建图和计算边交互
- IN-BiLSTM 推理时间更长，不适用于实时场景

#### 拓扑准确率（Figure 6, Gauss Code 匹配）
- 使用 Gauss Code（基于交叉点的有符号整数序列）量化拓扑一致性
- **RopeDreamer**：全 50 步保持 38-65% 准确率
- **GA-Net**：t=10 即降至 40%，t=30 低于 10%
- **GA-Net XS/Quat**：t=15 降至 0%
- 表明 RopeDreamer 有效维护了 DLO 的结构身份

### 训练细节
- 最大 200 epochs，lr=1e-4，β=1，batch=32
- 验证集上 checkpoint 选择，early stopping 10 epochs
- 实际多数配置在 epoch 50 附近收敛
- 硬件：Nvidia RTX Pro 6000 Blackwell


## Limitations

1. **纯仿真验证**：无真实机器人实验，Sim-to-Real 差距未评估
2. **初始重构损失**：潜空间信息瓶颈导致短期 RMSE 高于基线（trade-off）
3. **仅平面操控**：数据集限于 XY 平面 pick-and-place，未涉及 3D 空间操作
4. **未闭环部署**：作为动力学模型独立评估，未集成到完整 RL/MPC 框架中测试端到端任务性能
5. **固定物理参数**：未考虑不同材质（如不同刚度、摩擦）的泛化
6. **代码与数据集未发布**：声明将在后续版本中发布


## Key Takeaways

1. **四元数运动链是 DLO 表示的重要创新**：通过将 DLO 视为刚体运动链（类似机器人学中的串联机构），从表示层面而非损失函数层面保证物理约束。这对我们的 DLO 操控研究有直接借鉴价值——可替代或增强现有的笛卡尔坐标表示。

2. **RSSM 优于 GNN 处理 DLO 长程依赖**：GNN 的局部消息传递在自交叉场景下天然受限，RSSM 的全局潜空间编码更适合捕获 DLO 的整体构型变化。这提示在双臂 DLO 操控中，RSSM 可能比 GNN 更适合做动力学预测器。

3. **双解码器设计值得借鉴**：分离重构和预测任务，避免重构损失主导潜空间学习。这对长时序任务特别重要——"理解当前状态"和"预测未来状态"是不同能力。

4. **MPC 应用前景**：推理速度快（0.53ms/步）+ 长时序稳定预测，适合作为 Model Predictive Control 的动力学模型。与我们的双臂操控规划有直接衔接可能。

5. **未来方向与我们研究交集**：作者计划探索 Sim-to-Real、RL 集成、层次化潜空间架构——这些与我们的研究方向（DLO 操控 + Sim-to-Real + RL）高度重合。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[planning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[missal|Missal, Tim]]
- [[domingues|Domingues, Lucas]]
- [[guler|Guler, Berk]]
- [[manschitz|Manschitz, Simon]]
