---
title: "ExpertGen: Scalable sim-to-real expert policy learning from imperfect behavior priors"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本 Sim-to-Real 迁移，在工业装配（90.5%）和长时序操控（85%）任务上超越所有基线。"
authors: "Xu, Zifan; Gong, Ran; Minniti, Maria Vittoria; Gundogdu, Ahmet Salih; Rosen, Eric et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "EQFD8KNX"
---
## 摘要

Learning generalizable and robust behavior cloning policies requires large volumes of high-quality robotics data. While human demonstrations (e.g., through teleoperation) serve as the standard source for expert behaviors, acquiring such data at scale in the real world is prohibitively expensive. This paper introduces ExpertGen, a framework that automates expert policy learning in simulation to enable scalable sim-to-real（仿真到真实迁移） transfer. ExpertGen first initializes a behavior prior using a diffusion policy（扩散策略） trained on imperfect demonstrations, which may be synthesized by large language models or provided by humans. Reinforcement learning（强化学习） is then used to steer this prior toward high task success by optimizing the diffusion model（扩散模型）'s initial noise while keep original policy frozen. By keeping the pretrained diffusion policy（扩散策略） frozen, ExpertGen regularizes exploration to remain within safe, human-like behavior manifolds, while also enabling effective learning with only sparse rewards. Empirical evaluations on challenging manipulation（操控） benchmarks demonstrate that ExpertGen reliably produces high-quality expert policies with no reward（奖励） engineering. On industrial assembly（装配） tasks, ExpertGen achieves a 90.5% overall success rate, while on long-horizon（长时序） manipulation（操控） tasks it attains 85% overall success, outperforming all baseline methods. The resulting policies exhibit dexterous（灵巧） control and remain robust across diverse initial configurations and failure states. To validate sim-to-real（仿真到真实迁移） transfer, the learned state-based expert policies are further distilled into visuomotor policies via DAgger and successfully deployed on real robotic hardware.

## 中文简述

提出基于扩散策略的灵巧手方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. 将 Diffusion Steering RL 扩展到大规模并行机器人仿真（IsaacLab），证明其在保持扩散模型自然运动流形的同时显著提升稀疏奖励下的成功率
2. 提出 ExpertGen 端到端框架：从少量不完美演示到 Sim-to-Real 就绪的专家策略，无需手动奖励工程
3. 通过大规模 DAgger 蒸馏实现鲁棒的零样本 Sim-to-Real 迁移，识别了从仿真专家演示学习的关键瓶颈
## 结构化提取

- Problem: 如何从少量不完美演示出发，无需奖励工程即可大规模生成 Sim-to-Real 可迁移的专家策略
- Method: 三阶段管线——(1) 不完美演示训练 Diffusion Policy 先验; (2) DSRL + FastTD3 优化初始噪声; (3) DAgger 蒸馏为视觉运动策略
- Tasks: 桌面操控（抓取、推动、堆叠、抽屉操作、放置）、工业精密装配（peg-insertion）
- Sensors: 仿真环境 state-based（Phase 1-2）; 点云（3×RealSense D435i）和 RGB（108×192）用于 Phase 3 蒸馏
- Robot Setup: 单臂 Franka + Robotiq 2F-85 夹爪; 仿真使用 IsaacLab GPU 并行
- Metrics: 成功率（1024/256 rollouts）、DTW（轨迹相似度）、Jerk Cost（平滑度）、真实世界零样本成功率
- Limitations: 行为受限于先验覆盖；需大规模并行仿真；长时序任务仍有改进空间；未涉及双臂/DLO 场景
- Evidence Notes:

  - Table I: AnyTask 8 任务成功率，ExpertGen 全面最优
  - Table II: DTW/Jerk 平滑性度量，ExpertGen 在成功率和平滑度间取得最优平衡
  - Table III: 扰动恢复，ExpertGen 对夹爪开/外力扰动鲁棒
  - Table IV: Sim-to-Real 点云/RBG 策略成功率
  - Table V: DAgger α 退火消融
  - Fig 3: AutoMate 90.5% 总体成功率
  - Fig 7: 演示数量消融，200 条足够
  - Fig 8: 人类运动先验 vs 脚本策略先验
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high (完整阅读全文，含方法、实验、消融、Sim-to-Real 结果、附录引用)
- Confidence: high
- Summary: ExpertGen 用不完美演示训练扩散策略作为行为先验，通过 DSRL 在大规模并行仿真中仅优化扩散初始噪声来获取专家策略，再用 DAgger 蒸馏为视觉运动策略实现零样本 Sim-to-Real 迁移，在工业装配（90.5%）和长时序操控（85%）任务上超越所有基线。


## Problem

机器人行为克隆需要大量高质量专家数据，但真实世界遥操作采集成本极高。仿真提供可扩展替代方案，但现有方法存在局限：
1. 脚本策略/LLM 生成演示缺乏行为多样性和失败恢复能力
2. RL 方法需要精心设计奖励函数，跨任务泛化困难
3. 现有 offline-to-online 方法（Residual RL）对超参敏感，动作尺度难以调优
4. 从稀疏奖励学习高性能策略在长时序任务中极具挑战

ExpertGen 聚焦于学习满足四个属性的 Sim-to-Real 专家策略：空间泛化、失败恢复、真实世界可迁移、稀疏奖励无需奖励工程。


## Method

ExpertGen 分三阶段：

