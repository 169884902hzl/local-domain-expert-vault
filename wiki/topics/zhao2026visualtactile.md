---
title: "Visual-tactile peg-in-hole assembly learning from peg-out-of-hole disassembly"
tags: [manipulation, imitation, RL, robot-learning, tactile]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。"
authors: "Zhao, Yongqiang; Zhang, Xuyang; Chen, Zhuo; Leonetti, Matteo; Spyrakos-Papastavridis, Emmanouil et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VQABQ7UD"
---
## 摘要

Peg-in-hole (PiH) assembly（装配） is a fundamental yet challenging robotic manipulation（机器人操控） task. While reinforcement learning（强化学习） (RL) has shown promise in tackling such tasks, it requires extensive exploration. In this paper, we propose a novel visual-tactile（触觉） skill learning framework for the PiH task that leverages its inverse task, i.e., peg-out-of-hole (PooH) disassembly, to facilitate PiH learning. Compared to PiH, PooH is inherently easier as it only needs to overcome existing friction without precise alignment, making data collection more efficient. To this end, we formulate both PooH and PiH as Partially Observable Markov Decision Processes (POMDPs) in a unified environment with shared visual-tactile（触觉） observation space. A visual-tactile（触觉） PooH policy is first trained; its trajectories, containing kinematic, visual and tactile（触觉） information, are temporally reversed and action-randomized to provide expert data for PiH. In the policy learning, visual sensing facilitates the peg-hole approach, while tactile（触觉） measurements compensate for peg-hole misalignment. Experiments across diverse peg-hole geometries show that the visual-tactile（触觉） policy attains 6.4% lower contact forces than its single-modality counterparts, and that our framework achieves average success rates of 87.5% on seen objects and 77.1% on unseen objects, outperforming direct RL methods that train PiH policies from scratch by 18.1% in success rate. Demos, code, and datasets are available at https://sites.google.com/view/pooh2pih.

## 中文简述

提出基于强化学习的操控方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、强化学习、机器人学习、触觉感知

## 关键贡献

1. **PooH-to-PiH 框架**：首次将 PooH（拔出）和 PiH（插入）统一为共享观测/动作空间的 POMDP，通过训练简单的 PooH 策略并时间反演其轨迹来生成 PiH 训练数据
2. **视觉-触觉双模态融合**：视觉负责接近阶段的全局引导，触觉负责接触后的局部对齐校正，两者互补
3. **动作随机化**：在轨迹反演时引入随机偏移动作以丰富接触模式，弥补 PooH 和 PiH 之间的触觉不对称性
4. **大规模验证**：6 种几何形状 × 3 种间隙，仿真 + 真实双臂机器人实验，sim-to-real 迁移成功率达 72.1%
## 结构化提取

- **Problem**: PiH 装配中 RL 探索效率低，直接训练需要大量试错数据
- **Method**: PooH-to-PiH 框架；SAC + Hybrid Replay Buffer + BC Loss；POMDP 建模；动作随机化
- **Tasks**: Peg-in-hole 装配（刚性物体插入）
- **Sensors**: Intel RealSense 相机（96×96 视觉）、4× GelSight 类视觉触觉传感器（15D PCA 触觉标记流）、本体运动学（6D 末端位姿）
- **Robot Setup**: ABB YuMi 双臂机器人，仿真 MuJoCo + RoboSuite + FOTS
- **Metrics**: 成功率（插入深度 > 1cm）、最大接触力、训练奖励曲线
- **Limitations**: 触觉仿真保真度有限；紧间隙/复杂形状性能差；仅刚性物体；视觉迁移差距
- **Evidence Notes**:

  - 仿真平均成功率 80.6%（已见 87.5%，未见 77.1%），比 Direct RL 高 18.1%（Table I + Fig. 7）
  - 视觉-触觉策略降低 6.4% 接触力（Fig. 6）
  - Sim-to-real 平均 72.1%（Table I），紧间隙三角形最低 6/20
  - Ablation：去触觉 -38.3%，去视觉 -29.4%，去随机化 -14.8%（Fig. 7）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（从 arXiv 获取完整 PDF 转换文本）
- Evidence Coverage: high（全文可用，含方法、实验、ablation、sim-to-real）
- Confidence: high
- Summary: 利用逆向任务（拔出）的时间反转轨迹作为演示数据，结合视觉-触觉双模态感知和 RL，高效学习 peg-in-hole 装配策略，已验证 sim-to-real 迁移。


## Problem

Peg-in-hole (PiH) 装配是机器人的基础操作任务，但 RL 方法需要大量探索，直接从零训练 PiH 策略效率低、成功率受限。关键矛盾：
- RL 需要大量试错数据，但 PiH 接触丰富（卡死、过度力）使数据采集成本高且有硬件损伤风险
- 监督学习依赖高质量示教数据且泛化性差
- 现有利用拆装辅助装配的方法（如 Tang et al. [6]）仅反转运动学路径，未考虑正向/逆向任务的触觉不对称性


## Method

### 整体框架（三阶段）

**阶段 1：PooH 策略学习**
- 在仿真中用 SAC 训练 PooH 策略 π_out
- 观测：运动学 k_t (6D 末端位姿) + 视觉 v_t (96×96 图像) + 触觉 c_t (15D PCA 触觉标记流)
- 动作：末端执行器笛卡尔位移增量
- 奖励：负距离平方（goal-conditioned）
- 训练 1e5 steps，每 episode 50 步

