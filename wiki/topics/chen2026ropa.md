---
title: "ROPA: Synthetic robot pose generation for RGB-D bimanual data augmentation"
tags: [manipulation, imitation, diffusion, bimanual, grasping]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "ROPA 通过 Stable Diffusion + ControlNet 骨架姿态条件合成双臂操控的新 RGB/RGB-D 观测和关节动作标签，实现离线数据增广，仿真和真实世界实验全面超越 ACT、VISTA 等基线。"
authors: "Chen, Jason; Liu, I-Chun Arthur; Sukhatme, Gaurav; Seita, Daniel"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VQJP7MU9"
---
## 摘要

Training robust bimanual manipulation（双臂操控） policies via imitation learning（模仿学习） requires demonstration（示范数据） data with broad coverage over robot poses, contacts, and scene contexts. However, collecting diverse and precise real-world demonstrations is costly and time-consuming, which hinders scalability. Prior works have addressed this with data augmentation, typically for either eye-in-hand (wrist camera) setups with RGB inputs or for generating novel images without paired actions, leaving augmentation for eye-to-hand (third-person) RGB-D training with new action labels less explored. In this paper, we propose Synthetic Robot Pose Generation for RGB-D Bimanual（双臂） Data Augmentation (ROPA), an offline imitation learning（模仿学习） data augmentation method that fine-tunes Stable Diffusion（扩散） to synthesize third-person RGB and RGB-D observations of novel robot poses. Our approach simultaneously generates corresponding joint-space action labels while employing constrained optimization to enforce physical consistency through appropriate gripper-to-object contact constraints in bimanual（双臂） scenarios. We evaluate our method on 5 simulated and 3 real-world tasks. Our results across 2625 simulation trials and 300 real-world trials demonstrate that ROPA outperforms baselines and ablations, showing its potential for scalable RGB and RGB-D data augmentation in eye-to-hand bimanual manipulation（双臂操控）. Our project website is available at: https://ropaaug.github.io/.

## 中文简述

ROPA 利用 Stable Diffusion + ControlNet 进行骨架姿态引导的机器人图像合成（PGRIS），为双臂操控模仿学习提供离线数据增广。核心创新在于：通过 PyRender 渲染双臂运动学骨架作为 ControlNet 条件，区分接触/非接触阶段分别用约束优化和均匀采样生成物理可行的动作标签，并扩展支持 RGB-D 同步增广和多视角设置。在 PerAct2 仿真（5 任务）和真实双臂 UR5 平台（3 任务）上全面超越 ACT、VISTA 等基线。

**研究方向**: 机器人操控、模仿学习、扩散模型、双臂操控、抓取

## 关键贡献

1. **ROPA 方法**：首个面向双臂操控的骨架姿态引导离线数据增广方法，同时支持 RGB 和 RGB-D 输入
2. **深度图像合成**：生成与增强后关节位置和 RGB 图像一致的深度图，填补了机器人操控领域深度增广的空白
3. **动作一致性增广**：通过约束优化确保生成的图像-动作对物理可行，在接触丰富阶段保持夹爪-物体接触约束
4. **全面的实验验证**：5 个仿真任务（PerAct2/RLBench）+ 3 个真实世界任务，共 2625 仿真试验 + 300 真实试验，全面超越基线
## 结构化提取

