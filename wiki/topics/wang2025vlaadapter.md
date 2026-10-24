---
title: "VLA-adapter: An effective paradigm for tiny-scale vision-language-action model"
tags: [imitation, VLM]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 VLA-Adapter，系统分析 VLA 模型中 VL→A 桥接范式的有效性。发现中间层 Raw 特征优于深层（语义偏差）、深层 ActionQuery 最优、多层特征优于单层。提出 Bridge Attention（双交叉注意力+自注意力+可学习注入比例），用 0.5B 骨干在 LIBERO 达 97.3%（接近 OpenVLA-OFT 97.1%/7B），推理 219.2Hz，单卡 8 小时训练。冻结骨干仍达 86.4%。"
authors: "Wang, Yihao; Ding, Pengxiang; Li, Lingxiao; Cui, Can; Ge, Zirui et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "9VYG49GG"
---
## 摘要

Vision-Language-Action (VLA) models typically bridge the gap between perceptual and action spaces by pre-training a large-scale Vision-Language Model（视觉-语言模型） (VLM) on robotic data. While this approach greatly enhances performance, it also incurs significant training costs. In this paper, we investigate how to effectively bridge vision-language (VL) representations to action (A). We introduce VLA-Adapter, a novel paradigm designed to reduce the reliance of VLA models on large-scale VLMs and extensive pre-training. To this end, we first systematically analyze the effectiveness of various VL conditions and present key findings on which conditions are essential for bridging perception and action spaces. Based on these insights, we propose a lightweight Policy module with Bridge Attention, which autonomously injects the optimal condition into the action space. In this way, our method achieves high performance using only a 0.5B-parameter backbone, without any robotic data pre-training. Extensive experiments on both simulated and real-world robotic benchmarks demonstrate that VLA-Adapter not only achieves state-of-the-art（现有最优方法） level performance, but also offers the fast inference speed reported to date. Furthermore, thanks to the proposed advanced bridging paradigm, VLA-Adapter enables the training of a powerful VLA model in just 8 hours on a single consumer-grade GPU, greatly lowering the barrier to deploying the VLA model. Project page: https://vla-adapter.github.io/.

## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 模仿学习、视觉-语言模型

## 关键贡献

1. **首次系统性桥接范式分析**：在统一框架下比较 4 种 VL→A 桥接方式（单层 Raw、单层 ActionQuery、全层 Raw、全层 ActionQuery），给出 3 个关键发现：中间层 Raw 优于深层、深层 ActionQuery 最优、多层优于单层。
2. **Bridge Attention 机制**：双交叉注意力（CtR + CAQt）+ 自注意力 + 可学习注入比例 g（tanh 初始化为 0），自主选择最优条件注入策略。Policy 仅 97M 参数。
3. **极致效率**：0.5B 骨干（Qwen2.5）无需机器人数据预训练，LIBERO 97.3%（超越 π₀/GR00T N1/SmolVLA），推理 219.2Hz（3× OpenVLA-OFT），单卡 8 小时训练。
4. **冻结骨干有效**：VLM 冻结时仍达 86.4%（LIBERO-Long），远超 SmolVLA 77.0% 和 OpenVLA-OFT 0.0%。
## 结构化提取

- **Problem**: VLA 模型依赖大规模 VLM 和机器人数据预训练，训练成本高、推理慢。VL→A 桥接范式缺乏系统性比较，不清楚哪种条件对动作生成最关键。
- **Method**: VLA-Adapter：系统分析 4 种桥接范式，提出 Bridge Attention（双交叉注意力 CtR+CAQt + 自注意力 + 可学习注入比例）。0.5B Qwen2.5 骨干 + 97M Policy，L1 损失端到端训练，无需机器人数据预训练。
- **Tasks**: LIBERO（Spatial/Object/Goal/Long 四套件，50 trials/subtask）；CALVIN ABC→D（1000 任务序列）；真实 Pick/Move/Stack/Long 任务。
- **Sensors**: 仿真 RGB 图像 + 夹爪图像 + 本体感觉；真实 Logitech C920e 第三人称 + RealSense D405 夹爪相机。
- **Robot Setup**: 仿真 LIBERO（Franka Panda，10 demo/task）；仿真 CALVIN（Franka Panda）；真实 Synria Alicia-D 6-DOF + 1-DOF 夹爪。
- **Metrics**: Success Rate（50 trials/subtask），Avg. len（CALVIN 连续完成子任务数），Throughput（Hz），Latency（s），VRAM（GB）。
- **Limitations**: 真实泛化有限（0.5B 无大规模预训练）；真实世界仅 4 类 × 10 次试验；条件质量依赖 VLM；训练流程简单（仅 L1）；大骨干提升有限；ActionQuery 数量需调优。
- **Evidence Notes**: 桥接范式分析在 LIBERO-Long 上有系统消融（Fig. 4, Tab. 1, 7-8）。LIBERO 对比 22 种基线（Tab. 5），CALVIN 对比 14 种基线（Tab. 6），结果可靠。冻结骨干实验（Tab. 3）揭示关键洞见。效率对比（Tab. 4）含延迟和显存。真实世界仅 Fig. 7 柱状图（10 trials/task），无详细失败分析。VLA-Adapter-Pro 在附录补充。整体证据强度：仿真部分强，真实部分中。
## 本地引用关系

