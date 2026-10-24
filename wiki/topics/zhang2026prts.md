---
title: "PRTS: A primitive reasoning and tasking system via contrastive representations"
tags: [manipulation, VLM, RL, robot-learning, planning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂平台均达到 SOTA，尤其擅长长时序任务和零样本新指令泛化。"
authors: "Zhang, Yang; Zhao, Jiangyuan; Fan, Chenyou; Yan, Fangzheng; Li, Tian et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "3GH8S3RM"
---
## 摘要

Vision-Language-Action (VLA) models advance robotic control via strong visual-linguistic priors. However, existing VLAs predominantly frame pretraining（预训练） as supervised behavior cloning, overlooking the fundamental nature of robot learning as a goal-reaching process that requires understanding temporal task progress. We present \textbf{PRTS} (\textbf{P}rimitive \textbf{R}easoning and \textbf{T}asking \textbf{S}ystem), a VLA foundation model that reformulates pretraining（预训练） through Goal-Conditioned Reinforcement Learning（强化学习）. By treating language instructions as goals and employing contrastive reinforcement learning（强化学习）, PRTS learns a unified embedding space where the inner product of state-action and goal embeddings approximates the log-discounted goal occupancy, the probability of reaching the language-specified goal from the current state-action, quantitatively assessing physical feasibility beyond static semantic matching. PRTS draws this dense goal-reachability supervision directly from offline trajectories without reward（奖励） annotations, and folds it into the VLM backbone via a role-aware causal mask, incurring negligible overhead over vanilla behavior cloning. This paradigm endows the high-level reasoning system with intrinsic goal reachability awareness, bridging semantic reasoning and temporal task progress, and further benefits goal-conditioned action prediction. Pretrained on 167B tokens of diverse manipulation（操控） and embodied-reasoning data, PRTS reaches state-of-the-art（现有最优方法） performance on LIBERO, LIBERO-Pro, LIBERO-Plus, SimplerEnv, and a real-world suite of 14 complex tasks, with particularly substantial gains on long-horizon（长时序）, contact-rich（接触丰富）, and zero-shot（零样本） novel-instruction settings, confirming that injecting goal-reachability awareness significantly improves both execution success and long-horizon（长时序） planning of general-purpose robotic foundation policies.

## 中文简述

提出基于强化学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、机器人学习、运动规划

## 关键贡献

1. **语言条件对比 RL（Language-Conditioned CRL）表征学习**：首次将 Contrastive RL 扩展到 VLA 预训练阶段，将语言指令视为目标，通过双向 InfoNCE 损失学习 state-action 和 goal 的联合嵌入空间，无需奖励标注
2. **时序加权方案替代几何采样**：标准 CRL 从未来状态几何采样构建正对，但语言目标在轨迹内是共享的。PRTS 将几何采样转化为时序加权（γ^(T-t)），从离线轨迹直接获得稠密目标可达性监督
3. **单次前向传播设计**：通过 role-aware causal mask + 自定义 CuTe-FlashAttention kernel，将 CRL token 块和 BC token 在同一前向传播中处理，额外开销接近零（per-layer attention 仅 1.18x）
4. **大规模预训练**：在 167B token 的多样化操控与推理数据上预训练，64 H100 GPU 训练一周
5. **全面评估**：在 LIBERO、LIBERO-Plus、LIBERO-Pro、SimplerEnv + 真实双臂/单臂 14 项任务上全面达到或超越 SOTA
## 结构化提取

- **Problem**: VLA 预训练阶段仅用行为克隆，缺乏目标可达性感知能力，导致长时序任务、零样本新指令和分布偏移下的性能不足
- **Method**: 语言条件对比 RL（Language-Conditioned CRL）+ 双向 InfoNCE 损失 + 时序加权 + role-aware causal mask + flow-matching action expert
- **Tasks**: 桌面操控（pick-place-stack, 齿轮装配, 花束排列, 双臂协作等），涵盖单臂和双臂
- **Sensors**: 多视角 RGB 相机（ego-centric + wrist×2）+ 本体感知（关节角度等）
- **Robot Setup**: RealMan 双臂平台（14-DoF bimanual, 3 cameras）; Flexiv 单臂平台（3 cameras）; LIBERO/SimplerEnv 仿真
- **Metrics**: Task Success Rate (SR); 20 trials per task (real-world)
- **Limitations**: 未覆盖 DLO/线缆操控；未验证大模型缩放性；新指令精细放置成功率有限；预训练数据偏桌面
- **Evidence Notes**:

  - LIBERO: PRTS 98.4% avg (bs=32) vs ABot-M0 97.9% (matched budget) vs π0.5 96.9% (8x budget)
  - LIBERO-Plus zero-shot: 81.4% avg, 显著优势在 Robot/Background/Noise
  - LIBERO-Pro zero-shot Task axis: 31.5% vs π0.5 0.8%（零样本新指令跟随是核心优势）
  - SimplerEnv: 77.1% vs GR00T-N1.5 61.9%
  - RealMan 双臂: 95.9% vs π0.5 85.5%
  - Flexiv 单臂: 90.0% vs π0.5 75.0%
  - CRL 消融: Task +11.4%, Position +10.5%, Robot +16.3%
  - 真实世界 Task 泛化: 73.8% vs π0.5 35.0% vs π0 13.8%
  - 预训练额外开销: per-layer attention 1.18x FA3 baseline
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML, 120K+ chars)
- Evidence Coverage: complete (all sections: Introduction, Method, Data, Experiments, Ablation, Conclusion)
- Confidence: high
- Summary: 通过将语言条件对比强化学习（CRL）融入 VLA 预训练，PRTS 使 VLM backbone 学会目标可达性感知的表征，在 LIBERO、SimplerEnv 和真实双臂平台均达到 SOTA，尤其擅长长时序任务和零样本新指令泛化。


