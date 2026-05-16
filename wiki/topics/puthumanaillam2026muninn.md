---
title: "Muninn: Your trajectory diffusion model but faster"
tags: [manipulation, VLM, diffusion, diffusion-model, planning]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理加速且保持轨迹质量与安全性。"
authors: "Puthumanaillam, Gokul; Jiang, Hao; Hernandez, Ruben; Fuentes, Jose; Padrao, Paulo et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "MMQE4I6H"
---
## 摘要

Diffusion（扩散）-based trajectory planners can synthesize rich, multimodal（多模态） robot motions, but their iterative denoising makes online planning and control prohibitively slow. Existing accelerations either modify the sampler or compress the network--sacrificing plan quality or requiring retraining without accounting for downstream control risk. We address the problem of making diffusion（扩散）-based trajectory planners fast enough for real-time robot use without retraining the model or sacrificing trajectory quality, and in a way that works across diverse state-space diffusion（扩散） architectures. Our key insight is that diffusion（扩散） trajectory planners expose two signals we can exploit: a cheap probe of how their internal trajectory representation changes across steps, and analytic coefficients that describe how denoiser errors affect the sampler's state update. By calibrating the first signal against the second on offline runs, we obtain a per-step score that upper-bounds how far the final trajectory can deviate when we reuse a cached denoiser output, and we treat this bound as an uncertainty budget that we can spend over the denoising process. Building on this insight, we present Muninn, a training-free caching wrapper that tracks this uncertainty budget during sampling and, at each diffusion（扩散） step, chooses between reusing a cached denoiser output when the predicted deviation is small and recomputing the denoiser when it is not. Across standard benchmarks Muninn delivers up to 4.6x wall-clock speedups across several trajectory diffusion（扩散） models by reducing denoiser evaluations, while preserving task performance and safety metrics. Muninn further certifies that cached rollouts remain within a specified distance of their full-compute counterparts, and we validate these gains in real-time closed-loop（闭环） navigation and manipulation（操控） hardware deployments. Project page: https://github.com/gokulp01/Muninn.

## 中文简述

提出基于扩散模型的导航方法，具有闭环控制特点。

**研究方向**: 机器人操控、视觉-语言模型、扩散模型、扩散模型、运动规划

## 关键贡献

1. **Muninn 缓存框架**：首个面向轨迹扩散模型的训练无关（training-free）缓存包装器，通过 probe 信号和采样器灵敏度系数在线决策是否复用去噪器输出。
2. **轨迹级偏差预算**：基于采样器 Lipschitz 分析推导出全局误差传播公式 $\|\Delta_0\| \leq \sum_{t=1}^{T} L_t \|e_t\|$，将每步去噪误差的轨迹影响量化为可加权的 per-step cost，并提供概率偏差保证 $P(d(\tau_0^{full}, \tilde{\tau}_0) > \eta_{traj}) \leq \alpha$。
3. **Conformal 校准机制**：利用 split-conformal prediction 从离线标定数据中学习 score-to-error 的分布无关上界，避免启发式阈值调参。
4. **广泛验证**：覆盖 D4RL 离线 RL、配置空间运动规划、视觉运动扩散策略三大场景，以及 ASV/UAV/机械臂三类硬件平台的闭环部署。
## 结构化提取

- **Problem**: 扩散轨迹规划器迭代去噪导致推理延迟过高，无法满足实时机器人控制需求；现有加速方法要么牺牲质量要么需要重新训练，且不提供轨迹偏差保证。
- **Method**: Training-free 缓存包装器；利用去噪器 stem 的轻量 probe（$F_t$）和采样器解析灵敏度系数（$L_t$），通过 split-conformal prediction 校准 score-to-error 上界，在线维护轨迹偏差预算（$\eta_{traj}$）自适应决策复用/重算。
- **Tasks**: 离线 RL 轨迹规划（MuJoCo locomotion, Maze2D, AntMaze, FrankaKitchen, Kuka stacking）、配置空间运动规划（7-DoF arm in clutter）、视觉运动模仿操控（RLBench, MetaWorld, DP3 Pour）、硬件闭环部署（ASV 导航、UAV 导航、桌面操控）。
- **Sensors**: 视觉输入（RLBench/MetaWorld 2D 图像, DP3 3D 点云）、状态输入（关节角度、位姿、速度）、配置空间（关节空间）。
- **Robot Setup**: MuJoCo 仿真正运动/导航、Kuka 机械臂堆叠、7-DoF 机械臂规划、RLBench 桌面操控、SO-ARM100 桌面操控、Crazyflie 四旋翼、SeaRobotics ASV 水面艇。
- **Metrics**: D4RL 归一化分数、成功率、碰撞率、wall-clock 延迟（ms）、去噪器评估次数、轨迹偏差 $E[d]$、违反概率 $\hat{p}_{viol}$。
- **Limitations**: 仅适用状态空间轨迹扩散模型；probe 设计需针对架构调整；离线标定依赖部署分布可交换性；固定 $\eta_{traj}$ 不自适应场景难度；少步采样器加速空间有限。
- **Evidence Notes**: 全文 38 页包含完整的方法推导（Sections III-IV）、4 组仿真基准实验（Tables I-III, V-VII）、3 个硬件平台闭环验证（Table IV）、消融实验（Appendix D）、以及运行时升级策略（Appendix D）。所有实验在 NVIDIA A10 GPU 上运行，每个场景 150 个未见 episode 取平均。
## 本地引用关系

