---
title: "Benchmarking generalizable bimanual manipulation: RoboTwin dual-arm collaboration challenge at CVPR 2025 MEIS workshop"
tags: [manipulation, RL, robot-learning, tactile, bimanual]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "RoboTwin 双臂协作挑战赛（CVPR 2025 MEIS Workshop）技术报告。基于 RoboTwin 仿真平台（1.0/2.0）和 AgileX COBOT-Magic 真实平台，64 个团队/400+ 参与者完成 17 个双臂操控任务（刚体+可变形+触觉）。三阶段赛制（仿真 Round 1/2 + 真实世界 Round）。冠军方案 AnchorDP3（稀疏 keypose 扩散策略+3D 点云+任务专用编码器）和 SEM（3D 空间增强+机器人状态图编码+扩散解码器）。真实世界最佳团队仅 26.4/100 分，揭示双臂操控的巨大挑战。"
authors: "Chen, Tianxing; Wang, Kaixuan; Yang, Zhaohui; Zhang, Yuhao; Chen, Zanxin et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "VISVT3ZC"
---
## 摘要

Embodied Artificial Intelligence (Embodied AI) is an emerging frontier in robotics, driven by the need for autonomous systems that can perceive, reason, and act in complex physical environments. While single-arm systems have shown strong task performance, collaborative dual-arm（双臂） systems are essential for handling more intricate tasks involving rigid, deformable, and tactile（触觉）-sensitive objects. To advance this goal, we launched the RoboTwin Dual-Arm（双臂） Collaboration Challenge at the 2nd MEIS Workshop, CVPR 2025. Built on the RoboTwin Simulation platform (1.0 and 2.0) and the AgileX COBOT-Magic Robot platform, the competition consisted of three stages: Simulation Round 1, Simulation Round 2, and a final Real-World Round. Participants totally tackled 17 dual-arm manipulation（双臂操控） tasks, covering rigid, deformable, and tactile（触觉）-based scenarios. The challenge attracted 64 global teams and over 400 participants, producing top-performing solutions like SEM and AnchorDP3 and generating valuable insights into generalizable bimanual（双臂） policy learning. This report outlines the competition setup, task design, evaluation methodology, key findings and future direction, aiming to support future research on robust and generalizable bimanual manipulation（双臂操控） policies. The Challenge Webpage is available at https://robotwin-benchmark.github.io/cvpr-2025-challenge/.

## 中文简述

提出基于触觉感知的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、强化学习、机器人学习、触觉感知、双臂操控

## 关键贡献

1. **RoboTwin 双臂协作挑战赛**：CVPR 2025 MEIS Workshop 竞赛，64 个团队/400+ 参与者，17 个双臂操控任务（刚体 12 + 可变形 2 + 触觉 1 + 真实世界 5），覆盖三种模态（视觉、深度、触觉）。
2. **三阶段赛制设计**：Simulation Round 1（6 任务，无域随机化）→ Simulation Round 2（6 任务，域随机化+语言指令+统一模型）→ Real-World Round（5 任务，COBOT-Magic 平台，300+20 演示/任务）。
3. **AnchorDP3 冠军方案分析**：稀疏 keypose 动作表示（仅预测关键姿态，10-30 keypose vs 传统 20-25Hz 密集动作）+ 任务专用 PointNet++ 编码器（0.28M 参数）+ 共享扩散动作专家。98.7% 成功率。14.5x 更多样化的训练数据。
4. **SEM 亚军方案分析**：3D 空间增强器（多视图 2D→3D 特征提升）+ 机器人状态图编码器（关节图+注意力）+ 扩散动作解码器。强调显式 3D 空间推理的重要性。
5. **六项关键洞察**：模型容量与任务复杂度匹配、数据量与质量并重、多模态融合与深度编码、指令接地与语言鲁棒性、数据预处理与演示精炼、统一模型泛化与评估偏差。
## 结构化提取

