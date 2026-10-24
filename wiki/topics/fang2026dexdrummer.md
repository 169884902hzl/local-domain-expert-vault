---
title: "DexDrummer: In-hand, contact-rich, and long-horizon dexterous robot drumming"
tags: [manipulation, RL, sim-to-real, bimanual, planning]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "提出分层式灵巧鼓手机器人框架 DexDrummer，高层用参数化运动基元+残差 RL 实现鼓棒轨迹跟踪，低层用接触靶向奖励（指尖接触、支点奖励、手臂能量惩罚、接触课程）训练手指驱动的灵巧操控策略，在仿真中双臂 6 曲风 F1 达 1.87x 基线，真实世界闭环 F1=1.0。"
authors: "Fang, Hung-Chieh; Xie, Amber; Grannen, Jennifer; Llontop, Kenneth; Sadigh, Dorsa"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XTVA5SK5"
---
## 摘要

Performing in-hand, contact-rich（接触丰富）, and long-horizon（长时序） dexterous manipulation（灵巧操控） remains an unsolved challenge in robotics. Prior hand dexterity works have considered each of these three challenges in isolation, yet do not combine these skills into a single, complex task. To further test the capabilities of dexterity, we propose drumming as a testbed for dexterous manipulation（灵巧操控）. Drumming naturally integrates all three challenges: it involves in-hand control for stabilizing and adjusting the drumstick with the fingers, contact-rich（接触丰富） interaction through repeated striking of the drum surface, and long-horizon（长时序） coordination when switching between drums and sustaining rhythmic play. We present DexDrummer, a hierarchical object-centric bimanual（双臂） drumming policy trained in simulation with sim-to-real（仿真到真实迁移） transfer. The framework reduces the exploration difficulty of pure reinforcement learning（强化学习） by combining trajectory planning with residual RL corrections for fast transitions between drums. A dexterous manipulation（灵巧操控） policy handles contact-rich（接触丰富） dynamics, guided by rewards that explicitly model both finger-stick and stick-drum interactions. In simulation, we show our policy can play two styles of music: multi-drum, bimanual（双臂） songs and challenging, technical exercises that require increased dexterity. Across simulated bimanual（双臂） tasks, our dexterous（灵巧）, reactive policy outperforms a fixed grasp policy by 1.87x across easy songs and 1.22x across hard songs F1 scores. In real-world tasks, we show song performance across a multi-drum setup. DexDrummer is able to play our training song and its extended version with an F1 score of 1.0.

## 中文简述

提出基于强化学习的抓取方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、仿真到真实迁移、双臂操控、运动规划

## 关键贡献

1. **击鼓作为灵巧操控测试平台**：首次将手中操控、接触丰富交互和长时序鲁棒性统一到击鼓任务中，设计了 bimanual multi-drum 和 unimanual uni-drum 两类环境
2. **分层式 DexDrummer 框架**：高层策略用参数化运动基元生成鼓棒轨迹，经运动规划转换为手臂动作，再用残差 RL 进行校正；低层灵巧策略用接触靶向奖励处理手中和外部接触
3. **Contact Curriculum（接触课程）**：训练初期禁用鼓棒-鼓面接触，使策略先在自由空间学会轨迹跟踪，再逐步引入接触动力学，解决小幅度手指动作被外部接触力抵消的问题
4. **真实世界验证**：在 Franka + Tesollo DG-5F 硬件上展示 Sim-to-Real 迁移，闭环 F1=1.0
## 结构化提取

- **Problem**: 灵巧操控领域缺乏同时整合手中操控、接触丰富交互和长时序协调的统一测试平台和方法
- **Method**: 分层式框架（高层参数化运动基元 + 残差 RL 校正；低层接触靶向奖励训练灵巧策略），PPO 训练，ManiSkill3 仿真，域随机化 Sim-to-Real
- **Tasks**: 双臂多鼓歌曲演奏（仿真，6 种风格 Easy/Hard）、单臂单鼓高速练习（仿真+真实）、双臂双鼓歌曲（真实）
- **Sensors**: 关节本体感知（关节位置、速度）、鼓棒位姿（涂色标记 + RealSense RGB-D 相机 + 颜色分割 + 深度投影）
- **Robot Setup**: 2× Franka Panda（7-DOF）+ 2× Tesollo DG-5F（20-DOF 灵巧手），完整鼓组（仿真：snare/tom/ride/hi-hat/crash；真实：snare + cymbal）
- **Metrics**: F1 Score（歌曲演奏准确度）、Stick Hold Ratio（鼓棒保持时间比例）、Trajectory Error（轨迹跟踪误差）、Energy Consumption（能耗）
- **Limitations**: 歌曲降速 3×、仅 20 秒时长、真实仅 2 鼓、鼓棒追踪依赖颜色标记、无 Sim-to-Real gap 定量分析
- **Evidence Notes**: Reactive Grasp 在 Easy 歌曲 F1 超 Fixed Grasp 1.87x；Finger-driven 在高 BPM 下轨迹误差更低、能耗更低；Contact Curriculum 对 120-200 BPM F1 至关重要；Motion Planning + Residual RL F1=1.0 vs 纯 RL F1=0.5；真实世界闭环 F1=1.0（seen/extended），可泛化到 unseen 转换
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 版本，含正文、表格、参考文献和附录）
- Evidence Coverage: 完整覆盖方法、实验、消融、真实世界实验和附录
- Confidence: high
- Summary: 提出分层式灵巧鼓手机器人框架 DexDrummer，高层用参数化运动基元+残差 RL 实现鼓棒轨迹跟踪，低层用接触靶向奖励（指尖接触、支点奖励、手臂能量惩罚、接触课程）训练手指驱动的灵巧操控策略，在仿真中双臂 6 曲风 F1 达 1.87x 基线，真实世界闭环 F1=1.0。

