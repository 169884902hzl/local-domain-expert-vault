---
title: "DSSP: Diffusion state space policy with full-history encoding"
tags: [manipulation, imitation, diffusion, DLO]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出基于 Mamba SSM 的全历史编码扩散策略 DSSP，通过因果历史编码器和动力学感知辅助损失压缩长时序观测历史，以层级前缀条件机制融合历史上下文与近期状态进行动作去噪，在 RoboTwin 上以最小模型参数（44.3M）取得 SOTA。"
authors: "Guan, Zhiyuan; Hu, Jianshu; Fang, Han; Jiang, Yunpeng; Huang, Yize et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "7I6B9RUN"
---
## 摘要

Diffusion（扩散）-based imitation learning（模仿学习） has shown strong promise for robot manipulation（机器人操控）. However, most existing policies condition only on the current observation or a short window of recent observations, limiting their ability to resolve history-dependent ambiguities in long-horizon（长时序） tasks. To address this, we introduce DSSP, a history-conditioned Diffusion（扩散） State Space Policy that enables efficient, full-history conditioning for robot manipulation（机器人操控）. Leveraging the continuous sequence modeling properties of State Space Models (SSMs), our history encoder effectively compresses the entire observation stream into a compact context representation. To ensure this context preserves critical information regarding future state evolution, the encoder is optimized with a dynamics-aware auxiliary training objective. This high-level context representation is then seamlessly fused with recent state observations to form a hierarchical conditioning mechanism for action generation. Furthermore, to maintain architectural consistency and minimize GPU memory overhead, we also instantiate the diffusion（扩散） backbone itself using an SSM. Extensive experiments across simulation benchmarks and real-world manipulation（操控） tasks show that DSSP achieves state-of-the-art（现有最优方法） performance with a significantly smaller model size, demonstrating superior efficiency of the hierarchical conditioning in capturing crucial information as the history length increases.

## 中文简述

提出基于扩散模型的绳索操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、可变形物体操控

## 关键贡献

1. **层级条件化状态空间策略**：设计以 SSM（Mamba）为骨干的策略框架，采用层级条件机制——学习到的上下文表示和即时状态表示通过前缀条件融合，扩散时间步通过 AdaLN 独立注入，实现任务条件与去噪步调制的解耦。

2. **全历史上下文学习**：提出因果 SSM 历史编码器，通过递归方式将多模态观测流压缩为紧凑上下文表示；配合动力学感知辅助目标（预测下一状态表示），确保上下文保留对未来状态演化有预测力的历史信息。

3. **全面评测**：在 87 个仿真任务（RoboTwin 2.0、MetaWorld、Adroit）和 3 个真实世界长时序任务上验证，DSSP 以最小模型规模（44.3M）在 RoboTwin 上取得 SOTA。

4. **理论分析**：证明历史条件化的扩散策略的损失始终不高于纯观测策略（Proposition 4.1），且在存在观测混淆时严格降低损失（Proposition 4.2）。
## 结构化提取

- **Problem**: 长时序操控中的观测混淆（observation aliasing）——相似视觉观测对应不同任务阶段，短窗口策略无法区分
- **Method**: 因果 Mamba SSM 历史编码器 + 动力学感知辅助损失 + 层级前缀条件化 + SSM 去噪骨干
- **Tasks**: RoboTwin 2.0 双臂操控（50 任务）、MetaWorld 单臂桌面（34 任务）、Adroit 灵巧手（3 任务）、真实世界长时序（3 任务：Put Bottles / Object Swap / Morse Tapping）
- **Sensors**: Intel RealSense L515 点云 + 机器人本体感知（关节角等）
- **Robot Setup**: RoboTwin 双臂仿真、MetaWorld 单臂仿真、Adroit 灵巧手仿真、真实 AgileX 平台 + 固定 L515 摄像头
- **Metrics**: 任务成功率（success rate），RoboTwin 100 episodes，MetaWorld/Adroit 20 episodes × top-5 平均，真实世界 20 trials
- **Limitations**: 不解决底层感知/控制失败；仅 3 个真实桌面任务固定视角；未测试可变形物体和动态环境；轨迹级训练可能限制可扩展性
- **Evidence Notes**: 全文实验覆盖完整，消融研究充分（骨干对比、历史长度、扰动鲁棒性、组件消融），真实世界失败模式有详细分析。理论证明在 Appendix E，使用全方差分解和信息论推导。RoboTwin 按时序分组的依据（episode 长度阈值）在 Appendix C.3。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整（摘要、方法、实验、消融、附录均覆盖）
- Confidence: high
- Summary: 提出基于 Mamba SSM 的全历史编码扩散策略 DSSP，通过因果历史编码器和动力学感知辅助损失压缩长时序观测历史，以层级前缀条件机制融合历史上下文与近期状态进行动作去噪，在 RoboTwin 上以最小模型参数（44.3M）取得 SOTA。