- **Problem**: 双臂操控缺乏标准化基准评估泛化能力。现有单臂基准不涉及双臂协作复杂性。需要统一平台推动刚体+可变形+触觉多模态双臂操控研究。
- **Method**: 竞赛报告（非单一方法）。三阶段赛制：Sim R1（RoboTwin 1.0, 6 任务, 100 trials/任务）→ Sim R2（RoboTwin 2.0, 6 任务, 域随机化, 统一模型, 语言 unseen）→ Real（COBOT-Magic, 5 任务, 320 演示/任务, 20 trials）。冠军 AnchorDP3（稀疏 keypose+PointNet++ 任务编码器+CondUnet1D 扩散专家）。亚军 SEM（3D 空间增强+关节图编码+扩散解码）。
- **Tasks**: 17 个双臂操控任务。Sim R1: Place Empty Cup, Stack Bowls Three, Put Dual Shoes, Put Bottles Dustbin, Stack Blocks Three, Classify Tactile。Sim R2: Blocks Ranking RGB, Place Dual Shoes, Put Bottles Dustbin, Stack Blocks Three, Place Phone Stand, Place Object Scale。Real: Pour Water, Fold Towel, Fold Shorts, Stack Plates, Cap Pen。
- **Sensors**: Sim: RGB 图像 + 深度 + 点云（可选手动分割）。Real: RGB 相机（COBOT-Magic 配置），无详细传感器规格。触觉任务含 FEA 变形模拟。
- **Robot Setup**: Sim: RoboTwin 1.0/2.0 双臂仿真机器人。Real: AgileX COBOT-Magic 双臂 Piper 机器人。推理硬件: RTX 4090 单卡。
- **Metrics**: 仿真: Success Rate per task（100 trials, 阶段评分）, 总分 105/600。真实: Success Rate per task（20 trials, 15 seen + 5 unseen）, 总分 100。团队排名基于总分。
- **Limitations**: 竞赛报告非方法论文；outcome-based 评估偏差；仿真-真实差距巨大（103 vs 26.4）；可变形物体极困难；数据质量依赖人工；统一模型负迁移；触觉任务有限；语言泛化不足。
- **Evidence Notes**: 定量结果有官方评估表格（Tab. 1-3），64 团队/400+ 参与者。冠军 AnchorDP3 98.7% 仿真成功率（Sim R2 总分 596/600）。真实世界最佳 26.4/100，可变形物体最低 0.30/20。MOMODA 数据量消融：48.2% → 95.1%（100→3000 集）。六项洞察来自参赛团队方案分析。整体证据强度：强（大规模竞赛数据 + 官方评估 + 冠亚军方案详细描述）。
## 本地引用关系

- [[collaboration2025open]]
- [[kuroki2025gendom]]
- [[zhang2021dair]]
## 证据元数据

- **Zotero Key**: VISVT3ZC
- **Citekey**: chen2025benchmarking
- **Authors**: Chen Tianxing, Wang Kaixuan, Yang Zhaohui, Zhang Yuhao, Chen Zanxin, Chen Baijun, Dong Wanxi, Liu Ziyuan, Chen Dong, Yang Tianshuo, Yu Haibao, Yang Xiaokang, Qin Yusen, Xie Zhiqiang, Mu Yao, Luo Ping 等 27 个团队/机构
- **Affiliation**: HKU MMLab, SJTU, Huawei Germany, D-Robotics, AgileX Robotics 等
- **Venue**: arXiv preprint, 2025-07 (CVPR 2025 MEIS Workshop)
- **Paper Type**: Benchmark/Challenge Report（竞赛技术报告）
- **Fulltext Quality**: Complete, 13 pages with tables, figures, team solutions analysis
- **Evidence Coverage**: High for competition setup and task design; High for winning solutions (AnchorDP3, SEM); Medium for other team insights (aggregated observations)
- **Confidence**: High on competition structure and numerical results (official evaluation); Medium on generalizability of insights (derived from competition-specific observations)
- **Summary**: RoboTwin 双臂协作挑战赛（CVPR 2025 MEIS Workshop）技术报告。基于 RoboTwin 仿真平台（1.0/2.0）和 AgileX COBOT-Magic 真实平台，64 个团队/400+ 参与者完成 17 个双臂操控任务（刚体+可变形+触觉）。三阶段赛制（仿真 Round 1/2 + 真实世界 Round）。冠军方案 AnchorDP3（稀疏 keypose 扩散策略+3D 点云+任务专用编码器）和 SEM（3D 空间增强+机器人状态图编码+扩散解码器）。真实世界最佳团队仅 26.4/100 分，揭示双臂操控的巨大挑战。


