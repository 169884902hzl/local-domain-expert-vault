---
title: "UltraDexGrasp: Learning universal dexterous grasping for bimanual robots with synthetic data"
tags: [manipulation, imitation, sim-to-real, bimanual, planning]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移"
authors: "Yang, Sizhe; Xie, Yiman; Liang, Zhixuan; Tian, Yang; Zeng, Jia et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "AHQBPHZH"
---
## 摘要

Grasping（抓取） is a fundamental capability for robots to interact with the physical world. Humans, equipped with two hands, autonomously select appropriate grasp strategies based on the shape, size, and weight of objects, enabling robust grasping（抓取） and subsequent manipulation（操控）. In contrast, current robotic grasping（抓取） remains limited, particularly in multi-strategy settings. Although substantial efforts have targeted parallel-gripper and single-hand grasping（抓取）, dexterous（灵巧） grasping（抓取） for bimanual（双臂） robots remains underexplored, with data being a primary bottleneck. Achieving physically plausible and geometrically conforming grasps that can withstand external wrenches poses significant challenges. To address these issues, we introduce UltraDexGrasp, a framework for universal dexterous（灵巧） grasping（抓取） with bimanual（双臂） robots. The proposed data-generation pipeline integrates optimization-based grasp synthesis with planning-based demonstration（示范数据） generation, yielding high-quality and diverse trajectories across multiple grasp strategies. With this framework, we curate UltraDexGrasp-20M, a large-scale, multi-strategy grasp dataset comprising 20 million frames across 1,000 objects. Based on UltraDexGrasp-20M, we further develop a simple yet effective grasp policy that takes point clouds as input, aggregates scene features via unidirectional attention, and predicts control commands. Trained exclusively on synthetic data, the policy achieves robust zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer and consistently succeeds on novel objects with varied shapes, sizes, and weights, attaining an average success rate of 81.2% in real-world universal dexterous（灵巧） grasping（抓取）. To facilitate future research on grasping（抓取） with bimanual（双臂） robots, we open-source the data generation pipeline at https://github.com/InternRobotics/UltraDexGrasp.

## 中文简述

提出基于点云的抓取方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、双臂操控、运动规划

## 关键贡献

1. **UltraDexGrasp-20M 数据集**：首个面向双臂灵巧手的大规模多策略抓取数据集，包含 1000 物体、2000 万帧轨迹数据，覆盖双臂抓/全手抓/两指捏/三指夹四种策略
2. **数据生成管线**：将优化抓取合成（bilevel optimization）与规划示范生成（bimanual motion planning）互补集成，生成运动学可行、物理合理且多样化的闭环轨迹
3. **通用抓取策略**：基于 PointNet++ 编码器 + decoder-only transformer（单向注意力）+ 有界高斯动作预测的简洁策略架构，支持多策略抓取并泛化到未见物体
## 结构化提取

- **Problem**: 双臂灵巧手通用抓取——为不同尺寸/形状/重量物体自动选择并执行合适的多策略抓取（双臂/全手/两指/三指）
- **Method**: 优化抓取合成（bilevel optimization，接触力 QP + 手部位姿梯度下降）+ 双臂运动规划示范生成 + PointNet++ 编码器 + decoder-only transformer（单向注意力）+ 有界高斯动作预测
- **Tasks**: 通用抓取（universal grasping），包括四种策略：bimanual grasp、whole-hand grasp、two-finger pinch、three-finger tripod
- **Sensors**: 2× Azure Kinect DK 深度相机（eye-on-base 配置），生成场景点云（2048 点）；机器人关节状态（用于生成 imaged point cloud）
- **Robot Setup**: 双臂 2× UR5e（6-DoF），双灵巧手 2× XHand (12-DoF)，间距 0.9m，控制频率 10Hz
- **Metrics**: 抓取成功率（success rate）——物体抬升 ≥ 0.17m 且保持 ≥ 1s 不掉落
- **Limitations**: 仅单平台验证、无杂乱场景、大物体放置受限、数据生成成功率 68.5%、无反应式重规划、仅抓取不操控
- **Evidence Notes**:

  - 仿真 600 物体平均 84.0%，未见物体 83.4%，领先 DP3 37.3pp、DexGraspNet 25.2pp
  - 真实 25 物体平均 81.2%，零样本迁移，物体尺寸跨度 18-26400 cm³，重量跨度 3.6-1095g
  - 消融：有界高斯预测贡献 +10.5pp，单向注意力贡献 +15.8pp
  - 数据缩放：超过 1M 帧后策略超越数据生成成功率
## 本地引用关系

- [[yang2026ultradexgrasp]]
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 完整获取）
- Evidence Coverage: 完整覆盖 Introduction、Related Work、Preliminaries、Dataset、Policy、Experiments、Conclusion 全部章节；含完整表格数据（Table I-III）、消融实验和缩放曲线
- Confidence: high
- Summary: 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移


## Problem

双臂灵巧手机器人的**通用抓取**（universal dexterous grasping）问题。核心挑战：
1. **数据瓶颈**：现有灵巧抓取数据生成方法（RL 专家、优化合成、学习合成）各有局限——RL 专家缺乏多样性，优化/学习方法多为开环且忽略手臂运动学
2. **多策略需求**：不同尺寸/形状/重量物体需要不同抓取策略（双臂抓、全手抓、两指捏、三指夹），现有方法大多只处理单手场景
3. **物理可行性**：需要生成既符合几何贴合又能抵抗外力矩的抓取姿态
4. **Sim-to-Real 迁移**：如何仅用合成数据训练的策略直接部署到真实世界


## Method

### 数据生成管线（Section IV）

