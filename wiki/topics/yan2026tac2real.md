---
title: "Tac2Real: Reliable and GPU visuotactile simulation for online reinforcement learning and zero-shot real-world deployment"
tags: [manipulation, RL, sim-to-real, robot-learning, tactile]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实现 91.7% 的零样本 Sim-to-Real 迁移成功率。"
authors: "Yan, Ningyu; Wang, Shuai; Shen, Xing; Wang, Hui; Wang, Hanqing et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4B863P79"
---
## 摘要

Visuotactile sensors are indispensable for contact-rich（接触丰富） robotic manipulation（机器人操控） tasks. However, policy learning with tactile（触觉） feedback in simulation, especially for online reinforcement learning（强化学习） (RL), remains a critical challenge, as it demands a delicate balance between physics fidelity and computational efficiency. To address this challenge, we present Tac2Real, a lightweight visuotactile simulation framework designed to enable efficient online RL training. Tac2Real integrates the Preconditioned Nonlinear Conjugate Gradient Incremental Potential Contact (PNCG-IPC) method with a multi-node, multi-GPU high-throughput parallel simulation architecture, which can generate marker displacement fields at interactive rates. Meanwhile, we propose a systematic approach, TacAlign, to narrow both structured and stochastic sources of domain gap, ensuring a reliable zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer. We further evaluate Tac2Real on the contact-rich（接触丰富） peg insertion task. The zero-shot（零样本） transfer results achieve a high success rate in the real-world scenario, verifying the effectiveness and robustness of our framework. The project page is: https://ningyurichard.github.io/tac2real-project-page/

## 中文简述

提出基于强化学习的插入方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、仿真到真实迁移、机器人学习、触觉感知

## 关键贡献

1. **Tac2Real 仿真框架**：基于 PNCG-IPC 求解器的轻量级视触觉仿真器，支持多节点多 GPU 并行，可作为插件无缝集成到 Isaac Lab / MuJoCo 等物理引擎。
2. **TacAlign 校准管线**：四阶段系统化方法，从结构化（控制器对齐、材料参数校准、任务级参数微调）和随机化（域随机化）两个维度缩小 sim-to-real 差距。
3. **真实世界验证**：在盲 peg insertion 任务上实现 91.7% 的零样本迁移成功率，显著优于 TacSL（15%）和 Tacchi（8.3%）。
## 结构化提取

- Problem: 视触觉传感器仿真中物理保真度与计算效率的矛盾，以及触觉 RL 策略的零样本 Sim-to-Real 迁移
- Method: PNCG-IPC 求解器（非线性共轭梯度法替代 Newton 法）+ 多 GPU 并行 + TacAlign 四阶段校准
- Tasks: Peg insertion（8mm 销钉，初始朝向 ±35° 随机）；Nut threading（螺母旋入螺栓，初始朝向 ±35° 随机）
- Sensors: GelSight Mini 视触觉传感器，marker 位移场（9×7）
- Robot Setup: Franka Panda 机械臂，双指夹爪，Cartesian 阻抗控制
- Metrics: 成功率（peg 完全插入 / 螺母旋入 1.5 节距）；轨迹差异（mm / degree）；仿真 FPS
- Limitations: 仅 peg insertion 有真实部署；仅适配 GelSight Mini；传感器凝胶脆弱；单指触觉
- Evidence Notes:

  - 仿真 peg insertion 成功率 77.6%，nut threading 70.2%（Tab. 3）
  - 真实世界 peg insertion 零样本迁移成功率 91.7%（60 次试验）
  - TacSL 仿真中表现相当但真实部署仅 15%（仿真-真实域差距大）
  - Tacchi 因 MPM 数值不稳定在真实部署仅 8.3%
  - 消融：任务级校准去掉后从 91.7% 降至 25.0%；控制对齐去掉降至 53.3%
  - PNCG-IPC 在 4096 环境下达到 4465 FPS
  - 控制器对齐将轨迹差异从 11.11mm 降至 2.521mm
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（涵盖方法论、实验、消融、真实部署）
- Confidence: high
- Summary: 提出 Tac2Real 框架，基于 PNCG-IPC 求解器构建多 GPU 并行视触觉仿真器，配合四阶段 TacAlign 校准管线，在 peg insertion 任务上实现 91.7% 的零样本 Sim-to-Real 迁移成功率。


## Problem

接触丰富的机器人操控任务中，视触觉传感器（如 GelSight）至关重要。然而在仿真中进行在线 RL 训练面临两个核心挑战：
1. **物理保真度与计算效率的矛盾**：高保真触觉仿真（如 MPM、IPC）计算开销大，难以支撑大规模并行 RL 训练；而低成本的 penalty-based 方法（如 TacSL）物理一致性差。
2. **Sim-to-Real 域差距**：结构化差异（机器人动力学、材料参数、接触模型）和随机差异（噪声、环境不确定性）导致仿真训练的策略难以直接迁移到真实世界。


## Method

### PNCG-IPC 求解器
- 基于 Incremental Potential Contact (IPC) 方法，将接触仿真建模为变分优化问题
- 用非线性共轭梯度法（Dai-Kou 算法）替代 Newton 法，避免 Hessian 矩阵组装和分解
- 仅需梯度、对角 Hessian 和向量点积——全部高度可 GPU 并行
- CCD-free 线搜索：解析推导步长上界，消除昂贵的碰撞检测
- 用 Taichi 语言实现，编译为高性能 GPU kernel

