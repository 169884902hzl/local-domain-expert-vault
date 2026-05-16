---
title: "Semantic-Contact Fields for Category-Level Generalizable Tactile Tool Manipulation"
tags: [manipulation, imitation, VLM, diffusion, sim-to-real]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 Semantic-Contact Fields（SCFields），将视觉语义与密集外在接触概率和力估计融合为统一 3D 表示，通过仿真预训练+真实世界伪标签对齐的两阶段管线学习，使扩散策略在刮擦、蜡笔画、削皮三项接触丰富任务上实现类别级泛化。"
authors: "Ma, Kevin Yuchen; Zhang, Heng; Lin, Weisi; Shou, Mike Zheng; Wu, Yan"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PGXIWBUQ"
---
## 摘要

Generalizing tool manipulation（操控） requires both semantic planning and precise physical control. Modern generalist robot policies, such as Vision-Language-Action (VLA) models, often lack the physical grounding required for contact-rich（接触丰富） tool manipulation（操控）. Conversely, existing contact-aware policies that leverage tactile（触觉） or haptic sensing are typically instance-specific and fail to generalize across diverse tool geometries. Bridging this gap requires learning representations that are both semantically transferable and physically grounded, yet a fundamental barrier remains: diverse real-world tactile（触觉） data are prohibitive to collect at scale, while direct zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer is challenging due to the complex nonlinear deformation of soft tactile（触觉） sensors. To address this, we propose Semantic-Contact Fields (SCFields), a unified 3D representation that fuses visual semantics with dense extrinsic contact estimates, including contact probability and force. SCFields is learned through a two-stage Sim-to-Real（仿真到真实迁移） Contact Learning Pipeline: we first pre-train on large-scale simulation to learn geometry-aware contact priors, then fine-tune on a small set of real data pseudo-labeled via geometric heuristics and force optimization to align real tactile（触觉） signals. The resulting force-aware representation serves as the dense observation input to a diffusion policy（扩散策略）, enabling physical generalization to unseen tool instances. Experiments on scraping, crayon drawing, and peeling demonstrate robust category-level generalization, significantly outperforming vision-only and raw-tactile（触觉） baselines. Project page: https://kevinskwk.github.io/SCFields/.

## 中文简述

提出基于扩散策略的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、仿真到真实迁移

## 关键贡献

1. **SCFields 表示**：提出统一的 3D 表示 Semantic-Contact Fields，将预训练视觉模型的语义特征与密集外在接触概率和力估计融合到工具点云上，每个点携带力向量、接触概率和语义特征
2. **两阶段 Sim-to-Real 管线**：
   - Stage 1：在大规模仿真数据（300 工具、32 万帧）上预训练，学习几何感知的接触先验
   - Stage 2：使用几何启发式 + SOCP 力优化生成伪标签，在小量真实数据上微调对齐真实触觉信号
3. **实验验证**：在 Franka Panda 机器人上验证刮擦、蜡笔画、削皮三项任务，展现对未见工具实例的类别级泛化能力，显著超越 Vision-Only 和 Raw Tactile 基线
## 结构化提取

- Problem: 接触丰富的工具操控的类别级泛化——如何设计既语义可迁移又物理 ground 的表示，使策略在未见工具上仍能精确调控接触力
- Method: SCFields——统一 3D 表示（视觉语义 + 接触概率 + 力向量）；两阶段 Sim-to-Real 管线（仿真预训练 + 真实伪标签对齐）；Tactile-as-PointCloud 架构（PointNet++）；条件扩散策略
- Tasks: 刮擦（接触密集清洁）、蜡笔画（力调制绘线）、削皮（功能接触+力控制）
- Sensors: GelSight Mini 触觉传感器（双侧，7×9 标记网格）；3× RealSense D435 RGB-D 相机
- Robot Setup: Franka Emika Panda + 改装平行夹爪（集成 GelSight Mini）
- Metrics: 成功率(SR)、清洁效率(Eff)、归一化效率(Eff Norm)、绘画一致性(0-1)、接触百分比、切入百分比、平均削皮长度
- Limitations: 依赖模仿学习无法发现新功能、需要多传感器、假设接触区域部分可观测、无时序跟踪
- Evidence Notes: 核心证据来自 Table III-V 的策略评估和 Table II 的接触场评估；消融实验（Focal Loss、无触觉、无力向量、Sim-Only、Real-Only）提供了各组件贡献的直接证据；附录 F 提供了完整的统计显著性分析（95% CI 和 p-value）；蜡笔任务的显著性检验不完全 conclusive，作者将其作为支持性证据而非最强统计结果
## 本地引用关系

