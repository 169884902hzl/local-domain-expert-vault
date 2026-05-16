---
title: "MOBIUS: A multi-modal bipedal robot that can walk, crawl, climb, and roll"
tags: [manipulation, imitation, RL, planning, grasping]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模式的统一形态硬件与无缝切换，并在真实硬件上验证引体向上和儿童滑梯攀爬。"
authors: "Schperberg, Alexander; Tanaka, Yusuke; Cairano, Stefano Di; Hong, Dennis"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "C7EJ28JA"
---
## 摘要

This paper presents the MOBIUS platform, a bipedal robot capable of walking, crawling, climbing, and rolling. MOBIUS features four limbs, two 6-DoF arms with two-finger grippers for manipulation（操控） and climbing, and two 4-DoF legs for locomotion--enabling smooth transitions across diverse terrains without reconfiguration. A hybrid control architecture combines reinforcement learning（强化学习） for locomotion and force control for compliant contact interactions during manipulation（操控）. A high-level MIQCP planner autonomously selects locomotion modes to balance stability and energy efficiency. Hardware experiments demonstrate robust gait transitions, dynamic climbing, and full-body load support via pinch grasp. Overall, MOBIUS demonstrates the importance of tight integration between morphology, high-level planning, and control to enable mobile loco-manipulation（操控） and grasping（抓取）, substantially expanding its interaction capabilities, workspace, and traversability.

## 中文简述

提出基于强化学习的抓取方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、强化学习、运动规划、抓取

## 关键贡献

1. 新型多模态机器人形态设计：两个 6-DoF 手臂（带双指刺状夹爪）+ 两个 4-DoF 腿，集成背部导轨实现跌落保护和滚动
2. 统一形态实现双足步行、爬行、滚动、垂直自由攀爬和引体向上，无需零件替换或附肢装卸——据作者所知是首个实现上述全部功能的中大型双足机器人
3. 系统级软件栈：自适应导纳力控 + Reference Governor 安全保证 + model-free RL 运动控制 + MIQCP 高层模式选择规划器
## 结构化提取

- Problem: 多模态机器人需要硬件重构或专精单一模式，缺乏统一平台同时实现步行/爬行/攀爬/滚动
- Method: 统一形态硬件（6-DoF 手臂+夹爪、4-DoF 腿、背部导轨）+ RL 运动 + 导纳力控+RG + MIQCP 规划
- Tasks: 双足步行、四足爬行、后向滚动、垂直攀爬（儿童滑梯）、引体向上、模式间切换
- Sensors: 关节编码器、IMU、T265 VIO-SLAM (200Hz)、D435i RGB-D (30Hz)、力/力矩传感器
- Robot Setup: MOBIUS，10.3 kg 双足机器人，2×6-DoF 手臂 + 2×4-DoF 腿，MuJoCo 仿真 → 硬件零样本迁移
- Metrics: 速度跟踪误差、脉冲扰动容忍阈值、成功率（攀爬 8/10、引体 9/10）、力跟踪误差改善、EVC (Energy per Visited Cell)、CoT (Cost of Transport)
- Limitations: 齿轮疲劳、RL 泛化性、滚动状态估计不可靠、MIQCP 离线规划、双足能耗高、攀爬开环
- Evidence Notes: 全部实验结果来自真实硬件验证（步行、爬行、攀爬、引体向上）+ MuJoCo 仿真（RL vs MPC 对比、domain randomization 验证、高度图扰动）。未提供定量 sim-to-real gap 分析或户外测试数据
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML, 106K chars)
- Evidence Coverage: complete (主文 + 附录 Supplementary Material 全部精读)
- Confidence: high
- Summary: 提出 MOBIUS 多模态双足机器人平台，集成 RL 运动、导纳力控与 Reference Governor 安全约束、MIQCP 高层规划，实现步行/爬行/攀爬/滚动四种模式的统一形态硬件与无缝切换，并在真实硬件上验证引体向上和儿童滑梯攀爬。


## Problem

现有多模态机器人要么依赖机械重构切换运动模式（增加质量和复杂度），要么专精单一模式（缺乏适应性）。自由攀爬机器人（如 SCALER）牺牲了地面机动性，而通用步行机器人无法执行垂直攀爬。需要一个不重构硬件即可在步行、爬行、攀爬和滚动之间自主切换的统一平台。


## Method

### 硬件架构
- 总重 10.3 kg
- 两个 6-DoF 手臂：混合并联机构连杆，210° 工作空间，两指刺式夹爪（Tanaka et al. 2021 设计）既做灵巧夹爪又做承重接触面
- 两个 4-DoF 腿：平脚底端，105° 足间距
- 背部弯曲导轨：被动引导跌落后恢复姿态 + 滚动运动
- 前臂比下半身重 55%，这种不对称性有利于爬行-双足模式切换但增加双足运动难度
- 高减速比正齿轮执行器，AGMA 疲劳分析估计约 2.8×10^5 周期寿命

### RL 运动控制（PPO）
- POMDP 建模，PPO 训练
- 观测空间：躯干状态 + 关节编码器 + 前一动作 + 期望速度 + N=15 步历史
  - 双足模式：ℝ^416，爬行模式：ℝ^608
- 动作空间：目标关节位置，移动平均滤波平滑
- 奖励函数：平衡稳定性（惩罚垂直速度、角速度）、跟踪精度（速度跟踪奖励）、平滑性（惩罚动作变化、足滑）
- 两阶段训练：平地 300M 步 → 粗糙地形 100M 步
- 大规模 domain randomization：质量 ±5kg、摩擦 ±0.3~0.5、执行器增益/偏置 ±20、观测延迟、随机踢击

