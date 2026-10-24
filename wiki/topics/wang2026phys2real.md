---
title: "Phys2Real: Fusing VLM priors with interactive online adaptation for uncertainty-aware sim-to-real manipulation"
tags: [manipulation, VLM, RL, sim-to-real]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Real RL 策略迁移，在 T-block 和锤子推动任务上显著优于 Domain Randomization。"
authors: "Wang, Maggie; Tian, Stephen; Swann, Aiden; Shorinwa, Ola; Wu, Jiajun et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QN97PJMQ"
---
## 摘要

Learning robotic manipulation（机器人操控） policies directly in the real world can be expensive and time-consuming. While reinforcement learning（强化学习） (RL) policies trained in simulation present a scalable alternative, effective sim-to-real（仿真到真实迁移） transfer remains challenging, particularly for tasks that require precise dynamics. To address this, we propose Phys2Real, a real-to-sim-to-real（仿真到真实迁移） RL pipeline that combines vision-language model（视觉-语言模型） (VLM)-inferred physical parameter estimates with interactive adaptation through uncertainty-aware fusion. Our approach consists of three core components: (1) high-fidelity geometric reconstruction with 3D Gaussian splatting, (2) VLM-inferred prior distributions over physical parameters, and (3) online physical parameter estimation from interaction data. Phys2Real conditions policies on interpretable physical parameters, refining VLM predictions with online estimates via ensemble-based uncertainty quantification. On planar pushing tasks of a T-block with varying center of mass (CoM) and a hammer with an off-center mass distribution, Phys2Real achieves substantial improvements over a domain randomization baseline: 100% vs 79% success rate for the bottom-weighted T-block, 57% vs 23% in the challenging top-weighted T-block, and 15% faster average task completion for hammer pushing. Ablation studies indicate that the combination of VLM and interaction information is essential for success. Project website: https://phys2real.github.io/.

## 中文简述

提出基于强化学习的推动方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **VLM 先验与在线自适应的不确定性感知融合**：首次将 VLM（GPT-5）用于实时低层闭环控制的物理参数估计（而非高层规划），通过逆方差加权融合 VLM 先验和交互历史估计
2. **基于集成的不确定性量化**：将不确定性分解为认知不确定性和偶然不确定性，用于指导融合权重分配；当交互信息不足时自动增加对 VLM 先验的依赖
3. **物理信息驱动的数字孪生**：结合 3D Gaussian Splatting 重建几何信息 + 在线物理参数估计，创建既几何准确又物理准确的仿真资产
4. **物理可解释参数条件策略**：扩展 RMA 框架，直接在物理可解释参数（如 CoM）上条件化策略，而非学习隐空间表示，从而可以与 VLM 估计直接融合
## 结构化提取

- **Problem**: Sim-to-Real 迁移中，DR 策略在具有特定物理属性（如偏移质心）的物体上泛化性差；RMA 在间歇接触任务中交互历史信息不足；VLM 物理参数估计存在偏差
- **Method**: Real-to-Sim-to-Real 三阶段管线：(1) 3DGS + SuGaR 几何重建；(2) PPO + 物理参数条件策略 + RMA 集成自适应模型；(3) GPT-5 VLM 先验 + RMA 在线估计的逆方差加权融合
- **Tasks**: 平面推动（T-block 推动两种质心配置 + 锤子推动），非预hensile操控
- **Sensors**: Motion capture（物体位姿），机器人关节编码器（末端执行器位姿），GPT-5 VLM（视觉物理参数估计）
- **Robot Setup**: 6-DOF UFactory xArm + 圆柱末端执行器，桌面平面场景
- **Metrics**: 成功率（位置误差<3cm 且 角度误差<20°）、最终位置误差(cm)、最终角度误差(deg)、任务完成时间(s)
- **Limitations**: 单参数单轴；仅平面推动；依赖动捕；VLM 估计有偏；对称性假设
- **Evidence Notes**:

  - 全文从 arXiv HTML 获取，包含完整正文（6 章 + 附录 A/B）和所有实验表格
  - VLM 使用 GPT-5（OpenAI 2025），论文图 3 展示了 prompt 模板
  - 仿真基于 IsaacLab (Orbit)，PPO 训练，4096 并行环境
  - 集成规模 M=10，历史窗口 H=10，Phase 1.5 噪声 σ=1.5cm
  - Diffusion Policy 基线收集了 100 demonstrations
  - 锤子重建依赖镜像对称性，对非对称物体不适用
  - Appendix B 展示了 VLM CoM 估计的具体输出示例和偏差分析
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 获取，包含正文、实验表格、附录 A/B）
- Confidence: high
- Summary: 提出 Phys2Real 框架，通过 VLM（GPT-5）先验估计物理参数（如质心）与在线交互自适应模型的逆方差加权融合，实现非预hensile推动任务的 Sim-to-Real RL 策略迁移，在 T-block 和锤子推动任务上显著优于 Domain Randomization。


