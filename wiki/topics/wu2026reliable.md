---
title: "Toward reliable sim-to-real predictability for MoE-based robust quadrupedal locomotion"
tags: [imitation, RL, sim-to-real]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出 MoE-CTS 统一框架，将 Mixture-of-Experts 集成到学生编码器以增强多地形表征，并设计 RoboGauge 预测评估套件，通过 sim-to-sim 多维度指标（6 指标、7 地形、10 难度、9 域随机化）量化 Sim-to-Real 可迁移性，在 Unitree Go2 上实现 4 m/s 高速运动和 30 cm 障碍穿越。"
authors: "Wu, Tianyang; Guo, Hanwei; Wang, Yuhang; Yang, Junshu; Sui, Xinyang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XA4A8QAU"
---
## 摘要

Reinforcement learning（强化学习） has shown strong promise for quadrupedal agile locomotion, even with proprioception-only sensing. In practice, however, sim-to-real（仿真到真实迁移） gap and reward（奖励） overfitting in complex terrains can produce policies that fail to transfer, while physical validation remains risky and inefficient. To address these challenges, we introduce a unified framework encompassing a Mixture-of-Experts (MoE) locomotion policy for robust multi-terrain representation with RoboGauge, a predictive assessment suite that quantifies sim-to-real（仿真到真实迁移） transferability. The MoE policy employs a gated set of specialist experts to decompose latent terrain and command modeling, achieving superior deployment robustness and generalization via proprioception alone. RoboGauge further provides multi-dimensional proprioception-based metrics via sim-to-sim tests over terrains, difficulty levels, and domain randomizations, enabling reliable MoE policy selection without extensive physical trials. Experiments on a Unitree Go2 demonstrate robust locomotion on unseen challenging terrains, including snow, sand, stairs, slopes, and 30 cm obstacles. In dedicated high-speed tests, the robot reaches 4 m/s and exhibits an emergent narrow-width gait associated with improved stability at high velocity.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移

## 关键贡献

1. **RoboGauge 预测评估框架**：基于 MuJoCo 的 sim-to-sim 评估套件，通过 6 个本体感觉指标（ dof limits、dof power、velocity error、torque smoothness、orientation stability、ZMP margin + Coulomb friction margin）、7 种地形配置、10 个难度等级和 9 种域随机化，系统量化 Sim-to-Real 可迁移性，减少物理部署风险。
2. **MoE-CTS 运动策略**：将 Mixture-of-Experts 模块集成到 CTS（Concurrent Teacher-Student）框架的学生编码器中，通过门控网络动态分配 K 个专家子网络的权重，增强多地形和指令表征能力，仅依赖本体感觉即可实现鲁棒运动。
3. **高速运动与涌现步态**：在平地上使用相同训练配置达到 4.01 m/s 峰值速度，并在无显式运动约束下自主发展出窄基步态（narrow-width gait），提高高速稳定性。
## 结构化提取

- Problem: RL 四足运动策略的 Sim-to-Real Gap 和奖励过拟合导致策略迁移失败，且缺乏可靠的量化评估代理
- Method: MoE-CTS（Mixture-of-Experts 集成到 CTS 学生编码器）+ RoboGauge（基于 MuJoCo 的 sim-to-sim 预测评估框架，6 指标、7 地形、10 难度、9 域随机化）
- Tasks: 四足多地形运动（平地、波浪、斜坡、粗糙斜坡、上下楼梯、障碍）、高速平地运动（4 m/s）
- Sensors: 仅本体感觉（IMU 角速度、投影重力向量、关节位置、关节速度）
- Robot Setup: Unitree Go2 四足机器人，12 DOF，PD 控制 kp=20.0 kd=0.5，控制频率 50Hz，仿真频率 200Hz
- Metrics: RoboGauge 6 指标（dof limits、dof power、velocity error、torque smoothness、orientation stability、ZMP margin + friction margin）；真实世界：速度跟踪误差、生存率、峰值速度
- Limitations: 单一平台验证、仅本体感觉、未整合外部感知、未讨论专家数量选择和计算开销
- Evidence Notes: 全文可用，所有实验数据均有详细表格（Table III-VI, XII-XIV），消融研究完整（MoE 变体、训练策略），真实世界验证涵盖 5 种以上场景。动捕系统提供 ground truth 验证 RoboGauge 指标可靠性。
## 本地引用关系
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high (全文含附录，含所有实验数据表格、消融研究、训练细节)
- Confidence: high
- Summary: 提出 MoE-CTS 统一框架，将 Mixture-of-Experts 集成到学生编码器以增强多地形表征，并设计 RoboGauge 预测评估套件，通过 sim-to-sim 多维度指标（6 指标、7 地形、10 难度、9 域随机化）量化 Sim-to-Real 可迁移性，在 Unitree Go2 上实现 4 m/s 高速运动和 30 cm 障碍穿越。


