---
title: "REFINE-DP: Diffusion policy fine-tuning for humanoid loco-manipulation via reinforcement learning"
tags: [manipulation, imitation, RL, diffusion, diffusion-model]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "提出REFINE-DP框架，通过DPPO联合优化扩散策略高层规划器和RL底层控制器，使人形机器人loco-manipulation任务成功率从50-70%提升至90%+，仅需50条示教数据即可达到从头训练1000条的性能。"
authors: "Gu, Zhaoyuan; Chen, Yipu; Chai, Zimeng; Cueva, Alfred; Nguyen, Thong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "BBXHMZG9"
---
## 摘要

Humanoid loco-manipulation（操控） requires coordinated high-level motion plans with stable, low-level whole-body execution under complex robot-environment dynamics and long-horizon（长时序） tasks. While diffusion（扩散） policies (DPs) show promise for learning from demonstrations, deploying them on humanoids poses critical challenges: the motion planner trained offline is decoupled from the low-level controller, leading to poor command tracking, compounding distribution shift, and task failures. The common approach of scaling demonstration（示范数据） data is prohibitively expensive for high-dimensional humanoid systems. To address this challenge, we present REFINE-DP (REinforcement learning（强化学习） FINE-tuning of Diffusion Policy（扩散策略）), a hierarchical framework that jointly optimizes a DP high-level planner and an RL-based low-level loco-manipulation（操控） controller. The DP is fine-tuned via a PPO-based diffusion policy（扩散策略） gradient to improve task success rate, while the controller is simultaneously updated to accurately track the planner's evolving command distribution, reducing the distributional mismatch that degrades motion quality. We validate REFINE-DP on a humanoid robot performing loco-manipulation（操控） tasks, including door traversal and long-horizon（长时序） object transport. REFINE-DP achieves an over $90\%$ success rate in simulation, even in out-of-distribution cases not seen in the pre-trained data, and enables smooth autonomous task execution in real-world dynamic environments. Our proposed method substantially outperforms pre-trained DP baselines and demonstrates that RL fine-tuning is key to reliable humanoid loco-manipulation（操控）. https://refine-dp.github.io/REFINE-DP/

## 中文简述

提出基于扩散策略的操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、扩散模型

## 关键贡献

1. **分层人形机器人loco-manipulation框架**：DP作为高层规划器输出低维指令（base velocity + hand poses），RL策略作为底层控制器执行whole-body loco-manipulation。与latent vector或全关节角输入的方案相比，指令空间更可解释、更易于遥操作采集
2. **DPPO联合优化方法**：同时微调扩散策略规划器和RL底层控制器，而非仅优化规划器。联合优化保持规划器输出与控制器输入之间的分布一致性，显著提升跟踪精度和运动平滑度
3. **数据效率突破**：50条遥操作示教 + REFINE-DP微调即可达到95-97%成功率，对比从头训练需要~1000条轨迹，数据需求降低20倍
4. **Booster T1人形机器人全自主验证**：首次将扩散策略应用于人形机器人门开合穿越，并验证了物体搬运、楼梯拾取等四个challenging任务
## 结构化提取

- **Problem**: 人形机器人loco-manipulation中，离线DP规划器与底层控制器解耦导致分布偏移和累积错误；扩展示教数据代价高昂
- **Method**: REFINE-DP——三阶段管线（数据采集→DP预训练→DPPO联合RL微调），DiT骨干扩散策略 + 解耦式RL loco-manipulation控制器，joint optimization维持分布一致性
- **Tasks**: Object Pickup, Long-horizon Pick-and-Place (~40s), Door Opening and Traversal, Stair-assisted Object Retrieval
- **Sensors**: MoCap系统（90Hz，机器人躯干+物体位姿）、关节编码器、IMU（proprioception）
- **Robot Setup**: Booster T1人形机器人（29 DoF），AMD 7945HX CPU + RTX 4060 GPU，DP 10Hz + 控制器 50Hz，locomotion 0.2 m/s clamp，hand 0.05 m/s clamp
- **Metrics**: Task Success Rate（100 trials/task），tracking position/orientation error，end-effector velocity（运动平滑度），task completion time
- **Limitations**: 依赖MoCap（无视觉）、硬件SR低于仿真、需要预训练基线50-70%才能微调、仅验证刚体任务、速度受限
- **Evidence Notes**: 仿真>90% SR四任务全覆盖；硬件door 70%+、box 50%+；数据效率20倍提升；联合优化减半迭代次数；OOD课程学习从7%到>90%；FT策略具备失败恢复涌现能力。所有定量结果来自100 trials仿真实验和少量硬件trials。
## 本地引用关系

