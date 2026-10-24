---
title: "AVA-VLA: Improving vision-language-action models with active visual attention"
tags: [manipulation, imitation, VLM, robot-learning, bimanual]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉 token，在 LIBERO、CALVIN 和双臂真实任务上达到 SOTA。"
authors: "Xiao, Lei; Li, Jifeng; Gao, Juntao; Ye, Feiyang; Jin, Yan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "2QCE2HRH"
---
## 摘要

Vision-Language-Action (VLA) models have shown remarkable progress in embodied tasks recently, but most methods process visual observations independently at each timestep. This history-agnostic design treats robot manipulation（机器人操控） as a Markov Decision Process, even though real-world robotic control is inherently partially observable and requires reasoning over past interactions. To address this mismatch, we reformulate VLA policy learning from a Partially Observable Markov Decision Process perspective and propose AVA-VLA, a framework that conditions action generation on a recurrent state that serves as a neural approximation to the agent's belief over task history. Built on this recurrent state, we introduce Active Visual Attention (AVA), which dynamically reweights visual tokens in the current observation to focus on regions most relevant given both the instruction and execution history. Extensive experiments show that AVA-VLA achieves state-of-the-art（现有最优方法） performance on standard robotic benchmarks, including LIBERO and CALVIN, and transfers effectively to real-world dual-arm manipulation（双臂操控） tasks. These results demonstrate the effectiveness of temporally grounded active visual processing for improving VLA performance in robotic sequential decision-making. The project page is available at https://liauto-dsr.github.io/AVA-VLA-Page.

## 中文简述

提出基于视觉-语言的双臂方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习、双臂操控

## 关键贡献

1. **首次从 POMDP 视角重构 VLA 策略学习**：将 VLA 从 MDP 公式化为 POMDP，引入循环状态（recurrent state）作为 belief state 的神经网络近似，使策略条件化于历史上下文
2. **提出 Active Visual Attention（AVA）模块**：利用循环状态计算视觉 token 的软重要性权重，动态调制 LLM backbone 所有层的注意力矩阵，实现基于历史信息的主动视觉处理
3. **全面实验验证**：在 LIBERO（98.0%/98.2%）、CALVIN（avg len 4.65）、Mobile ALOHA 真实双臂任务上达到 SOTA，并展示视觉 token 剪枝的鲁棒性
## 结构化提取

- Problem: VLA 模型的 history-agnostic 设计（MDP 假设）无法处理部分可观测的机器人操控任务，导致视觉注意力每步从零计算，无法利用历史上下文
- Method: AVA-VLA — POMDP 视角下的 VLA 框架，引入循环状态（recurrent state）作为 belief 近似 + Active Visual Attention 模块动态重加权视觉 token；基于 OpenVLA-OFT 构建
- Tasks: LIBERO（4 suites, 100 tasks）、CALVIN ABC→D（34 tasks, long-horizon）、Mobile ALOHA 真实双臂（4 tasks: Pick&Place, Sequenced Instruction, Flexible Object Folding, Dexterous Action）
- Sensors: RGB 图像（LIBERO/CALVIN）、RGBD（CALVIN）、本体感觉状态
- Robot Setup: Franka Panda 单臂（模拟）、Cobot Magic 双臂（真实 Mobile ALOHA）
- Metrics: Success Rate（SR%）、Average Length（CALVIN）
- Limitations: Truncated BPTT（T=4）限制长程依赖学习；模拟仅单臂；真实评估规模小；计算开销未报告；循环状态长程遗忘未分析
- Evidence Notes:

  - LIBERO: 98.0% avg SR（one policy for all），LIBERO-Long 97.6% vs OpenVLA-OFT 95.3%（+2.3%）
  - CALVIN: avg len 4.65，全任务数领先次优 FLOWER 4.53
  - Real-world: 4 个双臂任务平均最优，Flexible Object Folding 含可变形物体折叠
  - Ablation: AVA module 和 state-based init 互补；跨 3 种 backbone 均有效
  - Token pruning: 70% 剪枝几乎无损（97.3% vs 98.0%），90% 剪枝仍 93.9%
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取完整正文，含所有公式、表格和图片描述）
- Evidence Coverage: 完整覆盖 Introduction、Related Work、Method、Experiments（含 LIBERO/CALVIN/Real-world）、Ablation、Conclusion
- Confidence: high
- Summary: 基于 POMDP 视角提出 AVA-VLA 框架，引入循环状态作为 belief 的神经网络近似，并设计 Active Visual Attention 模块动态重加权视觉 token，在 LIBERO、CALVIN 和双臂真实任务上达到 SOTA。


## Problem

现有 VLA 模型（如 OpenVLA、RT-2 等）在每个时间步独立处理当前视觉观测，隐式假设操控任务为 MDP。但真实机器人控制本质上是部分可观测的（POMDP），当前视觉帧只是环境状态的部分观测。这种 history-agnostic 设计导致：
1. 视觉注意力仅依赖静态语言指令，每步从零重新计算
2. 无法根据历史执行上下文抑制时间上冗余的视觉信息
3. 无法聚焦于因过去动作而变得重要的视觉区域
4. 长程任务（如 LIBERO-Long）性能显著受限