## Problem

强化学习训练的四足运动策略在仿真中表现优异，但面临两个核心问题：
1. **Sim-to-Real Gap 与奖励过拟合**：策略倾向于过拟合仿真器的特定动力学，高训练奖励不能保证真实世界的稳定性，尤其是在复杂地形上。
2. **缺乏可靠的量化评估代理**：现有方法依赖直接物理验证，既危险又低效；训练环境指标与真实表现之间误差显著。


## Method

### 核心架构：MoE-CTS
- 基础框架：CTS（Concurrent Teacher-Student），同时优化教师和学生网络的 actor-critic
- **MoE 学生编码器**：替代标准学生编码器，包含 K 个并行专家子网络 {E_k} 和门控网络 g
  - 门控权重：ω_k = softmax(g(o_{t-H:t}))_k
  - 潜在状态：z_s = Σ ω_k · E_k(o_{t-H:t})
  - 负载均衡损失：L_load balance = Σ(ω̄_k - 1/K)²，防止单一专家主导
- 观测序列长度 H=5，输入包括 IMU 角速度、投影重力、关节位置/速度、速度指令、前一步动作

### POMDP 建模
- 状态空间：完整动力学信息（线速度、地形高度、环境潜在参数）
- 观测空间：仅本体感觉（IMU + 关节编码器），无外部传感器
- 动作空间：关节位置偏移，通过 PD 控制器（kp=20.0, kd=0.5）转换为力矩

### 训练配置
- 仿真环境：IsaacGym，8192 个并行 agent
- 控制频率 50Hz，仿真频率 200Hz
- 地形课程：7 种地形（flat、wave、slope、rough slope、stairs up/down、obstacle）
- 域随机化：摩擦系数、有效载荷、电机延迟、观测噪声等

### 训练策略改进
1. **动态速度跟踪精度调整**：根据地形难度和指令幅值自适应调节 σ，避免复杂地形上的跟踪不稳定
2. **指令课程**：从低速指令逐步扩展到高速，避免直接大范围指令训练导致不稳定步态
3. **极端指令采样**：10% 概率零速指令、20% 概率最大速度指令组合
4. **动态指令采样**：保证累积指令距离超过地形升级阈值

### RoboGauge 评估框架
- 三层流水线架构：
  1. **BasePipeline**：单环境原子评估
  2. **Multi/Level Pipeline**：并行难度评估和域随机化
  3. **Stress Pipeline**：综合鲁棒性评分
- 评分方法：
  - 加权几何平均计算执行质量分数 Q（惩罚不均衡表现）
  - Worst-Case Mean 聚合运动目标得分（取最低 50% 均值）
  - 二分搜索确定最大可通行难度等级
  - 重叠评分函数：S = α(L*-1) + β·Q(L*)，β > α 确保高低难度间平滑过渡
- 稳定性指标：ZMP margin（零矩点到支撑多边形中心的距离误差）、Coulomb friction margin（摩擦锥边界的法力加权平均余量）


## Experiments

### 对比基线
- **DreamWaQ**：非对称 actor-critic + 变分估计器
- **HIM**：混合内部模型 + 对比学习
- **CTS**：非对称 teacher-student + 重建监督