- [[dai2024racer]]
- [[jeong2026your]]
- [[ma2025running]]
## 证据元数据

- **Zotero Key**: 9VYG49GG
- **Citekey**: wang2025vlaadapter
- **Authors**: Wang Yihao, Ding Pengxiang, Li Lingxiao, Cui Can, Ge Zirui, Tong Xinyang, Song Wenxuan, Zhao Han, Zhao Wei, Hou Pengxu, Huang Siteng, Tang Yifan, Wang Wenhui, Zhang Ru, Liu Jianyi, Wang Donglin
- **Affiliation**: BUPT + Westlake University + Zhejiang University + OpenHelix Team + HKUST(Guangzhou)
- **Venue**: arXiv preprint, 2025-09
- **Paper Type**: Methods paper (VLA bridging paradigm with systematic analysis)
- **Fulltext Quality**: Complete, 11 pages main text + appendix, with detailed tables and figures
- **Evidence Coverage**: High for bridging paradigm analysis (Tab. 1-8, Fig. 4, 8); High for benchmark comparison (LIBERO Tab. 5, CALVIN Tab. 6); Medium for real-world validation (Fig. 7, 10 trials per task)
- **Confidence**: High on simulation benchmarks (50 trials per subtask, 22 baselines); Medium on real-world generalizability (limited task diversity, single robot)
- **Summary**: 提出 VLA-Adapter，系统分析 VLA 模型中 VL→A 桥接范式的有效性。发现中间层 Raw 特征优于深层（语义偏差）、深层 ActionQuery 最优、多层特征优于单层。提出 Bridge Attention（双交叉注意力+自注意力+可学习注入比例），用 0.5B 骨干在 LIBERO 达 97.3%（接近 OpenVLA-OFT 97.1%/7B），推理 219.2Hz，单卡 8 小时训练。冻结骨干仍达 86.4%。


## Problem

VLA 模型依赖大规模 VLM（如 7B）在大量机器人数据上预训练，导致训练成本高、推理慢、显存消耗大。核心问题：如何有效且高效地将视觉-语言（VL）表征桥接到动作（A）空间？现有桥接范式（Raw features from last/intermediate/all layers vs. ActionQuery）缺乏系统性比较分析，不清楚哪种条件对动作生成最关键。


## Method

### 框架（Fig. 3）
- **输入**：第三人称图像 + 夹爪图像 + 语言指令 + ActionQuery tokens
- **VLM 骨干**：Prismatic VLM 架构，DINOv2 + SigLIP 视觉编码，Qwen2.5-0.5B LLM
- **输出**：每层输出 Raw latent CtR 和 ActionQuery latent CAQt
- **Policy**：L1 损失训练，输入初始动作（全零 H 步）+ 本体感觉，经 M 层 Bridge Attention 输出动作 chunk

### Bridge Attention（Fig. 5, Eq. 1）
- **第一交叉注意力**：CtR → MLP → K1,V1；action latent 为 Q1 → CA1
- **第二交叉注意力**：CAQt + proprio → MLP → K2,V2；action latent 为 Q2 → CA2
- **自注意力**：action latent 自身 Q,K,V → SA
- **拼接**：Ab = [CA1·tanh(g), CA2, SA]，g 初始化为 0，可学习
- **关键设计**：CtR 注入度可学习（tanh(g)），CAQt 全量注入（系数=1）

### 训练
- 端到端训练，Policy 从零训练
- L1 损失：min E[‖πθ(Aτ, CtR, CAQt, σ(P), τ) - At‖₁]
- 4×H100 GPU，8 小时完成（0.5B 骨干）


## Experiments

### 桥接范式分析（Fig. 4, LIBERO-Long）
- 全层 ActionQuery（95%）> 全层 Raw（~93%）> 单层最佳（~90%）
- 中间层 Raw（第 9-13 层）表现最佳（保留多模态细节）
- 深层 ActionQuery 最佳（聚合更丰富的多模态信息）