### 触觉表示选择
- 采用 marker 位移场（9×7）而非 RGB 触觉图像
- 实验表明 marker 位移场在不同接触模式（静止、下压、前移、后移）下区分度远高于 RGB
- 低维表示（126 维 vs 320×240×3）有利于 RL 训练的规律性和效率
- 通过 k-nearest neighbor 建立标记点与 IPC 网格节点的映射

### 多 GPU 并行架构
- 基于 Ray 集群构建多节点多 GPU 并行
- 每个 GPU 管理一组环境的触觉仿真任务
- RL 智能体发送动作 → 物理引擎执行一步 → 提取相对位姿 → 触觉仿真 → 合并观测返回
- 4096 环境下达到 4465 FPS（伪结构化网格）和 1665 FPS（非结构化网格）

### TacAlign 四阶段校准
1. **控制器对齐**：交替最小化仿真/真实端 Cartesian 阻抗控制器的 kp 参数，使轨迹差异降至 2.521 mm（平移）和 0.454°（旋转）
2. **基线 IPC 校准**：用 CMA-ES 优化材料参数（Young's modulus E, Poisson's ratio ν, density ρ, friction μ），最小化仿真与真实的 marker 位移场 MSE
3. **任务级校准**：在四种典型接触状态（静止夹持、下压、前移碰撞、后移碰撞）下微调 Isaac Lab 中的摩擦系数和接触刚度
4. **域随机化**：随机化控制器增益、摩擦、几何配置、观测噪声和 IPC 扰动


## Experiments

### 任务设置
- **Peg Insertion**：Franka 夹持 8mm 圆柱销钉插入 8mm 孔，初始朝向随机 ±35°，完全靠主动控制（不依赖重力）
- **Nut Threading**：Franka 夹持螺母旋入螺栓，初始朝向随机 ±35°，成功标准为旋入 1.5 节距

### 仿真训练
- 512 环境，4 节点各 16 GPU
- PPO + LSTM（2层，1024单元），共享 actor-critic
- 观测：末端位姿（7维）+ 单指 marker 位移场（7×9×2）+ 上一步动作
- 无物体位姿或视觉信息（"盲"设置）

### 仿真结果（Tab. 3）
| 方法 | Peg Insertion | Nut Threading |
|------|:---:|:---:|
| Tac2Real | 77.6% | 70.2% |
| TacSL | 78.9% | 70.8% |
| Tacchi | 17.3% | 15.2% |
| No Tactile | 16.8% | 31.3% |

仿真中 Tac2Real 与 TacSL 性能接近，均显著优于 Tacchi 和无触觉基线。

### 真实世界部署（Tab. 3）
- 60 次试验（0°, ±15° 各 20 次）
| 方法 | 成功率 |
|------|:---:|
| Tac2Real (TacAlign 全部) | **91.7%** (55/60) |
| TacSL | 15.0% |
| Tacchi | 8.3% |
| No Tactile | 6.7% |

### 消融实验（TacAlign 各阶段贡献）
| TacAlign 级别 | 成功率 |
|---|:---:|
| 1+2+3+4（全部） | 91.7% |
| 2+3+4（无控制对齐） | 53.3% |
| 1+2+4（无任务级校准） | 25.0% |
| 1+2+3（无随机化） | 76.7% |

**关键发现**：任务级校准（level 3）贡献最大，去掉后成功率从 91.7% 降至 25.0%；控制对齐贡献次之；域随机化也有显著帮助。

### PNCG-IPC 仿真质量对比（Fig. 5）
- 与真实数据对比：Tac2Real 和 Tacchi 在小变形下均接近真实；TacSL 因非物理方法有明显差异
- 大旋转/滑移变形下：Tacchi 出现粒子飞溅和数值不稳定；Tac2Real 稳定恢复
- 并行性能：4096 环境下 Tac2Real FPS 远超 Tacchi


## Limitations

1. 真实世界仅验证了 peg insertion，nut threading 未在真实世界部署
2. 传感器凝胶脆弱，需保护机制（MSE 阈值检测并回退）
3. 仅适配 GelSight Mini 传感器，未验证其他视触觉传感器
4. 策略仅用单指触觉信号，双指信息利用不充分
5. 未来方向（尚未实现）：灵巧手操控、可变形物体、VLA 训练数据生成、AI 加速触觉仿真


## Key Takeaways

1. **PNCG-IPC 的设计哲学**：牺牲单步精度换取迭代吞吐量，对触觉仿真场景（视觉合理即可，不需要机器精度收敛）非常合适。这一思路可推广到其他需要实时仿真的场景，包括 DLO 仿真。
2. **Marker 位移场优于 RGB 触觉图**：对于 RL 训练中的接触状态判断，低维 marker 位移场比高维 RGB 图像更有效。这与我们 DLO 操控中选择感知表示的思路一致——应优先考虑对任务有区分度的紧凑表示。
3. **TacAlign 四阶段校准是一个通用 Sim-to-Real 框架**：控制器对齐→材料参数校准→任务级微调→域随机化的流水线可迁移到其他触觉任务甚至 DLO 操控任务。
4. **任务级校准是 sim-to-real 的关键**：消融实验明确表明，在任务相关的接触条件下精细校准物理参数比域随机化更重要。
5. **多 GPU 并行 RL 训练的工程经验**：Ray 集群 + 插件式架构的设计模式值得借鉴，尤其对于需要复杂物理仿真的大规模 RL 训练。

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[tactile-sensing]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[yan|Yan, Ningyu]]
- [[shen|Shen, Xing]]
