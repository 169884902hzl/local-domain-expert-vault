---
title: "World4RL: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation"
tags: [manipulation, imitation, RL, diffusion, sim-to-real]
created: "2026-05-02"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-World 仿真和 Franka 真机 6 个任务上分别取得 16% 和 25% 的绝对成功率提升。"
authors: "Jiang, Zhennan; Liu, Kai; Qin, Yuxin; Tian, Shuai; Zheng, Yupeng et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "9BK3BDQH"
---
## 摘要

Robotic manipulation（机器人操控） policies are commonly initialized through imitation learning（模仿学习）, but their performance is limited by the scarcity and narrow coverage of expert data. Reinforcement learning（强化学习） can refine polices to alleviate this limitation, yet real-robot training is costly and unsafe, while training in simulators suffers from the sim-to-real（仿真到真实迁移） gap. Recent advances in generative models have demonstrated remarkable capabilities in real-world simulation, with diffusion（扩散） models in particular excelling at generation. This raises the question of how diffusion model（扩散模型）-based world models can be combined to enhance pre-trained policies in robotic manipulation（机器人操控）. In this work, we propose World4RL, a framework that employs diffusion（扩散）-based world models as high-fidelity simulators to refine pre-trained policies entirely in imagined environments for robotic manipulation（机器人操控）. Unlike prior works that primarily employ world models for planning, our framework enables direct end-to-end（端到端） policy optimization. World4RL is designed around two principles: pre-training a diffusion（扩散） world model that captures diverse dynamics on multi-task（多任务） datasets and refining policies entirely within a frozen world model to avoid online real-world interactions. We further design a two-hot action encoding scheme tailored for robotic manipulation（机器人操控） and adopt diffusion（扩散） backbones to improve modeling fidelity. Extensive simulation and real-world experiments demonstrate that World4RL provides high-fidelity environment modeling and enables consistent policy refinement, yielding significantly higher success rates compared to imitation learning（模仿学习） and other baselines.

## 中文简述

提出基于扩散模型的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、仿真到真实迁移

## 关键贡献

1. **World4RL 两阶段框架**：第一阶段在多任务数据上预训练扩散世界模型（转移模型 + 奖励分类器），第二阶段冻结世界模型，在想象 rollout 中用 RL 精炼策略，实现端到端策略优化而非仅用于规划。
2. **Two-hot action encoding**：针对连续动作设计的高效编码方案，在连续性和离散结构之间取得平衡，支持无损重建和端到端优化（K=21 bins），优于 one-hot、VQ-VAE、FAST、linear projection 等替代方案。
3. **策略精炼关键因素识别**：发现并验证了两个对稳定策略精炼至关重要的因素——更广的动作空间覆盖（训练世界模型时加入随机 rollout 数据）和受控探索（PPO 训练时将 σ 限制在 e^0 而非常见的 e^2）。
## 结构化提取

- Problem: 如何在不依赖真实机器人交互和物理仿真器的情况下，利用扩散世界模型端到端精炼模仿学习策略
- Method: World4RL 两阶段框架；扩散转移模型（EDM + U-Net 2D）+ 二分类奖励分类器（ResNet18）+ PPO 策略优化；two-hot action encoding；受控探索 σ ≤ e^0
- Tasks: Meta-World 6 任务（coffee-pull, soccer, hammer, door-lock, lever-pull, handle-pull）+ Franka 真机 6 任务（open/close drawer, pick bread in/out, pick apple, press button）
- Sensors: RGB 图像观测（视觉输入）
- Robot Setup: 仿真 Sawyer 机械臂（Meta-World）+ 真实 Franka Emika Panda + Space Mouse 遥操作数据采集
- Metrics: LPIPS, FID, FVD（世界模型质量）；Success Rate（策略性能）
- Limitations: 中等视觉分辨率/模型容量限制保真度；put bread in 真机略低于 DP；仅在少量任务验证；计算成本高；稀疏奖励对复杂长期任务不足
- Evidence Notes:

  - 仿真 6 任务平均 SR 67.5%，比 BC 基线提升 16%，超越所有 IL/Offline RL/世界模型基线（Table II）
  - 真机 6 任务平均 SR 93.3%，比 BC 提升 25%，比 DP 提升 5%（Table III）
  - 视频预测 FVD 326.5，全面优于 NWM/iVideoGPT/DiWA（Table I）
  - 样本效率：固定离线数据匹配 RLPD 346k 在线步的性能（Fig. 3）
  - Two-hot 编码优于 one-hot/linear/FAST/VQ-VAE（Table IV）
  - σ clipping 和随机 rollout 消融均显著影响性能（Fig. 5）
## 本地引用关系

- [[jiang2026world4rl]]
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取完整论文内容，含所有章节、表格、公式和参考文献）
- Evidence Coverage: complete（覆盖 Introduction、Related Work、Method、Experiments、Ablation Study、Conclusion 全部章节）
- Confidence: high
- Summary: 提出两阶段框架 World4RL，先用扩散世界模型在多任务数据上预训练动态转移模型和奖励分类器，再在冻结的想象环境中用 PPO 端到端精炼模仿学习策略，在 Meta-World 仿真和 Franka 真机 6 个任务上分别取得 16% 和 25% 的绝对成功率提升。


## Problem

机器人操控策略通常通过模仿学习（IL）初始化，但受限于专家数据的稀缺性和覆盖范围窄。强化学习（RL）可以精炼策略以缓解这一限制，但在真实机器人上训练成本高且有安全风险，而在仿真器中训练则存在 Sim-to-Real gap。核心问题：如何利用扩散模型构建的世界模型作为高保真模拟器，在完全想象的虚拟环境中端到端精炼预训练策略，避免真实交互和仿真偏差。