### LIBERO 基准（Tab. 5, 50 trials/subtask）
| 方法 | 骨干 | Spatial | Object | Goal | Long | Avg |
|------|------|---------|--------|------|------|-----|
| OpenVLA-OFT | 7B | 97.6 | 98.4 | 97.9 | 94.5 | 97.1 |
| π₀ | 3B | 96.8 | 98.8 | 95.8 | 85.2 | 94.2 |
| GR00T N1 | 2B | 94.4 | 97.6 | 93.0 | 90.6 | 93.9 |
| SmolVLA | 2.2B | 93.0 | 94.0 | 91.0 | 77.0 | 88.8 |
| **VLA-Adapter** | **0.5B** | **97.8** | **99.2** | **97.2** | **95.0** | **97.3** |
| VLA-Adapter-Pro | 0.5B | 99.6 | 99.6 | 98.2 | 96.4 | 98.5 |

### CALVIN ABC→D（Tab. 6, 1000 任务序列）
| 方法 | Avg. len |
|------|----------|
| OpenVLA-OFT (7B) | 4.10 |
| OpenHelix (7B) | 4.08 |
| Seer (0.57B) | 3.98 |
| **VLA-Adapter (0.5B)** | **4.42** |
| VLA-Adapter-Pro (0.5B) | 4.50 |

### 效率（Tab. 4）
| 方法 | Throughput | Latency | VRAM (8 batch) |
|------|-----------|---------|----------------|
| OpenVLA | 4.2 Hz | 0.2396 s | 62 GB |
| OpenVLA-OFT | 71.4 Hz | 0.1120 s | 62 GB |
| **VLA-Adapter** | **219.2 Hz** | **0.0365 s** | **24.7 GB** |

### 冻结骨干（Tab. 3, LIBERO-Long）
| 方法 | 成功率 |
|------|--------|
| OpenVLA-OFT (frozen) | 0.0% |
| SmolVLA (frozen) | 77.0% |
| **VLA-Adapter (frozen)** | **86.4%** |

### 真实世界（Fig. 7, Synria Alicia-D 6-DOF）
- 4 类任务：Pick / Move / Stack / Long-horizon
- 每任务 10 次平均
- VLA-Adapter 全面优于 ACT 和 0.5B+OFT

### 消融（Tab. 7-8, Fig. 8）
- ActionQuery 数量：64 最优平衡（Fig. 8）
- 桥接范式：全层 Raw + 全层 ActionQuery 组合最佳（95%，Tab. 7）
- 注入度：CtR 用 tanh(g) + CAQt 用 1.0 最优（95%，Tab. 8）


## Limitations

1. **真实世界泛化有限**：0.5B 骨干未在大规模具身数据上预训练，真实世界泛化能力需提升。作者在 Limitations 章节明确承认此问题。
2. **仅仿真基准全面评估**：LIBERO 和 CALVIN 是仿真基准，真实世界仅 4 类任务 × 10 次试验，无统计显著性分析。
3. **条件质量依赖 VLM**：动作生成质量取决于 VLM 提供的条件质量和使用方式，未分析不同 VLM 骨干对条件的敏感度。
4. **训练流程简单**：仅用 L1 损失端到端训练，未探索 RL、课程学习等更复杂的训练策略。
5. **骨干可扩展性未充分验证**：7B 骨干（LLaMA2 + OpenVLA）的提升有限（95.4% vs 95.0%），但未测试更大的骨干（如 14B、72B）。
6. **ActionQuery 数量选择需调优**：64 tokens 是在 LIBERO-Long 上调优的，不同任务可能需要不同数量。


## Key Takeaways

1. **桥接范式是 VLA 设计的关键变量**：中间层 Raw 特征保留更多空间细节（对操控重要），深层 ActionQuery 聚合更丰富的多模态语义。两者结合（Bridge Attention）效果最佳。
2. **0.5B VLA 可匹敌 7B**：VLA-Adapter 的 97.3% 与 OpenVLA-OFT 的 97.1% 相当，且推理速度快 3 倍，显存仅需 40%。这挑战了"VLA 必须依赖大模型"的共识。
3. **与 [[ma2025running]]（Running VLAs）互补**：Ma et al. 用 CUDA Graph + Triton kernel 优化推理至 30FPS，VLA-Adapter 通过架构轻量化实现 219.2Hz。两种路径可叠加：轻量架构 + 编译优化。
4. **冻结骨干 + Bridge Attention 是实用部署路径**：86.4% 成功率（冻结）意味着可将 VLM 作为固定特征提取器，仅训练 97M Policy，大幅降低部署门槛。
5. **对本研究方向的启示**：VLA-Adapter 的 Bridge Attention 设计可用于双臂 DLO 操控——将 DLO 状态（关键点/拓扑特征）作为额外条件注入 Policy，实现视觉-语言-DLO 状态三模态桥接。

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wang-yihao|Wang, Yihao]]
- [[ding|Ding, Pengxiang]]