## Method

### 整体框架
基于 OpenVLA-OFT（LLaMA2-7B backbone + DINOv2/SigLIP 双分支视觉编码器）构建。

### 核心组件

**1. 循环状态（Recurrent State）**
- 从上一时间步最后一层的隐藏状态提取：r^{t-1} = B(h_M^{t-1})
- B 是 MLP 模块，将隐藏状态投影为循环状态
- 作为 POMDP 中 belief state 的神经网络近似
- 同时用于初始化 action placeholder embedding（替代原来的零向量）

**2. Active Visual Attention（AVA）模块**
- 模态特定 MLP 编码视觉特征 z_I^t 和语言特征 z_S^t
- FiLM 调制：用语言特征条件化视觉特征
- Cross-Attention：视觉 token 为 Query，循环状态为 Key/Value
- Self-Attention 处理 cross-attention 输出
- FFN + Linear → Softmax → 生成软权重 ω^t ∈ R^{L_I}（每个视觉 token 一个重要性分数）
- γ 向量控制增强/抑制的标量分数
- 软权重应用于 LLM backbone 所有层的注意力矩阵（构造软注意力掩码 U^t）

**3. 训练策略**
- Truncated BPTT（T=4 步展开），平衡计算开销与时间依赖学习
- MAE 损失 + L2 正则化约束软权重均值（防止注意力过于分散）
- 初始时间步循环状态初始化为零向量

**4. 推理**
- 完全循环式推理，episode 开始时零初始化
- 每步执行前向传播，同时预测动作和提取新循环状态


## Experiments

### LIBERO 基准
| 设置 | AVA-VLA | OpenVLA-OFT | 提升 |
|------|---------|-------------|------|
| One policy for all 4 suites | 98.0% | 96.8% | +1.2% |
| One policy per suite | 98.2% | 97.1% | +1.1% |
| LIBERO-Long ( hardest ) | 97.6% | 95.3% | +2.3% |

- 在 LIBERO-Long 上尤其突出，验证了历史上下文对长程任务的重要性

### CALVIN ABC→D 基准
- AVA-VLA: avg len 4.65（SOTA）
- 次优 FLOWER: avg len 4.53
- 每个连续任务数均领先

### 真实双臂任务（Mobile ALOHA）
- 4 个任务：Pick & Place、Sequenced Instruction、Flexible Object Folding（可变形物体）、Dexterous Action
- 每任务 24-30 次试验，30-450 条演示数据
- 平均性能超越 UniVLA 和 OpenVLA-OFT

### Ablation 研究
- **Backbone 通用性**：在 OpenVLA-7B（+1.7%）、LLaMA2-7B（+2.6%）、Qwen2.5-0.5B（+1.4%）上均有提升
- **模块互补性**：State-based init 和 AVA module 各自提升（97.5%），组合最佳（98.0%）
- **Token 剪枝鲁棒性**：50-70% 剪枝比几乎无损，90% 剪枝仍优于多数 baseline


## Limitations

1. **训练时的截断 BPTT**（T=4）限制了真正长程依赖的学习能力，循环状态可能无法充分捕获超过 4 步的时间信息
2. **模拟基准仅单臂**：LIBERO 和 CALVIN 均为单臂 Franka 机器人，双臂场景仅在真实世界验证了少量任务
3. **真实世界评估规模有限**：仅 4 个任务，每任务 24-30 次试验，统计显著性有待加强
4. **依赖 OpenVLA-OFT 架构**：方法设计紧密耦合于 parallel decoding 架构，对 AR 解码的 VLA 适配性未充分探讨
5. **未讨论计算开销**：AVA 模块引入的额外计算量（cross-attention、self-attention、FFN）没有定量报告
6. **循环状态遗忘问题**：长 episode 中循环状态可能丢失早期关键信息，论文未分析


## Key Takeaways

1. **POMDP 视角对 DLO 操控的价值**：DLO 操控中可变形状态随时间演化，POMDP 公式化比 MDP 更合理；循环状态可以编码 DLO 的变形历史
2. **主动视觉注意力**：AVA 模块的软权重机制可以用于聚焦 DLO 的关键区域（如抓取点、弯曲处），而非背景
3. **FiLM 调制技术**：用语言特征条件化视觉特征的方式简洁有效，可用于将任务指令映射到 DLO 操控的视觉关注模式
4. **Sim-to-Real 可行性**：在双臂真实机器人上的成功验证了方法对真实世界的迁移能力，对 DLO 双臂操控有直接参考价值
5. **Token 剪枝的附带能力**：AVA 的权重可用于高效推理，对实时 DLO 操控有实际意义

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[xiao-lei|Xiao, Lei]]