## Problem

双臂机器人操控缺乏标准化基准来评估泛化能力。现有单臂基准（Meta-World, LIBERO, CALVIN）不涉及双臂协作的复杂性。关键挑战包括：（1）长视界多阶段操控；（2）可变形物体的高维欠驱动动力学；（3）触觉-视觉多模态融合；（4）域随机化下的鲁棒性；（5）Sim-to-Real 迁移。需要一个统一的竞赛平台来推动双臂操控策略的泛化研究。


## Method

### 赛制设计（非单一方法论文）

#### Simulation Round 1
- 平台：RoboTwin 1.0
- 6 任务：Place Empty Cup, Stack Bowls Three, Put Dual Shoes, Put Bottles Dustbin, Stack Blocks Three, Classify Tactile（触觉分类含 FEA 变形模拟）
- 每任务 100 trials 评估，测试种子未见过
- 单任务单模型，RTX 4090 单卡推理
- 满分 105（刚性任务 5×20，触觉任务 5）

#### Simulation Round 2
- 平台：RoboTwin 2.0
- 6 任务：Blocks Ranking RGB, Place Dual Shoes, Put Bottles Dustbin, Stack Blocks Three, Place Phone Stand, Place Object Scale
- 域随机化：未见背景纹理、场景杂乱、±3cm 桌面高度变化、光照变化
- **统一模型**要求：单模型解所有任务
- 语言指令在评估时不可见（unseen），需模型自行解析
- 完全完成才得分，每任务 100 分，总分 600

#### Real-World Round
- 平台：AgileX COBOT-Magic（双臂 Piper 机器人）
- 5 任务：Pour Water, Fold Towel, Fold Shorts, Stack Plates, Cap Pen
- 数据：300 演示/任务（非竞赛环境，多视角/桌面/背景变化）+ 20 演示/任务（竞赛环境，比赛前一周发布）
- 20 trials/任务（15 seen + 5 unseen 背景）
- 统一模型+共享权重
- 评估时语言指令不可见

### AnchorDP3（冠军方案）
- **稀疏 keypose 表示**：仅预测 affordance 锚定的关键姿态（pre-grasp, grasp, placement），10-30 keypose vs 密集动作序列
- **3D 点云分割**：利用仿真器完整场景知识自动生成点级分割掩码
- **任务专用编码器**：每个任务一个轻量 PointNet++（0.28M 参数），共享扩散动作专家（CondUnet1D）
- **双监督**：同时预测关节角和末端执行器位姿，利用几何一致性
- **两阶段训练**：LSMQ-D（大规模中等质量数据）→ SSHQ-D（小规模高质量数据微调）

### SEM（亚军方案）
- **空间增强器**：多视图 2D 图像特征→3D 位置嵌入（采样候选深度+跨视图投影）
- **机器人状态编码器**：关节图（每个关节为节点，注意力建模关节间距离）
- **扩散动作解码器**：条件化于语义+几何表示
- **即插即用模块**：视觉/语言/控制组件可独立升级


## Experiments

### Simulation Round 1 结果（Tab. 1）
| 任务 | 平均（有效提交） | 平均（全部） | 最高 |
|------|------------------|-------------|------|
| Place Empty Cup | 84.1 | 75.1 | 100.0 |
| Stack Bowls Three | 79.6 | 62.5 | 99.0 |
| Place Dual Shoes | 57.4 | 45.1 | 99.3 |
| Put Bottles Dustbin | 76.8 | 63.1 | 97.0 |
| Stack Blocks Three | 51.9 | 40.8 | 100.0 |
| Classify Tactile | 73.0 | 26.1 | 100.0 |

- 最高分 JD-TFS（AnchorDP3）103.31/105
- 多数团队>60 分，Round 1 难度适中

### Simulation Round 2 结果（Tab. 2）
| 任务 | 平均 | 最高 |
|------|------|------|
| Blocks Ranking RGB | 42.4 | 100.0 |
| Place Dual Shoes | 45.0 | 98.0 |
| Put Bottles Dustbin | 51.8 | 100.0 |
| Stack Blocks Three | 50.2 | 100.0 |
| Place Phone Stand | 43.8 | 100.0 |
| Place Object Scale | 32.8 | 100.0 |

