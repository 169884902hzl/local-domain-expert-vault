---
title: "HiF-VLA: Hindsight, insight and foresight through motion representation for vision-language-action models"
tags: [manipulation, imitation, VLM, DLO]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "HiF-VLA 利用 MPEG-4 运动向量作为紧凑时序表示，通过后视先验编码、前视推理和后视调制联合专家实现双向时序推理，在 LIBERO-Long（96.4%）和 CALVIN ABC-D（4.35）上达到 SOTA，推理延迟仅增加 1.67×。"
authors: "Lin, Minghui; Ding, Pengxiang; Wang, Shu; Zhuang, Zifeng; Liu, Yang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "BD5PIZUK"
---
## 摘要

Vision-Language-Action (VLA) models have recently enabled robotic manipulation（机器人操控） by grounding visual and linguistic cues into actions. However, most VLAs assume the Markov property, relying only on the current observation and thus suffering from temporal myopia that degrades long-horizon（长时序） coherence. In this work, we view motion as a more compact and informative representation of temporal context and world dynamics, capturing inter-state changes while filtering static pixel-level noise. From this perspective, HiF-VLA equips a motion-centric world model for the VLA, enabling agents to reason about temporal dynamics for future evolution during action generation. Building on this idea, we propose HiF-VLA (Hindsight, Insight, and Foresight for VLAs), a unified framework that leverages motion for bidirectional temporal reasoning. HiF-VLA encodes past dynamics through hindsight priors, anticipates future motion via foresight reasoning, and integrates both through a hindsight-modulated joint expert to enable a ''think-while-acting'' paradigm for long-horizon（长时序） manipulation（操控）. As a result, HiF-VLA surpasses strong baselines on LIBERO-Long and CALVIN ABC-D benchmarks, while incurring negligible additional inference latency. Furthermore, HiF-VLA achieves substantial improvements in real-world long-horizon（长时序） manipulation（操控） tasks, demonstrating its broad effectiveness in practical robotic settings.

## 中文简述

提出基于视觉-语言的绳索操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、可变形物体操控

## 关键贡献

1. **HiF-VLA 框架**：首次在 VLA 中引入双向时序推理（后视 + 前视），使用 MPEG-4 运动向量作为结构化低维时序基元，显式扩展时序感受野，同时大幅减少冗余
2. **后视调制联合专家（Hindsight-Modulated Joint Expert）**：在共享时序潜在空间中联合建模动作和运动，通过 AdaLN 条件注入历史信息，实现"边思考边行动"（think-while-acting）范式
3. **全面验证**：在 LIBERO-Long（94.4%/96.4%）、CALVIN ABC-D（4.08/4.35）上超越强 baseline，推理延迟仅增加 1.67×，在真实 AgileX Piper 机器人上取得显著改进
## 结构化提取

- Problem: VLA 模型因马尔可夫假设导致时序近视，在长时序操控中动作连贯性差；现有帧堆叠和子目标预测方案存在高冗余和高延迟
- Method: HiF-VLA——基于 MPEG-4 运动向量的双向时序推理框架，包含后视先验获取（ViT+3D conv 编码器）、前视推理（VLM 并行预测运动和动作 token）、后视调制联合专家（AdaLN 条件注入 + 跨流联合注意力）
- Tasks: 长时序桌面操控（物体拾取放置、堆叠、按钮按压、锅具放置等），包含 LIBERO-Long 10 任务、CALVIN ABC-D、3 个真实世界长时序任务
- Sensors: 第三人称视角 RGB 相机（RealSense D435）、腕部 USB 相机（多视角设置）
- Robot Setup: 仿真：LIBERO（Franka Panda）、CALVIN（Franka Panda）；真实世界：AgileX Piper（6-DoF + 1-DoF gripper），RTX 4090 推理
- Metrics: 成功率（Success Rate, %）、平均任务长度（Avg. Len., CALVIN）、推理延迟（ms）、GPU 峰值显存（GB）
- Limitations: 运动向量在高度动态场景中对噪声敏感；缺乏大规模视频预训练；3D 感知不足（深度/空间判断失败）；长前视预测误差累积；仅验证刚性物体
- Evidence Notes:

  - LIBERO-Long 第三视角 94.4%（+3.4% over OpenVLA-OFT），多视角 96.4%（+2.4%）
  - CALVIN ABC-D 第三视角 Avg. Len. 4.08（+0.28 over UniVLA），多视角 4.35（+0.07 over Seer）
  - 效率：仅 1.05× 显存、1.67× 延迟（vs 帧堆叠的 2.06×/3.15×）
  - 消融证明：MVs > 关节状态（+2.4%），双向注意力 > 因果（+7.0%），Expert 注入 > VLM 输入
  - 真实世界：Press-Buttons-Order 从 17.4% 大幅改善，时序感受野有效检测细微状态变化
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 版本获取完整论文内容）
- Evidence Coverage: 完整覆盖摘要、方法、实验（含 supplementary）、消融实验、真实世界实验和失败案例分析
- Confidence: high
- Summary: HiF-VLA 利用 MPEG-4 运动向量作为紧凑时序表示，通过后视先验编码、前视推理和后视调制联合专家实现双向时序推理，在 LIBERO-Long（96.4%）和 CALVIN ABC-D（4.35）上达到 SOTA，推理延迟仅增加 1.67×。


