---
title: "AsyncShield: A plug-and-play edge adapter for asynchronous cloud-based VLA navigation"
tags: [imitation, VLM, RL, sim-to-real, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束的自适应权衡，零样本泛化至异构底盘和多种 VLA 模型。"
authors: "Yang, Kai; Chu, Zedong; Guo, Yingnan; Wang, Zhengbo; Xie, Shichao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "JJGRWAN5"
---
## 摘要

While Vision-Language-Action (VLA) models have been demonstrated possessing strong zero-shot（零样本） generalization for robot control, their massive parameter sizes typically necessitate cloud-based deployment. However, cloud deployment introduces network jitter and inference latency, which can induce severe spatiotemporal misalignment in mobile navigation under continuous displacement, so that the stale intents expressed in past ego frames may become spatially incorrect in the current frame and lead to collisions. To address this issue, we propose AsyncShield, a plug-and-play asynchronous control framework. AsyncShield discards traditional black-box time-series prediction in favor of a deterministic physical white-box spatial mapping. By maintaining a temporal pose buffer and utilizing kinematic transformations, the system accurately converts temporal lag into spatial pose offsets to restore the VLA's original geometric intent. To balance intent restoration fidelity and physical safety, the edge adaptation is formulated as a constrained Markov decision process (CMDP). Solved via the PPO-Lagrangian algorithm, a reinforcement learning（强化学习） adapter dynamically trades off between tracking the VLA intent and responding to high-frequency LiDAR obstacle avoidance hard constraints. Furthermore, benefiting from a standardized universal sub-goal interface, domain randomization, and perception-level adaptation via Collision Radius Inflation, AsyncShield operates as a lightweight, plug-and-play module. Simulation and real-world experiments demonstrate that, without fine-tuning any cloud-based foundation models, the framework exhibits zero-shot（零样本） and robust generalization capabilities, effectively improving the success rate and physical safety of asynchronous navigation.

## 中文简述

提出基于强化学习的导航方法，具有零样本泛化特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **云端 VLA 导航边缘适配器**：用确定性白箱 SE(2) 空间映射替代传统黑箱时间序列预测，通过时间姿态缓冲和运动学变换将时间滞后精确转化为空间偏移；将边缘适配建模为 CMDP，PPO-Lagrangian 求解器实现意图恢复与避障约束的自适应权衡。
2. **强即插即用能力**：标准化 Universal Local Sub-goal 接口（5 个 waypoints，20cm 间距），无需微调云端 VLA 即可零样本适配不同 VLA 模型和异构机器人底盘，结合 Collision Radius Inflation 感知级适配实现跨实体泛化。
## 结构化提取

- **Problem**: 云端 VLA 模型的推理延迟和网络抖动导致移动导航中的时空错位，使过期指令引发碰撞；现有异步控制方法（面向机械臂设计）迁移到移动平台时逻辑失效
- **Method**: SE(2) 白箱空间映射（时间姿态缓冲 + 几何重投影） + CMDP 建模 + PPO-Lagrangian 求解 + 域随机化训练 + Collision Radius Inflation 跨实体适配
- **Tasks**: 移动机器人导航（点目标导航、人员跟随、物体目标导航）
- **Sensors**: 2D LiDAR (144 点) + 轮式里程计
- **Robot Setup**: 仿真：通用差速底盘、Doggo 四足、Racecar Ackermann 车辆；真实世界：Unitree Go2 四足机器人
- **Metrics**: SR（成功率）、CTE（交叉跟踪误差）、RER（风险暴露率）、TTG（到达目标时间）
- **Limitations**: 仅 SE(2) 2D 环境；单一 2D LiDAR 传感器；VLA 输出需标准化为 waypoints 格式
- **Evidence Notes**: 600 episode 仿真主实验 + 3 组消融 + 跨 4 种实体验证 + 真实世界 3 种 VLA × 4 场景 × 5 trials = 60 次真实实验。证据充分，定量和定性分析完备。
## 本地引用关系

- [[brohan2023rt2]]
- [[chi2024diffusion]]
- [[kim2024openvla]]
- [[team2024octo]]
## 证据元数据

- Fulltext Quality: fulltext (via arXiv MCP, 2604.24086v1)
- Evidence Coverage: 完整覆盖方法论、实验结果、消融实验、跨实体验证和真实世界部署
- Confidence: high
- Summary: 提出 AsyncShield 即插即用边缘适配框架，通过 SE(2) 白箱空间映射修正云部署 VLA 的时空错位，用 PPO-Lagrangian 实现意图跟踪与避障安全约束的自适应权衡，零样本泛化至异构底盘和多种 VLA 模型。


## Problem

云端部署的 VLA 模型因参数量大导致推理延迟和网络抖动，在移动导航中产生**时空错位**（spatiotemporal misalignment）：过期的 VLA 指令（基于过去 ego frame 生成）在当前帧中空间位置不正确，导致碰撞。现有异步控制方法（如 RTC、A2C2）面向固定基座机械臂设计，通过时间序列平滑拼接或局部残差修正，迁移到移动平台时存在**根本性逻辑失败**：盲目沿过期路径平滑拟合会驶向动态障碍物。

核心洞察：**"Latency is Geometry"** —— 延迟本质上是空间偏移问题，而非单纯的时间预测问题。


## Method

### 1. 时空意图重对齐（Spatio-Temporal Intent Realignment）

- **时间姿态缓冲**：边缘设备维护环形缓冲区 B = {(t_k, T^O_W(t_k))}，以 f_edge Hz 记录机器人里程计。当 VLA 数据包到达时（锚定时间戳 t_a），通过线性插值（平移）和最短路径角插值（航向）恢复历史姿态。
- **几何重投影**：设 P^A = {p̄^A_i} 为 VLA 在锚定 ego frame 生成的 N 个 waypoints，当前 ego frame (t > t_a) 的重对齐 waypoints 通过解析 SE(2) 变换计算：
  p̄^E_i(t) = (T^O_W(t))^{-1} · T^O_W(t_a) · p̄^A_i
  关键优势：每次新 VLA 数据包重置时间锚点，里程计漂移严格限制在单个通信周期内，避免全局发散。

### 2. CMDP 建模与 PPO-Lagrangian 求解

- **状态空间**：s_t = [o^geo_t, o^lidar_t]，其中 o^geo_t ∈ R^{10}（5 个前瞻采样点，0.2m 间隔），o^lidar_t ∈ R^{144}（2D LiDAR）
- **动作空间**：a_t = (Δx_t, Δy_t)，定义为 Universal Local Sub-goal，由底层控制器转为速度指令
- **奖励函数**：轨迹保真度 + 平滑性（flow 方向一致性 + 交叉跟踪误差 + 动作平滑性），与避障解耦
- **安全约束**：基于最小 LiDAR 距离 d_min，当 d_min < R_safe 时触发代价项（指示函数 + 连续惩罚）
- **PPO-Lagrangian**：对偶变量 λ 自适应调整，当 VLA 意图有碰撞风险时 λ 激增，迫使策略优先安全

### 3. 训练环境与运动学域随机化

- 10m × 10m 工作区，6 静态 + 6 动态障碍物
- 延迟采样 δ ~ U(0.3, 1.5)s，丢包率 p_loss ∈ [0, 0.2]
- 执行器随机化：一阶滞后系数 τ ~ U(0.2, 0.9)、最大加速度 a_max ~ U(0.5, 1.5) m/s²、高斯噪声 σ ~ U(0.05, 0.20)、角偏差 b_ω ~ U(-0.05, 0.05) rad/s
- 训练框架：OmniSafe

### 4. Collision Radius Inflation

跨实体适配的感知级机制：对原始 LiDAR 扫描距离减去膨胀补偿值，等效于在观测空间中把障碍物推近，使基策略无需重训即可适配更大碰撞体积的实体。


## Experiments

### 主实验（仿真，OmniSafe 框架）

**设置**：600 episodes，10m × 10m 随机地图，7 静态 + 4 动态障碍物，±40% 运动学域随机化

**网络条件**：
- Ideal（快更新）：~200ms 确定性延迟，零丢包
- Non-ideal（混合退化）：重尾延迟混合分布（90% U(0.15, 0.25)s + 10% U(0.5, 1.5)s）、15% 丢包、5% 瞬态中断 U(1.0, 2.0)s

**定量结果（Table I）**：

| Method | SR (Ideal) | CTE (Ideal) | RER (Ideal) | SR (Non-ideal) | CTE (Non-ideal) | RER (Non-ideal) |
|--------|-----------|-------------|-------------|----------------|-----------------|-----------------|
| **Ours** | **80.0%** | 0.717m | **1.2%** | **76.7%** | **0.725m** | **1.3%** |
| A2C2 | 56.7% | 0.937m | 1.5% | 43.3% | 1.146m | 1.7% |
| RTC | 40.0% | 0.673m | 3.0% | 30.0% | 1.178m | 4.0% |
| Naive | 20.0% | 1.175m | 5.2% | 16.7% | 1.272m | 5.5% |

**关键发现**：
- CTE 悖论：RTC 的 CTE 最低（0.673m）但 SR 仅 40%，盲目平滑跟踪 ≠ 安全
- AsyncShield 在共享成功集上 TTG 退化最小（8.87s → 9.29s），鲁棒决策

### 消融实验（Table II）

| 变体 | SR (Ideal) | SR (Non-ideal) | RER (Non-ideal) |
|------|-----------|----------------|-----------------|
| Full | 80.0% | 76.7% | 1.3% |
| w/o 时间对齐 | 53.3% | 36.7% | 3.6% |
| w/o RL Adapter | 66.7% | 53.3% | 1.4% |
| w/o 安全约束 | 40.0% | 23.3% | 4.7% |

- 去除时间对齐影响最大（Non-ideal SR -40pp），验证 "Latency is Geometry" 核心论点
- 去除安全约束导致 RER 飙升（1.3% → 4.7%），PPO-Lag 安全基线不可或缺
- 去除 RL Adapter 替换为 DWA 规划器，CTE > 1.2m，传统代价规划器难以平衡过期意图与安全

### 跨实体验证（Table III，仿真）

| 实体 | SR | RER |
|------|-----|------|
| Doggo A（四足） | 78.0% | 1.25% |
| Doggo B | 76.0% | 1.31% |
| Racecar A（Ackermann 转向） | 79.0% | 1.20% |
| Racecar B | 76.0% | 1.29% |

零样本部署到形态差异显著的实体，性能差异极小。

### 真实世界部署（Table IV）

硬件：Unitree Go2 四足机器人，边缘-云架构（板载 2D LiDAR + 里程计，云端 GPU 运行 VLA，Wi-Fi 基线 RTT ~200ms）

| Cloud VLA | Direct VLA | VLA + AsyncShield |
|-----------|-----------|-------------------|
| SocialNav（点目标导航） | 6/20 (30%) | **17/20 (85%)** |
| TrackVLA（人员跟随） | 8/20 (40%) | **16/20 (80%)** |
| Nav-R²（物体目标导航） | 5/20 (25%) | **18/20 (90%)** |

无需微调任何 VLA 模型，即插即用提升 SR 2-3.5 倍。


## Limitations

1. **2D 限制**：当前仅支持 SE(2) 平面环境，未扩展到 3D 非结构化环境（如楼梯、斜坡）
2. **仿真到真实差距**：尽管真实世界验证成功，但 OmniSafe 仿真器与真实物理环境仍有差距
3. **VLA 输出依赖**：框架假设云端 VLA 输出可标准化为 5 个 waypoints（20cm 间距），对输出格式有约束
4. **单一传感器**：仅使用 2D LiDAR，未利用多模态感知（相机、3D LiDAR）
5. **未来方向**：引入轻量多模态局部感知模型以增强安全冗余


## Key Takeaways

1. **"Latency is Geometry" 原则**：将异步延迟问题重新定义为空间对齐问题，用解析 SE(2) 变换替代黑箱预测。这一思想可推广到任何需要云端-边缘协作的机器人任务。
2. **CMDP + PPO-Lagrangian 的安全导航模式**：将意图跟踪与安全约束解耦，对偶变量自适应权衡，无需手动调参。适用于其他需要平衡任务性能与安全约束的 RL 导航场景。
3. **标准化接口设计的即插即用性**：Universal Local Sub-goal 接口使边缘模块独立于云端模型和底层底盘，工程实践价值高。
4. **Collision Radius Inflation 的跨实体策略**：通过感知级膨胀补偿而非模型级修改实现跨实体适配，简洁有效。
5. **对 DLO 操控的启发有限**：本工作聚焦移动导航而非操控，但其云-边缘异步架构和安全约束优化思路可为远程遥操作 DLO 任务提供参考。

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[yang-kai|Yang, Kai]]
- [[chu-zedong|Chu, Zedong]]