## Problem

Sim-to-Real 迁移中，Domain Randomization (DR) 训练的策略在面对特定物体物理属性变化时表现不佳——策略倾向于产生"平均化"行为，牺牲了对特定物体属性（如质心位置、摩擦系数）的适应性。特别是对于需要精确动力学建模的非预hensile操控任务（如推动），物体质心偏移会显著影响旋转动力学，DR 方法难以处理。

现有方法的核心矛盾：
1. DR 不区分不同物理参数配置，策略泛化但不够精细
2. System ID 方法通常离线、静态，无法在线适应
3. RMA 类方法在间歇接触（如推动）场景下交互历史信息不足，估计不准
4. VLM 可以提供物理参数先验，但单独使用估计偏差较大


## Method

### 整体架构
Phys2Real 是一个 Real-to-Sim-to-Real 三阶段管线：

### Stage 1: Real-to-Sim 场景重建
- 用视频采集物体多视角图像
- SAM-2 分割前景物体
- 3D Gaussian Splatting (GSplat) 重建 + SuGaR 提取水密网格
- 对近似对称物体，沿主轴镜像后用 Marching Cubes 生成干净网格

### Stage 2: 物理参数条件策略学习（三阶段训练）
1. **Phase 1**：策略以仿真中的 ground-truth 物理参数（如 CoM）为条件，用 PPO 在 IsaacLab（4096 并行环境）中训练
2. **Phase 1.5**（可选）：给物理参数加高斯噪声（σ=1.5cm）微调策略，增强对下游噪声估计的鲁棒性
3. **Phase 2**：冻结策略权重，训练 M=10 个集成自适应模型，从 H=10 步观测-动作历史预测物理参数

### Stage 3: Sim-to-Real 融合部署
**VLM 估计**（θ_vlm, σ_vlm）：
- 使用 GPT-5 从 V=5 张不同视角图像各查询 Q=5 次
- 每次查询要求输出 CoM 估计值和自报不确定性
- θ_vlm = 所有查询的均值
- σ_vlm = VLM 自报不确定性的均值（论文发现用估计值的标准差效果差，因为 VLM 可能"自信地错"）

**RMA 估计**（θ_rma, σ_rma）：
- 认知不确定性：集成方差 σ²_epistemic = (1/M)Σ(θᵢ - θ_rma)²
- 偶然不确定性：每个模型输出均值和方差，σ²_aleatoric = (1/M)Σσᵢ²
- 总不确定性：σ²_rma = σ²_epistemic + σ²_aleatoric

**逆方差加权融合**：
- θ̂ = (θ_vlm/σ²_vlm + θ_rma/σ²_rma) / (1/σ²_vlm + 1/σ²_rma)
- 理论保证：在估计无偏、噪声独立且方差已知的假设下，这是 BLUE（最优线性无偏估计）


## Experiments

### 实验设置
- **机器人**：6-DOF UFactory xArm，圆柱末端执行器
- **感知**：动捕系统获取物体位姿
- **动作空间**：末端执行器 xy 位置变化量
- **观测空间**：物体位姿、末端执行器 xy、估计的物理参数

### 任务 1: T-block 推动两种配置

**配置 A：配重在顶部**（CoM = +6.1cm，21 trials/method）

| 方法 | 成功率 | 位置误差 | 角度误差 | 时间(s) |
|------|--------|----------|----------|---------|
| Phys2Real (CoM=+4.0cm) | **57.14%** | 2.60±0.90 | 2.62±1.73 | 39.58 |
| VLM-only (CoM=+4.0cm) | 4.76% | 10.10±14.33 | 12.56±32.54 | 40.80 |
| Privileged (CoM=+6.1cm) | 90.48% | 1.90±0.98 | 1.78±1.71 | 43.43 |
| RMA-only | 14.29% | 7.60±8.10 | 4.70±4.44 | 37.23 |
| DR ([-3.5, +7.5]cm) | 23.81% | 6.00±5.78 | 6.77±6.90 | 37.00 |
| Diffusion Policy | 20.83% | 25.90±16.89 | 57.38±62.50 | 54.14 |