## Problem

现有 VLA（Vision-Language-Action）模型（如 π0、π0.5、OpenVLA）在预训练阶段几乎完全依赖行为克隆（behavior cloning），将其视为监督学习问题。这忽略了机器人轨迹本质上是**目标达成过程**的核心特征：模型需要理解"当前状态-动作对有多大概率最终实现语言指定的目标"——即**目标可达性（goal reachability）**。

具体问题：
1. VLM 擅长编码静态语义相似性，但缺乏目标可达性的定量估计能力
2. 现有 VLA 的预训练仅关注静态理解和即时动作预测，未显式注入时序目标可达性感知
3. 先前尝试（如 π0.6*、VLAC）依赖显式奖励标注、单独训练的价值网络或手工进度标签，成本高昂且无法直接编码目标达成的底层结构


## Method

### 核心思想

将 VLA 预训练重新定义为**目标条件强化学习**问题。通过对比 RL（CRL），学习一个统一嵌入空间，其中 state-action 嵌入 ϕ(s,a) 和 goal 嵌入 ψ(l) 的内积近似于 log-discounted goal occupancy measure（到达目标的折扣概率的对数）。

### 架构（PRTS Architecture）

- **Backbone**: Qwen3-VL-4B-Instruct
- **输入序列**: 多视角视觉 token（Qwen ViT 编码） + 文本化本体感知 token + 语言指令 token + FAST tokenized AR 动作 token + 两个辅助块 [CRL_action] 和 [CRL_goal]
- **[CRL_action] 块**: 重复动作 token + 可学习 token → 提取 ϕ(s, a)
- **[CRL_goal] 块**: 重复指令 token + 可学习 token → 提取 ψ(l)
- **Role-Aware Causal Mask**: 五种角色（vision/state, instruction, AR action, CRL_action, CRL_goal）间的结构化注意力约束：
  - AR action 使用标准因果注意力
  - CRL_action 仅关注视觉/本体感知 token 和自身，不接触语言
  - CRL_goal 仅在自身块内自注意力，完全隔离