## Problem

灵巧操控领域的现有工作通常将三个核心挑战孤立研究：
1. **手中操控**（in-hand control）：用手指稳定和调整物体姿态
2. **接触丰富交互**（contact-rich interaction）：反复与外部表面产生力接触
3. **长时序协调**（long-horizon coordination）：在长时间跨度内维持稳定操控

尚无工作将三者统一到单一任务中。本文提出将**击鼓**作为灵巧操控的测试平台——击鼓天然融合了这三项挑战：手指需在手中调整鼓棒、反复击打鼓面产生丰富接触、在多鼓之间切换并维持节奏。

## Method

### 整体架构
分层式、以物体为中心的架构，受 [11, 8] 启发：
- **高层策略**：从 MIDI 音乐输入生成参数化运动基元 → 鼓棒任务空间轨迹 → 通过相对位姿偏移转换为末端执行器运动 → 运动规划生成手臂标称指令 → **残差 RL** 学小幅度校正
- **低层灵巧策略**：处理接触丰富的手指-鼓棒和鼓棒-鼓面交互

### 奖励函数设计（Table I）
**手中接触奖励（In-Hand Contact Rewards）**：
1. **Fingertip Contact**：`exp(-1/(n_contacts + ε))`，鼓励指尖接触鼓棒（权重 1.0）
2. **Fulcrum Reward**：惩罚拇指和食指到鼓棒的平均距离，模拟人类击鼓的支点握法（权重 1.0）
3. **Arm Energy Penalty**：`||τ_arm|| + ||v_arm||`，惩罚手臂运动以激励手指驱动（权重 0.03）

**外部接触奖励（External Contact Rewards）**：
1. **Trajectory Reward**：`1_is_grasped · g(||p_stick - p̂_stick||)`，引导鼓棒跟踪参考轨迹（权重 2.0）
2. **Contact Curriculum**：训练前 10000 步禁用鼓棒-鼓面碰撞，让策略先学会自由空间轨迹跟踪，再引入接触力

**任务奖励**：Drum Hit——在正确时间窗口击中鼓面的稀疏奖励（权重 1.0）

### 参考轨迹生成
用正弦波建模击鼓动作，在击打位置之间插值生成鼓棒尖端轨迹。

### 训练配置
- 算法：PPO，60M 步（双臂任务）/ 40M 步（单臂任务）
- 框架：ManiSkill3
- 网络架构：3 层 MLP，隐藏维度 512
- γ=0.8，GAE λ=0.9，1024 并行环境
- Sim-to-Real：域随机化（本体感知噪声 N(0, 0.05²)、鼓棒摩擦系数 U(-0.2, 0.2)、控制增益 U(0.9, 1.1)）

### 硬件设置
- 2× 7-DOF Franka Panda 手臂
- 2× 20-DOF Tesollo DG-5F 灵巧手
- 策略推理频率 20 Hz，PID 关节位置控制器 100 Hz
- 鼓棒末端涂色，通过颜色分割 + RealSense 深度相机追踪鼓棒位姿

## Experiments

### 实验设置
- **仿真**：6 种音乐风格（Easy/Hard 各一曲），Easy 用 400 步（20 秒）测长时序稳定性，Hard 用 200 步（10 秒）测复杂节奏
- **真实世界**：军鼓 + 镲片双鼓设置；评估 seen/extended/unseen 三种曲目
- **Finger-Driven Control 任务**：单鼓高速击打，最高 240 BPM（4 次/秒）

### 主要结果