**阶段一：抓取合成（Grasp Synthesis）**
- 基于 BODex 的 bilevel optimization 框架：
  - **下层 QP**：优化接触力以实现目标力矩
  - **上层梯度下降**：更新手部位姿以缩小目标力矩与可达力矩误差
- 优化目标（Eq.6）包含四项：
  1. 力矩匹配损失（wrench matching）
  2. 接触距离能量（contact distance energy）
  3. 手-物体碰撞惩罚
  4. 手-手穿透惩罚
- 使用 cuRobo + GPU QP solver 高效求解
- **策略适配**：通过选择不同指尖接触点实现四种抓取策略（Fig.3）
- 每个物体生成 500 候选抓取 → 物理验证 → IK 可达性检查 → 碰撞检测 → SE(3) 距离排序选最优

**阶段二：示范生成（Demonstration Generation）**
- 四阶段轨迹：pregrasp（0.1m 撤回）→ grasp → squeeze → lift（0.2m 抬升）
- 双臂运动规划生成无碰撞协调轨迹
- 验证标准：物体抬升 ≥ 0.17m 且保持 ≥ 1s 不掉落
- 随机化：相机位姿、关节阻抗

### 策略架构（Section V）

**点云编码**：
- FPS 下采样至 2048 点
- PointNet++ 两层 Set Abstraction：
  - SA1：2048 点，k=32 kNN，保持点数
  - SA2：下采样至 256 点，提取高层特征

**动作预测**：
- Learnable action query tokens 通过单向注意力（unidirectional attention）从点云特征中聚合场景信息
- MLP 解码为动作向量
- **有界高斯分布**（bounded Gaussian / truncated normal）参数化动作，优化负对数似然而非直接回归

**Sim-to-Real 实现**：
- 坐标系统一对齐 + 相机内外参标定
- SOR 滤波去除深度噪声
- 模拟点云（imaged point cloud）补充机器人自身点云，显著减小 sim-to-real gap
- 关节阻抗随机化减小动力学差距


## Experiments

### 仿真实验（Section VI-A）

**设置**：
- 硬件：2× UR5e + 2× XHand (12-DoF)
- 测试集：600 物体（含训练可见和不可见类）
- 物体范围：重量 5g-1000g，尺寸 0.03m-0.5m+
- 每物体 10 次试验，按大/中/小分组评估

**主要结果（Table I）**：
| 方法 | Small | Medium | Large | Average | Unseen |
|------|-------|--------|-------|---------|--------|
| DP3 | 较低 | 较低 | 较低 | 46.7% | — |
| DexGraspNet | 较低 | 较高 | N/A | 58.8%* | — |
| **Ours** | **高** | **高** | **高** | **84.0%** | **83.4%** |

*DexGraspNet 仅支持单手抓取，无法处理大物体

**数据缩放（Fig.5）**：
- 数据量从 0.1M 增长到 20M，性能持续提升
- 超过 1M 帧后策略性能显著超越数据生成成功率（68.5%）

**消融实验（Table II）**：
| 变体 | 成功率 |
|------|--------|
| w/o 有界高斯预测 | 73.5% |
| w/o 单向注意力 | 68.2% |
| **完整模型** | **84.0%** |

### 真实实验（Section VI-B）

**设置**：
- 硬件：2× UR5e（间距 0.9m）+ 2× XHand + 2× Azure Kinect DK
- 25 个物体，每物体 15 次试验
- 控制频率 10 Hz
- 最小物体 18 cm³，最大 26400 cm³；最轻 3.6g，最重 1095g

**结果（Table III）**：
- 平均成功率 **81.2%**
- 零样本 sim-to-real 迁移，无需任何真实数据微调
- 有效适配多种抓取策略：三指夹、全手抓、双臂抓


## Limitations

1. **平台特定性**：仅在 UR5e + XHand 组合上验证，未测试其他灵巧手平台
2. **大物体放置受限**：大物体仅能在 0.15m × 0.16m 区域内随机放置（确保可达性），限制了大物体场景的多样性
3. **无杂乱场景评估**：所有实验均为桌面单物体场景，未测试多物体堆叠/杂乱环境
4. **数据生成成功率有限**：数据生成管线成功率为 68.5%，部分物体可能系统性地无法生成有效抓取
5. **缺乏反应式抓取**：策略为开环执行（预计算轨迹），不支持动态避障或在线重规划
6. **仅抓取任务**：只解决抓取（grasp），不涉及抓取后的操控（manipulation）任务


## Key Takeaways

1. **点云 + 单向注意力架构的有效性**：简洁的 PointNet++ + transformer 架构在双臂灵巧抓取上显著优于 DP3（+37.3pp），证明精心设计的点云编码器比通用 diffusion policy 更适合此类任务
2. **优化+规划的互补集成**：纯优化方法（如 DexGraspNet）受限于单手和开环，而结合运动规划可以生成闭环协调轨迹，这对双臂 DLO 操控有借鉴意义——DLO 的形变也需要优化+规划的协同
3. **合成数据可行性**：20M 帧纯合成数据即可实现 81.2% 真实成功率，无需真实数据，说明仿真管线的设计（随机化、imaged point cloud）对 sim-to-real 迁移至关重要
4. **多策略分治**：通过接触点选择统一四种抓取策略到同一优化框架中，而非分别训练不同策略，这种"参数化策略选择"思路可迁移到 DLO 的多种操控方式
5. **与 DLO 操控的相关性**：本方法不直接处理 DLO，但其双臂协调抓取框架和点云策略架构可作为 DLO 操控系统的抓取前置模块；优化合成+运动规划的管线设计思路对 DLO 轨迹规划也有参考价值

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[bimanual-manipulation]]
- [[planning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[yang-sizhe|Yang, Sizhe]]
- [[liang-zhixuan|Liang, Zhixuan]]