-
## 证据元数据

- **Fulltext Quality**: fulltext（arXiv HTML 全文 + 项目页面补充）
- **Evidence Coverage**: 完整覆盖方法、实验、消融、硬件验证、附录（观测/奖励表）
- **Confidence**: high
- **Summary**: 提出REFINE-DP框架，通过DPPO联合优化扩散策略高层规划器和RL底层控制器，使人形机器人loco-manipulation任务成功率从50-70%提升至90%+，仅需50条示教数据即可达到从头训练1000条的性能。


## Problem

人形机器人在执行loco-manipulation（行走+操控协同）任务时面临三大核心问题：

1. **规划器与控制器解耦**：离线训练的扩散策略（DP）高层规划器与底层whole-body控制器独立运行，导致指令跟踪误差和分布偏移（distribution shift）在长时序任务中累积放大
2. **数据扩展代价高昂**：高维人形机器人系统的示教数据采集成本极高（遥操作+启发式规划器生成1000条轨迹），且仍无法覆盖所有分布外场景
3. **长时序累积错误**：loco-manipulation任务涉及多阶段（行走→操控→行走），compounding error 导致预训练策略在实际部署中频繁失败（预训练成功率仅50-70%）


## Method

### 三阶段管线

**Stage 1: 数据采集**
- 通过VR遥操作和启发式行为规划器在IsaacLab仿真器中采集示教数据
- 50条遥操作轨迹 + 启发式规划器扩展至1000条
- 只保留成功轨迹，随机化初始物体配置和机器人初始状态
- 观测：手/足位姿（body frame）、夹爪状态、物体信息
- 动作：期望手位姿（SE(3)）、夹爪状态、base velocity指令

**Stage 2: DP预训练**
- 使用DiT（Diffusion Transformer）骨干网络训练扩散策略
- DP输出base velocity和hand pose指令 → 传递给底层RL控制器执行
- 观测窗口8步，动作chunk大小12步，每步0.1s间隔
- 噪声调度：cosine schedule
- DP推理频率10Hz（NVIDIA TensorRT加速）

**Stage 3: REFINE-DP联合微调**
- 采用DPPO（Diffusion Policy Policy Optimization）框架
- 将去噪过程展开为augmented MDP，每个去噪步骤视为一个决策步骤
- DP通过PPO风格的策略梯度更新（Eq. 6）
- 底层RL控制器同时用预训练奖励函数通过PPO更新
- 联合优化维持规划器输出与控制器输入的分布一致性

### 底层RL Loco-manipulation控制器

- **解耦架构**：上半身arm策略π_upper跟踪hand pose指令；下半身locomotion策略π_lower跟踪foot placement指令
- **Foot placement控制器**：输入为离散foot placement命令（swing foot indicator + countdown + target pose）+ 本体感知；RL motion imitation训练
- **Hand pose跟踪控制器**：输入SE(3) hand pose指令 + arm关节状态；domain randomization增强鲁棒性
- 总输出a_t ∈ R^26（12维leg joints + 14维arm joints），PD控制器跟踪目标关节位置
- 策略运行频率50Hz

### 关键技术细节

- **Foot placement vs velocity tracking**：采用foot placement跟踪而非速度跟踪，避免速度跟踪在频繁启停操控场景中的位置累积误差
- **OOD课程学习**：在最大随机化水平下预训练策略仅7% SR，采用课程策略逐步扩展10%范围至90% SR
- **Baseline对比**：DiT（预训练）、MLP（确定性骨干）、MLP-FT（微调确定性策略）、Residual RL（冻结DP + 残差策略）


## Experiments

### 仿真实验

**平台**：IsaacLab仿真器，Booster T1人形机器人（29 DoF）

**四个任务**：
1. **Task 1: Object Pickup** — 走到桌前捡起箱子
2. **Task 2: Long-horizon Pick-and-Place**（~40s）— 捡起箱子放到另一张桌
3. **Task 3: Door Opening and Traversal** — 首次将DP应用于人形机器人门开合穿越
4. **Task 4: Stair-assisted Object Retrieval** — 踩上高台拾取物体