### RoboGauge 指标可靠性（Q1）
- 使用 NOKOV Mars18H 动捕系统（12 相机，90Hz）获取真实世界 ground truth
- 对比训练环境指标误差 vs RoboGauge 指标误差
- 结果：训练环境指标误差显著大于 RoboGauge，RoboGauge 更准确反映真实表现

### RoboGauge 基线对比（Q2）
- 所有基线在 IsaacGym 中以 8192 agent 统一训练，3 个随机种子
- 本方法在所有地形类别的所有指标上显著优于或匹配 SOTA
- DreamWaQ 和 HIM 最大指令限制 1 m/s，CTS 和本方法 2 m/s
- 训练曲线显示：本方法训练时地形等级不一定最高，但 RoboGauge 分数精确反映底层性能

### MoE 消融研究（Q3）
- **MoE-NG**（去除指令信息）：性能下降
- **AC-MoE**（MoE 在 Actor-Critic 上而非学生编码器）：容易出现 loss 发散
- **MCP**（乘法组合策略）：同样不稳定
- 结论：MoE 在动作空间上的组合（AC-MoE、MCP）会导致训练不稳定；在学生编码器上的表征级组合更稳定有效
- PCA 可视化：MoE 在不同地形和指令下实现了更清晰的特征区分

### 真实世界部署（Q4-Q6）
- **地形挑战**：30 cm 障碍攀登（仅本方法成功）、85 级台阶（比基线快 17s）、80-100 N 横向冲量（仅本方法保持平衡）
- **速度跟踪精度**：
  - 台阶：平均 1.31 m/s，跟踪误差 0.15 m/s
  - 30° 斜坡：平均 1.53 m/s，比内置 RL 基线快 1.7s
  - 高速平地：峰值 4.01 m/s（2.16s 内达到），跟踪误差 0.20 m/s
- **稳定性与泛化**：
  - 持续 25-40 N 横向拉力下保持稳定
  - 60 cm 跌落恢复
  - 意外从平地跌落至台阶的姿态恢复
  - 户外测试（雪、沙、楼梯、斜坡、30cm 障碍）：100% 成功率，零意外终止
- **涌现步态**：高速时自主发展出窄基步态，减少横向质心振荡


## Limitations

1. 仅在 Unitree Go2 单一机器人平台上验证，未扩展到其他形态（如人形、双臂）
2. 仅使用本体感觉，不依赖外部感知传感器（相机、LiDAR、足部接触传感器），在极端条件（浓烟、光照不足）下有优势，但无法处理需要环境感知的结构性障碍
3. RoboGauge 基于 MuJoCo，与训练环境 IsaacGym 存在仿真器差异，可能引入额外偏差
4. 论文未详细讨论 MoE 专家数量 K 的选择标准和计算开销
5. 高速运动实验仅限于平地，未验证高速下的复杂地形运动
6. 未来工作方向明确提到需要整合外部感知和扩展到更多形态


## Key Takeaways

1. **Sim-to-Sim 评估作为 Sim-to-Real 代理的范式**：RoboGauge 验证了 sim-to-sim 指标比训练环境指标更接近真实世界表现，这一范式可能适用于操控任务（如 DLO manipulation 的 sim-to-sim 可迁移性评估）
2. **MoE 在表征层面的有效性**：MoE 集成在编码器（表征层）比集成在动作层更稳定，这个发现对多任务操控策略设计有参考价值
3. **训练奖励与真实表现的脱节是普遍问题**：不仅在运动控制中存在，在操控任务中同样值得关注，需要类似 RoboGauge 的预测评估工具
4. **本体感觉驱动的鲁棒性**：仅依靠 IMU + 关节编码器实现多地形鲁棒运动，避免了外部传感器在极端环境下的失效问题
5. **涌现行为的观察**：窄基步态作为高速稳定性的涌现行为，无显式编程，说明 RL 策略能发现人类未预设的运动模式


## 本地引用关系

-
## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[wu-tianyang|Wu, Tianyang]]