- [[ma2026semanticcontact]]
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取完整论文内容，含所有表格、附录）
- Evidence Coverage: high（覆盖方法架构、仿真数据生成、真实世界对齐、三项任务实验、消融实验、统计显著性分析）
- Confidence: high
- Summary: 提出 Semantic-Contact Fields（SCFields），将视觉语义与密集外在接触概率和力估计融合为统一 3D 表示，通过仿真预训练+真实世界伪标签对齐的两阶段管线学习，使扩散策略在刮擦、蜡笔画、削皮三项接触丰富任务上实现类别级泛化。


## Problem

机器人工具操控需要在语义层面理解工具的功能部位（如刀刃、手柄），同时在物理层面精确调控接触力。现有方法面临双重困境：
1. VLA 等通用策略缺乏接触丰富的物理 grounding，仅靠视觉语义无法区分"悬空"与"接触"状态
2. 触觉策略虽然能处理局部接触，但直接将触觉信号映射到动作，缺乏中间泛化表示，无法适应不同几何形状的工具

核心障碍：真实世界触觉数据难以大规模采集，而软体触觉传感器的非线性形变使得零样本 Sim-to-Real 迁移极为困难。


## Method

### 整体框架

方法分为两个独立学习问题：

1. **外在接触场估计**：学习感知映射 $f_\phi$，将工具/环境点云、触觉传感器读数和本体感知状态转换为工具表面上的密集外在接触场（每点分配接触概率 $c_i$ 和 3D 力向量 $\mathbf{f}_i$）
2. **泛化策略学习**：以 SCFields 作为观测输入，训练扩散策略 $\pi_\theta(a_{t:t+H}|O_t)$ 预测动作序列

### 接触场估计架构（Tactile-as-PointCloud）

- **核心思想**：将触觉信号视为 3D 几何实体，直接融合到场景几何中
- **输入**：复合点云 $P_{total} = P_{obj} \cup P_{env} \cup P_{tactile}$（894 点：256 工具 + 512 环境 + 126 触觉）
- **特征**：每点携带类型编码 + H 步触觉标记位移历史
- **骨干网络**：PointNet++ encoder-decoder（3 层 SA + 3 层 FP）
- **输出头**：接触概率头（Sigmoid，标量）+ 力回归头（无激活，3D 向量）

### 仿真数据生成

- **多仿真器管线**：
  - IsaacGym + TacSL：高吞吐刚体动力学 + GelSight 传感器仿真
  - Open3D：计算 SDF 用于软接触概率标签（指数衰减函数，5mm 半衰）
  - PyBullet：提取离散接触力，通过距离加权核插值外推到密集点云
- **数据规模**：300 个程序化生成工具（刮刀、蜡笔、削皮器），320,000 帧
- **触觉后处理**：空间高斯滤波（模拟弹性体扩散）+ 时域 Savitzky-Golay 滤波 + 接触相位平滑

### 真实世界伪标签生成

- **启发式接触概率**：利用已知桌面高度限制接触候选区域，通过触觉信号门控过滤误报
- **分析性力优化（SOCP）**：求解二阶锥规划，使分布点力与观测触觉力矩匹配
  - 目标：最小化力矩残差 + 正则化（与接触概率反比加权）
  - 约束：力幅值 ≤ 2 倍法向投影（确保压力在 ~60° 摩擦锥内）
  - 求解器：ECOS
- **关键优势**：伪标签数据与模仿学习演示数据同时采集，无需额外数据收集

### 两阶段训练

| 参数 | Stage 1 (仿真) | Stage 2 (真实) |
|------|----------------|----------------|
| 学习率 | 1e-4 | 5e-6 |
| Batch Size | 320 | 128 |
| Epochs | 400 | 60 |
| 点云平移增强 | ±0.1m | ±0.05m |
| 点云旋转增强 | ±30° | ±15° |

损失函数：$\mathcal{L} = \lambda_{prob}\mathcal{L}_{prob} + \lambda_{force}(\lambda_{mag}\mathcal{L}_{mag} + \lambda_{dir}\mathcal{L}_{dir})$
- $\mathcal{L}_{prob}$：Focal Loss（γ=0.75, α=0.9）处理类别不平衡
- $\mathcal{L}_{mag}$：自适应加权 MSE（对数幅值权重）
- $\mathcal{L}_{dir}$：余弦相似度（仅力幅值 > 0.005N 的点）

### 策略学习

- SCFields 观测：每点特征 $x_i = [\mathbf{f}^{ext}_i \parallel c_i \parallel S_i]$，其中 $S_i$ 来自 GenDP 的 3D 语义场
- 扩散策略：条件 U-Net，PointNet++ 提取全局特征作为条件输入
- 观测窗口 3 步，预测窗口 16 步，执行 8 步后重新规划


## Experiments

### 实验设置

- **机器人**：Franka Emika Panda
- **触觉传感器**：GelSight Mini（安装在平行夹爪两侧）
- **视觉**：3 台标定的 RealSense D435（前、左、右）
- **任务**：刮擦、蜡笔画、削皮