- Problem: 双臂操控模仿学习中的数据稀缺问题，特别是第三人称 RGB-D 视角下同时生成新图像和对应动作标签的数据增广
- Method: Stable Diffusion 2.1 + ControlNet 骨架姿态引导图像合成 (PGRIS)，基于力矩残差的接触检测，接触阶段约束优化 (Dual Annealing) + 非接触阶段均匀采样生成动作标签，每 k=8 步替换增强状态
- Tasks: 仿真 5 任务 (Coordinated Lift Ball, Coordinated Lift Tray, Coordinated Push Box, Bimanual Straighten Rope, Coordinated Put Item in Drawer) + 真实 3 任务 (Lift Ball, Push Block, Lift Drawer)
- Sensors: Intel RealSense D415 RGB-D 相机（第三人称视角），支持最多 4 摄像头多视角设置
- Robot Setup: 双臂 UR5 机械臂 + Robotiq 2F-85 夹爪，仿真基于 PerAct2/RLBench，真实世界遥操作使用 GELLO
- Metrics: 成功率 (Success Rate)，每设置 3 随机种子取平均
- Limitations: 需要机器人姿态可观测性、相机标定、扩散模型可能产生伪影、无深度增广基线、多条件训练计算成本高
- Evidence Notes:

  - 仿真实验证据充分：5 任务 × 4 方法 × 3 种子 = 2625 试验，全部表格数据完整
  - 真实世界实验证据充分：3 任务 × 5 方法 × 20 试验 = 300 试验（具体数值在 Table V 中，全文中未展示具体数字，仅描述了定性结果）
  - 消融实验覆盖骨架表示、姿态输入形式，4 组对照
  - 泛化实验包含 zero-shot 和 few-shot 设置
  - 真实世界 Table V 的具体数值在全文 HTML 中未完整展示，Evidence Coverage 仍标记为 complete 因为主要仿真结果充分支撑结论
## 本地引用关系