**配置 B：配重在底部**（CoM = -0.7cm，24 trials/method）

| 方法 | 成功率 | 位置误差 | 角度误差 | 时间(s) |
|------|--------|----------|----------|---------|
| Phys2Real (CoM=+0.76cm) | **100%** | 1.76±0.54 | 4.73±2.68 | 44.28 |
| VLM-only (CoM=+0.76cm) | 91.67% | 1.90±0.59 | 3.18±1.69 | 38.27 |
| Privileged (CoM=-0.71cm) | 95.83% | 1.92±0.50 | 2.76±1.75 | 37.80 |
| RMA-only | 79.17% | 2.23±0.81 | 3.62±2.10 | 45.22 |
| DR | 79.17% | 7.14±11.34 | 11.11±13.86 | 37.50 |
| Diffusion Policy | 50.00% | 19.34±22.20 | 40.71±52.00 | 38.71 |

### 任务 2: 锤子推动（15 trials）

| 方法 | 成功率 | 位置误差 | 角度误差 | 时间(s) |
|------|--------|----------|----------|---------|
| Phys2Real (CoM=+8.9cm) | 100% | 1.74 | 4.68 | 77.79±44.08 |
| DR ([-13, +13]cm) | 100% | 1.55 | 2.89 | 90.65±42.03 |

Phys2Real 比DR快14.2%完成任务。

### 消融实验（Appendix A）：VLM 先验偏差鲁棒性
在不同 VLM CoM 估计偏差下（从 +6.0cm 到 -2.0cm），Phys2Real 始终保持 66.7%-83.3% 成功率，而 Phase 1.5 基线从 75% 骤降到 33.3%。这证明不确定性感知融合对不准确的 VLM 先验具有强鲁棒性。

### 关键观察
- 在困难配置（配重顶部）中，单独使用 VLM 或 RMA 都不够（4.76% 和 14.29%），必须融合
- VLM 对 T-block 的 CoM 估计偏向几何中心（比真实值低约 2cm）
- 接触结束后 RMA 不确定性回升（缺乏新信息），此时 VLM 先验兜底


## Limitations

1. **单参数单轴估计**：只估计沿一个轴的质心位置，未涉及摩擦、质量、刚度等多参数耦合
2. **任务范围有限**：仅验证了平面推动（planar pushing）这一种非预hensile任务，两个物体（T-block、锤子）
3. **VLM 估计偏差**：GPT-5 对物理参数的估计可能偏向几何中心，存在系统性偏差；自报不确定性校准不够精确
4. **依赖动捕**：实验依赖 motion capture 获取物体位姿，尚未验证纯视觉感知下的表现
5. **对称性假设**：Real-to-Sim 重建中对物体做镜像处理，要求近似对称，不适用于一般非对称物体
6. **仿真引擎限制**：未讨论仿真中接触动力学模型（如摩擦模型）的准确性对迁移的影响


## Key Takeaways

### 对 DLO 操控的启示
- **物理参数在线估计思路可迁移**：DLO 的弯曲刚度、密度分布等物理参数同样影响操控动力学，Phys2Real 的不确定性感知融合框架可以扩展到估计 DLO 的刚度参数
- **间歇接触问题更突出**：DLO 操控中接触更不连续，RMA 类方法的信息不足问题会更严重，VLM 先验的价值更大
- **VLM 物理推理的局限**：VLM 对 DLO 这种非刚体物体的物理参数估计能力可能更弱，需要更谨慎的不确定性量化

### 对 VLM-based 控制的启示
- **从高层规划到低层控制**：Phys2Real 是少数将 VLM 输出直接用于低层闭环控制的工作，而非仅用于高层规划
- **物理可解释参数是关键桥梁**：通过在物理可解释参数（而非隐空间）上条件化策略，才能实现 VLM 估计和自适应估计的数学融合
- **不确定性比点估计更重要**：VLM 可能"自信地错"，自报不确定性比估计值方差更可靠

### 对 Sim-to-Real 的启示
- **DR 的替代范式**：不是让策略对参数范围鲁棒，而是让策略参数条件化 + 在线估计物理参数
- **数字孪生需要物理信息**：仅几何重建不够，物理参数估计对策略性能至关重要
- **Phase 1.5 噪声注入有效**：用高斯噪声扰动物理参数条件来微调策略，简单但实用

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[diffusion-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[wang-maggie|Wang, Maggie]]
- [[tian-stephen|Tian, Stephen]]
- [[swann|Swann, Aiden]]
- [[shorinwa-ola|Shorinwa, Ola]]