## Problem

大多数 VLA 模型假设马尔可夫性，仅依赖当前观测进行动作预测，导致**时序近视**（temporal myopia）：在长时序操控任务中，动作间的时序依赖关系退化，轨迹碎片化，任务级一致性下降。现有缓解方案（帧堆叠、子目标预测）存在根本性缺陷：

1. **帧堆叠**：引入大量像素级冗余，计算开销线性增长（8 帧时延迟达 4.5×），且静态信息掩盖任务相关动态
2. **子目标预测**：像素级未来预测容易产生局部失真和语义漂移，且缺乏连续时序建模

论文提出核心洞察：**运动（motion）** 而非原始像素，是时序上下文和世界动态的更紧凑、更高效表示。


## Method

### 整体架构

HiF-VLA 基于 OpenVLA（Prismatic-7B 骨干），扩展为三组件双向时序推理框架：

### 1. 后视先验获取（Hindsight Prior Acquisition）

- 使用 **MPEG-4 运动向量（MVs）** 编码历史动态：按 16×16 宏块布局提取帧间位移，形成 `h × (H/16) × (W/16) × 2` 的紧凑张量
- 构造 GOP（Group of Pictures）单元：`[MV_{t-m:t-m+1}, ..., MV_{t-1:t}, o_t]`
- 通过 **轻量 ViT + 3D 卷积** 编码器将运动序列压缩为后视 token `M_h ∈ R^{K_h × d}`
- 相比原始帧，MVs 保留任务相关动态同时丢弃静态冗余

### 2. 前视推理与洞察（Foresight Reasoning with Insight）

- 引入 `K_f` 个可学习前视查询 token 和 `K_a` 个空动作 token
- 这些 token 与指令嵌入、当前观测嵌入拼接后送入 VLM `F_θ`
- VLM 通过非因果注意力掩码**并行**生成前视运动 token `M_f` 和动作 token `A_f`
- 不预测原始未来像素，而是预测结构化运动向量作为未来视觉动态的紧凑目标

### 3. 后视调制联合专家（Hindsight-Modulated Joint Expert）

- 核心设计：历史运动不直接注入 VLM 输入（会干扰预训练视觉-语言对齐），而是通过 **AdaLN 条件注入** 到解码阶段
- 前视运动 token 和动作 token 形成两个并行流，通过**跨流联合注意力**交互，但保留独立 FFN
- 历史后视 token `M_h` 通过线性层投影为条件向量 `h_c`，通过 AdaLN 调制前视和动作表示：
  - `AdaLN(z; h_c) = γ(h_c) · (z - μ(z)) / σ(z) + β(h_c)`
- 联合专家由 6 层 Transformer 组成，使用 RoPE 位置编码

### 训练目标

- 双 L1 损失：`L_all = L_A + λ · L_MV`，λ = 0.01
- 训练配置：8×A100 GPU，batch size 64，chunk size n=8，hindsight 窗口默认 8


## Experiments

### LIBERO-Long（10 个多子目标任务）

