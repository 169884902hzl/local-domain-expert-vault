---
title: "OmniVLA-RL: A vision-language-action model with spatial understanding and online RL"
tags: [imitation, VLM, RL, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE 后与 GSPO 结合为 Flow-GSPO，在 LIBERO 达到 97.6% 成功率，LIBERO-Plus 上显著优于 PPO/GRPO。"
authors: "Jie, Haoxiang; Yan, Yaoyuan; Wei, Xiangyu; Wang, Kailin; Yan, Hongjie et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "63877G9I"
---
## 摘要

Visual-Language-Action (VLA) models represent a paradigm shift in embodied AI, yet existing frameworks often struggle with imprecise spatial perception, suboptimal multimodal（多模态） fusion, and instability in reinforcement learning（强化学习）. To bridge these gaps, we propose OmniVLA-RL, a novel architecture that leverages a Mix-of-Transformers (MoT) design to synergistically integrate reasoning, spatial, and action experts. Furthermore, we introduce Flow-GSPO, which reformulates flow matching as a Stochastic Differential Equation (SDE) process and integrates it with Group Segmented Policy Optimization (GSPO) to enhance action precision and training robustness. Extensive evaluations on the LIBERO and LIBERO-Plus benchmarks demonstrate that OmniVLA-RL achieves decent overall performance and surpasses mainstream existing methods, effectively overcoming the fundamental limitations of current VLA models.

## 中文简述

提出基于强化学习的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **MoT 三专家架构**：在共享 Transformer 层中集成 Spatial Expert、Reasoning Expert、Action Expert，实现语言指令、视觉语义和 3D 空间特征的深度双向交互
2. **Block-wise Causal Attention**：将空间-语义 token 设为全可见前缀（双向注意力），动作 token 为因果后缀（自回归），前缀不可 attend 到动作块以防止去噪噪声污染场景理解
3. **Flow-GSPO**：通过 Fokker-Planck 方程将 Flow Matching 的确定性 ODE 去噪转化为 SDE 过程，在 action-block 级别使用 GSPO 优化，避免 GRPO 的 token 级偏差
4. **SOTA 性能**：LIBERO 平均 97.6% 成功率；LIBERO-Plus 上 Flow-GSPO 收敛速度和最终性能均显著优于 PPO/GRPO
## 结构化提取

- **Problem**: VLA 模型空间感知不精确、多模态融合次优、RL 训练不稳定
- **Method**: MoT 三专家架构 + Block-wise Causal Attention + Flow-GSPO（SDE 随机流匹配 + GSPO 动作块优化）
- **Tasks**: 机器人操控（tabletop manipulation）：抓取、放置、开抽屉、多阶段组合任务
- **Sensors**: 多视图 RGB 相机（仿真环境）
- **Robot Setup**: 仿真桌面环境（LIBERO / LIBERO-Plus），Franka Panda 类机械臂
- **Metrics**: 成功率（success rate），收敛速度
- **Limitations**: 仅仿真验证无 Sim-to-Real、无世界模型、计算开销未讨论、依赖大规模数据
- **Evidence Notes**: 全文证据充分。LIBERO 有完整数值对比（Table 1）；LIBERO-Plus 仅有训练曲线图（Figure 4）无最终数值表；消融实验有量化数据（Table 2）。所有关键声明均有实验支撑。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文，含所有公式、图表描述和参考文献）
- Evidence Coverage: 完整覆盖 Method、Experiments（LIBERO + LIBERO-Plus）、Ablation、Limitations
- Confidence: high
- Summary: 提出 MoT 三专家 VLA 架构（空间+推理+动作）配合 Block-wise Causal Attention，并将 Flow Matching ODE 改造为 SDE 后与 GSPO 结合为 Flow-GSPO，在 LIBERO 达到 97.6% 成功率，LIBERO-Plus 上显著优于 PPO/GRPO。


## Problem

现有 VLA 模型存在三大瓶颈：
1. **空间感知不精确**：通用 VLM 难以精确输出 3D 位置和物体尺寸，影响机器人操控精度
2. **多模态融合次优**：早期融合（如 Evo-0）和晚期融合（如 FALCON）仅在编码器或动作头层面引入空间信息，未触及核心大模型，无法高效整合语言、视觉、空间和动作
3. **强化学习不稳定**：PPO 架构复杂（需价值模型），GRPO 的 token 级重要性比率设计存在偏差，训练易崩溃


## Method

### 整体架构
OmniVLA-RL 由 VLA 模型 + 在线 RL 模块组成。VLA 采用 Mixture-of-Transformers (MoT) 架构，三个专家共享 Transformer 层。

### Reasoning Expert
- 初始化：PaLiGemma 预训练权重
- 视觉编码器：SigLIP 提取多视图高层语义特征 z_sem ∈ R^{n×d}
- 语言 token z_lang 与视觉 embedding 拼接后送入 decoder-only Transformer
- 建模条件分布 p(z_lang | z_sem)，输出全局上下文

### Spatial Expert
- 使用 VGGT 提取细粒度 3D 结构特征
- 在 Transformer 块中与传递的语义信息做注意力计算
- 附加轻量 Transformer decoder 作为空间辅助头（仅训练时使用，推理时不参与）

### Action Expert
- Action chunking 策略：动作序列通过 linear projector 映射到 Transformer 潜空间
- 使用 Conditional Flow Matching (CFM) 建模动作分布 p(a | z_spatial, z_sem, z_lang)

### Block-wise Causal Attention
- **前缀区**（空间 + 语义 token）：全双向注意力，促进跨模态对齐
- **后缀区**（动作 token）：可 attend 到完整前缀，内部遵循因果（自回归）约束
- **隔离**：前缀 token 不可 attend 到动作 token，防止扩散采样噪声污染场景理解

### Flow-GSPO（核心 RL 创新）

**Stochastic Flow Matching**：
- 原始 Flow Matching 是确定性 ODE 过程：dx_t/dt = v_θ(x_t, t)
- 通过 Fokker-Planck 方程转化为 SDE，注入随机噪声实现可微随机探索
- 离散化使用 Euler-Maruyama 方法
- 转移概率为各向同性高斯分布 N(μ_τ, Σ_τ)

**GSPO on Stochastic Flow Matching**：
- 以 action block（整段动作序列 × 去噪步数）为优化单元，而非 token
- 重要性比率基于 action block 级似然
- 优势估计使用组内奖励归一化
- 加入 KL 散度约束防止策略剧变

**三阶段训练**：
1. **Stage I - 空间预训练**：在大规模 3D 数据集上联合训练 Reasoning + Spatial Expert（Action Expert 冻结），空间损失含点云重建 + 相机参数 + 表面法线
2. **Stage II - 动作预训练**：解冻 Action Expert，在 DROID 数据集上用 CFM 损失端到端训练
3. **Stage III - 在线 RL**：Flow-GSPO 微调整个模型，G=8, ε=0.2, β=0.01, σ_max=0.1, K=10 去噪步, H=16 动作长度


## Experiments

### LIBERO Benchmark（Table 1）
| 任务套件 | OmniVLA-RL | π0.5 | π0 | OpenVLA |
|---------|-----------|------|-----|---------|
| Spatial | **Top** | -0.4% | 显著低 | 显著低 |
| Object | **Top** | - | - | - |
| Goal | **Top** | -0.5% | 显著低 | 显著低 |
| Long | 93.5% (**Top**) | -1.1% | 显著低 | 显著低 |
| **Average** | **97.6%** | - | -21.1% vs Ours | - |

注：论文中 Table 1 未给出所有 baseline 的精确数值，仅提供差值关系。

### LIBERO-Plus Benchmark（Figure 4）
- Flow-GSPO 在前 50 步即超过 70% 成功率，远快于 PPO 和 GRPO
- PPO 在约 80 步附近出现明显性能回退
- Flow-GSPO 在 100 步后保持 80% 以上成功率
- Flow-GSPO 比 GRPO 高约 +14.6%

### Ablation Study（Table 2, LIBERO-Plus）
| 配置 | 成功率 | 变化 |
|------|-------|------|
| OmniVLA-RL (SFT only) | 41.2% | baseline |
| + Flow-GSPO | 80.3% | **+39.1%** |
| + PPO (替代 Flow-GSPO) | 78.7% | +1.6% vs PPO |
| + GRPO (替代 Flow-GSPO) | 65.7% | +14.6% vs GRPO |
| w/o Spatial Expert | 32.9% | **-8.3%**（最大架构消融退化） |

### RL 训练超参数
- G=8（组大小）, ε=0.2（裁剪系数）, β=0.01（KL 权重）
- σ_max=0.1, K=10 去噪步, H=16 动作长度
- AdamW, lr=1e-5, weight decay=0.01, 200 RL steps
- rollout buffer 每 10 步刷新

### 缺失的证据
- LIBERO-Plus 的精确数值结果表（Figure 4 为训练曲线图，未给出最终数值表格）
- Sim-to-Real 实验结果（论文明确指出未进行）
- 真实物理平台验证
- 各 LIBERO 子任务套件的逐任务明细


## Limitations

1. **仅仿真验证**：未在物理硬件上测试，Sim-to-Real gap 未探索
2. **缺少世界模型**：架构没有专门的世界模型用于长时域推理和环境转移预测
3. **计算开销**：MoT 三专家 + SDE 采样的计算成本未讨论
4. **数据依赖**：Stage II 使用完整 DROID 数据集（大规模机器人数据），数据需求量大


## Key Takeaways

1. **MoT 架构思路可迁移**：将空间感知专家和动作专家解耦的设计，对需要精细空间感知的 DLO 操控任务有参考价值——DLO 的形变状态同样需要精确 3D 感知
2. **Flow-GSPO 为 VLA + RL 提供了新范式**：将 Flow Matching 的 ODE 转 SDE 以实现随机探索，解决了扩散/流模型策略梯度中的随机性需求问题
3. **Action-block 级优化优于 token 级**：对于连续动作轨迹（如 DLO 的抓取点序列），以块为单位优化比逐 token 优化更稳定
4. **Block-wise Causal Attention 的前缀/后缀设计**：场景理解前缀和动作生成后缀的隔离设计，可防止去噪噪声反向污染感知——这对需要高精度感知的 DLO 任务尤其重要
5. **三阶段渐进训练范式**：空间预训练 → 动作预训练 → 在线 RL 的渐进式训练策略，对大规模 VLA 训练有工程参考价值

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[jie|Jie, Haoxiang]]