**Q1: 灵巧性是否必要？**
| 方法 | Easy Song F1 | Easy Hold Ratio | Hard Song F1 | Hard Hold Ratio |
|------|-------------|-----------------|-------------|-----------------|
| Reactive Grasp (本文) | 显著高于 baseline | 显著高于 baseline | 高于 baseline | 略高于 baseline |
| Fixed Grasp | baseline | baseline | baseline | baseline |

- Reactive Grasp 在 Easy 歌曲上 F1 超过 Fixed Grasp **1.87x**，Hold Duration 也大幅领先
- 在 Hard 歌曲上优势缩小到 **1.22x**，因为 Fixed Grasp 只需学习低维手臂动作即可处理复杂鼓间切换
- **结论**：长时序接触场景下灵巧操控必不可少；短时序复杂节奏场景存在灵巧性 vs 学习复杂度的权衡

**Q2: 手指驱动 vs 手臂驱动**
- BPM 越高，finger-driven 的轨迹误差越低，与 arm-driven 的差距越大
- Finger-driven 能耗显著更低
- 定性上 finger-driven 动作更自然、更接近人类鼓手；arm-driven 出现不自然甚至危险姿态

**Q3: Contact Curriculum 消融**
- 移除接触课程后轨迹误差大幅上升，F1 在大部分 BPM 下显著下降
- 唯一例外：240 BPM（动作幅度极小，手指运动本身容易学）
- 原因假设：手指动作幅度小，容易被外部接触力抵消

**Q4: 高层策略消融**
| 配置 | F1 Score |
|------|----------|
| Motion Planning + Residual RL（完整） | 1.0 |
| 仅 Motion Planning（无 Residual RL） | 0.8 |
| 纯 RL（无 Motion Planning） | 0.5 |

- 运动规划提供全局协调的结构先验，残差 RL 对局部校正至关重要

**Q5: 真实世界 Sim-to-Real**
| 曲目 | Open-loop F1 | Closed-loop F1 |
|------|-------------|----------------|
| Seen (ccdd) | < 1.0 | 1.0 |
| Extended (ccccdddd) | < 1.0 | 1.0 |
| Unseen (ccddccdd) | < 1.0 | 接近 1.0 |

- 闭环控制优于开环重放，说明策略能自适应真实世界动力学
- 未见过的鼓间切换（如 d→c）也能处理，可能得益于高层轨迹引导的条件输入
- 真实击镲时握持较松（镲片不固定、接触弱），击鼓垫后握持变紧（鼓垫固定、接触强），体现了 reactive grasp 的自适应性

### 未报告的证据
- 无定量 Sim-to-Real gap 分析（如仿真 vs 真实 F1 对比）
- 无多轮重复实验的标准差/置信区间
- 真实世界双臂全鼓组结果仅在网站视频展示，无定量数据
- 真实世界 Finger-Driven Control 仅定性展示（supplemental video）

## Limitations

1. **速度限制**：所有歌曲降速 3 倍，无法以人类速度演奏多鼓曲目
2. **时序范围**：真实世界实验仅测试至 400 步（20 秒），实际歌曲通常 3-5 分钟
3. **真实世界鼓组**：仅展示 2 鼓双臂设置，未展示全鼓组
4. **Sim-to-Real 技术**：仅使用域随机化，未探索更高级的迁移方法
5. **鼓棒追踪**：依赖涂色标记 + 颜色分割 + 深度相机，不鲁棒且需要手动标定
6. **泛化性**：仅在特定曲目上训练和测试，未见全新节奏结构的泛化结果
7. **双臂协调**：未详细分析左右手之间的干扰和协调机制

## Key Takeaways

1. **Contact Curriculum 是解决接触丰富灵巧操控的关键技巧**：先用自由空间学会轨迹跟踪，再引入接触力。这一思路可直接迁移到 DLO 操控——DLO 接触桌面的力同样会抵消手指的微小调整
2. **Arm Energy Penalty 促使手指驱动**：通过惩罚手臂运动迫使策略发展手指精细控制，适用于需要精细操控的 DLO 任务（如穿线、打结）
3. **分层规划 + 残差 RL 降低探索难度**：纯 RL 在高维动作空间（双臂 14 DOF + 双手 40 DOF）中探索效率极低；先用运动规划生成粗轨迹，再用 RL 做精细校正，将 F1 从 0.5 提升到 1.0
4. **以物体为中心的轨迹规划**：以鼓棒轨迹而非关节空间为规划主体，降低了任务维度。对 DLO 可类比：以绳子端点轨迹为规划主体
5. **击鼓作为灵巧操控 benchmark**：击鼓是一个可量化（F1 score、hold ratio）、可复现、具有明确成功标准的测试平台，比定性展示更具科学价值

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[bimanual-manipulation]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[fang-hung-chieh|Fang, Hung-Chieh]]
- [[sadigh|Sadigh, Dorsa]]