**Phase 1: Generative Behavior Prior Modeling**
- 收集不完美演示轨迹 D_P（可来自 LLM 合成脚本策略或人类遥操作）
- 不完美来源包括：不完整状态覆盖、缺乏恢复行为、动力学/具身不匹配
- 在演示上训练 state-based Diffusion Policy 作为行为先验
- 使用 DDIM 采样进行推理

**Phase 2: Expert Policy Acquisition (DSRL + FastTD3)**
- 采用 Diffusion Steering RL（DSRL）：不修改扩散模型参数，学习一个 steering policy 仅优化扩散模型的初始噪声 z_0
- Steering policy 与扩散模型输出在同一动作空间操作，保持原始去噪过程
- 使用 FastTD3（而非 SAC）作为 RL 算法：
  - FastTD3 是 TD3 的可扩展变体，专为大规模并行仿真设计
  - 引入大 batch 训练、分布式 critic、混合探索噪声
  - 比标准 PPO 在稀疏奖励大规模并行环境中更高效
- 奖励函数仅为二值任务成功信号（无奖励工程）
- 约束探索保持在人类似行为流形内

**Phase 3: Visuomotor Policy Distillation via DAgger**
- 状态空间专家策略 → 观测空间可部署策略
- DAgger 迭代收集学生策略诱导状态分布下的专家修正动作
- 大规模视觉 domain randomization（纹理、光照、相机位姿、物体外观）
- α 参数控制 teacher rollout 比例，线性退火策略


## Experiments

### Benchmarks
- **AnyTask**: 8 个桌面操控任务（Lift/Brick/Banana/Peach, Open Drawer, Push Pear, Stack Banana on Can, Put Object In Closed Drawer, Place Strawberry In Bowl），1000 演示/任务
- **AutoMate**: 工业装配 peg-insertion 任务（高精度、紧几何容差），500 演示/任务

### Main Results (Table I - AnyTask State-based)
| Task | Scripted | Diffusion | Residual RL | ExpertGen |
|------|----------|-----------|-------------|-----------|
| Lift Banana | 56.3 | 69.8 | 84.3 | **99.8** |
| Lift Brick | 66.4 | 72.6 | 98.4 | **99.7** |
| Lift Peach | 60.9 | 28.5 | 75.9 | **99.3** |
| Open Drawer | 28.1 | 77.6 | 99.5 | **100** |
| Push Pear | 18.0 | 50.5 | 56.5 | **83.3** |
| Stack Banana | 26.6 | 16.3 | 0.0 | **67.2** |
| Put In Drawer | 9.4 | 0.5 | 13.6 | **80.7** |
| Place In Bowl | 43.0 | 6.6 | 1.3 | **52.1** |

### AutoMate 工业装配
- ExpertGen 总体成功率 90.5%，超越所有基线

### 失败恢复（Table III）
- 随机夹爪打开扰动：ExpertGen 平均仅下降 0.5%
- 随机外力扰动：ExpertGen 平均下降 28.6%（扩散策略下降近至零）

### 轨迹平滑性（Table II）
- ExpertGen DTW=0.139, Jerk=5.97（平均）
- Residual RL (0.1): Jerk=35.3（明显抖动）
- Diffusion Policy: DTW=0.126（最贴近演示流形但成功率低）

### Sim-to-Real Transfer（Table IV-V）
- 机器人：Franka + Robotiq 2F-85 夹爪
- 传感器：3× Intel RealSense D435i（点云 + RGB）
- 点云策略：Lift Banana 75%, Push Pear 65%, Open Drawer 85%
- RGB 策略：Lift Banana 80%（零样本）
- BC 基线在真实世界几乎无法工作（RGB 基线 0% 成功）

### 消融实验
1. **演示数量**：200 条演示足以初始化有效先验，50 条显著下降
2. **RL 算法选择**：FastTD3 在所有 8 个任务上优于 PPO
3. **人类运动先验**：用 SkillMimicGen 增强的人类演示显著提升 Stack Banana 性能
4. **DAgger α 退火**：α→0.2 给出最佳真实世界结果（75%），纯学生 α=0 得 65%，纯教师 α=1.0 得 55%


## Limitations

1. 专家策略受限于演示覆盖范围——先验缺乏的行为无法被学习（如翻转倒扣物体）
2. 需要仿真环境支持大规模并行训练（IsaacLab）
3. DAgger 蒸馏需要多次仿真交互，计算开销较大
4. 长时序任务（如 Stack, Place）成功率仍低于短时序任务
5. 未涉及双臂操作或 DLO 操控场景


## Key Takeaways

1. **DSRL 核心思想**：冻结扩散策略权重，仅优化初始噪声 z_0 → 既保持似人行为流形，又能在稀疏奖励下有效学习。这一"动作空间不变"策略比 Residual RL 的残差修正更鲁棒
2. **不完美先验的价值**：约 200 条不完美演示足以提供可行行为流形，RL 负责补充覆盖和恢复能力。降低了数据采集门槛
3. **FastTD3 > PPO**：在大规模并行稀疏奖励场景下，off-policy 重放比 on-policy 更高效
4. **DAgger 优于 BC**：视觉策略蒸馏中 on-policy 数据收集对对抗分布漂移至关重要，α=0.2 是实际最优平衡点
5. **Sim-to-Real 可行路径**：三阶段管线（先验→RL 精炼→DAgger 蒸馏）提供了一个可复用的 Sim-to-Real 数据生成框架

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu-zifan|Xu, Zifan]]
- [[gong-ran|Gong, Ran]]
