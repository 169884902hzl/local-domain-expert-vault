---
title: "AR-VLA: True autoregressive action expert for vision-language-action models"
tags: [manipulation, imitation, VLM, diffusion]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出独立的自回归 Action Expert，通过 Hybrid KV Cache 维护滚动运动历史和可刷新视觉-语言前缀，配合 Dynamic Temporal Re-anchoring 解决感知-控制异步对齐问题，在通用和专用策略上均超越或匹配现有最优 VLA。"
authors: "Hu, Yutong; Zaech, Jan-Nico; Nikolov, Nikolay; Yao, Yuanqi; Dey, Sombit et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VZMVQUW5"
---
## 摘要

We propose a standalone autoregressive (AR) Action Expert that generates actions as a continuous causal sequence while conditioning on refreshable vision-language prefixes. In contrast to existing Vision-Language-Action (VLA) models and diffusion（扩散） policies that reset temporal context with each new observation and predict actions reactively, our Action Expert maintains its own history through a long-lived memory and is inherently context-aware. This structure addresses the frequency mismatch between fast control and slow reasoning, enabling efficient independent pretraining（预训练） of kinematic syntax and modular integration with heavy perception backbones, naturally ensuring spatio-temporally consistent action generation across frames. To synchronize these asynchronous hybrid V-L-A modalities, we utilize a re-anchoring mechanism that mathematically accounts for perception staleness during both training and inference. Experiments on simulated and real-robot manipulation（机器人操控） tasks demonstrate that the proposed method can effectively replace traditional chunk-based action heads for both specialist and generalist policies. AR-VLA exhibits superior history awareness and substantially smoother action trajectories while maintaining or exceeding the task success rates of state-of-the-art（现有最优方法） reactive VLAs. Overall, our work introduces a scalable, context-aware action generation schema that provides a robust structural foundation for training effective robotic policies. Code and Videos available at https://arvla.insait.ai

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型

## 关键贡献

1. **自回归 Action Expert 范式**：将动作生成建模为因果序列问题（而非独立快照），使策略具备固有的时序感知能力
2. **Hybrid Key-Value (HKV) Cache**：双流缓存架构——本体感觉流为滚动 FIFO、视觉-语言流为单槽可刷新缓冲区，实现感知与控制的结构化解耦
3. **Dynamic Temporal Re-anchoring (DTR)**：基于 RoPE 的位置编码机制，将静态 VLM 特征映射到动态动作时间线，数学上保证训练-推理的时间偏移不变性
4. **两阶段训练**：Phase 1 纯动作预训练学习运动语法，Phase 2 跨模态对齐接地到视觉感知，配合随机历史 Dropout 防止因果混淆
5. **异步双线程推理**：Action Thread 高频运行（29ms/step），Perception Thread 按自身频率刷新，控制频率不依赖特定视觉帧
## 结构化提取

- Problem: 现有 VLA/Diffusion Policy 采用反应式范式，每步丢弃时序上下文，导致动作抖动、缺乏历史意识、无法处理长视野非 Markov 任务
- Method: 独立自回归 Action Expert + Hybrid KV Cache（滚动本体感觉 FIFO + 可刷新 VL 前缀）+ Dynamic Temporal Re-anchoring（RoPE 位置编码解决异步对齐）+ 两阶段训练（纯动作预训练 → VL 对齐）
- Tasks: SimplerEnv 四项 WidowX 操控任务（通用策略）、真实 WidowX 零样本评估、PushT、ALOHA cube transfer、ALOHA peg insertion（专用策略）、PushT2（仿真历史意识）、Stack3（真实历史意识）
- Sensors: 单目外部相机（通用）、单目相机 + 本体感觉状态（专用）
- Robot Setup: WidowX 机器人臂（6-DOF，末端执行器控制），ALOHA 双臂系统（joint velocity 控制），PushT 2D 平面推动
- Metrics: 成功率（%）、Max IoU、Jerk（平滑度）、推理延迟（ms/step）
- Limitations: AR 复合误差导致 OOD 失败、需要 knowledge isolation 保护 VLM、视觉处理仍为快照式未实现流式 VLM、未在精细形变操控上评估
- Evidence Notes: 完整全文证据，包括方法定义（Def.1/2）、公式推导、SimplerEnv 四任务成功率表格、真实 WidowX 零样本对比、专用策略三任务对比、PushT2/Stack3 历史意识实验、四组消融实验、附录架构细节和超参数
## 本地引用关系

