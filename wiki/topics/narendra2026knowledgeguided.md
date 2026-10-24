---
title: "Knowledge-guided manipulation using multi-task reinforcement learning"
tags: [manipulation, imitation, RL, robot-learning]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出KG-M3PO框架，将在线3D场景图（动态更新空间/包含/可供性关系）通过GNN编码器端到端融入M3PO强化学习训练循环，在部分可观测的多任务机械臂操控中显著优于纯视觉基线，且对图噪声具有鲁棒性"
authors: "Narendra, Aditya; Maribjonov, Mukhammadrizo; Makarov, Dmitry; Yudin, Dmitry; Panov, Aleksandr"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "B8CSS7T6"
---
## 摘要

This paper introduces Knowledge Graph based Massively Multi-task（多任务） Model-based Policy Optimization (KG-M3PO), a framework for multi-task（多任务） robotic manipulation（机器人操控） in partially observable settings that unifies Perception, Knowledge, and Policy. The method augments egocentric vision with an online 3D scene graph that grounds open-vocabulary detections into a metric, relational representation. A dynamic-relation mechanism updates spatial, containment, and affordance（可供性） edges at every step, and a graph neural encoder is trained end-to-end（端到端） through the RL objective so that relational features are shaped directly by control performance. Multiple observation modalities (visual, proprioceptive, linguistic, and graph-based) are encoded into a shared latent space, upon which the RL agent operates to drive the control loop. The policy conditions on lightweight graph queries alongside visual and proprioceptive inputs, yielding a compact, semantically informed state for decision making. Experiments on a suite of manipulation（操控） tasks with occlusions, distractors, and layout shifts demonstrate consistent gains over strong baselines: the knowledge-conditioned agent achieves higher success rates, improved sample efficiency, and stronger generalization to novel objects and unseen scene configurations. These results support the premise that structured, continuously maintained world knowledge is a powerful inductive bias for scalable, generalizable manipulation（操控）: when the knowledge module participates in the RL computation graph, relational representations align with control, enabling robust long-horizon（长时序） behavior under partial observability.

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、强化学习、机器人学习

## 关键贡献

1. **统一架构KG-M3PO**：将动态更新的3D场景图与M3PO RL智能体集成，形成 Perception → Knowledge → Policy 管线
2. **在线关系更新机制**：每10步刷新受影响子图的CLIP嵌入和空间关系（spatial/containment/affordance边），保持时序一致性
3. **知识条件化策略接口**：通过轻量图查询提供目标和上下文信号，支持多任务策略学习
4. **全面基准测试**：覆盖5个操控任务、2种机器人（Franka 7-DoF、UR5 6-DoF）、全可观/部分可观设定，对比6种RL算法（PPO/SAC/DreamerV3/TD-MPC2/IMPALA/M3PO）
## 结构化提取

- Problem: 部分可观测环境下的多任务机械臂操控——目标被遮挡、隐藏或移动后，纯视觉策略因状态混叠而失败
- Method: KG-M3PO——在线3D场景图（BBQ构建，每10步动态更新空间/包含/可供性关系）+ GNN端到端编码（通过RL损失训练）+ M3PO model-based策略优化；多模态融合（视觉+图+语言+本体感知）
- Tasks: Pick (FO), Pick-Place (FO), Open-Cabinet (FO), PO Pick (墙后目标), PO Pick-Place (两阶段，先移遮挡物)
- Sensors: 腕部RGB相机 (64×64), 深度传感器（场景图构建用）, 关节编码器（本体感知）
- Robot Setup: Franka Emika Panda (7-DoF + Franka平行爪) / UR5 (6-DoF + Robotiq 2F平行爪); NVIDIA Isaac Sim/Lab仿真; 1024并行环境; RTX 5070 Ti
- Metrics: 归一化分数 (0-1000, 相对于随机策略和专家策略), 成功率, AUC, 采样效率（步数到目标分数）, 计算效率（GPU时间）
- Limitations: 仅仿真无真机验证; 图构建依赖仿真器GT微调; 快速动态场景关系时序一致性受限; 每步计算开销; 未测试DLO/双手等复杂操控场景
- Evidence Notes: 全文可获取（arXiv HTML），实验覆盖5个任务×2种机器人×6种算法×2种输入模式（camera-only/camera+KG），含噪声消融和计算效率分析。Table II-V中部分精确数值因HTML渲染限制不可直接读取，但图(Fig.6-8)中趋势清晰可辨
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML)
- Evidence Coverage: 完整覆盖摘要、方法、实验、消融、结论；表格数据部分缺失精确数值（HTML渲染导致），但趋势和对比关系清晰
- Confidence: high
- Summary: 提出KG-M3PO框架，将在线3D场景图（动态更新空间/包含/可供性关系）通过GNN编码器端到端融入M3PO强化学习训练循环，在部分可观测的多任务机械臂操控中显著优于纯视觉基线，且对图噪声具有鲁棒性


## Problem

机器人在非结构化环境中执行操控任务时面临**部分可观测性**问题：目标物体被遮挡、被移动、或隐藏在容器中，单视角视觉信息不足以维持可靠的状态估计。现有方法的不足：
1. **端到端反应式RL**：缺乏持久化的结构化世界模型，容易发生状态混叠（state aliasing），长时序信用分配困难
2. **静态预计算场景图**：无法跟踪动态变化，很快过时
3. **多任务泛化**：单一策略需支持异构目标（pick、place、open），且跨机器人平台（Franka/UR5）适用


## Method

### 核心架构

KG-M3PO由三个模块组成：

