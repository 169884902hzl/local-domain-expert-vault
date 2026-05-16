---
title: "LaST-R1: Reinforcing action via adaptive physical latent reasoning for VLA models"
tags: [manipulation, imitation, VLM, RL, bimanual]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配合自适应推理长度机制，在 LIBERO 达到 99.8% 成功率，真实双臂场景提升最高 44%。"
authors: "Chen, Hao; Liu, Jiaming; Yan, Zhonghao; Han, Nuowei; Zhang, Renrui et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CJE5U7UT"
---
## 摘要

Vision-Language-Action (VLA) models have increasingly incorporated reasoning mechanisms for complex robotic manipulation（机器人操控）. However, existing approaches share a critical limitation: whether employing explicit linguistic reasoning that suffers from latency and discretization, or utilizing more expressive continuous latent reasoning, they are predominantly confined to static imitation learning（模仿学习） that limits adaptability and generalization. While online reinforcement learning（强化学习） (RL) has been introduced to VLAs to enable trial-and-error exploration, current methods exclusively optimize the vanilla action space, bypassing the underlying physical reasoning process. In this paper, we present \textbf{LaST-R1}, a unified VLA framework that integrates latent Chain-of-Thought (CoT) reasoning over physical dynamics prior to action execution, along with a tailored RL post-training paradigm. Specifically, we propose \textbf{Latent-to-Action Policy Optimization (LAPO)}, a novel RL algorithm that jointly optimizes the latent reasoning process and the action generation. By bridging reasoning and control, LAPO improves the representation of physical world modeling and enhances robustness in interactive environments. Furthermore, an \textbf{adaptive latent CoT mechanism} is introduced to allow the policy to dynamically adjust its reasoning horizon based on environment complexity. Extensive experiments show that LaST-R1 achieves a near-perfect 99.8\% average success rate on the LIBERO benchmark with only one-shot（单样本） supervised warm-up, significantly improving convergence speed and performance over prior state-of-the-art（现有最优方法） methods. In real-world deployments, LAPO post-training yields up to a 44\% improvement over the initial warm-up policy across four complex tasks, including both single-arm and dual-arm（双臂） settings. Finally, LaST-R1 demonstrates strong generalization across simulated and real-world environments.

## 中文简述

提出基于强化学习的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、双臂操控

## 关键贡献

1. **LaST-R1 VLA 模型架构**：统一的 VLA 框架，在动作执行前集成基于物理动态的 latent CoT 推理，latent token 由 DINOv3 全局表征锚定，提供丰富的语义-空间先验。
2. **Latent-to-Action Policy Optimization (LAPO)**：新型 RL 算法，将 latent token 视为隐式决策变量，通过联合 likelihood ratio 同时优化推理空间和动作空间，让环境奖励信号同时塑造推理和动作。
3. **自适应 latent CoT 机制**：策略根据环境复杂度动态调整推理步数（2/4/6/8 token），平衡推理能力和推理效率，训练时采样探索、推理时置信度退出。
## 结构化提取

- Problem: 现有 VLA 的推理-执行耦合不足，RL 优化绕过推理过程，限制了物理理解和泛化
- Method: LaST-R1 (Qwen3-VL-4B + DINOv3 latent anchor + LAPO RL + Adaptive CoT)
- Tasks: LIBERO (Spatial/Object/Goal/Long 仿真), 4 个真实世界操控任务 (单臂+双臂)
- Sensors: 单前视相机 (仿真), 第三人称+双腕部相机 (真实)
- Robot Setup: Franka Panda (仿真), Franka Research 3 (真实), 7-DoF (单臂) / 14-DoF (双臂)
- Metrics: Success Rate (SR), 50 test scenarios per task (仿真), 20 rollouts (真实)
- Limitations: 真实世界任务数量少(4)、自适应候选位置固定、缺乏 DLO 场景验证、双臂协调分析不足
- Evidence Notes: 全文覆盖完整，LIBERO 主实验表格数据完整，真实世界部分具体数字因图片格式部分缺失，消融实验充分（4 组），泛化分析包含仿真 OOD 和真实世界 OOD
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML, 94615 chars)
- Evidence Coverage: high (Introduction, Methodology, Experiments, Ablation, Real-world, Generalization, Conclusion 均已覆盖)
- Confidence: high
- Summary: 提出 LaST-R1 框架，将 DINOv3 锚定的 latent CoT 物理推理与动作生成统一在 VLA 模型中，并设计 LAPO 强化学习算法联合优化推理与动作空间，配合自适应推理长度机制，在 LIBERO 达到 99.8% 成功率，真实双臂场景提升最高 44%。