### 导纳力控 + Reference Governor
- 导纳控制器映射测量力/力矩到期望运动
- 自动调谐模块在线适应控制器增益（Schperberg et al. 2023），力跟踪误差改善 45%
- 新增 Reference Governor (RG) 基于最大输出容许集 (MOAS) 强制安全约束
  - 离线计算 MOAS：对采样状态/参考组合做有限时域仿真，保留满足位置/速度/力约束的样本
  - 在线查询：KD-Tree 存储离散 MOAS 样本，对数时间最近邻搜索
  - 若当前参考不可行，替换为最近可行参考

### MIQCP 高层规划器
- Mixed Integer Quadratic Constraint Programming
- 网格化 2D 地图上的联合路径规划 + 离散模式选择
- Big-M 编码 if-then 逻辑：地形约束（圆形区域）+ 矩形障碍物避障
- 目标函数：最大化探索覆盖 + 目标到达 + 最小化模态切换能量代价
- 模态惩罚：爬行最低（最稳定高效）→ 双足较高 → 滚动最高（定位不稳定）
- Gurobi 求解器，20m×20m 地图约 10-11 秒

### 仿真到硬件
- MuJoCo 高保真仿真，零样本 sim-to-real 迁移
- RL 策略 60 Hz，底层 PID 电机控制 300 Hz
- 状态估计：T265 VIO-SLAM (200 Hz) + OptiState（Kalman filter + GRU + ViT autoencoder），互补滤波融合
- Visual-servo：YOLOv8 检测把手 → PID 控制 → IK → 关节角


## Experiments

### 主要结果

| 实验 | 结果 |
|------|------|
| 双足步行最大速度 | 0.1 m/s（侧向）, 0.25 rad/s（偏航） |
| 爬行最大速度 | 0.4 m/s（侧向）, 0.6 rad/s（偏航） |
| 滚动瞬时速度 | 0.7 m/s |
| 脉冲扰动鲁棒性 | RL 稳定至 0.25 m/s vs MPC 在 0.05 m/s 失败 |
| 儿童滑梯攀爬 | 8/10 成功 |
| 引体向上 | 9/10 成功 |
| 夹爪最大支撑力 | z轴 124.2±24.5 N（刺状啮合）, x轴 23.6±4.1 N（摩擦） |
| 导纳控制力跟踪误差改善 | 45%（auto-tuning vs 手动调谐） |
| 模态能量效率 | 爬行 5.11 J/cell < 滚动 21.96 < 双足 26.89 |

### RL vs Model-based 对比
- 双足模式：RL 全面优于 MPC，跟踪精度更高、跨轴耦合更小
- 爬行模式：RL 和 MPC 更接近，但 RL 在侧向和后退方向仍更优
- 原因分析：MOBIUS 的不对称动力学（重前臂）导致模型不准确，MPC 状态传播误差大

### 消融实验
- Reference Governor：无 RG 时位置/速度约束违反（0.0s, 2.5s, 10.0s），有 RG 时全程在 MOAS 内
- Auto-tuning：力跟踪误差降低 45%
- MIQCP 超参数：探索与目标权重均衡 + 低/高 ε/M 组合 → 最低 EVC；模式切换率约 25%/步

### 缺失证据
- 无定量 sim-to-real gap 分析（仅报告"零样本迁移"）
- 无户外或非结构化环境实验
- Visual-servo 仅在受控滑梯场景测试
- 爬升实验依赖开环轨迹，无闭环全身控制


## Limitations

1. 夹爪双重用途（抓取+步行）增加机械磨损，正齿轮在双足冲击载荷下易疲劳（~2.8×10^5 周期）
2. RL 策略依赖大量 domain randomization，对全新表面类型泛化能力存疑
3. 滚动模式状态估计不可靠（被动运动无法精确跟踪）
4. MIQCP 规划器离线运行（20m 地图 10-11s），需要预设地形知识，缺乏实时重规划能力
5. 双足运动能耗高（104 J/m vs 爬行 65 J/m）
6. 攀爬依赖开环轨迹，无闭环身体控制
7. 速度较慢（双足 0.1 m/s），实际部署受限


## Key Takeaways

1. **形态-控制协同设计**：MOBIUS 的核心思想是统一形态（不重构）支持多种运动模式，关键在于夹爪的"双角色"设计（灵巧夹爪 + 承重足端）和背部导轨的"双功能"（跌落保护 + 滚动轨道）
2. **RL 对复杂动力学机器人更有效**：当机器人动力学难以精确建模（如 MOBIUS 的不对称质量分布），model-free RL 显著优于传统 MPC，但代价是大量 domain randomization 和训练时间（400M 步）
3. **Reference Governor 是力控安全的实用方案**：离线计算 MOAS + KD-Tree 在线查询，为导纳力控提供了形式化的安全保证，且计算开销可控
4. **多模态规划的价值**：MIQCP 规划器表明多模态切换比单模态更高效（覆盖+能耗权衡），但离线规划限制了实际应用
5. **对 DLO 操控的启示有限**：本论文主要关注运动和多模态切换，夹爪力控和视觉伺服的方法可能对 DLO 夹持控制有参考价值，但场景差异较大

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[planning]]
- [[grasping]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[schperberg|Schperberg, Alexander]]
- [[tanaka-yusuke|Tanaka, Yusuke]]
- [[hong-dennis|Hong, Dennis]]