- [[hu2026arvla]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖摘要、方法、实验、消融、附录
- Confidence: high
- Summary: 提出独立的自回归 Action Expert，通过 Hybrid KV Cache 维护滚动运动历史和可刷新视觉-语言前缀，配合 Dynamic Temporal Re-anchoring 解决感知-控制异步对齐问题，在通用和专用策略上均超越或匹配现有最优 VLA。


## Problem

现有 VLA 模型（OpenVLA、π₀、Diffusion Policy 等）本质上是"反应式"策略：每个时间步重新编码视觉上下文并预测动作，丢弃时序连续性。这种"Markovian 失忆"导致：(1) 动作轨迹抖动、不平滑；(2) 长视野任务中缺乏历史意识，无法恢复丢失的中间状态；(3) 高频控制与低频感知之间的频率不匹配问题未得到结构化解决。


## Method

### 核心架构
AR-VLA 由 PaliGemma-3B VLM 骨干 + 300M Action Expert 组成。

**问题建模**：
- Reactive Actor（定义1）：$P_{\text{react}}(\tau) = \prod_{t=1}^{T} P(a_t | \Phi(v_t, l), s_t)$ — 每步重置上下文
- AR Actor（定义2）：$P_{\text{ar}}(\tau) = \prod_{t=1}^{T} P(a_t | \underbrace{\Phi(v_i, l)}_{\text{VL Prefix}}, \underbrace{a_{<t}, s_{<t}}_{\text{Kinematic History}})$ — 维护连续因果链

**Hybrid KV Cache**：
- $KV^X$：本体感觉流的 token-wise 滚动 FIFO，保存历史状态和动作
- $KV^{VL}$：视觉-语言流的 block-wise 单槽缓冲区，新帧到来时整体替换

**DTR 机制**：
- 利用 RoPE 的旋转矩阵 $\bm{R}(n)$ 编码位置
- 动作 token 按机器人因果时间线赋序号 $n$
- VL token 按图像捕获时刻赋序号 $n$
- 关键性质：$\text{Score}(q_{m+T}, k^{VL}_{n+T}) = \text{Score}(q_m, k^{VL}_n)$，即全局时间平移不变性
- 训练时短序列（如 $m=25, n=20, \Delta t=5$）学到的视觉接地逻辑，可直接迁移到推理时的长序列（如 $m=500, n=495$）

**训练协议**：
- Phase 1：$\mathcal{L}_{\text{Phase1}} = \sum_{t=1}^{T} \mathcal{L}(x_t | x_{<t})$，纯动作序列建模
- Phase 2：随机历史 Dropout $\mathcal{M}_k \in \{0,1\}^H$，以 0.6 掩码率随机遮蔽历史，防止模型过度依赖自身预测
- Knowledge insulation：VLM 参数仅通过 Fast Token 辅助损失更新，动作梯度不回传到 VLM


## Experiments

### 通用策略（Generalist）
**数据集**：BridgeV2 训练，SimplerEnv 仿真 + 真实 WidowX 评估

**SimplerEnv 仿真结果**（成功率%）：

| 模型 | spoon→towel | carrot→plate | stack blocks | eggplant→basket | 平均 |
|------|------------|-------------|-------------|----------------|------|
| OpenVLA | - | - | - | - | 较低 |
| Octo-Base | - | - | - | - | 较低 |
| Pi-0-FAST* | 62.5 | 29.2 | - | - | 49.0 |
| Pi-0.5* | 58.3 | 33.3 | - | - | 51.0 |
| CogACT | - | - | - | - | 52.1 |
| **AR-VLA** | **75.0** | **54.2** | - | - | **61.5** |

- AR-VLA 平均 61.5%，比第二名 CogACT 高 +9.4%
- 同骨干同参数量（3B+300M）下大幅超越 Pi-0-FAST*（49.0%）和 Pi-0.5*（51.0%）

**真实 WidowX 零样本**：AR-VLA 平均 89% 成功率，在 "cup on plate" 和 "Lobster" 任务上达到 100%。失败后能优雅地提升末端执行器重试，而基线方法常在目标附近表现出混乱运动。

### 专用策略（Specialist）
**任务**：PushT、ALOHA cube transfer、ALOHA peg insertion

| 模型 | PushT 成功率 | PushT Max IoU | ALOHA cube (scripted) | ALOHA cube (human) | ALOHA peg (scripted) |
|------|------------|--------------|----------------------|--------------------|--------------------|
| ACT | - | - | 86.0% | 50.0% | 32.0% |
| DP | **65.2%** | - | 33.3% | 10.0% | - |
| **AR Actor** | 60.4% | 0.920 | **97.3%** | **67.3%** | **54.7%** |

- AR Actor 在 ALOHA 双臂任务上大幅领先（cube +11.3%/+17.3%，peg +22.7% vs ACT）
- PushT 上略逊于 DP 但差距很小，且 Max IoU 高（0.920）
- 跨任务性能一致性显著优于 DP（DP 在 PushT 强但 ALOHA cube 崩溃）

### 平滑性与效率
- AR-VLA：29ms/step 控制延迟（VLM 70ms/帧）
- 最大/平均 Jerk 均为最低，轨迹显著平滑
- 异步执行保证控制频率稳定

### 历史意识评估
- **PushT2**（仿真）：需将 T 形块推到两个目标位置，中途目标可达信息不可观察 → AR-VLA 大幅超越所有基线
- **Stack3**（真实）：用杯子盖住电池后堆叠第二个杯子，电池位置被遮挡 → AR-VLA 依赖动作历史成功完成
- Reactive 策略出现"时间失忆"，在子目标间振荡

### 消融实验
- **因果预训练**：去掉 Phase 1 → Phase 2 收敛慢 2×，最终性能下降
- **RoPE 重锚定**：去掉 → 推理性能严重退化；完全去掉位置编码 → 52% 性能下降
- **历史掩码率**：0.0 → 验证误差最低但成功率 0%（过度依赖历史，rollout 时失败）；0.6 最优平衡
- **上下文长度**：1→40 步，成功率随上下文增加单调上升


## Limitations

1. **复合误差与 OOD 状态**：AR 模型依赖自身预测，错误可能编码进 KV cache 形成恶性反馈循环；历史 Dropout 只部分缓解
2. **梯度与知识隔离**：AR 动作梯度直接反传到 VLM 会损害语义能力，需要 knowledge insulation 策略，但目前缺少真正协同的联合训练目标
3. **视觉处理仍为快照式**：本体感觉历史有缓存，但视觉处理仍受限于标准快照方式，尚未实现"流式 VLM"
4. **集成 vs 模块化自回归**：当前 Action Expert 是独立模块，理论上 LLM 部分可直接建模动作序列，但本工作未探索
5. 未在 DLO 操控等需要精细形变感知的任务上评估


## Key Takeaways

1. **动作生成应当是因果序列问题**：将动作视为"运动语言"比 chunk-based 快照方式更能保证时空一致性和长视野稳定性
2. **感知-控制解耦的工程价值**：HKV Cache + DTR 实现了高频控制线程独立于低频感知线程运行，这对实时机器人系统至关重要
3. **RoPE 的训练-推理迁移技巧**：DTR 利用 RoPE 的平移不变性解决了短上下文训练→长上下文推理的分布外问题，这一技巧可泛化到其他异步多流架构
4. **历史掩码率的关键发现**：0% 掩码率验证误差最低但成功率 0%，揭示了自回归策略的"因果混淆悖论"——模型必须学会在历史不可靠时依赖视觉前缀
5. **对 DLO 操控的启发**：DLO 操控中时序一致性和平滑轨迹尤为重要（避免突然抖动导致线缆弹出），AR 模式天然适合此类需要连续运动控制的任务

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[hu|Hu, Yutong]]
- [[zaech|Zaech, Jan-Nico]]
- [[nikolov|Nikolov, Nikolay]]
