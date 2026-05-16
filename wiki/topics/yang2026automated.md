---
title: "Towards automated chicken deboning via learning-based dynamically-adaptive 6-DoF multi-material cutting"
tags: [imitation, RL, sim-to-real, physics-simulation, collision-avoidance]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。"
authors: "Yang, Zhaodong; Hu, Ai-Ping; Ravichandar, Harish"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "Z7MUTJ33"
---
## 摘要

Automating chicken shoulder deboning requires precise 6-DoF cutting through a partially occluded, deformable, multi-material joint, since contact with the bones presents serious health and safety risks. Our work makes both systems-level and algorithmic contributions to train and deploy a reactive force-feedback cutting policy that dynamically adapts a nominal trajectory and enables full 6-DoF knife control to traverse the narrow joint gap while avoiding contact with the bones. First, we introduce an open-source custom-built simulator for multi-material cutting that models coupling, fracture, and cutting forces, and supports reinforcement learning（强化学习）, enabling efficient training and rapid prototyping. Second, we design a reusable physical testbed to emulate the chicken shoulder: two rigid "bone" spheres with controllable pose embedded in a softer block, enabling rigorous and repeatable evaluation while preserving essential multi-material characteristics of the target problem. Third, we train and deploy a residual RL policy, with discretized force observations and domain randomization, enabling robust zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer and the first demonstration（示范数据） of a learned policy that debones a real chicken shoulder. Our experiments in our simulator, on our physical testbed, and on real chicken shoulders show that our learned policy reliably navigates the joint gap and reduces undesired bone/cartilage contact, resulting in up to a 4x improvement over existing open-loop（开环） cutting baselines in terms of success rate and bone avoidance. Our results also illustrate the necessity of force feedback for safe and effective multi-material cutting. The project website is at https://hal-zhaodong-yang.github.io/MultiMaterialWebsite/.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移、物理仿真、碰撞避免

## 关键贡献

1. **首个开源多材料切割仿真器**：基于 MLS-MPM 方法，支持异质材料的耦合、断裂和切割力建模，兼容 RL 框架（Stable-Baselines3），用 Taichi 实现。
2. **首个可复用的多材料切割物理测试台**：用 Kinetic Sand（模拟软组织）+ Reusable Clay 球体（模拟骨骼）构建可控、可重复的真实世界实验平台。
3. **首个学习型6-DoF多材料切割方法**：残差 RL 策略 + 力离散化 + 域随机化 → 零样本迁移到物理测试台和真实鸡肉肩部。
## 结构化提取

- **Problem**: 鸡肉肩部自动化去骨——在部分遮挡、可变形、多材料环境中实现6-DoF切割，避免骨骼接触
- **Method**: 残差RL策略（PPO），MLS-MPM多材料仿真器，力信号离散化 + 域随机化实现Sim-to-Real
- **Tasks**: 多材料切割（鸡肉肩部去骨），6-DoF刀具控制
- **Sensors**: Robotiq FT 300力/力矩传感器（0-300N），关节编码器（本体感觉）
- **Robot Setup**: UR5机械臂，末端安装力传感器+刀具，桌面固定工件
- **Metrics**: 违规时长（仿真）、成功率（无骨骼碰撞）、骨骼切割质量(g)、骨骼质量<0.05g比例
- **Limitations**: 球形骨骼假设、力归一化需预标定、名义轨迹依赖、仿真低精度、真实成功率50%
- **Evidence Notes**: 三阶段实验完整验证（仿真→物理测试台→真实鸡肉），力反馈消融实验证实其必要性，骨骼位置误差与性能关系图（Fig.7）显示方法鲁棒性。RoboNinja不适用的定性分析提供了问题边界。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（仿真 + 物理模型 + 真实鸡肉三阶段实验，含定量结果表和消融）
- Confidence: high
- Summary: 基于残差RL策略实现6-DoF多材料切割（鸡肉去骨），通过力反馈动态调整名义轨迹，结合力离散化和域随机化实现零样本Sim-to-Real迁移，成功率提升4倍。


## Problem

自动化鸡肉肩部去骨需要在部分遮挡、可变形、多材料的关节中进行精确的6-DoF切割。由于骨骼被软组织覆盖，无法预先精确规划轨迹；切割到骨骼/软骨会产生碎屑混入食品，带来安全风险。现有方法要么只支持2D平面切割，要么采用开环轨迹缺乏在线自适应能力。


## Method

### 仿真器设计
- 使用 MLS-MPM（Moving Least Squares Material Point Method）进行可变形材料仿真
- Von Mises 屈服准则区分肉类和骨骼材料（Lamé 参数不同）
- 刀具建模为时变 SDF（Signed Distance Field），近似为薄长方体
- Coulomb 摩擦模型处理接触，MPM 自然支持材料分离（切割）
- 仿真环境放大5倍（相对真实尺寸）以保证数值稳定性
- Python + Taichi 实现，继承 OpenAI Gym 接口