## Problem

现有 VLA 模型的推理机制存在两大局限：

1. **显式语言推理**（如生成文字 CoT）引入推理延迟和离散化瓶颈，难以捕捉连续高频物理动态。
2. **隐式连续 latent 推理**虽更高效，但现有方法均基于静态模仿学习（IL），受限于专家数据的质量和多样性，导致泛化能力差、累积误差。
3. **已有 VLA-RL 方法**（如 πRL、SimpleVLA-RL）仅在 action space 做优化，完全绕过了物理推理过程，无法让 RL 奖励信号塑造内部推理表征。

核心问题：能否设计一个 RL 框架，专门优化 VLA 中"先推理后执行"的潜在推理-动作耦合过程？


## Method

### 整体架构
- 基座模型：Qwen3-VL-4B（视觉编码器 SigLIP2-Large + LLM backbone）
- 视觉编码器输出 dense visual tokens（fv ∈ R^{Nv×2560}），与语言 tokens 拼接送入 LLM
- LLM 先自回归生成 latent reasoning tokens，再基于 latent 条件并行解码 action tokens
- 动作 tokenizer：parameter-free，连续动作归一化离散化为 token，扩展词汇表
- Value head：4 层 MLP，与 actor 共享 backbone

### Latent Representation（核心设计）
- 使用 DINOv3（SOTA 视觉基础模型）提取 <CLS> token（fd ∈ R^{1×4096}）作为全局图像嵌入
- 通过 top-k（k=2560）通道选择保留最显著视觉分量，对齐 VLA hidden size
- Latent targets 离线预计算，零额外推理开销
- 相比 Global Pooling / Convolution / Q-Former 替代方案效果最优（99.8% vs 96.8%/98.4%/97.2%）

### LAPO 算法
1. **Rollout 收集**：每步 t，策略先生成 latent tokens Z_t（自回归），再基于 latent 条件生成 action tokens C_t（并行解码），<latent_end> token 的 hidden embedding 送入 value head 估计状态价值
2. **联合 likelihood ratio**：
   - 动作序列：离散 token 联合概率 → r_t^a(θ)
   - Latent tokens：用各向同性高斯近似 → r_t^z(θ) = exp(-1/(2σ²) Σ ||z_old - z_θ||²)
3. **LAPO clipped surrogate loss**：L_policy = -E_t[Σ_{m∈{z,a}} min(r_t^m * A_t, clip(r_t^m, 1-ε_min, 1+ε_max) * A_t)]
4. **总损失**：L_total = L_action + λ₁ L_latent + λ₂ L_value
5. **关键机制**：当 A_t > 0 时，优化会拉近当前 latent 与"好推理"流形的距离

### 自适应 Latent CoT
- <latent_end> 从固定终止符变为动态退出信号
- M=4 个候选位置（2/4/6/8 token），推理时置信度阈值 p≥0.99 触发退出
- 训练时用温度参数 β 的 categorical 分布采样推理长度探索
- 额外损失项 L_end 加入总目标：L_total += λ₃ L_end

### 训练流程
1. 大规模预训练（多种机器人操控数据集）
2. 单样本 SFT warm-up（LIBERO 实验中每任务仅 1 条专家轨迹）
3. 在线 RL post-training（LAPO）


## Experiments

### 仿真实验（LIBERO Benchmark）
- 4 个任务集：Spatial / Object / Goal / Long，每集 10 个任务
- Franka Panda，单前视相机，256×256 分辨率
- 每任务 50 个 held-out 测试场景取平均 Success Rate

| 方法 | 范式 | Spatial | Object | Goal | Long | 平均 |
|------|------|---------|--------|------|------|------|
| LaST-R1 (Ours) | RL (1-shot warm-up) | **99.8** | **100.0** | **100.0** | **99.4** | **99.8** |
| πRL (2-camera) | RL | 99.6 | 100.0 | 99.6 | 94.0 | 98.3 |
| SimpleVLA-RL | RL | 98.2 | 98.7 | 98.8 | 91.7 | 96.9 |
| OpenVLA-OFT (full data) | SFT | 97.6 | 98.4 | 97.9 | 94.5 | 97.1 |
| π0.5 (full data) | SFT | 98.8 | 98.2 | 98.0 | 92.4 | 96.9 |