- 冠军 JD-TFS 596/600，亚军 TSAIL-HRL 580/600
- 域随机化后分数显著下降，R1 最高 97-100% → R2 平均 42-52%

### Real-World Round 结果（Tab. 3）
| 任务 | 平均 | 最高 |
|------|------|------|
| Pour Water | 1.31 | 6.0 |
| Fold Towel | 0.30 | 2.1 |
| Fold Shorts | 0.59 | 3.8 |
| Stack Plates | 6.80 | 17.0 |
| Cap Pen | 0.58 | 3.1 |

- 最佳团队 TSAIL-HRL 仅 26.4/100
- 可变形物体（Fold Towel 0.30, Fold Shorts 0.59）特别困难
- Stack Plates（6.80）相对最高但仍远低于满分

### 关键量化发现
- AnchorDP3：98.7% 仿真成功率，稀疏 keypose 使训练数据多样性提升 14.5x
- MOMODA：双鞋任务从 VLA π0 的 48.2% 提升到 95.1%（100→3000 训练集）
- 3D 模态优势：AnchorDP3 和 SEM 均使用显式 3D 表示，优于纯 2D VLA 方案
- 真实世界 Cap Pen：TSAIL-HRL 轨迹正确但最终插入偏差导致低分（3.1），揭示 outcome-based 评估的局限性


## Limitations

1. **竞赛报告而非方法论文**：不提出单一新方法，而是汇总竞赛发现。定量分析受限于各团队提交的策略差异。
2. **评估偏差**：outcome-based 评估（二值成功/失败），不奖励部分进展。Cap Pen 案例显示接近成功的策略被严重低估。
3. **仿真-真实差距巨大**：仿真 Round 1 最高 103/105，真实世界最高 26.4/100，揭示 Sim-to-Real 仍是核心挑战。
4. **可变形物体特别困难**：Fold Towel 0.30/20, Fold Shorts 0.59/20，现有方法几乎无法处理。
5. **数据质量依赖**：真实世界演示存在噪声（不一致初始状态、重复抓取、臂抖动），需人工预处理。
6. **统一模型的权衡**：强制单模型解所有任务导致任务间负迁移，长视界和可变形任务被刚性任务拖累。
7. **触觉任务有限**：仅 1 个触觉分类任务，未充分探索触觉-视觉融合策略。
8. **语言指令泛化不足**：评估时指令 unseen，但训练时指令多样性不够，导致语义接地困难。


## Key Takeaways

1. **显式 3D 表示优于纯 2D VLA**：AnchorDP3 和 SEM 均采用 3D 点云/空间增强，优于纯多视图 2D 的 VLA 方案。对双臂 DLO 操控的启示：DLO 的 3D 形状表示（关键点/点云）应作为策略核心输入。
2. **稀疏动作表示的价值**：AnchorDP3 的 keypose（10-30 个/轨迹）比密集动作序列（20-25Hz）更高效，14.5x 数据多样性提升。对 DLO 操控的启示：DLO 轨迹可抽象为"抓取-移动-释放"等关键姿态序列。
3. **与 [[mu2025robotwin]]（RoboTwin 1.0/2.0）直接关联**：本竞赛基于 RoboTwin 平台，提供了该基准的首个大规模社区评估结果。
4. **可变形物体是瓶颈**：真实世界 Fold Towel（0.30）和 Fold Shorts（0.59）极低分说明可变形物体操控仍远未解决。支撑 [[deformable-linear-object]] 和 [[sim-to-real]] 的核心挑战。
5. **与 [[zhang2021dair]]（DAIR）互补**：DAIR 解决双臂 RL 的支配/冲突问题（注意力层面），RoboTwin 挑战赛验证了双臂协作在更复杂任务（可变形物体、长视界）下的实际表现。
6. **对本研究方向的启示**：双臂 DLO 操控应采用 3D 表示+稀疏动作+统一模型范式。RoboTwin 2.0 平台可用于仿真评估，但真实世界迁移需要更好的 Real2Sim 参数估计（如 [[kuroki2025gendom]] 的方法）。

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[tactile-sensing]]
- [[bimanual-manipulation]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[chen-tianxing|Chen, Tianxing]]
- [[zhang-yuhao|Zhang, Yuhao]]
