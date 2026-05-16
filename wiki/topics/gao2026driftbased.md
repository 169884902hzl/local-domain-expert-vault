---
title: "Drift-based policy optimization: Native one-step policy learning for online robot control"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线 RL 框架，在双臂 UR5 上实现 105.2 Hz 高频闭环控制"
authors: "Gao, Yuxuan; Shen, Yedong; Zhang, Shiqi; Yu, Wenhao; Duan, Yifan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "EQGXP5FP"
---
## 摘要

Although multi-step generative policies achieve strong performance in robotic manipulation（机器人操控） by modeling multimodal（多模态） action distributions, they require multi-step iterative denoising at inference time. Each action therefore needs tens to hundreds of network function evaluations (NFEs), making them costly for high-frequency closed-loop（闭环） control and online reinforcement learning（强化学习） (RL). To address this limitation, we propose a two-stage framework for native one-step generative policies that shifts refinement from inference to training. First, we introduce the Drift-Based Policy (DBP), which leverages fixed-point drifting objectives to internalize iterative refinement into the model parameters, yielding a one-step generative backbone by design while preserving multimodal（多模态） action modeling capacity. Second, we develop Drift-Based Policy Optimization (DBPO), an online RL framework that equips the pretrained backbone with a compatible stochastic interface, enabling stable on-policy updates without sacrificing the one-step deployment property. Extensive experiments demonstrate the effectiveness of the proposed framework across offline imitation learning（模仿学习）, online fine-tuning, and real-world control scenarios. DBP matches or exceeds the performance of multi-step diffusion（扩散） policies while achieving up to $100\times$ faster inference. It also consistently outperforms existing one-step baselines on challenging manipulation（操控） benchmarks. Moreover, DBPO enables effective and stable policy improvement in online settings. Experiments on a real-world dual-arm（双臂） robot demonstrate reliable high-frequency control at 105.2 Hz.

## 中文简述

提出基于扩散模型的绳索操控方法，具有闭环控制特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. **Drift-Based Policy (DBP)**：基于 Drifting Models 原理的原生一步生成策略骨干，通过固定点漂移目标将迭代精修从推理阶段转移到训练阶段，天然 1-NFE 部署且保持多模态动作建模能力
2. **Drift-Based Policy Optimization (DBPO)**：在预训练 DBP 上构建最小随机接口，实现精确似然计算的 PPO 在线更新，同时严格保持 1-NFE 部署
3. **全面实证验证**：涵盖离线模仿学习、在线微调、真实世界部署三个维度，在 37 个点云操控任务上达到 88.4% 成功率（超越之前最优 1-NFE baseline 82.3%），真实双臂 UR5 达到 75% 成功率 @ 105.2 Hz
## 结构化提取

- **Problem**: 多步生成策略推理延迟高（数十~数百 NFE），不适合高频闭环控制和在线 RL
- **Method**: Drifting Models 原理 → DBP（训练时内化迭代精修）+ DBPO（精确似然 PPO 在线 RL）
- **Tasks**: Push-T, BlockPush, RoboMimic, Kitchen, Adroit (3 tasks), Meta-World (34 tasks), D4RL locomotion, 真实世界 Lift/Can/Transport
- **Sensors**: 低维状态, RGB 图像, 3D 点云, 多相机输入; 真实世界使用 RealSense L515 + Orbbec Gemini
- **Robot Setup**: 仿真多任务; 真实世界双臂 UR5 + NVIDIA RTX 3090 + 三相机阵列
- **Metrics**: 成功率（操控任务）, Episode Return（D4RL）, NFE（推理效率）, 控制频率 Hz, 端到端延迟 ms
- **Limitations**: 结构化桌面场景为主; 未验证非结构化长视野任务; from-scratch RL 采样效率未验证; 部分 Image 任务略逊多步方法
- **Evidence Notes**: (1) DBP 在 Diffusion Policy suite 12 任务上从 0.79→0.83，100x 加速; (2) 37 任务点云操控 88.4% 成功率，超越 OMP 82.3%; (3) Anchor 消融证实正则化关键作用; (4) 真实双臂 UR5 75% 成功率 @ 105.2 Hz, 9.5ms 延迟
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖 Abstract, Introduction, Related Work, Method (DBP+DBPO), Experiments (4 组), Conclusion; Supplementary Material 未逐段精读但正文数据完整
- Confidence: high
- Summary: 提出 Drift-Based Policy (DBP) 框架，将扩散策略的迭代去噪从推理阶段内化到训练阶段，实现原生单步 (1-NFE) 生成策略，并扩展为 DBPO 在线 RL 框架，在双臂 UR5 上实现 105.2 Hz 高频闭环控制


## Problem

多步生成策略（如 Diffusion Policy）在机器人操控中表现优异，但推理时需要数十到数百次网络评估（NFE），导致：
1. 高频闭环控制成本高昂（延迟过大）
2. 在线强化学习难以直接应用（交互代价大）

现有一步策略方案存在两类局限：
- **蒸馏加速路线**：依赖多步教师模型预训练，一步能力来自后处理压缩
- **校正路线**（Mean-Flow）：无需蒸馏但依赖辅助约束（如分散正则化、方向对齐），非原生一步

核心缺口：缺少一种将 1-NFE 效率和高策略质量作为骨干网络内在属性联合设计的原生一步策略。


## Method

### 核心思想：Drifting Models 原理

不同于扩散/流方法在推理时进行迭代精修，Drifting 将精修过程完全转移到训练阶段：
- 训练时：生成器通过 pushforward 分布的训练时演化，逐步内化校正行为
- 推理时：仅需一次前向传播生成高质量样本