- **实现**: 基于 FlashAttention4 的自定义 CuTe kernel，block-level 稀疏化，吞吐接近纯 BC

### 语言条件对比 RL（核心方法贡献）

**多正例问题**：同一语言目标在 mini-batch 中对应多个 state-action 对，打破标准 CRL 的单正例假设。

**双向对比目标**：

1. **(s,a) → l 方向**：任务级判别。每个 (s,a) 有唯一正例目标 l，用 γ^(T-t) 加权。推动 state-action 与其语言目标对齐。
2. **l → (s,a) 方向**：时序进展编码。语言锚点有多个正例，用时序权重 q_ij = γ^(Tj-tj) / Σγ^(Tj'-tj') 做软标签。强制内积满足 ψᵀϕ = (T-t)logγ + C，编码到目标完成的时序距离。

**理论保证（Theorem 1）**：最优表征满足 ψ*(l)ᵀϕ*(s,a) = log Q^π_l(s,a) + C(l)，即内积直接估计 log-discounted goal occupancy measure。

### 两阶段训练

**Pre-training**：联合优化 BC + RobotQA + Subtask + λ_crl(ℒ^{sa→l} + ℒ^{l→sa})。λ_crl=1.0, γ=0.995。~22K in-batch negatives。64x H100, batch=256, ~220K steps, 约 1 周。

**Post-training**：附加随机初始化的 DiT-based flow-matching action expert（675M params, 5 denoising steps），仅优化 ℒ_FM。

### 训练数据

- **Action-Labeled Data**: 404M samples，涵盖 Open X-Embodiment、Droid、RoboMind 等
- **Visual-Reasoning Data**: 空间推理、affordance 感知、任务规划等补充监督
- 总计 167B tokens


## Experiments

### 仿真实验

**LIBERO（Table 2）**：
- PRTS: 98.4% avg SR（bs=32, 30K steps）
- ABot-M0: 97.9%（同等预算）/ 98.6%（bs=64, 40K steps）
- π0.5: 96.9%（bs=256, 30K steps，8x 更大 batch）
- PRTS 在 Long suite 上达 96.6%，仅用 1/8 π0.5 的 post-training 算力

**LIBERO-Plus（Table 3，零样本评估）**：
- PRTS: 81.4% avg SR（零样本，未在扰动数据上训练）
- π0.5: 80.7%（8x 更大 batch）
- 显著优势在 Robot (+14.4), Background (+15.3), Noise (+9.0)

**LIBERO-Pro（Table 4，零样本评估）**：
- PRTS: 58.8% avg SR
- π0.5: 53.3%
- Task 轴（零样本新指令）：PRTS 31.5% vs π0.5 0.8%（+30.7）
- Position 轴：PRTS 24.3% vs π0.5 20.8%

**SimplerEnv WidowX（Table 5）**：
- PRTS: 77.1% avg SR
- GR00T-N1.5: 61.9%（同等计算预算）
- Put Eggplant in Yellow Basket: 100%

### 真实世界实验

**RealMan 双臂平台（11 tasks，多任务共享 checkpoint）**：
- PRTS: 95.9% avg SR
- π0.5: 85.5%
- π0: 67.3%
- Office Long Term: PRTS 95% vs π0.5 40%

**Flexiv 单臂平台（3 tasks，per-task fine-tuning）**：
- PRTS: 90.0% avg SR
- π0.5: 75.0%
- Flower Arrangement（长时序）: PRTS 70% vs π0.5 35%

### 消融实验（Table 6-7）