**阶段 2：PiH 演示数据生成**
- 时间反演 PooH 轨迹：运动学和视觉数据直接反转，触觉数据在仿真中重新生成
- **动作随机化**（Algorithm 1）：当 peg-hole z 距离 < 0.01m 时，采样随机偏移动作 a' = [Δx, Δy, d]，使 peg 偏移后产生丰富接触，再用恢复动作 a'' 返回原路径
- 50% 的轨迹应用随机化

**阶段 3：PiH 策略学习**
- 相同环境中用 SAC 训练 PiH 策略 π_in
- **Hybrid Replay Buffer**：标准 buffer + 专家 buffer（反演数据），采样比例从 0.3 线性退火到 0
- **Behavior Cloning Loss**：辅助 BC 损失，权重 λ 从 0.05 退火到 0，引导策略模仿专家行为

### 网络架构
- CNN 编码视觉图像 → 视觉特征
- MLP 编码运动学 + 触觉 → 本体/触觉特征
- 特征融合后输入 SAC actor-critic 网络

### Sim-to-Real 迁移策略
1. **触觉校准**：数据驱动触觉仿真器（FOTS），单球压头校准，PCA 降维到 15D
2. **视觉域随机化**：物体 RGB 值 × [0.8, 1.2] 随机缩放因子
3. **真实演示数据**：每种已知物体收集 20 条真实 PooH 轨迹混入专家 buffer


## Experiments

### 实验设置
- **机器人**：ABB YuMi 双臂机器人
- **传感器**：4 个 GelSight 类视觉触觉传感器（手指上）+ Intel RealSense 相机（机身）
- **仿真**：MuJoCo + RoboSuite + FOTS 触觉仿真器
- **物体**：6 对 3D 打印（PLA/PETG）peg-hole，间隙 0.5/1.0/2.0 mm
  - 已见：红色方块、红色 D 形
  - 未见：红色圆柱、红色六边形、白色方块、红色不等边三角形
- **训练**：PooH 1e5 steps，PiH 1e5 episodes，500 条仿真 + 20 条真实轨迹/每物体
- **评估**：每物体 20 trials

### 主要结果

| 方法 | 已见成功率 | 未见成功率 | 平均成功率 |
|------|-----------|-----------|-----------|
| **Ours (visual-tactile)** | **87.5%** | **77.1%** | **80.6%** |
| Direct RL (SAC) | 62.9% | 62.1% | 62.5% |
| Supervised Learning | — | — | ~69.2% |
| Residual Policy | ~87% | ~73% | ~76% |

- 比 Direct RL 高 18.1% 成功率
- 视觉-触觉策略比单模态降低 6.4% 最大接触力

### Sim-to-Real 结果（Table I）
- PLA 1.0mm：方块 18/20，圆柱 17/20，三角形 11/20
- PETG 1.0mm：方块 16/20，圆柱 16/20，三角形 10/20
- 平均 72.1% 成功率
- 紧间隙（0.5mm）和复杂形状（三角形）性能明显下降

### Ablation 研究

| 消融项 | 平均成功率 | 降幅 |
|--------|-----------|------|
| 完整方法 | 80.6% | — |
| 去视觉 | 51.2% | -29.4% |
| 去触觉 | 42.3% | -38.3% |
| 去动作随机化 | 65.8% | -14.8% |
| 去 Hybrid Buffer | 71.4% | -9.2% |
| 去 BC Loss | 65.8% | -14.8% |

- 去触觉影响最大（-38.3%），说明接触信息对 PiH 至关重要
- 动作随机化对未见物体泛化贡献显著
- Hybrid Buffer 和 BC Loss 都不可少


## Limitations

1. **触觉仿真保真度有限**：单球压头校准、简化为三种基本运动（膨胀/剪切/扭转），sim-to-real 触觉差距仍然存在
2. **视觉迁移差距**：真实环境有线缆、连接器等仿真未建模的视觉干扰
3. **紧间隙和复杂几何下性能下降明显**：0.5mm 间隙三角形仅 6/20（PETG）
4. **未考虑力惩罚**：奖励函数中未显式惩罚接触力（避免策略过度保守），但这也意味着接触力未最优化
5. **仅限刚性物体**：未涉及可变形物体装配


## Key Takeaways

1. **逆向任务范式**：利用简单逆向任务（PooH）的轨迹反演为困难正向任务（PiH）提供演示数据，这一思想可能泛化到其他操作任务（如学习解开绳结来辅助打结、学习展开线缆来辅助缠绕）
2. **视觉-触觉分工明确**：视觉管"远"（接近阶段全局引导），触觉管"近"（接触后局部对齐），与 DLO 操控中的感知分工类似（视觉捕获全局形状，触觉感知局部接触/力）
3. **动作随机化弥合接触不对称**：反演轨迹在触觉空间存在本质不对称，随机化偏移+恢复机制是实用的解决方案
4. **Hybrid Buffer + BC Loss 退火**：从模仿逐渐过渡到自主探索的 curriculum 学习策略，适用于所有"从演示到 RL"的场景
5. **Sim-to-Real 三板斧**：触觉校准 + 视觉域随机化 + 少量真实数据，是触觉操作 sim-to-real 的标准管线
6. **对 DLO 操控的启发**：DLO 操控同样存在"正向困难、逆向简单"的不对称性（如插入 vs 抽出、缠绕 vs 解开），可以考虑类似框架

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[tactile-sensing]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhao-yongqiang|Zhao, Yongqiang]]
