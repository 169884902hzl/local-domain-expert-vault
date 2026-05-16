---
title: "Jump-start reinforcement learning with vision-language-action regularization"
tags: [manipulation, imitation, VLM, RL, sim-to-real]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda 零样本 Sim-to-Real 部署。"
authors: "Moroncelli, Angelo; Zanetti, Roberto; Maccarini, Marco; Roveda, Loris"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "H5HBWCQC"
---
## 摘要

Reinforcement learning（强化学习） (RL) enables high-frequency, closed-loop（闭环） control for robotic manipulation（机器人操控）, but scaling to long-horizon（长时序） tasks with sparse or imperfect rewards remains difficult due to inefficient exploration and poor credit assignment. Vision-Language-Action (VLA) models leverage large-scale multimodal（多模态） pretraining（预训练） to provide generalist, task-level reasoning, but current limitations hinder their direct use in fast and precise manipulation（操控）. In this paper, we propose Vision-Language-Action Jump-Starting (VLAJS), a method that bridges sparse VLA guidance with on-policy RL to improve exploration and learning efficiency. VLAJS treats VLAs as transient sources of high-level action suggestions that bias early exploration and improve credit assignment, while preserving the high-frequency, state-based control of RL. Our approach augments Proximal Policy Optimization (PPO) with a directional action-consistency regularization that softly aligns the RL agent's actions with VLA guidance during early training, without enforcing strict imitation, requiring demonstrations, or relying on continuous teacher queries. VLA guidance is applied sparsely and annealed over time, allowing the agent to adapt online and ultimately surpass the guiding policy. We evaluate VLAJS on six challenging manipulation（操控） tasks: lifting, pick-and-place, peg reorientation, peg insertion, poking, and pushing in simulation, and validate a subset on a real Franka Panda robot. VLAJS consistently outperforms PPO and distillation-style baselines in sample efficiency, reducing required environment interactions by over 50% in several tasks. Real-world experiments demonstrate zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer and robust execution under clutter, object variation, and external perturbations.

## 中文简述

提出基于强化学习的推动方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **C1 — 奖励驱动的 Jump-Start 机制**：基于奖励改善趋势自适应减少 VLA 查询频率，并在策略可靠学习后永久关闭引导，使 RL 策略最终超越教师策略。
2. **C2 — 方向性动作一致性正则化**：用余弦对齐损失替代 MSE 蒸馏，仅约束动作方向不约束幅度，使 RL 策略保持自主探索能力。
3. **样本效率大幅提升**：在 6 个操控任务中，VLAJS 持续超越 PPO 和蒸馏基线，部分任务环境交互量减少 50% 以上。
4. **公开长时序评测环境**：将 ManiSkill 任务扩展为长时序和次优奖励版本，即将公开发布。
## 结构化提取

- **Problem**: RL 在长时序和次优奖励操控任务中探索效率低、信用分配差；VLA 模型语义能力强但控制频率低、依赖专家数据
- **Method**: VLAJS — PPO + 稀疏 VLA 方向引导 + 奖励趋势自适应关闭 + 方向性动作一致性正则化（余弦对齐）
- **Tasks**: 6 个桌面操控任务 — lifting (PickCube), pick-and-place (PickPlaceCube), peg reorientation (LiftPegUpright), peg insertion (PegInsertionSide), poking (PokeCube), pushing (PushCube-v2 OOD)
- **Sensors**: 仿真中 RL 策略使用本体感知 + 仿真器特权状态（物体位姿）；VLA 使用 RGB 图像 + 语言指令；真机使用 YOLO 检测器估计物体状态
- **Robot Setup**: Franka Panda 单臂机器人，仿真和真机验证
- **Metrics**: SR_t*（固定预算内成功率）、AUC（成功率曲线下面积）、bootstrap 95% CI（6 seeds）
- **Limitations**: 依赖 VLA 教师最低质量、训练 wall-clock 开销大、仅桌面场景+特权状态、启发式关闭阈值可能不稳定
- **Evidence Notes**: 论文提供完整的方法描述（Section III）、6 个任务的对比实验（Section VI）、消融（VLA 教师/相机视角/损失函数）、真机零样本迁移（Table II, Figure 9）。Table II 具体数值需查 PDF 原文确认。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 2604.13733v1, 9 sections + references)
- Evidence Coverage: complete — method, experiments (6 sim tasks + real robot), ablations, limitations 均有覆盖
- Confidence: high
- Summary: VLAJS 利用预训练 VLA 模型的稀疏方向性提示作为 PPO 的瞬态辅助正则化，在长时序和次优奖励任务中加速 RL 探索 50% 以上，并实现 Franka Panda 零样本 Sim-to-Real 部署。


## Problem

RL 在机器人操控中提供高频闭环控制，但在**长时序任务**和**稀疏/不完美奖励**场景下，因探索效率低和信用分配弱而难以扩展。VLA 模型拥有语义理解能力，但推理延迟高、控制频率低、依赖大量专家数据，无法直接用于快速精确操控。核心问题是：**能否用 VLA 的语义知识加速 RL，同时保留 RL 控制器的精度和可靠性？**


## Method

### 整体架构
VLAJS 在 PPO 框架上叠加 VLA 引导信号。RL 策略是高频、基于状态的控制器（本体感知 + 仿真器特权状态），VLA 教师仅作为稀疏、低频的方向提示源。