### 残差策略学习
- **观察空间**：当前刀具6D位姿 ξₜ、名义轨迹下一步位姿 ξ̂ₜ₊₁、3D力传感器读数 fₜ（离散化）、上一步残差位姿 eξₜ
- **动作空间**：6D残差位姿增量 aₜ，通过 eξₜ₊₁ = eξₜ + ηaₜ 递推，最终 ξ̃ₜ₊₁ = ξ̂ₜ₊₁ + eξₜ₊₁
- **奖励函数**：R = R_bone + R_action；R_bone 为骨骼碰撞惩罚（二值），R_action 为动作正则化
- **RL 算法**：PPO（Stable-Baselines3），MLP 2层×64，tanh 激活
- **力离散化**：将3D力归一化后离散到 {0, 0.1, 0.2, ..., 1.0}，缓解仿真-真实力信号域差异
- **域随机化**：位置加 N(0, 0.01) 噪声，姿态四元数加 N(0, 0.1) 噪声

### Sim-to-Real 迁移
- 力离散化 + 本体感觉域随机化
- 仿真中训练策略参数与真实部署完全一致
- 不需要真实世界数据微调


## Experiments

### 实验设置
- **机器人平台**：UR5 机械臂 + Robotiq FT 300 力/力矩传感器 + 刀具
- **仿真**：50次切割，随机采样骨骼位置（δx: ±5mm, δy: ±10mm, δz: ±10mm）
- **物理测试台**：20次切割，Reusable Clay 球体（半径21mm，间距50mm，间隙8mm）
- **真实鸡肉**：多只鸡肩切割实验

### 仿真结果（Table I）
| 方法 | 平均违规时长 (%) ↓ | 成功率 ↑ |
|------|---------------------|----------|
| Nominal | 18.1 ± 11.88 | 0.20 |
| Adaptive w/o Force | 9.04 ± 10.76 | 0.54 |
| **Adaptive (Ours)** | **4.74 ± 9.66** | **0.80** |

### 物理测试台结果（Table II）
| 方法 | 平均骨骼切割质量 (g) ↓ | 成功率 ↑ |
|------|------------------------|----------|
| Nominal | 3.032 ± 3.090 | 0.05 |
| Adaptive w/o Force | 0.730 ± 0.884 | 0.35 |
| **Adaptive (Ours)** | **0.065 ± 0.130** | **0.75** |

### 真实鸡肉结果（Table III）
| 方法 | 平均骨骼质量 (g) ↓ | 成功率 ↑ | 骨骼质量 < 0.05g ↑ |
|------|---------------------|----------|---------------------|
| Nominal | 0.339 ± 0.316 | 0.10 | 0.20 |
| **Adaptive (Ours)** | **0.121 ± 0.239** | **0.50** | **0.70** |

### 关键发现
- 力反馈是安全有效切割的必要条件（Adaptive w/o Force vs Adaptive）
- 骨骼位置估计误差增大时，Adaptive 仍保持较好性能
- RoboNinja 不适用于此任务（依赖碰撞探测、单方向调整、大调整量）
- 真实鸡肉成功率50%，骨骼质量<0.05g的比例70%（可接受范围）


## Limitations

1. 仅测试球形骨骼形状，未验证更复杂解剖结构
2. 力信号归一化需预先采集数据并手动设定最大值
3. 依赖名义轨迹作为基础，无法从零规划切割路径
4. 仿真器保真度有限（低精度近似），仅捕捉相对力趋势而非绝对接触动力学
5. 真实鸡肉成功率仅50%，仍有较大提升空间
6. 未考虑刀具磨损和多次切割后材料变化的影响


## Key Takeaways

1. **力离散化是Sim-to-Real迁移的有效技巧**：将连续力信号离散化为有限集合，能有效弥合仿真和真实的力信号域差异。这对所有涉及力反馈的Sim-to-Real任务都有参考价值。
2. **残差策略框架适合轨迹调整问题**：给定粗略名义轨迹，让RL策略学习残差修正，比从零学习完整策略更高效。
3. **可复用物理测试台设计思路**：用可控的简化材料（Kinetic Sand + Reusable Clay）替代真实物体，保留关键物理特性（多材料、不同硬度），实现可控可重复的真实世界评估。
4. **与DLO操控的关联**：多材料切割本质上是可变形物体操控（DLO操控）的一个特定子类——需要处理可变形材料、部分可观测性、力反馈驱动的在线适应。力离散化、残差策略、可复用测试台设计思路可迁移到DLO操控研究中。

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[collision-avoidance]]
- [[deformable-linear-object]]

## 相关研究者

- [[yang-zhaodong|Yang, Zhaodong]]
- [[hu-aiping|Hu, Ai-Ping]]
- [[ravichandar-harish|Ravichandar, Harish]]