### Stage 1: DBP（离线训练）

**策略设置**：
- 输入：观测历史序列 o_t^hist（长度 T_o）
- 输出：动作 chunk x_t = [a_t^1, ..., a_t^H]（H 步 horizon）
- 生成器：f_θ(o_hist, z; τ=0)，z ~ N(0,I)，τ=0 表示固定生成索引（始终一步）

**训练机制**：
- 每个 mini-batch 每条观测采样 G 个隐变量，生成 G 个假设
- 构建参考池 Y = [生成的假设, 可选负样本, 专家正样本]
- 通过 kernelized interaction 计算漂移场：
  - **吸引**：向专家正样本移动
  - **排斥**：远离生成假设和负样本
  - **反对称性质**：V_{p,q}(x) = -V_{q,p}(x)，分布平衡时漂移为零
- 固定点回归目标：x̃ = sg(G/s_norm + V)
- 损失：L_DBP = E[||G/s_norm - X̃||²]

**两种模式**：
- Chunk 模式：整条轨迹一起漂移（S = H·d_a）
- Step-wise 模式：逐步切片漂移（S = d_a），然后对 H 步平均

**收敛保证**：在标准随机逼近假设下，SGD 收敛到一阶驻点；若生成器 Jacobian 局部满秩且漂移场可识别，则零漂移稳定点对应目标分布。

### Stage 2: DBPO（在线 RL）

**精确似然随机 Actor**：
- 活跃骨干预测条件均值 μ_θ(o, z)
- 附加对数标准差头 log σ_ψ(o) = g_ψ(c_θ(o))
- Actor 分布：π_{θ,ψ}(x|o,z) = N(x; μ_θ(o,z), diag(σ_ψ(o)²))

**关键设计**：
- Rollout 时采样 z_t ~ p_0 和 x_t ~ π，存储 (z_t, x_t)
- PPO 重用存储的 z_t 计算精确条件似然比，无需对 z 边际化
- 仅优化执行前缀 x_exec 的似然（未执行后缀在下步被覆盖）

**Anchor 正则化**：
- L_anchor = E[||μ_θ(o,z) - μ_{θ̄}(o,z)||²]
- 惩罚更新后与冻结预训练均值预测的距离，稳定在线微调

**部署时**：去除高斯噪声，恢复确定性中心，严格保持 1-NFE。

### 多模态支持

支持低维状态、RGB 图像、3D 点云、多相机输入。


## Experiments

### Benchmark 1: Diffusion Policy Suite（12 任务）

| 方法 | 平均成功率 | NFE |
|------|-----------|-----|
| Diffusion Policy | 0.79 | 100 |
| **DBP (Ours)** | **0.83** | **1** |

DBP 在 Push-T (Low-Dim)、BlockPush、RoboMimic (Low-Dim) 上提升；Push-T (Image) 和 RoboMimic (Image) 略低；Kitchen 持平。100x 推理加速。

### Benchmark 2: 点云操控（37 任务，Adroit + MetaWorld）

| 方法 | 37 任务平均 | Easy | Medium | Hard | Very Hard |
|------|-----------|------|--------|------|-----------|
| MP1 (10 NFE) | 78.9% | — | — | — | — |
| OMP (1 NFE) | 82.3% | — | — | — | — |
| **DBP (1 NFE)** | **88.4±3.1%** | +2.0 | +12.9 | +12.7 | +8.9 |

相对 OMP 提升：Pen +20.0, Door 显著改善, Hammer 匹配最优。

### Benchmark 3: 在线 RL（RoboMimic + D4RL）

- DBPO 在 RoboMimic 图像任务上：离线初始化更强 + PPO 微调进一步提升
- D4RL 运动任务：跨域迁移有效
- Anchor 消融：移除 anchor 后 RoboMimic 从 0.90 降到 0.75，D4RL 从 4096.0 降到 3273.5

### Benchmark 4: 真实世界双臂 UR5

- 硬件：双臂 UR5 + NVIDIA RTX 3090 + 三相机（2x RealSense L515 腕部 + 1x Orbbec Gemini 头部）
- 演示：每任务 50 次遥操作
- 任务：Lift、Can、同步双臂 Transport
- 结果：75% 总成功率（45/60），平均延迟 9.5ms，控制频率 105.2 Hz
- 失败模式：Can 任务抓取滑动（光滑表面）；双臂 Transport 单臂不同步


## Limitations

1. 当前评估主要集中在桌面操控和运动任务的结构化场景
2. 未涉及接触密集、长视野组合任务和非结构化环境
3. DBPO 在 from-scratch 学习设置下的采样效率和大模型规模尚未验证
4. 部分任务（Push-T Image、RoboMimic Image）仍略低于多步 Diffusion Policy


## Key Takeaways

1. **原生一步 vs 后处理一步**：DBP 的 1-NFE 是训练目标本身的产物，而非蒸馏或辅助约束的结果。这一范式转变对高频控制场景有直接实用价值
2. **与 DLO 操控的关联**：DBP 的 action chunk 预测和闭环控制天然适合需要高频反馈的可变形体操控；多模态支持可适配 DLO 的视觉感知需求
3. **DBPO 的工程启示**：Anchor 正则化 + 精确条件似然比的设计使得在一步策略上做在线 RL 变得可行，这对需要在线适应的操控任务有参考价值
4. **Drifting Models 的通用性**：Drifting 原理作为生成建模框架（参考文献 [3]），可能不仅限于操控，也可用于其他需要高效采样的生成任务

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

- [[gao-yuxuan|Gao, Yuxuan]]
- [[shen-yedong|Shen, Yedong]]