### 关键技术细节

**稀疏 VLA 查询与时间离散化**：
- 每个 rollout 最多查询 VLA 20% 的步数
- 每次教师输出的 delta action 通过线性插值（平移）和 SLERP（旋转）离散化为 D 步增量
- 非引导窗口内辅助损失置零

**自适应查询率**（Section III-C）：
- N_calls = max(N_min, floor(N_max * exp(-κ * Δr̄)))
- Δr̄ 为滚动窗口内的奖励增益信号（裁剪为非负）
- 奖励改善越大 → VLA 查询越少

**永久关闭**：连续多个 iteration 的平均 rollout 奖励单调上升且 Δr̄ > 3 时，永久关闭引导。

**方向性动作一致性损失**（Section III-D）：
- ℓ_dir(x, y) = 1 - ⟨x, y⟩ / (‖x‖‖y‖ + ε)
- 分别作用于平移和旋转分量，跳过夹持器维度
- 仅在有引导的 time step 上激活（通过 1[valid_t] 掩码）
- **核心设计思想**：教师动作仅作方向提示，PPO 自主决定动作幅度

**训练目标**：
- L(θ) = L_PPO(θ) + λ_t * L_dir(θ)
- λ_t 随奖励趋势衰减，关闭后置零

### Baselines
- **PPO**：标准 PPO 从零训练
- **Sparse RPD**：持续稀疏引导（不关闭），MSE 动作匹配
- **VLAJS (RPD)**：与 VLAJS 相同的稀疏查询和关闭机制，但用 MSE 替代方向性损失（消融）


## Experiments

### 仿真环境
ManiSkill3 环境，6 个任务：PickCube, PickPlaceCube, LiftPegUpright, PegInsertionSide, PokeCube, PushCube-v2（OOD 任务）。

### Use Case 1 — 长时序（10x horizon）
- **对比**：PPO vs Sparse RPD
- **结果**（Table III 宏平均）：Sparse RPD 在 SR_t* 和 AUC 上均大幅领先 PPO
- **结论**：即使非常稀疏的 VLA 辅助引导也能显著加速长时序探索

### Use Case 2 — 次优奖励设计
- **对比**：PPO vs VLAJS(RPD) vs VLAJS
- **结果**（Table I）：
  - VLAJS(RPD) 在次优奖励下改进有限或不一致
  - VLAJS 在所有 6 个任务中均取得最高 SR_t* 和 AUC
  - 包括 OOD 任务 PushCube-v2（VLA 未训练过的任务）
  - 引导关闭后策略继续改善，说明未被教师约束
- **样本效率**：多任务环境交互减少 50% 以上

### 真实机器人部署（Franka Panda）
- **设置**：零样本 Sim-to-Real 迁移，YOLO 检测器提供状态估计
- **结果**（Table II）：每任务 20 次试验的成功率（具体数值见论文 Table II）
- **鲁棒性**（Figure 9）：VLA-only 策略在干扰/遮挡下失败，VLAJS 策略保持稳定

### 消融实验
- **不同 VLA 教师**（Figure 10a）：OpenVLA (10% s.r.), OpenVLA-best (40% s.r.), Octo (10% s.r.) — 即使弱教师也能加速学习
- **不同相机视角**（Figure 10b）：OOD 相机位置下 VLAJS 仍有效
- **方向性损失 vs MSE**：VLAJS 持续优于 VLAJS(RPD)，证明方向性约束的优势

### 实验缺失 / 未报告
- Table II 具体数值在 HTML 中未能完整提取（但表格存在）
- 推理延迟 / 训练 wall-clock 时间未详细报告（仅定性讨论）
- 多阶段任务 / 多物体场景未测试


## Limitations

1. **VLA 教师依赖**：仍需至少能提供方向性提示的教师，当前 VLA 通常需要环境特定的微调
2. **训练开销**：大 VLA 推理导致 GPU 显存压力和非平凡 wall-clock 开销
3. **场景局限**：实验限于桌面操控 + 特权状态；扩展到视觉 RL、力交互、多阶段任务需额外组件
4. **启发式关闭**：基于奖励的关闭阈值在高度随机环境中可能不稳定
5. **仅 Franka Panda**：未在其他机器人平台验证


## Key Takeaways

1. **稀疏瞬态引导优于持续蒸馏**：VLA 作为方向提示源比作为持续教师更实用，尤其在教师不完美时
2. **方向约束 vs 幅度约束**：仅约束方向释放了 RL 策略的动作幅度自由度，这是样本效率提升的关键机制
3. **弱教师也有效**：即使 10% 成功率的 VLA 也能加速 RL，降低了方法对教师质量的门槛
4. **状态策略的鲁棒性**：基于状态的 RL 策略天然抗视觉干扰，Sim-to-Real 迁移比 VLA 直接部署更稳定
5. **对 DLO 操控的启发**：DLO 任务中奖励设计极困难，VLAJS 的稀疏方向引导范式可能特别适用 — 用 VLA 提供粗略的 DLO 交互方向，RL 学习精确的力/轨迹控制

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[moroncelli|Moroncelli, Angelo]]
- [[roveda|Roveda, Loris]]
