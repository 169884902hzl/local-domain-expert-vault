---
title: "Implicit Maximum Likelihood Estimation for Real-time Generative Model Predictive Control"
tags: [imitation, VLM, RL, diffusion, planning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能"
authors: "Lee, Grayson; Bui, Minh; Zhou, Shuzi; Li, Yankai; Chen, Mo et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TWFPM6DW"
---
## 摘要

Diffusion（扩散）-based models have recently shown strong performance in trajectory planning, as they are capable of capturing diverse, multimodal（多模态） distributions of complex behaviors. A key limitation of these models is their slow inference speed, which results from the iterative denoising process. This makes them less suitable for real-time applications such as closed-loop（闭环） model predictive control (MPC), where plans must be generated quickly and adapted continuously to a changing environment. In this paper, we investigate Implicit Maximum Likelihood Estimation (IMLE) as an alternative generative modeling approach for planning. IMLE offers strong mode coverage while enabling inference that is two orders of magnitude faster, making it particularly well suited for real-time MPC tasks. Our results demonstrate that IMLE achieves competitive performance on standard offline reinforcement learning（强化学习） benchmarks compared to the standard diffusion（扩散）-based planner, while substantially improving planning speed in both open-loop（开环） and closed-loop（闭环） settings. We further validate IMLE in a closed-loop（闭环） human navigation scenario, operating in real-time, demonstrating how it enables rapid and adaptive plan generation in dynamic environments. Real-world videos and code are available at https://gmpc-imle.github.io/.

## 中文简述

提出基于扩散模型的导航方法，具有闭环控制特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、扩散模型、运动规划

## 关键贡献

1. **提出基于 IMLE 的轨迹生成框架**：将 IMLE 适配为条件生成模型用于规划域，通过单次前向传播生成候选轨迹，避免扩散模型的迭代推理开销
2. **奖励加权 IMLE（Reward-Weighted IMLE）**：借鉴 Control-as-Inference（CAI）理论，用 Boltzmann 指数权重或线性权重重新加权训练样本，使模型偏向高回报轨迹
3. **FiLM 条件化 U-Net 架构**：用 Feature-wise Linear Modulation 注入初始/目标状态条件，替代扩散模型的 inpainting 方式
4. **实时移动机器人验证**：在行人环境中以 50 Hz 板载 CPU 实时规划，验证 IMLE 作为 MPPI 提案分布的有效性
5. **开源代码和实验视频**：https://gmpc-imle.github.io/
## 结构化提取

- **Problem**: 扩散模型在轨迹规划中推理速度慢，不适合实时闭环 MPC
- **Method**: Conditional IMLE + 奖励加权 + FiLM 条件化 U-Net，集成 Score-Ranked MPC 或 MPPI
- **Tasks**: 离线 RL（MuJoCo locomotion, Maze2D）+ 实时行人导航（仿真 + 真实移动机器人）
- **Sensors**: 机器人位姿（里程计），行人位置（行人检测系统，论文未详细说明传感器类型）
- **Robot Setup**: 移动机器人，板载 CPU，低级控制器高频跟踪，规划器最高 50 Hz 重规划
- **Metrics**:
- **Limitations**: 行人数据不匹配机器人动力学；分布外退化；无自适应机制；未集成视觉感知
- **Evidence Notes**:

  - 离线 RL：归一化回报（D4RL 标准）
  - 导航：碰撞率、目标误差（到终点距离）、平滑度（最大速度变化）、jerk（速度二阶差分均值）
  - 推理：采样频率（Hz）、每计划延迟（ms）
  - MuJoCo: IMLE 在大多数 D4RL 环境达到与 Diffuser 竞争力的归一化回报，推理速度快约 100 倍
  - Maze2D: 在稀疏奖励场景与 Diffuser 性能相当
  - 导航仿真: IMLE+MPPI 在 0.7m 碰撞半径下提供高质量温启动
  - 真实机器人: 50 Hz 实时规划，成功避碰并到达目标（定性展示，缺乏定量成功率报告）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取完整正文、公式、表格标题、算法伪代码和参考文献）
- Evidence Coverage: 实验表格的具体数值未完全提取（HTML 中表格渲染为图片），但表格结构和结论均有文字描述
- Confidence: high
- Summary: 用隐式极大似然估计（IMLE）替代扩散模型进行单次前向传播轨迹生成，在离线 RL 基准和实时行人导航中实现比 Diffuser 快两个数量级的推理速度，同时保持竞争力性能


## Problem

扩散模型（如 Diffuser）在轨迹规划中能捕获多模态行为分布，但其迭代去噪过程导致推理速度慢，不适用于需要快速、持续适应的实时闭环 MPC 场景。现有缓解方法（层次建模、策略蒸馏）引入额外训练复杂度。


## Method

### 核心方法：Conditional IMLE（cIMLE）

IMLE 训练一个生成器 $f_\theta(z, c)$，将隐码 $z \sim \mathcal{N}(0, I)$ 和上下文 $c$（初始状态、目标）映射为完整轨迹。训练目标：

$$\mathcal{L}_{\text{IMLE}}(\theta) = \mathbb{E}_{\{\mathcal{Z}_i\}} \left[ \sum_{i=1}^{N} \min_{z \in \mathcal{Z}_i} \| f_\theta(z, c_i) - \tau_i \|_2^2 \right]$$

对每个数据点 $\tau_i$，采样 $m$ 个隐码，找到生成最近样本的隐码 $z_i^*$，最小化该距离。这确保生成器覆盖数据分布的所有模式。

### 奖励加权变体

$$\mathcal{L}_{\text{weighted}}(\theta) = \mathbb{E}_{\{\mathcal{Z}_i\}} \left[ \sum_{i=1}^{N} w_i \cdot \min_{z \in \mathcal{Z}_i} \| f_\theta(z, c_i) - \tau_i \|_2^2 \right]$$

- **Boltzmann 权重**：$w_i = \exp\left(\frac{r_i - \text{median}(r)}{\beta \cdot \text{MAD}(r)}\right)$，理论依据来自 CAI
- **线性权重**：$w_i = \frac{r_i - r_{\min}}{r_{\max} - r_{\min}}$，作为对比基线

### 架构

- U-Net 骨干网络（与 Diffuser 相同架构）
- FiLM 条件化：$\text{FiLM}(x; c) = \gamma(c) \cdot x + \beta(c)$，通过小 MLP 将条件 $c$ 映射为逐层缩放和偏移
- 条件信号（初始状态、目标状态）在所有时空尺度上注入网络

### 规划框架

1. **Score-Ranked MPC**（离线 RL）：生成一批候选轨迹 → 学习的奖励函数评分 → 执行最高分轨迹
2. **MPPI**（导航）：IMLE 替代标准高斯提案分布作为多模态轨迹生成器，控制代价包含 CBF 安全惩罚 + CLF 目标进度项 + 偏离前一计划的时序折扣惩罚


## Experiments

### MuJoCo 离线 RL（D4RL）

- **环境**：Walker2d, Hopper, HalfCheetah（Medium, Medium-Expert, Medium-Replay, Expert）
- **对比**：Diffuser（相同 U-Net 架构）
- **结果**：IMLE 在大多数环境中达到竞争力性能（Table I），推理速度快两个数量级
- **延迟分析**（Fig. 4）：IMLE 的 generator + guidance 延迟远低于 Diffusion 的迭代去噪
- **奖励加权效果**（Table II）：Medium-Replay 和 Medium 数据集提升最大（低质量轨迹分布下效果显著），指数权重优于线性权重

### Maze2D

- **环境**：Maze2D Open, Medium, Large, Dense/Ultra
- **结果**：IMLE 在稀疏奖励长视野规划中与 Diffuser 性能相当（Table III），速度快得多
- JAX 实现：Locomotion 87.56 Hz vs PyTorch 53.52 Hz；Maze2D 133.98 Hz vs 101.28 Hz

### 行人导航仿真

- **数据**：ETH（训练）+ UCY（评估，500 场景）
- **数据增强**：平移、旋转、平滑（因原始数据中满足 CBF 约束的轨迹较少）
- **对比方法**：Gaussian MPPI, CoBL-Diffusion（DDIM 50 步）, CFM（9 步 ODE）
- **碰撞半径 0.5m**（Table IV）：IMLE 和 IMLE+MPPI 产生更平滑、低 jerk 轨迹；目标规划器在短视野安全约束上更直接
- **碰撞半径 0.7m**（Table IV）：训练分布与安全约束不匹配增大，生成模型最适合作为提案分布
- **MPPI 温启动**（Table V）：IMLE 温启动显著优于直线初始化，同时保持实时采样

### 真实移动机器人

- **平台**：移动机器人，板载 CPU
- **频率**：最高 50 Hz 重规划，batch=8
- **场景**：1-4 名行人在室内环境中自由移动，未知目标，仅观测过去位置
- **结果**：规划器持续更新轨迹分布，保持避碰同时向目标前进

### 未报告的证据

- Table I-V 中具体数值未从 HTML 中提取（渲染为图片），仅有定性描述
- 真实机器人的定量指标（成功率、碰撞率）未在正文中明确报告


## Limitations

1. **行人数据与机器人动力学不匹配**：行人轨迹数据集不能完全代表机器人动力学约束，将机器人动力学纳入奖励加权或 MPPI 精修留给未来工作
2. **分布外退化**：当最优轨迹超出训练数据分布时，IMLE 如同其他生成模型一样退化；数据增强有帮助但不够
3. **无自适应机制**：缺乏对分布偏移的自适应调整，需要如 AdaptDiffuser 等机制提升鲁棒性
4. **缺乏 VLM/感知集成**：当前仅用状态观测，未集成视觉感知或语言指令


## Key Takeaways

1. **IMLE 作为扩散模型的实用替代**：对于需要实时推理的机器人规划场景，IMLE 的单次前向传播生成比迭代去噪有显著速度优势，同时保持模式覆盖
2. **MPPI + 生成模型提案分布的设计模式**：将生成模型作为 MPPI 的高质量提案分布而非直接执行，可兼顾分布质量和安全约束满足——这对 DLO 操控中的实时 MPC 有参考价值
3. **奖励加权的 CAI 理论基础**：Boltzmann 指数权重有概率推断理论支撑，在低质量数据集中效果显著，可借鉴到 DLO 操控的模仿学习场景
4. **FiLM 条件化优于 inpainting**：对于单次生成的场景，FiLM 逐层注入条件信息比扩散模型的 inpainting 更自然
5. **局限性启示**：该方法目前仅处理状态级观测和已知动力学，与 VLM 集成、处理部分可观测性和未知动力学是开放问题

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[planning]]
- [[deformable-linear-object]]

## 相关研究者

- [[lee-grayson|Lee, Grayson]]