CRL 消融（PRTS w/ CRL vs w/o CRL）：
- LIBERO: +0.6%（97.8% → 98.4%）
- LIBERO-Plus: +4.9%（76.5% → 81.4%），Robot 轴 +16.3%
- LIBERO-Pro: +5.0%（53.8% → 58.8%），Position +10.5%，Task +11.4%
- Suite 级别分解：Object-Position 从 4.8% → 36.0%（+31.2%），Spatial-Task 从 34.4% → 62.2%（+27.8%）

### 零样本真实世界泛化（Section 6.4）

四轴泛化测试：
- Illumination / Spatial / Object：PRTS 在大部分任务保持 ≥80%
- **Task（新指令组合）**：PRTS 73.8% vs π0.5 35.0% vs π0 13.8%
  - Paper Rubbish: 80%（π0.5 大部分失败）
  - Place Block: 55%
  - Pick Shoes: 85%
  - Stack Cups: 75%

### 人类干预恢复（Section 6.5）

在执行过程中人为干扰物体：
- π0: 忽略变化，继续回放固定任务阶段，所有干扰均导致失败
- π0.5: 简单中断可恢复，但已完成子目标的恢复失败
- PRTS: 持续重新选择动作，基于当前可达路径追踪语言目标

### CRL Value 可视化（Section 6.6）

在 RealMan 持出分布轨迹上（零样本，无 post-training）：
- 正确指令的 CRL 值曲线随任务进度上升，在关键里程碑处形成局部峰值
- 错误指令的值始终保持在 0.04-0.20 低区间，从不越过正确指令曲线
- 确认 CRL 捕获目标可达结构而非仅反应视觉变化

### 预训练效率（Section 6.7）

- CuTe kernel 的 per-layer attention 时间仅为 FA3 基准的 1.18x
- 端到端吞吐在 64 GPU 上保持 85.1% 扩展效率


## Limitations

1. **指令级重组仍是最大挑战**：Task 轴泛化虽有显著提升，但绝对成功率（31.5%-73.8%）表明仍有很大空间
2. **Object 轴 LIBERO-Pro 性能略有下降**（84.5% → 82.3%），说明 CRL 偶尔对特定物体外观特征的拟合不如纯 BC
3. **未评估 DLO 操控场景**：所有实验均为刚性物体或简单可变形物体（纸张、鞋等），未涉及线缆、绳索等连续可变形物体
4. **预训练数据规模虽大但偏重桌面操控**，未涵盖移动操控、野外场景等
5. **仅用 4B 参数 backbone**，未验证在更大 VLM 上的缩放性
6. **零样本评估中 Place Block 新指令仅 55%**，说明精细放置任务在新指令下的空间推理仍有不足


## Key Takeaways

1. **CRL 作为 VLA 预训练范式的有效性**：首次证明 reward-free 的对比 RL 可以融入 VLA 预训练并显著提升下游性能，尤其在分布外泛化上。这为 VLA 预训练提供了新的理论框架。
2. **目标可达性感知 vs 静态语义匹配**：关键区别在于 PRTS 不仅知道"做什么"（语义），还知道"当前状态有多大概率做到"（可达性）。这对长时序任务和干预恢复至关重要。
3. **对 DLO 操控的潜在价值**：虽然论文未涉及 DLO，但 goal-reachability-aware representation 对 DLO 操控中的长时序规划和中间状态恢复有直接借鉴意义。DLO 的形变过程也可以视为一个目标达成过程。
4. **工程实践的启示**：role-aware causal mask + CuTe kernel 的设计使得 CRL 预训练的额外开销接近零，这对后续工作将 RL 信号融入大模型预训练提供了工程参考。
5. **与 π0.5 的对比意义**：PRTS 用 1/8 的 post-training 算力达到同等或更优性能，说明预训练表征质量比下游微调算力更重要。
6. **时序加权的理论优雅性**：将几何采样转化为时序权重 γ^(T-t)，巧妙解决了语言目标无法几何采样的难题，理论证明等价于标准 CRL 的 discounted occupancy estimation。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhang-yang|Zhang, Yang]]