- 学习曲线：LAPO 收敛速度和渐近性能远超 Action-Only + PPO baseline
- LIBERO-Long（长时域任务）优势最显著：99.4% vs 次优 94.0%

### Ablation Studies
1. **Latent 推理效果**：SFT 阶段即提升 51.0%→62.0%（Long: 26.2%→48.6%）；RL 后进一步提升至 99.8%
2. **Latent 表征方法**：DINOv3 (99.8%) > Conv (98.4%) > Q-Former (97.2%) > Global Pooling (96.8%)
3. **Latent 长度**：N_z=1→96.2%, N_z=4→98.0%, N_z=8→98.4%；4→8 收益边际递减
4. **自适应 CoT**：M=4 最佳 (99.8%)，M=8 反而略降 (99.0%)

### 真实世界实验
- 硬件：Franka Research 3
- 任务：4 个（1 单臂 + 3 双臂）— 插入六角块、开袋子拉链、擦花瓶、开瓶盖
- SFT warm-up：每任务 30 条专家演示
- RL post-training：LoRA 微调，第三人称 + 双腕部相机

| 任务 | SFT warm-up | RL 后 | 提升 |
|------|------------|-------|------|
| Insert hexagon (单臂) | 45% | 90% | +45% |
| Open bag zipper (双臂) | - | - | - |
| Wipe vase (双臂) | - | - | - |
| Open bottle cap (双臂) | - | - | - |
| **平均** | **52.5%** | **93.75%** | **+41.25%** |

（部分任务具体数字在原文表格中以图片形式呈现，此处记录可从原文确认的数字）

### 泛化分析
- **仿真 OOD**：Action-Only PPO 出现严重过拟合（Goal/Long OOD 停滞甚至下降），LaST-R1+LAPO 持续提升
- **真实世界 OOD**：RL 后 LaST-R1 在未见物体/背景/光照条件下平均仅下降 8%


## Limitations

1. 真实世界 RL 实验依赖 LoRA 微调（全参微调可能效果更好但成本更高），且仅在 4 个任务上验证，任务多样性有限。
2. 自适应推理长度的候选位置固定为 M=4（2/4/6/8），是否适用于更广泛的任务谱（如超长时域任务）尚未验证。
3. Latent targets 依赖 DINOv3 离线预计算，模型本身的 latent 推理能力是否真正独立于外部锚定仍有疑问。
4. 真实世界实验中具体每任务数字部分以图片形式呈现，部分数值无法从文本直接提取。
5. 论文未讨论 DLO（可变形线性物体）操控场景的适用性。
6. 双臂实验中两个臂是否真正实现协调推理（还是独立的 14-DoF 向量）缺乏深入分析。


## Key Takeaways

1. **Latent CoT + RL 是 VLA 后训练的有效范式**：将推理过程纳入 RL 优化比仅在 action space 做 RL 效果显著更好，这对我们的 DLO 操控研究有直接启发——DLO 操控需要物理动态建模，latent reasoning 可以编码形变预测。
2. **LAPO 的联合优化思想值得关注**：latent token 作为隐式决策变量、高斯近似的 likelihood ratio、clipped surrogate loss 的设计可以迁移到其他需要"推理+执行"的操控场景。
3. **DINOv3 锚定的 latent representation 优于其他方法**：对于需要精细空间推理的 DLO 操控任务，这种全局语义锚定 + top-k 选择的方式值得借鉴。
4. **自适应推理长度**：简单任务少推理、复杂任务多推理的机制可以节省推理开销，对实时 DLO 操控控制频率有实际意义。
5. **单样本 warm-up + RL post-training 范式**：减少对大量专家演示的依赖，对难以收集专家数据的 DLO 操控场景特别有价值。
6. **Sim-to-Real 路径**：论文展示了从 LIBERO 仿真到 Franka 真实世界的迁移路线，泛化仅降 8%，为本领域 Sim-to-Real 提供参考。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]

## 相关研究者

- [[chen-hao|Chen, Hao]]
- [[liu-jiaming|Liu, Jiaming]]