**1. 知识图构建（BBQ + 在线更新）**
- 使用BBQ方法从RGB-D序列构建3D场景图
- 图节点编码：3D包围盒中心、包围盒尺寸、512维CLIP嵌入
- 图边类型：空间关系（in front of, behind, on, under）、包含关系、可供性
- 在线更新：每n=10步检测被移动物体，刷新受影响子图的CLIP嵌入和局部空间关系
- 用仿真器真值（物体身份和6D位姿）微调生成的图以提升鲁棒性

**2. 端到端融合**
- 视觉嵌入：z_img = f_ψ(I_t)，64×64腕部RGB图像
- 知识嵌入：q_t = GNN_φ(K_t) ∈ R^32，场景图经GNN编码
- 语言目标嵌入：u_t = e(g_t)，任务描述编码
- 本体感知：x_prop（关节状态）
- 融合策略状态：s_t = [W_I·z_img || W_K·q_t || W_T·u_t || x_prop]

**3. 控制头**
- 高斯策略 π_θ(a_t|s_t) = N(μ_θ(s_t), Diag(σ²_θ(s_t)))
- 标量价值函数 V_ξ(s_t)
- **关键创新**：GNN参数φ通过RL损失直接训练（Eq. 9），策略梯度通过s_t反向传播到q_t再到φ，无需辅助监督

### 训练基础设施
- 基于NVIDIA Isaac Lab + Isaac Sim
- 1024个并行环境，单RTX 5070 Ti (16GB) + 64GB RAM
- 课程学习（CurriculumManager）逐步增加任务难度
- 域随机化：质量、摩擦、外力推动、纹理、光照、相机噪声


## Experiments

### 实验设置

**任务（5个）**：
- 全可观测（FO）：Pick、Pick-Place、Open-Cabinet
- 部分可观测（PO）：PO Pick（目标隐藏在墙后）、PO Pick-Place（两阶段，需先移除遮挡物）
- Episode长度：FO任务24步，PO Pick-Place 48步

**机器人平台**：
- Franka Emika Panda (7-DoF) + Franka平行爪夹爪
- UR5 (6-DoF) + Robotiq 2F系列平行爪夹爪

**动作空间**：连续末端执行器delta位姿命令（SE(3) twist）+ 标量夹爪命令

**基线算法**：PPO、SAC、DreamerV3、TD-MPC2、IMPALA、M3PO

### 主要结果

**单任务结果（Fig. 6, Table II）**：
- 在所有3个FO任务中，添加KG一致提升采样效率并略微提高最终分数
- M3PO在整个训练过程中领先，IMPALA第二，TD-MPC2第三
- Pick任务（简单单物体）KG提升有限；Pick-Place和Open-Cabinet受益显著
- KG-M3PO相比M3PO在复杂任务中更快达到阈值性能

**多任务结果（Fig. 7）**：
- M3PO取得最高分数，IMPALA和TD-MPC2跟随
- MT-SAC和MT-PPO学习较慢

**部分可观测结果（Fig. 8）**：
- KG-M3PO稳步上升，camera-only M3PO因遮挡下的状态混叠停留在随机水平
- 动态场景图作为持久化关系状态，保留了超越当前像素观测的任务相关信息

**计算效率（Table III-IV）**：
- KG增加每步计算开销（检测、图更新、图编码）
- 但KG-M3PO在更少步数内达到目标分数，尤其PO任务
- 简单FO任务在紧计算预算下，camera-only可能稍快

### 消融实验

**图噪声鲁棒性（Table V, Open-Cabinet任务）**：
- 三种噪声轴：中心噪声(σ_c)、尺寸噪声(σ_e)、旋转噪声(σ_r)
- Clean → Low(2%,5%,5°) → High(5%,10%,5°)
- 即使High噪声，KG-M3PO (61%)仍显著优于camera-only M3PO (50%)
- 中心噪声影响最大（直接影响空间关系计算），尺寸和旋转影响较小
- 每10步局部更新策略限制了瞬态检测失败的误差累积


## Limitations

1. **无真实机器人验证**：所有实验均在仿真中完成，真实世界部署面临延迟、驱动约束、3D场景图构建鲁棒性等挑战
2. **图构建依赖仿真器真值**：实际使用BBQ生成图后用仿真器GT微调，真实场景中GT不可用
3. **动态场景限制**：快速物体运动、频繁接触、拓扑变化可能破坏关系的时序一致性
4. **每步计算开销**：KG管线（检测+图更新+GNN编码）增加计算成本，对简单任务可能不划算
5. **固定更新频率**：每10步更新一次子图，可能在快速动态变化中不够灵活
6. **实验规模**：5个任务、2种机器人，泛化到更多样化的操控场景（如DLO操控、双手操控）尚未验证


## Key Takeaways

1. **结构化知识作为归纳偏置**：将场景图嵌入RL训练循环是比纯像素更有效的部分可观测处理方式，图的关系表征直接服务于控制目标
2. **端到端训练GNN至关重要**：通过RL损失直接训练GNN（而非预训练或冻结）使关系表征与控制对齐，比解耦方法更有效
3. **动态更新优于静态图**：每步更新图编码、每10步刷新子图内容的策略平衡了信息新鲜度和计算开销
4. **多模态融合简洁有效**：视觉+图+语言+本体感知的拼接融合方式简单但有效，32维图嵌入已足够
5. **与DLO操控的关联**：虽然本文聚焦刚体操控，但其动态关系图框架可扩展至DLO——DLO的形变状态、与环境的接触/缠绕关系天然适合图结构表征

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[narendra|Narendra, Aditya]]
- [[panov-aleksandr|Panov, Aleksandr]]