## Problem

长时序（long-horizon）机器人操控任务中存在**观测混淆（observation aliasing）**问题：在多阶段任务的不同阶段，视觉观测可能高度相似，但所需的动作截然不同。例如，在重复敲击任务中每次敲击前的视觉场景几乎一样，但已完成敲击次数不同意味着应执行不同动作。现有基于扩散的模仿学习策略（如 DP3、DP）仅以当前观测或短窗口作为条件，无法区分这些时间混淆状态，导致策略忽略已完成的子目标或回退先前动作。

形式化为 POMDP 框架：观测函数 $O(o_t | s_t)$ 非单射，两条不同历史 $h_t^{[1]}, h_t^{[2]}$ 产生相同观测 $o_t$ 但需要不同专家动作分布。


## Method

### 整体架构

DSSP 由三个核心模块组成：
1. **因果历史编码器**（Causal History Encoder）
2. **层级前缀条件化**（Hierarchical Prefix Conditioning）
3. **SSM 去噪骨干**（SSM Denoising Backbone）

### Causal History Encoding

1. 多模态观测 $o_t$（点云 + 本体感知）经并行视觉/本体感知编码器 $E_{obs}$ 映射为状态表示 $z_t$
2. 因果 SSM $G_\psi$（Mamba，2 层）递归处理状态序列 $z_{1:t}$，生成时间整合表示 $\tilde{z}_{1:t}$
3. 上下文表示 $c_t = \tilde{z}_t$（最终输出 token），即完整历史的压缩记忆
4. Mamba 的选择性状态更新使编码器能过滤冗余观测、保留稀疏的任务相关事件（如物体状态转换、接触变化、子目标完成）

### Dynamics-Aware Auxiliary Loss

为确保 $c_t$ 保留对未来决策有用的历史信息，引入轻量动力学预测器 $g_\phi$：
- 输入：$c_t$ 和执行动作 $a_t$
- 目标：预测下一状态表示 $\hat{z}_{t+1} = g_\phi(c_t, a_t)$
- 损失：余弦相似度 $L_{dyn} = 1 - \cos(g_\phi(c_t, a_t), sg(z_{t+1}))$，sg 为 stop-gradient
- 效果：迫使 $c_t$ 保留与动作相关的历史信息

### Hierarchical Prefix Conditioning

条件序列构造：$C_t = [c_t, z_{t-N+1}, \ldots, z_t]$，将上下文 token + 近期 N 个状态 token 作为前缀拼接到含噪动作序列前。

- $c_t$：捕获长时序任务进度
- $z_{t-N+1:t}$：保留局部几何和本体感知细节
- 前缀通过因果 SSM 从左到右传播，长时序上下文先作用于近期状态再传递到动作 token

### Timestep-Decoupled Denoising

- 扩散步 $\tau$ 仅通过 AdaLN 注入动作 token，前缀条件保持不变
- 效果：任务条件与扩散步调制解耦，前缀在整个去噪过程中提供稳定条件

### 训练目标

$L = L_{diff} + \lambda L_{dyn}$（$\lambda = 0.05$），使用轨迹级批处理保证因果性。

### 关键超参数

- 近期观测窗口 $N = 3$（RoboTwin）/ 2（MetaWorld/Adroit）
- 动作窗口 $H = 8$（RoboTwin）/ 4
- 历史编码器：Mamba 2 层，去噪骨干：Mamba 8 层
- 隐维度 512，SSM 状态维度 64
- 推理步数 10，扩散训练步数 100