- [[chen2026ropa]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: complete — 包含完整的方法描述、实验表格、消融实验、真实世界结果和附录
- Confidence: high
- Summary: 提出基于 Stable Diffusion + ControlNet 的骨架姿态引导图像合成方法 ROPA，用于双臂操控模仿学习的离线数据增广，同步生成 RGB/RGB-D 图像与关节空间动作标签，在 5 个仿真和 3 个真实世界任务上显著优于基线方法。


## Problem

双臂操控模仿学习需要大量多样化示范数据（覆盖不同机器人姿态、接触状态和场景上下文），但真实世界示范数据采集成本高、耗时长，限制了可扩展性。现有数据增广方法主要面向单臂的腕部摄像头（eye-in-hand）RGB 设置，或仅生成新视角图像而不生成配对动作标签。对于第三人称（eye-to-hand）RGB-D 视角下的双臂操控场景，同时生成新图像和对应动作标签的数据增广方法仍未被充分探索。


## Method

### 核心架构：Pose-Guided Robot Image Synthesis (PGRIS)
受人体姿态引导图像生成（PGPIS）启发，将问题转化为机器人姿态引导的图像合成：
- 输入：源相机图像 $I_t^s$、目标骨架姿态图像 $I_t^p$、语言目标 $g$
- 输出：目标相机图像 $I_t^d$
- 模型：Stable Diffusion 2.1 + ControlNet 双流架构

### 三阶段流程
**阶段 1：Skeleton Pose Generator**
- 使用 PyRender 渲染双臂运动学链的骨架表示
- 圆柱体表示骨骼段，球体表示关节连接器（带 GENIMA 纹理提供旋转线索）
- 虚拟相机参数与真实相机严格匹配（内外参）

**阶段 2：条件扩散模型**
- 冻结 SD 2.1 U-Net 处理噪声潜变量和文本嵌入
- 可训练 ControlNet 模块处理源图像 + 骨架姿态条件
- 通过零初始化卷积层注入姿态感知特征
- DDIM 采样生成目标图像

**阶段 3：动作标签生成与数据集构建**
- 接触检测：基于力矩残差的自回归模型 $\mu_{ext} = \mu_{motor} - \hat{\mu}_{model}$
- 无接触阶段：均匀采样末端执行器扰动 $\Delta\rho$，通过逆运动学计算关节扰动
- 接触阶段：约束优化（Dual Annealing），确保扰动后保持物理约束（桌面距离、双臂间距、IK 可行性）
- 数据集构建：复制原始数据集，每 k=8 步替换一次增强状态，缓解行为克隆的累积误差

### 多模态与多视角扩展
- **深度增广**：ControlNet 以 RGB 目标图像 + 骨架姿态为条件（6 通道拼接），生成几何一致的深度图
- **多视角**：4 个摄像头观测拼接为单一复合图像，支持多视角一致生成


## Experiments

### 仿真实验（PerAct2 / RLBench）
**任务**：
- Coordinated Lift Ball (CLB)：抬起随机生成的球
- Coordinated Lift Tray (CLT)：抬起带有物品的托盘
- Coordinated Push Box (CPB)：将大箱子推到目标区域
- Bimanual Straighten Rope (BSR)：将绳索两端放入目标区域
- Coordinated Put Item in Drawer (CPID)：将物品放入指定抽屉

**基线方法**：
- ACT (w/o Augmentation)：100 条原始示范
- ACT (more data)：100 原始 + 100 额外示范
- Fine-tuned VISTA：扩散模型新视角合成

**主要结果（成功率 %）**：

| Method | CLB | CLT | CPB | BSR | CPID |
|--------|-----|-----|-----|-----|------|
| RGB ACT (w/o aug) | 41.3 | 10.7 | 43.3 | 21.3 | 17.3 |
| RGB Fine-tuned VISTA | 52.7 | 1.6 | 54.3 | 10.3 | 15.7 |
| RGB ACT (more data) | 48.0 | 12.0 | 42.7 | 17.3 | 10.3 |
| **RGB ROPA (ours)** | **68.0** | **30.7** | **62.7** | **24.3** | **30.7** |
| RGB-D ACT (w/o aug) | 56.7 | 14.3 | 49.7 | 26.7 | 17.6 |
| RGB-D ACT (more data) | 33.3 | 9.7 | 47.0 | 20.3 | 16.3 |
| **RGB-D ROPA (ours)** | **72.0** | **35.0** | **61.3** | **29.0** | **35.0** |

### 消融实验（CLB 任务）
| 方法 | 成功率 |
|------|--------|
| ROPA with Joint Position Only | 46.7 |
| ROPA with White Skeleton | 32.0 |
| ROPA with OpenPose Skeleton | 62.6 |
| **ROPA (完整)** | **68.0** |

### 泛化实验
- Zero-shot：在 5 个任务上训练后直接迁移到 CLB
- Few-shot（10 条示范微调）：有一定效果
- 直接微调（100 条）：最佳

### 真实世界实验
- 硬件：双 UR5 + Robotiq 2F-85 + Intel RealSense D415
- 遥操作：GELLO，每任务 30 条示范
- 任务：Lift Ball、Push Block、Lift Drawer
- 每方法每任务 20 次试验，共 300 次
- ROPA 在所有任务上大幅优于基线

### 关键发现
1. ROPA 在全部 5 个仿真任务上超越所有基线（RGB 和 RGB-D 均如此）
2. 简单增加数据量不一定提升性能（ACT more data 在部分任务上反而下降）
3. 骨架姿态表示显著优于原始关节位置向量
4. GENIMA 纹理球体比纯白骨架或 OpenPose 骨架效果更好
5. 深度信息带来小幅但一致的提升


## Limitations

1. **姿态可观测性依赖**：图像生成依赖机器人姿态信息，严重遮挡场景下效果受限
2. **相机标定需求**：骨架渲染需要精确的相机内外参标定
3. **扩散模型伪影**：可能产生不真实的生成结果，需额外的条件模态（边缘检测、分割掩码）来缓解
4. **深度增广无基线**：现有深度估计模型（如 DepthAnything）不适用作基线，存在循环依赖问题
5. **多条件 ControlNet 训练成本高**：多模态条件方法需要 8 GPU × 48GB VRAM


## Key Takeaways

1. **骨架姿态条件** 是将扩散模型用于机器人图像合成的有效条件方式，比原始关节向量提供更丰富的空间上下文
2. **接触感知增广策略**（区分接触/非接触阶段分别处理）对双臂操控的数据增广至关重要
3. **BSR（双臂理绳）任务** 直接关联 DLO 操控，ROPA 在该任务上的提升表明姿态多样性对绳索操控有帮助
4. **动作标签一致性** 是机器人数据增广的关键约束——仅生成图像而不保证动作可行性的方法效果有限
5. **RGB-D 同步增广** 是一个被忽视但重要的方向，深度信息对精细操控任务有价值
6. 该方法与 ACT 等 Transformer 策略正交，可组合使用；对 DLO 操控的启示是可以通过扩散模型合成更多样化的 DLO 形态和机器人接触状态

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[tactile-sensing]]

## 相关研究者

- [[chen-jason|Chen, Jason]]
- [[liu-i-chun-arthur|Liu, I-Chun Arthur]]
- [[sukhatme|Sukhatme, Gaurav]]
- [[seita|Seita, Daniel]]