| 设置 | HiF-VLA | 最强 Baseline | 提升 |
|------|---------|-------------|------|
| 第三视角 | **94.4%** | OpenVLA-OFT 91.0% | +3.4% |
| 多视角 | **96.4%** | OpenVLA-OFT 94.0% | +2.4% |

- 在 Put both pots on stove（最难任务）上从 72% 提升到 82%（多视角）
- 第三视角表现接近其他方法的多视角表现

### CALVIN ABC-D（ABC 训练，D 评估）

| 设置 | HiF-VLA Avg. Len | 最强 Baseline |
|------|-----------------|-------------|
| 第三视角 | **4.08** | UniVLA 3.80 |
| 多视角 | **4.35** | Seer 4.28 |

### LIBERO 全四套件综合

- HiF-VLA 平均 **98.0%**，超越 MemoryVLA（96.5%）、OpenVLA-OFT（97.1%）

### 效率分析（LIBERO-Long）

| 方法 | GPU 显存 | 推理延迟 | 成功率 |
|------|---------|---------|-------|
| Baseline | 30.8 GB (1.00×) | 72.9 ms (1.00×) | 91.0% |
| + History Frames | 63.6 GB (2.06×) | 229.5 ms (3.15×) | 90.4% |
| **HiF-VLA (Ours)** | **32.2 GB (1.05×)** | **121.6 ms (1.67×)** | **93.2%** |

- 帧堆叠反而降低性能（冗余像素信息冲淡任务相关时序线索）
- HiF-VLA 仅增加 5% 显存和 67% 延迟

### 消融实验关键发现

1. **MVs vs 机器人本体状态**：替换为关节状态（S+S）导致 94.4% → 92.0%，证明 MVs 捕获了交互驱动的视觉动态而非仅机械臂运动
2. **MVs vs 光流**：性能相当（94.4% vs 94.2%），但 MVs 推理延迟低 78%
3. **双向注意力 > 因果分离**：94.4% vs 87.4%，跨流交互至关重要
4. **Expert 条件注入 > VLM 输入拼接**：运动信息直接注入解码阶段更有效，避免干扰 VLM 的预训练视觉-语言对齐
5. **最优超参**：λ=0.01，Joint Expert 深度=6，hindsight/foresight 长度=8/8

### 真实世界实验

- 平台：AgileX Piper（6-DoF + 1-DoF gripper），RealSense D435 + USB 腕部摄像头，RTX 4090
- 3 个长时序任务，每任务 100 次示范训练，20 次试验评估
- HiF-VLA 在 Press-Buttons-Order 上从 OpenVLA-OFT 的 17.4% 大幅提升（利用宽时序感受野检测细微状态转换）


## Limitations

1. **运动向量估计精度受限**：在高度动态场景中对噪声敏感，MPEG-4 MVs 依赖视频编解码器质量
2. **缺乏大规模视频预训练**：未在互联网规模视频上预训练运动理解和生成能力
3. **3D 感知不足**：失败案例表明空间几何和深度估计是瓶颈（过早松手、提升高度不足、深度估计错误导致按压失败）
4. **长前视预测误差累积**：foresight 长度从 8 增至 16 时性能下降（94.6%），表明长程运动预测仍有挑战
5. 仅在刚性物体操控任务上验证，未涉及可变形物体


## Key Takeaways

1. **运动向量作为时序基元**：从视频编解码借鉴的 MVs 是 VLA 时序建模的高效选择，比光流计算成本低得多但信息量相当——这对 DLO 操控有启发：DLO 的形变运动可能也可用类似紧凑表示编码
2. **双向时序推理范式**：后视（历史动态）+ 前视（未来预测）的联合推理比单向历史堆叠或子目标预测更有效，特别是需要跨步骤因果一致性的长时序任务
3. **条件注入优于直接拼接**：历史信息通过 AdaLN 注入解码阶段优于直接拼入 VLM 输入——这一设计原则可迁移到其他需要引入辅助信息的 VLA 架构
4. **对 DLO 操控的启示**：DLO 操控天然是长时序任务，且状态变化（如绳子弯曲、打结）细微但关键，HiF-VLA 的宽时序感受野和运动感知可能有助于检测 DLO 的细微形变状态

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[lin|Lin, Minghui]]
- [[ding|Ding, Pengxiang]]