**主要结果**（100 trials/task）：

| 方法 | Task 1 | Task 2 | Task 3 | Task 4 |
|------|--------|--------|--------|--------|
| MLP（预训练） | 较低 | 较低 | 较低 | 较低 |
| DiT（预训练） | 50-70% | 50-70% | ~73%（door） | 50-70% |
| MLP-FT | 中等 | 中等 | 中等 | 中等 |
| Residual RL | 中等 | 中等 | 中等 | 中等 |
| **REFINE-DP（DiT-FT + Joint）** | **>90%** | **>90%** | **>90%（95%）** | **>90%** |

*注：精确数字来自Figure 4的柱状图，原文仅以文字描述">90%"。*

### 消融研究

1. **联合优化效率**：
   - 联合优化将DP微调迭代次数减半（20 vs 40次达到90% SR）
   - 仅优化底层控制器即可在long-horizon任务上提升18% SR
   - 联合优化降低末端执行器位置跟踪误差和orientation error up to 50%
   - 末端速度降低15%，运动更平滑

2. **数据效率**：
   - 从头训练需~1000条轨迹达到90% SR
   - 50条预训练 + FT达到95-97% SR
   - 数据需求降低20倍

3. **OOD泛化**：
   - 最大随机化下预训练SR仅7%
   - 课程FT将SR提升至>90%
   - 无课程的直接FT在最大随机化下仅30% SR

4. **任务吞吐量**：
   - FT减少任务完成时间15%（仿真均值）
   - 硬件：box pickup ~10%提速，door opening ~20%提速
   - FT策略消除了预训练策略中的犹豫和冗余动作

### 硬件实验

**平台**：Booster T1人形机器人，AMD 7945HX CPU + RTX 4060 GPU
**感知**：MoCap系统（90Hz）提供机器人躯干和目标物体位姿
**安全限制**：locomotion速度0.2 m/s，hand速度0.05 m/s

**硬件结果**：
- Door opening: >70% SR
- Box transport: >50% SR
- Sim-to-real差距来源：(1) 物体观测噪声（门把手位置、目标箱位姿），(2) locomotion颤抖和滑动

**恢复能力**：
- FT策略在目标位置变化时实时重新调整规划
- 在门把手抓取失败后自动重新尝试（迈小步接近后再试）
- 预训练策略在失败后倾向于卡住无法恢复


## Limitations

1. **感知依赖MoCap**：当前DP使用state-based观测，依赖MoCap系统提供物体位姿，未集成视觉感知（论文明确列为future work）
2. **硬件成功率仍有gap**：door opening从仿真90%+降至硬件70%+，box transport降至50%+，sim-to-real差距主要由观测噪声和locomotion不稳定性造成
3. **速度限制**：硬件实验中locomotion速度被钳位至0.2 m/s，hand速度0.05 m/s，牺牲了速度换精度
4. **预训练前提条件**：微调需要预训练策略达到~50-70% SR的基线水平，从随机初始化微调效果有限（sparse reward难以提供有效学习信号）
5. **启发式规划器依赖**：数据扩展依赖任务特定的启发式行为规划器进行stage-conditioned behavior transitions
6. **未涉及DLO操控**：实验仅涉及刚体（箱、门），未验证可变形物体操控


## Key Takeaways

1. **分层架构的有效性**：将高维whole-body控制问题分解为"低维指令规划 + RL底层执行"，使DP的动作空间从全关节角缩减为base velocity + hand poses，大幅降低学习难度
2. **DPPO > 纯模仿学习**：扩散策略的RL微调比纯模仿学习数据效率提升20倍，且通过课程学习可实现大幅OOD泛化
3. **联合优化是关键**：仅微调DP会导致控制器跟踪性能下降（DP学会"过度指令"来补偿跟踪误差）；联合优化同时提升跟踪精度、运动平滑度和成功率
4. **Foot placement优于velocity tracking**：对于频繁启停的操控场景，离散foot placement指令比连续velocity指令避免位置累积误差
5. **与DLO操控的关联**：虽然本文仅验证刚体，但"分层架构 + 扩散策略 + RL微调"的范式可迁移至DLO操控的高层规划；关键差异在于DLO需要处理形变状态观测和接触力约束

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[gu-zhaoyuan|Gu, Zhaoyuan]]
- [[chen-yipu|Chen, Yipu]]