### 接触场评估

**Sim-to-Sim 架构验证（Table II）**：
| 模型 | F1 Score | Force MSE |
|------|----------|-----------|
| NCF | 0.043 | N/A |
| No-Tactile | 0.539 | 0.0146 |
| Ours (Sim-Only) | 0.587 | 0.0147 |
| BCE Loss 消融 | 0.123 | 0.0146 |

**真实世界对齐精度（Table II）**：
| 模型 | 刮刀 F1 | 刮刀 Force MSE | 蜡笔 F1 | 蜡笔 Force MSE |
|------|---------|---------------|---------|---------------|
| Sim-Only | 0.002 | 0.0435 | 0.008 | 0.0284 |
| Real-Only | 0.458 | 0.0221 | 0.614 | 0.0106 |
| Ours (Aligned) | 0.534 | 0.0254 | 0.657 | 0.0085 |

关键发现：Sim-Only 在真实数据上几乎完全失败（F1 ~0.002），证明触觉 Sim-to-Real 差距严重。Ours (Aligned) 成功将对齐从刮刀迁移到蜡笔（未见类别）。

### 策略评估

**Task 1 - 刮擦（Table III）**：
| 方法 | Seen SR | Seen Eff Norm | Unseen SR | Unseen Eff Norm |
|------|---------|---------------|-----------|-----------------|
| GenDP | 39.1% | 30.5% | 35.1% | 35.1% |
| Raw Tactile | 35.1% | 35.7% | 50.0% | 27.3% |
| Ours | **73.5%** | **85.2%** | **79.6%** | **84.7%** |
| No Force 消融 | 31.3% | 29.9% | 26.0% | 27.6% |

**Task 2 - 蜡笔画（Table IV）**：
| 方法 | Seen 一致性 | Unseen 一致性 |
|------|------------|--------------|
| GenDP | 0.81 | 0.60 |
| Ours | **0.86** | **0.78** |

**Task 3 - 削皮（Table V）**：
| 方法 | Seen Contact | Seen Peel (cm) | Unseen Contact | Unseen Peel (cm) |
|------|-------------|----------------|----------------|------------------|
| GenDP | 45.0% | 1.50 | 50.0% | 1.12 |
| Ours | **80.0%** | **4.73** | **90.0%** | **4.52** |

削皮任务中接触场模型仅用刮刀数据做真实对齐，仍实现对削皮器（未见类别）的强泛化，平均削皮长度是 Vision-Only 的 4 倍。

### 关键消融发现

1. **Focal Loss 关键**：BCE 替换后 F1 从 0.587 降至 0.123（类别不平衡严重）
2. **力向量不可省略**：No Force 消融导致策略悬空或过度施压
3. **接触概率对扩展接触区域最有用**：刮刀（沿边缘分布）受益显著，蜡笔（近似点接触）影响较小
4. **Sim 预训练必要**：Real-Only 可拟合已见工具但无法泛化到新类别
5. **真实对齐必要**：Sim-Only 在真实触觉上完全失效


## Limitations

1. **依赖模仿学习**：策略局限于演示中的工具使用模式，无法发现新功能（如用刀削胡萝卜）
2. **部分可观测假设**：要求功能性接触区域至少部分在工具点云中可见
3. **多传感器依赖**：需要 3 台 RGB-D 相机 + 双侧 GelSight 传感器来获取可靠几何和接触估计
4. **无时序跟踪**：当前方法不支持完全遮挡的接触状态跟踪
5. **触觉仿真保真度有限**：尽管有真实对齐阶段，仿真触觉信号质量仍受限


## Key Takeaways

1. **Tactile-as-PointCloud 融合范式**：将触觉信号作为 3D 几何实体直接融合到点云中（而非独立编码器），是一种简洁高效的触觉-视觉融合方式，值得在 DLO 操控中借鉴
2. **两阶段 Sim-to-Real 对接触感知有效**：仿真预训练提供几何感知的接触先验，真实世界伪标签对齐弥合传感器域差异——这种范式对任何涉及触觉的策略都有参考价值
3. **力感知表示优于纯接触概率**：仅知道"是否接触"不够，需要力的方向和大小信息来调控交互——这对需要力控制的 DLO 操作（如柔性线缆穿引、绳结拉紧）同样重要
4. **伪标签策略巧妙**：利用已知环境几何（桌面高度）+ SOCP 力优化，在不依赖外部力传感器的情况下生成训练标签，数据采集与演示收集同步完成
5. **跨类别泛化证据**：刮刀对齐的模型成功迁移到削皮器，表明"功能性接触"这一抽象在不同工具间具有不变性——这种表示学习思路可扩展到其他操控场景

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[ma-kevin-yuchen|Ma, Kevin Yuchen]]
- [[zhang-heng|Zhang, Heng]]