## Experiments

### RoboTwin 2.0（50 个双臂任务，按 episode 长度分为 Short/Mid/Long）

| Method | Obs. | Params | Short(18) | Mid(15) | Long(17) | Average |
|--------|------|--------|-----------|---------|----------|---------|
| DP3 | P.C. | 264.4M | 59.83 | 52.53 | 52.76 | 55.24 |
| FlowPolicy | P.C. | 264.4M | 54.89 | 37.40 | 29.59 | 41.04 |
| SeedPolicy | RGB | 147.3M | 43.39 | 36.53 | 47.59 | 42.76 |
| **DSSP** | **P.C.** | **44.3M** | **64.78** | **57.33** | **64.06** | **62.30** |

- DSSP 对 DP3 的平均相对提升 **12.8%**，长时序任务提升最大 **21.4%**
- 模型参数量最小（44.3M vs DP3 264.4M）

### MetaWorld + Adroit（37 个任务）

- MetaWorld Average: DSSP 80.1% vs MP1 78.9% vs DP3 68.7%
- Adroit: DSSP 73.0% vs MP1 75.7%（略低于 MP1）
- 总体平均 DSSP 最好

### 真实世界实验（3 个任务，每任务 20 次）

| Method | Put Bottles | Object Swap | Morse Tapping | Average |
|--------|-------------|-------------|---------------|---------|
| DP3 | 40% | 35% | 15% | 30% |
| **DSSP** | **60%** | **65%** | **85%** | **70%** |

- Morse Tapping 提升最大（15% → 85%），证明历史追踪在计数类任务中至关重要

### 历史编码器分析（6 任务消融子集）

**时间骨干对比**（Table 3）：
- Transformer + 全历史：66.0%，3.61ms，586.2MB
- Mamba + 全历史：**71.33%**，1.97ms，238.5MB
- Mamba 延迟降低 45.4%，内存降低 59.3%

**扰动鲁棒性**（Table 4）：
- σ=0.15 时 DP3 3.17%、DSSP(无历史) 11.33%、DSSP(全历史) **20.83%**
- 证明策略确实依赖历史上下文而非仅依赖近期观测

**组件消融**（Table 5，相对于 DP3 的改进）：
- w/o 历史编码器：+9.65%
- w/o 时间步解耦：+13.64%
- w/o 近期状态：+16.21%
- w/o 动力学损失：+18.46%
- w/ Transformer 去噪：+16.75%
- Full DSSP：**+21.56%**


## Limitations

1. **不解决底层感知/控制失败**：如目标定位不准、抓取/放置不精确，这些仍是真实世界失败来源
2. **真实世界评测有限**：仅 3 个桌面任务，固定摄像头点云设置
3. **未测试可变形物体**：论文自身承认扩展到 DLO 操控是未来方向
4. **未测试动态环境**：当前局限于静态桌面场景
5. **轨迹级训练**：需要完整演示轨迹，可能限制在大规模数据集上的可扩展性


## Key Takeaways

1. **SSM 作为历史编码器的优势**：Mamba 的选择性状态更新天然适合过滤冗余观测、保留稀疏关键事件，且线性时间复杂度使其能高效处理任意长度的历史序列。这比 Transformer 的全局注意力更高效（内存降低 59.3%）。

2. **动力学感知辅助损失是关键**：仅压缩历史不够，必须通过预测下一状态的辅助目标确保上下文保留对未来有预测力的信息。这在 DLO 操控中尤其有价值——绳索的形变状态往往是部分可观测的。

3. **层级条件机制**：将长时序任务进度（context token）与短期局部细节（recent state tokens）分离，通过前缀方式注入，是处理多尺度时间依赖的有效范式。

4. **与 DLO 操控的关联**：论文明确指出未测试可变形物体是局限性之一。DLO 操控中的"观测混淆"问题更严重——绳索在不同操作阶段可能看起来高度相似（如缠绕 vs 已解缠但视觉相似的中间状态），DSSP 的全历史编码方法有直接应用潜力。

5. **小模型 SOTA**：44.3M 参数取得最佳性能，说明历史信息的高效利用比模型规模更重要。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[guan|Guan, Zhiyuan]]