## Method

### 整体架构（Fig. 1）
World4RL 由三个核心组件构成：
1. **扩散转移模型 D_θ**：基于 EDM 去噪框架的动态近似器，以历史观测 x_{t-T:t}^0 和编码动作 z_{t-T:t} 为条件预测下一帧观测 x_{t+1}^0。使用 U-Net 2D 作为 F_θ 主干网络，330M 参数。
2. **奖励分类器 C_ψ**：基于 ResNet18 视觉骨干的二分类器，评估想象 rollout 是否达到成功状态，输出 r ∈ {0, 1} 的稀疏奖励信号。
3. **RL 精炼策略 π_ξ**：高斯随机策略，用 BC 初始化，在冻结世界模型中用 PPO 精炼。

### Stage 1: 预训练
- **策略预训练**：标准行为克隆（BC），最大化专家动作的对数似然。
- **奖励分类器**：在专家演示 + BC 策略 rollout 数据上训练，使用二元交叉熵损失。
- **扩散转移模型**：
  - 训练数据混合三种来源：专家演示 D_exp + 策略 rollout D_rollout + 随机 rollout D_rand
  - Two-hot 编码：对每个动作维度 a_i ∈ R，将其映射到最近两个 bin 的线性插值权重，实现无损连续-离散转换
  - 遵循 EDM 预条件化设计（c_skip, c_out, c_in, c_noise）

### Stage 2: 策略优化
- 冻结世界模型，策略 π_ξ 与世界模型交互生成想象 rollout
- 使用 PPO 优化策略（clipped surrogate objective）和价值函数（TD learning）
- **受控探索机制**：将策略标准差 σ 限制在 e^0 以内（远小于常见的 e^2），防止 OOD 动作导致世界模型生成崩溃
- 每收集足够 batch 的想象数据后执行一次 PPO 更新


## Experiments

### 仿真实验（Meta-World benchmark，6 个任务）
- **视频预测质量（Table I）**：
  - World4RL 在 FVD/FID/LPIPS 三项指标上均为最优
  - FVD: 326.5 vs NWM 547.4, iVideoGPT 450.3, DiWA 803.6
  - LPIPS: 0.0192（最佳空间保真度）
- **策略学习成功率（Table II）**：
  - World4RL 平均 67.5%（+16% over BC base 51.5%）
  - 超越所有 IL、Offline RL 和世界模型基线
  - 最具挑战的任务（coffee-pull, soccer, lever-pull）提升最大（+21%, +13%, +21%）
  - DP 仅 45.0%，TD3+BC 57.7%，DiWA 59.8%，TD-MPC2 60.0%
- **样本效率（Fig. 3）**：
  - World4RL 仅用固定离线数据达到的性能，RLPD 和 Uni-O4 分别需要 346k 和 470k 在线步数才能匹配

### 真机实验（Franka Emika Panda，6 个任务，每任务 20 次评估）
- **成功率（Table III）**：
  - World4RL 平均 93.3%（+25% over BC 68.3%）
  - BC: 68.3%, DP: 88.3%, World4RL: 93.3%
  - 最佳任务（pick bread out, close drawer）达到 100%
  - Put bread in 任务略低于 DP（16/20 vs 18/20），其余全面超越

### 消融实验
- **动作编码消融（Table IV）**：Two-hot 在 FVD/FID/LPIPS 上全面优于 One-hot、Linear、FAST、VQ-VAE
- **策略优化消融（Fig. 5）**：
  - 移除 σ clipping 导致性能下降和训练方差增大
  - 移除随机 rollout 数据导致 Door-lock 和 Lever-pull 性能显著退化

### 计算开销
- 世界模型预训练：4 × A800 GPU，20 小时
- 单任务策略精炼：1 × A800 GPU，约 6 小时


## Limitations

1. 受计算资源限制，当前实现采用中等视觉分辨率和模型容量（330M），可能限制想象 rollout 的保真度
2. Put bread in 真机任务成功率略低于 Diffusion Policy（16/20 vs 18/20），说明并非所有场景都一致受益
3. 仅在 6 个 Meta-World 任务和 6 个真机任务上验证，泛化性尚待更广泛验证
4. 世界模型预训练需 4 GPU × 20h，单任务精炼需 6h，计算成本较高
5. 稀疏奖励信号依赖二分类器质量，对复杂长期任务可能不足


## Key Takeaways

1. **扩散世界模型作为策略精炼模拟器**：与仅用于 test-time 规划的方法（IRASim, NWM）不同，World4RL 证明扩散世界模型可以支持端到端 RL 策略优化，这是思路转变。
2. **Two-hot 编码的价值**：对 DLO 操控中连续高维动作空间（如关节角度、末端位姿）的建模有直接参考意义，比 VQ-VAE 和 tokenization 更高效且无损。
3. **训练数据混合策略**：专家演示 + 策略 rollout + 随机 rollout 的三源混合对世界模型泛化至关重要，特别是随机 rollout 提供了更广的动作空间覆盖。
4. **受控探索**：在想象环境中限制策略方差是避免 OOD 生成崩溃的关键实用技巧，σ ≤ e^0 的经验值值得记住。
5. **与我们研究方向的关联**：框架完全在想象环境中优化策略，天然避免了 Sim-to-Real gap；未来可探索将此框架应用于 DLO 操控，用真实 DLO 交互数据训练世界模型，实现无物理仿真的策略精炼。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[jiang-zhennan]]
- [[li-haoran]]
- [[zhao-dongbin]]