- [[chi2024diffusion]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文 38 页，涵盖方法推导、5 组基准实验、硬件验证、消融实验、附录）
- Confidence: high
- Summary: 提出训练无关的缓存包装器 Muninn，利用扩散去噪器的轻量 probe 和解析采样器灵敏度系数构建轨迹偏差预算，在线自适应决定复用/重算去噪器输出，实现最高 4.6× 推理加速且保持轨迹质量与安全性。


## Problem

扩散模型作为轨迹规划器能生成多模态机器人运动，但迭代去噪过程导致在线规划与控制速度过慢。现有加速方法要么修改采样器（牺牲规划质量），要么压缩网络（需要重新训练），且都不考虑下游控制风险。核心问题：如何在不重新训练模型、不牺牲轨迹质量的前提下，让扩散轨迹规划器足够快以支持实时机器人控制，且适用于多种状态空间扩散架构。


## Method

### 核心思想

扩散轨迹规划器在每个去噪步都有两个可利用的信号：
- **Probe 特征** $F_t = \Psi(\tilde{\tau}_t, t, c)$：去噪器中廉价的 input processing 阶段（stem）的中间表示。相邻步 probe 变化小 → 去噪器输出稳定 → 可安全复用。
- **解析灵敏度系数** $L_t = L'_t \prod_{j=1}^{t-1} K_j$：从采样器（DDPM/DDIM）的仿射更新公式中直接计算，描述第 t 步的误差被后续步放大的程度。

### 算法流程

1. **离线标定**（一次性）：
   - 运行 N 次完整扩散 + 配对的 ghost 复用链
   - 收集 (score $s_t$, 误差 $\epsilon_t$) 对
   - 用 split-conformal regression 拟合上界函数 $U(s)$

2. **在线推理**（每个规划周期）：
   - 初始化预算 $B_{rem} = \eta_{traj}$
   - 从 t=T 到 t=1 逐步执行：
     - 计算 probe $F_t$ 和 score $s_t$
     - 计算 per-step cost 上界 $\hat{c}_t(s_t) = \Gamma L_t U_t(s_t)$
     - 若 $\hat{c}_t > B_{rem}$ 或 t 在禁止区域：重算去噪器
     - 否则：复用缓存输出，扣减预算 $B_{rem} -= \hat{c}_t$

### 关键设计选择

- **Forbidden regions**：禁止在去噪链前缀（高噪声高灵敏度）和后缀（直接影响执行运动）复用
- **Probe 设计**：Transformer 用前几层 attention/MLP blocks + mean-pool；MLP 用倒数第二层隐藏层
- **Score 定义**：$s_t = \frac{\|F_t - F_{t+1}\|_1}{\|F_{t+1}\|_1 + \omega}$（相邻步 probe 变化的相对量）


## Experiments

### 基准与数据集

**离线 RL / 轨迹规划**（Table I）：
- D4RL MuJoCo（HalfCheetah, Hopper, Walker2d）
- D4RL Maze2D / AntMaze 导航
- D4RL FrankaKitchen 长时域操控
- Kuka 积木堆叠
- 模型：Diffuser, Decision Diffuser, Diffusion-QL, AdaptDiff, CompDiff

**配置空间运动规划**（Table II）：
- 7-DoF 机械臂在杂乱场景中的轨迹规划
- 模型：MPD, EDMP

**视觉运动模仿操控**（Table III）：
- RLBench Reach Target（Diffusion Policy）
- MetaWorld pick-place-v2（Diffusion Policy）
- DP3 Pour（3D Diffusion Policy）

**硬件部署**（Table IV）：
- SeaRobotics ASV 水面导航
- Crazyflie 四旋翼 3D 导航
- SO-ARM100 桌面机械臂（pick-and-place, stacking, peg insertion）

### 主要结果

- **加速**：最高 4.6× wall-clock 加速，去噪器评估次数减少最多 7.7×
- **任务性能保持**：D4RL 归一化分数下降 < 1%（大多数场景）
- **延迟降低**：最高 78% wall-clock 延迟降低
- **偏差控制**：$\hat{p}_{viol}$（轨迹偏差超阈值概率）均在 0.03-0.07 范围内，符合用户指定风险水平
- **硬件验证**：ASV 成功率 95.3%（vs 95.5% Full），UAV 92.8%（vs 93.0%），SO-100 操控 81.5%（vs 82.0%）

### 消融实验（Appendix D）

1. 增大 $\eta_{traj}$ 提供平滑的加速-保真度旋钮
2. Split-conformal 校准是可靠达到目标违反概率的必要条件
3. 灵敏度感知预算分配（$\Gamma L_t$）优于均匀分配
4. 浅层 stem probe 在预测性和开销之间达到最佳平衡
5. 禁止前缀/后缀复用进一步减少碰撞/约束违反
6. 校准具有样本效率，少量 rollout 后风险和速度即稳定

### 推理时加速基线对比（Table V, AntMaze）

| 方法 | 任务性能↑ | E[d]↓ | $\hat{p}_{viol}$↓ |
|------|-----------|--------|---------------------|
| Full | 68.7 | 0.00 | 0.00 |
| FewSteps | 56.1 | 0.12 | 0.17 |
| FixedSkip | 42.5 | 0.10 | 0.14 |
| ProbeThresh | 48.0 | 0.09 | 0.10 |
| **Muninn** | **67.6** | **0.07** | **0.04** |

Muninn 在任务-延迟-风险 Pareto 前沿上严格优于其他推理时加速方法。

### 训练时加速对比（Fig. 9, DP3 Pour）

Muninn 无需额外训练即可获得大部分可达延迟降低，且可与蒸馏/小型网络组合叠加加速。


## Limitations

1. **架构适用性**：目前仅适用于状态空间轨迹扩散模型（state-space trajectory diffusion），对像素空间扩散模型或其他架构族需重新定义 probe（文中承认 adaptation 可 nontrivial）。
2. **Probe 选择需人工判断**：stem 的截取深度和 probe 函数设计仍需针对具体架构调整。
3. **离线标定依赖**：需要部署分布上的标定数据，分布漂移（domain shift）可能使 conformal 上界失效。
4. **固定预算**：当前 $\eta_{traj}$ 由用户预设，不随场景难度自适应（作者指出这是未来方向）。
5. **增量改进有限**：对于已经很少步数的采样器（如 Diffusion-QL 仅 10 步），加速空间较小。
6. **理论假设**：依赖采样器的 Lipschitz 性质（Assumption 1），对于非标准采样器可能不成立。


## Key Takeaways

1. **扩散推理加速可保证安全性**：Muninn 证明了通过解析灵敏度分析 + conformal prediction，可以在不重新训练的情况下获得有概率保证的轨迹偏差上界，这对安全关键机器人部署意义重大。
2. **对 DLO 操控的启发**：DLO 操控中的扩散策略同样面临推理延迟问题（如 Diffusion Policy 在实时控制中的瓶颈），Muninn 的缓存框架可直接应用于 DLO 扩散策略加速。
3. **Probe 设计的通用性**：利用去噪器 stem 层的中间表示作为廉价稳定性信号是一个通用思路，可迁移到其他扩散策略架构。
4. **难度自适应计算**：Muninn 在复杂场景自动增加计算、简单场景自动减少，这比均匀跳步更合理，对于 DLO 操控中接触/自由空间切换等变难度场景有参考价值。
5. **Composable 加速**：Muninn 可叠加在蒸馏/压缩模型之上获得额外加速，这对已有加速优化的扩散策略有实用价值。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[planning]]
- [[deformable-linear-object]]

## 相关研究者

- [[puthumanaillam|Puthumanaillam, Gokul]]
